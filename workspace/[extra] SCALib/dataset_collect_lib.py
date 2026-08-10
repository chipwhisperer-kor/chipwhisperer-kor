"""[extra] SCALib 파형 수집 공용 로직.

0.0 (tiny-AES-c) 과 0.1 (masked-aes-c) 노트북이 같은 연결·캡처·저장 절차를 쓴다.
정의는 여기 한 곳, 노트북은 타겟 상수·내러티브·호출만 담당한다.

마스크 회수: capture_one(..., with_masks=True) 일 때 0x83 'm' 으로 10바이트를 읽는다.
호출은 반드시 trigger_low 이후(암호화 명령이 끝난 뒤)이므로 파형에 UART 가 섞이지 않는다.

장시간 수집은 중간에 깨진다. 그래서 캡처는 항상 Bench.capture() 로 하며, 실패하면
단순 재시도 → 재연결 → Husky 펌웨어 재기록 순으로 스스로 복구한다(Bench 참고).
사람이 지켜보다 다시 눌러 줄 필요가 없어야 한다.
"""

from __future__ import annotations

import datetime
import os
import stat
import subprocess
import sys
import time
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
try:
    from tqdm.notebook import trange
except Exception:  # 스크립트/비노트북 환경
    from tqdm import trange

import chipwhisperer as cw

from scalib_common import (
    AES_BLOCK,
    BATCH,
    MASK_LEN,
    N_ATTACK,
    N_EXPLORE,
    N_PROFILING,
    N_TVLA,
    SCHEMA,
    SCHEMA_VERSION,
    SEED,
    SUBSET_ROLE_MAP,
    F_CIPHERTEXT,
    F_KEY,
    F_MASK,
    F_PLAINTEXT,
    F_TRACE,
    validate_dataset,
)
# 골든 모델은 저장소 공용 정의를 쓴다. 수집기와 분석기가 서로 다른 참조 구현을 쓰면
# "타겟이 틀렸다" 와 "참조가 틀렸다" 를 구분할 수 없게 된다.
# (scalib_common 이 workspace/lib 를 sys.path 에 넣어 주므로 여기서는 그냥 import 한다)
from aes_ref import aes_ecb_encrypt

# 노트북이 재export 할 수 있도록 재노출
__all__ = [
    "my_fsr_cmd",
    "aes_ecb_encrypt",
    "target_aes_encrypt",
    "target_get_masks",
    "mask_seed_for",
    "set_mask_seed",
    "open_scope",
    "connect_all_devices",
    "build_firmware",
    "flash_firmware",
    "setup_husky",
    "measure_trig_count",
    "apply_trig_count",
    "to_adc_code",
    "capture_one",
    "capture_retry",
    "Bench",
    "reflash_husky_firmware",
    "collect_group",
    "run_full_collect",
    "resume_group",
    "run_resume",
    "disconnect_all",
    "GROUP_TARGETS",
    "GROUP_MODES",
    "write_root_metadata",
]


GROUP_TARGETS = {
    "explore": N_EXPLORE,
    "attack": N_ATTACK,
    "tvla_rk": N_TVLA,
    "tvla_fk": N_TVLA,
    "profiling": N_PROFILING,
}

GROUP_MODES = {
    "explore": ("random", "random", SEED + 1),
    "attack": ("fixed", "random", SEED + 2),
    "tvla_rk": ("random", "fixed", SEED + 3),
    "tvla_fk": ("fixed", "fixed", SEED + 4),
    "profiling": ("random", "random", SEED + 5),
}


def my_fsr_cmd(target, cmd, scmd, data, payload_only=False, timeout=500):
    """SimpleSerial2 명령 한 번을 보내고 응답을 읽는다.

    payload_only=True 면 응답 패킷에서 데이터 부분만 잘라 돌려준다.
    응답이 없으면 None.
    """
    target.flush()
    target.send_cmd(cmd=cmd, scmd=ord(scmd), data=data)
    response = target.read_cmd(timeout=timeout)
    if response is None:
        return None
    if payload_only:
        return response[3 : 3 + response[2]]
    return response


def target_aes_encrypt(target, key16, plain16):
    """타겟에서 AES-128 ECB 한 블록을 계산하고 암호문을 돌려준다.

    0x81 k/p/l → 0x82 c → 0x83 r. 'l' 은 매 회 보낸다.
    """
    key16 = bytearray(key16)
    plain16 = bytearray(plain16)
    if len(key16) != AES_BLOCK or len(plain16) != AES_BLOCK:
        raise ValueError("key/plain 길이는 16이어야 한다.")

    my_fsr_cmd(target, 0x81, "k", key16)
    my_fsr_cmd(target, 0x81, "p", plain16)
    my_fsr_cmd(target, 0x81, "l", bytearray([AES_BLOCK]))
    my_fsr_cmd(target, 0x82, "c", [])
    ct = my_fsr_cmd(target, 0x83, "r", [], payload_only=True)
    if ct is None:
        raise RuntimeError("타겟 응답 없음 (통신 실패)")
    return bytes(ct)


def target_get_masks(target):
    """마지막 암호화에 쓰인 마스크 10바이트 (0x83 'm').

    트리거 구간 밖에서 호출한다. 펌웨어 simpleserial_masked-aes-c 전용.
    """
    m = my_fsr_cmd(target, 0x83, "m", [], payload_only=True)
    if m is None or len(m) != MASK_LEN:
        raise RuntimeError(
            "마스크 회수 실패 (len=%s). masked 펌웨어·0x83 'm' 을 확인한다."
            % (None if m is None else len(m)))
    return bytes(m)


