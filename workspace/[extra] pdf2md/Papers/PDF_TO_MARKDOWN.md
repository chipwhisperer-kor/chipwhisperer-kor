# PDF → Markdown 파생본 규격

`curator` 소유. PDF 원본을 AI가 읽기 쉬운 Markdown으로 옮길 때의 단일 기준이다.

## 1. 원칙

1. PDF와 그 SHA-256이 **source of record**다. 원본은 교체·삭제하지 않는다.
2. Markdown은 같은 stem의 **파생본**이다. 요약·교정·보완·해석·재서술을 넣지 않는다.
3. 변환은 `tools/pdf_to_markdown.py`와 Poppler `pdftotext -bbox-layout`의 좌표·문자, `pdfimages -list`의 이미지 존재 정보만 사용한다. 생성형 AI나 신경망은 변환에 사용하지 않는다.
4. 확정할 수 없는 읽기 순서, 수식, 표 셀, 시각 내용은 추측하지 않고 `CONVERSION-ISSUE`로 표시한다.
5. 분석의 최종 인용 위치는 Markdown 줄이 아니라 PDF 페이지다.

## 2. 저장·추적

- 원본과 파생본: `Papers/<같은 stem>.pdf` + `.md`
- 원본·파생본은 각각 `Papers/ASSET_CATALOG.md` 행과 SHA-256을 갖는다.
- 파생본 행의 `notes`가 원본 `asset_id`를 `derived-from`으로 가리킨다.
- 기존 카탈로그 필드와 `verification` 값(`partial` / `verified`)을 재사용한다. 새 상태를 만들지 않는다.

## 3. 결정론적 변환

1. `pdfinfo`로 암호화·페이지 수·텍스트 층을 확인한다.
2. `pdftotext -bbox-layout`으로 단어·블록 좌표를 추출한다.
3. 페이지를 전폭 블록과 좌·우 열로 나눈다. 전폭 블록 사이마다 왼쪽 열을 먼저, 오른쪽 열을 다음에 배치한다.
4. 같은 열·같은 행에서 좌표가 인접한 단일행 블록은 왼쪽에서 오른쪽으로 병합한다.
5. PDF 페이지마다 `<!-- PDF_PAGE: n -->`과 `## PDF page n`을 둔다.
6. 명백한 절 제목만 기계적 정규식으로 Markdown heading으로 표시한다.
7. Figure·Table·Algorithm 표식은 캡션 텍스트와 함께 보존한다. `pdfimages -list`로 캡션 없는 래스터 이미지도 검출하며, 시각 본문은 PDF에 남아 있음을 `CONVERSION-ISSUE`로 표시한다.
8. PDF 전용 글리프 영역이나 대체문자가 검출되면 수식·기호 손상 가능성을 해당 페이지에 표시한다.

텍스트 층이 없는 스캔 PDF는 본 프로파일로 처리하지 않는다. OCR은 별도 사용자 승인 없이는 사용하지 않는다.

## 4. 자동 검사

- PDF 페이지 수 = Markdown 페이지 표식 수
- 모든 bbox 단어가 정확히 한 번 변환 입력으로 소비됨
- 원본 SHA-256·도구 버전·변환일·단어 수·블록 수·이슈 수가 Markdown 머리말에 기록됨
- 시각 표식과 PDF 전용 글리프가 조용히 누락되지 않고 이슈로 집계됨
- 출력 파일에 절대경로가 없음

## 5. curator 페이지별 검수

각 페이지에서 아래를 PDF와 대조한다.

- 좌열 → 우열의 문단 순서
- 제목·절·각주·캡션·참고문헌의 존재
- 숫자·단위·백분율·인용 번호
- 표의 행·열 대응과 수식·기호
- Figure/Table/Algorithm 시각 내용의 명시적 미전사 표식
- 앞뒤 페이지에서 분리된 문장의 연속성

미해결 `CONVERSION-ISSUE`가 하나라도 있거나 표·수식의 정확한 전사가 끝나지 않았으면 `partial`이다. 모든 페이지를 대조하고 이슈를 해소한 경우에만 `verified`다.

### 수동 교정 단계

- 기계 변환 뒤 curator가 PDF 페이지를 보며 표는 Markdown 표, 수식은 LaTeX로 전사할 수 있다.
- 그림·그래프·다이어그램·사진은 의미를 재서술하지 않고 PDF에서 추출한 원본 이미지 또는 페이지 crop을 삽입한다.
- 파생 이미지 경로는 `Papers/assets/<paper_id>/<derived_asset_id>/`이며, `MANIFEST.md`에 source PDF 페이지·SHA-256을 기록한다.
- 수동 교정은 원문에 없는 설명을 추가하지 않는다. 접근성 설명이 필요해도 별도 분석 역할의 산출물로 두며 본 파생본에는 넣지 않는다.
- 수동 교정 후 기계 변환 머리말의 원시 추출 수치는 provenance로 보존하고, 교정 프로파일·현재 이슈 수·검수 범위를 추가한다.

## 6. 실행

프로젝트 루트에서 실행한다.

```bash
python3 Papers/tools/pdf_to_markdown.py \
  --source "Papers/<논문명>.pdf" \
  --output "Papers/<논문명>.md" \
  --source-asset-id "<원본 asset_id>" \
  --derived-asset-id "<Markdown asset_id>" \
  --date YYYY-MM-DD
```

표준 출력의 JSON 검증 요약과 Markdown 머리말의 수치가 일치해야 한다.

## 7. 향후 활용 메모 — 비활성

`verified` Markdown 묶음은 빠른 리서치 갭 **후보 발굴**의 발견 계층으로 활용할 수 있다. 선형화된 절·표·수식·참고문헌을 여러 논문 사이에서 검색·청킹·비교한 뒤, 모든 후보를 source PDF 페이지의 표·그래프·수식·각주·인용 문맥으로 재검증한다.

한 편의 Markdown만으로 분야 수준 연구 갭을 확정하지 않는다. 실제 갭 분석·해석은 `analyst` 책임이며, curator는 검증된 자산과 PDF 페이지 추적성을 제공한다.

이 메모는 향후 가능성을 보존하기 위한 것이며 현재 ROADMAP·마일스톤·활성 업무가 아니다. 별도 사용자 지시와 역할 인계 전에는 착수하지 않는다.
