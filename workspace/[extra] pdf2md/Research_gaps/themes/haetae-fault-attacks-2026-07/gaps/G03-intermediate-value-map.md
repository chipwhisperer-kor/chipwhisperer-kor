# G03 — 중간값·시드 공격 지도

| 필드 | 값 |
|------|-----|
| id | `G03` |
| slug | `intermediate-value-map` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | B13–B24 |
| status | `supported` |

## Claim (갭 후보)

중간값 중 seed_ybb·b·A 언패킹·LSB 등은 실증되었으나, t 분해·힌트/압축 필드·리젝션 카운터 등 B축 전 항목에 대한 체계적 지도는 없다.

## Why it matters (테마 연결)

축 B. 구현 방어는 ‘어느 버퍼를 보호할지’가 비면 공백이 된다.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 5–8  
  **note:** 3.2.1–3.2.4 중간값 타깃 서술

## Open questions

B22 압축 필드 fault가 HAETAE 구현에 실재하는가?

## Next actions

1. B축 체크리스트를 대상 2편+참고에 표기
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
