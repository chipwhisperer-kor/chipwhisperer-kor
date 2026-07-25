# `Papers_md/` — Markdown 파생본 (리서치 갭 입력층)

`Papers_pdf` 아카이브의 PDF를 변환한 결과물이다.  
이 트리의 **검증된 Markdown**이 이후 **리서치 갭(Research Gap) 도출**의 중간 입력이다.

```text
Papers_md/
  <rel>.md                 # Papers_pdf/<rel>.pdf 와 1:1 미러
  <rel>/                   # 해당 논문 시각 자산·MANIFEST (필요 시)
```

예:

| source | output |
|--------|--------|
| `Papers_pdf/Foo.pdf` | `Papers_md/Foo.md` |
| `Papers_pdf/Foo/[1] Bar.pdf` | `Papers_md/Foo/[1] Bar.md` |

## 규칙

1. PDF가 아닌 파일은 여기에 “원본”으로 두지 않는다. 변환 대상은 오직 `Papers_pdf/**/*.pdf`.
2. 이미지 링크는 MD 기준 상대경로: 자산이 `Papers_md/<rel>/file.png`이면 링크는 그에 맞게.
3. 최종 인용은 항상 대응 **source PDF 페이지** (`kit/PDF_TO_MARKDOWN.md`).
4. 리서치 갭 분석 시 **`Papers_md`의 `.md` (및 명시적으로 첨부한 자산)** 만 컨텍스트에 넣고, `Papers_pdf` 안의 README·비PDF·미변환 잡파일은 넣지 않는다.
5. 규격: `kit/PDF_TO_MARKDOWN.md`
