# G01 — 서명 파이프라인 단계별 fault 커버리지

| 필드 | 값 |
|------|-----|
| id | `G01` |
| slug | `pipeline-stage-coverage` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | A01–A12 |
| status | `supported` |

## Claim (갭 후보)

HAETAE fault 실증은 Sign 내 특정 지점(LSB·UnpackA·sign-bit·sampling seed·challenge abort)에 편중되어 있으며, KeyGen 전체·Verify 전 구간에 대한 닫힌 커버리지 지도가 표준화되어 있지 않다.

## Why it matters (테마 연결)

축 A 전체. 키워드만으로는 어디를 공격·방어해야 하는지 운영 범위가 비어 1차 갭 축이 된다.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 1–2, 5–8  
  **note:** III장 4종 Sign 중심 공격(LSB·언패킹·부호비트·시드)
- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf`  
  **pages:** 1, 5–7  
  **note:** challenge sampling 루프 abort 중심; KeyGen/Verify 본 공격 범위 밖

## Open questions

KeyGen 재샘플·Verify 재계산 경로에 대한 HAETAE 전용 fault 실증 문헌이 존재하는가?

## Next actions

1. 참고 MD에서 KeyGen/Verify 키워드 스캔; PDF 페이지 재확인 후 맵 초안
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
