# [extra] pdf2md — 논문 PDF 아카이브 → Markdown → 리서치 갭 중간층

이 폴더가 **유일한 작업 단위**다. 패키지 밖 문서·대화·다른 저장소 없이도 이어갈 수 있어야 한다.

## 0. 목적과 철학

### 목적

**프레임워크 목표:** 논문 PDF가 충분히 쌓이면  
`Papers_pdf` → `Papers_md` → `Research_gaps/themes/<theme_id>/`  
로 **변환·품질보증·테마별 갭 발굴**을 반복 가능하게 한다.  
특정 키워드·도메인에 묶이지 않는다. 테마(의도)는 `Research_gaps`에만 쌓인다.

1. `Papers_pdf/`에 논문 PDF 아카이브가 쌓이면  
2. **모든 `*.pdf`**(하위 폴더·참고문헌 포함)를 **각 1개의** Markdown으로 변환해 `Papers_md/`에 두고  
3. `Papers_md/`를 **공유 입력**으로 **리서치 갭** 후보를 `Research_gaps/themes/<theme_id>/`에 남긴다.

**비PDF는 변환·갭 컨텍스트에서 배제한다.**  
예: `Papers_pdf` 아래 잡 README 등은 파이프라인·모델 입력에 넣지 않는다.

**그림 정책 (텍스트 전용):** 단일 PDF → 단일 MD. 그림 **픽셀·이미지 파일은 다루지 않는다.**  
캡션·본문 교차참조·`PDF_PAGE` 표기 등 비이미지 정보는 보존한다. 표·알고리즘은 그림이 아니며 텍스트 층 내용을 유지한다.  
이미지 AI 분석은 수행하지 않는다. 상세: `kit/PDF_TO_MARKDOWN.md` §1.2.

### 철학

1. **자기 완결성 (self-contained)**  
   규격·도구·예시·검수 기준·갭 폴더 계약이 이 폴더 안에서 닫힌다. 호스트 절대경로(`/home/…` 등)에 의존하지 않는다.

2. **Simplicity is the ultimate sophistication**  
   본질: PDF 아카이브 고정 → 결정론 변환·검증 → `Papers_md` 축적 → (의도별) 갭 테마 산출.  
   덜어낼 것: 로컬 OCR, 변환 단계 생성 합성, 정규본 자동 merge, 베이스 MD의 테마별 복제, 비PDF 본문화,  
   **그림 픽셀 저장(pdfimages/page render), 이미지 AI 분석, 사이드카 PNG 트리.**

> **시작 순서:** 이 파일 §1–4 → `kit/PDF_TO_MARKDOWN.md` → 변환 큐 → (선택) `Research_gaps/README.md` 로 테마 갭.

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
  Papers_md/                    # 파생 MD (리서치 갭 입력층; 텍스트만)
    <논문명>.md                 # 1 PDF → 1 MD
    <논문명>/[1] ….md           # 참고문헌 미러 예 (역시 단일 MD)
  kit/                          # 규격·도구·카탈로그·작업 부산물
    …
  Research_gaps/                # 리서치 갭 결과 (테마별; 베이스 비복사)
    INDEX.md
    themes/<theme_id>/
