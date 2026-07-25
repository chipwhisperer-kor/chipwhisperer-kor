# Synthesis — haetae-fault-attacks-2026-07

## 한 페이지

**키워드:** HAETAE + fault attacks  
**보완:** 100축 (`AXES-100.md`) → 20 갭 (`G01`–`G20`)

### 닫힌 클러스터
- Sign: LSB, UnpackA, sign-bit, sampling seed  
- challenge sampling abort (ML-DSA·HAETAE, PCM)  
- clock-glitch on Cortex-M4 + SW 폴트 시뮬  
- 대응 4종(서명 후 검증, 루프 내 이동, 부분 이중, 정상성 검사)의 **부분** 효과

### 열린 클러스터 (갭 질량)
- KeyGen / Verify 전 구간  
- 중간값 전 지도·다중 오류·permanent/zeroing 택소노미  
- EMFI·광학·마스킹·가속기  
- 전 보안 레벨·교차 보드 재현  
- 대응 스택 잔여면·우회 상한  
- 공유 coverage map · 시스템/OTA 승격  

### 다음 한 가지
`AXES-100`을 스프레드시트로 두고 앵커 2편부터 칸을 채운 뒤, open 밀도가 높은 **P1–P3 아젠다**만 실험·논문 가설로 승격한다.

상세: `REPORT.md`.
