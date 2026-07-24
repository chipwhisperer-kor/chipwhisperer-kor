# DIL-10-U1 — Correction 개념 · FIPS Sign/Verify 대응 · 공격 1 진입점

단위: **DIL-10-U1**  
논문: [10] Krahmer et al., TCHES 2024 No.3, §1–§3 · §4.1 진입  
표준: FIPS 204 **Algorithm 7** (특히 L5·L17–L20·L33), **Algorithm 8**, **Algorithm 32 ExpandA**  
자산: `HAETAE-FIA-REF-10` · `HAETAE-FIA-REF-01-FIPS204` · `HAETAE-FIA-REF-10-ARTIFACT` (`HO-20260723-11`)  
상태: **approved** (2026-07-24 답변 `승인`) · producer handoff `HO-20260724-06`

용어 정책 (D26): 전문 용어 *English italic*, 일상 설명 한글.

---

## 0. 자산 패킷 소비 기록 (`HO-20260723-11`)

| asset_id | 로컬 경로 | bytes | sha256 (앞 16) | open |
|----------|-----------|------:|----------------|------|
| `HAETAE-FIA-REF-10` | `Papers/…/[10] Correction Fault Attacks….pdf` | 1049112 | `9c187b306377f9ed…` | OK · 26p |
| `HAETAE-FIA-REF-01-FIPS204` | `Papers/…/[1] Module-Lattice-Based….pdf` | 3291746 | `57239b9f84c03227…` | OK |
| `HAETAE-FIA-REF-10-ARTIFACT` | `Papers/assets/HAETAE-FIA/REF-10/tches-2024-a19.zip` | 366604 | `feff393cddf9141a…` | 무결성 catalog 일치 · **미실행** |

카탈로그 행과 byte·hash **일치**. 해석은 아래 단위부터.

---

## 1. 논문이 푸는 문제 (원문사실 · Abstract·§1)

| 항목 | 원문 근거 | 내용 |
|------|-----------|------|
| 대상 모드 | Abstract; §1 | *randomized* / *hedged Dilithium* (NIST 기본). 논문: hedged≈randomized 동일 취급 (§1 각주) |
| 공백 | §1 | det 모드 *DFA*는 잘 알려져 있음; **rand/hedged** FI는 구현 가정·소수 연산에 국한된 선행이 많음 |
| 기여 2공격 | Abstract | (1) *instruction-skip* 확장 — 덧셈 순서와 무관하게 rand에서도 성립 (2) 공개 행렬 **A** (*ExpandA*) 계수 *fault* |
| 공통 핵심 | Abstract | **correcting faulty signatures after signing** — 보정 성공 시 비밀 중간값 → 다수 수집 후 $s_1$ |
| Dilithium2 규모 | Abstract | 공격1 **~1024** · 공격2 **~512** faulty signatures (서명당 단일 표적 *fault*) |
| 실증 | Abstract | *simulated faults* + ARM *clock glitches* |
| 아티팩트 | §1 contrib | github `dilithium-faults` · IACR Artifact `tches/2024/a19` (로컬 ZIP) |

---

## 2. Correction vs 고전 DFA (원문사실 · §3 Attack Intuition)

### 2.1 고전 *differential* 경로 (논문이 대비하는 것)

- 동일 $y$ 를 전제로 **정상 서명**과 **오류 서명**의 차분을 씀 ([BP18], [RJH+19] Case II).
- 동일 $y$ 는 **deterministic** 재서명(동일 $m$)에서 쉽고, **randomized** 에서는 동일 $y$ 재현이 어려움.

### 2.2 본 논문 *Correction* 절차 (한 번만 서명)

**출처:** [10] §3 *Attack Intuition*; Fig.1–2 스케치.

1. 서명 루틴 **1회** 호출 + **단일 표적** *fault* → 대개 **verify 실패** 서명 $\sigma'$ 획득  
2. 선택한 중간값 후보로 $\sigma'$ (또는 검증 입력)을 **수정**  
3. **verify 성공**할 때까지 열거 → 그 보정값 = 키 관련 정보  
4. 다수 방정식 수집 후 **선형대수** 또는 **격자 축소**로 $s_1$

선행 유사: [IMS+22] 는 $s_1$ **비트 플립** + *correction oracle*. 본 논문은 동일 *oracle* 아이디어를 **skip-덧셈**·**공개 A** 로 확장 (§3).

### 2.3 공격자 모델 (§3)

| 가정 | 논문 서술 | 비판 메모 |
|------|-----------|-----------|
| 물리 접근 · *sign* 트리거 · $pk$ 공개 | 명시 | 표준 물리 모델 |
| 서명당 **단일** 표적 *fault* | 명시 | 이론 분석 전제 |
| *rejection loop* **최종 반복**에 *fault* (또는 매 루프 동일 *fault*) | 분석 단순화용 | 논문 스스로 **비현실** 인정. 대안: **첫 시도만** *fault* 후 성공 시만 사용 → 기대 *fault* 수 ÷ 첫 시도 성공확률 (Dilithium2/3/5 ≈ 0.23 / 0.19 / 0.26) |
| 이론 파트: 주입 항상 성공 | §3; 실패 탐지는 §6 | 실증부에서 별도 |

