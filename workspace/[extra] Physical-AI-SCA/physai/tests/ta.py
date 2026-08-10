"""필수 시험 1 — 타이밍 분석 (TA) = constant-time 검증.

## 왜 캐시가 없어도 수행하는가

ISO/IEC 17825 의 두 조항을 혼동하기 쉽다.

| | 조항 | 조동사 | 캐시 조건 |
|---|---|---|---|
| **일반 타이밍 분석** | §7.3.4 + `shall [07.07]` + A.2.4 `shall collect` | **shall** | **없음 — 무조건** |
| 캐시 타이밍 공격 프레임워크 | §8.2 (Reference [50]) | can | 캐시가 있을 때만 |

**Annex A 전체에서 `shall collect` 는 A.2.4(Level 3 타이밍) 하나뿐이다.** SPA(A.2.2)와
DPA(A.2.3)는 `should collect` 다. 즉 타이밍 측정 수집이 normative Annex 에서 가장 강한
데이터 수집 요구다. §7.3.4 의 절차에는 캐시라는 단어가 나오지 않는다.

## 절차 (§7.3.4)

1단계 — 랜덤 CSP + 고정 평문: 실행시간이 **CSP** 에 의존하는가
2단계 — 고정 CSP + 랜덤 평문: 실행시간이 **평문** 에 의존하는가
1단계에서 fail 이면 2단계로 가지 않는다.

판정: `|T1 - T2| < ε` 이면 pass. ε 는 클럭 1사이클에 해당하는 값이며 채널마다 다르다
(`exec_time_unit`·`exec_time_epsilon`).

**평균 차이뿐 아니라 분산 차이도 계산한다** — §7.3.4 가 2차 타이밍 누설 검출을 위해
요구한다(`shall`). 고차 제외는 DPA 에만 해당하고 타이밍에는 해당하지 않는다.

## 에뮬레이션 채널의 한계 — 결과에 반드시 실린다

**Unicorn 에는 사이클 카운터가 없다.** `exec_time` 은 명령어 수이지 사이클 수가 아니다.
- 명령어 수가 **다르면** → 데이터 의존 제어흐름이라는 **확정 소견**
- 명령어 수가 **같아도** → constant-time 을 **증명하지 못한다.** Cortex-M4 는 명령어마다
  사이클이 다르고 플래시 wait state 도 있다. 확정은 실물 `trig_count` 나 디버그
  트레이스의 몫이다.
"""

import numpy as np
from scipy import stats

from .. import paths        # noqa: F401 — workspace/lib 를 sys.path 에 넣는다

import sca_schema as S      # noqa: E402


