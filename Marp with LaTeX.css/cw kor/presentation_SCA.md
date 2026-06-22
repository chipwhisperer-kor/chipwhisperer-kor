---
marp: true
math: mathjax
paginate: true
header: "ChipWhisperer로 배우는 부채널 분석 — 파형 수집부터 와이어태핑까지"
footer: ""
---

<style>
/* LaTeX.css 불러오기 */
@import url('../style.min.css');

/* 로컬 Noto Serif KR 폰트 */
@font-face {
    font-family: 'Noto Serif KR Local';
    src: url('../NotoSerifKR-Regular.ttf') format('truetype');
    font-weight: 400;
}
@font-face {
    font-family: 'Noto Serif KR Local';
    src: url('../NotoSerifKR-Bold.ttf') format('truetype');
    font-weight: 700;
}

/* 폰트 우선 적용 */
body, h1, h2, h3, h4, h5, h6, p, li, header, footer {
    font-family: 'Latin Modern', 'Noto Serif KR Local', serif !important;
}

/* Marp 슬라이드 기본 스타일 */
section {
    background-color: #fdfdff;
    font-size: 26px;
}

h1, h2 {
    text-align: center;
}

pre {
    background-color: #fffdfd;
    font-size: 18px;
    line-height: 1.35;
}

/* 표 중앙 정렬 */
section table {
    display: table !important;
    margin-left: auto !important;
    margin-right: auto !important;
    max-width: 100% !important;
    word-break: keep-all;
}

