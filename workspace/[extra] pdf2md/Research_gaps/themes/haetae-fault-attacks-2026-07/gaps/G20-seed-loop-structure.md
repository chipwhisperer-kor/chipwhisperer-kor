# G20 — 시드·리젝션 루프 구조 공백

| 필드 | 값 |
|------|-----|
| id | `G20` |
| slug | `seed-loop-structure` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | C35, H81–H82, J92 |
| status | `supported` |

## Claim (갭 후보)

시드가 리젝션 루프 밖에서 한 번 생성되는 구조가 시드 공격의 핵심이나, 루프 내 이동 대응 이후에도 남는 구조적 변형(다중 오류·다른 시드 경로) 분석이 완전하지 않다.

## Why it matters (테마 연결)

축 C35·H·J92. HAETAE 특화 구조 갭.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 6–7, 10  
  **note:** 시드 공격·루프 내 이동 대응

## Open questions

루프 내 이동 후에도 부호 비트·LSB 공격면은 그대로인가? (문서상 시드 외 잔여)

## Next actions

1. 구조 다이어그램을 텍스트 단계도로 고정
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
