# `kit/` — 규격·도구·카탈로그·작업 부산물

논문 원문·정규 Markdown이 **아닌** 변환 인프라를 둔다.

| 경로 | 역할 |
|------|------|
| `PDF_TO_MARKDOWN.md` | 변환·검수 SSOT |
| `TOOL_ALLOWLIST.md` | 2b 클래식 도구 목록 |
| `REF_FOLDERS.md` | 참고문헌 폴더 사람용 메모 (갭 입력 아님) |
| `ASSET_CATALOG.md` / `ASSET_CATALOG_SCHEMA.md` | 자산 메타 |
| `CONVERSION_STATUS.md` | 2a·큐레이션·verified 현황 (초기화 시 pending) |
| `conversion_batch_log.json` | 2a 배치 로그 (실행 시 생성) |
| `curation_log.json` | text-only 큐레이션 로그 (실행 시 생성) |
| `tools/curate_to_verified.py` | 글리프 정리·레거시 이미지 제거 → verified (텍스트 전용) |
| `tools/list_pdf_queue.py` | `Papers_pdf/**/*.pdf` 변환 큐 |
| `tools/paths.py` | 미러 경로 헬퍼 |
| `tools/pdf_to_markdown.py` 등 | 2a·2b·3B |
| `candidates/` | 후보 작업물 (`<rel>/` 키) |

철학·목적: 루트 `README.md`.
