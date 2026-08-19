"""CLI — Dataset(데이터셋)을 분석하고 `runs/<id>/results.json`을 만든다.

    python3 -m physai.analyze --spec exp/001.yaml

## 시험 순서

ISO/IEC 17825 §7.3.2 `shall [07.03]` 과 §8.1 `shall [08.01]` 은 TA·SPA·DPA **셋 모두**를
요구하고, §7.3.2 는 순서도 정한다 — 다만 "the testing laboratory **should** follow the
order" 이므로 순서는 권고이고 **셋 다 평가하는 것이 의무**다.

그래서 `analyze` 는 **TA → SPA → DPA 순서로 수행하되 앞이 fail 이어도 뒤를 계속 돌린다.**
앞이 fail 이면 종합 판정은 이미 정해지지만, 뒤 시험은 **어디가 얼마나 새는지**를 알려 준다.
건너뛰면 그 정보를 잃고 §8.1 도 어긴다. 앞 시험의 실패는 뒤 시험 결과에
`preceded_by_failure` 로 기록된다.

유일한 예외는 TA 내부의 2단계다 — §7.3.4 가 1단계 실패 시 2단계로 가지 않는다고
**명시**하므로 그것은 `tests/ta.py` 안에서 지킨다.

## 판정과 참고를 구분한다

| 항목 | 지위 |
|---|---|
| `ta` · `spa` · `dpa` | **필수 판정** |
| `soundness` | 판정 (에뮬레이션 채널에 적용한 1차 누설 검출) |
| `snr` | 보조 — 누설 위치 탐색 |
| `cpa` | **양성 대조** — 배관 검증용. 표준상 필수 시험이 아니며 판정에 쓰지 않는다 |

`results.json` 이 이 등급을 명시하지 않으면 AI 가 참고 수치로 합/부를 주장하게 된다.
"""

import argparse
import json
import sys
import time

import numpy as np

from . import artifacts, paths, spec as spec_mod, preprocess
from . import soundness as soundness_mod
from .tests import dpa as dpa_mod, spa as spa_mod, ta as ta_mod, tvla as tvla_mod
from .algorithms import get as get_algorithm

import sca_schema as S          # noqa: E402
MANDATORY = ("ta", "spa", "dpa")
ANALYSIS_ORDER = ("ta", "spa", "tvla", "dpa")


def window_boundaries(dataset_path):
    """`window_symbols` + `sample_map` 으로 관측 구간의 내부 경계를 찾는다.

    출력: {심볼 이름: 명령어 인덱스}. 그 심볼이 구간 안에 없으면 빠진다.

    ELF를 다시 열지 않는다 — Dataset만으로 분석할 수 있어야 하기 때문이다.
    """
    attrs = S.root_attrs(dataset_path)
    text = str(attrs.get("window_symbols", ""))
    if not text:
        return {}
    smap = S.load_sample_map(dataset_path)
    # 첫 성분(segment 0)만 보면 명령어 순서가 그대로 나온다.
    seg0 = smap[smap[:, 0] == 0]
    addrs, idxs = seg0[:, 2], seg0[:, 1]
    out = {}
    for part in text.split(","):
        name, _, hexaddr = part.partition(":")
        if not hexaddr:
            continue
        a = int(hexaddr, 16)
        hit = np.flatnonzero(addrs == a)
        if hit.size:
            out[name.strip()] = int(idxs[hit[0]])
    return out


def sensitive_window(spec, boundaries, n_instr):
    """spec 의 `sensitive_leakage_time` 을 명령어 인덱스 구간으로 옮긴다.

    Annex H — **이 경계 안의 누설만 fail 로 센다.** 밖의 누설은 검출하되 별도 목록이다.
    """
    slt = spec["criteria"]["sensitive_leakage_time"]
    def resolve(v, default):
        """심볼·정수·`end` 경계값을 명령어 인덱스로 해석하고 실패 시 기본값을 쓴다."""
        if v is None:
            return default
        v = str(v)
        if v in boundaries:
            return boundaries[v]
        if v == "end":
            return n_instr
        try:
            return int(v, 0)
        except ValueError:
            return default
    lo = resolve(slt.get("from"), 0)
    hi = resolve(slt.get("to"), n_instr)
    return (lo, hi)


