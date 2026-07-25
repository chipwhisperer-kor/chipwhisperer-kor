# Research Gap Report — HAETAE × fault attacks

| 항목 | 값 |
|------|-----|
| theme_id | `haetae-fault-attacks-2026-07` |
| date | 2026-07-26 |
| keywords | HAETAE, fault attacks |
| method | 키워드 2개 + **구체화 축 100** (`AXES-100.md`) → 갭 묶음 20 (`gaps/G01`–`G20`) |
| base | `Papers_md/` text-only **verified** (61편 중 테마 범위 MD) |
| status | `review` |

---

## 1. Executive summary

키워드 **「HAETAE」** 와 **「fault attacks」** 만으로는 (i) 어느 파이프라인 단계, (ii) 어떤 중간값, (iii) 어떤 오류·관측 모델, (iv) 어떤 대응이 닫혔는지가 결정되지 않는다.  
본 테마는 구체성 확보를 위해 **보완 요소 100개**를 정의하고, 패키지 내 골든셋 2편과 관련 참고 MD를 축에 투영하여 **열린 공백(갭)** 을 보고한다.

**한 줄 결론:** Sign 중심의 소수 지점 공격·부분 대응은 **supported** 수준으로 문헌에 존재하나, **KeyGen/Verify 전 구간, 교차 플랫폼 재현, 파라미터 전 레벨, 대응 스택 잔여면, 공유 coverage map** 은 체계적으로 비어 있다.

---

## 2. 왜 100개 보완 요소가 필요한가

| 문제 | 키워드만 쓸 때 | 100축 적용 후 |
|------|----------------|---------------|
| 범위 폭발 | 모든 격자 서명 fault로 확산 | A–K 축으로 범위 고정 |
| 비교 불능 | 논문마다 ‘성공’ 정의 상이 | I85–I90 지표 강제 |
| 대응 착시 | ‘대응 제안’ = 해결로 오인 | J91–J96 × 공격 매트릭스 |
| 이전 오류 | Dilithium 결과 무비판 이전 | G16 이전 조건 명시 |
| 재현 공백 | 장비 한 조합 결과 일반화 | E·K 재현 체크리스트 |

축 전문: [`AXES-100.md`](AXES-100.md).  
묶음 매핑: 동 문서 하단 표 → `gaps/G01`–`G20`.

---

## 3. 베이스 문헌 (1차 앵커)

| 역할 | MD | PDF (인용) |
|------|-----|------------|
| HAETAE FI + 대응 | `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md` | 동명 `.pdf` |
| challenge/public coeff. | `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md` | 동명 `.pdf` |
| 스펙·설계·SoK·Dilithium FI 등 | 각 1-deep 참고 MD | 대응 `Papers_pdf/...` |

최종 근거는 항상 **source PDF 페이지**. MD는 검색·구조화 입력. 그림 픽셀은 사용하지 않음(캡션·페이지 표기만).

### 3.1 앵커 논문이 닫는 것 (요약)

**HAETAE FI 논문 (국내 저널 골든셋)**  
- Sign: LSB, UnpackA, sign-bit b, sampling seed (`seed_ybb`)  
- 실험: SW 시뮬 + Cortex-M4 클럭 글리치  
- 대응: 서명 후 검증, 리젝션 루프 내 이동, 부분 이중, 정상성 검사  

**PCM (Public Coefficient Matters)**  
- ML-DSA·HAETAE challenge 샘플링 루프 abort  
- 공개 계수/파라미터와 결합한 키 복구·위조 프레임  
- 실험 성공률 보고, 대응 논의  

### 3.2 앵커가 비우는 것 (요약)

- KeyGen 전 구간 (A01–A05)  
- Verify 전용 공격 (A11–A12, G18)  
- EMFI/레이저/마스킹/가속기 (E51–E56)  
- 전 파라미터 레벨 민감도 (G71–G76)  
- 대응 조합 최적화·강공격 우회 (G12–G13)  
- 공유 coverage map (K100)  

---

## 4. 100축 커버리지 스냅샷 (테마 베이스 기준)

기호: ● covered(부분 이상 서술) · ◐ partial · ○ open · – n/a

