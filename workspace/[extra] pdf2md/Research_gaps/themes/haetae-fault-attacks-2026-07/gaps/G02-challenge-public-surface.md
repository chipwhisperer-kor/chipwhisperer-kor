# G02 — 도전값·공개계수 공격 표면

| 필드 | 값 |
|------|-----|
| id | `G02` |
| slug | `challenge-public-surface` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | A09, B21, D41 |
| status | `supported` |

## Claim (갭 후보)

공개 계수/공개 파라미터와 challenge 샘플링 루프를 결합한 공격(PCM)은 HAETAE·ML-DSA 공통 표면을 제시하나, HAETAE 전용 challenge 계수 공간·공개 판별 전 경우의 닫힌 분류는 없다.

## Why it matters (테마 연결)

축 A09·B21·D41. ‘fault attacks’만으로는 challenge vs 기타 표면이 구분되지 않는다.

## Evidence (base data)

- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf`  
  **pages:** 1, 5–8  
  **note:** public coefficient·challenge loop abort·키 복구 프레임

## Open questions

HAETAE 파라미터 세트별 challenge abort 성공 조건이 동일한가?

## Next actions

1. G71–G73과 교차; 레벨별 표 작성
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
