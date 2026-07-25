# G18 — Verify 구간 전용 공백

| 필드 | 값 |
|------|-----|
| id | `G18` |
| slug | `verify-gap` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | A11–A12, D45 |
| status | `supported` |

## Claim (갭 후보)

대상 골든셋의 주 기여는 Sign(및 challenge) 쪽이며, HAETAE Verify 재계산·비교 분기에 대한 전용 fault 실증·대응이 부족하다.

## Why it matters (테마 연결)

축 A11–A12. 파이프라인 대칭 공백.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 2–3, 10  
  **note:** Verify는 서명 후 검증 대응 맥락에서 주로 등장

## Open questions

Verify 스킵으로 위조 수락이 가능한 구현 패턴이 있는가?

## Next actions

1. A11–A12 전용 실험 설계
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
