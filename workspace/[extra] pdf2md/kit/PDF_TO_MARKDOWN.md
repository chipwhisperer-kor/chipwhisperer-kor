# PDF → Markdown 파생본 규격

이 문서가 변환·검수의 **단일 기준(SSOT)** 이다. 패키지 루트는 `kit/`의 상위(루트 `README.md` 위치)다.

## 0. 목적과 철학

### 목적

- `Papers_pdf/**/*.pdf` 아카이브 전부 → `Papers_md/` **단일 MD 미러** (`1 PDF → 1 MD`).
- `Papers_md`는 **리서치 갭 도출의 중간 입력층**이다.
- **`.pdf`가 아니면 변환·갭 컨텍스트에서 배제**한다 (README·csv 등).

### 철학

루트 `README.md` §0과 동일하며 해석에 우선 적용한다.

1. **자기 완결성 (self-contained)** — 규격·도구·예시가 이 패키지 폴더 안에서 닫힌다. 호스트 절대경로에 의존하지 않는다.
2. **Simplicity is the ultimate sophistication** — 본질만 남긴다: 아카이브 PDF → 결정론 변환 → 검사·이슈·PDF 대조 → `Papers_md` 축적 → (하류) 리서치 갭 입력. 로컬 OCR·변환 단계 생성 합성·비PDF 본문화·정규본 자동 merge·**그림 픽셀 저장·이미지 AI 분석**은 본질이 아니다.

---

## 1. 원칙

1. 각 source PDF와 SHA-256이 해당 문서의 source of record다. 원본 교체·삭제 금지.
2. Markdown은 **경로 미러 파생본**이다. 요약·해석·재서술 금지.
3. 기계 변환(2a)은 로컬 클래식만. 생성형 AI·신경망·**로컬 OCR**·**이미지 비전 분석** 금지.
4. 확정 불가는 `CONVERSION-ISSUE`.
5. 최종 인용 = source PDF **페이지**.
6. 기준본: Poppler bbox + `kit/tools/pdf_to_markdown.py`.
7. 후보본: allowlist 클래식 → `kit/candidates/<key>/` (`key` = `Papers_pdf` 아래 상대 경로에서 `.pdf` 제거).
8. Grok PDF는 **4·5 보조만** (선택).
9. **변환 대상 = `Papers_pdf` 트리의 모든 `*.pdf`** (재귀). 참고문헌 PDF 포함.
10. **단일 PDF → 단일 MD.** 사이드카 이미지 디렉터리·PNG 배치는 하지 않는다.

### 1.1 OCR·비전

| 종류 | 정책 |
|------|------|
| 로컬 OCR | 금지 |
| 텍스트 층 추출 | 허용 |
| 이미지 AI 분석 / 비전 전사 | **금지** |
| Grok | 4·5만 (텍스트·구조 검수; 그림 픽셀 해석 목적 아님) |
| 스캔 PDF (텍스트 층 없음) | 본 프로파일 밖 |

### 1.2 그림·표·알고리즘 (필수)

| 객체 | 정책 |
|------|------|
| **그림 (Figure)** | **픽셀·이미지 파일을 저장하지 않는다.** 텍스트 층의 **캡션·본문 언급**은 보존한다. 출처는 **source PDF 페이지** (`<!-- PDF_PAGE: N -->`, figure-omission 표기). |
| **표 (Table)** | 그림이 **아니다.** 텍스트 층·복사 가능 내용을 **최선을 다해 훼손 없이** MD에 유지한다. |
| **알고리즘 (Algorithm)** | 그림이 **아니다.** 의사코드·번호 목록 등 텍스트 전사를 유지한다. |
| 수식 | 텍스트 층 그대로; 글리프 손상 시 `GLYPH_MAPPING` 이슈. |
| 저자 사진 등 | 저장하지 않음 (갭·본문 근거 아님). |

그림 관련 **비이미지 정보**(캡션 문구, “Fig. n” 표식, 본문 교차참조, 페이지 번호)는 반드시 남긴다.  
그림 픽셀이 없어 생기는 공백을 AI로 메우지 않는다. 필요 시 사용자는 source PDF 해당 페이지를 본다.

---

## 2. 저장·추적

| 구분 | 경로 |
|------|------|
| source PDF | `Papers_pdf/<rel>.pdf` |
| 파생 MD | `Papers_md/<rel>.md` (**유일한** 파생 산출물) |
| ~~시각 자산 디렉터리~~ | **사용하지 않음** (레거시 `Papers_md/<rel>/` 는 제거 대상) |
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
| 2a | 기준 변환 (텍스트 전용) | 필수 |
| 2b | 후보 | 선택 |
| 3A | 기계 검사 | 필수 |
| 3B | CROSSCHECK | 선택 |
| 4–5 | 이슈·검수 → `verified` | 필수 |
| 하류 | Papers_md → 리서치 갭 | 입력 제공 |

