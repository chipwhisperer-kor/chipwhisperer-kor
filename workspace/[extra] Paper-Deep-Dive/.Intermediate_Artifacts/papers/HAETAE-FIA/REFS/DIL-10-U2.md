# DIL-10-U2 — 공격1 심화: Skipping-fault Correction (Alg 4.1–4.3 · 대응)

단위: **DIL-10-U2**  
논문: [10] §4 *Skipping Fault Correction Attack* (pp.182–186)  
표준: FIPS 204 **Algorithm 7 L17–L20**, **Algorithm 8**, **Algorithm 29 SampleInBall**  
선행: **DIL-10-U1** approved  
상태: **approved** (2026-07-24 — [10] 전체 작업 승인) · producer `HO-20260724-07`

용어 정책 (D26): 전문 용어 *English italic*, 일상 설명 한글.

---

## 1. FI 대상 라인 (표준 · 구현)

| 층 | 위치 | 내용 |
|----|------|------|
| 상위 대수 | FIPS Alg 7 **L20** | $\mathbf{z}\leftarrow\mathbf{y}+\langle\langle c s_1\rangle\rangle$ |
| NTT 경로 | L17–18 | $\hat{c}\leftarrow\mathrm{NTT}(c)$; $\langle\langle c s_1\rangle\rangle\leftarrow\mathrm{NTT}^{-1}(\hat{c}\circ\hat{s}_1)$ |
| 논문 simplified | Alg 2.1 **L12** | $z:=y+cs_1$ (**공격 1 타겟** 주석) |
| 오류 모델 | 구현 | **한** 성분 $j$ · **한** 계수 $i$ 에서 덧셈 *skip* 또는 피연산자 *load* → 합 대신 **한 합mand만** 출력 |
| 오라클 | FIPS Alg 8 | 공개 *verify* 로 $\alpha$ 후보 판정 |

**출처:** [10] §4.1; U1 대응표.

전제 (U1 재확인):

