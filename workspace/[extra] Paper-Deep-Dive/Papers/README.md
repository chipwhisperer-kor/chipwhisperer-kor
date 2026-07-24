# Papers — 연구 자산 저장소 (`curator` 소유)

## 구성

| 경로 | 내용 |
|------|------|
| `*.pdf` | 대상 논문 2편 + 표준문서 1편 |
| `<PDF와 같은 stem>.md` | PDF를 대체하지 않는 검증 상태 명시 Markdown 파생본 |
| `<논문제목>/[n] 제목.pdf` | 1-deep 참고문헌 (HAETAE 24, PCM 35 PDF) |
| `reference-download-manifest.csv` | 레거시 파일 존재·크기 장부 |
| `ASSET_CATALOG_SCHEMA.md` | 신규·재검증 메타 **필드 규격** |
| `ASSET_CATALOG.md` | 신규·재검증 메타 **기록 표** |
| `PDF_TO_MARKDOWN.md` | PDF 원본과 병존하는 기계적 Markdown 파생본 규격·검수 기준 |
| `tools/pdf_to_markdown.py` | Poppler bbox 기반 결정론적 변환기 |
| `assets/<paper_id>/<asset_id>/` | 코드·구현·데이터·실험 원본 또는 Markdown 파생 시각자산·매니페스트 |

## 상태 (D34)

- 대상 논문 2 · 참고 PDF 59 · 표준 1 · PDF 대상 누락 0
- v2 카탈로그 8건 · 공식 재현 아티팩트 ZIP 1건
- Markdown 파생본 2건 (`HAETAE-FIA-TARGET-MD`, `PCM-DFA-TARGET-MD`; 모두 `verified`)
- 기존 장부 빈 출처는 **추정 채움 금지**

## 운영

- 쓰기: `curator` only
- 신규/재검증: SCHEMA 필드 → CATALOG 행 + 파일 저장
- analyst/producer: 읽기만
