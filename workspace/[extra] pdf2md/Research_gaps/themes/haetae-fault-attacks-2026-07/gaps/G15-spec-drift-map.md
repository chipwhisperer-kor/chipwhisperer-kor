# G15 — 스펙 드리프트·커버리지 맵 표준

| 필드 | 값 |
|------|-----|
| id | `G15` |
| slug | `spec-drift-map` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | G72–G73, K100 |
| status | `candidate` |

## Claim (갭 후보)

HAETAE 버전·ML-DSA(FIPS 204)와의 구조 차이·커뮤니티 공유 coverage map이 없어, 키워드 검색만으로 최신 위협 우선순위를 고정할 수 없다.

## Why it matters (테마 연결)

축 G·K100. 연구 아젠다 공백.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[1] Module-Lattice-Based Digital Signature Standard (FIPS 204).md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[1] Module-Lattice-Based Digital Signature Standard (FIPS 204).pdf`  
  **pages:** 1–5  
  **note:** 표준 스펙 존재

## Open questions

AXES-100을 공개 coverage map 스키마로 쓸 수 있는가?

## Next actions

1. K100 산출물로 AXES-100 유지
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
