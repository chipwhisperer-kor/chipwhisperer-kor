# [extra] pdf2md — 논문 PDF→Markdown 변환 패키지

**자기완결 패키지.** 이 폴더 하나만 있으면 논문 PDF를 검증 가능한 Markdown 파생본으로 변환하는 작업을 제로부터 다시 시작하지 않고 이어갈 수 있다. 기법·도구·규격·검수 기준·검증된 산출물 예시가 모두 안에 있다.

> **외부 프로젝트 매니저에게:** 지금까지의 PDF→Markdown 변환 작업과 기술은 **전부 이 패키지 안에 있다.** 문의 대신 이 `README.md`부터 읽고, 상세는 `Papers/PDF_TO_MARKDOWN.md`(규격 SSOT)를 보라. 이 패키지 밖의 어떤 파일·프로젝트에도 의존하지 않는다.

전제 자원: **AI 서비스 1개 + 사용자 1명.** 아래 「역할」 참고 — 원본 프로젝트의 `curator` 역할이 하던 수집·검증·변환 규율을 1인 AI가 그대로 수행한다.

---

## 1. 폴더 구성

| 경로 | 내용 | 성격 |
|------|------|------|
| `README.md` | 이 문서 — 패키지 진입점·사용법·주의 | 안내 |
| `Papers/PDF_TO_MARKDOWN.md` | **변환 규격·검수 기준 SSOT** (원칙·결정론적 변환·자동 검사·페이지별 검수·수동 교정·실행) | 규격 |
| `Papers/tools/pdf_to_markdown.py` | Poppler bbox 기반 **결정론적 변환기** (생성형 AI·OCR 미사용) | 도구 |
| `Papers/ASSET_CATALOG_SCHEMA.md` | 자산 메타데이터 **필드 규격** | 규격 |
| `Papers/ASSET_CATALOG.md` | 이 패키지 변환 자산 4건의 **메타 기록**(원본 PDF 2 + 파생본 2) | 기록 |
| `Papers/<stem>.pdf` | 검증된 예시의 **source PDF**(원본·source of record) | 산출물 |
| `Papers/<stem>.md` | 같은 stem의 **verified Markdown 파생본** | 산출물 |
| `Papers/assets/<paper_id>/<...-TARGET-MD>/` | 파생본 **시각 자산**(그림·표·알고리즘 crop·저자 사진) + `MANIFEST.md` | 산출물 |
| `Papers/assets/README.md` | 시각 자산 레이아웃 설명 | 안내 |

`Papers/`가 변환 작업 공간이다. 명령·경로·파생본 머리말이 모두 이 레이아웃을 기준으로 하므로 **폴더 이름을 바꾸지 말 것.**

---

## 2. 환경 요구사항

| 항목 | 요구 | 확인 방법 |
|------|------|-----------|
| **Poppler** (`pdftotext` · `pdfimages` · `pdftoppm` · `pdfinfo`) | `-bbox-layout` 지원 버전. 산출물은 **26.01.0**으로 생성 | `pdftotext -v` |
| **Python** | 3.8+ (표준 라이브러리만 사용, 외부 패키지 없음) | `python3 --version` |
| 네트워크 | 불필요 (변환은 전부 로컬) | — |

설치 예: Debian/Ubuntu `sudo apt-get install poppler-utils` · macOS `brew install poppler`.
Poppler 버전이 다르면 좌표·추출이 미세하게 달라질 수 있으니 파생본 머리말의 `pdftotext` 버전을 함께 기록한다.

**변환에 생성형 AI·신경망·OCR을 쓰지 않는다** (`PDF_TO_MARKDOWN.md` §1·3). 결정론적이라 같은 입력·같은 도구 버전이면 같은 출력이 나온다.

---

## 3. 빠른 시작

패키지 루트(이 `README.md`가 있는 폴더)에서 실행한다. 경로는 **루트 상대경로**여야 하고(절대경로는 도구가 거부한다), source와 output은 **같은 stem**이어야 한다.

```bash
python3 Papers/tools/pdf_to_markdown.py \
  --source "Papers/<논문명>.pdf" \
  --output "Papers/<논문명>.md" \
  --source-asset-id "<원본 asset_id>" \
  --derived-asset-id "<Markdown asset_id>" \
  --date YYYY-MM-DD
```

