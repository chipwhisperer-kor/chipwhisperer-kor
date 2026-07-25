# G11 — 대응 택소노미 공백

| 필드 | 값 |
|------|-----|
| id | `G11` |
| slug | `countermeasure-taxonomy` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | J91–J96 |
| status | `supported` |

## Claim (갭 후보)

알고리즘 수준(서명 후 검증·루프 내 이동)과 구현 수준(부분 이중·정상성 검사)이 제시되나, 전면 이중·마스킹 병행·프로세서 수준 대응까지 포함한 HAETAE 전용 대응 택소노미·커버리지 매트릭스가 없다.

## Why it matters (테마 연결)

축 J. 방어 설계의 체크리스트 공백.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 9–11  
  **note:** V장 대응 4종
- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[23] Countermeasures Against Fault Injection Attacks in Processors - A Review.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[23] Countermeasures Against Fault Injection Attacks in Processors - A Review.pdf`  
  **pages:** 1–5  
  **note:** 프로세서 수준 대응 일반론

## Open questions

4종 대응 조합(I90)의 잔여 공격면은?

## Next actions

1. 공격×대응 매트릭스 작성(G12)
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
