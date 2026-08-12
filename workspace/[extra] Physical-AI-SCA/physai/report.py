"""보고서 3종과 증거 번들을 만든다.

    python3 -m physai.report --run <spec-id>

| 산출물 | 생성 시점 | 무엇을 담나 |
|---|---|---|
| `01_experiment_plan.md` | **수집 전** | 적용 범위 선언 · 요건 대조표 · 판정 기준 · 트레이스 수 산정 근거 |
| `02_analysis_report.md` | 분석 후 | 필수 시험 3종 결과 · 결함 후보(명령어 주소) · 갱신된 대조표 |
| `03_evidence_manifest.md` + `manifest.json` | 마지막 | 모든 파일의 sha256 · 생성 명령 · 툴체인 · 재현 절차 |

## 계획 보고서를 수집 **전에** 만드는 이유

결과를 본 뒤 판정 기준을 고르는 사후 정당화를 구조로 막기 위해서다.
ISO/IEC 17825 §8.4 `shall [08.04]` 도 통계 시험 전에 effect size·α·β 를 지정하라고
요구한다. `collect` 가 수집을 시작하기 전에 이 파일을 먼저 쓴다.

## LLM 이 관여하는 곳

**서술 초안뿐이다.** 수치·판정·해시·대조표는 전부 도구가 만든다. `llm.py` 의 환경변수가
설정되어 있지 않으면 서술 칸이 비고 나머지는 다 채워진 문서가 나온다 —
**LLM 이 없어도 산출물은 나온다.**
"""

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time

import numpy as np

from . import conformance, llm, paths, spec as spec_mod

# SVG 안의 래스터 요소를 화면에서 읽을 수 있게 하는 렌더링 해상도다. 판정 수치에는
# 영향을 주지 않으며 보고서 파일 크기가 불필요하게 커지지 않는 수준으로 둔다.
FIG_DPI = 110


