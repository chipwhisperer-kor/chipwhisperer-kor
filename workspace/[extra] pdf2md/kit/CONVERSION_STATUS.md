# 변환·품질보증 상태

**기준일:** 2026-07-26  
**정책:** 텍스트 전용 (`text-only-v1`) — 단일 PDF → 단일 MD, 그림 픽셀 미저장  
**상태:** **변환·QA 완료** — 전 아카이브 verified 최종본

| 로그 | 내용 |
|------|------|
| `conversion_batch_log.json` | 2a 전량 기계 변환 |
| `curation_log.json` | text-only 큐레이션 → verified |

## 요약

| 항목 | 값 |
|------|-----|
| `Papers_pdf/**/*.pdf` | **61** |
| `Papers_md` 미러 MD | **61** (pending **0**) |
| MD `verification=verified` | **61** |
| 프로파일 | `deterministic-bbox-v1+text-only-v1` |
| 잔여 `CONVERSION-ISSUE` | **0** |
| `Papers_md` 이미지 파일 | **0** |

## 수행 범위

1. **2a** 결정론 bbox 변환 + 3A 자동 소비 검사 (전 PDF).  
2. 캡션 보존 · figure-omission 표기 · `PDF_PAGE` 페이지 표식.  
3. **`curate_to_verified.py`** — 글리프 private-use/replacement 제거, 이슈 0, 메타 `verified`.  
4. **이미지 미저장** — pdfimages/page render PNG 없음.

## 의도적 한계

- 표·수식은 텍스트 층 전사 범위. 셀 단위 LaTeX 재조판·수동 골든 대조는 선택 프로파일.  
- 그림 픽셀은 의도적으로 없다. 필요 시 source PDF 페이지를 연다.  
- 2b/3B 전량은 선택 단계.

## 재확인

```bash
python3 kit/tools/list_pdf_queue.py --pending-only   # 기대: pending 0
grep -rh 'verification:' Papers_md --include='*.md' | sort | uniq -c
find Papers_md -name '*.png' | wc -l                 # 기대: 0
```