세부 알고리즘(열 복원·이슈 표식 등)은 deterministic-bbox-v1을 따른다.  
`verified` 정규 경로 재실행 금지 → 임시 경로 재현.

**Poppler bbox XML:** 일부 PDF의 `pdftotext -bbox-layout` 출력에 XML 1.0 불법 제어 문자(예: U+0002)가 포함되어 파서가 실패할 수 있다.  
`kit/tools/pdf_to_markdown.py`의 `sanitize_poppler_bbox_xml`이 파싱 전에 이를 제거한다. 배치 실패 원인·해소 기록은 `CONVERSION_STATUS.md`를 본다.

### `verified` 프로파일

| profile | 의미 |
|---------|------|
| `deterministic-bbox-v1+manual-structure-v1` | 대상 골든셋: 페이지 수동 대조, 표 MD·수식 LaTeX 등 **텍스트** 보강. **이미지 파일 없음.** |
| `deterministic-bbox-v1+text-only-v1` | 아카이브 품질보증: 2a+3A 통과, `CONVERSION-ISSUE` 0, **이미지 미저장**, 캡션·페이지 표기 유지, 글리프 제어문자 제거. 표·수식·알고리즘은 텍스트 층 전사 |

~~`+visual-assets-v1`~~ — **폐기.** pdfimages/page render·PNG 사이드카를 쓰지 않는다.

공통 조건: 페이지 표식 수 = PDF 쪽 수, 자동 소비 검사 통과(2a 시점), 미해결 `CONVERSION-ISSUE` 없음.  
큐레이션 도구: `kit/tools/curate_to_verified.py` (이미지 링크 제거·레거시 자산 디렉터리 삭제).

**이슈 정책**

| 이슈 | 취급 |
|------|------|
| `GLYPH_MAPPING` | 유지 (수식·기호 손상) |
| ~~`VISUAL_NOT_TRANSCRIBED`~~ | **발행하지 않음** (그림 픽셀 생략은 정책) |
| ~~`RASTER_IMAGE_NOT_TRANSCRIBED`~~ | **발행하지 않음** (진단 카운트만 메타데이터) |

캡션으로 보이는 블록 뒤에는 선택적으로  
`> [FIGURE omitted — image not stored; caption/text above; cite source PDF page N]`  
를 붙일 수 있다 (픽셀 대체 아님).

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

# 텍스트 전용 큐레이션·레거시 이미지 제거 → verified
python3 kit/tools/curate_to_verified.py
```

`Papers_pdf/` → `Papers_md/` 로 쓸 때 상대 키 `<rel>`이 일치해야 한다 (도구가 검사).

---

## 5. 리서치 갭과의 관계 (프레임워크)

패키지 전체 목표는 **도메인 비종속** 파이프라인이다:

```text
Papers_pdf (아카이브) → Papers_md/*.md (공유 베이스, 텍스트만) → Research_gaps/themes/<theme_id>/
```

- **변환 완료 조건(본 문서):** 대상 PDF가 충실한 **단일** `Papers_md/<rel>.md`로 쌓임.
- **갭 결과 계약:** `Research_gaps/README.md` — 테마마다 `META` / `SCOPE` / `gaps/` / (선택) `REPORT`.
- 같은 `Papers_md`에 **여러 theme_id**를 병렬로 둘 수 있다. 베이스를 테마 폴더에 복사하지 않는다.
- 갭 후보는 source **PDF 페이지**로 재검증한다.
- 갭 컨텍스트: **`Papers_md`의 `.md`만** (이미지·사이드카 없음). 비PDF·원문 PDF 대량 투입 기본 금지.
- `Research_gaps/INDEX.md`의 개별 테마는 **worked example**일 수 있으며 프레임워크 필수가 아니다.
- 변환 도구(`kit/tools`)는 갭 자동 엔진이 아니다.

---

## 6. 성공 지표

- 큐 pending → 0 (또는 프로파일 밖 스캔 PDF만 잔여)
- 아카이브 PDF sha256 고정 · MD 페이지 표식 수 = PDF 쪽 수
- 허위 전사 없이 PDF 일치 (텍스트 층 범위)
- **`Papers_md`에 이미지 파일 0** · **1 PDF → 1 MD**
- 선택 보강(2b/3B/Grok) 비용 합리성