def mask_seed_for(group_name, round_idx):
    """그룹·라운드마다 쓸 마스크 시드. SEED 로부터 결정적으로 파생한다.

    재현 가능해야 하므로 난수가 아니고, 재접속·재플래시마다 달라져야 하므로
    라운드 번호를, 그룹끼리 겹치지 않도록 그룹 이름을 섞는다.
    값 자체에 암호학적 의미는 없다 — 목적은 "같은 수열의 재생 방지" 뿐이다.
    """
    h = 0
    for ch in group_name:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return (SEED * 1000003 + h * 40503 + int(round_idx) * 2654435761) & 0xFFFFFFFF


def _seed_masks(target, group_dset, group_name):
    """with_masks 수집 직전에 새 마스크 시드를 심고 그룹 attrs 에 남긴다.

    라운드 번호는 프로세스 변수가 아니라 **그룹 attrs 에 이미 쌓인 시드 개수**에서
    센다. 이어받기 스크립트를 껐다 켜도 번호가 되감기지 않아야 하기 때문이다
    (프로세스 카운터로 하면 재실행 때마다 1번 시드로 돌아가 결함이 그대로 재현된다).
    """
    prev = [int(s) for s in group_dset.attrs.get("mask_seeds", [])]
    seed = mask_seed_for(group_name, len(prev) + 1)
    set_mask_seed(target, seed)
    group_dset.attrs["mask_seeds"] = np.array(prev + [seed], dtype=np.uint32)
    print("    마스크 시드 0x%08x (/%s round %d)"
          % (seed, group_name, len(prev) + 1))
    return seed


def set_mask_seed(target, seed):
    """Masked 펌웨어의 rand() 시드를 지정한다 (0x81 's', 4바이트 LE).

    **연결·재플래시 직후 반드시 호출한다.** 타겟은 스스로 엔트로피를 만들지 못해
    부팅 시드가 매번 같다. 이 호출을 빠뜨리면 재시작할 때마다 같은 마스크 수열이
    처음부터 재생되고, 그렇게 모은 파형은 마스크가 중복되어 분석에 쓸 수 없다.

    Normal(tiny-AES-c) 펌웨어에는 없는 명령이다. 호출하면 응답이 없다.

    반환: 타겟이 에코한 시드 4바이트. 불일치면 RuntimeError.
    """
    seed = int(seed) & 0xFFFFFFFF
    data = bytearray(seed.to_bytes(4, "little"))
    echo = my_fsr_cmd(target, 0x81, "s", data, payload_only=True)
    if echo is None or bytes(echo) != bytes(data):
        raise RuntimeError(
            "마스크 시드 설정 실패 (echo=%r). masked 펌웨어와 0x81 's' 를 확인한다."
            % (None if echo is None else bytes(echo)))
    return bytes(echo)


def open_scope(sn, name, tries=4, pause=3.0):
    """장치 하나를 연다. 실패하면 쉬었다가 재시도."""
    last = None
    for attempt in range(1, tries + 1):
        try:
            s = cw.scope(sn=sn)
            if attempt > 1:
                print("       (%d회째 시도에서 성공)" % attempt)
            return s
        except Exception as e:
            last = e
            if attempt < tries:
                print("  [재시도 %d/%d] %s — %s" % (attempt, tries, name, str(e)[:60]))
                time.sleep(pause)
    raise RuntimeError("%s 연결 실패 (%d회 시도): %s" % (name, tries, last))


def connect_all_devices(required=("ChipWhisperer_Lite", "ChipWhisperer_Husky"), tries=4):
    """USB 의 ChipWhisperer 를 모두 열어 {이름: scope} 로 돌려준다."""
    device_list = []
    for attempt in range(1, tries + 1):
        device_list = cw.list_devices()
        if device_list:
            break
        print("  [재시도 %d/%d] 장치가 아직 보이지 않는다" % (attempt, tries))
        time.sleep(3.0)
    if not device_list:
        raise RuntimeError(
            "연결된 ChipWhisperer 장치가 없다.\n"
            "  - USB 케이블과 전원을 확인한다\n"
            "  - 호스트에서 `lsusb | grep 2b3e` 로 장치가 보이는지 본다\n"
            "  - 컨테이너가 privileged 로 /dev/bus/usb 를 매핑하고 있는지 확인한다")

    print("발견된 장치 수:", len(device_list))
    scopes = {}
    for device in device_list:
        name = device["name"].replace("-", "_")
        scopes[name] = open_scope(device["sn"], name, tries=tries)
        print("  [OK]", name, " (SN:", device["sn"], ")")

    missing = [n for n in required if n not in scopes]
    if missing:
        raise RuntimeError(
            "필요한 장치를 열지 못했다: %s\n"
            "  열린 장치: %s\n"
            "  Lite(통신·플래시)와 Husky(관측)가 모두 필요하다."
            % (missing, list(scopes)))
    return scopes


