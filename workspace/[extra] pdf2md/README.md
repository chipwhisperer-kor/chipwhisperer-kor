# [extra] pdf2md — 논문 PDF 아카이브 → Markdown → 리서치 갭 중간층

이 폴더가 **유일한 작업 단위**다. 패키지 밖 문서·대화·다른 저장소 없이도 이어갈 수 있어야 한다.

## 0. 목적과 철학

### 목적

1. `Papers_pdf/`에 논문 PDF 아카이브가 쌓이면  
2. **모든 `*.pdf`**(하위 폴더·참고문헌 포함)를 Markdown으로 변환해 `Papers_md/`에 두고  
3. `Papers_md/`를 입력으로 **리서치 갭(Research Gap, 연구 공백) 도출**에 쓰는 **중간 단계**를 제공한다.

**비PDF는 변환·갭 컨텍스트에서 배제한다.**  
예: `Papers_pdf/.../README.md` 는 사람이 읽을 메모일 뿐, 파이프라인·모델 입력에 넣지 않는다 (토큰 낭비).

### 철학

1. **자기 완결성 (self-contained)**  
   규격·도구·예시·검수 기준이 이 폴더 안에서 닫힌다. 호스트 절대경로(`/home/…` 등)에 의존하지 않는다.

2. **Simplicity is the ultimate sophistication**  
   본질: PDF 아카이브 고정 → 결정론 기준 변환 → 기계 검사 → (선택) 클래식 후보 힌트 → 이슈 → PDF 페이지 검수 → `verified` MD 축적 → (하류) 리서치 갭.  
   덜어낼 것: 로컬 OCR, 변환 단계 생성 합성, 정규본 자동 merge, 비PDF를 본문으로 취급.

> **시작 순서:** 이 파일 §1–4 → `kit/PDF_TO_MARKDOWN.md` → `python3 kit/tools/list_pdf_queue.py` → 변환.

전제: **사용자 1명** (+ 선택 AI curator). 오프라인 핵심: 2a·2b·3A·3B. Grok는 4·5 보조만.

---

## 1. 폴더 구조

```text
[extra] pdf2md/                 # 패키지 루트
  README.md
  Papers_pdf/                   # PDF 아카이브 (재귀적으로 모든 *.pdf 가 변환 대상)
    <논문명>.pdf
    <논문명>/                   # 참고문헌 등
      [1] ….pdf
  Papers_md/                    # 파생 MD (리서치 갭 입력층)
    <논문명>.md
    <논문명>/                   # 시각 자산 등
    <논문명>/[1] ….md           # 참고문헌 미러 예
  kit/                          # 규격·도구·카탈로그·작업 부산물
    PDF_TO_MARKDOWN.md
    TOOL_ALLOWLIST.md
    REF_FOLDERS.md              # 참고문헌 폴더 사람용 메모
    ASSET_CATALOG.md
    tools/
      list_pdf_queue.py         # 변환 큐
      pdf_to_markdown.py
      run_candidates.py
      diff_candidates.py
    candidates/
```

| 경로 | 역할 |
|------|------|
| `Papers_pdf/` | source PDF 아카이브. **`*.pdf`만** 변환 대상 |
| `Papers_md/` | 파생 Markdown + 부속 자료. **갭 도출 입력** |
| `kit/` | 규격·도구·장부·후보 작업물 |
| `README.md` | 진입점 |

**경로 규칙**

1. 패키지 루트 = 이 README + `Papers_pdf` + `Papers_md` + `kit`가 있는 폴더.  
2. **루트 상대경로만** 사용. 호스트 절대경로 금지. 도구도 절대경로 거부.  
3. 미러: `Papers_pdf/<rel>.pdf` → `Papers_md/<rel>.md` (파일 stem·상대 키 동일).  
4. 임시 재현 출력은 `kit/.tmp/…` 허용 (verified 정규본 덮지 않기).

---

## 2. 환경 요구사항

| 항목 | 요구 |
|------|------|
| Poppler | `pdftotext`(`-bbox-layout`), `pdfinfo`, `pdfimages`, `pdftoppm` |
| Python 3.8+ | 2a·큐 도구는 표준 라이브러리 (+ 동봉 `paths.py`) |
| 2b 선택 | `pymupdf`, `pdfminer.six` |

로컬 OCR·변환용 생성형 AI 금지.

---

