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
import base64
import html
import json
import platform
import re
import subprocess
import sys
import time

import numpy as np

from . import artifacts, conformance, llm, paths, spec as spec_mod

import sca_schema as S  # noqa: E402  # paths가 workspace/lib를 import 경로에 넣는다

# SVG 안의 래스터 요소를 화면에서 읽을 수 있게 하는 렌더링 해상도다. 판정 수치에는
# 영향을 주지 않으며 보고서 파일 크기가 불필요하게 커지지 않는 수준으로 둔다.
FIG_DPI = 110

REPORT_CSS = """
:root{--bg:#f5f7fb;--paper:#fff;--ink:#172033;--muted:#62708a;--line:#dce3ef;--accent:#3157d5;--ok:#147d64;--bad:#c33b4a;--warn:#a26300}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1120px;margin:36px auto;padding:42px 52px;background:var(--paper);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 50px #24345418}
h1{font-size:2rem;letter-spacing:-.03em;margin-top:0}h2{margin-top:2.2em;padding-top:.5em;border-top:1px solid var(--line)}h3{color:#29428b}
table{width:100%;border-collapse:separate;border-spacing:0;margin:1rem 0;overflow:hidden;border:1px solid var(--line);border-radius:12px}th{background:#edf2ff;text-align:left}th,td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}.status{display:inline-block;padding:.08rem .48rem;border-radius:999px;font-weight:700;font-size:.84em;background:#e8edf7}.status-pass,.status-detected{color:var(--ok);background:#e4f5ef}.status-fail{color:var(--bad);background:#fde9ec}.status-inconclusive,.status-pending,.status-underpowered{color:var(--warn);background:#fff1d6}
blockquote{margin:1rem 0;padding:12px 16px;border-left:4px solid var(--accent);background:#f0f4ff;border-radius:0 10px 10px 0;color:#33405b}code{background:#edf0f6;padding:.15em .4em;border-radius:5px}pre{overflow:auto;padding:16px;background:#101827;color:#eef3ff;border-radius:12px}pre code{background:none;padding:0}img{display:block;max-width:100%;margin:18px auto;border:1px solid var(--line);border-radius:12px}.meta{color:var(--muted)}strong{color:#172a67}details{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:1rem 0}
@media(max-width:760px){main{margin:0;padding:24px 18px;border:0;border-radius:0}table{display:block;overflow-x:auto}}
@media print{body{background:#fff}main{max-width:none;margin:0;padding:0;border:0;box-shadow:none}h2{break-after:avoid}table,img,blockquote{break-inside:avoid}}
"""