# ─────────────────────────────────────────────────────────────
# 01 실험 계획 보고서 — 수집 전
# ─────────────────────────────────────────────────────────────
def write_plan(spec, out_dir, dataset_path=None):
    """수집 전에 확정할 기준을 `01_experiment_plan.md`로 기록한다.

    검증된 `spec`과 선택적 Dataset 경로를 받아 `out_dir`을 만들고 기존 계획 보고서를
    덮어쓴다. 보통 이 시점에는 Dataset이 없어 대조표가 `미기록`이다. 파일 쓰기·명세
    계산 실패는 호출자에게 전파되며 생성된 `Path`를 반환한다.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    rep = conformance.check(dataset_path=dataset_path, spec=spec, results=None,
                            level=spec["criteria"]["security_level"])
    need = spec_mod.required_n(spec["criteria"])
    c = spec["criteria"]

    L = ["# 실험 계획 보고서 — %s" % spec["title"], "",
         "| | |", "|---|---|",
         "| spec id | `%s` |" % spec["id"],
         "| 생성 | %s |" % time.strftime("%Y-%m-%d %H:%M:%S"),
         "| 문서 성격 | **수집 전에 작성한다.** 결과를 본 뒤 판정 기준을 고치는 일이 "
         "구조적으로 불가능하도록 순서를 고정한 것이다. |", ""]

    if spec.get("rationale"):
        L += ["## 이 실험을 하는 이유", "", spec["rationale"].strip(), ""]

    L += [conformance.to_markdown(rep), ""]

    L += ["## 판정 기준 (수집 전 확정)", "",
          "| 항목 | 값 | 근거 |", "|---|---|---|",
          "| 보안수준 | Level %d | Annex %s |" % (c["security_level"],
                                                 "A.2" if c["security_level"] == 3 else "A.3"),
          "| 표준화 효과크기 d | %s | A.%d.3 |" % (c["effect_size_d"],
                                                2 if c["security_level"] == 3 else 3),
          "| 위양성률 α | %s | §8.4 |" % c["alpha"],
          "| 위음성률 β | %s | §8.4 — 낮게 잡는다. 누설을 놓치지 않는 것이 우선이다 |" % c["beta"],
          "| 다중비교 보정 | %s | §8.4 `shall [08.03]` |" % c["multiplicity_correction"],
          "| t 임계 (보정 전) | %s | §8.4 — 99.999 %% |" % c["t_threshold"],
          "| 수집 시간 상한 | %s h | %s.1 `shall [07.01]` |"
          % (c["max_acquisition_hours"], "A.2" if c["security_level"] == 3 else "A.3"),
          "| 전처리 평균 | %d회 | A.2.5 `shall [A.01]` 은 10회를 요구한다 |"
          % c["preprocessing"]["average_n"],
          "| 정렬 | %s | A.2.6 `shall [A.02]` |" % c["preprocessing"]["alignment"], "",
          "### 필요 장수 — 판단이 아니라 계산 결과", "",
          "```", "%s" % need["formula"],
          "Z_(α/2) = %.4f,  Z_β = %.4f,  d = %s" % (need["z_alpha_half"], need["z_beta"],
                                                    c["effect_size_d"]),
          "N = %d" % need["n_required"], "```", "",
          "출처: %s. 장수를 spec 에 적지 않고 여기서 계산하는 이유는, 그것이 α·β·d 의 "
          "**결과**이지 별도의 판단이 아니기 때문이다. 따로 적으면 파라미터와 어긋날 수 있다."
          % need["source"], ""]

    L += ["## 민감 누설 경계 (Annex H)", "",
          "| | |", "|---|---|",
          "| 1라운드 포함 | **%s** |" % ("예" if c["sensitive_leakage_time"]["include_round1"] else "아니오"),
          "| 시작 | `%s` |" % c["sensitive_leakage_time"].get("from", "0"),
          "| 끝 | `%s` |" % c["sensitive_leakage_time"].get("to", "end"), "",
          "**근거**", "", c["sensitive_leakage_time"]["rationale"].strip(), "",
          "> Annex H 는 informative 이며 승인 기관이 대체할 수 있다. 이 경계는 **제안**이고 "
          "확정은 사람·기관의 몫이다. 그러나 경계가 합/부를 직접 바꾸므로 그 판단을 여기 남긴다.", ""]

    v = c["vendor_info"]
    L += ["## 벤더 정보 (§7.3.3 `shall [07.04]`)", "",
          "> 이 환경은 **벤더와 시험자가 동일**하다. 표준이 상정한 구도가 아니므로, "
          "정보를 받는 대신 스스로 적어 남긴다. 이 사실 자체가 적합성 평가가 될 수 없는 이유다.", "",
          "**(a) 구현 알고리즘**", "", v["algorithms"].strip(), "",
          "**(b) 구현 설계**", "", v["design"].strip(), "",
          "**(c) 부채널에 취약해지는 조건·모드**", "", v["susceptible_conditions"].strip(), ""]

    L += ["## 수집 계획", "", "| Subset | role | 장수 | 키 | 평문 |", "|---|---|---|---|---|"]
    for s in spec["subsets"]:
        L.append("| `%s` | %s | %d | %s | %s |"
                 % (s["name"], s["role"], s["n"], s["key_mode"], s["pt_mode"]))
    L += ["", "## 수행할 시험", "",
          "| 분석 | 지위 |", "|---|---|"]
    grade = {"ta": "**필수 판정**", "spa": "**필수 판정**", "dpa": "**필수 판정**",
             "soundness": "판정 (에뮬 채널의 1차 누설 검출)",
             "snr": "보조 — 판정에 쓰지 않음",
             "cpa": "양성 대조 — 배관 검증용. 표준상 필수 시험이 아니다"}
    for a in spec["analyses"]:
        L.append("| `%s` | %s |" % (a, grade.get(a, "?")))
    L += ["", "필수 시험은 **TA → SPA → DPA** 순서로 수행한다(§7.3.2). 다만 그 조항의 순서는 "
          "권고(`should`)이고 **셋 모두 평가하는 것이 의무**(§8.1 `shall [08.01]`)이므로, "
          "앞 시험이 fail 이어도 뒤 시험을 계속 수행한다 — 어디가 얼마나 새는지를 알아야 "
          "고칠 수 있기 때문이다.", ""]

    p = out_dir / "01_experiment_plan.md"
    p.write_text("\n".join(L), encoding="utf-8")
    return p


# ─────────────────────────────────────────────────────────────
# 02 분석 결과 보고서
# ─────────────────────────────────────────────────────────────
def write_analysis(spec, results, out_dir, dataset_path):
    """분석 결과와 증거 그림을 `02_analysis_report.md`로 기록한다.

    `results`의 수치·판정을 문장으로 재구성할 뿐 새 판정을 만들지 않는다. 출력 디렉터리와
    그림 파일을 생성하고 기존 동명 보고서를 덮어쓴다. Dataset·명세는 변경하지 않으며
    필수 결과가 없거나 파일 쓰기에 실패하면 예외가 전파된다.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = _make_figures(spec, results, out_dir, dataset_path)
    rep = conformance.check(dataset_path=dataset_path, spec=spec, results=results,
                            level=spec["criteria"]["security_level"])

    tests = results["tests"]
    overall = ("fail" if any(t.get("verdict") == "fail" for t in tests.values())
               else "inconclusive" if any(t.get("verdict") == "inconclusive" for t in tests.values())
               else "pass")

    L = ["# 분석 결과 보고서 — %s" % results["title"], "",
         "| | |", "|---|---|",
         "| spec id | `%s` |" % results["spec_id"],
         "| Dataset | `%s` |" % paths.Path(results["dataset"]).name,
         "| 분석 시각 | %s |" % results["generated"],
         "| **종합** | **%s** |" % overall, ""]

    L += [conformance.to_markdown(rep), ""]

    L += ["## 필수 시험 3종 (§7.3.2 `shall [07.03]`)", ""]
    for k, title in (("ta", "TA — 타이밍 분석 (constant-time 검증)"),
                     ("spa", "SPA — 단순 분석 (key schedule 표적)"),
                     ("dpa", "DPA — 차분 분석 (Welch t-test)")):
        r = tests.get(k, {})
        L += ["### %s" % title, "",
              "**판정: %s**  %s" % (r.get("verdict", "미수행"),
                                  r.get("verdict_qualified", "")), ""]
        if r.get("reason"):
            L += ["> %s" % r["reason"], ""]
        if k == "ta":
            L += _ta_body(r)
        elif k == "spa":
            L += _spa_body(r)
        else:
            L += _dpa_body(r, figs)
        if r.get("caveat"):
            L += ["> **한계**: %s" % r["caveat"], ""]

    if "soundness" in tests:
        L += _soundness_body(tests["soundness"], figs)

    if results.get("reference", {}).get("cpa"):
        c = results["reference"]["cpa"]
        L += ["## 양성 대조 — CPA (판정 아님)", "",
              "> %s" % c["note"], "",
              "| | |", "|---|---|",
              "| 복구 바이트 | **%d / 16** |" % c["bytes_recovered"],
              "| 평균 순위 | %.1f |" % c["mean_rank"],
              "| 트레이스 | %d |" % c["n_traces"], "",
              "복구 키: `%s`" % c["recovered_key"], "",
              "정답 키: `%s`" % c["true_key"], ""]
        if c["bytes_recovered"] == 16:
            L += ["> 배관(입력 주입·정렬·라벨링)이 정상이라는 뜻이다. "
                  "이 대조가 실패하면 데이터가 아니라 도구를 먼저 의심해야 한다.", ""]
        else:
            L += ["> 마스킹 등으로 키가 복구되지 않는 것은 정상일 수 있다. "
                  "**이 수치는 판정 근거가 아니다** — 표준은 누설 관측만으로 판정한다(§7.2).", ""]

    L += _narrative(results, overall)

    L += ["## 이 시험이 본 고리와 보지 않은 고리", "",
          "| 고리 | 본 도구 | 이번에 봤나 |", "|---|---|---|",
          "| 이론 (마스킹 수식) | 논문·형식 검증 | **아니오** — 범위 밖 |",
          "| 구현 (소스→기계어) | 에뮬레이션 | %s |"
          % ("예" if "soundness" in tests else "아니오"),
          "| 물리 (실제 칩) | 실물 전력 수집 | **아니오** — 실장비 미구성 |",
          "| 실행 흐름 | 디버그 트레이스 | **아니오** — 실장비 미구성 |", "",
          "> **어느 하나가 깨끗하다는 사실만으로 안전을 주장할 수 없다.** 에뮬레이션의 HW/HD "
          "모델은 글리치·커플링 같은 물리 효과를 담지 않으므로, 여기서 깨끗해도 실물에서 샐 수 "
          "있다. 반대로 실측에서 잡음에 묻힌 누설이 여기서는 보인다. 세 관측은 상보재다.", "",
          "> **DPA 는 1차 한정이다.** 고차 DPA 는 ISO/IEC 17825 Fig.1 NOTE 3 에 따라 필수 "
          "시험이 아니며, 1차 부울 마스킹이 2차에서 뚫리는 것은 이론적으로 정상이라 결함으로 "
          "보고할 수 없다. **단 TA 의 2차(분산) 검정은 `shall` 이므로 수행했다.**", ""]

    p = out_dir / "02_analysis_report.md"
    p.write_text("\n".join(L), encoding="utf-8")
    return p