표준 출력에 JSON 검증 요약이 찍히고, 같은 수치가 파생본 머리말 `<!-- PDF_TO_MARKDOWN_METADATA ... -->`에도 기록된다. 둘이 일치해야 한다.

기계 변환은 시작일 뿐이다. 표·수식·시각 자산은 이어서 **사람(또는 AI)이 source PDF와 페이지별로 대조·교정**해야 `verified`가 된다. 전체 절차는 `Papers/PDF_TO_MARKDOWN.md` §4–6.

> **주의 (덮어쓰기):** `--output`을 **이미 `verified`인 파생본의 정규 경로**(`Papers/<stem>.md`)로 지정해 재실행하면, 도구는 원시 기계 변환본을 쓰므로 **수동 교정 결과가 사라진다.** 정규 경로 출력은 **새 논문**에만 쓰고, 기존 예시를 재현·확인만 할 때는 §9처럼 **임시 경로**로 출력한다.

---

## 4. 변환 파이프라인 (요약 — 상세는 `Papers/PDF_TO_MARKDOWN.md`)

| 단계 | 하는 일 | 산출·검사 |
|------|---------|-----------|
| 1. 원본 고정 | PDF와 SHA-256을 source of record로 고정. 원본은 교체·삭제 안 함 | `ASSET_CATALOG.md` 행 |
| 2. 결정론적 변환 | `pdftotext -bbox-layout` 좌표로 2단 열 순서 복원·블록 병합 → Markdown | 도구 JSON 요약 |
| 3. 자동 검사 | 페이지 수 = 페이지 표식 수 · 모든 bbox 단어/블록/숫자 토큰이 정확히 1회 소비 · 절대경로 없음 · provenance 머리말 | 불일치 시 예외로 중단 |
| 4. 이슈 표식 | 확정 못한 읽기 순서·수식·표·시각 내용은 추측 없이 `CONVERSION-ISSUE`로 표시 | 이슈 있으면 `partial` |
| 5. 페이지별 검수·교정 | source PDF를 보며 문단 순서·숫자·표·수식·캡션 대조. 표는 Markdown 표, 수식은 LaTeX, 그림은 PDF에서 추출한 원본 이미지/crop 삽입 | 이슈 0·전 페이지 대조 시 `verified` |

**규율 (변하지 않는다):** 요약·보완·해석·재서술을 넣지 않는다 · 최종 인용 기준은 Markdown 줄이 아니라 **source PDF 페이지**다 · 확정 못 하면 추측하지 않고 이슈로 남긴다.

---

## 5. 검증된 산출물 (worked examples)

두 편 모두 자동 검사 통과 + 전 페이지 수동 대조 완료 → `verified`. 재현·교차확인의 기준점이다.

| paper_id | 논문 | 쪽 | 파생본 bytes / SHA-256 | 상태 |
|----------|------|----|------------------------|------|
| `HAETAE-FIA` | 양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법 | 14 | 53,346 / `aa774afb…9ceff` | `verified` |
| `PCM-DFA` | Public Coefficient Matters: A Practical Differential Fault Attack on ML-DSA and HAETAE | 10 | 58,525 / `c129062d…4e7219` | `verified` |

- 수식·알고리즘·표 구조 전사 완료, 시각 자산은 `assets/<paper_id>/<...-TARGET-MD>/`에 추출·매니페스트화(각 이미지에 source PDF 페이지·SHA-256 기록).
- 파생본 머리말이 원본 SHA-256·도구 버전·단어/블록 소비 수치를 담아 provenance를 자체 증명한다.
- 전체 메타(bytes·해시·검증 근거)는 `Papers/ASSET_CATALOG.md`.

---

## 6. 포함 / 미포함

| 포함 | 미포함 (의도적) |
|------|------------------|
| 변환 기법·도구·규격·스키마 | 원본 프로젝트의 참고문헌 PDF·표준문서(FIPS 204) — 변환 대상이 아님 |
| 검증된 파생본 2편 + source PDF + 시각 자산 | 레거시 파일 장부(`reference-download-manifest.csv`) — 변환 무관 |
| 변환 자산 4건의 카탈로그 행 | 분석·발표(Marp) 산출물 — 다른 역할·다른 파이프라인 |

