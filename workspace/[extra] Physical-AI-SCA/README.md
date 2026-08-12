# [extra] Physical-AI-SCA — 피지컬 AI 기반 부채널 취약점 **사전 진단** 환경

AI 가 사람 개입 최소로 **실험 설계 → 수집 → 분석 → 보고**를 수행하고, 정형화된 세 문서를
산출하는 환경이다. 준용 표준은 ISO/IEC 17825:2024 이며, **적합성 평가가 아니라 사전
진단(pre-assessment)** 이다 — 그 이유는 §2 에 있다.

---

## 1. 무엇을 왜 만들었나

이 저장소에는 부채널 검증에 필요한 조각이 이미 넷 다 있었다. 그러나 산출 형식이 제각각이라
**하나의 분석기가 셋을 다 받을 수 없었고**, 실험 설계·판정 기준·보고서는 사람의 머릿속과
노트북 서술에만 있어 AI 가 이어받을 수 있는 형태가 아니었다.

이 프로젝트는 그 넷을 **하나의 스키마와 하나의 판정 규칙** 위에 놓는다.

### 설계를 지배하는 명제 — Security is only as strong as the weakest link

고리는 층마다 다르고, 층마다 그것을 볼 수 있는 도구가 다르다.

| 고리 | 깨지는 방식 | 도구 | 이 프로젝트 |
|---|---|---|---|
| 이론 (마스킹 수식) | 증명의 가정이 실제와 안 맞음 | 논문·형식 검증 | **범위 밖** |
| 구현 (소스 → 기계어) | 전이 누설, share 재사용, 컴파일러가 만든 스필 | **에뮬레이션** | 과거 데모 출력 있음, 현재 증거 번들 없음 |
| 물리 (실제 칩) | 글리치·커플링·파이프라인 | **실물 전력 수집** | 골격만 — **미실행** |
| 실행 흐름 | 데이터 의존 분기·타이밍 | **디버그 트레이스** | 골격만 — **미실행** |

**에뮬레이션에서 깨끗해도 실물에서 샐 수 있다** — HW/HD 모델은 물리 효과를 담지 않는다.
**실물에서는 잡음에 묻혀 안 보이는 구조적 누설을 에뮬레이션에서 분리해 볼 수 있다.**
셋은 대체재가 아니라 **상보재**이고, 어느 하나가 깨끗하다는 사실만으로 안전을 주장할 수 없다.

### 에뮬레이션이 검사하는 것

논문이 증명하는 명제는 이렇다 — **올바르게 마스킹된 구현에서는 모든 연산의 HW·HD 가
비마스킹 알고리즘의 민감값과 통계적으로 독립이다.**

코딩 과정의 휴먼 에러는 그 고리를 되살린다. 같은 레지스터에 두 share 를 연달아 쓰면

```
HD = HW(share1 ^ share2) = HW(민감값)
```

이 되어 **수식은 그대로인데 구현만 새는** 상태가 된다. 이 결함은 실측으로 찾기 어렵다 —
잡음에 묻히고, 명령어 단위로 짚기 어렵다. 에뮬레이션은 물리 측정 Noise를 모델링하지 않고
**Trace의 각 Sample(샘플)을 명령어 하나에 대응**시킨다. 선택한 누설 모델과 라벨에서 통계적
종속성이 검출되면 `sample_map`으로 후보 명령어를 역추적할 수 있다. 이는 물리적 누설 위치를
확정하는 것이 아니라 실측으로 교차 확인할 구현 후보를 만드는 절차다.

---

## 2. 이 환경의 위치 — 왜 "적합성 평가" 가 아닌가

ISO/IEC 17825 §1 Scope 가 못박는다. 이 표준은 **ISO/IEC 19790:2012 적합성 판정용**이고,
**ISO/IEC 24759:2017 과 함께** 쓰이며, **"암호모듈의 정의된 경계"** 에서 시험한다.
우리가 가진 것은 그 삼각 구조의 한 다리뿐이다.