def _stage(exec_time, split_by, eps, alpha, label):
    """한 단계의 판정.

    입력
        exec_time  : (n,) 실행시간
        split_by   : (n,) 이분 기준값 (CSP 또는 평문의 첫 바이트)
        eps        : 같다고 볼 허용 오차
        alpha      : per-test 유의수준 (다중비교 보정 후)

    **평균과 분산을 통계량이 아니라 p 값으로 판정한다.** Welch 는 t 를, Levene 은 F 를
    돌려주므로 두 통계량을 같은 임계에 대면 서로 다른 유의수준을 적용하게 된다
    (자유도 1 에서 F = t² 이라 t 임계를 F 에 그대로 쓰면 훨씬 느슨해진다).
    p 값으로 비교하면 검정 종류와 무관하게 선언한 α 를 그대로 지킨다.

    판정 순서
        1) 전체 퍼짐(max-min)이 ε 미만이면 **그 자체로 pass** 다 — 어떤 입력에서도
           실행시간이 같다는 직접 증거이므로 통계 검정이 필요 없다.
        2) 아니면 두 집단으로 나눠 평균(Welch t)과 분산(Levene)을 검정한다.
    """
    t = np.asarray(exec_time, dtype=np.float64)
    spread = float(t.max() - t.min())
    uniq = int(np.unique(t).size)

    out = {
        "stage": label,
        "n": int(t.size),
        "mean": float(t.mean()),
        "min": float(t.min()),
        "max": float(t.max()),
        "spread": spread,
        "unique_values": uniq,
        "epsilon": float(eps),
    }

    if spread < eps:
        out.update(verdict="pass", reason="모든 실행시간이 ε 안에 있다 (퍼짐 %g < ε %g)"
                                          % (spread, eps),
                   t_mean=None, p_mean=None, t_var=None, p_var=None)
        return out

    # 두 집단: 이분 기준값의 중앙값으로 나눈다. 표준이 나누는 방법을 정하지 않았으므로
    # 재현 가능한 결정적 규칙을 쓰고 그 사실을 결과에 남긴다.
    b = np.asarray(split_by, dtype=np.float64)
    med = np.median(b)
    lo, hi = t[b <= med], t[b > med]
    out["split_rule"] = "이분 기준값의 중앙값(%g) 기준" % med
    out["n_low"], out["n_high"] = int(lo.size), int(hi.size)

    if lo.size < 2 or hi.size < 2:
        out.update(verdict="inconclusive",
                   reason="집단 하나의 표본이 2 미만이라 검정할 수 없다",
                   t_mean=None, p_mean=None, t_var=None, p_var=None)
        return out

    tm, pm = stats.ttest_ind(lo, hi, equal_var=False)          # 평균 — Welch
    try:
        tv, pv = stats.levene(lo, hi, center="mean")           # 분산 — 2차 타이밍 누설
    except Exception:
        tv, pv = float("nan"), float("nan")

    diff = abs(float(lo.mean()) - float(hi.mean()))
    fail = (diff >= eps) and np.isfinite(pm) and float(pm) < alpha
    fail_var = np.isfinite(pv) and float(pv) < alpha

    out.update(
        t_mean=float(tm), p_mean=float(pm),
        f_var=float(tv), p_var=float(pv),
        alpha=float(alpha),
        mean_diff=diff,
        verdict="fail" if (fail or fail_var) else "pass",
        reason=("평균차 %g ≥ ε 이고 p=%.3g < α=%.3g" % (diff, pm, alpha) if fail
                else "분산 검정 p=%.3g < α=%.3g (2차 타이밍 누설)" % (pv, alpha) if fail_var
                else "평균차 %g, 평균 p=%.3g · 분산 p=%.3g — α=%.3g 이상"
                     % (diff, pm, pv, alpha)),
    )
    return out


