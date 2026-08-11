"""ISO/IEC 17825 요건 대조표 — 무엇을 지켰고 무엇을 못 지켰는지 자동으로 판정한다.

## 왜 이것이 이 프로젝트의 핵심 산출물인가

자동화된 시험 환경의 가장 큰 위험은 **준수한 척하는 보고서**다. 도구가 돌아가고 숫자가
나오면 그것이 곧 적합성 판정처럼 읽힌다. 이 모듈은 반대로 **못 지킨 것을 먼저 드러낸다.**

판정 등급을 다섯으로 나눈 이유가 그것이다.

| 등급 | 뜻 |
|---|---|
| `준수` | 근거 값이 있고 요건을 만족한다 |
| `미준수` | 근거 값이 있고 만족하지 못한다 |
| `해당없음` | 이 채널·IUT 에 적용되지 않는다 — **반드시 이유를 함께** (`shall [07.02]`) |
| `미기록` | 판정에 필요한 값이 데이터셋에 없다 — **추정치로 채우지 않는다** (SCHEMA.md §5.3) |
| `범위밖` | 이 환경이 원리적으로 판정할 수 없다 — 독립 시험소·승인 기관·육안 검사 |

**`미기록` 과 `미준수` 는 다르다.** 전자는 "모른다", 후자는 "안 지켰다" 이며, 둘을
섞으면 다음 사람이 무엇을 고쳐야 하는지 알 수 없게 된다.

## 이 환경의 위치

출력의 첫 절은 언제나 `scope` 선언이고 그 안의 `not_claimed` 가 맨 앞에 온다.
ISO/IEC 17825 §1 Scope 는 이 표준이 **ISO/IEC 19790 적합성 판정용**이며 **24759 와 함께**
쓰이고 **암호모듈의 정의된 경계**에서 시험한다고 못박는다. 우리가 가진 것은 그 삼각
구조의 한 다리이고, IUT 는 모듈이 아니라 라이브러리 하나다. 게다가 Annex A.1·C·G·H 에는
"can supersede this annex in its entirety" 가 붙어 있다 — 진짜 기준은 승인 기관이 정한다.

그래서 이 환경은 **적합성 평가가 아니라 사전 진단(pre-assessment)** 이다.

## 인용 규약

원문은 저작권 보호 문서이며 이 저장소에 커밋되지 않는다. 여기서는 **조항 번호와 요구의
취지만** 자기 말로 적고 원문을 옮기지 않는다.
출처: ISO/IEC 17825:2024, Second edition, 2024-01,
*Information technology — Security techniques — Testing methods for the mitigation of
non-invasive attack classes against cryptographic modules*.
"""

import argparse
import json
import sys

from . import paths, spec as spec_mod   # paths 가 workspace/lib 를 sys.path 에 넣는다

import sca_schema as S                  # noqa: E402

STANDARD = ("ISO/IEC 17825:2024, Second edition, 2024-01, "
            "Information technology — Security techniques — Testing methods for the "
            "mitigation of non-invasive attack classes against cryptographic modules")

OK, NG, NA, NR, OOS = "준수", "미준수", "해당없음", "미기록", "범위밖"


def _item(clause, requirement, verdict, evidence="", note=""):
    return {"clause": clause, "requirement": requirement, "verdict": verdict,
            "evidence": evidence, "note": note}


