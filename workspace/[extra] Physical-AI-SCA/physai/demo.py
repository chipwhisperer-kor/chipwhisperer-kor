"""Physical-AI-SCA 통합 데모의 결정적 교차 검증과 Grok 감사 경계.

이 모듈은 네 Dataset·results.json·보고서·manifest에서 이미 존재하는 사실만 읽어 비교한다.
새 누설 수치나 판정을 만들지 않으며, 물리 파형에 명령어 주소를 대응시키지 않는다. Grok은
이 모듈이 만든 제한된 감사 입력만 읽고 문장·등급 정합성을 구조화 JSON으로 확인한다.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import h5py
import numpy as np

from . import paths, verify

import sca_schema as S  # noqa: E402
from aes_ref import aes_ecb_encrypt  # noqa: E402

RUNS = (
    "004_demo_emul_tinyaes", "005_demo_emul_masked",
    "006_demo_hw_tinyaes", "007_demo_hw_masked",
)
PAIRS = ((RUNS[0], RUNS[2]), (RUNS[1], RUNS[3]))
GROK_EXECUTION = {
    "model": "grok-4.6", "reasoning_effort": "xhigh", "web": False,
    "memory": False, "subagents": False, "editing": False,
    "allowed_tool": "Shell(cat:*)",
}


def _load_results(run_id):
    """실행 ID의 results.json을 dict로 읽으며 파일 부재·JSON 오류를 전파한다."""
    return json.loads((paths.run_dir(run_id) / "results.json").read_text(encoding="utf-8"))


def _dataset_check(run_id):
    """한 Dataset의 행 정렬·골든 AES·반복 평균·마스크 보존을 전수 검사한다."""
    result = _load_results(run_id)
    dataset = Path(result["dataset"])
    schema_bad = S.validate_dataset(dataset)
    logical = raw = masks = 0
    golden_ok = True
    row_aligned = True
    repeat_means_ok = True
    with h5py.File(dataset, "r") as h5:
        attrs = {k: h5.attrs[k] for k in h5.attrs}
        subset_rows = {}
        for name in S.subset_names(dataset):
            g = h5[name]
            rows = {field: d.shape[0] for field, d in g.items()}
            row_aligned &= len(set(rows.values())) == 1
            n = int(g[S.F_TRACE].shape[0])
            subset_rows[name] = n
            logical += n
            for key, plaintext, ciphertext in zip(
                    g[S.F_KEY], g[S.F_PLAINTEXT], g[S.F_CIPHERTEXT]):
                golden_ok &= bytes(ciphertext) == aes_ecb_encrypt(key, plaintext)
            if S.F_TRACE_REPEATS in g:
                repeats = int(g[S.F_TRACE_REPEATS].shape[1])
                raw += n * repeats
                for beg in range(0, n, 16):
                    tr = g[S.F_TRACE_REPEATS][beg:beg + 16].astype(np.float64)
                    repeat_means_ok &= np.array_equal(
                        np.rint(tr.mean(axis=1)).astype(np.int16), g[S.F_TRACE][beg:beg + 16])
                    et = g[S.F_EXEC_TIME_REPEATS][beg:beg + 16].astype(np.float64)
                    repeat_means_ok &= np.array_equal(
                        np.rint(et.mean(axis=1)).astype(np.uint32),
                        g[S.F_EXEC_TIME][beg:beg + 16])
            else:
                raw += n
            if S.F_MASK_REPEATS in g:
                masks += int(np.prod(g[S.F_MASK_REPEATS].shape[:2]))
        recoveries = [x.decode() if isinstance(x, bytes) else str(x)
                      for x in attrs.get("recoveries", [])]
        return {
            "run": run_id, "dataset": str(dataset), "schema_ok": not schema_bad,
            "schema_violations": schema_bad, "logical_records": logical,
            "raw_captures": raw, "mask_captures": masks, "golden_aes_ok": bool(golden_ok),
            "row_alignment_ok": bool(row_aligned), "repeat_means_ok": bool(repeat_means_ok),
            "subsets": subset_rows, "samples_per_trace": int(attrs["samples_per_trace"]),
            "target_clock_hz": float(attrs["target_clock_hz"]),
            "sample_rate_hz": (None if "sample_rate_hz" not in attrs
                               else float(attrs["sample_rate_hz"])),
            "recoveries": recoveries,
        }


def _shared_inputs(emul_run, hw_run):
    """실물 레코드 수만큼 에뮬레이션 선두 key·plaintext가 완전히 같은지 전수 비교한다."""
    emul, hw_run_result = _load_results(emul_run), _load_results(hw_run)
    comparisons = {}
    with h5py.File(emul["dataset"], "r") as a, h5py.File(hw_run_result["dataset"], "r") as b:
        for name in sorted(set(S.subset_names(emul["dataset"])) &
                           set(S.subset_names(hw_run_result["dataset"]))):
            n = b[name][S.F_KEY].shape[0]
            comparisons[name] = bool(
                np.array_equal(a[name][S.F_KEY][:n], b[name][S.F_KEY][:]) and
                np.array_equal(a[name][S.F_PLAINTEXT][:n], b[name][S.F_PLAINTEXT][:]))
    return {"all_equal": all(comparisons.values()), "subsets": comparisons}


def build_summary():
    """네 결과에서 검수 사실·비교표를 계산해 dict로 반환하며 파일을 변경하지 않는다."""
    datasets = {run: _dataset_check(run) for run in RUNS}
    results = {run: _load_results(run) for run in RUNS}
    verified = {run: verify.verify(run) for run in RUNS}
    rows = []
    for run in RUNS:
        r = results[run]
        tests = r["tests"]
        rows.append({
            "run": run,
            "channel": "emulation" if "emul" in run else "physical-power",
            "iut": "masked-aes-c" if "masked" in run else "tiny-AES-c",
            "ta": tests.get("ta", {}).get("verdict", "not-run"),
            "spa": tests.get("spa", {}).get("verdict", "not-run"),
            "dpa": tests.get("dpa", {}).get("verdict", "not-run"),
            "soundness": tests.get("soundness", {}).get("verdict", "not-applicable"),
            "soundness_candidates": tests.get("soundness", {}).get("n_candidates"),
            "cpa_bytes": r.get("reference", {}).get("cpa", {}).get("bytes_recovered"),
            "verify": bool(verified[run]["ok"]),
        })
    shared = {"tiny-AES-c": _shared_inputs(*PAIRS[0]),
              "masked-aes-c": _shared_inputs(*PAIRS[1])}
    length_comparison = {}
    for iut, (emul_run, hw_run) in zip(("tiny-AES-c", "masked-aes-c"), PAIRS):
        emul_instr = results[emul_run]["derived"]["instructions"]
        hw = datasets[hw_run]
        target_cycles = hw["samples_per_trace"] / (
            hw["sample_rate_hz"] / hw["target_clock_hz"])
        length_comparison[iut] = {
            "emulated_instructions": int(emul_instr),
            "physical_trigger_samples": hw["samples_per_trace"],
            "physical_target_clock_equivalent_cycles": float(target_cycles),
            "note": "명령어 수와 타깃 클럭 환산 길이는 단위가 달라 동일하다고 주장하지 않는다.",
        }
    required = {
        "all_schema_ok": all(x["schema_ok"] for x in datasets.values()),
        "all_verify_ok": all(x["ok"] for x in verified.values()),
        "all_shared_inputs_equal": all(x["all_equal"] for x in shared.values()),
        "all_golden_aes_ok": all(x["golden_aes_ok"] for x in datasets.values()),
        "all_rows_aligned": all(x["row_alignment_ok"] for x in datasets.values()),
        "all_repeat_means_ok": all(x["repeat_means_ok"] for x in datasets.values()),
        "hardware_logical_records_ok": all(datasets[x]["logical_records"] == 332 for x in RUNS[2:]),
        "hardware_raw_captures_ok": all(datasets[x]["raw_captures"] == 3320 for x in RUNS[2:]),
        "masked_repeated_masks_ok": datasets[RUNS[3]]["mask_captures"] == 3320,
        "tiny_cpa_16_of_16": results[RUNS[2]]["reference"]["cpa"]["bytes_recovered"] == 16,
        "emulation_sample_map_soundness": all(
            results[x]["tests"]["soundness"].get("candidates") for x in RUNS[:2]),
    }
    return {"runs": list(RUNS), "datasets": datasets, "comparison_rows": rows,
            "shared_inputs": shared, "length_comparison": length_comparison,
            "requirements": required, "pre_grok_ok": all(required.values())}


def write_summary(path=None):
    """결정적 통합 비교를 JSON으로 쓰고 경로를 반환한다."""
    out = paths.RUNS / "demo_0_1_summary.json" if path is None else Path(path)
    out.write_text(json.dumps(build_summary(), ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def validate_grok_audit(audit):
    """Grok 감사가 형식뿐 아니라 실제 네 증거 필드를 인용했는지 검사한다.

    `ok`·정합성 플래그·평가 근거를 읽기만 하며 파일은 변경하지 않는다. placeholder,
    파일을 읽기 전의 계획, 네 실행 ID·핵심 결과 필드 누락은 `ValueError`로 거부한다.
    통과하면 `True`를 반환한다. 이 검사는 LLM의 결론을 대신하지 않고 빈 구조화 응답을
    성공으로 오인하지 않게 하는 최소 의미 경계다.
    """
    if not audit.get("ok") or not all(audit.get("consistency", {}).values()) or audit.get("issues"):
        raise ValueError("Grok 감사의 정합성 판정이 통과하지 않았다.")
    review = audit.get("assessor_review", {})
    serialized = json.dumps(review, ensure_ascii=False).lower()
    forbidden = ("placeholder", "읽지 않았", "읽기 전", "판단을 보류", "응답은 파일", "평가 골격")
    required = ("004_demo_emul_tinyaes", "005_demo_emul_masked", "006_demo_hw_tinyaes",
                "007_demo_hw_masked", "results.json", "bytes_recovered", "inconclusive",
                "soundness", "150", "shunt_max_verified=false")
    if (any(word in serialized for word in forbidden) or
            any(word not in serialized for word in required) or
            len(review.get("reasoning", [])) < 4):
        raise ValueError("Grok 평가관 근거가 실제 네 증거 파일과 필수 필드를 인용하지 않았다.")
    return True


def grok_audit(grok_bin="grok"):
    """Grok 4.6 xhigh로 제한된 네 증거 번들의 정합성만 감사한다.

    파일 편집·웹·메모리·서브에이전트를 끄고 shell 도구를 읽기 전용 ``cat``으로 제한한다.
    Grok이 개별 시험의 수치나 판정을 바꿀 수 없도록 JSON Schema와 프롬프트를 고정한다.
    감사자는 각 총평을 뒷받침한 파일·필드, 판단, 한계를 함께 반환한다. 이것은 비공개 내부
    사고 기록이 아니라 제3자가 재검산할 수 있는 평가 근거다. 인증·네트워크·모델 부재 또는
    감사 불통과는 예외로 중단하며 결과를 ``runs/grok_audit.json``에 쓴다.
    """
    summary_path = write_summary()
    audit_files = [summary_path]
    for run in RUNS:
        directory = paths.run_dir(run)
        audit_files += [directory / "results.json", directory / "02_analysis_report.md",
                        directory / "03_evidence_manifest.md", directory / "manifest.json"]
    schema = {
        "type": "object", "additionalProperties": False,
        "required": ["ok", "consistency", "issues", "assessor_review"],
        "properties": {
            "ok": {"type": "boolean"},
            "consistency": {
                "type": "object", "additionalProperties": False,
                "required": ["grades", "inconclusive", "positive_control", "nominal_metadata"],
                "properties": {k: {"type": "boolean"} for k in
                               ("grades", "inconclusive", "positive_control", "nominal_metadata")},
            },
            "issues": {"type": "array", "items": {"type": "string"}},
            "assessor_review": {
                "type": "object", "additionalProperties": False,
                "required": ["persona", "overall_verdict", "reasoning", "limitations",
                             "final_commentary"],
                "properties": {
                    "persona": {"type": "string", "minLength": 8},
                    "overall_verdict": {"type": "string", "minLength": 80},
                    "reasoning": {
                        "type": "array", "minItems": 4,
                        "items": {
                            "type": "object", "additionalProperties": False,
                            "required": ["finding", "evidence", "judgment"],
                            "properties": {
                                "finding": {"type": "string", "minLength": 40},
                                "evidence": {"type": "array", "minItems": 2,
                                             "items": {"type": "string", "minLength": 30}},
                                "judgment": {"type": "string", "minLength": 40},
                            },
                        },
                    },
                    "limitations": {"type": "array", "minItems": 1,
                                    "items": {"type": "string", "minLength": 40}},
                    "final_commentary": {"type": "string", "minLength": 160},
                },
            },
        },
    }
    prompt = ("독립된 안전성 평가 검증자 페르소나로 아래 파일만 읽어 정합성을 감사하라. "
              "개별 시험의 새 수치·판정·보안 주장을 만들거나 기존 판정을 바꾸지 말고, "
              "results.json의 등급, inconclusive 표현, tiny-AES-c CPA 양성 대조, "
              "150 MHz 명목값·shunt_max_verified=false와 보고서 문장이 서로 같은지만 확인하라. "
              "manifest의 해시를 새로 계산하지 말고 기록된 항목의 존재와 문장 정합성만 보라. "
              "assessor_review에는 평가관 관점의 총평을 한국어로 작성하되, 각 판단에 사용한 "
              "파일명·JSON 필드·기록값을 evidence에 명시하라. A-Z 실행 무결성 통과와 암호 구현의 "
              "안전성 입증을 구분하고, inconclusive·soundness fail·명목 메타데이터의 한계를 빠뜨리지 "
              "마라. 응답 전에 나열된 모든 파일을 cat으로 실제 읽어라. 파일을 읽기 전의 계획·골격·"
              "placeholder·판단 보류 응답은 금지한다. 네 실행 ID와 results.json의 정확한 필드명·값을 "
              "근거에 인용해야 한다. 비공개 내부 chain-of-thought나 토큰별 독백 대신 제3자가 재검산할 수 있는 "
              "finding→evidence→judgment 근거만 반환하라.\n파일:\n" +
              "\n".join(str(p) for p in audit_files))
    cmd = [str(grok_bin), "--single", prompt, "--cwd", str(paths.PROJECT),
           "--model", GROK_EXECUTION["model"],
           "--reasoning-effort", GROK_EXECUTION["reasoning_effort"],
           "--no-memory", "--no-subagents", "--disable-web-search", "--no-plan",
           "--tools", GROK_EXECUTION["allowed_tool"], "--permission-mode", "dontAsk",
           "--json-schema", json.dumps(schema, separators=(",", ":"))]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("Grok 감사 실행 실패(rc=%d): %s" % (proc.returncode, proc.stderr[-1000:]))
    envelope = json.loads(proc.stdout)
    audit = envelope.get("structuredOutput")
    if audit is None:
        text = envelope.get("text", proc.stdout) if isinstance(envelope, dict) else proc.stdout
        audit = json.loads(text)
    audit["execution"] = dict(GROK_EXECUTION)
    validate_grok_audit(audit)
    out = paths.RUNS / "grok_audit.json"
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    if not audit.get("ok"):
        raise RuntimeError("Grok 감사 불통과: %s" % audit.get("issues"))
    return out


def write_markdown_report(summary_path=None, audit_path=None, output_path=None):
    """실행 산출물만 사용해 한눈에 읽는 통합 마크다운 보고서를 만든다.

    입력은 결정적 교차 검증 JSON과 Grok 구조화 감사 JSON이다. 보고서는 개별 시험 판정을
    재계산하지 않고 그대로 표시하며, 평가관 총평의 근거·판단·한계를 분리한다. 입력 누락,
    사전 검수 실패, 구형 감사 스키마는 예외로 중단한다. 기본 출력은 demo 폴더의 단일
    ``0.1.Demo_without_TraceWhisperer_Report.md``이며 인증정보나 장비 시리얼을 기록하지 않는다.
    """
    summary_file = (paths.RUNS / "demo_0_1_summary.json" if summary_path is None
                    else Path(summary_path))
    audit_file = paths.RUNS / "grok_audit.json" if audit_path is None else Path(audit_path)
    output_file = (paths.PROJECT / "demo" / "0.1.Demo_without_TraceWhisperer_Report.md"
                   if output_path is None else Path(output_path))
    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    audit = json.loads(audit_file.read_text(encoding="utf-8"))
    if not summary.get("pre_grok_ok"):
        raise RuntimeError("결정적 사전 검수가 통과하지 않아 통합 보고서를 만들 수 없다.")
    validate_grok_audit(audit)

    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")

    rows = []
    for item in summary["comparison_rows"]:
        rows.append("| " + " | ".join(cell(item[key]) for key in
                    ("run", "channel", "iut", "ta", "spa", "dpa", "soundness",
                     "soundness_candidates", "cpa_bytes", "verify")) + " |")
    requirement_lines = [
        "- `%s`: **%s**" % (key, "통과" if value else "실패")
        for key, value in summary["requirements"].items()
    ]
    hardware_lines = []
    for run_id in RUNS[2:]:
        item = summary["datasets"][run_id]
        recoveries = ", ".join(item["recoveries"]) if item["recoveries"] else "없음"
        hardware_lines.append(
            "- `%s`: 논리 레코드 %d개, 원 파형 %d개, 마스크 반복 %d개, 파형 길이 %d samples, "
            "타깃 클럭 %.0f Hz, ADC %.0f Hz, 자연 발생 복구 `%s`"
            % (run_id, item["logical_records"], item["raw_captures"],
               item["mask_captures"], item["samples_per_trace"], item["target_clock_hz"],
               item["sample_rate_hz"], recoveries))
    length_lines = []
    for iut, item in summary["length_comparison"].items():
        length_lines.append(
            "- %s: 에뮬레이션 %d instructions, 실측 %d trigger samples ≈ %.0f target-clock cycles. %s"
            % (iut, item["emulated_instructions"], item["physical_trigger_samples"],
               item["physical_target_clock_equivalent_cycles"], item["note"]))
    review = audit["assessor_review"]
    reasoning_lines = []
    for index, step in enumerate(review["reasoning"], 1):
        reasoning_lines.extend([
            "%d. **관찰:** %s" % (index, step["finding"]),
            "   - 근거: " + "; ".join(step["evidence"]),
            "   - 평가: " + step["judgment"],
        ])
    limitation_lines = ["- " + item for item in review["limitations"]]
    execution = audit["execution"]
    text = "\n".join([
        "# 0.1 Physical-AI-SCA 통합 데모 실행 보고서",
        "",
        "> **실행 무결성:** 통과  ",
        "> **암호 구현 안전성 결론:** 확정하지 않음 — inconclusive 및 soundness fail을 보존함  ",
        "> **Grok 평가관 총평:** " + review["overall_verdict"],
        "",
        "## 한눈에 보는 결과",
        "",
        "| 실행 ID | 채널 | IUT | TA | SPA | DPA | soundness | 후보 수 | CPA 복구 | verify |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- |",
        *rows,
        "",
        "`inconclusive`는 통과가 아니다. CPA는 수집·정렬·라벨 배관 확인용 참고 시험이며, "
        "tiny-AES-c의 16/16만 양성 대조 완료 조건이다. 에뮬레이션 soundness 후보는 "
        "`sample_map`으로 명령어 주소에 연결했지만, 실물 파형에는 주소를 대응시키지 않았다.",
        "",
        "## 완료 조건과 데이터 무결성",
        "",
        *requirement_lines,
        "",
        "모든 실물 암호문은 골든 AES와 일치했고, 저장 평균은 각 10개 원 파형 및 트리거 "
        "길이의 반올림 평균과 일치했다. 공유 subset의 key·plaintext 배열도 실물 행 수만큼 "
        "에뮬레이션 선두 입력과 완전히 일치했다.",
        "",
        "## 실물 수집 현황",
        "",
        *hardware_lines,
        "",
        "복구는 정상 캡처 실패 때 자연 발생한 reconnect만 기록했다. SAM firmware reflash는 "
        "발생하지 않았으므로 해당 단계를 실물 검수했다고 주장하지 않는다.",
        "",
        "## 에뮬레이션·실측 길이 대조",
        "",
        *length_lines,
        "",
        "## 측정 메타데이터 해석",
        "",
        "- `shunt_ohm=12.0`은 CW308T-STM32F3의 공장 R3 설계값이며 동작 가능한 최대값을 "
        "실험한 결과가 아니므로 `shunt_max_verified=false`다.",
        "- `bandwidth_hz=150000000`은 Husky 전단 AD8330의 공식 명목 대역폭이다. 현재 "
        "실험대에서 교정한 실측 대역폭이 아니며 Dataset과 개별 보고서도 이를 nominal로 표시한다.",
        "- 실측 타깃 클럭·ADC·이득·파형 길이·펌웨어 해시·복구 이력은 실행 시점 값이다.",
        "",
        "## Grok 독립 평가관 총평",
        "",
        "Grok 감사 설정: model=`%s`, reasoning=`%s`, web=%s, memory=%s, subagents=%s, "
        "editing=%s, allowed_tool=`%s`. 입력은 네 results·보고서·manifest와 통합 요약으로 제한했다."
        % (execution["model"], execution["reasoning_effort"], execution["web"],
           execution["memory"], execution["subagents"], execution["editing"],
           execution["allowed_tool"]),
        "",
        "아래 내용은 모델의 비공개 토큰별 사고 기록이 아니라, 평가 결론을 제3자가 원본 "
        "필드에서 재검산할 수 있도록 정리한 **관찰→근거→평가** 기록이다.",
        "",
        *reasoning_lines,
        "",
        "### 평가 한계",
        "",
        *limitation_lines,
        "",
        "### 최종 평가관 의견",
        "",
        review["final_commentary"],
        "",
        "이 총평은 NIST 적합성 인증이나 암호 구현의 안전성 보증이 아니다. 고정된 명세로 "
        "수행한 사전 안전성 평가의 실행 무결성, 증거 추적성, 보고 문장 정합성에 대한 검토다.",
        "",
    ])
    output_file.write_text(text, encoding="utf-8")
    return output_file


def main(argv=None):
    """통합 비교 또는 Grok 감사를 실행해 마지막 줄에 JSON 요약을 출력한다."""
    parser = argparse.ArgumentParser(prog="physai.demo")
    parser.add_argument("--grok", action="store_true")
    parser.add_argument("--grok-bin", default="grok")
    args = parser.parse_args(argv)
    if args.grok:
        out = grok_audit(args.grok_bin)
        payload = {"ok": True, "grok_audit": str(out)}
    else:
        out = write_summary()
        summary = json.loads(out.read_text(encoding="utf-8"))
        payload = {"ok": summary["pre_grok_ok"], "summary": str(out),
                   "requirements": summary["requirements"]}
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
