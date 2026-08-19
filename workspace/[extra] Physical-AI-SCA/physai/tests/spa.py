"""필수 시험 2 — 단순 분석 (SPA/SEMA), ISO/IEC 17825 §7.3.5·§8.3.1.

## 대칭키에서 SPA 가 겨냥하는 것

§8.3.1: 대칭키 암호에서 SPA·SEMA 의 알려진 위협은 **key derivation(key schedule)** 이다.
"시험소가 중간값의 Hamming weight 를 알아낼 수 있으면 키가 드러난다."

이 저장소의 두 IUT 는 키 스케줄을 관측 구간 **안**에서 수행하고, `masked-aes-c` 조차
`KeyExpansion` 은 벤더 원본 비마스킹이다. 그래서 시험 대상이 명확히 존재한다.

## 요건 (Annex A.2.2 / A.3.2)

| | Level 3 | Level 4 |
|---|---|---|
| Trace(트레이스) 수 | 11 (같은 데이터쌍 1 + 미리 정한 다른 쌍 1 + 랜덤 다른 쌍 4) | 21 |
| 해상도 | CSP 비트당 ≥100 Sample(샘플) | ≥1,000 Sample |

**"육안 검사와 통계 검정을 둘 다 통과해야 한다."**

## 통계 검정의 구성 — 무엇을 fail 로 볼 것인가

**"평문이 다르면 트레이스도 다르다"는 fail 조건이 아니다.** 그 기준을 쓰면 완벽하게
마스킹된 구현을 포함해 **모든 구현이 실패한다** — 데이터가 다르면 소비 전력이 다른 것은
당연하고, 그것 자체는 비밀의 누설이 아니다.

§8.3.1 이 지목한 SPA 표적은 **key derivation** 이다. 그래서 판정 기준을 키에 건다.

| 트레이스 쌍 | 무엇을 보나 | 판정에서의 역할 |
|---|---|---|
| `same-data` (같은 키·평문) | 관측의 재현성 = **잡음 바닥** | 대책 없으면 0 이어야 한다. 마스킹이면 마스크 재랜덤화로 0 이 아니며 그것이 기준선이 된다 |
| `different-data-fixed` (**키가 다름**, 평문 고정) | 단일 트레이스가 키에 따라 달라지는가 | **판정 근거** — 특히 key schedule 구간 |
| `different-data-random` (키 고정, 평문 다름) | 평문 의존 구조 | 참고. **fail 근거가 아니다** |

## 최종 판정은 이 도구가 내리지 못한다

A.2.2 는 **"육안 검사와 통계 검정 둘 다 통과해야 한다"** 고 정한다. 육안 검사는 정의상
사람의 행위다. 또한 잡음이 0인 결정적 채널에서는 키가 다를 때 트레이스가 달라지는 것만으로
통계 실패를 확정할 수 없다. 따라서 이 도구는 구조 관측 여부와 요건 부족을 기록하되 최종
결과를 항상 **`inconclusive`**로 둔다. 사람은 증거 그림과 수치를 함께 검토해 판정해야 한다.

**AI 가 "육안으로 확인했다" 고 쓰지 않는다.** 그렇게 쓰면 하지 않은 시험을 했다고
주장하는 것이 되고, 그 한 줄이 보고서 전체의 신뢰를 무너뜨린다.
"""

import numpy as np

from .. import paths        # noqa: F401 — workspace/lib 를 sys.path 에 넣는다

import sca_schema as S      # noqa: E402


def _pair_distance(traces):
    """소수 Trace의 모든 쌍을 비교해 최대 절대차·위치·쌍을 반환한다.

    입력은 `(n, ns)` 배열이며 새 float64 배열을 만들어 계산하므로 원본을 변경하지 않는다.
    빈 입력은 차이 0과 쌍 없음으로 반환한다. shape이 2차원이 아니면 NumPy 오류가 전파된다.
    """
    n = traces.shape[0]
    t = traces.astype(np.float64)
    best = {"max_abs_diff": 0.0, "argmax": -1, "pair": None}
    diffs = []
    for i in range(n):
        for j in range(i + 1, n):
            d = np.abs(t[i] - t[j])
            m = float(d.max())
            diffs.append(m)
            if m > best["max_abs_diff"]:
                best = {"max_abs_diff": m, "argmax": int(np.argmax(d)), "pair": [i, j]}
    best["mean_max_abs_diff"] = float(np.mean(diffs)) if diffs else 0.0
    best["n_pairs"] = len(diffs)
    return best


