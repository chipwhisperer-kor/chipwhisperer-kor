# G14 — 재현·캘리브레이션·구현 변이

| 필드 | 값 |
|------|-----|
| id | `G14` |
| slug | `repro-calibration` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | E54–E59, K97–K98 |
| status | `candidate` |

## Claim (갭 후보)

글리치 탐색 결과는 보고되나 교차 구현·교차 보드·컴파일러 최적화에 대한 재현 프로토콜이 표준화되어 있지 않다.

## Why it matters (테마 연결)

축 E·K. 과학적 재현성 갭.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 7–9  
  **note:** 탐색 절차·어셈블리 구간 서술
- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[34] Fast Calibration of Fault Injection Equipment with Hyperparameter Optimization Techniques.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[34] Fast Calibration of Fault Injection Equipment with Hyperparameter Optimization Techniques.pdf`  
  **pages:** 1–3  
  **note:** 장비 캘리브레이션 일반

## Open questions

공개 재현 패키지(트리거·파라미터 범위)가 존재하는가?

## Next actions

1. 최소 재현 체크리스트 초안
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
