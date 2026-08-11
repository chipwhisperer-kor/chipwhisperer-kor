"""필수 시험 3 — 차분 분석 (DPA/DEMA), ISO/IEC 17825 §8.4.

## 절차

§8.4 `shall [08.02]`: 트레이스를 **처리되는 민감 정보가 크게 다른 두 subset 으로 나누고**,
두 집단이 높은 신뢰도로 통계적으로 다르면 **누설이 있는 것이며 IUT 는 fail** 이다.
도구는 Welch t-test 다.

**판정은 키 복구가 아니라 누설 관측이다** (§7.2 — "test passes unless leakage is observed").
키가 복구되지 않아도 누설이 임계를 넘으면 fail 이다.

## 임계와 보정

§8.4: 신뢰수준 99,99 % → C = 3,9 / 99,999 % → C = 4,5.
그리고 **다중비교 보정이 의무**다(`shall [08.03]`, Bonferroni 선호). 샘플이 수만 개인
파형에서 보정 없이 |t| > 4.5 를 쓰면 귀무가설이 참이어도 수십 개가 우연히 넘는다.
보정은 `spec.corrected_threshold()` 가 계산한다.

## 고차는 시험하지 않는다

Fig.1 NOTE 3 — 고차 DPA 와 CPA 는 이 표준의 필수 시험이 아니다. 그리고 1차 부울 마스킹이
2차에서 뚫리는 것은 이론적으로 정상이라 결함으로 보고할 수도 없다. **계산하지 않으면
오보할 일도 없다** — 규칙보다 구조로 막는다.

## 트레이스 수가 모자라면 판정하지 않는다

Formula (1) 이 요구하는 N 에 못 미치면 `inconclusive` 로 보고한다.
부족한 트레이스 수로 "누설 없음"이라고 쓰는 것이 이 도구가 낼 수 있는 가장 나쁜 결과다 —
검정력이 없어서 못 본 것과 정말 없는 것을 구분할 수 없기 때문이다.
"""

import numpy as np
from scalib.metrics import Ttest

from .. import paths        # noqa: F401 — workspace/lib 를 sys.path 에 넣는다

import sca_schema as S      # noqa: E402

BATCH = 500