---

## 3. FIPS 204 대응표 (논문 Alg 2.1/2.2 ↔ 표준)

**출처:** [10] Alg 2.1–2.2 (pp.178); FIPS 204 Alg 7–8 · Alg 32.

| 논문 Alg 2.1 (sign) | FIPS 204 Alg 7 | 대응 |
|---------------------|----------------|------|
| L1 `A := ExpandA(ρ)` | **L5** $\hat{\mathbf{A}}\leftarrow\mathrm{ExpandA}(\rho)$ | **공격 2 타겟** (§5) · 공개 $\rho$ |
| L4–5 `rnd` · $\rho'$ | L7 $\rho''\leftarrow H(K\|\mathit{rnd}\|\mu)$ | *hedged*: $rnd$ 난수 · *det*: $rnd=0^{32}$ (Alg 2 경로) |
| L7 `y := ExpandMask` | L11 | [9] 타겟과 동일 계층 (본 단위 비초점) |
| L8–9 `w,w1` | L12–13 | |
| L10–11 $\tilde{c},c$ | L15–16 | 서명 필드는 $\tilde{c}$ (FIPS); 논문 $\tilde{c}$/ $c$ 표기 혼용 시 **SampleInBall 리맵** |
| L12 **`z := y + c s1`** | **L17–20**: $\hat{c}\leftarrow\mathrm{NTT}(c)$; $\langle\langle c s_1\rangle\rangle\leftarrow\mathrm{NTT}^{-1}(\hat{c}\circ\hat{s}_1)$; **$\mathbf{z}\leftarrow\mathbf{y}+\langle\langle c s_1\rangle\rangle$** | **공격 1 타겟** (§4). 표준은 NTT 경로; 대수적으로 $z=y+cs_1$ |
| L13–19 거부·hint | L21–28 | |
| return $(\tilde{c},z,h)$ | L33 `sigEncode` | 논문·FIPS 동일 계열 |