| 영역 | 축 수 | 앵커 문헌 경향 | 대표 open |
|------|------:|---------------|-----------|
| A 파이프라인 | 12 | Sign ● / KeyGen·Verify ○ | A01–A05, A11–A12 |
| B 중간값 | 12 | seed,b,A,LSB ● / 압축·카운터 ○ | B22–B24 |
| C 오류 모델 | 12 | skip·glitch ● / multi·permanent ○ | C26, C28, C30 |
| D 해석 | 12 | 키복구·일부 DFA ● / lattice-hint 전이 ○ | D38–D39 |
| E 플랫폼 | 12 | clock+M4 ● / 기타 ○ | E51–E57 |
| F 관측 | 10 | 로컬·오류서명 ● / oracle-only ○ | F63, F70 |
| G 파라미터 | 8 | 단레벨 실험 ● | G71–G76 |
| H 난수 | 6 | seed 경로 ● | H79, H84 |
| I 지표 | 6 | 표 일부 ● / 표준 ○ | I85–I87 통합 |
| J 대응 | 6 | 4종 ● / 스택·우회 ○ | J95–J96, I90 |
| K 재현·시스템 | 4 | 단일 셋업 ● | K97–K100 |

**해석:** 키워드 매칭으로 “HAETAE fault 연구 있음”은 참이지만, 100축 기준으로는 **Sign 로컬 물리 스킵 클러스터**에 질량이 몰려 있고 나머지 축 다수는 open이다. 이것이 본 보고서의 갭 정의이다.

---

## 5. 갭 후보 요약 (G01–G20)

| ID | 제목 | 축 | status | 한 줄 |
|----|------|-----|--------|------|
| G01 | 파이프라인 커버리지 | A01–A12 | supported | Sign 편중, KeyGen/Verify 지도 부재 |
| G02 | challenge·공개계수 | A09,B21,D41 | supported | PCM이 열었으나 전 경우 분류 미완 |
| G03 | 중간값 지도 | B13–B24 | supported | 4지점 외 B축 open |
| G04 | 효과 택소노미 | C,D 일부 | candidate | SoK 파라미터 미적용 |
| G05 | 스킵·예산·윈도우 | C29–C36 | supported | 기대 시도 수 표준 없음 |
| G06 | 주입·플랫폼 | E49–E60 | supported | clock-M4 편중 |
| G07 | 관측·오라클 | F61–F70 | candidate | 가정 암묵적 |
| G08 | 파라미터 세트 | G71–G78 | candidate | 레벨 일반화 위험 |
| G09 | 결정성·난수 | H79–H84 | supported | 시드 경로 외 미완 |
| G10 | 복구 지표 | I,D 일부 | candidate | 성공 정의 불통일 |
| G11 | 대응 택소노미 | J91–J96 | supported | 4종 너머 맵 없음 |
| G12 | 잔여 공격면 | J+I | supported | 조합 미최적화 |
| G13 | 대응 우회 | J95–96,C28 | candidate | 다중 오류 상한 미정량 |
| G14 | 재현·캘리브 | E,K | candidate | 교차 재현 프로토콜 없음 |
| G15 | 스펙·맵 표준 | G72–73,K100 | candidate | coverage map 부재 |
| G16 | 교차 스킴 이전 | D39,G73 | supported | 이전 조건 미정리 |
| G17 | 시스템·OTA | K99,F70 | candidate | 물리→시스템 승격 공백 |
| G18 | Verify 공백 | A11–12 | supported | Verify 전용 실증 부족 |
| G19 | KeyGen 공백 | A01–05 | supported | 키 수명 위협 과소 가능 |
| G20 | 시드·루프 구조 | C35,H,J92 | supported | 구조 잔여 변형 미완 |

상세 claim·evidence·open questions: `gaps/` 각 파일.

---

## 6. 연구 질문 답변 초안

### Q-T1. 닫힌 면 vs 열린 면

| 닫힌( baselined ) | 열린( gap ) |
|-------------------|-------------|
| Sign LSB / UnpackA / b / seed_ybb | KeyGen 전 구간 |
| challenge abort (PCM) | Verify 전 구간 |
| clock glitch on M4 + SW 시뮬 | EMFI·광학·가속기·마스킹 |
| 대응 4종 각각의 부분 효과 | 대응 스택 잔여면·우회 |
| 단일 셋업 성공률 표 | 전 레벨·교차 보드 지도 |