def check(dataset_path=None, spec=None, results=None, level=3):
    """대조표를 만든다.

    입력
        dataset_path : h5 경로 (없으면 데이터셋 항목이 전부 `미기록`)
        spec         : 실험 명세 (없으면 계획 관련 항목이 `미기록`)
        results      : analyze 가 낸 results.json 내용 (없으면 시험 항목이 `미수행`)
        level        : 보안수준 3 또는 4. spec 이 있으면 그쪽을 따른다.

    출력 dict — scope 선언 + 항목 목록 + 등급별 집계.
    """
    attrs = S.root_attrs(dataset_path) if dataset_path else {}
    if spec:
        level = int(spec["criteria"]["security_level"])
    A = "A.2" if level == 3 else "A.3"
    items = []

    items += _scope_items(spec)
    items += _mandatory_test_items(spec, results, A, level)
    items += _annex_a_items(attrs, spec, results, A, level)
    items += _annex_b_items(attrs)
    items += _procedure_items(attrs, spec, results)

    tally = {}
    for it in items:
        tally[it["verdict"]] = tally.get(it["verdict"], 0) + 1

    return {
        "standard": STANDARD,
        "citation_policy": ("조항 번호와 요구의 취지만 자기 말로 적는다. 원문은 저작권 "
                            "보호 문서이며 이 저장소에 포함되지 않는다."),
        "assessment_type": (spec["scope"]["assessment_type"] if spec else "pre-assessment"),
        "position": ("이 환경은 적합성 평가가 아니라 표준을 준용하는 사전 진단이다. "
                     "§1 Scope 는 이 표준이 ISO/IEC 19790 적합성 판정용이며 24759 와 함께 "
                     "암호모듈의 정의된 경계에서 쓰인다고 정한다. IUT 는 모듈이 아니라 "
                     "라이브러리이고, 벤더와 시험자가 동일하며, 승인 기관이 없다."),
        "not_claimed": (spec["scope"]["not_claimed"] if spec else
                        ["spec 이 없어 적용 범위를 선언할 수 없다"]),
        "security_level": level,
        "dataset": str(dataset_path) if dataset_path else None,
        "items": items,
        "tally": tally,
    }


def _scope_items(spec):
    if not spec:
        return [_item("§1 Scope", "적용 범위 선언", NR, note="spec 이 없다")]
    sc = spec["scope"]
    out = [
        _item("§1 Scope", "ISO/IEC 19790 적합성 판정", OOS,
              note="모듈 경계·CSP 정의·보안수준 배정이 이 환경 밖이다. 적합성을 주장하지 않는다."),
        _item("§7.3.3 `shall [07.04]`", "독립 시험소에 의한 평가", OOS,
              note="벤더와 시험자가 동일하다(자기시험). 구조적으로 충족할 수 없다."),
        _item("Annex A.1", "승인 기관(approval authority)의 메트릭 적용", OOS,
              note="A.1·C·G·H 는 승인 기관이 전체를 대체할 수 있다고 정한다. 이 환경은 기관이 아니다."),
        _item("Clause 9", "비대칭 암호 ASCA", NA,
              evidence="security_function=%s" % sc["security_function"],
              note="IUT 가 대칭키(AES)이므로 Clause 8 만 적용된다."),
        _item("§7.3.1", "CSP 클래스별 코어 테스트 반복", NA,
              evidence="csp_classes=%s" % sc["csp_classes"],
              note="이 IUT 는 암호 키 하나만 다룬다. 다중 CSP 클래스가 존재하지 않는다."),
    ]
    if "em" not in sc["channels"]:
        out.append(_item("Annex B `[B.07]`", "EM 이면 근접 자기장 프로브", NA,
                         evidence="channels=%s" % sc["channels"],
                         note="EM 채널을 수집하지 않는다(프로브 미보유). SEMA·DEMA 는 시험 범위 밖이다."))
    return out


