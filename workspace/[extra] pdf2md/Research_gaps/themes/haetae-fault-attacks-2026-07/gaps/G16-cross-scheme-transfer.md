# G16 — 교차 스킴 이전 가능성

| 필드 | 값 |
|------|-----|
| id | `G16` |
| slug | `cross-scheme-transfer` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | D39, G73, K97 |
| status | `supported` |

## Claim (갭 후보)

Dilithium/ML-DSA fault 결과의 HAETAE 이전은 구조 유사성(FS with aborts, 모듈 격자)에 의존하나, 하이퍼볼 샘플링·압축·시드 구조 차이로 이전 조건이 명시된 정리가 부족하다.

## Why it matters (테마 연결)

축 이전성. ‘격자 서명 fault’ 일반화의 오류 가능.

## Evidence (base data)

- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf`  
  **pages:** 1–2, 5–7  
  **note:** ML-DSA와 HAETAE 동시 공격 프레임
- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[9] From MLWE to RLWE A Differential Fault Attack on Randomized and Deterministic Dilithium.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[9] From MLWE to RLWE A Differential Fault Attack on Randomized and Deterministic Dilithium.pdf`  
  **pages:** 1–3  
  **note:** Dilithium MLWE→RLWE fault

## Open questions

MLWE→RLWE 계열 공격이 HAETAE 파라미터에서 성립하는가?

## Next actions

1. 구조 차이 표 + 이전 가능/불가 열
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
