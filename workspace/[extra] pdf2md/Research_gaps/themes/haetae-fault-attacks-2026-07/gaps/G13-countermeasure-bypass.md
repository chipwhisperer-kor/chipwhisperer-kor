# G13 — 강공격·대응 우회

| 필드 | 값 |
|------|-----|
| id | `G13` |
| slug | `countermeasure-bypass` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | J95–J96, E55, C28 |
| status | `candidate` |

## Claim (갭 후보)

다중 오류·마스킹 구현·전면 이중 우회에 대한 HAETAE 특화 분석이 부족하며, 제시 대응의 위협 모델 상한을 넘는 공격자에서의 잔존 위험이 정량화되지 않았다.

## Why it matters (테마 연결)

축 J 후반·C28. 보안 주장의 상한.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 10–11  
  **note:** 부분 이중이 다중 오류에 취약할 수 있음 언급류 서술

## Open questions

이중 경로 동시 글리치가 현실적 예산 안에 있는가?

## Next actions

1. C28×J93 교차 실험 설계
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