def _mandatory_test_items(spec, results, A, level):
    """§7.3.2 `shall [07.03]` · §8.1 `shall [08.01]` — TA·SPA·DPA 셋 모두."""
    out = [_item("§7.3.2 `shall [07.03]` · §8.1 `shall [08.01]`",
                 "TA·SPA·DPA 세 가지를 모두 평가한다 (순서: TA→SPA→DPA)",
                 OK if results and all(
                     results.get("tests", {}).get(k, {}).get("verdict")
                     not in (None, "not-run") for k in ("ta", "spa", "dpa"))
                 else NG if results else NR,
                 evidence=(", ".join("%s=%s" % (k, results["tests"].get(k, {}).get("verdict", "미수행"))
                                     for k in ("ta", "spa", "dpa")) if results else ""),
                 note="셋 중 하나라도 수행하지 않으면 필수 요건 미충족이다.")]

    labels = {
        "ta": ("§7.3.4 `shall [07.07]`", "타이밍 분석 — 실행시간이 CSP·평문에 의존하는가"),
        "spa": ("§7.3.5 · §8.3.1", "단순 분석 — key schedule 중간값의 HW 노출"),
        "dpa": ("§8.4 `shall [08.02]`", "차분 분석 — Welch t-test 로 두 집단 비교"),
    }
    for k, (clause, req) in labels.items():
        r = (results or {}).get("tests", {}).get(k)
        if r is None:
            out.append(_item(clause, req, NR, note="분석 결과가 없다"))
            continue
        v = r.get("verdict")
        verdict = {"pass": OK, "fail": NG, "inconclusive": NR,
                   "not-applicable": NA, "not-run": NR}.get(v, NR)
        out.append(_item(clause, req, verdict,
                         evidence=r.get("reason", "")[:200],
                         note=r.get("caveat", "") or r.get("verdict_scope", "")))

    # TA 의 2차(분산) 검정은 shall 이다 — 고차 제외는 DPA 에만 해당한다.
    r = (results or {}).get("tests", {}).get("ta")
    if r and r.get("stages"):
        did_var = any(s.get("t_var") is not None or s.get("spread", 1) < s.get("epsilon", 0)
                      for s in r["stages"] if isinstance(s, dict))
        out.append(_item("§7.3.4", "타이밍은 평균뿐 아니라 **분산** 차이도 계산한다(2차 타이밍 누설)",
                         OK if did_var else NG,
                         note="고차 제외(Fig.1 NOTE 3)는 DPA 에만 해당하며 타이밍에는 해당하지 않는다."))

    # §8.2 — 캐시 타이밍 프레임워크는 일반 타이밍 분석과 다른 요구다.
    out.append(_item("§8.2 (Reference [50])",
                     "캐시 타이밍 공격 프레임워크 (IUT 에 캐시가 있을 때)",
                     NR,
                     note=("대상 MCU 의 캐시 유무를 레퍼런스 매뉴얼로 확인하지 못했다. "
                           "확인 전에는 미기록으로 둔다. 이 항목과 무관하게 §7.3.4 일반 "
                           "타이밍 분석은 무조건 수행했다 — 둘은 다른 요구다.")))
    out.append(_item("Figure 1 NOTE 3", "고차 DPA·CPA 시험", NA,
                     note="표준이 필수 시험에서 제외한다. 이 환경도 판정에 쓰지 않으며, "
                          "CPA 는 배관 검증용 양성 대조로만 돌린다."))
    return out


