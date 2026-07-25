# G06 — 주입 수단·구현 플랫폼

| 필드 | 값 |
|------|-----|
| id | `G06` |
| slug | `injection-platform` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | E49–E60 |
| status | `supported` |

## Claim (갭 후보)

보고된 실증은 주로 클럭 글리치 + Cortex-M4/ChipWhisperer·SW 시뮬에 집중되어 EMFI·레이저·가속기·마스킹 구현 등 E축 대부분이 open이다.

## Why it matters (테마 연결)

축 E. 플랫폼 일반화 없이는 ‘HAETAE fault’ 주장의 외적 타당성이 제한된다.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 7–8  
  **note:** CW308·Husky·클럭 글리치·공식 구현 v3.0
- **MD:** `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md`  
  **PDF:** `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf`  
  **pages:** 7–8  
  **note:** 실험 환경·성공률 표 서술

## Open questions

동일 공격이 다른 MCU/최적화 레벨에서 재현되는가? (K97–K98)

## Next actions

1. E58–E59 체크리스트를 실험 섹션에 강제
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
