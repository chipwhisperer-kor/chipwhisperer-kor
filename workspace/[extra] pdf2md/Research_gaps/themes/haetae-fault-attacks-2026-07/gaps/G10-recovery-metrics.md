# G10 — 복구 목표·성공 지표 표준

| 필드 | 값 |
|------|-----|
| id | `G10` |
| slug | `recovery-metrics` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | I85–I90, D42–D45 |
| status | `candidate` |

## Claim (갭 후보)

키 복구·위조·성공률·오버헤드가 논문마다 다른 정의로 보고되어, 축 I의 비교 가능한 지표 세트가 없다.

## Why it matters (테마 연결)

축 I. 갭 우선순위 산정에 필요.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 9–11  
  **note:** 성공률·대응 오버헤드 표 서술
- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf`  
  **pages:** 7–9  
  **note:** 실험 성공률·위조/복구 프레임

## Open questions

커뮤니티 최소 지표 세트(I85–I89)를 합의할 수 있는가?

## Next actions

1. REPORT 권고 지표표 채택
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