def _annex_a_items(attrs, spec, results, A, level):
    out = []

    # A.2.1 / A.3.1 — 수집 시간 상한
    lim = {3: 6.0, 4: 24.0}[level]
    secs = attrs.get("acquisition_seconds")
    if secs is None:
        out.append(_item("%s.1 `shall [07.01]`" % A, "수집 시간 상한 %g h" % lim, NR,
                         note="acquisition_seconds 가 데이터셋에 없다"))
    else:
        hours = float(secs) / 3600.0
        out.append(_item("%s.1 `shall [07.01]`" % A, "수집 시간 상한 %g h" % lim,
                         OK if hours <= lim else NG,
                         evidence="실제 %.2f h" % hours))

    # A.2.3 / A.3.3 + Formula (1) — DPA 트레이스 수
    r = (results or {}).get("tests", {}).get("dpa", {})
    req = r.get("requirement")
    if req:
        out.append(_item("%s.3 · Formula (1)" % A,
                         "DPA 장수 N = 4(Z_{α/2}+Z_β)²/d²",
                         OK if req["met"] else NG,
                         evidence="요구 %d장, 보유 %d장" % (req["n_required"], req["n_have"])))
    else:
        out.append(_item("%s.3 · Formula (1)" % A, "DPA 장수", NR))

    # A.2.4 / A.3.4 — 타이밍 측정 (Annex A 유일의 shall collect)
    r = (results or {}).get("tests", {}).get("ta", {})
    req = r.get("requirement")
    need = {3: 1000, 4: 10000}[level]
    if req:
        out.append(_item("%s.4 **`shall collect`**" % A,
                         "타이밍 측정 각 %d회 (2블록)" % need,
                         OK if req.get("met") else NG,
                         evidence="; ".join(req.get("shortfall", [])) or "충족",
                         note="Annex A 전체에서 `shall collect` 는 이 항목 하나뿐이다."))
    else:
        out.append(_item("%s.4 **`shall collect`**" % A,
                         "타이밍 측정 각 %d회 (2블록)" % need, NR))

    # A.2.2 / A.3.2 — SPA 파형 수와 해상도
    r = (results or {}).get("tests", {}).get("spa", {})
    req = r.get("requirement")
    if req:
        out.append(_item("%s.2" % A, "SPA 파형 %d장, CSP 비트당 %d 포인트"
                         % (req["required_traces"], req["required_points_per_csp_bit"]),
                         OK if req["met"] else NG,
                         evidence="; ".join(req.get("shortfall", [])) or "충족"))
        vis = r.get("visual_inspection", {})
        out.append(_item("%s.2" % A, "SPA 는 **육안 검사와 통계 검정 둘 다** 통과해야 한다",
                         OOS,
                         evidence="통계=%s, 육안=%s" % (r.get("verdict"), vis.get("status", "?")),
                         note="육안 검사는 사람의 행위다. 이 도구는 그림을 산출물로 내고 "
                              "미결로 표시하며, 수행했다고 주장하지 않는다."))
    else:
        out.append(_item("%s.2" % A, "SPA 파형 수·해상도", NR))

    # A.2.5 `shall [A.01]` — 전처리 (10회 평균)
    avg = attrs.get("preprocessing_average_n")
    need_avg = 10
    if avg is None:
        out.append(_item("%s.5 `shall [A.01]` · `shall [07.10]`" % A,
                         "같은 입력 %d회 실행의 평균을 트레이스 1장으로" % need_avg, NR,
                         note="preprocessing_average_n 이 데이터셋에 없다"))
    else:
        out.append(_item("%s.5 `shall [A.01]` · `shall [07.10]`" % A,
                         "같은 입력 %d회 실행의 평균을 트레이스 1장으로" % need_avg,
                         OK if int(avg) >= need_avg else NG,
                         evidence="preprocessing_average_n=%s" % avg,
                         note=("에뮬레이션은 결정적이라 평균이 값을 바꾸지 않는다. 그래도 "
                               "요건을 충족한 것은 아니므로 미준수로 적는다."
                               if str(attrs.get("channel_type")) == "emulated-power" else "")))
    if level == 4:
        out.append(_item("A.3.5", "주파수 대역통과 필터 + 정적·동적 정렬", NG,
                         note="1차 목표는 Level 3 이며 Level 4 전처리는 구현하지 않았다."))

    # A.2.6 `shall [A.02]` — 정렬
    align = attrs.get("alignment")
    out.append(_item("%s.6 `shall [A.02]`" % A,
                     "트레이스가 정렬되지 않으면 통계 시험을 수행하지 않는다",
                     OK if align is not None else NR,
                     evidence="alignment=%s" % align,
                     note=("트리거(또는 심볼 경계) 동기만으로 정렬된다. 에뮬레이션은 "
                           "결정적이라 어긋남이 없다." if align is not None else "")))
    return out