def build_firmware(ss_dir, platform, crypto_target, ss_ver, hex_path):
    if not Path(ss_dir).is_dir():
        raise FileNotFoundError("펌웨어 폴더가 없다: %s" % ss_dir)
    cmd = ["make", "PLATFORM=%s" % platform,
           "CRYPTO_TARGET=%s" % crypto_target, "SS_VER=%s" % ss_ver]
    print("빌드:", " ".join(cmd), "cwd=", ss_dir)
    r = subprocess.run(cmd, cwd=str(ss_dir), capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        raise RuntimeError("펌웨어 빌드 실패")
    if not Path(hex_path).is_file():
        raise FileNotFoundError("hex 없음: %s" % hex_path)
    print("[OK] 빌드 완료:", hex_path)


def flash_firmware(lite_scope, platform, hex_path):
    if "STM" not in platform and platform not in ("CWLITEARM", "CWNANO"):
        raise OSError("지원하지 않는 PLATFORM: %s" % platform)
    prog = cw.programmers.STM32FProgrammer
    lite_scope.default_setup()
    cw.program_target(lite_scope, prog, str(hex_path))
    print("[OK] 플래시 완료")


def setup_husky(husky_scope, adc_mul, gain_db):
    """Husky 외부 클럭·트리거·게인. samples 는 아직 정하지 않는다.

    반환: clk_hz (타겟 클럭 최빈값 Hz)
    """
    husky_scope.default_setup()
    time.sleep(0.5)

    husky_scope.clock.clkgen_freq = 0
    husky_scope.clock.reset_adc()
    husky_scope.io.aux_io_mcx = "high_z"
    husky_scope.clock.clkgen_src = "extclk_aux_io"
    husky_scope.clock.reset_adc()
    print("aux_io_mcx   =", husky_scope.io.aux_io_mcx)
    print("clkgen_src   =", husky_scope.clock.clkgen_src)

    husky_scope.clock.pll._allow_rdiv = True
    husky_scope.clock.freq_ctr_src = "extclk"
    time.sleep(0.5)

    freqs = []
    for _ in range(20):
        freqs.append(husky_scope.clock.freq_ctr)
        time.sleep(0.2)
    clk_hz = float(pd.Series(freqs).mode().iloc[0])
    print("외부 클럭 최빈값 ≈ %.0f Hz" % clk_hz)

    husky_scope.clock.clkgen_freq = clk_hz
    husky_scope.clock.adc_mul = adc_mul
    husky_scope.clock.reset_adc()
    print("adc_locked   =", husky_scope.clock.adc_locked,
          " adc_freq =", husky_scope.clock.adc_freq)
    print("clkgen_locked=", husky_scope.clock.clkgen_locked,
          " clkgen_freq =", husky_scope.clock.clkgen_freq)

    if not husky_scope.clock.adc_locked or not husky_scope.clock.clkgen_locked:
        raise RuntimeError("Husky PLL/ADC lock 실패 — AUX 클럭 배선과 진폭을 확인한다.")

    husky_scope.trigger.triggers = "userio_d0"
    husky_scope.trigger.module = "basic"
    husky_scope.adc.basic_mode = "rising_edge"
    husky_scope.gain.db = gain_db
    husky_scope.adc.offset = 0
    husky_scope.adc.presamples = 0
    husky_scope.adc.decimate = 1
    print("gain.db      =", husky_scope.gain.db)
    print("[OK] Husky 측정 설정 완료 (samples 미정)")
    return clk_hz


def measure_trig_count(target, scope, key16, plain16):
    """AES 한 번을 돌려 트리거 폭(샘플 수)을 잰다."""
    scope.arm()
    ct = target_aes_encrypt(target, key16, plain16)
    if scope.capture():
        raise RuntimeError("capture 타임아웃 — TRIG(D0) 배선·펌웨어 트리거를 확인한다.")
    if ct != aes_ecb_encrypt(key16, plain16):
        raise RuntimeError("골든 불일치 — 측정 전에 통신 상태를 확인한다.")
    return int(scope.adc.trig_count)


def apply_trig_count(husky_scope, trig_counts, adc_mul):
    """trig_count 실측 목록으로 adc.samples 를 정하고 (TRIG_COUNT, NS) 를 돌려준다."""
    print("trig_count 회차:", list(trig_counts))
    if len(set(trig_counts)) != 1:
        print("[주의] trig_count 가 일정하지 않다. 트리거 배선·클럭 안정성을 확인한다.")
    trig_count = max(trig_counts)
    try:
        husky_scope.adc.samples = trig_count
    except Exception as e:
        raise RuntimeError(
            "adc.samples = %d 설정 실패: %s\n"
            "AES 전체가 Husky 버퍼보다 길다는 뜻이다. 대응:\n"
            "  - ADC_MUL 을 낮춘다.\n"
            "  - 또는 husky_scope.adc.decimate 를 키운다."
            % (trig_count, e)) from e
    ns = int(husky_scope.adc.samples)
    print("TRIG_COUNT = %d  →  adc.samples = %d  (≈ %.0f 사이클 @ adc_mul=%d)"
          % (trig_count, ns, ns / float(adc_mul), adc_mul))
    return trig_count, ns


def to_adc_code(wave_f):
    """Husky 정규화 실수(±0.5) → ADC 코드 스케일 int16."""
    return np.rint(np.asarray(wave_f, dtype=np.float64) * 32768.0).astype(np.int16)


def capture_one(target, scope, key16, plain16, check_golden=True, with_masks=False):
    """arm → 타겟 AES → capture → (파형, 암호문[, 마스크]).

    with_masks=True 이면 마스크 10바이트를 세 번째 값으로 추가한다.
    마스크 UART 는 capture 이후(트리거 밖)에 수행한다.
    """
    scope.arm()
    ct = target_aes_encrypt(target, key16, plain16)
    if scope.capture():
        raise RuntimeError("capture 타임아웃 — TRIG(D0) 배선·펌웨어 트리거를 확인한다.")
    if check_golden and ct != aes_ecb_encrypt(key16, plain16):
        raise RuntimeError("암호문 골든 불일치")
    wave = np.asarray(scope.get_last_trace(), dtype=np.float64)
    if with_masks:
        masks = target_get_masks(target)
        return wave, ct, masks
    return wave, ct


def capture_retry(target, scope, k, p, with_masks=False, tries=3, pause=2.0):
    """복구 사다리의 **1단계** — 단순 재시도. 골든 불일치는 재시도하지 않는다.

    LIBUSB_ERROR_IO 등 USB 단절은 잠깐 쉰 뒤 재시도한다 (이 실험대에서 장시간
    캡처 중 관측된 실패 모드). 연속 tries 회 실패하면 마지막 예외를 올린다.

    이 함수를 직접 부르지 말고 `Bench.capture()` 를 쓴다. 여기서 못 살리는 고장은
    재연결·펌웨어 재기록으로 넘어가야 하는데, 그 판단은 Bench 가 한다.

    Masked 주의: 재시도는 타겟에서 암호화를 한 번 더 돌리므로 rand() 가 그만큼
    전진한다. 즉 시드를 알아도 "n번째 트레이스의 마스크" 를 호스트에서 계산할 수는
    없다 — 마스크의 정본은 언제나 0x83 'm' 으로 회수해 i_m 에 저장한 값이다.
    """
    last = None
    for attempt in range(tries):
        try:
            return capture_one(target, scope, k, p, with_masks=with_masks)
        except RuntimeError as e:
            if "골든" in str(e) or "불일치" in str(e) or "마스크" in str(e):
                raise
            last = e
        except Exception as e:
            # usb1.USBErrorIO, USBErrorNoDevice 등
            last = e
        time.sleep(pause * (1.0 + 0.25 * attempt))
    raise RuntimeError("캡처 %d회 연속 실패: %s" % (tries, last))


def write_root_metadata(h5, bench, cipher_attr, fixed_key, fixed_pt):
    """루트 Metadata 를 SCHEMA.md §3 대로 기록한다.

    이 함수가 스키마와 실측 장비를 잇는 **유일한 지점**이다. 필드가 늘거나 이름이
    바뀌면 여기만 고친다.

    모르는 값은 적지 않는다(SCHEMA.md §5.3). 예를 들어 대역폭은 Husky 설정에서
    바로 읽을 수 없으므로 기록하지 않는다 — 추정치를 넣으면 다음 사람이 그것을
    측정값으로 오해한다.
    """
    husky = bench.husky
    # cipher_attr 예: "AES-128-ECB (masked-aes-c, MASKED=1)" → 알고리즘과 구현으로 쪼갠다.
    algo, _, impl = cipher_attr.partition(" (")
    impl = impl.rstrip(")") or algo

    h5.attrs["schema"] = SCHEMA
    h5.attrs["schema_version"] = SCHEMA_VERSION

    h5.attrs["target_name"] = bench.platform
    h5.attrs["target_device"] = "STM32F303"
    h5.attrs["target_clock_hz"] = float(bench.clk_hz)
    h5.attrs["iut_algorithm"] = algo
    h5.attrs["iut_implementation"] = impl
    h5.attrs["iut_countermeasure"] = (
        "1st-order Boolean masking (masked-aes-c, CipherMasked only; "
        "KeyExpansion unprotected)" if bench.with_masks else "none")

    h5.attrs["channel_type"] = "power"
    h5.attrs["channel_probe"] = "CW308 SHUNTL (내장 션트), Husky Measure 입력"
    h5.attrs["channel_gain_db"] = float(husky.gain.db)

    h5.attrs["sample_rate_hz"] = float(husky.clock.adc_freq)
    h5.attrs["sample_resolution_bits"] = 12          # Husky ADC
    h5.attrs["samples_per_trace"] = int(bench.ns)
    h5.attrs["sample_dtype"] = "int16"
    h5.attrs["sample_scale"] = 32768.0               # 정규화 값 = trace / scale
    # 타겟 클럭을 AUX 로 받아 그 배수로 샘플링한다(clkgen_src="extclk_aux_io").
    h5.attrs["synchronous_sampling"] = True

    h5.attrs["trigger_source"] = "userio_d0"
    h5.attrs["trigger_semantics"] = (
        "MY_AES_ECB 전체 — AES_init_ctx(KeyExpansion) + AES_ECB_encrypt")
    h5.attrs["trigger_samples"] = int(bench.trig_count)

    # 트리거로 동기화만 하고 후처리 정렬은 하지 않았다 (ISO/IEC 17825 A.2.6).
    h5.attrs["alignment"] = "none"

    h5.attrs["acquisition_start"] = datetime.datetime.now().isoformat(timespec="seconds")
    h5.attrs["tool_chain"] = "chipwhisperer %s; python %s; numpy %s" % (
        cw.__version__, sys.version.split()[0], np.__version__)
    h5.attrs["rng_seed"] = SEED

    # 이 저장소 고유 — 교육용 채점 기준이다 (SCHEMA.md §8).
    h5.attrs["fixed_key"] = fixed_key
    h5.attrs["fixed_pt"] = fixed_pt


def collect_group(h5, name, n_traces, key_mode, pt_mode, fixed_key, fixed_pt, seed,
                  bench, batch=BATCH):
    """한 그룹을 HDF5 에 스트리밍 저장한다. 캡처 사고는 bench 가 스스로 복구한다."""
    ns, with_masks = bench.ns, bench.with_masks
    g = h5.create_group(name)
    # 배열 이름은 SCHEMA.md 를 따른다 (상수는 scalib_common 에 있다).
    d_k = g.create_dataset(F_KEY, shape=(0, AES_BLOCK), maxshape=(None, AES_BLOCK),
                           dtype=np.uint8, chunks=True)
    d_p = g.create_dataset(F_PLAINTEXT, shape=(0, AES_BLOCK), maxshape=(None, AES_BLOCK),
                           dtype=np.uint8, chunks=True)
    d_o = g.create_dataset(F_CIPHERTEXT, shape=(0, AES_BLOCK), maxshape=(None, AES_BLOCK),
                           dtype=np.uint8, chunks=True)
    d_t = g.create_dataset(F_TRACE, shape=(0, ns), maxshape=(None, ns),
                           dtype=np.int16, chunks=(min(batch, 64), ns))
    d_m = None
    if with_masks:
        d_m = g.create_dataset(F_MASK, shape=(0, MASK_LEN), maxshape=(None, MASK_LEN),
                               dtype=np.uint8, chunks=True)

    bench.bind_group(g, name)
    if with_masks:
        _seed_masks(bench.target, g, name)

    rng = np.random.RandomState(seed)
    buf_k, buf_p, buf_o, buf_t, buf_m = [], [], [], [], []
    t_start = time.time()

    def flush():
        if not buf_t:
            return
        m = len(buf_t)
        for d, buf in ((d_k, buf_k), (d_p, buf_p), (d_o, buf_o), (d_t, buf_t)):
            d.resize(d.shape[0] + m, axis=0)
            d[-m:] = np.array(buf)
        if d_m is not None:
            d_m.resize(d_m.shape[0] + m, axis=0)
            d_m[-m:] = np.array(buf_m)
        buf_k.clear(); buf_p.clear(); buf_o.clear(); buf_t.clear(); buf_m.clear()

    for _ in trange(n_traces, desc=name, leave=True):
        k = bytearray(fixed_key) if key_mode == "fixed" else \
            bytearray(rng.randint(0, 256, AES_BLOCK, dtype=np.uint8).tolist())
        p = bytearray(fixed_pt) if pt_mode == "fixed" else \
            bytearray(rng.randint(0, 256, AES_BLOCK, dtype=np.uint8).tolist())
        if with_masks:
            wave, ct, masks = bench.capture(k, p)
            buf_m.append(list(masks))
        else:
            wave, ct = bench.capture(k, p)
        buf_k.append(list(k)); buf_p.append(list(p))
        buf_o.append(list(ct)); buf_t.append(to_adc_code(wave))
        if len(buf_t) >= batch:
            flush()
            # 배치마다 디스크에 반영 — USB 사고 시 손실 구간을 줄인다
            h5.flush()
    flush()
    h5.flush()

    g.attrs["role"] = SUBSET_ROLE_MAP[name]
    g.attrs["key_mode"] = key_mode
    g.attrs["pt_mode"] = pt_mode
    g.attrs["n_records"] = n_traces
    g.attrs["seconds"] = time.time() - t_start
    print("  [OK] %-11s %6d 장  %.1f 분" % (name, n_traces, (time.time() - t_start) / 60))


def run_full_collect(out_path, bench, cipher_attr):
    """§8 본 수집. 그룹을 작은 것부터 저장한다.

    bench : Bench — 장비·측정 설정을 들고 있으며 캡처 사고를 스스로 복구한다.
    """
    with_masks = bench.with_masks
    rng_fix = np.random.RandomState(SEED)
    fixed_key = rng_fix.randint(0, 256, AES_BLOCK, dtype=np.uint8)
    fixed_pt = rng_fix.randint(0, 256, AES_BLOCK, dtype=np.uint8)
    print("고정 키  :", fixed_key)
    print("고정 평문:", fixed_pt)
    print()

    Path(out_path).parent.mkdir(exist_ok=True)
    t_all = time.time()
    with h5py.File(out_path, "w") as h5:
        write_root_metadata(h5, bench, cipher_attr, fixed_key, fixed_pt)

        for name in ("explore", "attack", "tvla_rk", "tvla_fk", "profiling"):
            key_mode, pt_mode, seed = GROUP_MODES[name]
            collect_group(
                h5, name, GROUP_TARGETS[name], key_mode, pt_mode,
                fixed_key, fixed_pt, seed, bench)
        _record_recoveries(h5, bench)

    _report_schema(out_path)
    print()
    print("[완료] 총 %.1f 분, %s (%.2f GB)"
          % ((time.time() - t_all) / 60, out_path, Path(out_path).stat().st_size / 1e9))
    return fixed_key, fixed_pt


def resume_group(h5, name, bench, fixed_key, fixed_pt, batch=BATCH):
    """그룹이 목표 장수에 못 미치면 모자란 만큼 이어서 채운다."""
    with_masks = bench.with_masks
    target_n = GROUP_TARGETS[name]
    key_mode, pt_mode, seed = GROUP_MODES[name]
    g = h5[name]
    have = g[F_TRACE].shape[0]
    if have >= target_n:
        print("  /%-10s %6d 장 — 이미 충족" % (name, have))
        return

    print("  /%-10s %6d → %d 장, %d 장 추가" % (name, have, target_n, target_n - have))
    rng = np.random.RandomState(seed)
    for _ in range(have):
        rng.randint(0, 256, AES_BLOCK, dtype=np.uint8)
        rng.randint(0, 256, AES_BLOCK, dtype=np.uint8)

    d_k, d_p, d_o, d_t = g[F_KEY], g[F_PLAINTEXT], g[F_CIPHERTEXT], g[F_TRACE]
    d_m = g[F_MASK] if (with_masks and F_MASK in g) else None
    if with_masks and d_m is None:
        raise RuntimeError("with_masks 인데 그룹에 %s 가 없다: /%s" % (F_MASK, name))

    bench.bind_group(g, name)
    if with_masks:
        # 이어받기는 재플래시·재부팅 뒤에 들어오는 경로다. 새 시드를 심지 않으면
        # 타겟이 앞 라운드와 똑같은 마스크 수열을 처음부터 재생한다.
        _seed_masks(bench.target, g, name)

    buf_k, buf_p, buf_o, buf_t, buf_m = [], [], [], [], []
    t_start = time.time()

    def flush():
        if not buf_t:
            return
        m = len(buf_t)
        for dset, buf in ((d_k, buf_k), (d_p, buf_p), (d_o, buf_o), (d_t, buf_t)):
            dset.resize(dset.shape[0] + m, axis=0)
            dset[-m:] = np.array(buf)
        if d_m is not None:
            d_m.resize(d_m.shape[0] + m, axis=0)
            d_m[-m:] = np.array(buf_m)
        h5.flush()
        buf_k.clear(); buf_p.clear(); buf_o.clear(); buf_t.clear(); buf_m.clear()

    for _ in trange(target_n - have, desc="%s (resume)" % name):
        time.sleep(0.01)
        k = bytearray(fixed_key) if key_mode == "fixed" else \
            bytearray(rng.randint(0, 256, AES_BLOCK, dtype=np.uint8).tolist())
        p = bytearray(fixed_pt) if pt_mode == "fixed" else \
            bytearray(rng.randint(0, 256, AES_BLOCK, dtype=np.uint8).tolist())
        if with_masks:
            wave, ct, masks = bench.capture(k, p)
            buf_m.append(list(masks))
        else:
            wave, ct = bench.capture(k, p)
        buf_k.append(list(k)); buf_p.append(list(p))
        buf_o.append(list(ct)); buf_t.append(to_adc_code(wave))
        if len(buf_t) >= batch:
            flush()
    flush()
    # collect_group 과 같은 attrs 를 남긴다. 예전에는 n_traces·seconds 만 써서
    # resume 로 만든 그룹은 key_mode/pt_mode 가 비었고, dataset_summary 가 '키=? 평문=?'
    # 를 찍었다. 값의 정본은 위에서 이미 꺼내 쓴 GROUP_MODES[name] 이다.
    g.attrs["role"] = SUBSET_ROLE_MAP[name]
    g.attrs["key_mode"] = key_mode
    g.attrs["pt_mode"] = pt_mode
    g.attrs["n_records"] = int(d_t.shape[0])
    g.attrs["seconds"] = float(g.attrs.get("seconds", 0.0)) + (time.time() - t_start)
    print("    → %d 장 완료 (%.1f 분)" % (d_t.shape[0], (time.time() - t_start) / 60))


def _report_schema(out_path):
    """수집 직후 스키마 준수를 확인한다 (SCHEMA.md §6).

    여기서 걸러야 규약 위반이 분석 단계까지 흘러가지 않는다. 수집은 이미 끝났으므로
    예외로 죽이지 않고 보고만 한다 — 데이터 자체는 살아 있기 때문이다.
    """
    bad = validate_dataset(path=out_path)
    if bad:
        print("[경고] SCHEMA.md 위반 %d건:" % len(bad))
        for b in bad:
            print("   -", b)
    else:
        print("[OK] SCHEMA.md 준수 확인")


def _record_recoveries(h5, bench):
    """수집 중 몇 번, 무엇으로 살아났는지 파일에 남긴다.

    자동 복구는 조용히 지나가기 쉬운데, 나중에 데이터 품질을 의심할 때 이 기록이
    첫 단서가 된다. 복구가 잦았다면 배선·USB 를 손봐야 한다는 뜻이다.
    """
    prev = list(h5.attrs.get("recoveries", []))
    h5.attrs["recoveries"] = np.array(
        prev + [s.encode() for s in bench.recoveries], dtype="S16")
    if bench.recoveries:
        print("[기록] 자동 복구 %d회: %s"
              % (len(bench.recoveries), ", ".join(bench.recoveries)))


def run_resume(out_path, bench):
    """§8.1 이어받기."""
    rng_fix = np.random.RandomState(SEED)
    fixed_key = rng_fix.randint(0, 256, AES_BLOCK, dtype=np.uint8)
    fixed_pt = rng_fix.randint(0, 256, AES_BLOCK, dtype=np.uint8)

    t_all = time.time()
    with h5py.File(out_path, "a") as h5:
        stored = np.array(h5.attrs["fixed_key"], dtype=np.uint8)
        if not np.array_equal(stored, fixed_key):
            raise RuntimeError(
                "파일의 fixed_key 가 현재 SEED 로 만든 값과 다르다. "
                "다른 설정으로 만든 데이터셋에 이어붙이면 안 된다.")
        for name in ("explore", "attack", "tvla_rk", "tvla_fk", "profiling"):
            resume_group(h5, name, bench, fixed_key, fixed_pt)
        _record_recoveries(h5, bench)
    _report_schema(out_path)
    print()
    print("[완료] %.1f 분, %s (%.2f GB)"
          % ((time.time() - t_all) / 60, out_path, Path(out_path).stat().st_size / 1e9))


def _samba_port(timeout=25.0):
    """SAM-BA 부트로더의 시리얼 포트 경로. 없으면 기다렸다가, 노드가 없으면 만든다.

    컨테이너의 /dev 는 호스트와 분리된 tmpfs 이고 /dev/bus/usb 만 bind-mount 라,
    새로 생긴 tty 노드가 컨테이너에 안 보일 수 있다. pyserial 은 /sys 를 읽으므로
    이름은 찾아내지만 열 수는 없다. 그래서 major:minor 를 읽어 직접 만든다.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        ports = cw.get_at91_ports()
        if ports:
            path = ports[0]
            if not Path(path).exists():
                dev = Path("/sys/class/tty/%s/dev" % Path(path).name).read_text().strip()
                major, minor = (int(x) for x in dev.split(":"))
                os.mknod(path, 0o600 | stat.S_IFCHR, os.makedev(major, minor))
                print("    /dev 노드 생성: %s (%d:%d)" % (path, major, minor))
            return path
        time.sleep(1.0)
    raise RuntimeError(
        "SAM-BA 부트로더 포트를 찾지 못했다. lsusb 에 03eb:6124 가 보이는지 확인한다.")


def reflash_husky_firmware(serial_number):
    """Husky 의 SAM 펌웨어를 소거하고 다시 기록한다.

    **왜 필요한가:** Husky 펌웨어가 손상되면 버전은 정상값(1.5.0)으로 보고하면서
    FPGA 레지스터 읽기만 어긋난다(모든 FPGA_READ 응답 앞에 0xff 한 바이트가 더 붙어
    cw.scope() 가 `Unknown hwInfoVer: Default/Unknown` 으로 실패). 이 상태는
    USB 전원 차단·허브 재열거·물리적 재삽입 어느 것으로도 낫지 않고, 재기록만 듣는다.

    실패해도 벽돌이 되지 않는다 — SAM 의 하드웨어 부트로더는 지울 수 없어서, 소거 뒤
    재기록이 실패하면 장치는 SAM-BA(03eb:6124) 로 계속 USB 에 보이고 재시도할 수 있다.

    실패 조건: 부트로더 진입 실패나 포트 탐색 실패면 예외.
    """
    from chipwhisperer.hardware.naeusb.naeusb import NAEUSB

    # 고장 상태에서는 serial_number 로 찾는 경로가 실패하므로 hw_location 을 쓴다.
    loc = None
    for dev in cw.list_devices():
        if "Husky" in dev["name"] and dev["sn"] == serial_number:
            loc = dev["hw_loc"]
    if loc is None:
        raise RuntimeError("Husky(SN %s) 가 USB 에 보이지 않는다." % serial_number)

    usb = NAEUSB()
    usb.con(idProduct=[0xACE5], hw_location=loc)
    print("    부트로더 진입 (펌웨어 소거)")
    usb.enterBootloader(forreal=True)
    time.sleep(8.0)

    port = _samba_port()
    print("    재기록:", port)
    cw.program_sam_firmware(serial_port=port, hardware_type="cwhusky")
    time.sleep(10.0)
    print("    [OK] Husky 펌웨어 재기록 완료")


class Bench:
    """수집 장비 한 벌(Lite + Husky + 타겟)과 측정 설정을 들고, 사고 시 스스로 복구한다.

    노트북이 연결·플래시·측정 설정을 마친 뒤 그 상태를 넘겨 받는다. 복구란 그 설정을
    그대로 다시 만드는 일이므로, 여기 넘기지 않은 값은 복구할 수 없다.

    복구 사다리 (위에서부터, 성공하면 멈춘다)

    | 단계 | 내용 | 최대 |
    |------|------|:----:|
    | 1 | 단순 재시도 | 3회 |
    | 2 | 재연결 + 측정 설정 복원 | 2회 |
    | 3 | Husky 펌웨어 재기록 | 1회 |

    전부 실패하면 예외를 올려 수집을 멈춘다. 이미 저장된 그룹은 유효하므로
    노트북의 이어받기로 재개하면 된다.
    """

    RETRY_CAPTURE = 3
    RETRY_RECONNECT = 2
    RETRY_REFLASH = 1

    def __init__(self, scopes, target, platform, adc_mul, gain_db,
                 trig_count, ns, clk_hz, with_masks):
        self.scopes = scopes
        self.target = target
        self.platform = platform
        self.adc_mul = adc_mul
        self.gain_db = gain_db
        self.trig_count = int(trig_count)
        self.ns = int(ns)
        self.clk_hz = float(clk_hz)
        self.with_masks = bool(with_masks)
        self.recoveries = []          # 무엇으로 몇 번 살아났는지 (h5 attrs 로 남는다)
        self._group = None            # 복구 후 마스크 재시드에 쓸 (그룹, 이름)
        self.husky_sn = next(
            d["sn"] for d in cw.list_devices() if "Husky" in d["name"])

    @property
    def lite(self):
        return self.scopes["ChipWhisperer_Lite"]

    @property
    def husky(self):
        return self.scopes["ChipWhisperer_Husky"]

    def bind_group(self, group, name):
        """지금 채우는 그룹을 알려 준다. 복구 후 마스크 시드를 여기에 기록한다."""
        self._group = (group, name)

    def disconnect(self):
        disconnect_all(self.scopes, self.target)

    def _reopen(self):
        """장비를 다시 열고 측정 설정을 원래대로 복원한다.

        adc.samples 는 처음 실측한 ns 를 그대로 다시 넣는다. 여기서 trig_count 를
        다시 재면 값이 달라져 행마다 파형 길이가 어긋날 수 있다.
        """
        try:
            disconnect_all(self.scopes, self.target)
        except Exception:
            pass
        time.sleep(2.0)
        self.scopes = connect_all_devices()
        # Lite 를 먼저 세운다. HS2 클럭이 타겟으로 나가야 타겟이 돌고, 그 클럭이 AUX 로
        # 들어와야 Husky 의 PLL 이 lock 된다. 이 한 줄이 없으면 setup_husky 가
        # "PLL/ADC lock 실패" 로 죽는다 — 배선 문제로 오해하기 쉽다.
        self.lite.default_setup()
        self.target = cw.target(self.lite, cw.targets.SimpleSerial2)

        # 타겟을 리셋해 통신 상태를 초기화한다. 재연결 직후의 타겟은 앞선 명령이 중간에
        # 끊긴 상태일 수 있어 그대로 두면 응답이 어긋난다.
        self.lite.io.nrst = False
        time.sleep(0.05)
        self.lite.io.nrst = "high_z"
        time.sleep(0.5)
        self.target.flush()

        self.clk_hz = setup_husky(self.husky, self.adc_mul, self.gain_db)
        self.husky.adc.samples = self.ns

        # 여기서 통신을 직접 확인한다. 반쯤 살아난 상태로 돌아가면 이후 수천 장이
        # 조용히 망가지므로, 안 되면 예외를 올려 사다리의 다음 단계로 넘긴다.
        probe_k = bytearray(range(AES_BLOCK))
        probe_p = bytearray(range(AES_BLOCK, 2 * AES_BLOCK))
        if target_aes_encrypt(self.target, probe_k, probe_p) != \
                aes_ecb_encrypt(probe_k, probe_p):
            raise RuntimeError("복구 후 골든 불일치 — 타겟 통신이 정상이 아니다.")

        # 타겟을 리셋했으므로 rand() 수열이 처음부터 재생된다. 새 시드를 심어야
        # 앞 구간과 같은 마스크가 반복되지 않는다 (mask_seeds attr 에 누적 기록).
        if self.with_masks and self._group is not None:
            _seed_masks(self.target, *self._group)

    def _try_capture(self, k, p):
        return capture_retry(self.target, self.husky, k, p,
                             with_masks=self.with_masks, tries=self.RETRY_CAPTURE)

    def capture(self, k, p):
        """복구를 포함한 캡처. 사람이 개입할 필요가 없다.

        반환: capture_one 과 같다 (with_masks 면 (파형, 암호문, 마스크)).
        실패 조건: 사다리를 다 내려가도 안 되면 RuntimeError.
        """
        try:
            return self._try_capture(k, p)
        except Exception as e:
            last = e

        for i in range(self.RETRY_RECONNECT):
            print("\n  [복구 2단계] 재연결 %d/%d — 직전 오류: %s"
                  % (i + 1, self.RETRY_RECONNECT, last))
            try:
                self._reopen()
                out = self._try_capture(k, p)
                self.recoveries.append("reconnect")
                print("  [복구 성공] 재연결로 회복, 수집을 계속한다.")
                return out
            except Exception as e:
                last = e

        for i in range(self.RETRY_REFLASH):
            print("\n  [복구 3단계] Husky 펌웨어 재기록 %d/%d — 직전 오류: %s"
                  % (i + 1, self.RETRY_REFLASH, last))
            try:
                reflash_husky_firmware(self.husky_sn)
                self._reopen()
                out = self._try_capture(k, p)
                self.recoveries.append("reflash")
                print("  [복구 성공] 펌웨어 재기록으로 회복, 수집을 계속한다.")
                return out
            except Exception as e:
                last = e

        raise RuntimeError(
            "복구 실패 — 수집을 중단한다.\n"
            "  마지막 오류: %s\n"
            "  이미 저장된 그룹은 유효하다. 노트북의 이어받기 셀로 재개한다." % last)


def disconnect_all(scopes_dict, target_obj):
    try:
        target_obj.dis()
        print("[OK] target.dis()")
    except Exception as e:
        print("[WARN] target.dis():", e)
    for name, sc in list(scopes_dict.items()):
        try:
            sc.dis()
            print("[OK] %s.dis()" % name)
        except Exception as e:
            print("[WARN] %s.dis(): %s" % (name, e))
    scopes_dict.clear()
