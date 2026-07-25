# 시각 파생자산 (`assets/`)

Markdown 파생본이 참조하는 **시각 자산**을 보관한다. source PDF의 그림·표·알고리즘·저자 사진을 **기계적으로 추출**한 것이다.

```text
assets/<paper_id>/<derived_asset_id>/
  MANIFEST.md          # 각 이미지의 source PDF 페이지·종류·크기·bytes·SHA-256
  p<NN>-*.png          # 페이지별 추출 이미지
```

- `pdfimages -png`: PDF에 포함된 래스터 스트림(그림·사진)을 재인코딩 없이 내용 추출.
- page crop: Poppler로 source PDF를 렌더링(예: 200 dpi)한 뒤 원문 영역만 기계적으로 crop.
- **의미 보완·재그림·생성형 이미지 처리는 하지 않는다.** 접근성 설명 등은 별도 분석 산출물로 두며 파생본·매니페스트에 넣지 않는다.
- 각 이미지는 `MANIFEST.md`에 source PDF 페이지와 SHA-256으로 추적된다. 최종 인용 기준은 언제나 source PDF 페이지다.

현재 자산: `HAETAE-FIA/HAETAE-FIA-TARGET-MD/`(20개), `PCM-DFA/PCM-DFA-TARGET-MD/`(20개).