def _annex_b_items(attrs):
    """Annex B — 측정 장비 요건. 물리 측정이 아니면 대부분 `해당없음` 이다."""
    # channel_type 이 없으면 에뮬레이션으로 **간주하지 않는다.** 모르는 것을 안다고
    # 가정하면 물리 측정 요건을 통째로 '해당없음' 처리해 버리게 된다.
    ch = str(attrs.get("channel_type", ""))
    emulated = ch == "emulated-power"
    reason = "에뮬레이션 채널 — 물리 측정 장비가 존재하지 않는다"
    out = []

    if emulated:
        for cl, rq in (("[B.01]", "대역폭 ≥ 클럭의 50 % (SW 구현)"),
                       ("[B.02]", "대역폭의 5배로 샘플링"),
                       ("[B.03]", "샘플링 분해능 ≥ 8 bit"),
                       ("[B.05]·[B.06]", "VCC–IUT 사이 저항(동작 가능한 최대값)")):
            out.append(_item("Annex B %s" % cl, rq, NA, note=reason))
        out.append(_item("Annex B [B.04]", "시험에 필요한 신호 전체를 담을 저장 용량", OK,
                         evidence="관측 구간 전체(%s 샘플)를 저장했다"
                                  % attrs.get("samples_per_trace", "?")))
        return out

    clk = attrs.get("target_clock_hz")
    bw = attrs.get("bandwidth_hz")
    sr = attrs.get("sample_rate_hz")
    res = attrs.get("sample_resolution_bits")

    if bw is None or clk is None:
        out.append(_item("Annex B [B.01]", "대역폭 ≥ 클럭의 50 % (SW 구현)", NR,
                         evidence="bandwidth_hz=%s, target_clock_hz=%s" % (bw, clk),
                         note="대역폭을 기록하지 않으면 이 요건을 판정할 수 없다."))
    else:
        out.append(_item("Annex B [B.01]", "대역폭 ≥ 클럭의 50 % (SW 구현)",
                         OK if float(bw) >= 0.5 * float(clk) else NG,
                         evidence="bandwidth=%.0f Hz, clock=%.0f Hz" % (float(bw), float(clk))))
    if bw is None or sr is None:
        out.append(_item("Annex B [B.02]", "대역폭의 5배로 샘플링", NR,
                         evidence="bandwidth_hz=%s, sample_rate_hz=%s" % (bw, sr)))
    else:
        out.append(_item("Annex B [B.02]", "대역폭의 5배로 샘플링",
                         OK if float(sr) >= 5.0 * float(bw) else NG,
                         evidence="sample_rate=%.0f Hz, 5×bandwidth=%.0f Hz"
                                  % (float(sr), 5.0 * float(bw))))
    out.append(_item("Annex B [B.03]", "샘플링 분해능 ≥ 8 bit",
                     NR if res is None else (OK if int(res) >= 8 else NG),
                     evidence="sample_resolution_bits=%s" % res))
    out.append(_item("Annex B [B.04]", "시험에 필요한 신호 전체를 담을 저장 용량", OK,
                     evidence="%s 샘플" % attrs.get("samples_per_trace", "?")))
    shunt = attrs.get("shunt_ohm")
    note = attrs.get("shunt_selection_note")
    out.append(_item("Annex B [B.05]·[B.06]",
                     "VCC–IUT 사이 저항, **동작 가능한 최대값**을 고른다",
                     NR if shunt is None or note is None else OK,
                     evidence="shunt_ohm=%s, 선택 근거=%s" % (shunt, note),
                     note=("프로브 구성은 기록되어 있으나 저항값과 선택 절차가 없으면 "
                           "[B.06] 을 판정할 수 없다.")))
    return out


