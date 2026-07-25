# G07 — 공격자 관측·오라클 가정

| 필드 | 값 |
|------|-----|
| id | `G07` |
| slug | `attacker-oracle` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | F61–F70 |
| status | `candidate` |

## Claim (갭 후보)

오류 서명 수집·공개키 지식·로컬 물리 접근·내부 트리거 가정이 암묵적인 경우가 많아, 원격/검증오라클-only 등 약한 관측 모델에서의 성립 여부가 분리되지 않는다.

## Why it matters (테마 연결)

축 F. 시스템 위협(K99)과 직결.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 5, 7  
  **note:** 공격 모델·실험 트리거 서술

## Open questions

Verify-oracle만으로 성립하는 HAETAE fault 공격이 있는가?

## Next actions

1. F63·F70을 공격 논문 표에 열로 추가
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