def _narrative(results, overall):
    """해석 서술 — **LLM 이 관여하는 유일한 곳.**

    수치·판정·해시·대조표는 전부 도구가 만들었고, 여기서는 그것을 사람이 읽을 문장으로
    옮기기만 한다. 환경변수가 없으면 이 절은 **왜 비었는지**를 적고 넘어간다 —
    LLM 이 없어도 문서의 사실관계는 그대로 유효하다.

    LLM 이 쓴 문장은 반드시 그 사실을 표시한다. 표시하지 않으면 다음 사람이 그것을
    도구가 계산한 결과로 오해한다.
    """
    L = ["## 해석 (서술)", ""]
    if not llm.available():
        L += ["> %s" % llm.why_unavailable(), "",
              "> 설정하려면 `PHYSAI_LLM_BASE_URL`·`PHYSAI_LLM_MODEL` 을 준다 "
              "(온라인·오프라인 어느 쪽이든 OpenAI 호환 엔드포인트면 된다).", ""]
        return L

    facts = json.dumps({
        "종합": overall,
        "판정": {k: v.get("verdict") for k, v in results["tests"].items()},
        "근거": {k: v.get("reason", "")[:200] for k, v in results["tests"].items()},
        "적용범위_주장하지_않음": results["scope"]["not_claimed"],
    }, ensure_ascii=False, indent=1)
    prompt = (
        "아래는 부채널 사전 진단 도구가 계산한 결과다. 이것을 근거로 3~5문장의 한국어 "
        "요약을 써라.\n"
        "규칙: (1) 주어진 수치와 판정만 쓰고 새 수치를 만들지 마라. "
        "(2) inconclusive 를 안전하다고 바꿔 쓰지 마라. "
        "(3) 적합성(conformance)을 주장하지 마라 — 이것은 사전 진단이다. "
        "(4) 수행하지 않은 시험을 했다고 쓰지 마라.\n\n" + facts)
    try:
        text = llm.complete(prompt, system="너는 부채널 평가 보고서를 쓰는 조수다.")
    except RuntimeError as e:
        L += ["> LLM 호출에 실패했다: %s" % e, "",
              "> 수치·판정·대조표는 도구가 만들었으므로 이 문서의 사실관계는 그대로 유효하다.", ""]
        return L
    cfg = llm.describe_config()
    L += ["> **아래 문단은 LLM 이 생성한 서술 초안이다** (`%s` / `%s`). "
          "수치·판정·대조표는 전부 도구가 만든 것이며, 이 문단은 그것을 옮긴 것에 지나지 "
          "않는다. 사람이 대조해 검토한다." % (cfg["model"], cfg["base_url"]), "",
          text.strip(), ""]
    return L