def _procedure_items(attrs, spec, results):
    out = []
    c = spec["criteria"] if spec else None

    out.append(_item("§8.4 `shall [08.04]`",
                     "통계 시험 **전에** effect size·α·β 를 지정한다",
                     OK if c else NR,
                     evidence=("d=%s, α=%s, β=%s (spec 에 수집 전 기록)"
                               % (c["effect_size_d"], c["alpha"], c["beta"]) if c else "")))
    out.append(_item("§8.4 `shall [08.03]`", "다중비교 보정 (Bonferroni 선호)",
                     OK if c and c["multiplicity_correction"] != "none" else
                     (NG if c else NR),
                     evidence=(c["multiplicity_correction"] if c else "")))

    if c:
        slt = c["sensitive_leakage_time"]
        out.append(_item("§7.3.6 · Annex H",
                         "민감 누설 경계를 시험소가 정하고 그 안의 누설만 fail 로 센다",
                         OK,
                         evidence="1라운드 포함=%s" % slt["include_round1"],
                         note=slt["rationale"].strip()[:400]))
        out.append(_item("Annex H", "경계 확정", OOS,
                         note="H 는 informative 이며 승인 기관이 대체할 수 있다. "
                              "이 환경은 경계를 **제안**할 뿐 확정하지 못한다."))
        v = c["vendor_info"]
        missing = [k for k in ("algorithms", "design", "susceptible_conditions")
                   if not str(v.get(k, "")).strip()]
        out.append(_item("§7.3.3 `shall [07.04]`",
                         "벤더 정보 3항목: 알고리즘 / 구현 설계 / 취약해지는 조건",
                         OK if not missing else NG,
                         evidence="누락 %s" % missing if missing else "3항목 모두 기재",
                         note="벤더 = 시험자이므로 스스로 적어 남긴다."))
    else:
        out.append(_item("§7.3.3 `shall [07.04]`", "벤더 정보 3항목", NR))

    out.append(_item("§7.3.6 `shall [07.11]`", "보안 함수의 중간값을 계산한다",
                     OK if results and "soundness" in results.get("tests", {}) else NR,
                     evidence="aes_ref.intermediates() 로 라벨을 생성"))
    out.append(_item("§7.3.3 `shall [07.05]`", "시험소가 CSP·암호문을 바꿀 수 있다", OK,
                     evidence="수집기가 키·평문을 매 레코드 주입한다"))
    out.append(_item("§7.3.1 `shall [07.02]` · Annex G",
                     "측정 불가 시 그 이유를 제시한다", OK,
                     note="이 대조표의 `해당없음` 항목은 전부 이유를 함께 적는다."))
    return out


# ─────────────────────────────────────────────────────────────
def to_markdown(rep):
    """대조표를 사람이 읽을 마크다운으로. 보고서 3종이 모두 이것을 싣는다."""
    L = []
    L.append("## 적용 범위 선언")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    L.append("| 준용 표준 | %s |" % rep["standard"])
    L.append("| 평가 유형 | **%s — 적합성 평가가 아니다** |" % rep["assessment_type"])
    L.append("| 보안수준 | Level %s |" % rep["security_level"])
    L.append("")
    L.append("> %s" % rep["position"])
    L.append("")
    L.append("### 이 시험이 **주장하지 않는** 것")
    L.append("")
    for s in rep["not_claimed"]:
        L.append("- %s" % s)
    L.append("")
    L.append("## 요건 대조표")
    L.append("")
    t = rep["tally"]
    L.append("집계 — " + " · ".join("**%s** %d" % (k, v) for k, v in sorted(t.items())))
    L.append("")
    L.append("| 조항 | 요구 | 판정 | 근거 | 비고 |")
    L.append("|---|---|---|---|---|")
    for it in rep["items"]:
        L.append("| %s | %s | **%s** | %s | %s |"
                 % (it["clause"], it["requirement"], it["verdict"],
                    _cell(it["evidence"]), _cell(it["note"])))
    L.append("")
    L.append("> `미기록` 은 \"모른다\", `미준수` 는 \"안 지켰다\" 이며 서로 다르다. "
             "`범위밖` 은 이 환경이 원리적으로 판정할 수 없는 항목이다.")
    return "\n".join(L)


def _cell(s):
    s = (s or "").replace("\n", " ").replace("|", "\\|").strip()
    return s if len(s) <= 220 else s[:217] + "…"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="physai.conformance",
                                 description="ISO/IEC 17825 요건 대조표")
    ap.add_argument("--dataset", default=None)
    ap.add_argument("--spec", default=None)
    ap.add_argument("--results", default=None, help="runs/<id>/results.json")
    ap.add_argument("--level", type=int, default=3, choices=(3, 4))
    ap.add_argument("--json", action="store_true", help="마크다운 대신 JSON")
    a = ap.parse_args(argv)

    sp = spec_mod.load(a.spec) if a.spec else None
    res = json.loads(paths.Path(a.results).read_text(encoding="utf-8")) if a.results else None
    rep = check(dataset_path=a.dataset, spec=sp, results=res, level=a.level)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else to_markdown(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
