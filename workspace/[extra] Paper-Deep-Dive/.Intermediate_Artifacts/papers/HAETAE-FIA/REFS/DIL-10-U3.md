# DIL-10-U3 — 공격2: ExpandA / 공개 행렬 $A$ fault · Correction

단위: **DIL-10-U3**  
논문: [10] §5 *Correction Attack with a Fault in A* (pp.187–192)  
표준: FIPS 204 **Algorithm 7 L5**, **Algorithm 8 L5·L9–L13**, **Algorithm 32 ExpandA**  
선행: DIL-10-U1–U2 approved  
상태: **approved** (2026-07-24 — [10] 전체 작업 승인) · producer `HO-20260724-08`

용어 정책 (D26): 전문 용어 *English italic*, 일상 설명 한글.

---

## 1. FI 대상 (원문사실 · §5 Fault Model)

| 층 | 위치 | 내용 |
|----|------|------|
| 논문 | Alg 2.1 **L1** | $A:=\mathrm{ExpandA}(\rho)$ — §5 타겟 주석 |
| FIPS | Alg 7 **L5** · Alg 32 | $\hat{\mathbf{A}}\leftarrow\mathrm{ExpandA}(\rho)$ — *NTT* 영역 행렬 |
| 검증측 | Alg 8 **L5** | 동일 *ExpandA* — **정상** $A$ (공개 $\rho$) |

**오류 모델:**

- $\hat{A}'=\hat{A}+\Delta\hat{A}$
- $\Delta\hat{A}$ 는 **정확히 한** 행렬 성분·한 계수만 비영: $(\Delta\hat{A})_{j_1,j_2}[i]\neq 0$
- 공격자는 표적 위치를 알고, 주입 차분 $\delta=(\Delta\hat{A})_{j_1,j_2}[i]$ 를 **알아야** 함 (값 선택 권한은 불필요)
- 실현 예: 비트 플립/세트/리셋 · 계수 *zeroing* · *load/store* 교란 · *ExpandA* 내 SHAKE 마지막 라운드·거절 샘플 · $Ay$ 곱 · 메모리 상 $A$

**공개성 의의:** $A$ 확장은 비밀을 직접 다루지 않음 → 부채널 대응이 약할 수 있음 (§1·§5).

**루프 위치:** 많은 구현이 *rejection loop* **밖**에서 $A$ 1회 생성 → 공격1과 달리 “최종 반복 *fault*” 스케일(÷0.23) **불필요** (§5.3).

---

## 2. 검증식에서 Correction 항 $?$ (원문 · §5.1 Eq.(1))