def _ta_body(r):
    """TA 결과 사전을 단계별 판정과 계측 요건 Markdown 줄로 변환한다."""
    if not r.get("stages"):
        return [""]
    L = ["| 단계 | subset | 판정 | 실행시간 min–max | 고유값 | 근거 |",
         "|---|---|---|---|---|---|"]
    for s in r["stages"]:
        L.append("| %s | `%s` | **%s** | %s–%s | %s | %s |"
                 % (s.get("stage", "?"), s.get("subset", "-"), s.get("verdict", "?"),
                    s.get("min", "-"), s.get("max", "-"), s.get("unique_values", "-"),
                    _c(s.get("reason", ""))))
    L += ["", "계측: **%s**, ε = %s" % (r.get("instrument"), r.get("epsilon")), ""]
    req = r.get("requirement", {})
    L += ["요건 %s — 블록당 %s회 (%s)" % (req.get("clause", ""),
                                       req.get("required_per_block", "?"),
                                       "충족" if req.get("met") else "; ".join(req.get("shortfall", []))), ""]
    return L


def _spa_body(r):
    """SPA 결과를 통계 소견과 미결 육안 검사 상태가 함께 보이도록 변환한다."""
    L = ["관측 재현성(같은 입력 쌍의 최대 절대차) = **%s** — %s" %
         (r.get("noise_floor"), r.get("noise_floor_note", "")), ""]
    if r.get("findings"):
        L += ["| 쌍 종류 | subset | 최대 절대차 | 구별 가능 | key schedule 구간 |",
              "|---|---|---|---|---|"]
        for f in r["findings"]:
            L.append("| %s | `%s` | %s | %s | %s |"
                     % (f["pair_kind"], f["subset"], f["max_abs_diff"],
                        "예" if f["distinguishable"] else "아니오",
                        f.get("key_schedule_max_abs_diff", "-")))
        L.append("")
    vis = r.get("visual_inspection", {})
    L += ["> **육안 검사: %s**" % vis.get("status", "?"), ">",
          "> %s" % vis.get("required_by", ""), ">",
          "> %s 근거 자료: `%s`" % (vis.get("note", ""), vis.get("artifact", "")), ""]
    return L


