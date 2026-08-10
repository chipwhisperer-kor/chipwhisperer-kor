"""필수 시험 2 — 단순 분석 (SPA/SEMA), ISO/IEC 17825 §7.3.5·§8.3.1.

## 대칭키에서 SPA 가 겨냥하는 것

§8.3.1: 대칭키 암호에서 SPA·SEMA 의 알려진 위협은 **key derivation(key schedule)** 이다.
"시험소가 중간값의 Hamming weight 를 알아낼 수 있으면 키가 드러난다."

이 저장소의 두 IUT 는 키 스케줄을 관측 구간 **안**에서 수행하고, `masked-aes-c` 조차
`KeyExpansion` 은 벤더 원본 비마스킹이다. 그래서 시험 대상이 명확히 존재한다.

## 요건 (Annex A.2.2 / A.3.2)

| | Level 3 | Level 4 |
|---|---|---|
| 파형 수 | 11 (같은 데이터쌍 1 + 미리 정한 다른 쌍 1 + 랜덤 다른 쌍 4) | 21 |
| 해상도 | CSP 비트당 ≥100 포인트 | ≥1,000 포인트 |

**"육안 검사와 통계 검정을 둘 다 통과해야 한다."**

## 통계 검정의 구성 — 무엇을 fail 로 볼 것인가

**"평문이 다르면 파형도 다르다" 는 fail 조건이 아니다.** 그 기준을 쓰면 완벽하게
마스킹된 구현을 포함해 **모든 구현이 실패한다** — 데이터가 다르면 소비 전력이 다른 것은
당연하고, 그것 자체는 비밀의 누설이 아니다.

§8.3.1 이 지목한 SPA 표적은 **key derivation** 이다. 그래서 판정 기준을 키에 건다.

| 파형쌍 | 무엇을 보나 | 판정에서의 역할 |
|---|---|---|
| `same-data` (같은 키·평문) | 관측의 재현성 = **잡음 바닥** | 대책 없으면 0 이어야 한다. 마스킹이면 마스크 재랜덤화로 0 이 아니며 그것이 기준선이 된다 |
| `different-data-fixed` (**키가 다름**, 평문 고정) | 단일 파형이 키에 따라 달라지는가 | **판정 근거** — 특히 key schedule 구간 |
| `different-data-random` (키 고정, 평문 다름) | 평문 의존 구조 | 참고. **fail 근거가 아니다** |

## 최종 판정은 이 도구가 내리지 못한다

A.2.2 는 **"육안 검사와 통계 검정 둘 다 통과해야 한다"** 고 정한다. 육안 검사는 정의상
사람의 행위이므로, 이 도구가 낼 수 있는 결과는 다음 둘뿐이다.

- 통계 검정 **실패** → `fail` (A.2.2: 둘 중 하나라도 못 통과하면 시험은 실패한다)
- 통계 검정 통과 → **`inconclusive`** — 육안 검사가 남아 있어 `pass` 라고 쓸 수 없다

**AI 가 "육안으로 확인했다" 고 쓰지 않는다.** 그렇게 쓰면 하지 않은 시험을 했다고
주장하는 것이 되고, 그 한 줄이 보고서 전체의 신뢰를 무너뜨린다.
"""

import numpy as np

from .. import paths        # noqa: F401 — workspace/lib 를 sys.path 에 넣는다

import sca_schema as S      # noqa: E402


def _pair_distance(traces):
    """모든 쌍의 최대 절대차와 그 위치. n 이 작으므로 전수 비교한다."""
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

    출력 dict — `verdict`, 통계 결과, **육안 항목은 항상 미결**.
    """
    lvl = int(spec["criteria"]["security_level"])
    need_traces = {3: 11, 4: 21}[lvl]
    need_points = {3: 100, 4: 1000}[lvl]

    subs = [s for s in spec["subsets"] if s["role"] == "simple-analysis"]
    if not subs:
        return {"verdict": "not-applicable",
                "reason": "role=simple-analysis 인 subset 이 없다",
                "requirement": {"met": False,
                                "note": "A.%d.2 는 %d 파형을 요구한다" % (2 if lvl == 3 else 3, need_traces)}}

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
    # 같은 입력에서의 차이 = 관측 잡음의 상한. 에뮬레이션은 결정적이라 0 이어야 한다.
    noise = same["full"]["max_abs_diff"] if same else 0.0

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
        shortfall.append("파형 %d장 (요구 %d장)" % (n_total, need_traces))
    if ns < need_points:
        shortfall.append("해상도 %d 포인트 (요구 %d 포인트)" % (ns, need_points))
    if not judged:
        shortfall.append("키가 다른 파형쌍(spa_pair_kind=different-data-fixed)이 없다 "
                         "— §8.3.1 이 지목한 표적을 시험할 수 없다")

    # 판정 의미론 — 이 도구는 SPA 에서 `pass` 도 `fail` 도 스스로 내지 않는다.
    #
    # 잡음 바닥이 0 인 결정적 채널에서 "키가 다르면 파형도 다르다" 는 사실상 항상 참이라,
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
        "statistical_verdict": stat,
        "verdict_scope": ("이 도구는 SPA 의 최종 판정을 내지 않는다. A.2.2 는 육안 검사와 "
                          "통계 검정을 **둘 다** 통과하라고 요구하는데 육안은 사람의 행위이고, "
                          "잡음 바닥이 0 인 결정적 채널에서는 '키가 다르면 파형도 다르다' 가 "
                          "거의 항상 참이라 그것만으로 fail 을 내면 판별력이 없다. "
                          "관측값과 `statistical_verdict` 를 근거로 사람이 판정한다."),
        "statistical_verdict_meaning": {
            "key-dependent-structure-observed":
                "키가 다른 단일 파형들이 잡음 바닥을 넘어 구별된다 — §8.3.1 이 지목한 "
                "key derivation 노출의 소견. 실제 키 복구 가능성은 육안·후속 분석의 몫이다.",
            "no-difference-beyond-noise":
                "키가 달라도 잡음 바닥을 넘는 차이가 없다.",
            "requirements-unmet":
                "A.2.2 의 파형 수·해상도 요건을 못 채웠거나 키가 다른 쌍이 없다.",
        },
        "clause": "ISO/IEC 17825 §7.3.5·§8.3.1, Annex A.%d.2" % (2 if lvl == 3 else 3),
        "target": "key derivation (key schedule) — §8.3.1 이 지목한 대칭키 SPA 표적",
        "noise_floor": noise,
        "noise_floor_note": ("같은 입력 쌍의 최대 절대차 = 판정의 기준선. "
                             "**대책이 없는 구현**이면 에뮬레이션은 결정적이므로 0 이어야 하고, "
                             "0 이 아니면 데이터가 아니라 관측 절차를 의심한다. "
                             "**마스킹 구현**이면 같은 입력이어도 마스크가 매번 새로 뽑혀 0 이 "
                             "아니며, 그 변동이 곧 대책이 만들어 낸 잡음 바닥이다 — 키 의존 "
                             "차이가 이 값을 넘어야 SPA 누설로 센다."),
        "findings": findings,
        "judged_on": ("키가 다른 파형쌍(different-data-fixed)만 판정에 넣는다. "
                      "평문이 다르면 파형도 다른 것은 모든 구현에서 당연하므로 "
                      "fail 근거가 될 수 없다."),
        "key_dependent_single_trace": bool(key_leak),
        "key_schedule_leak": bool(ks_leak),
        "visual_inspection": {
            "status": "미결 — 사람 확인 필요",
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