def run_cpa(dataset_path, spec, n=None):
    """양성 대조 — 1차 CPA 로 키를 복구해 본다.

    **판정이 아니다.** 표준은 CPA 를 필수 시험으로 두지 않는다(Fig.1 NOTE 3).
    이것이 확인하는 것은 '이 데이터에 키가 있는가' 가 아니라
    **'입력 주입·정렬·라벨링 배관이 옳은가'** 다. 비마스킹 타겟에서 복구되지 않으면
    데이터가 아니라 도구를 의심해야 한다.
    """
    # 정답 키는 attack subset 이 고정 키를 쓰므로 그 첫 행에서 읽는다.
    # 루트 HDF5 attrs에 fixed_key를 복제하지 않는다. 정답 키의 정본은 attack Subset 첫
    # 레코드이며 두 곳에 두면 한쪽만 갱신될 수 있다.
    algo = get_algorithm(spec["algorithm"])
    subset = spec["analysis_inputs"]["cpa"]["subset"]
    g = S.load_group(dataset_path, subset, n=n,
                     fields=[S.F_TRACE, S.F_KEY, S.F_PLAINTEXT])
    tr = g[S.F_TRACE].astype(np.float64)
    pt = g[S.F_PLAINTEXT]
    truth = g[S.F_KEY][0]

    tr -= tr.mean(axis=0)
    denom_t = np.sqrt((tr ** 2).sum(axis=0))
    denom_t[denom_t == 0] = np.inf

    recovered, ranks, rhos = [], [], []
    for j in range(algo.KEY_BYTES):
        guesses = np.arange(256, dtype=np.uint8)
        # (256, n) 예측: HW(SBOX[p_j ^ g])
        pred = algo.cpa_predictions(pt[:, j], guesses).astype(np.float64)
        pred -= pred.mean(axis=1, keepdims=True)
        denom_p = np.sqrt((pred ** 2).sum(axis=1))
        denom_p[denom_p == 0] = np.inf
        corr = (pred @ tr) / denom_p[:, None] / denom_t[None, :]
        score = np.nanmax(np.abs(corr), axis=1)
        order = np.argsort(-score)
        best = int(order[0])
        recovered.append(best)
        ranks.append(int(np.flatnonzero(order == int(truth[j]))[0]))
        rhos.append(float(score[best]))

    ok = int(sum(1 for j in range(16) if recovered[j] == int(truth[j])))
    return {
        "role": "positive-control",
        "note": ("판정이 아니다. 배관(입력 주입·정렬·라벨링)이 옳은지 확인하는 양성 대조다. "
                 "ISO/IEC 17825 Fig.1 NOTE 3 — CPA 는 필수 시험이 아니다."),
        "n_traces": int(tr.shape[0]),
        "subset": subset,
        "key_bytes": int(algo.KEY_BYTES),
        "bytes_recovered": ok,
        "mean_rank": float(np.mean(ranks)),
        "ranks": ranks,
        "best_rho": rhos,
        "recovered_key": " ".join("%02x" % b for b in recovered),
        "true_key": " ".join("%02x" % b for b in truth),
    }


