"""OpenAI 호환 LLM 클라이언트 — 함수 하나.

## 이 파일이 하지 않는 것

에이전트 루프, 툴콜 파싱, 재시도, 컨텍스트 관리 — **아무것도 하지 않는다.**
그것은 이미 성숙한 하네스(grok 헤드리스, Claude Code 등)가 하는 일이고, 다시 구현하면
유지보수 대상만 늘어난다. 특히 로컬 소형 모델의 툴콜 신뢰도를 맞추려다 보면 그 루프가
곧 특정 모델 전용 튜닝 덩어리가 된다.

## 온라인 ↔ 오프라인 전환 비용은 환경변수 세 개다

| 변수 | 온라인 (예) | 오프라인 (예) |
|---|---|---|
| `PHYSAI_LLM_BASE_URL` | `https://api.x.ai/v1` | `http://localhost:11434/v1` (Ollama) |
| `PHYSAI_LLM_MODEL` | 서비스가 제공하는 모델 id | 로컬에 올린 모델 id |
| `PHYSAI_LLM_API_KEY` | 발급받은 키 | 보통 아무 값 |

**코드 변경은 없다.** OpenAI 호환 `/chat/completions` 만 쓰기 때문이다.

## 경계 — 무엇을 LLM 에게 맡기고 무엇을 맡기지 않는가

**수치·판정·해시·요건 대조표는 전부 도구가 만든다.** LLM 이 관여하는 곳은 보고서의
**서술 초안** 하나뿐이고, 환경변수가 없으면 그 칸이 비고 나머지는 다 채워진 문서가 나온다.
즉 **LLM 이 없어도 산출물은 나온다.** 이것이 설계의 핵심이다 — 판정의 근거가 모델의
출력에 걸려 있으면 그 보고서는 재현할 수 없다.

의존성도 두지 않는다. `urllib` 만 쓴다.
"""

import json
import os
import urllib.error
import urllib.request

ENV_BASE = "PHYSAI_LLM_BASE_URL"
ENV_MODEL = "PHYSAI_LLM_MODEL"
ENV_KEY = "PHYSAI_LLM_API_KEY"


def available():
    """호출할 수 있는 설정이 갖춰졌는가. 보고서 생성기가 이것부터 본다."""
    return bool(os.environ.get(ENV_BASE) and os.environ.get(ENV_MODEL))


def why_unavailable():
    """왜 못 쓰는지 사람이 읽을 문장. 보고서의 빈 칸에 그대로 들어간다."""
    missing = [k for k in (ENV_BASE, ENV_MODEL) if not os.environ.get(k)]
    if not missing:
        return ""
    return ("LLM 서술을 생성하지 않았다 — 환경변수 %s 가 설정되지 않았다. "
            "수치·판정·대조표는 도구가 만들었으므로 이 문서의 사실관계는 그대로 유효하다."
            % ", ".join(missing))


def complete(prompt, system=None, timeout=120, max_tokens=2048, temperature=0.2):
    """한 번 묻고 한 번 받는다.

    출력: 응답 문자열. 설정이 없으면 **None** (예외가 아니다 — 없어도 파이프라인이
    끝까지 돌아야 하기 때문이다).

    실패 조건: 설정은 있는데 호출이 실패하면 RuntimeError. 이때는 조용히 넘어가지
    않는다 — 쓰겠다고 해 놓고 못 쓴 것은 알려야 한다.
    """
    if not available():
        return None
    base = os.environ[ENV_BASE].rstrip("/")
    body = {
        "model": os.environ[ENV_MODEL],
        "messages": ([{"role": "system", "content": system}] if system else [])
                    + [{"role": "user", "content": prompt}],
        "max_tokens": int(max_tokens),
        "temperature": float(temperature),
    }
    req = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer %s" % os.environ.get(ENV_KEY, "")},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("LLM 호출 실패 (HTTP %s): %s"
                           % (e.code, e.read().decode("utf-8", "replace")[:400]))
    except Exception as e:
        raise RuntimeError("LLM 호출 실패: %s" % e)
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError("LLM 응답 형식을 해석할 수 없다: %s"
                           % json.dumps(payload, ensure_ascii=False)[:400])


def describe_config():
    """지금 무엇으로 붙게 되어 있는지. 증거 번들에 남긴다 (키는 싣지 않는다)."""
    return {
        "base_url": os.environ.get(ENV_BASE, ""),
        "model": os.environ.get(ENV_MODEL, ""),
        "api_key_set": bool(os.environ.get(ENV_KEY)),
        "available": available(),
    }