def run(dataset_path, spec, threshold_info, n_required, sensitive_window=None):
    """고정 집단 vs 랜덤 집단 1차 Welch t-test.

    입력
        sensitive_window : (start, end) 또는 None — Annex H 민감 누설 경계.
                           경계 **밖**의 초과 샘플은 검출하되 fail 로 세지 않는다.

    출력 dict — `verdict`, 초과 샘플 목록, 임계, 트레이스 수 충족 여부.
    """
    fixed = [s for s in spec["subsets"] if s["role"] == "leakage-detection-fixed"]
    random = [s for s in spec["subsets"] if s["role"] == "leakage-detection-random"]
    if not fixed or not random:
        return {"verdict": "not-applicable",
                "reason": "leakage-detection-fixed / -random subset 이 둘 다 있어야 한다"}

    a_name, b_name = fixed[0]["name"], random[0]["name"]
    n_a = S.group_len(dataset_path, a_name)
    n_b = S.group_len(dataset_path, b_name)
    n_total = n_a + n_b

    # 두 집단을 각각 한 번씩 읽어 SCALib 에 배치로 먹인다.
    # 배치로 나누는 이유는 메모리가 아니라 SCALib 의 누적 인터페이스에 맞추기 위함이다.
    ttest = Ttest(d=1)
    ns = None
    for name, cls in ((a_name, 0), (b_name, 1)):
        tr_all = S.load_group(dataset_path, name, fields=[S.F_TRACE])[S.F_TRACE]
        ns = tr_all.shape[1]
        for beg in range(0, tr_all.shape[0], BATCH):
            tr = np.ascontiguousarray(tr_all[beg:beg + BATCH], dtype=np.int16)
            ttest.fit_u(tr, np.full(tr.shape[0], cls, dtype=np.uint16))
        del tr_all
    t = np.asarray(ttest.get_ttest())[0]          # (ns,)

    th = float(threshold_info["threshold"])
    at = np.abs(t)
    # NaN 처리 — 잡음 없는 채널에서는 흔하다.
    #
    # 에뮬레이션은 결정적이라 "고정 키 + 고정 평문" 집단의 모든 트레이스가 **완전히
    # 동일**하다. 그 결과 두 집단 다 분산이 0 인 샘플에서 Welch t 가 0/0 = NaN 이 된다.
    # 이것은 "검정할 수 없음" 이지 "누설 없음" 이 아니므로 **초과로 세지 않되 개수를 보고**한다.
    # (비교 연산은 NaN 에서 False 이므로 초과 판정 자체는 이미 안전하다.)
    n_nan = int(np.count_nonzero(np.isnan(t)))
    absmax = float(np.nanmax(at)) if n_nan < at.size else float("nan")
    over = np.flatnonzero(at > th)

    # Annex H — 민감 경계 **안**의 초과만 fail 로 센다. 밖의 것은 따로 보고한다.
    # 경계는 **명령어 인덱스**로 주어지므로 샘플 열로 옮겨야 한다 (성분이 연접되어 있다).
    in_win, out_win = over, np.array([], dtype=int)
    win_cols = None
    if sensitive_window is not None:
        win_cols = S.instruction_window_columns(dataset_path, *sensitive_window)
        if win_cols is None:                       # 시간 축 데이터셋 — 샘플 인덱스 그대로
            lo, hi = sensitive_window
            mask = (over >= lo) & (over < hi)
        else:
            mask = np.isin(over, win_cols)
        in_win, out_win = over[mask], over[~mask]

    enough = n_total >= n_required
    if not enough:
        verdict = "inconclusive"
        reason = ("장수 부족 — 보유 %d장(=%d+%d), Formula (1) 요구 %d장. "
                  "검정력이 모자라 '누설 없음' 을 주장할 수 없다."
                  % (n_total, n_a, n_b, n_required))
    elif in_win.size > 0:
        verdict = "fail"
        reason = ("민감 경계 안에서 보정 임계 %.3f 를 넘는 샘플 %d개 (|t|max=%.2f)"
                  % (th, in_win.size, absmax))
    else:
        verdict = "pass"
        reason = ("민감 경계 안에서 보정 임계 %.3f 를 넘는 샘플이 없다 (|t|max=%.2f)"
                  % (th, absmax))

    return {
        "verdict": verdict,
        "reason": reason,
        "clause": "ISO/IEC 17825 §8.4 (Welch t-test, shall [08.02]·[08.03])",
        "groups": {"fixed": a_name, "random": b_name, "n_fixed": n_a, "n_random": n_b},
        "samples": int(ns),
        "abs_t_max": absmax,
        "abs_t_max_index": int(np.nanargmax(at)) if n_nan < at.size else -1,
        "n_undefined": n_nan,
        "n_undefined_note": ("t 를 정의할 수 없는 샘플 수(0/0). 잡음 없는 에뮬레이션에서 두 "
                             "집단이 모두 상수인 지점에 생긴다. '검정 불가' 이지 "
                             "'누설 없음' 이 아니므로 초과로 세지 않고 개수만 보고한다."),
        "threshold": threshold_info,
        "n_over_threshold": int(over.size),
        "n_over_in_window": int(in_win.size),
        "n_over_outside_window": int(out_win.size),
        "over_indices_head": over[:64].tolist(),
        "sensitive_window": (None if sensitive_window is None
                             else [int(sensitive_window[0]), int(sensitive_window[1])]),
        "requirement": {
            "n_required": int(n_required),
            "n_have": int(n_total),
            "met": bool(enough),
            "source": "ISO/IEC 17825 Formula (1)",
        },
        "_t": t,                      # 그림용. results.json 에는 싣지 않는다.
    }
