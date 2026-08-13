"""ChipWhisperer Lite + Husky 실물 전력 수집기.

논리 레코드 하나는 같은 키·평문을 ``average_n``회 모두 성공적으로 캡처한 뒤에만 HDF5에
추가한다. 대표 ``trace``와 ``exec_time``은 원 반복 배열의 반올림 평균이며, 원 파형·트리거
길이·masked IUT의 실제 회수 마스크는 별도 배열에 보존한다. 따라서 평균 근거와 행 정렬을
Dataset 하나만으로 검증할 수 있다.

복구는 자연 발생한 정상 캡처 실패에만 실행한다. 타깃 reset, 장비 reconnect와 설정 복원,
Husky SAM 펌웨어 재기록을 차례로 각각 최대 3회 시도하며 인위적인 실패를 만들지 않는다.
재기록은 장비 상태를 크게 바꾸므로 마지막 단계에서만 수행한다.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import platform as platform_mod
import sys
import time
from pathlib import Path

import h5py
import numpy as np

from .. import paths

if str(paths.SCALIB) not in sys.path:
    sys.path.insert(0, str(paths.SCALIB))

import sca_schema as S  # noqa: E402
from aes_ref import aes_ecb_encrypt  # noqa: E402
import dataset_collect_lib as hw  # noqa: E402

STATUS = "구현됨 — 실제 완료 여부는 실행 Dataset·manifest·verify로만 판단한다."
SS_VER = "SS_VER_2_1"
CRYPTO_TARGET = "NONE"
MAX_RECOVERY_TRIES = 3


def _sha256(path):
    """파일을 1 MiB씩 읽어 SHA-256 문자열을 반환하며 파일을 변경하지 않는다."""
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _device_inventory(cw):
    """Lite와 Husky가 종류별로 정확히 한 대인지 확인하고 장치 설명을 반환한다.

    시리얼 전체는 반환하거나 출력하지 않고 마지막 네 자리만 보존한다. 누락이나 중복이면
    어떤 장치도 열기 전에 중단해 자동 선택이 임의 장비를 고르지 못하게 한다.
    """
    devices = list(cw.list_devices())
    by_kind = {}
    for kind in ("ChipWhisperer_Lite", "ChipWhisperer_Husky"):
        matches = [d for d in devices if d.get("name", "").replace("-", "_") == kind]
        if len(matches) != 1:
            raise RuntimeError("%s 장치가 정확히 한 대여야 한다 (현재 %d대)" % (kind, len(matches)))
        by_kind[kind] = matches[0]
    redacted = {k: {"name": v["name"], "serial_suffix": str(v["sn"])[-4:]}
                for k, v in by_kind.items()}
    return by_kind, redacted


class PowerBench:
    """한 실물 벤치의 연결·측정 설정과 단계별 복구 상태를 보관한다."""

    def __init__(self, spec, firmware_hex, ns=None):
        import chipwhisperer as cw

        self.cw = cw
        self.spec = spec
        self.coll = spec["collector"]
        self.firmware_hex = Path(firmware_hex)
        self.with_masks = spec["iut"]["name"] == "masked-aes-c"
        self.scopes = {}
        self.target = None
        self.ns = None if ns is None else int(ns)
        self.trig_count = None
        self.clk_hz = None
        self.recoveries = []
        self._mask_epoch = 0
        self._firmware_ready = False
        self._devices, self.inventory = _device_inventory(cw)
        self._open()

    @property
    def lite(self):
        return self.scopes["ChipWhisperer_Lite"]

    @property
    def husky(self):
        return self.scopes["ChipWhisperer_Husky"]

    def _open(self):
        """확정된 두 장치를 열고 타겟 통신·Husky 설정을 복원한다."""
        self.scopes = {}
        for kind, dev in self._devices.items():
            self.scopes[kind] = hw.open_scope(dev["sn"], kind)
        self.lite.default_setup()
        self.target = self.cw.target(self.lite, self.cw.targets.SimpleSerial2)
        self.clk_hz = hw.setup_husky(
            self.husky, int(self.coll["adc_mul"]), float(self.coll["gain_db"]))
        if self.ns is not None:
            self.husky.adc.samples = self.ns
        self.reset_target(seed_masks=self._firmware_ready)

    def flash_target(self):
        """빌드된 IUT 펌웨어를 Lite로 플래시하고 통신 상태를 초기화한다."""
        hw.flash_firmware(self.lite, self.coll["platform"], self.firmware_hex)
        self._firmware_ready = True
        self.reset_target()

    def reset_target(self, seed_masks=True):
        """STM32 nRST를 짧게 내린 뒤 통신 버퍼와 masked PRNG 시드를 초기화한다."""
        self.lite.io.nrst = False
        time.sleep(0.05)
        self.lite.io.nrst = "high_z"
        time.sleep(0.5)
        self.target.flush()
        if self.with_masks and seed_masks:
            self._mask_epoch += 1
            seed = (int(self.spec["seed"]) + self._mask_epoch * 2654435761) & 0xFFFFFFFF
            hw.set_mask_seed(self.target, seed)

    def configure_length(self, key, plaintext):
        """20번의 정상 AES로 트리거 길이를 재고 가장 긴 값에 ADC 길이를 맞춘다."""
        counts = [hw.measure_trig_count(self.target, self.husky, key, plaintext)
                  for _ in range(20)]
        self.trig_count, self.ns = hw.apply_trig_count(
            self.husky, counts, int(self.coll["adc_mul"]))
        return counts

    def _capture_once(self, key, plaintext):
        out = hw.capture_one(self.target, self.husky, key, plaintext,
                             with_masks=self.with_masks)
        wave, ciphertext = out[0], out[1]
        if len(wave) != self.ns:
            raise RuntimeError("파형 길이 %d가 고정 samples %d와 다르다" % (len(wave), self.ns))
        return wave, ciphertext, int(self.husky.adc.trig_count), (out[2] if self.with_masks else None)

    def capture(self, key, plaintext):
        """한 캡처를 수행하고 실패할 때만 reset→reconnect→SAM reflash로 복구한다."""
        try:
            return self._capture_once(key, plaintext)
        except Exception as exc:
            last = exc

        for attempt in range(1, MAX_RECOVERY_TRIES + 1):
            try:
                self.reset_target()
                out = self._capture_once(key, plaintext)
                self.recoveries.append("target_reset")
                return out
            except Exception as exc:
                last = exc

        for attempt in range(1, MAX_RECOVERY_TRIES + 1):
            try:
                self.close()
                time.sleep(1.0)
                self._open()
                out = self._capture_once(key, plaintext)
                self.recoveries.append("reconnect")
                return out
            except Exception as exc:
                last = exc

        husky_sn = self._devices["ChipWhisperer_Husky"]["sn"]
        for attempt in range(1, MAX_RECOVERY_TRIES + 1):
            try:
                self.close()
                hw.reflash_husky_firmware(husky_sn)
                self._open()
                out = self._capture_once(key, plaintext)
                self.recoveries.append("husky_sam_reflash")
                return out
            except Exception as exc:
                last = exc
        raise RuntimeError("복구 사다리 소진; 불완전한 논리 레코드는 저장하지 않았다: %s" % last)

    def close(self):
        """열린 target과 scope를 가능한 만큼 닫는다. 개별 종료 실패는 다음 연결로 전파하지 않는다."""
        try:
            if self.target is not None:
                self.target.dis()
        except Exception:
            pass
        for scope in list(self.scopes.values()):
            try:
                scope.dis()
            except Exception:
                pass
        self.scopes = {}
        self.target = None


def _firmware_paths(iut, platform):
    """IUT 펌웨어 디렉터리와 생성 HEX·ELF 경로를 반환한다."""
    folder = paths.SCALIB / ("simpleserial_%s" % iut)
    base = folder / ("simpleserial-base-%s" % platform)
    return folder, base.with_suffix(".hex"), base.with_suffix(".elf")


def _build_firmware(spec):
    """명세의 공용 IUT 소스를 SimpleSerial 펌웨어로 빌드하고 산출물 경로를 반환한다."""
    coll = spec["collector"]
    folder, hex_path, elf_path = _firmware_paths(spec["iut"]["name"], coll["platform"])
    hw.build_firmware(folder, coll["platform"], CRYPTO_TARGET, SS_VER, hex_path)
    if not elf_path.is_file():
        raise FileNotFoundError("빌드 ELF가 없다: %s" % elf_path)
    return hex_path, elf_path


def _expected_inputs(spec):
    """에뮬레이션 수집기와 같은 정본 함수로 모든 Subset 입력 배열을 만든다."""
    from ..collect import _make_inputs, _rng_for

    seed = int(spec["seed"])
    fixed_rng = np.random.RandomState(seed)
    fixed_key = fixed_rng.randint(0, 256, 16).astype(np.uint8)
    fixed_pt = fixed_rng.randint(0, 256, 16).astype(np.uint8)
    expected = {}
    for sub in spec["subsets"]:
        expected[sub["name"]] = _make_inputs(
            sub, _rng_for(seed, sub["name"]), fixed_key, fixed_pt, int(sub["n"]))
    return fixed_key, fixed_pt, expected


def _write_root(h5, spec, bench, elf_path, trigger_counts):
    """실행 시점의 실제 장비 설정과 명세의 명목 프로브 근거를 분리해 기록한다."""
    coll = spec["collector"]
    husky = bench.husky
    h5.attrs["schema"] = S.SCHEMA
    h5.attrs["schema_version"] = S.SCHEMA_VERSION
    h5.attrs["spec_id"] = spec["id"]
    h5.attrs["target_name"] = coll["platform"]
    h5.attrs["target_device"] = "STM32F303RCT7 on CW308T-STM32F3"
    h5.attrs["target_clock_hz"] = float(bench.clk_hz)
    h5.attrs["iut_algorithm"] = spec["scope"]["security_function"]
    h5.attrs["iut_implementation"] = spec["iut"]["name"]
    h5.attrs["iut_countermeasure"] = spec["iut"]["countermeasure"]
    h5.attrs["channel_type"] = "power"
    h5.attrs["channel_probe"] = "CW308 SHUNTL to Husky Measure input"
    h5.attrs["channel_gain_db"] = float(husky.gain.db)
    h5.attrs["sample_axis"] = "time"
    h5.attrs["sample_rate_hz"] = float(husky.clock.adc_freq)
    h5.attrs["sample_resolution_bits"] = 12
    h5.attrs["samples_per_trace"] = int(bench.ns)
    h5.attrs["sample_dtype"] = "int16"
    h5.attrs["sample_scale"] = 32768.0
    h5.attrs["trigger_source"] = "userio_d0"
    h5.attrs["trigger_semantics"] = coll["window"]["semantics"]
    h5.attrs["alignment"] = spec["criteria"]["preprocessing"]["alignment"]
    h5.attrs["acquisition_start"] = datetime.datetime.now().isoformat(timespec="seconds")
    h5.attrs["tool_chain"] = "chipwhisperer %s; python %s; numpy %s" % (
        bench.cw.__version__, platform_mod.python_version(), np.__version__)
    h5.attrs["rng_seed"] = int(spec["seed"])
    h5.attrs["exec_time_unit"] = "adc_sample"
    h5.attrs["exec_time_epsilon"] = float(coll["adc_mul"])
    h5.attrs["preprocessing_average_n"] = int(spec["criteria"]["preprocessing"]["average_n"])
    h5.attrs["platform"] = coll["platform"]
    h5.attrs["adc_mul"] = int(coll["adc_mul"])
    h5.attrs["bandwidth_hz"] = float(coll["bandwidth_hz"])
    h5.attrs["bandwidth_basis"] = coll["bandwidth_basis"]
    h5.attrs["bandwidth_is_nominal"] = bool(coll["bandwidth_is_nominal"])
    h5.attrs["shunt_ohm"] = float(coll["shunt_ohm"])
    h5.attrs["shunt_selection_note"] = coll["shunt_selection_note"]
    h5.attrs["shunt_max_verified"] = bool(coll["shunt_max_verified"])
    h5.attrs["firmware_sha256"] = _sha256(elf_path)
    h5.attrs["firmware_path"] = str(elf_path.relative_to(paths.WORKSPACE))
    h5.attrs["trigger_measurements"] = np.asarray(trigger_counts, dtype=np.uint32)
    h5.attrs["device_inventory_redacted"] = json.dumps(bench.inventory, sort_keys=True)
    h5.attrs["husky_hardware_version"] = str(getattr(husky, "hwInfo", "unknown"))
    h5.attrs["husky_firmware_version"] = str(getattr(husky, "fw_version", "unknown"))
    h5.attrs["lite_hardware_version"] = str(getattr(bench.lite, "hwInfo", "unknown"))
    h5.attrs["lite_firmware_version"] = str(getattr(bench.lite, "fw_version", "unknown"))
    h5.attrs["recoveries"] = np.asarray([], dtype="S24")


def _check_resume(h5, spec, expected):
    """기존 파일이 같은 명세·seed·입력 순서·평균 횟수인지 읽기만 해 확인한다."""
    checks = {
        "spec_id": spec["id"],
        "rng_seed": int(spec["seed"]),
        "preprocessing_average_n": int(spec["criteria"]["preprocessing"]["average_n"]),
    }
    for key, value in checks.items():
        if key not in h5.attrs or h5.attrs[key] != value:
            raise RuntimeError("resume 계약 불일치: %s (파일=%r, 명세=%r)"
                               % (key, h5.attrs.get(key), value))
    for sub in spec["subsets"]:
        if sub["name"] not in h5:
            continue
        g = h5[sub["name"]]
        rows = {name: d.shape[0] for name, d in g.items()}
        if len(set(rows.values())) != 1:
            raise RuntimeError("resume 행 정렬 불일치 /%s: %s" % (sub["name"], rows))
        have = next(iter(rows.values()), 0)
        if have > int(sub["n"]):
            raise RuntimeError("resume 파일이 명세 목표보다 많다 /%s: %d > %d"
                               % (sub["name"], have, sub["n"]))
        keys, pts = expected[sub["name"]]
        if have and (not np.array_equal(g[S.F_KEY][:], keys[:have]) or
                     not np.array_equal(g[S.F_PLAINTEXT][:], pts[:have])):
            raise RuntimeError("resume 입력 prefix 불일치: /%s" % sub["name"])


def _new_group(h5, sub, ns, repeats, with_masks):
    """한 Subset의 resizable 배열을 모두 빈 상태로 만들고 그룹을 반환한다."""
    g = h5.create_group(sub["name"])
    g.attrs["role"] = sub["role"]
    g.attrs["n_records"] = 0
    g.attrs["key_mode"] = sub["key_mode"]
    g.attrs["pt_mode"] = sub["pt_mode"]
    if "spa_pair_kind" in sub:
        g.attrs["spa_pair_kind"] = sub["spa_pair_kind"]
    g.create_dataset(S.F_KEY, (0, 16), maxshape=(None, 16), dtype=np.uint8, chunks=True)
    g.create_dataset(S.F_PLAINTEXT, (0, 16), maxshape=(None, 16), dtype=np.uint8, chunks=True)
    g.create_dataset(S.F_CIPHERTEXT, (0, 16), maxshape=(None, 16), dtype=np.uint8, chunks=True)
    g.create_dataset(S.F_TRACE, (0, ns), maxshape=(None, ns), dtype=np.int16,
                     chunks=(1, ns))
    g.create_dataset(S.F_TRACE_REPEATS, (0, repeats, ns), maxshape=(None, repeats, ns),
                     dtype=np.int16, chunks=(1, repeats, ns))
    g.create_dataset(S.F_EXEC_TIME, (0,), maxshape=(None,), dtype=np.uint32, chunks=True)
    g.create_dataset(S.F_EXEC_TIME_REPEATS, (0, repeats), maxshape=(None, repeats),
                     dtype=np.uint32, chunks=True)
    if with_masks:
        g.create_dataset(S.F_MASK_REPEATS, (0, repeats, 10), maxshape=(None, repeats, 10),
                         dtype=np.uint8, chunks=True)
    return g


def _append_record(g, key, plaintext, ciphertext, traces, times, masks=None):
    """완성된 반복 묶음을 같은 행에 추가하고 쓰기 실패 시 모든 배열 크기를 되돌린다."""
    trace = np.rint(traces.astype(np.float64).mean(axis=0)).astype(np.int16)
    exec_time = np.uint32(np.rint(times.astype(np.float64).mean()))
    payload = {
        S.F_KEY: np.asarray(key, dtype=np.uint8),
        S.F_PLAINTEXT: np.asarray(plaintext, dtype=np.uint8),
        S.F_CIPHERTEXT: np.frombuffer(ciphertext, dtype=np.uint8),
        S.F_TRACE: trace,
        S.F_TRACE_REPEATS: traces,
        S.F_EXEC_TIME: exec_time,
        S.F_EXEC_TIME_REPEATS: times,
    }
    if masks is not None:
        payload[S.F_MASK_REPEATS] = masks
    before = {name: d.shape[0] for name, d in g.items()}
    try:
        for name, value in payload.items():
            dset = g[name]
            dset.resize(before[name] + 1, axis=0)
            dset[-1] = value
    except Exception:
        for name, size in before.items():
            g[name].resize(size, axis=0)
        raise
    g.attrs["n_records"] = int(g[S.F_TRACE].shape[0])


def collect(spec, out_path, verbose=True, resume=False):
    """실물 펌웨어 빌드·플래시·설정 후 명세의 모든 논리 레코드를 수집한다.

    기존 파일은 ``resume=True``일 때만 열며 계약과 입력 prefix가 맞지 않으면 장비 수집 전에
    중단한다. 성공하면 완성 경로를 반환하고 장비는 항상 닫는다. 캡처·복구·골든 AES·마스크
    회수·파일 오류는 예외로 전파되며 불완전한 논리 레코드는 저장하지 않는다.
    """
    out_path = Path(out_path)
    fixed_key, fixed_pt, expected = _expected_inputs(spec)
    if out_path.exists() and not resume:
        raise FileExistsError("기존 Dataset을 덮어쓰지 않는다. 이어받으려면 --resume: %s" % out_path)
    if out_path.exists():
        with h5py.File(out_path, "r") as h5:
            _check_resume(h5, spec, expected)

    firmware_hex, firmware_elf = _build_firmware(spec)
    existing_ns = None
    if out_path.exists():
        with h5py.File(out_path, "r") as h5:
            existing_ns = int(h5.attrs["samples_per_trace"])
    bench = PowerBench(spec, firmware_hex, ns=existing_ns)
    try:
        bench.flash_target()
        if existing_ns is None:
            trigger_counts = bench.configure_length(fixed_key, fixed_pt)
        else:
            trigger_counts = []
            bench.husky.adc.samples = existing_ns
        probe = hw.target_aes_encrypt(bench.target, fixed_key, fixed_pt)
        if probe != aes_ecb_encrypt(fixed_key, fixed_pt):
            raise RuntimeError("본 수집 전 골든 AES 확인 실패")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if out_path.exists() else "w"
        with h5py.File(out_path, mode) as h5:
            if mode == "w":
                _write_root(h5, spec, bench, firmware_elf, trigger_counts)
            repeats = int(spec["criteria"]["preprocessing"]["average_n"])
            for sub in spec["subsets"]:
                keys, pts = expected[sub["name"]]
                g = (h5[sub["name"]] if sub["name"] in h5 else
                     _new_group(h5, sub, bench.ns, repeats, bench.with_masks))
                have = int(g[S.F_TRACE].shape[0])
                for row in range(have, int(sub["n"])):
                    trace_rows = np.empty((repeats, bench.ns), dtype=np.int16)
                    time_rows = np.empty(repeats, dtype=np.uint32)
                    mask_rows = (np.empty((repeats, 10), dtype=np.uint8)
                                 if bench.with_masks else None)
                    ciphertext = None
                    for repeat in range(repeats):
                        wave, ct, trig, mask = bench.capture(keys[row], pts[row])
                        if ciphertext is not None and ct != ciphertext:
                            raise RuntimeError("같은 논리 레코드 반복에서 암호문이 달라졌다")
                        ciphertext = ct
                        trace_rows[repeat] = hw.to_adc_code(wave)
                        time_rows[repeat] = trig
                        if mask_rows is not None:
                            mask_rows[repeat] = np.frombuffer(mask, dtype=np.uint8)
                    if ciphertext != aes_ecb_encrypt(keys[row], pts[row]):
                        raise RuntimeError("논리 레코드 골든 AES 불일치")
                    _append_record(g, keys[row], pts[row], ciphertext,
                                   trace_rows, time_rows, mask_rows)
                    h5.flush()
                    if verbose:
                        print("\r  /%-14s %4d/%d" % (sub["name"], row + 1, sub["n"]),
                              end="", flush=True)
                if verbose:
                    print()
            previous = [x.decode() if isinstance(x, bytes) else str(x)
                        for x in h5.attrs.get("recoveries", [])]
            h5.attrs["recoveries"] = np.asarray(
                previous + bench.recoveries, dtype="S24")
            h5.attrs["acquisition_end"] = datetime.datetime.now().isoformat(timespec="seconds")
        return out_path
    finally:
        bench.close()