def main(argv=None):
    """명세와 Dataset(데이터셋)을 분석해 결과·중간 증거 파일을 기록한다.

    `argv`는 CLI 인자 목록이며 `None`이면 `sys.argv`를 사용한다. 스키마 위반, 누락된
    입력, 분석 오류는 예외 또는 `SystemExit`로 중단된다. 성공하면 `runs/<spec-id>/`에
    `results.json`, SPA·DPA 증거 배열을 쓰고 종료 코드 0을 반환한다. 저장된 Dataset과
    판정 기준은 변경하지 않는다.
    """
    ap = argparse.ArgumentParser(prog="physai.analyze")
    ap.add_argument("--spec", default=None, help="독립 v2 experiment YAML")
    ap.add_argument("--study", default=None, help="v2 study YAML")
    ap.add_argument("--experiment", default=None, help="--study에서 분석할 experiment id")
    ap.add_argument("--dataset", default=None)
    ap.add_argument("--n-soundness", type=int, default=None,
                    help="soundness 에 쓸 트레이스 수 (기본 전부)")
    # CPA 는 (256 × n) 예측 행렬과 (n × ns) 트레이스를 곱한다. 실측 데이터셋처럼
    # n·ns 가 크면 float64 중간 배열이 수 GB 로 불어나 메모리가 터진다. 배관 검증이
    # 목적이므로 전량이 필요하지 않다 — 기본을 제한하고 필요하면 늘린다.
    ap.add_argument("--n-cpa", type=int, default=3000,
                    help="CPA(양성 대조)에 쓸 트레이스 수. 0 이면 전부")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    if bool(a.spec) == bool(a.study):
        ap.error("--spec 또는 --study 중 정확히 하나가 필요하다")
    if a.study and not a.experiment:
        ap.error("--study에는 --experiment가 필요하다")
    sp = (spec_mod.load(a.spec) if a.spec else
          spec_mod.load_from_study(a.study, a.experiment))
    fixed_permutations = int(sp["analysis_parameters"]["soundness_permutations"])
    if a.dataset is None:
        source_ds, _ = artifacts.load_capture_manifest(sp["id"], sp)
    else:
        source_ds = paths.Path(a.dataset)
    bad = S.validate_dataset(path=source_ds)
    if bad:
        raise SystemExit("Dataset이 스키마를 어긴다 (%d건):\n  - %s"
                         % (len(bad), "\n  - ".join(bad)))

    ds = preprocess.prepare(source_ds, sp)
    bad = S.validate_dataset(path=ds)
    if bad:
        raise SystemExit("전처리 Dataset이 스키마를 어긴다 (%d건):\n  - %s"
                         % (len(bad), "\n  - ".join(bad)))
    attrs = S.root_attrs(ds)
    ns = int(attrs["samples_per_trace"])
    n_instr = ns // len(sp["collector"].get("components", ["x"])) \
        if str(attrs.get("sample_axis")) == "instruction" else ns
    bounds = window_boundaries(ds)
    win = sensitive_window(sp, bounds, n_instr)
    th = spec_mod.corrected_threshold(sp["criteria"], ns)
    need = spec_mod.required_n(sp["criteria"])

    say = (lambda *x: None) if a.quiet else print
    say("=" * 70)
    say(" 분석: %s — %s" % (sp["id"], sp["title"]))
    say("=" * 70)
    say("  Dataset       : %s" % ds.name)
    say("  샘플/트레이스 : %d (명령어 %d × 성분 %d)"
        % (ns, n_instr, max(1, ns // max(1, n_instr))))
    say("  구간 경계     : %s" % (bounds or "(window_symbols 없음)"))
    say("  민감 경계     : 명령어 %d–%d (Annex H)" % win)
    say("  보정 임계     : |t| > %.3f  (보정 전 %.1f, m=%d, Bonferroni)"
        % (th["threshold"], th.get("threshold_uncorrected", th["threshold"]), th["n_tests"]))
    say("  Formula (1)   : N = %d 장 필요" % need["n_required"])
    say("-" * 70)

    results = {
        "spec_id": sp["id"],
        "title": sp["title"],
        "dataset": str(ds),
        "source_dataset": str(source_ds),
        "dataset_sha_note": "manifest.json 이 해시를 기록한다",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "scope": sp["scope"],
        "criteria": sp["criteria"],
        "derived": {"required_n": need, "threshold": th,
                    "window_boundaries": bounds,
                    "sensitive_window_instructions": list(win),
                    "samples_per_trace": ns, "instructions": n_instr},
        "assessment_profile": sp["assessment_profile"],
        "campaign_stage": sp["campaign_stage"],
        "algorithm": sp["algorithm"],
        "analysis_parameters": sp["analysis_parameters"],
        "grades": {"mandatory": list(MANDATORY),
                   "judgement": (["soundness"] if "soundness" in sp["analyses"] else []),
                   "independent": ["tvla"],
                   "reference_only": ["snr"],
                   "positive_control": (["cpa"] if
                                        sp["iut"]["countermeasure"] == "none" and
                                        "cpa" in sp["analyses"] else [])},
        "tests": {},
        "reference": {},
    }

    # ── 필수 시험: TA → SPA → DPA ──────────────────────────
    #
    # 순서는 §7.3.2 가 정한다("should follow the order of the operations").
    # 그러나 **앞 시험이 fail 이어도 뒤 시험을 계속 수행한다.** §8.1 `shall [08.01]` 이
    # 세 가지를 **모두** 평가하라고 요구하기 때문이다 — 순서는 should, 전부 평가는 shall
    # 이므로 shall 이 이긴다. 앞이 fail 이면 종합 판정은 이미 fail 이고, 뒤 시험은 그
    # 사실을 바꾸지 못하지만 **어디가 얼마나 새는지**를 알려 준다. 건너뛰면 그 정보를
    # 잃고 §8.1 도 어긴다.
    #
    # 유일한 예외는 TA 내부의 2단계다 — §7.3.4 가 1단계 실패 시 2단계로 가지 않는다고
    # 명시하므로 그것은 tests/ta.py 안에서 지킨다.
    failed_earlier = []
    for name in ANALYSIS_ORDER:
        if name not in sp["analyses"]:
            results["tests"][name] = {"verdict": "not-run",
                                      "reason": "spec 의 analyses 에 없다"}
            continue

        if name == "ta":
            r = ta_mod.run(source_ds, sp)
        elif name == "spa":
            ks = (bounds.get(sp["collector"]["window"]["from_symbol"], 0),
                  bounds.get(sp["collector"]["window"]["to_symbol"], n_instr)) \
                if bounds else None
            r = spa_mod.run(ds, sp, key_schedule_window=ks)
            r.pop("_groups", None)
            # 육안 검사용 Trace를 증거로 남긴다. SPA Subset은 Trace가 십여 장뿐이라
            # 통째로 저장해도 부담이 없고, 사람이 확인하려면 반드시 있어야 한다.
            _save_spa_traces(ds, sp, paths.run_dir(sp["id"], create=True))
        elif name == "tvla":
            r = tvla_mod.run(ds, sp, th, need["n_required"])
            t_arr = r.pop("_t", None)
            if t_arr is not None:
                np.save(paths.run_dir(sp["id"], create=True) / "tvla_t.npy", t_arr)
        else:
            r = dpa_mod.run(ds, sp, th, need["n_required"], sensitive_window=win)
            t_arr = r.pop("_t", None)
            if t_arr is not None:
                np.save(paths.run_dir(sp["id"], create=True) / "dpa_t.npy", t_arr)
        if failed_earlier and name in MANDATORY:
            r["preceded_by_failure"] = list(failed_earlier)
            r["note_order"] = ("앞선 필수 시험 %s 가 이미 fail 이므로 종합 판정은 바뀌지 "
                               "않는다. 그래도 수행한 이유는 §8.1 `shall [08.01]` 이 세 "
                               "시험을 모두 평가하라고 요구하고, 어디가 새는지를 알아야 "
                               "고칠 수 있기 때문이다." % ", ".join(x.upper() for x in failed_earlier))
        results["tests"][name] = r
        say("  %-4s : %-14s %s" % (name.upper(), r["verdict"],
                                   r.get("reason", r.get("verdict_scope", ""))[:80]))
        if name in MANDATORY and r["verdict"] == "fail":
            failed_earlier.append(name)

    # ── 판정: soundness ──
    if "soundness" in sp["analyses"]:
        say("-" * 70)
        say("  soundness 검정 중 (라벨 순열 %d회)…" % fixed_permutations)
        r = soundness_mod.run(ds, sp, n_traces=a.n_soundness, n_perm=fixed_permutations,
                              sensitive_window=win)
        results["tests"]["soundness"] = r
        say("  SOUNDNESS: %-10s 결함 후보 %d개 (경계 안 %d)"
            % (r["verdict"], r["n_candidates"],
               sum(x.get("n_over_in_window", 0) for x in r["labels"].values()
                   if isinstance(x, dict))))

    # ── 양성 대조: cpa ──
    if "cpa" in sp["analyses"]:
        r = run_cpa(ds, sp, n=(a.n_cpa or None))
        results["reference"]["cpa"] = r
        say("  CPA(대조): %d/%d 바이트 복구, 평균 순위 %.1f"
            % (r["bytes_recovered"], r["key_bytes"], r["mean_rank"]))

    mandatory_verdicts = {name: results["tests"].get(name, {}).get("verdict")
                          for name in MANDATORY}
    local_control_required = (sp["iut"]["countermeasure"] == "none" and
                              "cpa" in sp["analyses"])
    positive_control_ok = not (
        local_control_required and
        results["reference"]["cpa"]["bytes_recovered"] !=
        results["reference"]["cpa"]["key_bytes"])
    if "fail" in mandatory_verdicts.values():
        overall = "fail"
    elif not positive_control_ok or any(v != "pass" for v in mandatory_verdicts.values()):
        overall = "inconclusive"
    else:
        overall = "pass"
    if not positive_control_ok and results["tests"].get("dpa", {}).get("verdict") != "fail":
        results["tests"]["dpa"]["control_status"] = "failed"
        results["tests"]["dpa"]["preassessment_verdict"] = "inconclusive"
        results["tests"]["dpa"]["verdict"] = "inconclusive"
        results["tests"]["dpa"]["reason"] += " 양성 대조 실패로 미검출 해석을 차단한다."
        mandatory_verdicts["dpa"] = "inconclusive"
    results["overall"] = {
        "preassessment_verdict": overall,
        "procedure_status": ("complete" if all(
            results["tests"].get(x, {}).get("procedure_status") == "complete"
            for x in MANDATORY) else "incomplete"),
        "human_review": {"spa": "pending"},
        # CPA는 비마스킹 기준 구현에서 수집·정렬·라벨 배관을 확인하는 양성 대조다.
        # 대책 구현의 CPA 미복구는 안전 판정도 대조 실패도 아니므로 적용불가로 구분한다.
        "positive_control": (("pass" if positive_control_ok else "fail")
                             if local_control_required else "not-applicable"),
        "claim_scope": "ISO/IEC 17825:2024 방법론 준용 사전진단; 적합성 평가는 주장하지 않음",
    }

    results["json_conventions"] = {
        "non_finite": ("무한대는 문자열 \"+inf\"/\"-inf\" 로, NaN 은 null 로 적는다. "
                       "JSON 표준에는 Infinity·NaN 리터럴이 없어 그대로 쓰면 엄격한 "
                       "파서가 읽지 못한다 — 계약 파일이므로 표준을 지킨다."),
        "snr_inf_meaning": ("SNR 무한대는 클래스 내 분산이 0이라는 수치 상태다. 유효한 "
                            "귀무 임계가 함께 산정된 경우에만 강한 종속 소견으로 해석하며, "
                            "임계 산정 실패 시에는 판정 근거로 쓰지 않는다."),
    }
    out_dir = paths.run_dir(sp["id"], create=True)
    (out_dir / "results.json").write_text(
        json.dumps(_json_safe(results), ensure_ascii=False, indent=2,
                   default=_json_default, allow_nan=False),
        encoding="utf-8")

    verdicts = {k: v.get("verdict") for k, v in results["tests"].items()}
    results_summary = {"ok": positive_control_ok, "spec": sp["id"], "overall": overall,
                       "verdicts": verdicts, "results": str(out_dir / "results.json")}
    say("-" * 70)
    say("  종합: %s" % overall)
    print(json.dumps(results_summary, ensure_ascii=False))
    if not positive_control_ok:
        say("  [실패] tiny-AES-c CPA 양성 대조가 16바이트를 복구하지 못했다. "
            "수집·정렬·라벨 설정을 점검해야 한다.")
    return 0 if positive_control_ok else 1


def _save_spa_traces(ds, sp, out_dir):
    """SPA Subset의 Trace(트레이스)를 압축 NPZ 증거 파일로 저장한다.

    `simple-analysis` 역할이 없으면 파일을 만들지 않는다. 입력 Dataset은 읽기 전용이며,
    기존 `spa_traces.npz`가 있으면 최신 분석 증거로 덮어쓴다. 저장 실패는 호출자에게
    전파된다. 이 파일은 사람이 수행할 육안 검사(A.2.2)의 입력이지 자동 판정이 아니다.
    """
    payload = {}
    for s in sp["subsets"]:
        if s["role"] != "simple-analysis":
            continue
        tr = S.load_group(ds, s["name"], fields=[S.F_TRACE])[S.F_TRACE]
        payload["%s|%s" % (s["name"], s.get("spa_pair_kind", "?"))] = tr
    if payload:
        np.savez_compressed(out_dir / "spa_traces.npz", **payload)


def _json_safe(o):
    """inf·NaN 을 표준 JSON 이 표현할 수 있는 형태로 바꾼다.

    JSON 표준에는 `Infinity`·`NaN` 리터럴이 없다. 파이썬의 `json` 은 기본으로 그것을
    써 버리지만, 엄격한 파서(다른 언어의 표준 라이브러리 대부분)는 읽지 못한다.
    `results.json` 은 **AI 와 도구 사이의 계약 파일**이므로 표준을 지켜야 한다.

    inf 를 큰 숫자로 바꾸지 않는 이유: 그러면 거짓 수치가 되고, 다음 사람이 그것을
    측정값으로 오해한다. 문자열로 두면 타입 검사를 강요하는 대신 사실이 보존된다.
    """
    import math
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_json_safe(v) for v in o]
    if isinstance(o, (float, np.floating)):
        f = float(o)
        if math.isinf(f):
            return "+inf" if f > 0 else "-inf"
        if math.isnan(f):
            return None
        return f
    if isinstance(o, np.ndarray):
        return _json_safe(o.tolist())
    return o


def _json_default(o):
    """NumPy 스칼라·배열·바이트를 표준 JSON 직렬화 가능 값으로 바꾼다.

    알려지지 않은 객체는 문자열로 보존한다. 파일을 쓰지 않으며 디코딩할 수 없는 바이트는
    대체 문자를 사용한다.
    """
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (bytes, np.bytes_)):
        return o.decode("utf-8", "replace")
    return str(o)


if __name__ == "__main__":
    sys.exit(main())