def run(dataset_path, spec):
    """타이밍 분석을 수행하고 결과 dict 를 돌려준다.

    입력
        dataset_path   : h5 경로
        spec           : 실험 명세 (α·보정 방식은 criteria 에서 읽는다)

    출력 dict
        verdict     : "pass" | "fail" | "inconclusive" | "not-applicable"
        stages      : 단계별 결과
        instrument  : 실행시간을 무엇으로 쟀는가
        cycle_accurate : bool — False 면 "같다"가 constant-time 을 증명하지 못한다
        requirement : Annex A 의 장수 요건 충족 여부
    """
    attrs = S.root_attrs(dataset_path)
    unit = str(attrs.get("exec_time_unit", ""))
    eps = float(attrs.get("exec_time_epsilon", 1.0))
    lvl = int(spec["criteria"]["security_level"])
    need = {3: 1000, 4: 10000}[lvl]

    subs = [s for s in spec["subsets"] if s["role"] == "timing"]
    if not subs:
        return {"verdict": "not-applicable",
                "reason": "role=timing 인 subset 이 없다",
                "requirement": {"met": False,
                                "note": "A.%d.4 는 각 1,000/10,000 회 수집을 shall 로 요구한다" % (2 if lvl == 3 else 3)}}

    # 1단계 = 랜덤 키 + 고정 평문, 2단계 = 고정 키 + 랜덤 평문 (§7.3.4 순서)
    stage1 = next((s for s in subs if s["key_mode"] == "random" and s["pt_mode"] == "fixed"), None)
    stage2 = next((s for s in subs if s["key_mode"] == "fixed" and s["pt_mode"] == "random"), None)

    stages, shortfall = [], []
    # 다중비교 보정의 m 은 **이 시험이 실제로 수행하는 검정 수**여야 한다.
    # DPA 는 샘플마다 검정하므로 m = 수만이지만, TA 는 단계마다 평균·분산 두 번씩
    # 최대 4회다. DPA 의 임계를 그대로 쓰면 α 가 네 자릿수 과보정되어, 명백한
    # 타이밍 차이도 pass 로 나온다.
    n_ta_tests = 4
    alpha = float(spec["criteria"]["alpha"]) / (
        n_ta_tests if spec["criteria"]["multiplicity_correction"] != "none" else 1)

    for sub, split_field, label in ((stage1, S.F_KEY, "1단계: CSP 의존성 (랜덤 키 · 고정 평문)"),
                                    (stage2, S.F_PLAINTEXT, "2단계: 평문 의존성 (고정 키 · 랜덤 평문)")):
        if sub is None:
            stages.append({"stage": label, "verdict": "not-applicable",
                           "reason": "해당 규약의 subset 이 없다"})
            continue
        g = S.load_group(dataset_path, sub["name"],
                         fields=[S.F_EXEC_TIME, split_field])
        # 장수는 **목표치가 아니라 실보유량**으로 센다. spec 의 n 을 믿으면 수집이
        # 중간에 끊긴 데이터셋에서 요건 충족을 거짓으로 보고하게 된다.
        have = int(g[S.F_EXEC_TIME].shape[0])
        if have < need:
            shortfall.append("%s: %d장 (요구 %d장)" % (sub["name"], have, need))
        r = _stage(g[S.F_EXEC_TIME], g[split_field][:, 0], eps, alpha, label)
        r["subset"] = sub["name"]
        stages.append(r)
        if r["verdict"] == "fail":
            # §7.3.2 — 1단계가 실패하면 2단계로 가지 않는다.
            break

    verdicts = [s["verdict"] for s in stages]
    if "fail" in verdicts:
        overall = "fail"
    elif all(v in ("pass", "not-applicable") for v in verdicts) and "pass" in verdicts:
        overall = "pass"
    else:
        overall = "inconclusive"

    cycle_accurate = unit != "instruction"
    out = {
        "verdict": overall,
        "stages": stages,
        "instrument": unit or "미기록",
        "epsilon": eps,
        "cycle_accurate": cycle_accurate,
        "alpha_per_test": alpha,
        "n_tests": n_ta_tests,
        "correction_note": ("TA 는 최대 4회(단계 2 × 평균·분산) 검정하므로 그 수로 보정한다. "
                            "DPA 의 샘플 수 보정을 그대로 쓰면 네 자릿수 과보정되어 "
                            "명백한 타이밍 차이도 pass 가 된다."),
        "requirement": {
            "clause": "ISO/IEC 17825 A.%d.4 (shall collect)" % (2 if lvl == 3 else 3),
            "required_per_block": need,
            "met": not shortfall,
            "shortfall": shortfall,
        },
    }
    if not cycle_accurate:
        out["caveat"] = (
            "실행시간을 **명령어 수**로 쟀다. Unicorn 에는 사이클 모델이 없으므로, "
            "명령어 수가 같다는 것이 constant-time 을 증명하지는 못한다 "
            "(Cortex-M4 는 명령어마다 사이클이 다르고 플래시 wait state 도 있다). "
            "확정하려면 실물 trig_count 나 디버그 트레이스로 다시 재야 한다. "
            "반대로 명령어 수가 다르면 데이터 의존 제어흐름이라는 확정 소견이다.")
    if not cycle_accurate and overall == "pass":
        out["verdict_qualified"] = "pass (명령어 수 기준 — 사이클 미검증)"
    return out
