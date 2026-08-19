"""study 기반 통합 데모, 호스트 Grok one-shot 자문·출판 감사와 통합 보고서.

수치와 시험 판정은 각 ``results.json``의 값만 옮긴다. Grok은 읽기 전용 정합성 자문이며
파일·판정·명령을 바꿀 권한이 없다. 출판 감사는 정확한 입력 경로·크기·SHA-256을 기록하고
현재 파일과 하나라도 달라지면 폐기된다. 컨테이너는 요청을 쓴 뒤 응답을 기다리고, 사용자가
호스트에서 표시된 Python 한 줄을 실행해야 다음 단계로 진행한다.
"""

import argparse
import json
from pathlib import Path
import sys
import time

from . import artifacts, grok_once, paths, report, spec as spec_mod, verify

DEFAULT_STUDY = paths.PROJECT / "demo" / "study.yaml"


def _entry(path):
    return grok_once.file_entry(paths.PROJECT, path)


def _study_context(study_path=DEFAULT_STUDY):
    study, experiments = spec_mod.study_experiments(study_path)
    return study, experiments, [sp["id"] for _, sp in experiments]


def write_summary(study_path=DEFAULT_STUDY):
    """각 실행 결과와 verify 상태를 재계산 없이 모은 결정적 study JSON을 쓴다."""
    study, experiments, run_ids = _study_context(study_path)
    rows, requirements = [], {}
    for meta, sp in experiments:
        result_path = paths.run_dir(sp["id"]) / "results.json"
        if not result_path.is_file():
            raise FileNotFoundError("분석 결과가 없다: %s" % result_path)
        result = json.loads(result_path.read_text(encoding="utf-8"))
        verification = verify.verify(sp["id"], study_path)
        cpa = result.get("reference", {}).get("cpa", {})
        rows.append({
            "run_id": sp["id"], "role": meta["role"], "compare_with": meta.get("compare_with"),
            "channel": ",".join(sp["scope"]["channels"]), "iut": sp["iut"]["name"],
            "ta": result["tests"].get("ta", {}).get("verdict", "not-run"),
            "spa": result["tests"].get("spa", {}).get("verdict", "not-run"),
            "tvla": result["tests"].get("tvla", {}).get("early_finding", "not-run"),
            "dpa": result["tests"].get("dpa", {}).get("verdict", "not-run"),
            "overall": result.get("overall", {}).get("preassessment_verdict", "inconclusive"),
            "spa_human_review": result.get("overall", {}).get("human_review", {}).get("spa"),
            "cpa_bytes": cpa.get("bytes_recovered"), "cpa_key_bytes": cpa.get("key_bytes"),
            "verify": verification["ok"],
        })
        requirements[sp["id"]] = {
            "verify": verification["ok"],
            "positive_control": result.get("overall", {}).get("positive_control"),
            "compare_with": meta.get("compare_with"),
        }
    for run_id, requirement in requirements.items():
        reference_id = requirement["compare_with"]
        reference = requirements.get(reference_id) if reference_id else requirement
        reference_ok = bool(reference and reference["verify"] and
                            reference["positive_control"] == "pass")
        requirement["reference_positive_control_ok"] = reference_ok
        requirement["pipeline_ok"] = bool(requirement["verify"] and reference_ok)
    summary = {
        "schema_version": 2, "study_id": study["id"], "title": study["title"],
        "assessment_profile": study["assessment_profile"],
        "campaign_stage": study["campaign_stage"], "algorithm": study["algorithm"],
        "runs": run_ids, "comparison_rows": rows, "requirements": requirements,
        "pre_grok_ok": all(x["pipeline_ok"] for x in requirements.values()),
        "claim_scope": "ISO/IEC 17825:2024 방법론 준용 사전진단; 적합성 평가는 아님",
    }
    output = paths.RUNS / (study["id"] + "_summary.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def write_preflight(study_path=DEFAULT_STUDY):
    """수집 전 Grok이 실제 resolved 기준을 검토할 수 있는 결정적 JSON을 쓴다.

    프로파일에서 유도된 수량·통계·전처리를 원본 YAML에 복제하지 않고, 로더가 실제 수집기에
    넘길 resolved spec을 그대로 직렬화한다. 설치 경로용 ``_`` 필드는 계약이 아니므로 뺀다.
    이 함수는 수집·분석을 실행하지 않으며 ``runs/<study>_preflight.json``만 갱신한다.
    """
    study, experiments, _ = _study_context(study_path)
    study_contract = dict(study)
    study_contract["experiments"] = [
        {key: value for key, value in item.items() if key != "spec_path"}
        for item in study["experiments"]
    ]
    payload = {
        "schema_version": 1,
        "study": study_contract,
        "claim_scope": "ISO/IEC 17825:2024 방법론 준용 사전진단; 적합성 평가는 아님",
        "experiments": [
            {"role": meta["role"], "compare_with": meta.get("compare_with"),
             "resolved_spec": artifacts.resolved_spec_payload(resolved)}
            for meta, resolved in experiments
        ],
    }
    output = paths.RUNS / (study["id"] + "_preflight.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def write_failure(study_id, error):
    """실패 자문에 전달할 예외 종류·메시지·명령을 JSON으로 기록한다.

    traceback 전체에는 설치경로나 불필요한 프레임이 섞이므로 넣지 않는다. subprocess 오류의
    명령과 종료 코드는 별도 필드로 보존한다. 원래 예외를 변경하거나 다시 실행하지 않는다.
    """
    payload = {"schema_version": 1, "study_id": study_id,
               "error_type": type(error).__name__, "message": str(error)}
    if hasattr(error, "returncode"):
        payload["returncode"] = error.returncode
    if hasattr(error, "cmd"):
        payload["command"] = [str(value) for value in error.cmd]
    output = paths.RUNS / (study_id + "_failure.json")
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def _grok_checkpoint(study_id, task, files):
    """요청을 쓰고 사용자의 호스트 one-shot이 끝날 때까지 현재 셀에서 기다린다.

    Grok이나 감시기를 실행하지 않는다. 응답을 1초마다 확인하는 주체는 이미 실행 중인
    노트북 커널이며, 현재 요청과 ID가 같은 응답만 받아들인다. 사용자가 호스트 명령을
    실행하지 않으면 셀은 의도적으로 다음 셀로 넘어가지 않는다.
    """
    request = grok_once.create_request(paths.PROJECT, study_id, task, files)
    output = grok_once.response_path(paths.PROJECT, study_id, task)
    print("\nGrok 검토가 필요합니다. 호스트의 chipwhisperer-kor 저장소 루트에서", flush=True)
    print("다음 한 줄을 실행하십시오:\n", flush=True)
    print(grok_once.HOST_COMMAND, flush=True)
    print("\n호스트 응답을 기다리는 중입니다. 취소하려면 이 셀을 중단하십시오.", flush=True)
    while True:
        if output.is_file():
            response = json.loads(output.read_text(encoding="utf-8"))
            if response.get("request_id") == request["request_id"]:
                review = grok_once.validate_response(paths.PROJECT, request, response)
                if not review["ok"]:
                    raise RuntimeError("Grok %s 검토가 통과하지 않았다" % task)
                return output
        time.sleep(1)


def assist(study_path=DEFAULT_STUDY, phase="pre-collection", error=None):
    """호스트 one-shot을 요청하고 계획·실패·결과 자문 응답을 기다린다."""
    study, experiments, _ = _study_context(study_path)
    files = [Path(study_path), paths.PROJECT / "AGENTS.md"] + \
        [item["spec_path"] for item, _ in experiments]
    if phase == "pre-collection":
        files.append(write_preflight(study_path))
    if phase == "failure" and error is not None:
        files.append(write_failure(study["id"], error))
    if phase != "pre-collection":
        files += [paths.run_dir(sp["id"]) / "results.json" for _, sp in experiments
                  if (paths.run_dir(sp["id"]) / "results.json").is_file()]
    return _grok_checkpoint(study["id"], "assist-" + phase, files)


def grok_audit(study_path=DEFAULT_STUDY):
    """호스트 xhigh one-shot을 요청하고 신선도 검증 가능한 출판 감사를 기다린다."""
    study, experiments, _ = _study_context(study_path)
    summary = write_summary(study_path)
    summary_data = json.loads(summary.read_text(encoding="utf-8"))
    if not summary_data["pre_grok_ok"]:
        failed = [run_id for run_id, value in summary_data["requirements"].items()
                  if not value["pipeline_ok"]]
        raise RuntimeError("검증 또는 비교 양성 대조가 실패해 출판 감사를 시작하지 않는다: %s"
                           % failed)
    files = [Path(study_path), summary]
    for _, sp in experiments:
        run = paths.run_dir(sp["id"])
        files += [run / "results.json", run / "02_analysis_report.md", run / "manifest.json"]
    missing = [str(p) for p in files if not Path(p).is_file()]
    if missing:
        raise FileNotFoundError("출판 감사 입력 누락: %s" % missing)
    return _grok_checkpoint(study["id"], "publish", files)


def validate_grok_audit(audit_path):
    """감사 입력의 경로·크기·SHA-256을 현재 파일과 비교해 stale 감사를 거부한다."""
    audit_path = Path(audit_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("mode") != "publish" or not audit.get("review", {}).get("ok"):
        raise ValueError("출판용 통과 감사가 아니다: %s" % audit_path)
    for entry in audit.get("inputs", []):
        grok_once.resolve_entry(paths.PROJECT, entry)
    return audit


def write_markdown_report(study_path=DEFAULT_STUDY, audit_path=None):
    """감사 신선도를 확인한 뒤 통합 Markdown·standalone HTML·publication manifest를 쓴다."""
    study, experiments, _ = _study_context(study_path)
    summary_path = write_summary(study_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    audit_path = Path(audit_path or (paths.RUNS / (study["id"] + "_grok_audit.json")))
    audit = validate_grok_audit(audit_path)
    review = audit["review"]
    lines = ["# %s" % study["title"], "",
             "> **문서 성격:** ISO/IEC 17825:2024 방법론 준용 사전진단. 적합성 평가가 아니다.", "",
             "| 프로파일 | 캠페인 단계 | 출판 감사 |", "|---|---|---|",
             "| `%s` | `%s` | Grok `%s/%s`, stale 검증 통과 |"
             % (study["assessment_profile"], study["campaign_stage"],
                audit["execution"]["model"], audit["execution"]["reasoning_effort"]), "",
             "## 결과 요약", "",
             "| 실행 | 역할 | 채널 | IUT | TA | SPA | TVLA | DPA | 종합 | SPA 사람 검토 | verify |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in summary["comparison_rows"]:
        lines.append("| `{run_id}` | {role} | {channel} | {iut} | {ta} | {spa} | {tvla} | {dpa} | **{overall}** | {spa_human_review} | {verify} |".format(**row))
    lines += ["", "> CW Lab은 저표본 파일럿이다. 절차 완료와 통계 검정력은 별개이며, "
              "미검출은 표본 부족 상태에서 pass가 아니다. SPA는 사람이 최종 보고서의 그림을 검토하기 전까지 pending이다.", "",
              "## Grok 독립 출판 감사", "", review["overview"], ""]
    for finding in review["findings"]:
        lines += ["### %s" % finding["finding"], "",
                  "- 근거: %s" % "; ".join(finding["evidence"]),
                  "- 판단: %s" % finding["judgment"], ""]
    lines += ["## 감사 한계", ""] + ["- %s" % x for x in review["limitations"]]
    md = paths.PROJECT / "demo" / "0.1.Demo_without_TraceWhisperer_Report.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    html_path = report.write_html(md)
    publication_files = [summary_path, audit_path, md, html_path]
    publication = {"study_id": study["id"], "status": "published",
                   "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "files": [_entry(p) for p in publication_files]}
    manifest = paths.RUNS / (study["id"] + "_publication_manifest.json")
    manifest.write_text(json.dumps(publication, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"markdown": md, "html": html_path, "manifest": manifest}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="physai.demo")
    ap.add_argument("--study", default=str(DEFAULT_STUDY))
    ap.add_argument("--assist", choices=["pre-collection", "failure", "results"])
    ap.add_argument("--grok", action="store_true", help="호스트 one-shot 필수 출판 감사")
    ap.add_argument("--report", action="store_true", help="감사 후 통합 MD/HTML 출판")
    args = ap.parse_args(argv)
    if args.assist:
        result = assist(args.study, args.assist)
    elif args.grok:
        result = grok_audit(args.study)
    elif args.report:
        result = write_markdown_report(args.study)
    else:
        result = write_summary(args.study)
    if isinstance(result, dict):
        payload = {k: str(v) for k, v in result.items()}
    else:
        payload = {"output": str(result)}
    print(json.dumps({"ok": True, **payload}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