| 논문 Alg 2.2 (verify) | FIPS 204 Alg 8 | 역할 in Correction |
|-----------------------|----------------|---------------------|
| L1 ExpandA | L5 | 검증측 **정상 A** (공격 2에서 서명측 A'와 불일치) |
| L3 SampleInBall | L8 | |
| L4 UseHint / $Az-ct_1 2^d$ | L9–10 | 공격 2: 보정 항 $?$ 탐색 무대 |
| L5 accept 조건 | L12–13 $\|\mathbf{z}\|_\infty$ · $\tilde{c}=\tilde{c}'$ | **Correction oracle** = 공개 *verify* |

**한 줄:** *Correction* 의 “성공 판정기”는 FIPS **Alg 8** 전체(또는 동치 검증식)이고, 공격 1은 주로 **Alg 7 L20** 계수 단위 왜곡 → 서명 $\mathbf{z}$ 한 계수 보정으로 Alg 8을 통과시킨다.

---

## 4. 공격 1 진입 — *Skipping fault* + Case II (원문 · §2.2·§4.1)

### 4.1 FI가 바꾸는 값

**출처:** [10] §2.2 *Skipping Fault*; §4.1.

- 대상: $z = y + cs_1$ 의 **한 성분 $j$ · 한 계수 $i$** 덧셈.
- 수단 예: *instruction skip* · 피연산자 *load* 교란으로 한 합을 0/상수.
- 결과 $z'_j[i]$ 가 구현 순서에 따라:
  - **Case I:** $(cs_1)_j[i]$ 만 남음 → [RJH+19] 식으로 **즉시** 선형식 (rand에도 성립 가능)
  - **Case II:** $y_j[i]$ 만 남음 → 고전법은 **det 재서명 차분** 필요 → **rand에서 막힘**

### 4.2 Correction이 Case II를 여는 방식 (§3 Fig.1 · §4.1)

오류 서명 $(\tilde{c},\,z',\,h)$ 에서 표적 계수만:

$$
(z'')_j[i] \;=\; (z')_j[i] + \alpha, \quad \alpha \in \{0,\pm1,\pm2,\ldots\}
$$

(실제 탐색은 $|\alpha|$ 작은 쪽 우선; $(cs_1)$ 계수는 0 근처 집중 — Fig.3, 분산 근사 $N(0,80)$ 등 Dilithium2).

- $\mathrm{verify}(\tilde{c},z'',h)=\mathrm{accept}$ 인 $\alpha$ 를 $(cs_1)_j[i]$ 로 채택.
- $c\leftarrow\mathrm{SampleInBall}(\tilde{c})$ 후 **회전 곱** 형태로 $(s_1)_j$ 에 대한 **선형식 1개** (논문 `rotmult`).
- 성분마다 $n=256$ 개 독립식 → $\ell\cdot n \in \{1024,1280,1792\}$ (Dilithium2/3/5) — §4.2.

**FIPS 이식:**

| 층 | 위치 | 내용 |
|----|------|------|
| 상위 | Alg 7 **L20** | $\mathbf{z}\leftarrow\mathbf{y}+\langle\langle c s_1\rangle\rangle$ 계수 단위 왜곡 |
| 하위 | 구현 덧셈/로드 | 표준 의사코드에 *skip* 없음 — **구현 FI 모델** |
| 오라클 | Alg 8 | 공개 키로 로컬 검증 가능 |

### 4.3 C 코드

- 로컬: artifact ZIP **미실행** (계약). pqm4 등 라인 매핑은 artifact/README·논문 asm 인용 범위에서만 후속 단위.
- 논문: skip 실증은 [RJH+19] 실험 인용 + 자체 ARM *clock glitch* (후속 단위 수치).

---

## 5. 공격 2 한 줄 예고 (다음 단위 · §3 Fig.2 · §5)

- 타겟: Alg 2.1 L1 / FIPS Alg 7 **L5** · Alg 32 **ExpandA** — **공개** $A$ 한 계수 *fault* ($\Delta A$ 공격자가 알 수 있음).
- 서명측 $A'$ 사용 → 검증 실패. 서명 $\sigma'$ 자체를 고치지 않고 검증식에 $? \approx \Delta A\cdot y$ 꼴을 열거 → $y$ 정보 → $s_1$.
- 의의: *side-channel* 비민감 연산도 FI 타겟 (§1).

(본 단위에서는 개념·대응만. 열거 범위·격자 가속은 **DIL-10-U3** 예정.)

---

## 6. 키 복구 스케치 (원문사실)

| 단계 | 내용 | 출처 |
|------|------|------|
| 중간값 | 공격1: $\alpha=(cs_1)_j[i]$ · 공격2: $?$ ↔ $y$ 정보 | §3–§5 |
| 선형/격자 | 공격1: 가우스 소거 · 공격2: 격자 축소로 *fault* 수 감소 가능 | Abstract; §4–§5 |
| 부분키 | 성공 시 **$s_1$** (전체 $sk$ 아님) | §2.2 말미 |
| 위조 | $s_1$ 만으로 임의 메시지 서명 가능 주장 — [BP18],[RJH+19] 인용 | §2.2 |

---

## 7. 원문사실 / 저자주장 / 해석 / 불확실

| 구분 | 내용 |
|------|------|
| **원문사실** | 두 공격·Correction 절차·Alg 2.1 L1/L12 타겟·Dilithium2 ~1024/~512·sim+glitch·첫 시도 확률 보정 수치(0.23/0.19/0.26) |
| **저자주장** | rand/hedged 기본 환경에서도 다양 FI 가능; 일부 대응(셔플 등) 우회 가능; A 확장도 보호 필요 |
| **해석** | FIPS L20/L5 매핑은 대수·역할 대응. Case II *Correction* 은 “verify를 공개 오라클로 쓰는 단일 실행 *DFA 대체*”로 읽힘. [9] nonce-skip·[11] NTT 와 **직교** (다른 줄) |
| **불확실** | (1) 실제 SoC에서 L20 계수 단위 skip 성공률 — 논문+인용 의존 (2) *masking*+*shuffling* 동시 적용 시 주입 난이도 정량 (3) artifact 코드 라인↔FIPS 1:1 은 미실행 상태라 미확정 (4) HAETAE 수치 이식 금지(G2) — 구조 비교만 |

---

## 8. 비판적 점검 (표준·구현)

| 항목 | 판정 |
|------|------|
| 논문 simplified $z=y+cs_1$ vs FIPS NTT 경로 | **대수 동치** (기본 경로). Attack-2 of [11] 식 대안 경로와 무관 |
| 서명 필드 $c$ vs $\tilde{c}$ | FIPS는 $\tilde{c}$ — *SampleInBall* 리맵으로 선형식 구성 가능 (**마이너**) |
| “최종 *rejection* 반복 *fault*” 가정 | 논문이 비용 보정법 제시 — **분석 수치 ≠ 실측 주입 횟수** 구분 필요 |
| Case I vs II | 구현 덧셈 순서에 의존. *Correction* 은 **II를 rand에서 살리는** 기여; I는 기존 논리 |
| 공개 A *fault* | 표준상 ExpandA는 공개 시드 — **부채널 보호 공백** 지적은 설득력 있음. 단 FI 보호 비용은 별 문제 |
| G2 | 본 단위 수치는 논문 Abstract·§3–§4.2에 한정. 시뮬레이션 표는 후속 단위 |

---

## 9. 다음 단위 예고

| ID | 내용 |
|----|------|
| **DIL-10-U2** | 공격1 심화: Alg 4.1 · $(cs_1)$ 분포·$b$ bound · 셔플 우회 Alg 4.2 · FIPS L20 전파 전개 |
| **DIL-10-U3** | 공격2: ExpandA/ΔA · 검증식 $?$ · 격자 · ~512 |
| **DIL-10-U4** | 대응·실증 수치·[9]/[11] 대비 정리 |

---

## 10. 청중용 출처 문구 (producer 인계 시)

> 출처: [10] Krahmer et al., TCHES 2024 — Correction FA; FIPS 204 Alg 7 L20 · Alg 8 · Alg 32.