def _dpa_body(r, figs):
    """DPA 결과를 임계·Trace 수 부족·검정 불가 Sample을 구분한 Markdown으로 만든다."""
    if r.get("verdict") in (None, "not-applicable", "not-run"):
        return [""]
    L = ["| | |", "|---|---|",
         "| 집단 | 고정 `%s` (%d장) vs 랜덤 `%s` (%d장) |"
         % (r["groups"]["fixed"], r["groups"]["n_fixed"],
            r["groups"]["random"], r["groups"]["n_random"]),
         "| \\|t\\|max | **%s** (샘플 %s) |" % (_num(r["abs_t_max"], "%.2f"),
                                              r["abs_t_max_index"]),
         "| 보정 임계 | %.3f (보정 전 %.1f, m=%d, %s) |"
         % (r["threshold"]["threshold"], r["threshold"].get("threshold_uncorrected", 0),
            r["threshold"]["n_tests"], r["threshold"]["correction"]),
         "| 임계 초과 샘플 | %d |" % r["n_over_threshold"],
         "| 검정 불가(0/0) 샘플 | %s |" % r.get("n_undefined", "—"),
         "| 필요 장수 | %d (보유 %d) |" % (r["requirement"]["n_required"],
                                       r["requirement"]["n_have"]), ""]
    if r.get("n_undefined"):
        L += ["> 검정 불가 샘플 %d개는 두 집단이 모두 상수라 t 를 정의할 수 없는 지점이다"
              "(잡음 없는 에뮬레이션의 구조적 특성). **\"누설 없음\" 이 아니라 \"검정할 수 "
              "없음\"** 이므로 초과로 세지 않았다. 실측 채널에서는 잡음 때문에 거의 생기지 않는다."
              % r["n_undefined"], ""]
    if "dpa" in figs:
        L += ["![DPA t-test](%s)" % figs["dpa"], ""]
    if not r["requirement"]["met"]:
        L += ["> **장수가 Formula (1) 요구에 못 미친다.** 검정력이 모자라므로 "
              "\"누설 없음\" 을 주장할 수 없다. 이 결과는 `inconclusive` 이며, "
              "누설이 관측되었다면 그 사실만은 유효하다(관측된 것은 관측된 것이다).", ""]
    return L


def _soundness_body(r, figs):
    """연구자 관점 soundness 결과와 명령어별 결함 후보를 Markdown으로 만든다."""
    L = ["## soundness — 구현 층 1차 누설 검출 (판정)", "",
         "**판정: %s**" % r["verdict"], "",
         "> 검사하는 명제: %s" % r["proposition"], "",
         "> 관점: %s" % r["perspective"], "",
         "| | |", "|---|---|",
         "| subset | `%s` (%d장) |" % (r["subset"], r["n_traces"]),
         "| 차수 | %d차 한정 |" % r["order"],
         "| 임계 산정 | %s |" % r["threshold_method"],
         "| 민감 경계 | 명령어 %s |" % r.get("sensitive_window"), ""]
    L += ["| 민감값 | SNR max | 귀무 임계 | 초과 샘플 | 경계 안 | 경계 밖 |",
          "|---|---|---|---|---|---|"]
    for name, x in r["labels"].items():
        if "error" in x:
            L.append("| `%s` | %s | — | — | — | **%s** |"
                     % (name, _num(x.get("snr_max")), _c(x["error"])))
            continue
        L.append("| `%s` | %s | %s | %d | **%d** | %d |"
                 % (name, _num(x["snr_max"]), _num(x["null_threshold"]), x["n_over"],
                    x["n_over_in_window"], x["n_over_outside_window"]))
    L.append("")
    if any(isinstance(x, dict) and x.get("snr_max") in ("+inf", float("inf"))
           for x in r["labels"].values()):
        L += ["> SNR 이 무한대인 것은 오류가 아니다. 잡음 없는 에뮬레이션에서 클래스 내 분산이 "
              "0 이라는 뜻이며, 그 샘플이 민감값에 **완전히 결정적으로 종속**한다는 가장 강한 "
              "누설의 표시다. 실측 채널에서는 잡음 때문에 유한한 값이 나온다.", ""]
    if "soundness" in figs:
        L += ["![soundness SNR](%s)" % figs["soundness"], ""]

    cand = [c for c in r["candidates"] if c["in_sensitive_window"]]
    if cand:
        L += ["### 결함 후보 — 민감 경계 안 (상위 %d개)" % min(30, len(cand)), "",
              "| 명령어 주소 | 성분 | 명령어 # | 민감값 | 통계량 | 임계 |",
              "|---|---|---|---|---|---|"]
        for c in sorted(cand, key=_stat_key, reverse=True)[:30]:
            L.append("| `%s` | %s | %d | `%s` | %s | %s |"
                     % (c["address"], c["component"], c["instruction_index"],
                        c["label"], _num(c["statistic"]), _num(c["threshold"])))
        L += ["", "> 주소는 `emul_harness/build/<IUT>.elf` 기준이다. "
              "`arm-none-eabi-addr2line -e <elf> <주소>` 로 소스 행을 찾을 수 있다 "
              "(하네스는 `-gdwarf-2` 로 빌드한다).", ""]
    out = [c for c in r["candidates"] if not c["in_sensitive_window"]]
    if out:
        L += ["### 민감 경계 **밖**의 검출 (%d개) — fail 로 세지 않는다" % len(out), "",
              "> Annex H 에 따라 경계 밖의 누설은 판정에 넣지 않는다. 다만 감추지도 않는다 — "
              "경계 설정이 옳았는지 다음 사람이 다시 볼 수 있어야 한다.", "",
              "| 명령어 주소 | 성분 | 명령어 # | 민감값 | 통계량 |", "|---|---|---|---|---|"]
        for c in sorted(out, key=_stat_key, reverse=True)[:15]:
            L.append("| `%s` | %s | %d | `%s` | %s |"
                     % (c["address"], c["component"], c["instruction_index"],
                        c["label"], _num(c["statistic"])))
        L.append("")
    return L