def run(dataset_path, spec, key_schedule_window=None):
    """SPA 시험.

    입력
        key_schedule_window : (start, end) **명령어 인덱스** 구간 — §8.3.1 이 지목한
                              key schedule. None 이면 전 구간만 본다.

    출력 dict — `verdict`, 통계 결과, **육안 항목은 항상 미결**. Dataset은 읽기 전용이며
    필드·Subset 누락은 스키마 로더 예외 또는 `not-applicable` 결과로 드러난다.
    """
    lvl = int(spec["criteria"]["security_level"])
    need_traces = int(spec["profile_requirements"]["spa_required_traces"])
    need_points = int(spec["profile_requirements"]["spa_points_per_csp_bit"])

    subs = [s for s in spec["subsets"] if s["role"] == "simple-analysis"]
    if not subs:
        return {"verdict": "not-applicable",
                "procedure_status": "incomplete", "statistical_power": "not-applicable",
                "early_finding": "not-applicable", "preassessment_verdict": "inconclusive",
                "reason": "role=simple-analysis 인 subset 이 없다",
                "requirement": {"met": False,
                                "note": "A.%d.2는 Trace %d장을 요구한다" % (2 if lvl == 3 else 3, need_traces)}}

    attrs = S.root_attrs(dataset_path)
    ns = int(attrs["samples_per_trace"])

    # 명령어 구간 → 샘플 열. 변환 정의는 workspace/lib/sca_schema.py 한 곳에 있다.
    cols = (None if key_schedule_window is None else
            S.instruction_window_columns(dataset_path, *key_schedule_window))

    groups, n_total = {}, 0
    for s in subs:
        kind = s.get("spa_pair_kind", "different-data-random")
        tr = S.load_group(dataset_path, s["name"], fields=[S.F_TRACE])[S.F_TRACE]
        n_total += tr.shape[0]
        groups[kind] = {"subset": s["name"], "n": int(tr.shape[0]),
                        "full": _pair_distance(tr)}
        if cols is not None and cols.size:
            groups[kind]["key_schedule"] = _pair_distance(tr[:, cols])

    same = groups.get("same-data")
    # 같은 입력에서의 차이 = 관측 잡음의 상한. 결정적 에뮬레이션만 0을 기대한다.
    noise = same["full"]["max_abs_diff"] if same else 0.0
    emulated = "emulated-power" in spec["scope"]["channels"]
    masked = spec["iut"]["countermeasure"] != "none"

    # 판정 근거는 **키가 다른 쌍**뿐이다 (§8.3.1 — key derivation).
    # 평문이 다른 쌍은 참고로만 싣는다.
    JUDGED = "different-data-fixed"
    findings = []
    for k in (k for k in groups if k != "same-data"):
        d = groups[k]["full"]["max_abs_diff"]
        f = {
            "pair_kind": k, "subset": groups[k]["subset"],
            "varies": "key" if k == JUDGED else "plaintext",
            "counts_toward_verdict": k == JUDGED,
            "max_abs_diff": d, "noise_floor": noise,
            "distinguishable": bool(d > noise),
            "argmax_sample": groups[k]["full"]["argmax"],
        }
        if "key_schedule" in groups[k]:
            ks = groups[k]["key_schedule"]
            f["key_schedule_max_abs_diff"] = ks["max_abs_diff"]
            f["key_schedule_distinguishable"] = bool(ks["max_abs_diff"] > noise)
        findings.append(f)

    judged = [f for f in findings if f["counts_toward_verdict"]]
    ks_leak = any(f.get("key_schedule_distinguishable") for f in judged)
    key_leak = any(f["distinguishable"] for f in judged)

    enough = (n_total >= need_traces) and (ns >= need_points)
    shortfall = []
    if n_total < need_traces:
        shortfall.append("Trace %d장(요구 %d장)" % (n_total, need_traces))
    if ns < need_points:
        shortfall.append("해상도 %d Sample(요구 %d Sample)" % (ns, need_points))
    if not judged:
        shortfall.append("키가 다른 트레이스 쌍(spa_pair_kind=different-data-fixed)이 없다 "
                         "— §8.3.1 이 지목한 표적을 시험할 수 없다")

    # 판정 의미론 — 이 도구는 SPA 에서 `pass` 도 `fail` 도 스스로 내지 않는다.
    #
    # 잡음 바닥이 0인 결정적 채널에서 "키가 다르면 트레이스도 다르다"는 사실상 항상 참이라,
    # 그것만으로 fail 을 내면 **어떤 구현도 통과할 수 없는 판별력 없는 시험**이 된다.
    # 반대로 pass 를 내려면 A.2.2 가 요구하는 육안 검사가 필요한데 그것은 사람의 몫이다.
    #
    # 그래서 측정값은 그대로 싣되 판정은 `inconclusive` 로 두고, 관측된 것이 무엇인지
    # (키 의존 구조가 보였는가, 특히 key schedule 구간에서)를 `statistical_verdict` 로
    # 분명히 적는다. 판별은 사람이 그림과 이 수치를 보고 한다.
    if not enough or not judged:
        verdict, stat = "inconclusive", "requirements-unmet"
    elif key_leak:
        verdict, stat = "inconclusive", "key-dependent-structure-observed"
    else:
        verdict, stat = "inconclusive", "no-difference-beyond-noise"

    return {
        "verdict": verdict,
        "procedure_status": "complete",
        "statistical_power": "sufficient" if enough else "underpowered",
        "early_finding": ("detected" if key_leak else "not-detected-at-N"),
        "preassessment_verdict": "inconclusive",
        "claim_scope": "자동 통계 절차만 완료; 사람의 SPA 육안 검토는 포함하지 않음",
        "statistical_verdict": stat,
        "verdict_scope": ("이 도구는 SPA 의 최종 판정을 내지 않는다. A.2.2 는 육안 검사와 "
                          "통계 검정을 **둘 다** 통과하라고 요구하는데 육안은 사람의 행위다. "
                          "키가 다른 파형의 차이만으로 비밀 의존성과 실제 공격 가능성을 "
                          "확정할 수 없으므로, 관측 잡음 바닥과 `statistical_verdict` 및 "
                          "증거 그림을 함께 보고 사람이 판정한다."),
        "statistical_verdict_meaning": {
            "key-dependent-structure-observed":
                "키가 다른 단일 트레이스들이 잡음 바닥을 넘어 구별된다 — §8.3.1이 지목한 "
                "key derivation 노출의 소견. 실제 키 복구 가능성은 육안·후속 분석의 몫이다.",
            "no-difference-beyond-noise":
                "키가 달라도 잡음 바닥을 넘는 차이가 없다.",
            "requirements-unmet":
                "A.2.2의 Trace 수·해상도 요건을 못 채웠거나 키가 다른 쌍이 없다.",
        },
        "clause": "ISO/IEC 17825 §7.3.5·§8.3.1, Annex A.%d.2" % (2 if lvl == 3 else 3),
        "target": "key derivation (key schedule) — §8.3.1 이 지목한 대칭키 SPA 표적",
        "noise_floor": noise,
        "noise_floor_note": _noise_floor_note(emulated, masked),
        "findings": findings,
        "judged_on": ("키가 다른 트레이스 쌍(different-data-fixed)만 판정에 넣는다. "
                      "평문이 다르면 트레이스도 다른 것은 모든 구현에서 당연하므로 "
                      "fail 근거가 될 수 없다."),
        "key_dependent_single_trace": bool(key_leak),
        "key_schedule_leak": bool(ks_leak),
        "visual_inspection": {
            "status": "pending",
            "required_by": "ISO/IEC 17825 A.%d.2 — 육안과 통계 **둘 다** 통과해야 한다"
                           % (2 if lvl == 3 else 3),
            "artifact": "spa_traces.svg (증거 번들)",
            "note": "이 도구는 육안 검사를 수행하지 않으며 수행했다고 주장하지 않는다.",
        },
        "requirement": {
            "required_traces": need_traces, "have_traces": n_total,
            "required_points_per_csp_bit": need_points, "have_points": ns,
            "met": bool(enough), "shortfall": shortfall,
        },
        "_groups": groups,          # 그림용
    }


def _noise_floor_note(emulated, masked):
    """수집 채널과 대책에 맞는 같은-입력 잡음 바닥의 의미를 반환한다."""
    prefix = "같은 입력 쌍의 최대 절대차 = 판정의 경험적 기준선. "
    if not emulated:
        return (prefix + "실물 전력 채널에서는 계측 잡음·동기 오차가 포함되고, 마스킹 구현이면 "
                "마스크 재난수화 변동도 포함된다. 키 의존 차이는 이 기준선과 증거 그림을 "
                "함께 검토하며, 이 값만으로 SPA 최종 판정을 내리지 않는다.")
    if masked:
        return (prefix + "결정적 에뮬레이션이라도 마스킹 구현은 같은 입력에서 마스크를 새로 "
                "뽑으므로 0이 아닐 수 있다. 이 변동을 기준으로 삼되 최종 판정은 사람이 한다.")
    return (prefix + "대책 없는 결정적 에뮬레이션은 같은 입력에서 0을 기대한다. 0이 아니면 "
            "수집 재현성과 입력 계약을 점검하며, 이 값만으로 SPA 최종 판정을 내리지 않는다.")
