# G09 — 결정성·hedged·시드 난수성

| 필드 | 값 |
|------|-----|
| id | `G09` |
| slug | `determinism-randomness` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | H79–H84 |
| status | `supported` |

## Claim (갭 후보)

seed_ybb 스킵으로 예측 가능 y를 유도하는 경로는 실증되었으나, hedged/deterministic 모드 전 조합·RNG 실패 모드·엔트로피 원 신뢰까지 닫힌 난수성 지도는 없다.

## Why it matters (테마 연결)

축 H. Fiat–Shamir with aborts + 시드 구조 핵심.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 2–3, 6–7, 10  
  **note:** expandYbb·시드 공격·루프 내 이동 대응

## Open questions

루프 내 재시드(J92) 후에도 다중 오류로 시드를 고정할 수 있는가?

## Next actions

1. H82×C28 교차 분석
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
