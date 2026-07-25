# G17 — 시스템·OTA·배치 맥락

| 필드 | 값 |
|------|-----|
| id | `G17` |
| slug | `system-threat` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | K99, F70 |
| status | `candidate` |

## Claim (갭 후보)

로컬 물리 fault 결과가 펌웨어 서명·OTA·원격 위협 모델로 어떻게 승격되는지에 대한 시스템 수준 분석이 키워드 결합만으로는 비어 있다.

## Why it matters (테마 연결)

축 K99·F70. 운영 리스크 커뮤니케이션 갭.

## Evidence (base data)

- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[1] Over-the-Air Software Updates in the Internet of Things - An Overview of Key Principles.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE/[1] Over-the-Air Software Updates in the Internet of Things - An Overview of Key Principles.pdf`  
  **pages:** 1–3  
  **note:** OTA 맥락 참고

## Open questions

임베디드 서명 검증 경로에 HAETAE 채택 시 물리 접근 가정이 유효한가?

## Next actions

1. 위협 모델 템플릿에 F70·K99 필수화
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
