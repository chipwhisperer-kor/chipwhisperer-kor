# SCOPE — HAETAE × fault attacks (구체화 테마)

## 포함

1. 대상 골든셋 MD  
   - `Papers_md/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.md`  
   - `Papers_md/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.md`
2. 위 두 논문 1-deep 참고 중 **격자 서명 fault / HAETAE·ML-DSA 스펙 / 주입·대응 일반론**에 해당하는 MD  
   (예: FIPS 204, HAETAE 설계, Dilithium fault, SoK adversary, 대응 서베이)
3. `AXES-100.md`의 100개 구체화 축에 매핑되는 주장·실험·대응 서술

## 제외

- HAETAE와 무관한 순수 AES/RSA/ECC DFA 본론 (인용 맥락만)
- 부채널(SCA) only · fault 비포함
- 이미지/그래프 픽셀 재해석, 신규 물리 실험
- 갭 엔진 자동화

## 연구 질문 (테마 수준)

- **Q-T1.** HAETAE fault 문헌이 **닫은 공격면**과 **열린 공격면**은 무엇인가? (축 A–F)
- **Q-T2.** Dilithium/ML-DSA fault 결과를 HAETAE로 **이전 가능한 조건**은? (축 G, K, 이전성)
- **Q-T3.** 제안 대응이 **어느 축**을 커버하고 어디를 비우는가? (축 J)
- **Q-T4.** 실험·재현·시스템 맥락에서 **운영 가능한 위험 평가**를 가로막는 공백은? (축 I, K)

## 증거 규칙

- 각 갭: `Papers_md/...` 경로 + **`Papers_pdf/...` 페이지**
- MD 줄만으로 확정하지 않음. 최종 인용 = source PDF 페이지
- 그림은 캡션·교차참조·페이지 표기만 사용 (픽셀 없음)

## 구체화 방법

키워드 2개만으로는 검색·가설 공간이 과대하므로, `AXES-100.md`의 **100개 보완 요소**를 체크리스트로 쓴다.  
갭 후보(`gaps/Gnn`)는 축 묶음에 대한 **닫힘/열림** 주장을 담는다.
