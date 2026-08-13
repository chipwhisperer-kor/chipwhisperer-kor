"""CLI — spec을 읽어 SCHEMA.md 검증을 통과하는 Dataset(데이터셋)을 만든다.

    python3 -m physai.collect --spec exp/001.yaml

수집 **전에** 실험 계획 보고서를 먼저 만든다. 결과를 본 뒤 판정 기준을 고르는
사후 정당화를 구조로 막기 위해서다 — ISO/IEC 17825 §8.4 `shall [08.04]` 도 통계 시험
전에 파라미터를 지정하라고 요구한다.

stdout 마지막 줄에 JSON 요약을 낸다. 종료 코드 0 = 성공.
"""

import argparse
import datetime
import json
import sys
import time

import h5py
import numpy as np

from . import paths, spec as spec_mod
from .collectors import cw_power, emulation

import sca_schema as S          # noqa: E402  (paths 가 workspace/lib 를 넣는다)

# HDF5 스트리밍 버퍼의 레코드 수다. 판정 기준이 아니며, 200개씩만 메모리에 보관해
# 전체 수집량이 늘어도 버퍼 크기가 커지지 않게 한다.
BATCH = 200


def _rng_for(seed, subset_name):
    """subset 마다 결정적이면서 서로 다른 난수열.

    이름에서 유도하므로 subset 을 더하거나 순서를 바꿔도 기존 subset 의 입력 벡터가
    바뀌지 않는다. 순번으로 파생하면 순서만 바꿔도 데이터가 통째로 달라진다.
    """
    h = 0
    for ch in subset_name:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return np.random.RandomState((int(seed) + h) & 0xFFFFFFFF)


def _make_inputs(sub, rng, fixed_key, fixed_pt, n):
    """Subset의 `key_mode`·`pt_mode`에 따라 키·평문 `n`쌍을 만든다.

    반환값은 각각 `(n, 16)` uint8 배열이다. 알 수 없는 모드는 명세 검증기가 앞에서
    거부해야 하며 이 함수는 입력 배열이나 난수 생성기 외의 상태를 변경하지 않는다.
    """
    if sub["key_mode"] == "fixed":
        k = np.repeat(fixed_key[None, :], n, axis=0)
    else:
        k = rng.randint(0, 256, (n, 16)).astype(np.uint8)
    if sub["pt_mode"] == "fixed":
        p = np.repeat(fixed_pt[None, :], n, axis=0)
    else:
        p = rng.randint(0, 256, (n, 16)).astype(np.uint8)
    return k, p


# SPA Trace 쌍(ISO/IEC 17825 A.2.2)도 별도 생성기를 두지 않는다.
#
# 한때 `spa_pair_kind` 로 입력을 만드는 함수를 따로 두었는데, 그것이 subset 의
# `key_mode`/`pt_mode` 를 무시해 **spec 이 "키 랜덤" 이라 선언한 subset 에 고정 키가
# 들어가는** 버그가 있었다. h5 의 subset attrs 에는 선언값이 적히므로 메타데이터가
# 거짓이 된다 — Dataset에서 가장 나쁜 종류의 결함이다.
#
# `spa_pair_kind` 는 **그 쌍을 어떤 의도로 만들었는지 적는 라벨**일 뿐이고, 입력을
# 실제로 결정하는 것은 언제나 `key_mode`/`pt_mode` 다. 생성기가 하나뿐이면
# 선언과 데이터가 어긋날 수 없다.
#
#   same-data              → key_mode=fixed,  pt_mode=fixed
#   different-data-fixed   → key_mode=random, pt_mode=fixed   (키가 다르다)
#   different-data-random  → key_mode=fixed,  pt_mode=random  (평문이 다르다)


