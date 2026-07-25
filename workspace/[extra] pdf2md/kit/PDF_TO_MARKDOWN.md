# PDF → Markdown 파생본 규격

이 문서가 변환·검수의 **단일 기준(SSOT)** 이다. 패키지 루트는 `kit/`의 상위(루트 `README.md` 위치)다.

## 0. 목적과 철학

### 목적

- `Papers_pdf/**/*.pdf` 아카이브 전부 → `Papers_md/` 미러 Markdown.
- `Papers_md`는 **리서치 갭 도출의 중간 입력층**이다.
- **`.pdf`가 아니면 변환·갭 컨텍스트에서 배제**한다 (README·csv 등).

### 철학

루트 `README.md` §0과 동일하며 해석에 우선 적용한다.

1. **자기 완결성 (self-contained)** — 규격·도구·예시가 이 패키지 폴더 안에서 닫힌다. 호스트 절대경로에 의존하지 않는다.
2. **Simplicity is the ultimate sophistication** — 본질만 남긴다: 아카이브 PDF → 결정론 변환 → 검사·이슈·PDF 대조 → `Papers_md` 축적 → (하류) 리서치 갭 입력. 로컬 OCR·변환 단계 생성 합성·비PDF 본문화·정규본 자동 merge는 본질이 아니다.

---

## 1. 원칙

1. 각 source PDF와 SHA-256이 해당 문서의 source of record다. 원본 교체·삭제 금지.
2. Markdown은 **경로 미러 파생본**이다. 요약·해석·재서술 금지.
3. 기계 변환(2)은 로컬 클래식만. 생성형 AI·신경망·**로컬 OCR** 금지.
4. 확정 불가는 `CONVERSION-ISSUE`.
5. 최종 인용 = source PDF **페이지**.
6. 기준본: Poppler bbox + `kit/tools/pdf_to_markdown.py`.
7. 후보본: allowlist 클래식 → `kit/candidates/<key>/` (`key` = `Papers_pdf` 아래 상대 경로에서 `.pdf` 제거).
8. Grok PDF는 **4·5 보조만** (선택).
9. **변환 대상 = `Papers_pdf` 트리의 모든 `*.pdf`** (재귀). 참고문헌 PDF 포함.

### 1.1 OCR

| 종류 | 정책 |
|------|------|
| 로컬 OCR | 금지 |
| 텍스트 층 추출 | 허용 |
| Grok | 4·5만 |
| 스캔 PDF (텍스트 층 없음) | 본 프로파일 밖 |

---

## 2. 저장·추적

| 구분 | 경로 |
|------|------|
| source PDF | `Papers_pdf/<rel>.pdf` |
| 파생 MD | `Papers_md/<rel>.md` |
| 시각 자산 | `Papers_md/<rel>/` |
| 큐 | `kit/tools/list_pdf_queue.py` |
| 후보 | `kit/candidates/<rel>/…` |
| 카탈로그 | `kit/ASSET_CATALOG.md` |
| 참고 폴더 메모 | `kit/REF_FOLDERS.md` (사람용, 갭 입력 아님) |

`relation` 예: 루트 대상 논문 `target`, 참고문헌 `reference` (스키마 값 사용).

---

## 3. 파이프라인

| 단계 | 내용 | 필수 |
|------|------|------|
| 0 | `list_pdf_queue` | 권장 |
| 1 | 아카이브 고정·카탈로그 | 필수 |
| 2a | 기준 변환 | 필수 |
| 2b | 후보 | 선택 |
| 3A | 기계 검사 | 필수 |
| 3B | CROSSCHECK | 선택 |
| 4–5 | 이슈·검수 → `verified` | 필수 |
| 하류 | Papers_md → 리서치 갭 | 입력 제공 |

세부 알고리즘(열 복원·이슈 표식 등)은 기존 deterministic-bbox-v1과 동일하다.  
`verified` 정규 경로 재실행 금지 → 임시 경로 재현.

---

## 4. 실행

패키지 루트 · 루트 상대경로.

```bash
python3 kit/tools/list_pdf_queue.py --pending-only

python3 kit/tools/pdf_to_markdown.py \
  --source "Papers_pdf/<rel>.pdf" \
  --output "Papers_md/<rel>.md" \
  --source-asset-id "<id>" \
  --derived-asset-id "<id>-MD" \
  --date YYYY-MM-DD

python3 kit/tools/run_candidates.py --source "Papers_pdf/<rel>.pdf"
python3 kit/tools/diff_candidates.py \
  --source "Papers_pdf/<rel>.pdf" \
  --canonical "Papers_md/<rel>.md"
```

`Papers_pdf/` → `Papers_md/` 로 쓸 때 상대 키 `<rel>`이 일치해야 한다 (도구가 검사).

---

## 5. 리서치 갭과의 관계

- 본 패키지의 **완료 조건(변환 쪽)** 은 아카이브 PDF가 충실한 `Papers_md` 파생본으로 쌓이는 것이다.
- 갭 도출은 `Papers_md`의 Markdown(필요 시 시각 자산)을 읽는다.
- 갭 후보를 source PDF 페이지로 재검증하는 규율은 유지한다.
- 비PDF·미변환 바이너리 PDF 원문을 갭 컨텍스트에 대량 투입하지 않는 것을 기본으로 한다 (토큰·잡음).

갭 **방법론·보고서 엔진** 자체는 별도 지시 전까지 필수 산출이 아니다. 이 문서는 입력층 품질을 보장한다.

---

## 6. 성공 지표

- 큐 pending → 0 (또는 프로파일 밖 스캔 PDF만 잔여)
- 골든셋 해시·링크 정합
- 허위 전사 없이 PDF 일치
- 선택 보강(2b/3B/Grok) 비용 합리성