# ─────────────────────────────────────────────────────────────
# 03 증거 번들
# ─────────────────────────────────────────────────────────────
def write_evidence(spec, out_dir, dataset_path):
    """증거 파일의 해시·툴체인·재현 명령을 JSON과 Markdown으로 기록한다.

    `manifest.json`이 기계 판독 정본이고 `03_evidence_manifest.md`는 사람이 읽는 파생물이다.
    자기참조 해시는 만들지 않으며, 기존 두 파일은 덮어쓴다. Dataset과 ELF는 읽기만 한다.
    누락된 선택 파일은 제외하고 파일 I/O 실패는 호출자에게 전파한다.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    # 자기 자신을 목록에 넣지 않는다.
    #
    # `manifest.json` 은 자기 해시를 자기 안에 담을 수 없다(순환). 그리고
    # `03_evidence_manifest.md` 는 이 함수가 **manifest 를 만든 뒤에** 다시 쓰므로,
    # 목록에 넣으면 기록된 해시가 항상 실제와 어긋난다 — verify 가 매번 실패한다.
    # (실제로 그 버그가 있었고 verify 가 잡아냈다.)
    #
    # 무결성이 손상되지 않는 이유: `manifest.json` 이 정본이고 `03_…md` 는 그것을
    # 사람이 읽게 옮긴 파생물이다. Dataset·결과·그림은 모두 목록에 들어간다.
    SELF = {"manifest.json", "03_evidence_manifest.md"}
    files = []
    for p in sorted(out_dir.iterdir()):
        if p.is_file() and p.name not in SELF:
            files.append(_file_entry(p, out_dir))
    if dataset_path and paths.Path(dataset_path).is_file():
        files.append(_file_entry(paths.Path(dataset_path), out_dir, label="dataset"))
    for name in (spec["iut"]["name"],):
        elf = paths.HARNESS_BUILD / ("%s.elf" % name)
        if elf.is_file():
            files.append(_file_entry(elf, out_dir, label="emulated binary"))

    manifest = {
        "spec_id": spec["id"],
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "toolchain": _toolchain(),
        "reproduce": [
            "docker exec -it chipwhisperer-kor bash",
            "cd '/workspace/[extra] Physical-AI-SCA'",
            "make -C emul_harness IUT=%s" % spec["iut"]["name"],
            "python3 -m physai.collect --spec exp/%s.yaml" % spec["id"],
            "python3 -m physai.analyze --spec exp/%s.yaml" % spec["id"],
            "python3 -m physai.report  --run %s" % spec["id"],
            "python3 -m physai.verify  --run %s" % spec["id"],
        ],
        "files": files,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    L = ["# 산출물 목록 — %s" % spec["title"], "",
         "제3자가 이 번들만으로 결과를 재현·검증할 수 있어야 한다.", "",
         "## 재현 절차", "", "```bash"] + manifest["reproduce"] + ["```", "",
         "## 툴체인", "", "| 도구 | 버전 |", "|---|---|"]
    for k, v in manifest["toolchain"].items():
        L.append("| %s | %s |" % (k, v))
    L += ["", "## 파일", "", "| 파일 | 크기 | sha256 | 비고 |", "|---|---|---|---|"]
    for f in files:
        L.append("| `%s` | %s | `%s` | %s |"
                 % (f["path"], _human(f["bytes"]), f["sha256"][:16] + "…", f.get("label", "")))
    L += ["", "## 검증", "", "```bash", "python3 -m physai.verify --run %s" % spec["id"], "```", "",
          "`verify`는 위 해시를 다시 계산해 대조하고, Dataset이 여전히 스키마를 지키는지, "
          "툴체인이 같은지 확인한다. 하나라도 어긋나면 0 이 아닌 종료 코드를 낸다.", ""]
    p = out_dir / "03_evidence_manifest.md"
    p.write_text("\n".join(L), encoding="utf-8")
    return p


def _file_entry(p, out_dir, label=""):
    """파일 하나의 상대경로·바이트 크기·SHA-256·표시 라벨을 반환한다."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    try:
        rel = str(p.relative_to(out_dir))
    except ValueError:
        rel = str(p.relative_to(paths.PROJECT)) if str(p).startswith(str(paths.PROJECT)) else str(p)
    return {"path": rel, "bytes": p.stat().st_size, "sha256": h.hexdigest(), "label": label}