서명측은 $A'$ 사용 → 오류 서명 $\sigma'=(\tilde{c}',z',h')$.  
검증측은 공개 $\rho$ 로 **정상** $A$ 재생성.

목표: *HighBits* 재구성이 서명 시 $w_1'$ 와 맞게 하여 $\tilde{c}'$ 해시 검사 통과.

논문 핵심 항 (개념):

$$
\mathrm{HighBits}_q\big(\underbrace{A z' - c' t}_{\text{검증자 계산}} + \underbrace{?}_{\approx\,\mathrm{NTT}^{-1}(\Delta\hat{A}\circ\hat{y})}\big) \;=\; w_1'
$$

단일 비영 $\Delta\hat{A}$ 이면 $?$ 는 **한** $\hat{y}_{j_2}[i]$ 계수에만 의존 → $\alpha\in\{0,\ldots,q-1\}$ 전수 탐색.

참 $\alpha=\hat{y}_{j_2}[i]$ 이면 *verify* 성공. 이어서 (NTT 선형성):

$$
(\hat{s}_1)_{j_2}[i]
=\big(\hat{z}'_{j_2}[i]-\hat{y}_{j_2}[i]\big)\cdot(\hat{c}'[i])^{-1}
\pmod q
$$

전 계수 반복 후 $\mathrm{NTT}^{-1}$ → $s_1$.

### $t$ vs $t_1$ (키 압축)

- 공개키는 $t_1$ 만. $t_0$ 는 소량 서명으로 복원 가능([NIS23] 인용)이나,
- **$t_1$ 만으로도** 공격 성립: $Az'-c't_1\cdot 2^d$ 에 $\Delta A y$ 보정을 더하면, 참 $y$ 에서 *UseHint* 입력이 서명 시 hint 생성과 일치 (§5.1).

### Algorithm 5.1–5.2 (구조 요약)

- **5.1 verify'**: 정상 *ExpandA* + $\Delta\hat{A}$ 한 칸 $\delta$ + 시험 $\hat{y}$ 한 칸 $\alpha$ → $X=\mathrm{NTT}^{-1}(\Delta\hat{A}\circ\hat{y})$ → *UseHint* 후 $\tilde{c}$ 일치 검사  
- **5.2**: 각 $(j_2,i)$ 에 *fault oracle* → $\alpha=0..q-1$ 탐색 → $\hat{s}_1$ 채움 → $\mathrm{NTT}^{-1}$

**출처:** [10] Alg 5.1–5.2 pp.189–190.

---

## 3. 격자 가속 (§5.2) — fault 수 절반

- 계수 전수 *fault* 없이 $\hat{s}_1$ 의 **절반**만 알면 $s_1$ 소계수 성질로 LWE/격자 문제로 나머지 복구 (Kyber [HHP+21] 유사).
- primal embedding $t=1$; BKZ block 30 (fplll).
- 결과 주장: fault 수 $\{1024,1280,1792\}\to\{512,640,892\}$ (Dil2/3/5).
- 노트북 i5 1.6 GHz: 다항식 1개 복구 평균 **~90 min** (절반 계수 기지). 40회 실험 **전부 성공**.
- 추가 최적화 여지 있음 (논문).

→ Abstract Dilithium2 **~512** 는 이 **격자 가속 후** 규모.

---

## 4. 복잡도·실용성 (§5.3)

| 항목 | 내용 |
|------|------|
| 계수당 탐색 | $|\mathbb{Z}_q|=q$ ≫ $2\beta$ (공격1보다 오프라인 비쌈) |
| 전계수 | $\ell n$ *fault* (격자 없으면) |
| 격자 | ~$\ell n/2$ |
| 주입 위치 | 최대 $\ell n$ 개 **서로 다른** 시점/위치 (공격1은 성분당 $\ell$ 수준) |
| 오탐 | 잘못된 $\hat{y}$ → 전 계수 교란 + *UseHint* 허용 범위 좁음 → 오탐 확률 무시 가능 (App.A lemma 인용) |
| 주입 실패 | 전수 실패·다중 계수 오염 시 보정 실패로 폐기 가능. $\Delta$ 불명이면 오복구 → 다중 시행·일치 확인 필요 (실측 §6.3) |

---

## 5. 대응 (§5.4)

| 대응 | 논문 요지 |
|------|-----------|
| *ExpandA* 비용 | 서명 사이클 큰 비중; RAM 제약 시 루프마다 재생성 → 최대 ~6× 저속 인용 [GKS21] → 대응은 **저비용**이어야 함 |
| *Shuffling* (행) | $w_1$ 의 $k$ 행 보정 시험 → 런타임 ×$k$ |
| *Shuffling* (행+열) | 후보 $\hat{y}/\hat{s}_1$ 다수 저장 후 동일 값 2회 → birthday ~$2^{-15}$ 오인; fault ×**14/19/29** (Dil2/3/5 sim) |
| 이중계산 / STV | 단일 *fault* 모델에서 *Correction* 차단. 비효과 *fault* 확률 $1/q\approx 2^{-23}$ → 비실용 |
| CRT [HP23] | *sampling* 단계 대부분 비보호; **저장/재로드 $A$** 오류는 탐지 가능 |

---

## 6. FIPS 이식 메모

| 논문 | FIPS | 판정 |
|------|------|------|
| ExpandA 의사코드 Alg 6.1 (실측부) | Alg 32 + *RejNTTPoly* | 역할 동일; 바이트/거절 세부 구현 |
| $Az-ct_1 2^d$ | Alg 8 L9 | 대응 |
| $\tilde{c}$ vs $c$ | SampleInBall 리맵 | U1과 동일 마이너 |

---

## 7. 원문사실 / 저자주장 / 해석 / 불확실

| 구분 | 내용 |
|------|------|
| **원문사실** | 단일 계수 $\Delta A$; $?$ 탐색; $t_1$ 만으로 성립; 격자 절반·512; 셔플 배수 14/19/29; 오탐 무시 주장 |
| **저자주장** | 공개 연산도 FI 타겟; 부채널 보호 공백이 fault 노출로 이어질 수 있음 |
| **해석** | 공격1=비밀 경로 L20 · 공격2=공개 경로 L5 — **직교**. 오프라인 $q$-탐색 대 온라인 위치 다양성 트레이드오프 |
| **불확실** | (1) 임의 $\delta$ vs zeroing만 실측 (2) 격자 최소 *fault* 미최적화 (3) HAETAE 수치 이식 금지 |

---

## 8. 청중용 출처

> 출처: [10] §5 Fault in $A$ — Eq.(1), Alg 5.1–5.2; FIPS 204 Alg 7 L5 · Alg 8 · Alg 32.
