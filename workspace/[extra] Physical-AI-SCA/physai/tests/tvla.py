"""독립 TVLA — 고정 입력과 랜덤 입력의 1차 Welch t-test.

TVLA는 널리 쓰이는 누설 탐색 절차지만 ISO/IEC 17825의 필수 TA·SPA·DPA 판정과 같은
항목은 아니다. 따라서 검출 여부와 검정력을 독립 축으로 보고하고 ISO 종합 판정에는
합산하지 않는다. 검출은 저표본에서도 사실이지만 미검출은 충분한 표본 없이는 결론이 아니다.
"""

import numpy as np
from scipy.stats import ttest_ind

from .. import paths  # noqa: F401
import sca_schema as S  # noqa: E402

def run(dataset_path, spec, threshold_info, n_required):
    """사전 지정된 fixed/random subset의 TVLA 통계와 결과 축을 반환한다."""
    cfg = spec["analysis_inputs"]["tvla"]
    names = (cfg["fixed"], cfg["random"])
    counts = [S.group_len(dataset_path, name) for name in names]
    fixed = np.asarray(S.load_group(dataset_path, names[0],
                                    fields=[S.F_TRACE])[S.F_TRACE], dtype=np.float64)
    random = np.asarray(S.load_group(dataset_path, names[1],
                                     fields=[S.F_TRACE])[S.F_TRACE], dtype=np.float64)
    ns = fixed.shape[1]
    # 파생 Dataset의 float64 평균을 정수형으로 되돌리면 10회 평균의 분수 정보가 사라진다.
    # scipy의 벡터화 Welch 검정은 입력 정밀도를 보존하며 equal_var=False가 절차의 정본이다.
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.asarray(ttest_ind(fixed, random, axis=0, equal_var=False).statistic,
                       dtype=np.float64)
    at = np.abs(t)
    threshold = float(threshold_info["threshold"])
    over = np.flatnonzero(at > threshold)
    n_nan = int(np.count_nonzero(np.isnan(t)))
    enough = sum(counts) >= int(n_required)
    detected = bool(over.size)
    finding = "detected" if detected else "not-detected-at-N"
    reason = ("보정 임계를 넘는 샘플 %d개가 관측되었다" % over.size if detected else
              "보정 임계를 넘는 샘플이 없다%s" %
              ("" if enough else "; 표본 부족이므로 누설 없음으로 해석하지 않는다"))
    return {
        "role": "independent-leakage-assessment",
        "standard_verdict_role": "TVLA는 ISO 필수 TA·SPA·DPA 종합 판정에 합산하지 않는다.",
        "procedure_status": "complete",
        "statistical_power": "sufficient" if enough else "underpowered",
        "early_finding": finding,
        "preassessment_verdict": "not-applicable",
        "verdict": "detected" if detected else ("not-detected" if enough else "inconclusive"),
        "reason": reason,
        "groups": {"fixed": names[0], "random": names[1],
                   "n_fixed": counts[0], "n_random": counts[1]},
        "samples": int(ns),
        "abs_t_max": float(np.nanmax(at)) if n_nan < at.size else float("nan"),
        "abs_t_max_index": int(np.nanargmax(at)) if n_nan < at.size else -1,
        "n_undefined": n_nan,
        "threshold": threshold_info,
        "n_over_threshold": int(over.size),
        "over_indices_head": over[:64].tolist(),
        "requirement": {"n_required": int(n_required), "n_have": int(sum(counts)),
                        "met": bool(enough),
                        "note": "Formula (1)을 TVLA 검정력 표시에 적용한 프로젝트 정책이며 별도 ISO 의무항목은 아니다."},
        "_t": t,
    }
