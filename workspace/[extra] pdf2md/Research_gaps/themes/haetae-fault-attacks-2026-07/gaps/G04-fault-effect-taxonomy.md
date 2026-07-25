# G04 — 오류 효과·대수 해석 유형

| 필드 | 값 |
|------|-----|
| id | `G04` |
| slug | `fault-effect-taxonomy` |
| theme | `haetae-fault-attacks-2026-07` |
| axes | C25–C28, C31–C32, D37–D40 |
| status | `candidate` |

## Claim (갭 후보)

스킵·랜덤 오류·차분 해석이 혼재 보고되나, HAETAE에 대한 permanent vs transient, zeroing vs bit-flip, DFA 방정식 vs lattice-hint 유형의 표준 택소노미 적용 표가 없다.

## Why it matters (테마 연결)

축 C·D 일부. 동일 ‘fault’ 키워드 아래 다른 수학적 위협이 섞인다.

## Evidence (base data)

- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`  
  **pages:** 3–5  
  **note:** 2.2 스킵·DFA 배경; III 공격 모델
- **MD:** `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[8] SoK - Parameterization of Fault Adversary Models Connecting Theory and Practice.md`  
  **PDF:** `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/[8] SoK - Parameterization of Fault Adversary Models Connecting Theory and Practice.pdf`  
  **pages:** 1, 5–12  
  **note:** adversary parameterization 일반론

## Open questions

HAETAE Sign에 zeroing-NTT류 공격(D32/D39 계열) 적용 가능 조건은?

## Next actions

1. SoK 파라미터를 HAETAE 공격 4종에 매핑
2. PDF 해당 페이지 재확인 후 status를 `supported` / `rejected`로 유지·갱신
3. `AXES-100.md` 해당 축을 covered/open으로 갱신
