# `Papers_md/` — Markdown 파생본 (리서치 갭 입력층)

`Papers_pdf` 아카이브의 PDF를 변환한 결과물이다.  
이 트리의 **검증된 Markdown**이 이후 **리서치 갭(Research Gap) 도출**의 중간 입력이다.

```text
Papers_md/
  <rel>.md                 # Papers_pdf/<rel>.pdf 와 1:1 미러 (유일한 산출물)
```

예:

| source | output |
|--------|--------|
| `Papers_pdf/Foo.pdf` | `Papers_md/Foo.md` |
| `Papers_pdf/Foo/[1] Bar.pdf` | `Papers_md/Foo/[1] Bar.md` |

## 규칙

1. PDF가 아닌 파일은 여기에 “원본”으로 두지 않는다. 변환 대상은 오직 `Papers_pdf/**/*.pdf`.
2. **단일 PDF → 단일 MD.** 이미지 사이드카 디렉터리(`Papers_md/<rel>/*.png`)를 두지 않는다.
3. **그림:** 픽셀을 저장하지 않는다. 캡션·본문 언급 등 텍스트와 source PDF **페이지** 표기만 유지한다. 이미지 AI 분석 금지.
4. **표·알고리즘:** 그림이 아니다. 텍스트 층 내용을 최선을 다해 유지한다.
5. 최종 인용은 항상 대응 **source PDF 페이지** (`kit/PDF_TO_MARKDOWN.md`).
6. 리서치 갭 분석 시 **`Papers_md`의 `.md`만** 컨텍스트에 넣고, `Papers_pdf` 안의 README·비PDF·미변환 잡파일은 넣지 않는다.
7. 규격: `kit/PDF_TO_MARKDOWN.md`