### Q-T2. Dilithium/ML-DSA → HAETAE 이전

- **가능 후보:** FS-with-aborts, 모듈 격자, challenge/nonce 계열 아이디어 (PCM이 양 스킴 동시 다룸).  
- **제약:** 하이퍼볼/bimodal 샘플, 시드 구조, 압축·부호 비트, 파라미터 세트 (G16).  
- **갭:** 이전 가능/불가 정리 표와 MLWE→RLWE류의 HAETAE 성립 조건 (D39).

### Q-T3. 대응 커버리지

| 대응 | 주로 막는 것 | 남는 것 (문헌 서술 경향) |
|------|--------------|---------------------------|
| 서명 후 검증 | c 교란형 (LSB·Unpack) | 시드·부호비트 등 다른 면 |
| 루프 내 이동 | 단일 시드 고정 | 타 공격·다중 오류 |
| 부분 이중 | 시드·부호비트 경로 일부 | LSB/Unpack·다중 오류 |
| 정상성 검사 | 전0/단일패턴 시드 | 다른 패턴·다른 지점 |

→ **최소 비용으로 4공격면을 동시에 닫는 조합**이 최적화되지 않음 (G12).

### Q-T4. 운영 가능 평가를 가로막는 것

- 지표 비표준 (G10)  
- 재현 프로토콜 부재 (G14)  
- 시스템 위협 모델 단절 (G17)  
- coverage map 부재 (G15, K100)

---

## 7. 우선 연구 아젠다 (권고)

| 순위 | 아젠다 | 관련 갭 | 100축 |
|------|--------|---------|-------|
| P1 | HAETAE **coverage map v1** 공개 (A–J 체크리스트) | G01,G15 | 전 축 |
| P2 | **KeyGen + Verify** 전용 fault 실증 | G18,G19 | A01–A05, A11–A12 |
| P3 | 공격×대응 **잔여면 매트릭스** + 스택 최적화 | G11,G12 | J,I |
| P4 | **교차 구현/보드** 재현 프로토콜 | G06,G14 | E,K |
| P5 | ML-DSA 결과 **이전 조건 정리** | G16 | D39,G73 |
| P6 | 지표 표준 (성공·시도·오버헤드) | G05,G10 | I85–I89 |
| P7 | 다중 오류·대응 우회 상한 | G13 | C28,J93 |
| P8 | 시스템/OTA 위협 승격 시나리오 | G17 | K99,F70 |

---

## 8. Limitations

- 근거는 패키지 내 verified MD·특히 골든셋 2편에 **가중**. 전 세계 문헌 전수는 범위 밖.  
- `supported` = 베이스 안에서 공백 서술이 뒷받침됨. 외부 미발표 연구 존재 가능성을 배제하지 않음.  
- 그림 픽셀 없이 캡션·본문·표 텍스트·PDF 페이지에 의존. 곡선 수치 등은 PDF 재확인 필요.  
- 100축은 **연구 설계 체크리스트**이며 자동 완성된 실험 결과가 아님.

---

## 9. Deliverable index

| 경로 | 설명 |
|------|------|
| `META.md` | 의도·상태 |
| `SCOPE.md` | 포함·제외·질문 |
| `AXES-100.md` | **구체화 보완 요소 100** |
| `gaps/G01-*.md` … `G20-*.md` | 축 묶음별 갭 후보 |
| `synthesis.md` | 한 페이지 요약 |
| `REPORT.md` | 본 보고서 |
| `Research_gaps/INDEX.md` | 테마 등록 |

---

## 10. Closing

HAETAE fault 연구는 **‘있다’** 와 **‘운영 가능한 위협 지도가 닫혀 있다’** 가 다르다.  
본 테마는 후자를 위해 키워드 2개에 **100개 구체화 축**을 덧붙였고, 그 위에서 **20개 갭 후보**와 **8개 우선 아젠다**를 제시한다.  
후속 작업은 새 실험을 나열하기보다, `AXES-100` 각 칸을 `covered/open`으로 채우며 PDF 페이지 근거를 붙이는 것이다.