이 패키지는 **PDF→Markdown 변환**만 다룬다. 분석·해석·발표는 범위 밖이다(`PDF_TO_MARKDOWN.md` §7의 「향후 활용 메모」는 비활성 참고).

---

## 7. 라이선스·접근 주의 (중요 — 그대로 인계)

두 source PDF는 **사용자 제공(user-provided)** 자료이고 **재배포 라이선스가 확인되지 않았다(`license: unknown`).** 파생본도 같은 제약을 물려받는다.

| 자산 | access | license | 비고 |
|------|--------|---------|------|
| `HAETAE-FIA-TARGET` | user-provided | unknown | KCI 저작권 고지 확인, 재배포 라이선스 미확인 |
| `PCM-DFA-TARGET` | user-provided | unknown | 미출판 원고(unpublished manuscript) |

**공개 재배포 전 반드시 저작권·라이선스를 별도 확인할 것**(스키마 검증 원칙 §3 — 라이선스 불명 자료 재배포 금지). 확인 불가 필드는 `unknown`으로 두고 **추측해 채우지 않는다**(스키마 필드 정의 — `creators`·`year`·`license` 「확인 불가 시 unknown」).

---

## 8. 역할 매핑 (1인 AI 운용)

원본 문서의 `curator`는 「수집·검증·변환·정리」 역할이다. AI 1개·사용자 1명 구성에서는 **그 AI가 curator 역할을 맡는다.** 규율은 그대로다:

- 원본을 무단 교체·삭제하지 않는다 · 확정 못 한 것은 추측하지 않고 이슈로 남긴다.
- 파생본은 원본을 **대체하지 않는 사이드카**다 — 최종 인용은 언제나 source PDF 페이지.
- 새 자산은 `ASSET_CATALOG_SCHEMA.md` 필드를 채워 `ASSET_CATALOG.md`에 한 행으로 기록한다. 새 논문의 `paper_id`·`asset_id`는 AI가 예시 패턴(`<약칭>-TARGET` / `<약칭>-TARGET-MD`)을 따라 부여한다.

복사된 규격 문서에는 원본 **다역할 프로젝트**의 이름이 일부 남아 있다 — `PDF_TO_MARKDOWN.md` §7의 `analyst`·`ROADMAP`·`마일스톤`·「역할 인계」. 이 1인 구성에는 그런 별도 역할·산출물·게이트가 없다. 해당 §7 「향후 활용 메모」는 **비활성**이며(분석·해석은 이 패키지 범위 밖 — §6), 이 패키지의 활성 범위는 §7 상단까지의 **변환·검증**이다.

---

## 9. 무결성·재현 확인

패키지를 받은 직후 아래로 자체 검증할 수 있다(패키지 루트에서).

```bash
# (a) 파생본·원본이 카탈로그 SHA-256과 일치하는지
sha256sum "Papers/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf" \
          "Papers/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf"
#   → ASSET_CATALOG.md의 sha256 값과 대조

# (b) 도구가 이 환경에서 도는지 (임시 출력 후 삭제; stem은 source와 같아야, 경로는 루트 상대여야 함)
mkdir -p Papers/.tmp
python3 Papers/tools/pdf_to_markdown.py \
  --source "Papers/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf" \
  --output "Papers/.tmp/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md" \
  --source-asset-id PCM-DFA-TARGET --derived-asset-id PCM-DFA-TARGET-MD --date 2026-07-25
rm -rf Papers/.tmp
```

(b)는 원시 기계 변환이라 검증 결과가 `partial`로 나온다(시각·표 이슈를 아직 교정 전이라 정상). 배포된 `.md`는 그 뒤 **수동 교정을 마친 `verified` 판**이다. 도구가 exit 0으로 돌고 `source_sha256`·`pages`·단어 소비 수치가 나오면 환경 정상이다.

이 패키지는 생성 시점에 (a) 4개 파일 해시 일치, (b) 도구 정상 실행(PCM 10쪽·bbox 단어 9208/9208 전량 소비)을 확인했다.

---

## 10. 출처 (provenance, 의존성 아님)

이 패키지는 `Paper-Deep-Dive` 연구 파이프라인의 `curator` 역할 산출물에서 **PDF→Markdown 변환 부분만** 추출했다. 출처 표기일 뿐이며, 이 패키지는 그 프로젝트에 의존하지 않는다 — 여기 있는 것만으로 완결된다.