def _toolchain():
    """현재 Python·분석 모듈·ARM 컴파일러 버전을 증거용 사전으로 수집한다.

    모듈이나 컴파일러가 없으면 `없음`으로 기록한다. 파일을 변경하지 않지만 컴파일러
    버전 확인을 위해 최대 10초짜리 하위 프로세스를 한 번 실행한다.
    """
    out = {"python": platform.python_version()}
    for mod in ("numpy", "h5py", "scalib", "unicorn", "capstone", "lief", "scipy"):
        try:
            m = __import__(mod)
            out[mod] = getattr(m, "__version__", "?")
        except Exception:
            out[mod] = "없음"
    try:
        r = subprocess.run(["arm-none-eabi-gcc", "--version"],
                           capture_output=True, text=True, timeout=10)
        out["arm-none-eabi-gcc"] = r.stdout.splitlines()[0] if r.returncode == 0 else "없음"
    except Exception:
        out["arm-none-eabi-gcc"] = "없음"
    return out


def _human(n):
    """바이트 수를 B·KB·MB·GB 단위의 한 자리 소수 문자열로 바꾼다."""
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return "%.1f %s" % (n, u)
        n /= 1024.0


# ─────────────────────────────────────────────────────────────
# 그림
# ─────────────────────────────────────────────────────────────
def _make_figures(spec, results, out_dir, dataset_path):
    """그림은 **사람이 보라고** 만든다. 특히 SPA 육안 검사는 이것 없이는 불가능하다."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    try:
        matplotlib.rcParams["font.family"] = "NanumGothic"
        matplotlib.rcParams["axes.unicode_minus"] = False
    except Exception:
        pass

    figs = {}
    t_path = out_dir / "dpa_t.npy"
    r = results["tests"].get("dpa", {})
    if t_path.is_file() and r.get("threshold"):
        t = np.load(t_path)
        th = r["threshold"]["threshold"]
        fig, ax = plt.subplots(figsize=(11, 3.2))
        ax.plot(np.abs(t), lw=0.4, color="#1f4e79")
        ax.axhline(th, color="crimson", lw=1.0,
                   label="보정 임계 %.2f (Bonferroni)" % th)
        ax.axhline(r["threshold"].get("threshold_uncorrected", 4.5), color="orange",
                   lw=0.8, ls="--", label="보정 전 %.1f"
                   % r["threshold"].get("threshold_uncorrected", 4.5))
        ax.set_xlabel("샘플"); ax.set_ylabel("|t|")
        ax.set_title("DPA — Welch t-test (ISO/IEC 17825 §8.4)")
        ax.legend(fontsize=8); ax.grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(out_dir / "dpa_t.svg", dpi=FIG_DPI); plt.close(fig)
        figs["dpa"] = "dpa_t.svg"

    spa_path = out_dir / "spa_traces.npz"
    if spa_path.is_file():
        z = np.load(spa_path)
        keys = list(z.keys())
        fig, axes = plt.subplots(len(keys), 1, figsize=(11, 3.0 * len(keys)), squeeze=False)
        for ax, k in zip(axes[:, 0], keys):
            tr = z[k]
            for i in range(min(4, tr.shape[0])):
                ax.plot(tr[i], lw=0.4, alpha=0.8, label="#%d" % i)
            ax.set_title("SPA — %s" % k, fontsize=10)
            ax.set_xlabel("샘플"); ax.set_ylabel("누설")
            ax.legend(fontsize=7, ncol=4); ax.grid(alpha=0.3)
        fig.suptitle("SPA 육안 검사용 (ISO/IEC 17825 A.2.2) — 사람이 확인해야 한다", y=1.0)
        fig.tight_layout(); fig.savefig(out_dir / "spa_traces.svg", dpi=FIG_DPI); plt.close(fig)
        figs["spa"] = "spa_traces.svg"

    s = results["tests"].get("soundness")
    if s and s.get("labels"):
        names = [k for k, v in s["labels"].items() if "error" not in v]
        if names:
            fig, ax = plt.subplots(figsize=(9, 3.2))
            x = np.arange(len(names))
            # results.json 은 무한대를 문자열 "+inf" 로 적는다(표준 JSON 에 리터럴이 없다).
            # 그대로 넘기면 matplotlib 이 범주형으로 해석해 **막대 높이가 0** 이 되고,
            # 범례는 여전히 "실제 SNR max" 라고 말한다 — 조용히 거짓말하는 그림이 된다.
            ths = [_f(s["labels"][n]["null_threshold"]) for n in names]
            raw = [_f(s["labels"][n]["snr_max"]) for n in names]
            cap = max([v for v in ths if np.isfinite(v)] + [1.0]) * 1e3
            vals = [cap if not np.isfinite(v) else v for v in raw]
            ax.bar(x - 0.2, vals, 0.4, label="실제 SNR max", color="#1f4e79")
            ax.bar(x + 0.2, ths, 0.4, label="귀무 임계 (라벨 순열)", color="#c0c0c0")
            for xi, v in zip(x, raw):
                if not np.isfinite(v):
                    # 무한대는 막대 높이로 표현할 수 없으므로 잘라 그리고 ∞ 로 표시한다.
                    ax.text(xi - 0.2, cap, "∞", ha="center", va="bottom", fontsize=11)
            ax.set_xticks(x); ax.set_xticklabels(names, rotation=20, ha="right", fontsize=8)
            ax.set_yscale("log"); ax.set_ylabel("SNR")
            ax.set_title("soundness — 민감값별 1차 종속성")
            ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")
            fig.tight_layout(); fig.savefig(out_dir / "soundness_snr.svg", dpi=FIG_DPI)
            plt.close(fig)
            figs["soundness"] = "soundness_snr.svg"
    return figs


def _c(s):
    """보고서 표 셀용으로 줄바꿈·구분자를 정리하고 140자로 제한한다."""
    return (s or "").replace("\n", " ").replace("|", "\\|")[:140]


def _f(v):
    """`results.json` 의 수치를 float 으로. "+inf"/"-inf" 문자열과 None 을 다룬다."""
    if v is None:
        return float("nan")
    if isinstance(v, str):
        return {"+inf": float("inf"), "-inf": float("-inf")}.get(v, float("nan"))
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def _stat_key(c):
    """정렬용 수치. "+inf" 문자열도 가장 큰 값으로 다룬다."""
    v = c.get("statistic")
    if v == "+inf":
        return float("inf")
    if v == "-inf":
        return float("-inf")
    try:
        f = float(v)
        return f if f == f else float("-inf")
    except (TypeError, ValueError):
        return float("-inf")


def _num(v, fmt="%.4g"):
    """수치를 사람이 읽을 형태로. 무한대는 그 뜻과 함께 적는다.

    `results.json` 은 무한대를 문자열 "+inf" 로 적는다(표준 JSON 에 리터럴이 없다).
    보고서에 그대로 `inf` 라고 쓰면 오류처럼 보이지만, 실제로는 **클래스 내 분산이 0** —
    즉 그 샘플이 민감값에 완전히 결정적으로 종속한다는, 가장 강한 누설의 표시다.
    """
    if v is None:
        return "—"
    if isinstance(v, str):
        if v in ("+inf", "-inf"):
            return "∞ (클래스 내 분산 0 — 완전 종속)"
        return v
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f == float("inf"):
        return "∞ (클래스 내 분산 0 — 완전 종속)"
    if f != f:
        return "—"
    return fmt % f


def main(argv=None):
    """실행 ID의 분석 결과를 읽어 분석 보고서와 증거 번들을 생성한다.

    계획 보고서가 없으면 사후 생성 사실을 경고해 사전 확정 증거로 오인되지 않게 한다.
    결과 파일이 없으면 `SystemExit`로 중단하고, 성공하면 생성 파일 JSON과 종료 코드 0을
    반환한다. Dataset과 명세는 읽기 전용이다.
    """
    ap = argparse.ArgumentParser(prog="physai.report")
    ap.add_argument("--run", required=True, help="spec id")
    ap.add_argument("--spec", default=None, help="생략하면 exp/<run>.yaml")
    a = ap.parse_args(argv)

    sp = spec_mod.load(a.spec or (paths.EXP / ("%s.yaml" % a.run)))
    out_dir = paths.run_dir(a.run, create=True)
    res_path = out_dir / "results.json"
    if not res_path.is_file():
        raise SystemExit("results.json 이 없다: %s\n  먼저 analyze 를 돌린다." % res_path)
    results = json.loads(res_path.read_text(encoding="utf-8"))
    ds = paths.Path(results["dataset"])

    made = []
    plan = out_dir / "01_experiment_plan.md"
    if not plan.is_file():
        # 정상 흐름에서는 collect 가 수집 전에 만든다. 없으면 만들되 그 사실을 알린다.
        made.append(write_plan(sp, out_dir, dataset_path=ds))
        print("[주의] 계획 보고서가 없어 지금 생성했다. 정상 흐름에서는 collect 가 "
              "수집 **전에** 만든다 — 사후 생성은 사전 확정의 증거가 되지 못한다.")
    made.append(write_analysis(sp, results, out_dir, ds))
    made.append(write_evidence(sp, out_dir, ds))

    print(json.dumps({"ok": True, "run": a.run,
                      "files": [str(p.relative_to(paths.PROJECT)) for p in made]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
