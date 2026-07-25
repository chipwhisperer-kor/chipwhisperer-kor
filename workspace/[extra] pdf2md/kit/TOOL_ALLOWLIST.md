# 클래식 도구 Allowlist (2b 후보 변환)

`PDF_TO_MARKDOWN.md` §1·§3.3 부속. 철학: 루트 `README.md` §0.

**로컬 OCR 금지.** 기준 변환(2a)은 유지하고, 버킷 A로 후보만 보강한다.

---

## 버킷 A — 로컬 클래식 (2b 허용)

| tool_id | 엔진 | 명령·경로 | 기본 활성 | 비고 |
|---------|------|-----------|-----------|------|
| `poppler-layout` | Poppler | `pdftotext -layout` | 예 (설치 시) | 열 보존에 유리한 경우 |
| `poppler-raw` | Poppler | `pdftotext` (기본) | 예 (설치 시) | 단순 스트림 순서 |
| `pymupdf-text` | PyMuPDF | `page.get_text("text")` | 선택 | 텍스트 층만; OCR 경로 금지 |
| `pdfminer-text` | pdfminer.six | `extract_text` | 선택 | 텍스트 층만 |

---

## 버킷 B — 원격 (2b 아님)

| 서비스 | 2b | 4·5 | 비고 |
|--------|----|-----|------|
| xAI/Grok Files | **금지** | **허용** | `tools/GROK_REVIEW_PROMPTS.md` |
| 기타 원격 PDF API | 기본 금지 | 정책 후 | 업로드·라이선스 승인 |

---

## 버킷 C — 제외

로컬 OCR 전부 · 로컬 NN pdf2md · 대량 비전 전사 · 이미지 AI 분석 · pdfimages/page-render PNG 사이드카 · 정규본 자동 merge

---

## 산출

```text
kit/candidates/<rel>/
  CROSSCHECK.md
  <tool_id>/extract.md
  <tool_id>/META.json
```

`<rel>` = `Papers_pdf/` 아래 상대 경로에서 `.pdf`를 뺀 키  
(예: `Foo/[1] Bar`). stem만 쓰면 참고문헌 간 충돌한다.

필수 런타임: **Poppler + Python 3.8+**. 선택 패키지 없으면 해당 tool 스킵.
