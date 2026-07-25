# G08 — 파라미터·스펙 세트 민감도

| 필드 | 값 |
|------|-----|
| id | `G08` |
| slug | `parameter-sets` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | G71–G78 |
| status | `candidate` |

## Claim (갭 후보)

보안 레벨·스펙 버전·모듈 파라미터별 공격 성공률·대응 오버헤드 비교가 체계적이지 않아, 한 레벨 결과가 전 레벨로 일반화될 위험이 있다.

## Why it matters (테마 연결)

축 G. 표준화·KpqC 맥락에서 필수.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[2] HAETAE - Shorter Lattice-Based Fiat-Shamir Signatures.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[2] HAETAE - Shorter Lattice-Based Fiat-Shamir Signatures.pdf`  
  **pages:** 1–5  
  **note:** HAETAE 설계·파라미터 배경
- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[1] Module-Lattice-Based Digital Signature Standard (FIPS 204).md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[1] Module-Lattice-Based Digital Signature Standard (FIPS 204).pdf`  
  **pages:** 1–10  
  **note:** ML-DSA 스펙 대조용

## Open questions

HAETAE-120 vs 상위 레벨에서 시드 공격 비용 차이는?

## Next actions

1. 실험 재현 시 레벨을 독립 변수로 고정
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
