"""공유 저장소의 요청 하나를 호스트 Grok CLI로 처리하는 one-shot 브리지.

노트북은 이 모듈의 계약으로 ``runs/grok_request.json``을 만들고 응답을 기다린다. 사용자는
호스트의 저장소 루트에서 이 파일을 Python으로 한 번 실행한다. 스크립트는 요청 당시의 입력
크기와 SHA-256을 확인하고 Grok을 포그라운드에서 정확히 한 번 실행한 뒤 응답 JSON을 쓰고
종료한다. 감시기, 데몬, 백그라운드 Grok 프로세스와 인증정보 공유는 사용하지 않는다.

요청이 없거나 입력이 바뀌었거나 Grok 실행·구조화 출력이 실패하면 0이 아닌 코드로 끝난다.
Grok이 검토 실패(``review.ok=false``)를 반환하면 그 결과를 기록한 뒤 실패로 끝나므로 기다리던
노트북도 같은 실패를 관측한다. 파일 편집 부작용은 요청·응답 JSON에 한정된다.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


PROTOCOL_VERSION = 1
HOST_COMMAND = "python3 'workspace/[extra] Physical-AI-SCA/physai/grok_once.py'"
REQUEST_NAME = "grok_request.json"
GROK = {
    "assist": {"model": "grok-4.6", "reasoning_effort": "high"},
    "publish": {"model": "grok-4.6", "reasoning_effort": "xhigh"},
}
READ_ONLY_FLAGS = ["--no-memory", "--no-subagents", "--disable-web-search", "--no-plan",
                   "--tools", "Shell(cat:*)", "--permission-mode", "dontAsk"]
TASKS = {
    "assist-pre-collection": {
        "mode": "assist",
        "instruction": "pre-collection 단계의 계획·증거 정합성을 자문하라.",
        "suffix": "grok_assist_pre-collection",
    },
    "assist-failure": {
        "mode": "assist",
        "instruction": "failure 단계의 계획·증거 정합성을 자문하라.",
        "suffix": "grok_assist_failure",
    },
    "assist-results": {
        "mode": "assist",
        "instruction": "results 단계의 계획·증거 정합성을 자문하라.",
        "suffix": "grok_assist_results",
    },
    "publish": {
        "mode": "publish",
        "instruction": ("출판 전 독립 평가관으로서 등급·표본 부족·TVLA 분리·CPA 양성 대조·"
                        "메타데이터 문장의 정합성을 감사하라."),
        "suffix": "grok_audit",
    },
}


def review_schema():
    """Grok 구조화 출력의 단일 JSON Schema 정의를 새 객체로 반환한다."""
    return {
        "type": "object", "additionalProperties": False,
        "required": ["ok", "overview", "findings", "limitations"],
        "properties": {
            "ok": {"type": "boolean"},
            "overview": {"type": "string", "minLength": 40},
            "findings": {"type": "array", "minItems": 1, "items": {
                "type": "object", "additionalProperties": False,
                "required": ["finding", "evidence", "judgment"],
                "properties": {"finding": {"type": "string"},
                               "evidence": {"type": "array", "minItems": 1,
                                            "items": {"type": "string"}},
                               "judgment": {"type": "string"}}}},
            "limitations": {"type": "array", "minItems": 1,
                            "items": {"type": "string"}},
        },
    }


def _canonical_hash(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_root():
    """설치 위치와 현재 작업 디렉터리에 무관한 서브프로젝트 루트를 반환한다."""
    return Path(__file__).resolve().parent.parent


def request_path(project):
    return Path(project).resolve() / "runs" / REQUEST_NAME


def response_path(project, study_id, task):
    """검증된 study/task 조합의 고정 응답 경로를 반환한다."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", str(study_id)):
        raise ValueError("안전하지 않은 study id: %r" % study_id)
    if task not in TASKS:
        raise ValueError("지원하지 않는 Grok task: %s" % task)
    return Path(project).resolve() / "runs" / ("%s_%s.json" %
                                                (study_id, TASKS[task]["suffix"]))