def collect_emulation(spec, out_path, verbose=True, resume=False):
    """명세의 Subset을 순서대로 에뮬레이션해 Dataset을 담은 HDF5 파일을 만든다.

    첫 실행의 누설 모델 산출물에서 Trace 길이를 확인한다. 기존 파일은 ``resume=True``일
    때만 열고 명세·seed·입력 prefix·행 정렬이 일치하는 경우 각 Subset의 다음 완성 행부터
    이어받는다. ELF·심볼·명세·파일 I/O 오류는 호출자에게 전파된다. 이 채널의 값은 물리
    측정치가 아니라 누설 모델의 산출값이다.
    """
    iut = spec["iut"]["name"]
    coll = spec["collector"]
    tgt = emulation.EmulationTarget(iut, window=coll.get("window"),
                                    components=coll.get("components", emulation.COMPONENTS))

    seed = int(spec["seed"])
    rng_fix = np.random.RandomState(seed)
    fixed_key = rng_fix.randint(0, 256, 16).astype(np.uint8)
    fixed_pt = rng_fix.randint(0, 256, 16).astype(np.uint8)
    has_masks = emulation._has_masks(iut)

    # 첫 실행으로 트레이스 길이를 확정한다. 상수로 정하지 않는다.
    k0 = bytes(fixed_key)
    p0 = bytes(fixed_pt)
    _, _, tr0, _ = tgt.run(k0, p0, seed, trace=True)
    ns = int(tr0.shape[0])
    if verbose:
        print("관측 구간 %d 명령어 × 성분 %d = %d 샘플"
              % (tgt.n_instr, len(tgt.components), ns))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and not resume:
        raise FileExistsError("기존 Dataset을 덮어쓰지 않는다. 이어받으려면 --resume: %s"
                              % out_path)
    t_start = time.time()

    mode = "a" if out_path.exists() else "w"
    with h5py.File(out_path, mode) as h5:
        if mode == "w":
            _write_root_metadata(h5, spec, tgt, ns)
            h5.create_dataset(S.F_SAMPLE_MAP, data=tgt.sample_map(), dtype=np.uint32)
        else:
            for key, expected in (("spec_id", spec["id"]), ("rng_seed", seed)):
                if key not in h5.attrs or h5.attrs[key] != expected:
                    raise RuntimeError("resume 계약 불일치: %s (파일=%r, 명세=%r)"
                                       % (key, h5.attrs.get(key), expected))
            if int(h5.attrs.get("samples_per_trace", -1)) != ns or \
                    not np.array_equal(h5[S.F_SAMPLE_MAP][:], tgt.sample_map()):
                raise RuntimeError("resume sample_map 또는 Trace 길이가 현재 ELF와 다르다")

        for sub in spec["subsets"]:
            n = int(sub["n"])
            rng = _rng_for(seed, sub["name"])
            keys, pts = _make_inputs(sub, rng, fixed_key, fixed_pt, n)
            seeds = rng.randint(0, 2 ** 31, n).astype(np.uint32)

            if sub["name"] in h5:
                g = h5[sub["name"]]
                rows = {name: d.shape[0] for name, d in g.items()}
                if len(set(rows.values())) != 1:
                    raise RuntimeError("resume 행 정렬 불일치 /%s: %s" % (sub["name"], rows))
                have = next(iter(rows.values()), 0)
                if have > n or not np.array_equal(g[S.F_KEY][:], keys[:have]) or \
                        not np.array_equal(g[S.F_PLAINTEXT][:], pts[:have]):
                    raise RuntimeError("resume 입력 prefix 또는 목표 수 불일치: /%s"
                                       % sub["name"])
            else:
                g = h5.create_group(sub["name"])
                g.attrs["role"] = sub["role"]
                g.attrs["n_records"] = 0
                g.attrs["key_mode"] = sub["key_mode"]
                g.attrs["pt_mode"] = sub["pt_mode"]
                if "spa_pair_kind" in sub:
                    g.attrs["spa_pair_kind"] = sub["spa_pair_kind"]
                if has_masks:
                    g.attrs["mask_seeds"] = seeds
                g.create_dataset(S.F_TRACE, shape=(0, ns), dtype=np.int16,
                                 chunks=(min(BATCH, n), ns), maxshape=(None, ns))
                g.create_dataset(S.F_KEY, shape=(0, 16), dtype=np.uint8,
                                 chunks=True, maxshape=(None, 16))
                g.create_dataset(S.F_PLAINTEXT, shape=(0, 16), dtype=np.uint8,
                                 chunks=True, maxshape=(None, 16))
                g.create_dataset(S.F_CIPHERTEXT, shape=(0, 16), dtype=np.uint8,
                                 chunks=True, maxshape=(None, 16))
                g.create_dataset(S.F_EXEC_TIME, shape=(0,), dtype=np.uint32,
                                 chunks=True, maxshape=(None,))
                if has_masks:
                    g.create_dataset(S.F_MASK, shape=(0, 10), dtype=np.uint8,
                                     chunks=True, maxshape=(None, 10))
                have = 0

            d_t, d_k, d_p = g[S.F_TRACE], g[S.F_KEY], g[S.F_PLAINTEXT]
            d_o, d_e = g[S.F_CIPHERTEXT], g[S.F_EXEC_TIME]
            d_m = g[S.F_MASK] if has_masks else None

            t0 = time.time()
            buf_t = np.empty((BATCH, ns), dtype=np.int16)
            buf_o = np.empty((BATCH, 16), dtype=np.uint8)
            buf_e = np.empty(BATCH, dtype=np.uint32)
            buf_m = np.empty((BATCH, 10), dtype=np.uint8) if has_masks else None
            fill = 0
            base = have
            for i in range(have, n):
                ct, mk, tr, et = tgt.run(bytes(keys[i]), bytes(pts[i]),
                                         int(seeds[i]), trace=True)
                buf_t[fill] = tr
                buf_o[fill] = np.frombuffer(ct, dtype=np.uint8)
                buf_e[fill] = et
                if has_masks:
                    buf_m[fill] = np.frombuffer(mk, dtype=np.uint8)
                fill += 1
                if fill == BATCH or i == n - 1:
                    for dset in (d_t, d_k, d_p, d_o, d_e):
                        dset.resize(base + fill, axis=0)
                    if d_m is not None:
                        d_m.resize(base + fill, axis=0)
                    d_t[base:base + fill] = buf_t[:fill]
                    d_k[base:base + fill] = keys[base:base + fill]
                    d_p[base:base + fill] = pts[base:base + fill]
                    d_o[base:base + fill] = buf_o[:fill]
                    d_e[base:base + fill] = buf_e[:fill]
                    if has_masks:
                        d_m[base:base + fill] = buf_m[:fill]
                    base += fill
                    g.attrs["n_records"] = base
                    h5.flush()
                    fill = 0
                    if verbose:
                        pct = 100.0 * base / n
                        print("\r  /%-14s %6d/%d (%5.1f%%)" % (sub["name"], base, n, pct),
                              end="", flush=True)
            g.attrs["seconds"] = time.time() - t0
            if verbose:
                print("   %.1fs" % g.attrs["seconds"])

        # `recoveries`(자동 복구 이력)는 실물 수집기의 것이다. 에뮬레이션은 장비가
        # 없어 복구할 일이 없으므로 적지 않는다 — 빈 배열을 남기면 "복구 없음" 과
        # "이 채널에는 개념이 없음" 이 구분되지 않는다.
        h5.attrs["acquisition_seconds"] = time.time() - t_start

    return out_path