## 3. 빠른 시작

### 3.0 변환 큐 (아카이브 전체)

```bash
python3 kit/tools/list_pdf_queue.py
python3 kit/tools/list_pdf_queue.py --pending-only
python3 kit/tools/list_pdf_queue.py --json
```

### 3.1 기준 변환 (2a)

```bash
python3 kit/tools/pdf_to_markdown.py \
  --source "Papers_pdf/<rel>.pdf" \
  --output "Papers_md/<rel>.md" \
  --source-asset-id "<원본 asset_id>" \
  --derived-asset-id "<Markdown asset_id>" \
  --date YYYY-MM-DD
```

`<rel>` 예: `Foo` 또는 `Foo/[1] Bar`.

### 3.2 후보·교차 (선택)

```bash
python3 kit/tools/run_candidates.py --source "Papers_pdf/<rel>.pdf"
python3 kit/tools/diff_candidates.py \
  --source "Papers_pdf/<rel>.pdf" \
  --canonical "Papers_md/<rel>.md"
```

> **덮어쓰기:** `verified` 정규 MD에 2a 재실행 금지. 재현은 `kit/.tmp/`.

상세: `kit/PDF_TO_MARKDOWN.md`.

---

## 4. 파이프라인

| 단계 | 내용 | 필수 |
|------|------|------|
| 0 | `list_pdf_queue`로 대기 PDF 파악 | 권장 |
| 1 | PDF 아카이브 고정 + 카탈로그(대상·참고) | 필수 |
| 2a | 기준 변환 → `Papers_md/` 미러 | 필수 |
| 2b | 클래식 후보 | 선택 |
| 3A | 기계 검사 | 필수(2a) |
| 3B | CROSSCHECK | 선택 |
| 4–5 | 이슈·페이지 검수 → `verified` | 필수 |
| 하류 | `Papers_md`로 리서치 갭 도출 | 본 패키지 산출물 사용 (갭 방법론은 별도 지시 시) |

**규율:** 요약·보완 금지 · 인용 = source PDF 페이지 · 로컬 OCR 금지 · **비PDF 제외**.

---

## 5. 검증된 산출물 (초기 골든셋)

| paper_id | 내용 | 상태 |
|----------|------|------|
| `HAETAE-FIA` | 대상 논문 MD | `verified` |
| `PCM-DFA` | 대상 논문 MD | `verified` |

참고문헌 PDF는 아카이브에 포함되어 있으며, 큐상 **pending**이면 순차 변환한다.  
카탈로그: `kit/ASSET_CATALOG.md`.

---

## 6. 포함 / 미포함

| 포함 | 미포함 |
|------|--------|
| `Papers_pdf/**/*.pdf` 전부 변환 대상 | 비PDF (README, csv 등)를 변환·갭 입력으로 사용 |
| 참고문헌 PDF | 로컬 OCR, 2단계 NN 변환기 |
| `Papers_md`를 갭 도출 **입력층**으로 제공 | 이 패키지 밖의 비밀 문서 |
| 규격·도구·큐 스크립트 | (기본) 갭 보고서 자동 확정 엔진 — 별도 지시 전 |

---

## 7. 라이선스

자료는 대체로 **user-provided**, `license: unknown` 가능. 재배포·원격 업로드 전 확인·승인.

---

## 8. 역할 (`curator`)

아카이브 보존 · PDF만 변환 · 사이드카 MD · 추측 금지 · 카탈로그 갱신.  
AI만으로 `verified` 금지. 갭 단계에서도 최종 근거는 source PDF 페이지.

---

## 9. 무결성·재현

```bash
# 큐
python3 kit/tools/list_pdf_queue.py --pending-only

# 골든셋 해시 (대상 2편)
sha256sum "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf" \
          "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf"

# 2a 임시 (정규 verified 비덮어쓰기)
mkdir -p kit/.tmp
python3 kit/tools/pdf_to_markdown.py \
  --source "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf" \
  --output "kit/.tmp/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md" \
  --source-asset-id PCM-DFA-TARGET --derived-asset-id PCM-DFA-TARGET-MD --date 2026-07-25
rm -rf kit/.tmp
```

---

## 10. 출처 표기 (의존성 아님)

초기 기법은 별도 파이프라인에서 추출되었을 수 있다. **출처 표기일 뿐**, 이 폴더만으로 완결된다.
