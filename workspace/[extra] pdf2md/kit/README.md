# `kit/` — 규격·도구·카탈로그·작업 부산물

논문 원문·정규 Markdown이 **아닌** 변환 인프라를 둔다.

| 경로 | 역할 |
|------|------|
| `PDF_TO_MARKDOWN.md` | 변환·검수 SSOT |
| `TOOL_ALLOWLIST.md` | 2b 클래식 도구 목록 |
| `REF_FOLDERS.md` | 참고문헌 폴더 사람용 메모 (갭 입력 아님) |
| `ASSET_CATALOG.md` / `ASSET_CATALOG_SCHEMA.md` | 자산 메타 |
| `tools/list_pdf_queue.py` | `Papers_pdf/**/*.pdf` 변환 큐 |
| `tools/paths.py` | 미러 경로 헬퍼 |
| `tools/pdf_to_markdown.py` 등 | 2a·2b·3B |
| `candidates/` | 후보 작업물 (`<rel>/` 키) |

철학·목적: 루트 `README.md`.