def _write_root_metadata(h5, spec, tgt, ns):
    """에뮬레이션 Dataset의 루트 HDF5 attrs를 열린 파일에 기록한다.

    입력은 쓰기 가능한 h5py 파일, 검증된 명세, 초기화된 타겟, Trace당 Sample 수다.
    물리 측정값을 추정하지 않으며, 에뮬레이터에 없는 클럭은 0과 설명을 함께 기록한다.
    쓰기 실패는 h5py 예외로 전파되고 반환값은 없다.
    """
    import platform
    import unicorn

    c = spec["criteria"]
    h5.attrs["schema"] = S.SCHEMA
    h5.attrs["schema_version"] = S.SCHEMA_VERSION

    h5.attrs["target_name"] = "emulated:%s" % tgt.metadata()["instruction_set"]
    h5.attrs["target_device"] = "Unicorn ARM (Cortex-M4 코드, 사이클 모델 없음)"
    # 에뮬레이터에는 클럭이 없다. 축이 명령어이므로 이 값은 의미가 없지만 스키마가
    # 요구하므로 0 을 적고 그 뜻을 schema_note 에 남긴다 — 비워 두면 필수 필드 누락이 된다.
    h5.attrs["target_clock_hz"] = 0.0
    h5.attrs["iut_algorithm"] = spec["scope"]["security_function"]
    h5.attrs["iut_implementation"] = spec["iut"]["name"]
    h5.attrs["iut_countermeasure"] = spec["iut"]["countermeasure"]

    h5.attrs["channel_type"] = "emulated-power"
    h5.attrs["channel_probe"] = ("물리 프로브 없음 — 에뮬레이터가 누설 모델로 산출한 값이다")

    h5.attrs["samples_per_trace"] = int(ns)
    h5.attrs["sample_dtype"] = "int16"
    h5.attrs["sample_scale"] = 1.0
    h5.attrs["sample_axis"] = "instruction"

    win = tgt.window
    h5.attrs["trigger_source"] = "symbol:%s" % win["from_symbol"]
    h5.attrs["trigger_semantics"] = win.get(
        "semantics",
        "%s 진입부터 %s 복귀까지 — 실측 펌웨어의 MY_AES_ECB 트리거와 같은 구간"
        % (win["from_symbol"], win["to_symbol"]))
    h5.attrs["alignment"] = "none"

    h5.attrs["acquisition_start"] = datetime.datetime.now().replace(microsecond=0).isoformat()
    h5.attrs["tool_chain"] = ("unicorn %s; python %s; physai collect"
                              % (unicorn.__version__, platform.python_version()))
    h5.attrs["rng_seed"] = int(spec["seed"])

    for k, v in tgt.metadata().items():
        h5.attrs[k] = v

    h5.attrs["exec_time_unit"] = "instruction"
    h5.attrs["exec_time_epsilon"] = 1.0        # 명령어 1개
    h5.attrs["preprocessing_average_n"] = int(c["preprocessing"]["average_n"])

    h5.attrs["spec_id"] = spec["id"]
    h5.attrs["schema_note"] = (
        "에뮬레이션 채널. trace 값은 측정치가 아니라 leakage_model 의 출력이다. "
        "target_clock_hz=0 은 에뮬레이터에 클럭이 없다는 뜻이며 "
        "sample_axis=instruction 이므로 시간 단위 값은 존재하지 않는다. "
        "exec_time 은 명령어 수이지 사이클 수가 아니다 — Unicorn 에 사이클 모델이 없다.")


