"""ISO/IEC 17825 §8.4 DPA — 사전 지정 민감값으로 나눈 두 집단의 Welch t-test.

fixed-vs-random 입력 검정은 ``tvla.py``가 담당한다. 이 모듈은 알고리즘 계약이 수집 전에
고정한 민감값을 계산하고 그 값으로 동일 subset을 분할한다. 누설 관측은 표본 수와 무관하게
fail이며, 미검출만 Formula (1) 수량을 충족해야 pass가 될 수 있다.
"""

import numpy as np
from scipy.stats import ttest_ind

from .. import paths  # noqa: F401
from ..algorithms import get as get_algorithm
import sca_schema as S  # noqa: E402

def run(dataset_path, spec, threshold_info, n_required, sensitive_window=None):
    """민감값 집단 DPA를 실행해 수치, 판정 축과 그래프용 t 배열을 반환한다."""
    cfg = spec["analysis_inputs"]["dpa"]
    group = S.load_group(dataset_path, cfg["subset"],
                         fields=[S.F_TRACE, S.F_KEY, S.F_PLAINTEXT])
    traces = group[S.F_TRACE]
    labels = get_algorithm(spec["algorithm"]).dpa_partition(
        group[S.F_PLAINTEXT], group[S.F_KEY], cfg["target"])
    counts = [int(np.count_nonzero(labels == x)) for x in (0, 1)]
    if min(counts) < 2:
        return {"verdict": "inconclusive", "procedure_status": "incomplete",
                "statistical_power": "underpowered", "early_finding": "not-applicable",
                "preassessment_verdict": "inconclusive",
                "reason": "민감값 분할 집단 하나의 표본이 2 미만이다: %s" % counts,
                "target": cfg["target"]}

    # 파생 trace는 10회 평균의 분수를 보존한 float64다. 다시 int16으로 양자화하지 않고
    # 두 민감값 집단에 대해 직접 Welch 검정을 수행한다.
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.asarray(ttest_ind(np.asarray(traces[labels == 0], dtype=np.float64),
                                 np.asarray(traces[labels == 1], dtype=np.float64),
                                 axis=0, equal_var=False).statistic, dtype=np.float64)
    at = np.abs(t)
    threshold = float(threshold_info["threshold"])
    over = np.flatnonzero(at > threshold)
    in_window, outside = over, np.array([], dtype=int)
    if sensitive_window is not None:
        cols = S.instruction_window_columns(dataset_path, *sensitive_window)
        if cols is None:
            lo, hi = sensitive_window
            mask = (over >= lo) & (over < hi)
        else:
            mask = np.isin(over, cols)
        in_window, outside = over[mask], over[~mask]

    n_total = int(traces.shape[0])
    enough = n_total >= int(n_required)
    detected = bool(in_window.size)
    if detected:
        verdict = "fail"
        reason = "민감 경계 안에서 보정 임계를 넘는 샘플 %d개가 관측되었다" % in_window.size
    elif enough:
        verdict = "pass"
        reason = "충분한 표본에서 민감 경계 안의 임계 초과가 없다"
    else:
        verdict = "inconclusive"
        reason = ("장수 부족 — 보유 %d장, Formula (1) 요구 %d장. "
                  "미검출을 누설 없음으로 해석하지 않는다." % (n_total, n_required))
    n_nan = int(np.count_nonzero(np.isnan(t)))
    return {
        "verdict": verdict,
        "procedure_status": "complete",
        "statistical_power": "sufficient" if enough else "underpowered",
        "early_finding": "detected" if detected else "not-detected-at-N",
        "preassessment_verdict": verdict,
        "claim_scope": "ISO/IEC 17825 §8.4의 사전 지정 1차 민감값 분할 DPA",
        "reason": reason,
        "clause": "ISO/IEC 17825 §8.4 (Welch t-test, shall [08.02]·[08.03])",
        "subset": cfg["subset"], "target": cfg["target"],
        "groups": {"class_0": counts[0], "class_1": counts[1], "n_total": n_total},
        "samples": int(traces.shape[1]),
        "abs_t_max": float(np.nanmax(at)) if n_nan < at.size else float("nan"),
        "abs_t_max_index": int(np.nanargmax(at)) if n_nan < at.size else -1,
        "n_undefined": n_nan,
        "threshold": threshold_info,
        "n_over_threshold": int(over.size),
        "n_over_in_window": int(in_window.size),
        "n_over_outside_window": int(outside.size),
        "over_indices_head": over[:64].tolist(),
        "sensitive_window": None if sensitive_window is None else list(sensitive_window),
        "requirement": {"n_required": int(n_required), "n_have": n_total,
                        "met": bool(enough), "source": "ISO/IEC 17825 Formula (1)"},
        "_t": t,
    }
