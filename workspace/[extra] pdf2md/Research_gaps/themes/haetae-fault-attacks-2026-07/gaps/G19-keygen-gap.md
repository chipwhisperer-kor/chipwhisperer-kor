# G19 — KeyGen 구간 전용 공백

| 필드 | 값 |
|------|-----|
| id | `G19` |
| slug | `keygen-gap` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | A01–A05 |
| status | `supported` |

## Claim (갭 후보)

KeyGen의 시드·비밀 샘플링·t 분해·리젝션에 대한 HAETAE fault 실증이 Sign 대비 현저히 적어, 장기 키 수명 관점의 위협이 과소평가될 수 있다.

## Why it matters (테마 연결)

축 A01–A05. 키 수명 vs 서명 수명.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 2–3, 5–6  
  **note:** 배경 알고리즘에 KeyGen 서술, 공격은 Sign 중심

## Open questions

KeyGen 1회 fault로 약한 키를 고정하는 경로가 있는가?

## Next actions

1. A02–A05 위협 모델링
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
