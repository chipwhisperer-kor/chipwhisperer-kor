# `Papers_pdf/` — PDF 아카이브 (변환 source)

이 트리 아래의 **모든 `*.pdf` 파일**이 변환 대상이다 (하위 폴더 포함).

```text
Papers_pdf/
  <대상 논문명>.pdf                 # 루트 대상 논문
  <대상 논문명>/                    # 참고문헌 등 관련 PDF 묶음
    [1] ….pdf
    [2] ….pdf
  …
```

## 규칙

1. **확장자 `.pdf`만** 변환·큐·리서치 갭 입력에 넣는다.  
   `README.md`, `.csv`, 기타 비PDF는 **배제**한다 (토큰·컨텍스트 낭비 방지).
2. 원본 PDF는 source of record다. 교체·삭제하지 않는다.
3. 패키지 루트 **상대경로**만 사용한다. 호스트 절대경로 금지.
4. 변환 미러: `Papers_pdf/<rel>.pdf` → `Papers_md/<rel>.md`  
   시각 자산 폴더: `Papers_md/<rel>/` (필요 시).
5. 큐 목록: `python3 kit/tools/list_pdf_queue.py`  
   미변환만: `python3 kit/tools/list_pdf_queue.py --pending-only`
6. 참고문헌 묶음 메모(사람용): `kit/REF_FOLDERS.md`

메타·해시(우선 대상): `kit/ASSET_CATALOG.md`.