```

| 경로 | 역할 |
|------|------|
| `Papers_pdf/` | source PDF 아카이브. **`*.pdf`만** 변환 대상 |
| `Papers_md/` | 파생 **단일** Markdown. **갭 도출 입력** (이미지 사이드카 없음) |
| `kit/` | 규격·도구·장부·후보 작업물 |
| `Research_gaps/` | **테마별** 갭 리포트·후보 (의도마다 폴더 분리) |
| `README.md` | 진입점 |

**경로 규칙**

1. 패키지 루트 = 이 README + `Papers_pdf` + `Papers_md` + `kit` (+ `Research_gaps`)가 있는 폴더.  
2. **루트 상대경로만** 사용. 호스트 절대경로 금지. 도구도 절대경로 거부.  
3. 미러: `Papers_pdf/<rel>.pdf` → `Papers_md/<rel>.md` (상대 키 동일).  
4. 갭 결과는 `Research_gaps/themes/<theme_id>/`만; **`Papers_md`를 테마 안으로 복사하지 않음.**  
5. 임시 재현 출력은 `kit/.tmp/…` 허용 (verified 정규본 덮지 않기).

---

## 2. 환경 요구사항

| 항목 | 요구 |
|------|------|
| Poppler (필수) | `pdftotext`(`-bbox-layout`), `pdfinfo` |
| Poppler (비필수) | `pdfimages` — 진단 메타만(픽셀 저장 안 함). 없어도 2a 가능 |
| Python 3.8+ | 2a·큐 도구는 표준 라이브러리 (+ 동봉 `paths.py`) |
| 2b 선택 | `pymupdf`, `pdfminer.six` |

로컬 OCR·변환용 생성형 AI·**이미지 비전 분석** 금지. `pdftoppm` 페이지 렌더는 파이프라인에 쓰지 않는다.

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
| 하류 | `Papers_md` → `Research_gaps/themes/<theme_id>/` | 의도(키워드·질문)별 갭 산출; 계약은 `Research_gaps/README.md` |

**규율:** 요약·보완 금지 · 인용 = source PDF 페이지 · 로컬 OCR 금지 · **비PDF 제외**.

---

## 5. 변환·품질보증 산출 현황

| 구분 | 상태 |
|------|------|
| 아카이브 PDF | **61** (source of record) |
| 아카이브 PDF → MD (2a) | **61/61** (pending **0**) |
| MD `verified` 최종본 | **61/61** · `+text-only-v1` |
| `Papers_md` 이미지 | **0** |
| 리서치 갭 테마 | **0** (프레임워크·템플릿만; 하류 단계) |
| 정책 | 텍스트 전용: 단일 PDF→단일 MD, 캡션·페이지 출처 유지 |

상세: `kit/CONVERSION_STATUS.md`, `kit/ASSET_CATALOG.md`,  
`kit/conversion_batch_log.json`, `kit/curation_log.json`.

---

## 6. 포함 / 미포함

| 포함 | 미포함 |
|------|--------|
| `Papers_pdf/**/*.pdf` 전부 변환 대상 | 비PDF (README, csv 등)를 변환·갭 입력으로 사용 |
| 참고문헌 PDF | 로컬 OCR, 2단계 NN 변환기, **이미지 AI 분석** |
| `Papers_md` 단일 MD를 갭 도출 **입력층**으로 제공 | 그림 픽셀·PNG 사이드카·페이지 렌더 저장 |
| 그림 **캡션**·PDF **페이지** 출처 보존 | 그림 파일을 “전사”한 것처럼 위장하는 생성 |
| 표·알고리즘 텍스트 층 유지 | (기본) 갭 보고서 자동 확정 엔진 — 별도 지시 전 |
| 규격·도구·큐 스크립트 | |

---

## 7. 라이선스

자료는 대체로 **user-provided**, `license: unknown` 가능. 재배포·원격 업로드 전 확인·승인.

---

## 8. 역할 (`curator`)

아카이브 보존 · PDF만 변환 · 파생 MD(텍스트 전용) · 추측 금지 · 카탈로그 갱신.  
AI만으로 `verified` 금지. 갭 단계에서도 최종 근거는 source PDF 페이지.

---

## 9. 무결성·재현

```bash
# 큐
python3 kit/tools/list_pdf_queue.py --pending-only

# 아카이브 고정 확인 (대상 루트 PDF 예)
sha256sum "Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf" \
          "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf"

# 2a 임시 재현 (정규 Papers_md 비덮어쓰기; 상대경로만)
mkdir -p kit/.tmp
python3 kit/tools/pdf_to_markdown.py \
  --source "Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf" \
  --output "kit/.tmp/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md" \
  --source-asset-id PCM-DFA-TARGET --derived-asset-id PCM-DFA-TARGET-MD --date YYYY-MM-DD
rm -rf kit/.tmp
```

---

## 10. 출처 표기 (의존성 아님)

초기 기법은 별도 파이프라인에서 추출되었을 수 있다. **출처 표기일 뿐**, 이 폴더만으로 완결된다.