/* 그림 중앙 정렬 */
section img {
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Header 스타일 */
header { font-size: 16px; }

/* 페이지 번호 (오른쪽 하단) */
section::after {
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    bottom: 5px;
    font-size: 10px;
}

/* 섹션 구분(divider) 슬라이드 */
section.divider h1 {
    border-bottom: 2px solid #333;
    padding-bottom: 0.15em;
}

/* 결론 슬라이드의 강조 박스 */
.takeaway {
    border: 1px solid #888;
    border-left: 6px solid #0000ff;
    background: #f5f5ff;
    padding: 0.5em 1em;
    margin: 0.6em 0;
    font-weight: 700;
    text-align: center;
}

/* 참고문헌 목록: 작게, 줄간격 좁게 */
.references {
    font-size: 0.78em;
    line-height: 1.45;
}

/* Title / divider 슬라이드에서 header·footer·페이지번호 숨기기 */
section.lead header,
section.lead footer,
section.lead::after {
    display: none !important;
}
</style>

<!-- _class: lead -->
# ChipWhisperer로 배우는<br>부채널 분석(SCA)

### 전력 파형 수집부터 와이어태핑까지

**발표자:** 김박사  
**날짜:** 2026년 6월 16일

---

## 목차 (Contents)

1. **서론** — 부채널 분석과 ChipWhisperer
2. **1부** · 기본 파형 수집 — *단일 장치로 안정적으로 trace 모으기*
3. **2부** · 와이어태핑 응용 — *두 장치로 도청 시나리오 재현하기*
4. **결론** 및 참고문헌

<!--
1부는 SCA_main 노트북(5단계), 2부는 Wiretapping 노트북(7단계)을 기반으로 합니다.
-->

---

<!-- _class: lead divider -->
# 서론
## 부채널 분석과 ChipWhisperer

---

## 부채널 분석(SCA)이란?

암호 알고리즘이 **수학적으로 안전**하더라도, 하드웨어가 연산을 수행할 때 새어 나오는 **부수 정보**(전력 소비·전자기 방사·처리 시간)에는 비밀 키와 관련된 정보가 누설됩니다.

이를 측정·분석해 키를 복원하는 기법이 **부채널 분석(Side-Channel Analysis)** 입니다.

<div class="definition">

(전력 누설의 원리) CMOS 회로의 스위칭 활동은 처리 중인 **중간값(intermediate value)** 의 해밍 가중치/거리에 따라 달라진다. 따라서 *"같은 키 + 다른 평문"* 으로 여러 번 측정하면, 각 시점의 전력 소비와 중간값 사이에 **통계적 상관관계**가 나타난다.

</div>

---

## 왜 ChipWhisperer를 쓰는가?

부채널 측정은 본래 고가의 오실로스코프와 정밀 트리거 환경을 요구합니다.
**ChipWhisperer**는 이를 한 보드에 통합한 오픈소스 플랫폼입니다.

* 타겟 MCU 클럭에 **동기화된 ADC** — jitter(지터) 최소화
* 측정 트리거 + 타겟 통신 + 전력 분석을 **USB 한 줄**로 처리
* **Python API**로 손쉬운 자동화

```text
호스트 PC (Python / Jupyter)
    │  USB
    ▼
ChipWhisperer-Husky (scope + 제어보드)
    │  20-pin 커넥터
    ▼
CW308 UFO 보드 — STM32F303 (타겟 MCU)
```

---

## 핵심 용어집 (Glossary)

| 용어 | 의미 |
|:----|:----|
| **Power Trace** | 시간에 따른 타겟의 전력 소비 측정값 (1차원 배열) |
| **Trigger** | 측정 시작/종료 시점을 알려주는 GPIO 신호 |
| **trig_count** | 트리거 ON → OFF 사이에 ADC가 수집한 샘플 개수 |
| **samples** | 한 trace당 저장할 전체 샘플 수 |
| **TV (Test Vector)** | 측정에 사용할 입력값 세트 (`fixed` 또는 `random`) |
| **Golden Model** | 호스트 PC에서 동일 연산을 직접 계산한 기준 출력값 |
| **HDF5** | 대용량 trace 저장에 적합한 계층적 바이너리 포맷 |
| **CPA / DPA** | 통계적 부채널 공격 기법 (후속 강의 주제) |

---

<!-- _class: lead divider -->
# 1부 · 기본 파형 수집
## 단일 장치로 안정적인 Trace 모으기

---

## 1부 전체 흐름 — 5단계

목표: 부채널 실험의 가장 기본인 **"전력 파형을 안정적으로 수집하기"** 까지.

| 단계 | 내용 | 핵심 산출물 |
|:----:|:----|:----|
| **1** | ChipWhisperer ↔ 타겟 데이터 송수신 | SimpleSerial 통신 검증 |
| **2** | 파형 수집 파라미터 이해 | `trig_count` 측정 → `samples` 결정 |
| **3** | 단일 파형 수집 및 시각화 | 1개의 Power Trace 확인 |
| **4** | 다량 파형 수집 + DB 저장 | `*.h5` 파일 (수백~수만 trace) |
| **5** | HDF5 DB 불러오기 및 검증 | 저장 데이터 재확인 + 시각화 |

> 측정 품질은 곧 **파형 수집의 품질**입니다. 셀 단위로 차근차근 의미를 이해하는 것이 중요합니다.

---

## 1단계 — SimpleSerial 패킷 구조

ChipWhisperer는 **SimpleSerial 프로토콜**로 타겟과 통신합니다. 각 명령 패킷은 고정 구조를 가집니다.

```text
┌──────┬──────┬─────────┬──────────┬─────┐
│ cmd  │ scmd │  len    │  data[]  │ crc │
│(1B)  │(1B)  │  (1B)   │(최대245B)│(1B) │
└──────┴──────┴─────────┴──────────┴─────┘
```

| 필드 | 의미 |
|:----:|:----|
| `cmd`  | 명령 종류 — `0x81`(쓰기), `0x82`(연산실행), `0x83`(결과읽기) |
| `scmd` | 하위 명령 — `'k'`(키), `'p'`(평문), `'l'`(길이), `'c'`(연산), `'r'`(결과) |
| `len` / `data` / `crc` | 데이터 길이 / 실제 전송 데이터 / 오류 검출용 체크섬 |

> SimpleSerial V1은 패킷당 최대 64바이트, **V2는 최대 249바이트**를 전송합니다.

---

## 1단계 — 골든 모델(Golden Model) 검증

오늘 실험에서 타겟은 단순한 `k XOR p` 연산을 수행합니다.
호스트가 직접 계산한 값(골든 모델)과 비교해 **통신·연산의 정상성**을 검증합니다.

```python
# 타겟 보드에서 받은 결과
Return_k_XOR_p = ret_k_XOR_p[3 : 3 + ret_k_XOR_p[2]]

# 호스트(Python)에서 직접 계산한 골든 모델
Golden_k_XOR_p = bytes(x ^ y for x, y in zip(data_k, data_p))

if Golden_k_XOR_p == Return_k_XOR_p:
    print('✅ 통신 및 연산 검증 성공! (타겟 출력 == 골든 모델)')
```

> 💡 골든 모델과 하드웨어 출력이 일치하면 **펌웨어와 통신 모두 정상**임을 의미합니다.

---

## 2단계 — 파형 수집 파라미터

타겟 연산이 몇 클럭이나 걸리는지 측정해, **잘리지 않으면서도 메모리 낭비가 없는** 적정 `samples`를 결정합니다.

```text
                트리거 신호 (gpio4)
          │◄─pre──► │◄───── 연산 구간 (trig_count) ─────►│
          │samples  │                                   │
```

$$
\text{samples} = \left\lfloor \frac{\text{trig\_count}}{\text{decimate}} \right\rfloor + \text{presamples}
$$

* `trig_count` — 실제 연산에 걸린 ADC 샘플 수 (자동 측정, 읽기전용)
* **너무 짧게** → 파형 끝이 잘림 / **너무 길게** → 메모리 낭비·속도 저하

---

## 2단계 — ADC 클럭 동기화

ChipWhisperer-Husky는 타겟 MCU 클럭에 **동기화된 ADC**를 사용합니다.

```python
scope.clock.adc_src  = 'clkgen_x4'   # MCU 클럭의 4배 속도로 샘플링
scope.clock.adc_mul  = 4             # 클럭 1주기당 4개 샘플
scope.adc.presamples = 0
scope.adc.decimate   = 1
```

MCU가 7.37 MHz로 동작하면 ADC는 **29.5 MHz**로 샘플링 → 파형이 더 정밀해지고 시점 식별이 쉬워집니다.

| 하드웨어 | 최대 샘플 수 |
|:--------:|:-----------:|
| CW-Lite  | 24,400 |
| CW1200   | 96,000 |
| CW-Husky | 131,070 |

---

## 3단계 — 단일 파형 수집 & 시각화

`my_get_trace()`는 **arm → 연산 트리거 → capture → 결과 읽기**를 한 번에 처리하고,
`(타겟 출력값, 파형 numpy 배열)` 튜플을 반환합니다.

본 강의의 모든 파형 시각화는 **Bokeh**(인터랙티브)으로 그립니다.

> 🔬 **파형을 보며 점검할 사항**
> - 파형이 중간에 잘리지 않는가? → `samples` 재조정
> - 진폭이 너무 크거나 작지 않은가? → `scope.gain` 조정
> - 명확한 클럭 패턴(주기적 봉우리)이 보이는가? → 동기 ADC 정상 작동

---

## 4단계 — 다량 파형 수집 + HDF5 DB

부채널 분석에는 보통 **수천~수만 개의 파형**이 필요합니다.
메모리에 한꺼번에 올리지 않고 **HDF5 데이터셋에 점진적으로 append**합니다.

```text
SCA_DB.h5
├── i_k  [N × data_len]  uint8     ← 입력 키 배열
├── i_p  [N × data_len]  uint8     ← 입력 평문 배열
├── o    [N × data_len]  uint8     ← 연산 출력 배열
└── t    [N × tr_len]    float32   ← 전력 파형 배열
```

* `maxshape=(None, ...)` → 파형 수 N을 **동적으로 확장**
* `chunks=True` → 청크 저장으로 random access I/O 성능 향상

---

## 4단계 — TV(Test Vector)의 두 가지 용도

| `TV_case`  | 설명 | 용도 |
|:---------:|:----|:----|
| `'fixed'`  | 매번 동일한 k, p 사용 | 파형 반복성 확인, fixed-vs-random t-test |
| `'random'` | 매번 랜덤한 k, p 사용 | 상관분석(CPA) 등 실제 공격 데이터 수집 |

```python
for i in trange(NUM_OF_TRACES, desc='파형 수집 중'):
    # TV 생성 → 타겟에 주입·검증 → my_get_trace() → HDF5에 1행씩 append
    dset_t.resize(dset_t.shape[0] + 1, axis=0)
    dset_t[-1:] = np.array(trace)
```

> 💡 `debug_mode = True` 로 두면 5개만 수집해 화면 출력만 합니다(DB 저장 X). 본격 수집 전 점검용.

---

## 5단계 — DB 불러오기 & 누설 확인

저장한 `.h5`를 다시 불러와 구조를 확인하고, `o == i_k XOR i_p` 관계를 검증합니다.
여러 파형을 **겹쳐(overlay)** 그려 수집 안정성을 점검합니다.

> 💡 **파형 겹쳐 보기의 의미**
> - 패턴이 잘 일치 → 수집이 안정적이며 재현성 높음
> - 어긋나거나 흔들림 → 트리거 타이밍 문제, 샘플레이트 조정 필요
> - 동일 시점에서 trace 간 진폭 차이 → 이것이 바로 **부채널 누설(side-channel leakage)**

---

## 1부 요약

| 단계 | 핵심 함수 / 명령 | 결과 |
|:----:|:---|:---|
| 1 | `send_cmd()` / `read_cmd()` / `my_fsr_cmd()` | 송수신 및 골든 모델 검증 |
| 2 | `scope.arm()` → `capture()` → `trig_count` | 연산 구간 측정 → `samples` 결정 |
| 3 | `my_get_trace()` + Bokeh | 단일 파형 수집·시각화 |
| 4 | HDF5 dataset + `resize` + `trange` | 다량 파형 수집·동적 DB 저장 |
| 5 | `h5py.File('r')` + Bokeh overlay | DB 불러오기·다중 파형 비교 |

**핵심 개념:** SimpleSerial 패킷 구조 · `samples` 공식 · HDF5 동적 데이터셋 · TV의 용도 · 시각화 기반 신호 점검

---

<!-- _class: lead divider -->
# 2부 · 와이어태핑 응용
## 두 장치로 도청 시나리오 재현하기

---

## 와이어태핑(Wire-Tapping)이란?

단일 보드 실습에서는 측정 장비가 곧 **"공격자가 통제하는 통신 단말"** 입니다.
하지만 실제 공격자는 보통 **동작 중인 시스템의 신호선에 프로브만 부착**할 뿐, 통신 흐름에는 개입할 수 없습니다.

이 **수동 측정(passive measurement) 시나리오**를 두 장치로 재현합니다.

```text
ChipWhisperer-Lite   ──  "정상 사용자" 역할
   └─ 타겟과 UART 통신 · 펌웨어 플래싱 · 시스템 클럭(HS2) 공급

ChipWhisperer-Husky  ──  "은밀한 관측자" (wire-tap) 역할
   └─ 트리거 / 클럭 / 전력 세 가닥만 분기 측정
   └─ 펌웨어·통신에는 일체 개입하지 않음
```

---

## 단일 장치 vs 다중 장치 와이어태핑

| 항목 | 단일 장치 SCA | 다중 장치 와이어태핑 |
|:----:|:----:|:----:|
| 측정 장비 수 | 1대 (Husky) | **2대 (Lite + Husky)** |
| UART 통신 / 프로그래밍 | Husky | **Lite** 전담 |
| 타겟 클럭 공급원 | Husky `clkgen` | **Lite `clkgen` (HS2)** |
| 측정 장치 역할 | 통신 + 측정 | **측정만** (passive observer) |
| 측정 장치 클럭 소스 | 내부 PLL | **외부 클럭(`extclk_aux_io`)** + 주파수 탐색 |
| 공격 시나리오 현실성 | 낮음 | **높음** (제3자 도청) |

> 통신을 주관하는 Lite의 시각과, 외부에서 신호선만 보는 Husky의 시각을 **동시에** 확보합니다.

---

## 물리적 배선 — 핵심 3선

Husky는 통신에 개입하지 않고 **세 신호선만** 물리적으로 분기해 측정합니다.

| 라인 | 출처 (타겟 보드) | 입력 (Husky) | 의미 |
|:----:|:----:|:----:|:----|
| 트리거 | GPIO4 / TRIG | 전면 20-pin **D0** | 캡처 시점 정렬용 디지털 신호 |
| 클럭 | CLKIN | 전면 **AUX MCX** | 타겟 동작 클럭 (정확한 주파수 미상) |
| 전압 | SHUNTL | 측면 **Measure (Pos)** | 션트 양단 전압 강하 (전력 소비 비례) |

> ⚠️ 실습 편의를 위해 펌웨어가 암호화 진입 시 GPIO4를 트리거로 토글합니다.
> 실제 공격에서는 통신 신호(UART idle, 특정 패턴 등)를 트리거로 활용해야 합니다.

---

## 2부 전체 흐름 — 7단계

| 단계 | 내용 | 핵심 산출물 |
|:----:|:----|:----|
| **1** | 다중 장치(Lite + Husky) 동시 연결 | `lite_scope`, `husky_scope` |
| **2** | Lite ↔ 타겟 통신 채널 확보 | `target` 객체 |
| **3** | 펌웨어 빌드 + Lite 경유 플래싱 | 플래싱 완료 타겟 |
| **4** | 골든 모델로 통신·연산 검증 | 통신 검증 완료 |
| **5** | **Husky 와이어태핑 환경 구성** | 측정 준비된 Husky |
| **6** | `Encrypt()` + 다수 파형 수집 루프 | `t_husky`, `t_lite` 배열 |
| **7** | Husky vs Lite 파형 비교 + 자원 해제 | 인터랙티브 Bokeh 그래프 |

---

## 핵심 ① — 시리얼 넘버 기반 다중 장치 연결

`cw.scope()`만 호출하면 **가장 먼저 발견된 장치 하나**만 연결됩니다.
두 장치를 동시에 다루려면 **시리얼 넘버**를 명시해야 합니다.

```python
def connect_all_devices() -> dict:
    device_list = cw.list_devices()       # USB 버스 스캔 (sn 포함)
    scopes = {}
    for device in device_list:
        name = device['name'].replace("-", "_")
        scopes[name] = cw.scope(sn=device['sn'])   # sn 명시 연결
    return scopes

scopes = connect_all_devices()
lite_scope  = scopes["ChipWhisperer_Lite"]
husky_scope = scopes["ChipWhisperer_Husky"]
```

> 💡 시리얼 넘버는 호스트가 두 장치를 안정적으로 구분하는 **유일한 식별자**입니다.

---

## 핵심 ② — 외부 클럭 동기화 (3-스텝 부트스트랩)

단일 Husky는 자기가 클럭을 공급해 동기화가 자동이지만, 여기서 Husky는 **외부 클럭을 받아오는 입장**입니다. 주파수·위상을 모르므로 **탐색·정렬**해야 합니다.

```python
husky_scope.io.aux_io_mcx    = 'high_z'          # ① AUX를 입력으로
husky_scope.clock.clkgen_src = 'extclk_aux_io'   #   PLL 입력=외부 클럭

husky_scope.clock.clkgen_freq = data.mode().iloc[0]  # ② freq_ctr 최빈값으로 잠금
husky_scope.clock.adc_mul = 4                        # ③ 클럭당 4 샘플
husky_scope.clock.reset_adc()
```

| 단계 | 동작 |
|:----:|:----|
| ① 소스 전환 | PLL 입력을 외부 AUX(`high_z` 입력)로 |
| ② 주파수 탐색 | 내장 카운터 `freq_ctr`로 외부 클럭(≈7.4 MHz) 측정 → PLL 목표 잠금 |
| ③ 오버샘플링 | `adc_mul=4`로 ADC 정렬 후 `adc_locked` / `clkgen_locked` 확인 |

---

## 핵심 ③ — 동시 arm 패턴

두 스코프를 **모두 arm한 뒤** 단일 트리거가 발생해야 두 파형이 시간축으로 정렬됩니다.

```python
for i in range(N_TRACES):
    husky_scope.arm()                 # 1) 두 스코프 모두
    lite_scope.arm()                  #    "트리거 대기" 진입
    ct = Encrypt(data_k, data_p)      # 2) Lite 통신 → 타겟이 GPIO4 토글
    ret_h = husky_scope.capture()     # 3) 동일 트리거에
    ret_l = lite_scope.capture()      #    두 스코프 동시 반응
    t_husky.append(husky_scope.get_last_trace())
    t_lite.append(lite_scope.get_last_trace())
```

> ⚠️ `Encrypt()` *후* 에 `arm()`을 부르면 트리거가 이미 지나가 캡처가 실패합니다. **arm 순서를 뒤바꾸지 마세요.**

---

## 7단계 — Husky vs Lite 파형 비교

동일 연산을 두 스코프가 캡처한 파형을 **Bokeh으로 겹쳐** 와이어태핑 경로의 충실도를 검증합니다.

> 🔬 **점검 사항**
> - **거시 패턴 일치** — 피크 위치·반복 패턴이 일치하는가?
> - **상대 진폭** — 절대값은 달라도 *변동 구조*는 같아야 함
> - **노이즈 플로어** — 와이어태핑은 케이블이 길어 SNR이 낮을 수 있음
> - **시간축 정렬** — 동일 특징점의 sample index가 거의 같아야 함

<div class="takeaway">

두 파형이 거시적으로 일치하면, Husky 데이터만으로 CPA·DPA를 수행할 수 있다 — 즉 현실적 와이어태핑 공격의 실험적 타당성 확보.

</div>

---

## 2부 요약

| 단계 | 핵심 함수 / 명령 | 결과 |
|:----:|:---|:---|
| 1 | `cw.list_devices()` + `cw.scope(sn=...)` | 다중 장치 동시 연결 |
| 2 | `cw.target(lite_scope, SimpleSerial2)` | Lite ↔ 타겟 채널 확립 |
| 3 | `make` + `cw.program_target(lite_scope, ...)` | Lite가 프로그래머로 동작 |
| 4 | `my_fsr_cmd()` + Golden Model | 통신·연산 정상성 검증 |
| 5 | `clkgen_src='extclk_aux_io'` + `freq_ctr` | Husky가 외부 클럭에 PLL 잠금 |
| 6 | 양쪽 `arm()` → `Encrypt()` → 양쪽 `capture()` | 두 스코프 동시 캡처 |
| 7 | Bokeh overlay (Husky vs Lite) | 와이어태핑 신호 품질 검증 |

---

<!-- _class: lead divider -->
# 결론

---

## 결론 및 정리

본 강의는 부채널 분석을 위한 **파형 수집 파이프라인**을 두 단계로 다뤘습니다.

1. **1부** — 단일 장치로 SimpleSerial 통신부터 HDF5 DB 저장까지, *안정적 trace 수집*의 기본기.
2. **2부** — 두 장치 역할 분리로 *현실적 도청 시나리오*를 재현하고, 외부 클럭 동기화·동시 arm으로 와이어태핑 파형을 확보.
3. **검증 중심 사고** — 모든 단계에서 골든 모델·overlay 비교로 *데이터 신뢰성*을 먼저 확인.

<div class="takeaway">

"제대로 모은 파형 한 세트가, 화려한 공격 알고리즘보다 먼저다."

</div>

**향후:** 수집된 trace에 **CPA / DPA** 등 통계적 부채널 공격을 적용해 실제 키 복원으로 이어집니다.

---

## 참고문헌 (References)

<div class="references">

[1] NewAE Technology, "ChipWhisperer Documentation — SimpleSerial Protocol," https://chipwhisperer.readthedocs.io, 2025.
[2] NewAE Technology, "ChipWhisperer-Husky & CW308 UFO Target Board User Manual," 2024.
[3] C. O'Flynn and Z. Chen, "ChipWhisperer: An Open-Source Platform for Hardware Embedded Security Research," *COSADE*, pp. 243–260, 2014.
[4] P. Kocher, J. Jaffe, and B. Jun, "Differential Power Analysis," *CRYPTO '99*, LNCS 1666, pp. 388–397, 1999.
[5] The HDF Group, "HDF5 for Python (h5py) Documentation," https://docs.h5py.org, 2025.
[6] Bokeh Contributors, "Bokeh Visualization Library Documentation," https://docs.bokeh.org, 2025.

</div>

> 본 슬라이드는 `1_0_SCA_main.ipynb` 와 `1_0_Wiretapping4SCA.ipynb` 강의 노트북을 기반으로 구성되었습니다.
