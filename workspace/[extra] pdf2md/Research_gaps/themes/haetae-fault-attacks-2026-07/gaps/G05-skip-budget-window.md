# G05 — 스킵·글리치 예산·타이밍 윈도우

| 필드 | 값 |
|------|-----|
| id | `G05` |
| slug | `skip-budget-window` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | C29–C30, C33–C36 |
| status | `supported` |

## Claim (갭 후보)

클럭 글리치 파라미터 탐색·공격별 성공 분포는 보고되나, 평균 서명 예산·다중 오류·삽입/재실행 모델까지 포함한 예산 표준은 없다.

## Why it matters (테마 연결)

축 C 후반. 현실 위협 비교에 필수.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 7–9  
  **note:** IV 글리치 탐색·Fig.6·Table 1–2 계열 결과 서술

## Open questions

공격 유형별 기대 글리치 수(I86)를 단일 표로 통합할 수 있는가?

## Next actions

1. Table 계열 PDF 페이지 재확인·I85–I87 정의 고정
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