def _inline_markdown(text):
    """보고서가 쓰는 제한된 강조·코드 문법을 안전한 HTML로 바꾼다."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    for status in ("pass", "fail", "inconclusive", "pending", "underpowered", "detected"):
        escaped = re.sub(r"\b%s\b" % status,
                         '<span class="status status-%s">%s</span>' % (status, status),
                         escaped, flags=re.IGNORECASE)
    return escaped


def _table_cells(line):
    """escaped pipe를 셀 구분자로 오인하지 않고 Markdown 표 한 줄을 나눈다."""
    marker = "\x00PIPE\x00"
    return [x.strip().replace(marker, "|")
            for x in line.strip().strip("|").replace("\\|", marker).split("|")]


def write_html(markdown_path):
    """정본 Markdown을 외부 CDN 없는 standalone HTML로 결정적으로 렌더링한다.

    로컬 SVG/PNG는 data URI로 내장한다. 지원하지 않는 Markdown 구문도 텍스트로 보존하며
    입력 파일이나 그림은 변경하지 않는다. 반환값은 생성한 ``Path``다.
    """
    markdown_path = paths.Path(markdown_path)
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    out, paragraph, i, in_code = [], [], 0, False

    def flush():
        if paragraph:
            out.append("<p>%s</p>" % _inline_markdown(" ".join(paragraph)))
            paragraph.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            if not in_code:
                out.append("<pre><code>")
            else:
                out.append("</code></pre>")
            in_code = not in_code; i += 1; continue
        if in_code:
            out.append(html.escape(line)); i += 1; continue
        if not line.strip():
            flush(); i += 1; continue
        if line.startswith("#"):
            flush(); level = min(6, len(line) - len(line.lstrip("#")))
            out.append("<h%d>%s</h%d>" % (level, _inline_markdown(line[level:].strip()), level)); i += 1; continue
        if line.startswith(">"):
            flush(); quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i][1:].strip()); i += 1
            out.append("<blockquote>%s</blockquote>" % _inline_markdown(" ".join(quote))); continue
        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", line.strip())
        if image_match:
            flush(); alt, src = image_match.groups(); asset = markdown_path.parent / src
            if asset.is_file():
                mime = "image/svg+xml" if asset.suffix.lower() == ".svg" else "image/png"
                encoded = base64.b64encode(asset.read_bytes()).decode("ascii")
                src = "data:%s;base64,%s" % (mime, encoded)
            out.append('<img alt="%s" src="%s">' % (html.escape(alt, quote=True), src)); i += 1; continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-+", lines[i + 1]):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(_table_cells(lines[i])); i += 1
            if len(rows) >= 2:
                out.append("<table><thead><tr>%s</tr></thead><tbody>" % "".join(
                    "<th>%s</th>" % _inline_markdown(x) for x in rows[0]))
                for row in rows[2:]:
                    out.append("<tr>%s</tr>" % "".join("<td>%s</td>" % _inline_markdown(x) for x in row))
                out.append("</tbody></table>")
            continue
        if line.startswith(("- ", "* ")):
            flush(); items = []
            while i < len(lines) and lines[i].startswith(("- ", "* ")):
                items.append(lines[i][2:]); i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _inline_markdown(x) for x in items)); continue
        paragraph.append(line.strip()); i += 1
    flush()
    title = next((x[2:].strip() for x in lines if x.startswith("# ")), markdown_path.stem)
    page = ("<!doctype html><html lang='ko'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>%s</title><style>%s</style></head><body><main>%s</main></body></html>"
            % (html.escape(title), REPORT_CSS, "\n".join(out)))
    target = markdown_path.with_suffix(".html")
    target.write_text(page, encoding="utf-8")
    return target


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
         "| 프로파일 | `%s` / `%s` |" % (spec["assessment_profile"], spec["campaign_stage"]),
         "| 알고리즘 | `%s` |" % spec["algorithm"],
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
          "| 전처리 평균 | %d회 | Annex %s.5 `shall [A.01]` |"
          % (c["preprocessing"]["average_n"], "A.2" if c["security_level"] == 3 else "A.3"),
          "| 정렬 | %s | Annex %s.6 `shall [A.02]` |"
          % (c["preprocessing"]["alignment"], "A.2" if c["security_level"] == 3 else "A.3"), "",
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
             "tvla": "독립 누설 평가 — ISO 종합 판정에는 합산하지 않음",
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
    write_html(p)
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
    dataset_attrs = S.root_attrs(dataset_path)
    channel_type = str(dataset_attrs.get("channel_type", ""))

    tests = results["tests"]
    overall = results.get("overall", {}).get("preassessment_verdict", "inconclusive")

    L = ["# 분석 결과 보고서 — %s" % results["title"], "",
         "| | |", "|---|---|",
         "| spec id | `%s` |" % results["spec_id"],
         "| 프로파일 | `%s` / `%s` |" % (results.get("assessment_profile", "?"),
                                          results.get("campaign_stage", "?")),
         "| 원본 수집 HDF5 | `%s` (`raw-acquisition`, 불변) |"
         % paths.Path(results["source_dataset"]).name,
         "| 파생 분석 HDF5 | `%s` (`derived-analysis`, 재생성 가능) |"
         % paths.Path(results["dataset"]).name,
         "| 원본 SHA-256 | `%s` |" % dataset_attrs.get("source_dataset_sha256", "미기록"),
         "| 파생 계약 SHA-256 | `%s` |"
         % dataset_attrs.get("derivation_contract_sha256", "미기록"),
         "| 분석 시각 | %s |" % results["generated"],
         "| **종합** | **%s** |" % overall, ""]

    L += [conformance.to_markdown(rep), ""]

    if channel_type == "power":
        recoveries = dataset_attrs.get("recoveries", [])
        recovery_names = [x.decode() if isinstance(x, bytes) else str(x) for x in recoveries]
        L += ["## 실물 측정 메타데이터", "",
              "| 항목 | 실행 기록 |", "|---|---|",
              "| 플랫폼 | `%s` |" % dataset_attrs.get("platform", "미기록"),
              "| 타깃 클럭 | `%s Hz` |" % dataset_attrs.get("target_clock_hz", "미기록"),
              "| ADC | `%s Hz`, `%s-bit`, 타깃 클럭 × `%s` |"
              % (dataset_attrs.get("sample_rate_hz", "미기록"),
                 dataset_attrs.get("sample_resolution_bits", "미기록"),
                 dataset_attrs.get("adc_mul", "미기록")),
              "| 이득 | `%s dB` |" % dataset_attrs.get("channel_gain_db", "미기록"),
              "| 파형 길이 | `%s samples` |" % dataset_attrs.get("samples_per_trace", "미기록"),
              "| 같은 입력 평균 | `%s회` (원 파형 보존) |"
              % dataset_attrs.get("aggregation_n", "미기록"),
              "| 대역폭 | `%s Hz`; %s |"
              % (dataset_attrs.get("bandwidth_hz", "미기록"),
                 _c(str(dataset_attrs.get("bandwidth_basis", "미기록")))),
              "| 션트 | `%s Ω`; 최대값 검증=`%s`; %s |"
              % (dataset_attrs.get("shunt_ohm", "미기록"),
                 dataset_attrs.get("shunt_max_verified", "미기록"),
                 _c(str(dataset_attrs.get("shunt_selection_note", "미기록")))),
              "| IUT 펌웨어 SHA-256 | `%s` |" % dataset_attrs.get("firmware_sha256", "미기록"),
              "| 자연 발생 복구 | `%d회`: %s |"
              % (len(recovery_names), ", ".join(recovery_names) or "없음"), "",
              "> `bandwidth_is_nominal=%s`: 위 대역폭은 현재 실험대에서 교정한 실측값이 "
              "아니라 공식 부품 구성의 명목값이다. `shunt_max_verified=%s`이므로 공장 "
              "저항에서 동작했다는 사실을 ‘동작 가능한 최대 저항을 확인했다’로 확대하지 않는다."
              % (dataset_attrs.get("bandwidth_is_nominal", "미기록"),
                 dataset_attrs.get("shunt_max_verified", "미기록")), ""]
        if "l4" in figs:
            L += ["### Level 4 전처리 증거", "",
                  "![L4 preprocessing evidence](%s)" % figs["l4"], ""]

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

    if "tvla" in tests:
        L += ["## TVLA — 독립 fixed-vs-random 누설 평가", "",
              "> TVLA는 중요한 독립 결과이지만 ISO 필수 TA·SPA·DPA 종합 판정에는 합산하지 않는다.", "",
              "**소견: %s** — %s" % (tests["tvla"].get("early_finding"),
                                      tests["tvla"].get("reason", "")), ""]
        L += _tvla_body(tests["tvla"], figs)

    if "soundness" in tests:
        L += _soundness_body(tests["soundness"], figs)

    if results.get("reference", {}).get("cpa"):
        c = results["reference"]["cpa"]
        L += ["## 양성 대조 — CPA (판정 아님)", "",
              "> %s" % c["note"], "",
              "| | |", "|---|---|",
              "| 복구 바이트 | **%d / %d** |" % (c["bytes_recovered"], c.get("key_bytes", 16)),
              "| 평균 순위 | %.1f |" % c["mean_rank"],
              "| 트레이스 | %d |" % c["n_traces"], "",
              "복구 키: `%s`" % c["recovered_key"], "",
              "정답 키: `%s`" % c["true_key"], ""]
        if c["bytes_recovered"] == c.get("key_bytes", 16):
            L += ["> 배관(입력 주입·정렬·라벨링)이 정상이라는 뜻이다. "
                  "이 대조가 실패하면 데이터가 아니라 도구를 먼저 의심해야 한다.", ""]
        elif spec["iut"]["name"] == "tiny-AES-c":
            L += ["> **양성 대조 실패**: 비마스킹 tiny-AES-c에서 16바이트를 복구하지 "
                  "못했으므로 정상 완료가 아니다. 수집·정렬·라벨 설정을 점검해야 한다.", ""]
        else:
            L += ["> 마스킹 구현에서 키가 복구되지 않는 것은 정상일 수 있다. "
                  "**이 수치는 판정 근거가 아니다** — 표준은 누설 관측만으로 판정한다(§7.2).", ""]

    L += _narrative(results, overall)

    L += ["## 이 시험이 본 고리와 보지 않은 고리", "",
          "| 고리 | 본 도구 | 이번에 봤나 |", "|---|---|---|",
          "| 이론 (마스킹 수식) | 논문·형식 검증 | **아니오** — 범위 밖 |",
          "| 구현 (소스→기계어) | 에뮬레이션 | %s |"
          % ("**예** — 에뮬레이션 Dataset 분석"
             if channel_type == "emulated-power" else "아니오 — 이 Dataset의 채널이 아님"),
          "| 물리 (실제 칩) | 전력·EM 관측 | %s |"
          % ("**예** — `%s` Dataset 분석" % channel_type
             if channel_type in ("power", "em") else "아니오 — 이 Dataset의 채널이 아님"),
          "| 실행 흐름 | 디버그 트레이스 | %s |"
          % ("**예** — 디버그 트레이스 Dataset 분석"
             if channel_type == "debug-trace" else "아니오 — 이 Dataset의 채널이 아님"), "",
          "> **어느 하나가 깨끗하다는 사실만으로 안전을 주장할 수 없다.** 에뮬레이션의 HW/HD "
          "모델은 글리치·커플링 같은 물리 효과를 담지 않으므로, 여기서 깨끗해도 실물에서 샐 수 "
          "있다. 반대로 실측에서 잡음에 묻힌 누설이 여기서는 보인다. 세 관측은 상보재다.", "",
          "> **DPA 는 1차 한정이다.** 고차 DPA 는 ISO/IEC 17825 Fig.1 NOTE 3 에 따라 필수 "
          "시험이 아니며, 1차 부울 마스킹이 2차에서 뚫리는 것은 이론적으로 정상이라 결함으로 "
          "보고할 수 없다. **단 TA 의 2차(분산) 검정은 `shall` 이므로 수행했다.**", ""]

    p = out_dir / "02_analysis_report.md"
    p.write_text("\n".join(L), encoding="utf-8")
    write_html(p)
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
    if not r.get("threshold") or not r.get("requirement"):
        return ["> DPA 통계량을 만들 수 없어 수치 표를 생성하지 않는다: %s" %
                r.get("reason", "원인 미기록"), ""]
    groups = r.get("groups", {})
    L = ["| | |", "|---|---|",
         "| 사전 지정 표적 | `%s` |" % r.get("target", "미기록"),
         "| 분석 subset | `%s` |" % r.get("subset", "미기록"),
         "| 민감값 집단 | class 0: %s장 / class 1: %s장 |"
         % (groups.get("class_0", "?"), groups.get("class_1", "?")),
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


def _tvla_body(r, figs):
    """TVLA 수치와 검정력은 표시하되 ISO 판정과 분리한 Markdown을 반환한다."""
    groups = r.get("groups", {})
    L = ["| | |", "|---|---|",
         "| 집단 | `%s` %s장 vs `%s` %s장 |"
         % (groups.get("fixed"), groups.get("n_fixed"),
            groups.get("random"), groups.get("n_random")),
         "| 통계 검정력 | **%s** |" % r.get("statistical_power"),
         "| \\|t\\|max | **%s** (샘플 %s) |"
         % (_num(r.get("abs_t_max"), "%.2f"), r.get("abs_t_max_index")),
         "| 임계 초과 샘플 | %s |" % r.get("n_over_threshold"),
         "| 필요/보유 | %s / %s |"
         % (r.get("requirement", {}).get("n_required"),
            r.get("requirement", {}).get("n_have")), ""]
    if "tvla" in figs:
        L += ["![TVLA fixed-vs-random t-test](%s)" % figs["tvla"], ""]
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
        if r.get("procedure_status") == "complete":
            note = ("> SNR 무한대는 클래스 내 분산이 0이라는 뜻이다. 유효한 귀무 임계가 "
                    "함께 산정됐으므로 강한 1차 종속 소견으로 기록한다.")
        else:
            note = ("> SNR 무한대는 클래스 내 분산이 0이라는 수치 상태다. 이 실행은 귀무 "
                    "임계를 산정하지 못했으므로 누설 검출이나 안전 판정의 근거로 쓰지 않는다.")
        L += [note, ""]
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
def write_evidence(spec, out_dir, source_dataset_path, derived_dataset_path):
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
    SELF = {"manifest.json", "03_evidence_manifest.md", "03_evidence_manifest.html"}
    files = []
    for p in sorted(out_dir.iterdir()):
        if p.is_file() and p.name not in SELF:
            files.append(_file_entry(p, out_dir))
    if source_dataset_path and paths.Path(source_dataset_path).is_file():
        files.append(_file_entry(paths.Path(source_dataset_path), out_dir,
                                 label="raw-acquisition dataset"))
    if derived_dataset_path and paths.Path(derived_dataset_path).is_file():
        files.append(_file_entry(paths.Path(derived_dataset_path), out_dir,
                                 label="derived-analysis dataset"))
        provenance = paths.Path(derived_dataset_path).with_suffix(".provenance.json")
        if provenance.is_file():
            files.append(_file_entry(provenance, out_dir,
                                     label="derived-analysis provenance"))
    emulated = "emulated-power" in spec["scope"]["channels"]
    for name in ((spec["iut"]["name"],) if emulated else ()):
        elf = paths.HARNESS_BUILD / ("%s.elf" % name)
        if elf.is_file():
            files.append(_file_entry(elf, out_dir, label="emulated binary"))

    if spec.get("_study_path"):
        study_rel = str(paths.Path(spec["_study_path"]).relative_to(paths.PROJECT))
        collect_cmd = "python3 -m physai.collect --study %s --experiment %s" % (study_rel, spec["id"])
        analyze_cmd = "python3 -m physai.analyze --study %s --experiment %s" % (study_rel, spec["id"])
        report_cmd = "python3 -m physai.report --run %s --study %s" % (spec["id"], study_rel)
        verify_cmd = "python3 -m physai.verify --run %s --study %s" % (spec["id"], study_rel)
    else:
        spec_rel = str(paths.Path(spec["_spec_path"]).relative_to(paths.PROJECT))
        collect_cmd = "python3 -m physai.collect --spec %s" % spec_rel
        analyze_cmd = "python3 -m physai.analyze --spec %s" % spec_rel
        report_cmd = "python3 -m physai.report --run %s --spec %s" % (spec["id"], spec_rel)
        verify_cmd = "python3 -m physai.verify --run %s" % spec["id"]
    manifest = {
        "spec_id": spec["id"],
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "toolchain": _toolchain(),
        "reproduce": [
            "docker exec -it chipwhisperer-kor bash",
            "cd '/workspace/[extra] Physical-AI-SCA'",
        ] + (["make -C emul_harness IUT=%s" % spec["iut"]["name"]]
             if emulated else []) + [collect_cmd, analyze_cmd, report_cmd, verify_cmd],
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
    L += ["", "## 검증", "", "```bash", verify_cmd, "```", "",
          "`verify`는 위 해시를 다시 계산해 대조하고, Dataset이 여전히 스키마를 지키는지, "
          "툴체인이 같은지 확인한다. 하나라도 어긋나면 0 이 아닌 종료 코드를 낸다.", ""]
    p = out_dir / "03_evidence_manifest.md"
    p.write_text("\n".join(L), encoding="utf-8")
    write_html(p)
    return p


def _file_entry(p, out_dir, label=""):
    """파일 하나의 상대경로·바이트 크기·SHA-256·표시 라벨을 반환한다."""
    try:
        rel = str(p.relative_to(out_dir))
    except ValueError:
        rel = str(p.relative_to(paths.PROJECT)) if str(p).startswith(str(paths.PROJECT)) else str(p)
    return {"path": rel, "bytes": p.stat().st_size,
            "sha256": artifacts.sha256_file(p), "label": label}


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
    tvla_path = out_dir / "tvla_t.npy"
    tvla_result = results["tests"].get("tvla", {})
    if tvla_path.is_file() and tvla_result.get("threshold"):
        t = np.load(tvla_path)
        th = tvla_result["threshold"]["threshold"]
        fig, ax = plt.subplots(figsize=(11, 3.2))
        ax.plot(np.abs(t), lw=0.45, color="#6a45b8")
        ax.axhline(th, color="crimson", lw=1.0, label="보정 임계 %.2f" % th)
        ax.set(xlabel="샘플", ylabel="|t|", title="TVLA — fixed vs random (독립 평가)")
        ax.legend(fontsize=8); ax.grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(out_dir / "tvla_t.svg", dpi=FIG_DPI); plt.close(fig)
        figs["tvla"] = "tvla_t.svg"

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

    l4_path = out_dir / "l4_preprocessing_evidence.npz"
    if l4_path.is_file():
        z = np.load(l4_path)
        fig, axes = plt.subplots(2, 1, figsize=(11, 6.2))
        axes[0].semilogy(z["frequency_hz"], np.maximum(z["calibration_power"], 1e-30),
                        color="#3157d5", lw=0.7, label="교정 PSD")
        axes[0].plot(z["response_frequency_hz"], np.maximum(z["response_abs"], 1e-8),
                     color="#c33b4a", lw=1.0, label="필터 응답")
        axes[0].set(title="L4 필터 교정 증거", xlabel="Hz", ylabel="power / response")
        axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)
        axes[1].plot(z["reference_before"], lw=0.45, alpha=0.7, label="전처리 전")
        axes[1].plot(z["reference_after"], lw=0.55, label="필터·정렬·crop 후")
        axes[1].set(title="L4 기준 파형 전후", xlabel="샘플", ylabel="ADC code")
        axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(out_dir / "l4_preprocessing.svg", dpi=FIG_DPI)
        plt.close(fig); figs["l4"] = "l4_preprocessing.svg"
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
    ap.add_argument("--spec", default=None, help="독립 experiment YAML")
    ap.add_argument("--study", default=None, help="study가 프로파일·단계를 소유하는 경우")
    a = ap.parse_args(argv)

    sp = (spec_mod.load_from_study(a.study, a.run) if a.study else
          spec_mod.load(a.spec or (paths.EXP / ("%s.yaml" % a.run))))
    out_dir = paths.run_dir(a.run, create=True)
    res_path = out_dir / "results.json"
    if not res_path.is_file():
        raise SystemExit("results.json 이 없다: %s\n  먼저 analyze 를 돌린다." % res_path)
    results = json.loads(res_path.read_text(encoding="utf-8"))
    ds = paths.Path(results["dataset"])
    source_ds = paths.Path(results["source_dataset"])

    made = []
    plan = out_dir / "01_experiment_plan.md"
    if not plan.is_file():
        # 정상 흐름에서는 collect 가 수집 전에 만든다. 없으면 만들되 그 사실을 알린다.
        made.append(write_plan(sp, out_dir, dataset_path=source_ds))
        print("[주의] 계획 보고서가 없어 지금 생성했다. 정상 흐름에서는 collect 가 "
              "수집 **전에** 만든다 — 사후 생성은 사전 확정의 증거가 되지 못한다.")
    made.append(write_analysis(sp, results, out_dir, ds))
    made.append(write_evidence(sp, out_dir, source_ds, ds))

    print(json.dumps({"ok": True, "run": a.run,
                      "files": [str(p.relative_to(paths.PROJECT)) for p in made]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