def main(argv=None):
    """명세를 검증하고 계획 보고서와 Dataset을 생성한다.

    `argv`가 `None`이면 `sys.argv`를 사용한다. 수집 전에 계획 보고서를 기록하고
    `collector.kind`에 따라 에뮬레이션 또는 실물 전력 수집기를 실행한다. 성공 시 JSON
    요약을 stdout에 쓰고 스키마 위반이 없으면 0, 있으면 1을 반환한다.
    """
    ap = argparse.ArgumentParser(prog="physai.collect",
                                 description="spec → SCHEMA.md 검증을 통과하는 Dataset 생성")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", default=None, help="생략하면 traces/<spec.id>.h5")
    ap.add_argument("--resume", action="store_true",
                    help="기존 파일의 계약·입력 prefix가 일치할 때 다음 완성 레코드부터 재개")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    sp = spec_mod.load(a.spec)
    if not a.quiet:
        print("\n".join(spec_mod.summary_lines(sp)))
        print("-" * 66)

    # 실험 계획 보고서를 **수집 전에** 만든다. 결과를 본 뒤 판정 기준을 고치는 일이
    # 구조적으로 불가능하도록 순서를 고정한 것이다 (§8.4 `shall [08.04]`).
    # 지연 import: report 는 matplotlib 을 쓰므로 수집만 할 때 불러올 이유가 없다.
    from . import report as report_mod
    plan = report_mod.write_plan(sp, paths.run_dir(sp["id"], create=True))
    if not a.quiet:
        print("계획 보고서(수집 전): %s" % plan.relative_to(paths.PROJECT))
        print("-" * 66)

    out = paths.TRACES / ("%s.h5" % sp["id"]) if a.out is None else paths.Path(a.out)
    kind = sp["collector"]["kind"]
    if kind == "emulation":
        collect_emulation(sp, out, verbose=not a.quiet, resume=a.resume)
    else:  # JSON Schema가 지원 종류를 emulation과 cw_power로 한정한다.
        cw_power.collect(sp, out, verbose=not a.quiet, resume=a.resume)

    bad = S.validate_dataset(path=out)
    result = {"ok": not bad, "spec": sp["id"], "dataset": str(out),
              "schema_violations": bad}
    if not a.quiet:
        print("-" * 66)
        print("스키마 준수: %s" % ("예" if not bad else "위반 %d건" % len(bad)))
        for b in bad:
            print("  -", b)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