- Case II: $(z')_j[i] = y_j[i]$ (rand에서 고전 차분 불가 → *Correction* 필요)
- Case I: $(z')_j[i]=(cs_1)_j[i]$ 이면 보정 없이 선형식 가능 (§2.2) — 본 단위는 **Case II + Correction** 중심

---

## 2. 정상 vs 오류 값

단일 계수 관점 (성분 $j$, 계수 $i$):

| | 정상 | 오류 (Case II skip) |
|--|------|---------------------|
| 정의 | $z_j[i]=y_j[i]+(cs_1)_j[i]$ | $z'_j[i]=y_j[i]$ |
| 서명 | $(\tilde{c},z,h)$ *verify* 통과 가능 | $(\tilde{c},z',h)$ **대개 거부** |

$(cs_1)_j[i]$ 분포 ([10] Fig.3, $2^{25}$ 샘플 시뮬):

- 0 근처 집중; 논문이 $N(0,80)$ (Dilithium2), $N(0,335)$ (3), $N(0,120)$ (5) PDF와 비교 플롯
- 탐색은 $|\alpha|$ 작은 순: $0,1,-1,2,-2,\ldots$

---

## 3. Correction 절차 → 선형식 (원문사실 · §4.1)

오류 서명 $\sigma'=(\tilde{c},z',h)$ 확보 후:

1. $z_{\mathrm{temp}}\leftarrow z'$  
2. 표적 계수만 $(z_{\mathrm{temp}})_j[i]\leftarrow (z')_j[i]+\alpha$  
3. $\mathrm{verify}(\tilde{c},z_{\mathrm{temp}},h)=\mathrm{accept}$ 이면 $\alpha^\star\leftarrow\alpha$ 채택  
4. $c\leftarrow\mathrm{SampleInBall}(\tilde{c})$  
5. 식: $\alpha^\star = \langle \mathrm{rotmult}(c,i),\,(s_1)_j\rangle$ 형태 (논문 표기) → $(s_1)_j$ 의 **선형식 1개**

**보정 상한** $0\le b\le\beta$: $|\alpha|$ 탐색을 $b$ 로 컷. 성공 *fault*면 $\alpha$ 가 0 근처 → 오래 걸릴수록 주입 실패 가능성↑ (§4.2).

### Algorithm 4.1 (논문 의사코드 요약 · 수정 없이 구조 수록)

```
Input: pk, O_skip (sign-with-fault oracle)
for j = 0 .. ℓ−1:
  S := {}
  target := (j, 0)          # 예: 계수 i=0 고정 가능
  while S not solvable:
    (c̃, z', h) := O_skip(M, target)
    for α = 0, 1, −1, 2, −2, … to bound b:
      z_temp := z';  (z_temp)_j[0] := z'_j[0] + α
      if verify(c̃, z_temp, h) = accept:
        c := SampleInBall(c̃)
        S.append( (rotmult(c,0), α) ); break
  (s1)_j := Solve(S)
return s1
```

**출처:** [10] Alg 4.1 p.184.

---

## 4. 복잡도 · fault 수 (원문사실 · §4.2)

| 항목 | 값 | 비고 |
|------|-----|------|
| 성분당 식 수 | $n=256$ | 테스트에서 선형종속 **관측 없음** (주장) |
| 최소 *faulty signatures* | $\ell\cdot n \in \{1024,1280,1792\}$ | Dilithium2/3/5 |
| 첫 시도만 *fault* 보정 | ÷ 0.23 / 0.19 / 0.26 | → 평균 주입 **~4500 / 6600 / 7000** (§3 확률) |
| 보정 탐색 | $2\beta<400$ | 복잡도 지배 항 아님 |
| 가역 확률 근사 | $\approx 1-1/q$ | [Wat87] 인용; $c$ 분포로 소폭 변동 가능 |

Abstract의 Dilithium2 **~1024** 는 **최소 성공 오류 서명 수**($\ell n$)에 해당. 실측 주입 횟수는 *rejection*·실패 주입에 따라 증가.

---

## 5. 알고리즘 전파 (FIPS 경로)

```
Alg7 L16  c ← SampleInBall(c̃)
     L17  ĉ ← NTT(c)
     L18  ⟨⟨c s1⟩⟩ ← NTT^{-1}(ĉ ∘ ŝ1)
     L20  z ← y + ⟨⟨c s1⟩⟩     ← 여기 한 계수 skip
     L23–28  범위·hint 검사 후 출력 가능
     L33  σ ← sigEncode(c̃, z, h)
```

*Correction* 은 장치 밖:

```
z'' ← z' with one coeff += α
Alg8 verify(pk, M', σ'')  → accept ⇒ α = (cs1)_j[i]
```

표준 의사코드에 *skip* 없음 — **구현 FI**. 대수 동치는 U1과 동일.

---

## 6. 대응 기법과 우회 (원문 · §4.3)

### 6.1 *Shuffling* → Alg 4.2

- 덧셈 순서 셔플 → 표적 $(j,i)$ 불명.
- 우회: 모든 $(j,i)$·$\alpha$ 에 대해 보정 시도. 첫 *accept* 가 위치+값.
- **비효과 *fault*** ($(cs_1)_j[i]=0$ skip) 는 위치 복구 불가 → **폐기**.
- 비용: 런타임 ×$\ell n$; *fault* 수 **+10–14%** (비효과 ~4.5%/2.2%/3.6% Dilithium2/3/5 + 표적 비선택).
- **출처:** Alg 4.2 p.185.

### 6.2 *Masking*

- 모든 *share* 의 동일 계수 덧셈을 skip 해야 함.
- 부분 skip → $z$ 사실상 난수 → 서명 루프에서 거부되기 쉬움 → 공격자 탐지 가능 여지.
- 셔플+마스킹 결합 시 주입 난이도↑ (정량 실험 수치 없음 — 서술).

### 6.3 *Double computation* / *sign-then-verify* → Alg 4.3 (*ineffective*)

- STV는 일반 *Correction* 을 **원천 차단** (오류 서명 미출력).
- 우회: $b=0$ — **비효과 *fault*만** 사용 ($(cs_1)=0$ skip → 서명이 정상처럼 통과).
- 수집: 해가 $0$ 인 식 → $\ker(S)$ 계산 후 $S_\eta$ 후보·위조 서명 시험으로 $s_1$ 스케일 확정 (Alg 4.3).
- 비용: 비효과 확률 ≤~5% (Dilithium2 Fig.3) → 기대 **>20 주입 / 비효과 1건**.
- **상호 배타:** 셔플 우회(Alg 4.2)와 비효과 우회(Alg 4.3)를 **동시에** 이 방식으로 결합 불가 (§4.3).
- 비효과 모드에서는 주입 실패 탐지 어려움.

### 6.4 CRT 무결성 [HP23]

- 확장 환 연산 + 사전 검사값 → skip 시 $q'$ 쪽도 깨짐 → 높은 확률로 폐기.
- 오버헤드 70% 보고는 **Kyber NTT** 초점 — Dilithium 수치 불일치 가능 (논문 명시).

### 6.5 *NTT-domain addition* ([RJH+19] 제안)

- $z=\mathrm{NTT}^{-1}(\hat{y}+\hat{c}\circ\hat{s}_1)$ 로 바꾸면 skip 오류가 서명 출력까지 전파되기 어려움.
- 단, 다른 FI([RYB+23] *twiddle* 계열)를 **열 수** 있음 — 논문 경고.

---

## 7. C 코드 · 실증

| 항목 | 내용 |
|------|------|
| 로컬 artifact | `tches-2024-a19.zip` **미실행** (계약). 라인 매핑 후속 가능 |
| skip 실증 선행 | [RJH+19] 실험 인용 (§4.2) |
| 본 논문 실증 | sim + ARM *clock glitch* (Abstract; 수치 표는 §6 쪽 — **U4**에서 정리) |
| pqm4 등 | workspace 소스 없음 — 상상 금지 |

---

## 8. 원문사실 / 저자주장 / 해석 / 불확실

| 구분 | 내용 |
|------|------|
| **원문사실** | Alg 4.1–4.3 구조; $\ell n$·첫시도 보정 수치; Fig.3 분포; 셔플 +10–14%; 비효과 ~4.5%(Dil2); STV 차단·비효과 우회; 셔플↔비효과 동시 우회 불가; CRT·NTT-add 서술 |
| **저자주장** | Case II+Correction 으로 rand에서도 skip 공격 가능; 다수 관용 대응을 합리적 비용으로 우회 가능(개별적으로) |
| **해석** | FIPS L20 한 계수 *skip* 모델은 표준 밖 구현 가정. *verify* 공개성 = 오라클 비용 ≈0. 키 복구는 **$s_1$ 부분** (U1과 동일) |
| **불확실** | (1) 실칩에서 계수 단위 skip 성공률 (2) 고차 마스킹+셔플 정량 (3) Alg 4.3 커널 위조 경로 성공률 재현 (4) HAETAE 수치 이식 금지 |

---

## 9. 비판적 점검

| 항목 | 판정 |
|------|------|
| $\ell n=1024$ vs Abstract 1024 | **일치** (최소 오류 서명). “주입 4500”은 **별 가정** — 슬라이드에 혼용 금지 |
| 선형종속 없음 | 실험적 주장; 이론 $1-1/q$ 로 뒷받침하나 $c$ sparse 영향은 “약간”만 언급 |
| STV 우회 | *ineffective* 로 전환 시 **Correction 개념 포기** — 비용·모델이 달라 “같은 공격”으로 묶으면 오해 |
| NTT addition 대응 | skip 차단 vs [11]/[RYB+23] 경로 개방 — **트레이드오프** (U1 [11]과 교차 참조 가능) |
| G2 | 수치는 §4·Fig.3·§3 확률만. §6 실측 표는 U4 |

---

## 10. 다음 단위

| ID | 내용 |
|----|------|
| **DIL-10-U3** | 공격2: *ExpandA*/$\Delta A$ · Eq.(1) $?$ · Alg 5.1–5.2 · 격자 가속 · ~512 |
| **DIL-10-U4** | 실증·대응 종합 · [9]/[11] 대비 |

---

## 11. 청중용 출처 문구 (producer)

> 출처: [10] §4 Skipping-fault Correction — Alg 4.1–4.3; FIPS 204 Alg 7 L20 · Alg 8.