| 구조적으로 불가능한 것 | 왜 |
|---|---|
| 적합성 판정 | 모듈 경계·CSP 정의·보안수준 배정이 ISO/IEC 19790 의 일이다. IUT 는 모듈이 아니라 라이브러리다 |
| 독립 시험소 평가 | `shall [07.04]` 는 벤더가 시험소에 정보를 주는 구도다. 여기서는 **벤더 = 시험자 = AI** 다 |
| 기준 설정 | Annex A.1·C·G·H 에 "can supersede this annex in its entirety" 가 붙어 있다 — 승인 기관이 정한다 |
| 육안 검사 | A.2.2 는 육안과 통계를 **둘 다** 요구한다. 육안은 사람의 행위다 |

그래서 목표는 **"표준의 방법론을 준용해, 실제 시험소가 그대로 이어받을 수 있는 형태로
증거를 내되, 못 지킨 것을 전부 드러내는 것"** 이다.

`scope.not_claimed` 를 spec 의 **필수 필드**로 만든 이유가 그것이다 —
**무엇을 주장하지 않는지 적지 않으면 나머지가 전부 주장으로 읽힌다.**

---

## 3. 4층 구조 — AI 는 무엇을 하고 도구는 무엇을 하나

| 층 | 내용 | LLM 관여 |
|---|---|---|
| 1. 결정적 CLI | `collect` · `analyze` · `report` · `verify` · `conformance` | **없음** |
| 2. 계약 파일 | `exp/<id>.yaml` (AI 가 쓴다) · `results.json` (AI 가 읽는다) · `manifest.json` | — |
| 3. 에이전트 지침 | `AGENTS.md` · `PROMPT.md` | — |
| 4. LLM 클라이언트 | `physai/llm.py` — 함수 하나 | 서술 초안만 |

**수치·판정·해시·요건 대조표는 전부 도구가 만든다.** LLM 이 관여하는 곳은 보고서의 서술
초안 하나뿐이고, 환경변수가 없으면 그 칸이 빈 채로 나머지가 다 채워진 문서가 나온다 —
**LLM 이 없어도 산출물은 나온다.**

에이전트 루프·툴콜 파싱·재시도는 만들지 않는다. 그것은 grok 헤드리스·Claude Code 같은
하네스가 하는 일이다. 온라인↔오프라인 전환 비용은 환경변수 세 개다(`physai/llm.py`).

---

## 4. 실행

모든 실행은 **컨테이너 안**이다. 호스트에는 `unicorn`·`lief`·`scalib` 가 없다.

```bash
docker exec -it chipwhisperer-kor bash
cd "/workspace/[extra] Physical-AI-SCA"

# 0) 에뮬레이션용 ELF 빌드 — 소스는 workspace/iut/ 의 것을 그대로 컴파일한다
make -C emul_harness IUT=tiny-AES-c
make -C emul_harness IUT=masked-aes-c

# 0-1) 자가검사 — 수집 전에 반드시 통과해야 한다
python3 -m physai.collectors.emulation --selftest --n 10

# 1) 수집 (실험 계획 보고서를 **수집 전에** 먼저 만든다)
python3 -m physai.collect --spec exp/001_emul_tinyaes.yaml
python3 -m physai.collect --spec exp/002_emul_masked.yaml

# 2) 분석 — TA → SPA → DPA 순서로 수행한다
python3 -m physai.analyze --spec exp/001_emul_tinyaes.yaml
python3 -m physai.analyze --spec exp/002_emul_masked.yaml

# 3) 보고서 3종 + 증거 번들
python3 -m physai.report --run 001_emul_tinyaes

# 4) 증거 검증 — 해시·스키마·툴체인 대조
python3 -m physai.verify --run 001_emul_tinyaes

# 기존 Dataset에 요건 대조표만 생성
python3 -m physai.conformance --dataset "/workspace/[extra] SCALib/traces/scalib_dataset_tiny-AES-c.h5" --level 3
```

