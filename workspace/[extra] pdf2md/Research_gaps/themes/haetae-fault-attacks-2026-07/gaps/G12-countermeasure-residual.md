# G12 — 대응 비용·잔여 공격면

| 필드 | 값 |
|------|-----|
| id | `G12` |
| slug | `countermeasure-residual` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | J91–J94, I88–I90 |
| status | `supported` |

## Claim (갭 후보)

각 대응은 특정 공격(예: 시드 vs LSB/언패킹)만 막거나 성능 트레이드오프를 남기며, 전 공격면을 닫는 최소 비용 조합이 최적화되어 있지 않다.

## Why it matters (테마 연결)

축 J+I. ‘대응 있음’ ≠ ‘갭 없음’.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 10–11  
  **note:** Table 3–6 계열 오버헤드·대응 범위 서술

## Open questions

Sign-then-Verify + 부분이중 + 정상성검사 스택의 잔여면은?

## Next actions

1. 매트릭스: 행=공격4, 열=대응4
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
