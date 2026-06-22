---
marp: true
math: mathjax
paginate: true
header: "LaTeX.css와 Marp의 만남"
footer: ""
---

<style>
/* LaTeX.css 불러오기 */
@import url('../style.min.css');

/* 로컬 Noto Serif KR 폰트 */
@font-face {
    font-family: 'Noto Serif KR Local';
    src: url('../NotoSerifKR-Regular.ttf') format('truetype');
    font-weight: 400;
}
@font-face {
    font-family: 'Noto Serif KR Local';
    src: url('../NotoSerifKR-Bold.ttf') format('truetype');
    font-weight: 700;
}

/* 폰트 우선 적용 */
body, h1, h2, h3, h4, h5, h6, p, li, header, footer {
    font-family: 'Latin Modern', 'Noto Serif KR Local', serif !important;
}

/* Marp 슬라이드 기본 스타일 */
section {
    background-color: #fdfdff;
    font-size: 28px;
}

h1, h2 {
    text-align: center;
}

pre {
    background-color: #fffdfd;
    font-size: 24px;
}

/* 표 중앙 정렬 */
section table {
    display: table !important;
    margin-left: auto !important;
    margin-right: auto !important;
    max-width: 100% !important;
    word-break: keep-all;
}

/* 그림 중앙 정렬 */
section img {
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Header 스타일 */
header { font-size: 16px; }

/* 페이지 번호 (오른쪽 하단) */
section::after {
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    bottom: 5px;
    font-size: 10px;
}

/* 섹션 구분(divider) 슬라이드 */
section.divider h1 {
    border-bottom: 2px solid #333;
    padding-bottom: 0.15em;
}

/* 결론 슬라이드의 강조 박스 */
.takeaway {
    border: 1px solid #888;
    border-left: 6px solid #0000ff;
    background: #f5f5ff;
    padding: 0.5em 1em;
    margin: 0.6em 0;
    font-weight: 700;
    text-align: center;
}

/* 참고문헌 목록: 작게, 줄간격 좁게 */
.references {
    font-size: 0.78em;
    line-height: 1.45;
}

/* Title / divider 슬라이드에서 header·footer·페이지번호 숨기기 */
section.lead header,
section.lead footer,
section.lead::after {
    display: none !important;
}
</style>

<!-- _class: lead -->
# LaTeX.css와 Marp의 만남

**발표자:** 김박사  
**날짜:** 2026년 6월 16일

---

## 목차 (Contents)

<!-- 실제 발표에서는 이 목차를 여러분의 섹션 구성에 맞게 바꿔 쓰세요. -->

1. 서론 — Marp와 LaTeX.css 소개
2. 1부 · 기본 기능과 타이포그래피
3. 2부 · 목록과 레이아웃
4. 3부 · 고급 스타일과 마무리
5. 결론 및 참고문헌

---

<!-- _class: lead divider -->
# 1부 · 기본 기능과 타이포그래피

---

## 서론 (Introduction)

이 프레젠테이션은 **마크다운**만을 사용하여 작성되었습니다.
LaTeX.css를 적용하여 마치 실제 논문을 읽는 듯한 타이포그래피를 제공합니다.

* 디자인에 신경 쓸 필요가 없습니다.
* 텍스트와 논리에만 집중하세요.
* <u>_**Simplicity is the Ultimate Sophistication**_</u>

---

## 마크다운 파일에 주석 달기

아래 마크다운 주석은 발표자료에서 보이지 않습니다.

<!--
발표자료에 보이지 않는 주석은 이렇게 작성합니다.
-->

---

## 수식 입력 (Mathematics)

Marp에서 프론트매터에 `math: mathjax`를 설정하면 LaTeX 수식을 완벽하게 렌더링합니다.

근의 공식은 다음과 같습니다:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

인라인 수식도 지원합니다: 아인슈타인의 질량-에너지 등가 원리는 $E = mc^2$ 입니다.

---

## 표와 코드 (Tables & Code)

연구 데이터를 표로 나타낼 수도 있습니다.

| 모델     | 정확도  | 훈련 시간 |
|:--------:|:-------:|:---------:|
| Model A  | 92.5%   | 1.2h      |
| Model B  | 95.1%   | 2.5h      |

| 모델     | 정확도 | 훈련 시간 |
|----------|--------|-----------|
| Model A  | 92.5%  | 1.2h      |
| Model B  | 95.1%  | 2.5h      |

* 정렬 표시: `:---:` 가운데, `---:` 오른쪽, `:---`·`---` 왼쪽(기본)

```python
# 파이썬 코드 예시
def greet(name):
    print(f"Hello, {name}!")
```

---

## 이미지 삽입

Marp는 표준 Markdown 이미지 문법을 완전히 지원합니다.

![h:500](images/이미지_삽입_데모.png "이미지 설명 문구")

---

## 인용문 (Blockquote)

LaTeX.css는 인용문을 논문 스타일로 아름답게 렌더링합니다.

> 인용문은 연구 배경이나 중요한 문장을 강조할 때 유용합니다.
> LaTeX.css에서는 들여쓰기와 왼쪽 테두리로 시각적으로 구분됩니다.

중첩 인용도 지원합니다:

> 첫 번째 인용
>> 두 번째 수준의 인용문입니다.

---

<!-- _class: lead divider -->
# 2부 · 목록과 레이아웃

---

## 목록과 체크리스트 (Lists & Task Lists) (1/3)

Marp는 모든 종류의 목록을 완벽하게 지원합니다.

### 순서 없는 목록

* 항목 1
  * 하위 항목 1-1
  * 하위 항목 1-2
* **강조된 항목**
* `코드 스타일` 항목

---

## 목록과 체크리스트 (Lists & Task Lists) (2/3)

### 순서 있는 목록

1. 첫 번째 단계
2. 두 번째 단계
   1. 하위 단계
   2. 또 다른 하위 단계
3. 세 번째 단계

---

## 목록과 체크리스트 (Lists & Task Lists) (3/3)

### 체크리스트 (Task List)

* [x] LaTeX.css 적용 완료
* [x] Marp 기본 설정 완료
* [ ] 이미지 경로 확인
* [ ] 최종 PDF 내보내기

---

<style scoped>
section {
    font-size: 16px;
}
</style>

## 너무 많은 내용 다루기

폰트를 줄여 어쩔수 없는 텍스트 분량을 커버합니다.
(다만 실제 발표에서는 글자를 줄여 욱여넣기보다 슬라이드를 나누는 편이 전달에 좋습니다.)

* 항목 1
  * 하위 항목 1-1
  * 하위 항목 1-2
* **강조된 항목**
* `코드 스타일` 항목

1. 첫 번째 단계
2. 두 번째 단계
   1. 하위 단계
   2. 또 다른 하위 단계
3. 세 번째 단계

* [x] LaTeX.css 적용 완료
* [x] Marp 기본 설정 완료
* [ ] 이미지 경로 확인
* [ ] 최종 PDF 내보내기

---

## 하이퍼링크 (Hyperlinks)

Markdown의 링크 문법을 그대로 사용할 수 있습니다.

* 외부 링크: [Google](https://www.google.com)
* 제목이 있는 링크: [Marp 공식 문서](https://marp.app "Marp 공식 사이트")

---

<style scoped>
.columns {
    display: flex;
    gap: 50px;
    align-items: flex-start;
}
.column { flex: 1; }
</style>

## 두 컬럼 레이아웃

<div class="columns">
<div class="column">

### 왼쪽 컬럼

* 장점 1
* 장점 2
* 장점 3

</div>
<div class="column">

### 오른쪽 컬럼

1. 단점 1
2. 단점 2
3. 단점 3

</div>
</div>

> `gap`과 `flex` 값을 조정하면 원하는 간격과 비율을 만들 수 있습니다.

---

<!-- _class: lead divider -->
# 3부 · 고급 스타일과 마무리

---

## LaTeX.css 특별 스타일 (Theorem / Definition)

LaTeX.css는 학술 논문 스타일의 특별한 환경을 지원합니다.
정리·정의의 이름은 본문 안에 적고(괄호 권장), 증명만 `title` 속성으로 이름을 답니다.

<div class="theorem">

(피타고라스 정리) 직각삼각형에서 빗변의 제곱은 다른 두 변의 제곱의 합과 같다.

</div>

<div class="definition">

(함수의 연속성, Continuity) 함수 $f$가 점 $a$에서 연속이라는 것은 $\lim_{x \to a} f(x) = f(a)$ 가 성립함을 뜻한다.

</div>

<div class="proof" title="피타고라스 정리">

넓이가 같은 두 정사각형을 비교하여 보일 수 있다.

</div>

---

<!-- _backgroundColor: #f0f0ff -->
<!-- _color: #0000ff -->

## 슬라이드별 스타일 변경 예시

각 슬라이드마다 배경색이나 스타일을 다르게 적용할 수 있습니다.
이 슬라이드는 연한 파란색 배경에 어두운 파랑색 글씨로 표시됩니다.

* `backgroundColor` 지시어로 배경색 변경
* `color` 지시어로 글자색 변경

---

## 결론 및 기여 (Conclusion & Contributions)

본 연구의 기여는 다음 세 가지입니다.

1. **첫 번째 기여** — 무엇을 처음으로/더 낫게 했는지 한 줄로.
2. **두 번째 기여** — 앞 항목과 병렬 구조로 간결하게.
3. **세 번째 기여** — 청중이 기억할 핵심만 남기기.

<div class="takeaway">

"제안 기법은 □□를 통해 △△ 성능을 ○○ 개선한다."

</div>

**한계와 향후 연구:** 한두 줄로 솔직하게 (예: 데이터 규모 한계 → 대규모 검증이 다음 단계).

<center>이메일 user@gmail.com · 논문 arXiv:2606.xxxxx · 코드 github.com/user/project</center>

---

## 참고문헌 (References)

<div class="references">

[1] 김박사, 이연구, "LaTeX.css 기반 학술 슬라이드 제작 기법," *한국정보보호학회 논문지*, 53(2), pp. 101–110, 2026.
[2] Doerig, V., "LaTeX.css: Make your website look like a LaTeX document," *GitHub*, 2024.
[3] Marp Team, "Marpit Framework Documentation," https://marpit.marp.app, 2025.
[4] Author, A. and Author, B., "Citation Processing in Document Pipelines," *Proc. of XYZ*, pp. 55–62, 2025.

</div>

> Marp에는 참고문헌 자동 생성 기능이 없어 직접 정리합니다.
> 인용 자동화가 꼭 필요하면 Pandoc(`--citeproc` + `.bib`) 파이프라인이 정석입니다.