각 CLI 는 마지막 줄에 JSON 요약을 내고 종료 코드로 성패를 알린다.

---

## 5. 산출물 세 가지

| 문서 | 생성 시점 | 담는 것 |
|---|---|---|
| `01_experiment_plan.md` | **수집 전** | 적용 범위 선언(`not_claimed` 포함) · 요건 대조표 · 판정 기준 · 필요 트레이스 수 산정 근거 · 벤더 정보 |
| `02_analysis_report.md` | 분석 후 | 필수 시험 3종 결과 · **결함 후보의 명령어 주소** · 갱신된 대조표 · 본 고리와 보지 않은 고리 |
| `03_evidence_manifest.md` + `manifest.json` | 마지막 | 모든 파일의 sha256 · 생성 명령 · 툴체인 · 재현 절차 |

**계획 보고서를 수집 전에 만드는 것이 핵심이다.** 결과를 본 뒤 판정 기준을 고르는 사후
정당화를 구조로 막는다. ISO/IEC 17825 §8.4 `shall [08.04]` 도 통계 시험 전에 effect
size·α·β 를 지정하라고 요구한다.

---

## 6. 판정 기준

**"취약/안전" 은 키 복구가 아니라 누설 관측으로 판정한다** (§7.2 — "test passes unless
leakage is observed"). 키가 복구되지 않아도 누설이 임계를 넘으면 fail 이다.

### 필수 시험은 3종이다

§7.3.2 `shall [07.03]` 와 §8.1 `shall [08.01]` 이 **TA·SPA·DPA 셋 모두**를 요구한다.

| 시험 | 대칭키에서의 표적 | Level 3 요건 |
|---|---|---|
| **TA** | 실행시간이 CSP·평문에 의존하는가 (= constant-time) | A.2.4 — 각 1,000회, **Annex A 유일의 `shall collect`** |
| **SPA** | key derivation (§8.3.1) | A.2.2 — 11 트레이스, 육안 + 통계 **둘 다**. 도구는 통계만 하므로 **판정을 내지 않는다**(§9) |
| **DPA** | Welch t-test 로 두 집단 비교 (§8.4) | A.2.3 — Formula (1) |

- **TA 는 캐시 유무와 무관하게 수행한다.** §8.2 의 캐시 면제는 Reference [50] 의 캐시
  공격 프레임워크에만 걸린다. §7.3.4 의 절차에는 캐시라는 단어가 나오지 않는다.
- **TA 는 평균뿐 아니라 분산도 검정한다** (2차 타이밍 누설, `shall`).
- **고차 제외는 DPA 에만 해당한다** (Fig.1 NOTE 3). 타이밍의 2차는 의무다.
- **CPA 는 판정에 쓰지 않는다.** 표준상 필수 시험이 아니며, 여기서는 배관(입력 주입·정렬·
  라벨링)이 옳은지 확인하는 **양성 대조**로만 쓴다.

### 순서와 예외

§7.3.2 는 TA → SPA → DPA 순서를 정한다("should"). 그러나 **앞이 fail 이어도 뒤를 계속
수행한다** — §8.1 이 셋을 **모두** 평가하라고 `shall` 로 요구하기 때문이다. shall 이 should
를 이긴다. 유일한 예외는 TA 내부의 2단계로, §7.3.4 가 1단계 실패 시 2단계로 가지 않는다고
명시한다.

### 대조군이 판정의 신뢰를 만든다

| 대조군 | 기대 | 어긋나면 |
|---|---|---|
| `tiny-AES-c` (비마스킹) | 민감 구간에서 검출 | 검출기·라벨·Trace 수·구간 설정을 점검하고 원인 확인 전 판정 중단 |
| masked 의 `KeyExpansion` 구간 | 검출됨 (문서화된 보호 범위 밖) | 구간 경계 산정 오류 |
| masked 의 `CipherMasked` 구간 | 검출 없음 | 결함 후보 — 찾으려던 것 |

**"masked 에서 아무것도 안 나왔다" 는 결과는, 같은 검출기가 tiny-AES 에서 반응한다는
증거가 있어야만 의미가 있다.** `exp/001` 이 그 증거를 만드는 실험이다.

---

## 7. 누설 벡터 (에뮬레이션 채널)

명령어마다 네 성분을 뽑아 **성분별로 연접**한다. 길이 = 4 × L (L = 구간 명령어 수).

```
trace = [ hw_reg | hd_reg | hw_mem | hd_mem ]
```

| 성분 | 정의 | 잡는 것 |
|---|---|---|
| `hw_reg` | 그 명령어가 쓴 레지스터의 실행 후 값의 HW 합 | 값 자체의 누설 |
| `hd_reg` | **HW(R_before ^ R_after)** — 같은 레지스터의 앞뒤 | 레지스터 전이 누설 |
| `hw_mem` | 메모리 쓰기 값의 HW 합 | 메모리 값 누설 |
| `hd_mem` | **HW(old ^ new)** — 같은 주소의 앞뒤 | 메모리 전이 누설 |

**HD 는 같은 저장소의 한 명령어 앞뒤 값끼리만 계산한다.** `HD(R2_before, R5_after)` 같은
서로 다른 레지스터 쌍은 실제 하드웨어에서 전이 누설이 생기는 방식이 아니고, 조합이
폭발해 오탐만 만든다.

메모리 성분을 넣는 이유: tiny-AES 계열은 state 를 메모리 배열에 두고 **in-place 로
갱신**한다. 전이 결함은 레지스터보다 이 state 버퍼에서 더 자주 난다.

**PC 는 뺀다.** 제어흐름이 데이터 독립이면 PC 는 상수라 신호가 없고, 데이터 의존이면 그것은
타이밍 분석이 잡을 일이며 이 벡터에 섞으면 정렬이 무너진다.

---

## 8. 왜 실측과 같은 소스를 컴파일하나

`emul_harness/Makefile` 은 `../../iut/<IUT>/aes.c` 를 직접 컴파일한다. 실물 펌웨어
(`[extra] SCALib/simpleserial_<IUT>/`)도 **같은 파일**을 컴파일한다. 컴파일 플래그도
펌웨어에서 그대로 옮겼다 — 특히 **`-Os`** 다.

> 최적화 수준이 전이 누설을 **만들기도 하고 없애기도 한다.** 같은 C 소스라도 `-Os` 와
> `-O2` 는 레지스터 할당과 명령어 선택이 달라 서로 다른 구현이 된다. 플래그가 다르면
> "에뮬레이션에서 찾은 결함이 실측 타겟에도 있다" 고 말할 근거가 사라진다.

과거 노트북 출력에서 실측 HDF5의 Trace 길이 비율(masked/normal)은 **1.6636**, 에뮬레이션
명령어 수 비율은 **1.6828**(10,147 / 6,030)로 기록됐다. 비율이 가깝다는 사실만으로 두
채널의 구간 대응이 검증되지는 않는다. 차이는 명령어별 사이클 수 등으로 설명될 수 있지만,
실측 정렬과 명령어 구간을 대조하기 전에는 원인을 확정하지 않는다. 현재 HDF5와 실행 증거
번들이 없으므로 새 실행에서 다시 산출해야 한다.

---

## 9. 알려진 한계 — 감추지 않는다

| 한계 | 영향 |
|---|---|
| **Unicorn 에 사이클 모델이 없다** | 에뮬 TA 는 명령어 수 기준이다. 수가 **다르면** 데이터 의존 제어흐름의 확정 소견이지만, **같아도** constant-time 을 증명하지 못한다 |
| **실물 수집기 2종 미실행** | `cw_power.py`·`cw_debugtrace.py` 는 한 번도 실행된 적이 없다. 각 파일 머리말에 명시 |
| **A.2.5 전처리 미적용** | Level 3 은 같은 입력 10회 평균을 `shall` 로 요구한다. `preprocessing_average_n=1` 이며 대조표에 그대로 나온다 |
| **SPA 판정 불가** | 육안 검사가 사람의 행위이고, 잡음 바닥이 0인 결정적 채널에서는 "키가 다르면 트레이스도 다르다"가 거의 항상 참이라 그것만으로 fail을 내면 판별력이 없다. **언제나 `inconclusive`**를 내고 관측값(`statistical_verdict`)으로 사람이 판정한다 |
| **STM32F303 캐시 유무 미확인** | §8.2 면제의 전제인데 저장소 안에 근거 문서가 없다. 대조표에 `미기록` 으로 나온다 |
| **EM 채널 없음** | 근접 자기장 프로브 미보유. Annex E 는 오히려 EM 을 선호한다고 적는다 |
| **현재 DPA 판정 근거 없음** | 저장소에 현재 결과 파일이 없다. 제공된 데모 명세의 수집량도 Formula (1)의 N보다 작으므로, 그 규모로 실행하면 DPA는 `inconclusive`가 된다. |

---

> 한계를 줄이려면 실물 수집기 검증, Level 3 전처리 적용, 충분한 트레이스 확보, 사람이
> 수행하는 SPA 육안 검사가 필요하다. [`To_Do_List.md`](To_Do_List.md)는 이 작업을 실장비
> 필요 여부로 나누고 각 항목의 완료 판정 기준까지 기록한 실행 목록이다.

## 10. 디렉터리

```
physai/
  paths.py         저장소 경로 해결 (workspace/lib 를 sys.path 에 넣는다)
  spec.py          실험 명세 로드·검증, Formula (1)·보정 임계 계산
  collect.py       CLI: spec → HDF5 생성 → SCHEMA 1.1 검증(위반 시 실패)
  collectors/
    emulation.py   ★ 에뮬레이션 수집기 (과거 데모 출력 있음, 현재 증거 번들 없음)
    cw_power.py    실물 전력 (미실행)
    cw_debugtrace.py  디버그 트레이스 (미실행)
  analyze.py       CLI: TA→SPA→DPA 순서 수행 → results.json
  tests/{ta,spa,dpa}.py   필수 시험 3종
  soundness.py     구현 층 1차 누설 검출 + 명령어 지목
  conformance.py   ISO/IEC 17825 요건 대조표
  report.py        보고서 3종 + 증거 번들
  verify.py        증거 번들 검증
  llm.py           OpenAI 호환 클라이언트 (함수 하나)
emul_harness/      에뮬레이션용 ELF 빌드 (workspace/iut/ 소스를 직접 컴파일)
To_Do_List.md      남은 작업 — 실장비 필요분 · 추가 확인분 (항목마다 완료 판정 기준)
contracts/         experiment_spec.schema.json
exp/               실험 명세 (AI 가 작성)
runs/              실행 산출물 (gitignore)
traces/            Dataset (gitignore — GB 단위)
```

공용 정의는 이 프로젝트 밖에 있다.

| 위치 | 내용 |
|---|---|
| `workspace/lib/sca_schema.py` | 스키마 상수·검증기·경로 기반 로더 |
| `workspace/lib/aes_ref.py` | SBOX·HW·`intermediates()` 민감값 참조 계산 |
| `workspace/iut/` | IUT(테스트 대상 구현) 암호 라이브러리 (펌웨어와 공유) |

---

## 11. 인용 규약

ISO/IEC 17825:2024 원문은 저작권 보호 문서이며 **이 저장소에 포함되지 않는다.**
이 프로젝트의 문서·보고서는 **조항 번호와 요구의 취지만 자기 말로** 적고 원문을 옮기지 않는다.

출처: ISO/IEC 17825:2024, Second edition, 2024-01,
*Information technology — Security techniques — Testing methods for the mitigation of
non-invasive attack classes against cryptographic modules*.