def file_entry(project, path):
    """프로젝트 내부 파일의 이식 가능한 상대경로·크기·SHA-256을 반환한다."""
    root = Path(project).resolve()
    resolved = Path(path).resolve(strict=True)
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Grok 입력은 서브프로젝트 내부 파일이어야 한다: %s" % resolved) from exc
    if not resolved.is_file():
        raise ValueError("Grok 입력이 일반 파일이 아니다: %s" % resolved)
    return {"path": relative.as_posix(), "bytes": resolved.stat().st_size,
            "sha256": _sha256_file(resolved)}


def resolve_entry(project, entry):
    """상대경로가 프로젝트 내부의 현재 지문 파일인지 확인하고 절대경로를 반환한다."""
    root = Path(project).resolve()
    relative = Path(entry["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Grok 입력 경로는 프로젝트 상대경로여야 한다: %s" % relative)
    resolved = (root / relative).resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Grok 입력이 프로젝트 밖을 가리킨다: %s" % relative) from exc
    if not resolved.is_file() or resolved.stat().st_size != int(entry["bytes"]) or \
            _sha256_file(resolved) != entry["sha256"]:
        raise ValueError("Grok 요청 입력이 변경되었다(stale): %s" % relative)
    return resolved


def _atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(".%s.%d.tmp" % (path.name, os.getpid()))
    try:
        with open(temporary, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def create_request(project, study_id, task, files):
    """현재 입력의 요청을 원자적으로 기록하고 request dict를 반환한다."""
    root = Path(project).resolve()
    response_path(root, study_id, task)  # study/task를 파일 쓰기 전에 검증한다.
    request = {
        "protocol_version": PROTOCOL_VERSION,
        "study_id": str(study_id),
        "task": task,
        "inputs": [file_entry(root, path) for path in files],
    }
    request["request_id"] = _canonical_hash(request)
    _atomic_json(request_path(root), request)
    return request


def load_request(project):
    """현재 요청의 계약·ID·입력 지문을 검증하며 파일을 변경하지 않는다."""
    path = request_path(project)
    if not path.is_file():
        raise FileNotFoundError("대기 중인 Grok 요청이 없다: %s" % path)
    request = json.loads(path.read_text(encoding="utf-8"))
    expected_keys = {"protocol_version", "study_id", "task", "inputs", "request_id"}
    if set(request) != expected_keys or request.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError("지원하지 않는 Grok 요청 계약")
    unsigned = {key: request[key] for key in request if key != "request_id"}
    if request["request_id"] != _canonical_hash(unsigned):
        raise ValueError("Grok request_id가 요청 내용과 일치하지 않는다")
    response_path(project, request["study_id"], request["task"])
    if not isinstance(request["inputs"], list) or not request["inputs"]:
        raise ValueError("Grok 요청 입력이 비어 있다")
    for entry in request["inputs"]:
        if set(entry) != {"path", "bytes", "sha256"}:
            raise ValueError("Grok 입력 지문 필드가 잘못되었다")
        resolve_entry(project, entry)
    return request


def _validate_review(review):
    if not isinstance(review, dict) or set(review) != {"ok", "overview", "findings", "limitations"}:
        raise ValueError("Grok review 최상위 구조가 계약과 다르다")
    if not isinstance(review["ok"], bool) or not isinstance(review["overview"], str) or \
            len(review["overview"]) < 40:
        raise ValueError("Grok review 요약이 계약과 다르다")
    if not isinstance(review["findings"], list) or not review["findings"] or \
            not isinstance(review["limitations"], list) or not review["limitations"]:
        raise ValueError("Grok review finding/limitation이 비어 있다")
    for finding in review["findings"]:
        if not isinstance(finding, dict) or set(finding) != {"finding", "evidence", "judgment"} or \
                not isinstance(finding["evidence"], list) or not finding["evidence"]:
            raise ValueError("Grok review finding 구조가 계약과 다르다")
    return review


def validate_response(project, request, response):
    """응답이 현재 요청에서 나온 성공 결과인지 검증하고 review를 반환한다."""
    if response.get("request_id") != request["request_id"]:
        raise ValueError("Grok 응답이 현재 요청과 일치하지 않는다")
    if response.get("error"):
        raise RuntimeError("호스트 Grok 실행 실패: %s" % response["error"])
    task = TASKS[request["task"]]
    setting = GROK[task["mode"]]
    if response.get("mode") != task["mode"] or response.get("inputs") != request["inputs"] or \
            response.get("execution", {}).get("model") != setting["model"] or \
            response.get("execution", {}).get("reasoning_effort") != setting["reasoning_effort"]:
        raise ValueError("Grok 응답 실행 계약이 현재 요청과 다르다")
    for entry in response["inputs"]:
        resolve_entry(project, entry)
    return _validate_review(response.get("review"))


def _prompt(task, entries):
    envelope = json.dumps(entries, ensure_ascii=False, indent=2)
    return (TASKS[task]["instruction"] +
            "\n수치·판정·해시를 새로 만들거나 변경하지 말고, 아래 입력만 cat으로 실제로 읽어 "
            "finding→evidence→judgment를 한국어로 반환하라. 웹·기억·서브에이전트와 파일 "
            "편집은 허용되지 않는다. inconclusive를 안전으로 바꾸지 말고 적합성을 주장하지 "
            "마라. ok=true는 해당 다음 단계 진행을 막는 구체적인 계약 위반이 없다는 뜻이다. "
            "명시된 비주장, 저표본 검정력 부족, 사람 검토 pending과 입력 범위의 한계는 반드시 "
            "limitations에 남기되 그것만으로 ok=false로 만들지 마라. 실제 모순·필수 계약 누락·"
            "증거 불일치가 있을 때만 ok=false로 하라.\n입력 지문:\n" + envelope)


def run_once(project=None, grok_bin="grok"):
    """현재 요청 하나를 Grok 포그라운드 호출 한 번으로 처리하고 즉시 종료한다."""
    root = Path(project or project_root()).resolve()
    request = load_request(root)
    task = TASKS[request["task"]]
    setting = GROK[task["mode"]]
    output = response_path(root, request["study_id"], request["task"])
    command = [str(grok_bin), "--single", _prompt(request["task"], request["inputs"]),
               "--cwd", str(root), "--model", setting["model"],
               "--reasoning-effort", setting["reasoning_effort"], *READ_ONLY_FLAGS,
               "--json-schema", json.dumps(review_schema(), separators=(",", ":"))]
    try:
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode:
            raise RuntimeError("Grok rc=%d: %s" % (process.returncode, process.stderr[-1200:]))
        raw = json.loads(process.stdout)
        structured = raw.get("structuredOutput") if isinstance(raw, dict) else None
        if structured is None:
            structured = json.loads(raw.get("text", process.stdout)) \
                if isinstance(raw, dict) else raw
        review = _validate_review(structured)
    except Exception as exc:
        _atomic_json(output, {"protocol_version": PROTOCOL_VERSION,
                             "request_id": request["request_id"], "error": str(exc)})
        raise
    response = {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request["request_id"],
        "mode": task["mode"],
        "execution": {**setting, "headless": True, "web": False, "memory": False,
                      "subagents": False, "permission": "read-only Shell(cat:*)"},
        "inputs": request["inputs"],
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "review": review,
    }
    _atomic_json(output, response)
    if not review["ok"]:
        raise RuntimeError("Grok 검토가 통과하지 않았다; 응답은 기록했다: %s" % output)
    return output


def main():
    try:
        output = run_once()
    except Exception as exc:
        print("Grok one-shot 실패: %s" % exc, file=sys.stderr)
        return 1
    print("Grok one-shot 완료: %s" % output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
