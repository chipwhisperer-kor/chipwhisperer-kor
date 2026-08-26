# SCHEMA — 부채널 Trace(트레이스) Dataset(데이터셋) 스키마

이 저장소가 만드는 모든 Trace Dataset은 이 스키마를 따른다.
용어는 [`GLOSSARY.md`](GLOSSARY.md) 를 정본으로 하며, 여기서 쓰는 *Dataset*·*Record*·
*Attributes*·*Metadata*·*Trace* 는 전부 그 문서의 OPTIMIST 정의다.

---

## 0. 이 스키마의 지위

**부채널 분야에는 공표된 표준 데이터셋 스키마가 없다.** OPTIMIST 는 용어와 파일 포맷
평가 기준을 정의했지만 **구체적인 필드명이나 레이아웃은 정의하지 않았고**, ISO/IEC 17825
는 시험 방법을 규정할 뿐 데이터 저장 형식을 다루지 않는다.

따라서 아래 레이아웃과 필드명은 **이 저장소가 정한 것**이다. 표준으로 인용하면 안 된다.
표준에서 온 것은 용어와 "무엇을 기록해야 하는가" 라는 요구뿐이고, "어떤 이름으로 어디에
적을 것인가" 는 우리가 정했다.

| 이 스키마의 근거 | 출처 |
|---|---|
| 데이터 모델(Dataset/Record/Attributes/Metadata/Trace) | OPTIMIST 용어 |
| 포맷 선택 기준 | OPTIMIST 평가 기준 16개 |
| 어떤 메타데이터가 있어야 하는가 | ISO/IEC 17825:2024 Annex B·7.3, OPTIMIST Metadata 정의 |
| 필드 이름·레이아웃·필수 여부 | **이 문서 (프로젝트 정의)** |

`schema_version` 은 이 문서의 판번호다. 현재 **1.3**.

> **1.1 은 필드를 더하기만 했다.** 기존 1.0 데이터셋은 그대로 유효하며, 검증기는
> 파일에 적힌 판번호의 규칙으로 검사한다. 나중에 만든 규칙으로 옛 파일을 소급
> 위반 처리하면 "부분 준수" 라는 판정의 뜻이 무너지기 때문이다.
>
> 1.1 이 더한 것: 물리 측정이 아닌 채널(`emulated-power`·`debug-trace`), 샘플 축의
> 정체(`sample_axis`), 샘플 → 명령어 역매핑(`sample_map`), 레코드별 실행시간
> (`exec_time`), 그리고 ISO/IEC 17825 요건을 **판정할 수 있게 하는** 측정 조건 몇 가지.
>
> 1.2가 더한 것: Level 3의 같은 입력 10회 평균을 검증할 수 있도록 실물 전력 Dataset에
> 평균 전 `trace_repeats`·`exec_time_repeats`와 masked IUT의 실제 `mask_repeats`를
> 보존한다. 명목 대역폭과 교정 실측값, 공장 션트값과 최대값 검증도 Metadata로 구분한다.
>
> 1.3이 바꾼 것: Execution 한 번을 Record 한 행으로 저장하는 `raw-acquisition`과,
> 완성된 반복 묶음을 전처리·평균한 `derived-analysis`를 분리한다. 1.3 원본에는 평균값이
> 없고 `repeat_group_id`·`repeat_index`로 같은 입력 10회를 묶는다. 1.2의 3차원 반복 배열은
> 기존 파일에서만 유지하며 1.3 파일에는 사용하지 않는다.

---

## 1. 왜 HDF5 인가

OPTIMIST 평가 기준으로 후보를 견줬다. 우리 조건은 **단일 파일 10 GB 이상**,
**부분 로드가 잦음**(POI 창 수십 열만 읽는 일이 대부분), **메타데이터를 데이터와 한 파일에**.

| 기준 | HDF5 | Numpy(.npy) | TRS | Zarr |
|---|---|---|---|---|
| Open | ○ | ○ | ○ | ○ |
| 메타데이터 내장 | **○** | ✕ (별도 파일 필요) | ○ | ○ |
| Chunking / 부분 로드 | **○** | ✕ (전체 로드) | △ | ○ |
| Scalability (10 GB+) | ○ | △ | ○ | ○ |
| Support (도구 수) | **○** (SCARED·LASCAR 등) | ○ | △ (Riscure 계열) | △ |
| Simplicity | ○ | ◎ | △ | ○ |
| 단일 파일 | ○ | ✕ | ○ | ✕ (디렉터리) |

Zarr 도 요건을 만족하지만 산출물이 디렉터리라 배포·이동이 번거롭고, 이 저장소가 이미
`h5py` 로 수집·분석 경로를 갖추고 있다. **HDF5 를 쓴다.**

> 다른 포맷으로 내보낼 일이 생기면 이 스키마의 논리 구조(§2)를 유지한 채 매핑한다.
> 논리 구조와 저장 포맷은 분리되어 있다.

---

## 2. 레이아웃

```text
<name>.h5                          ← Dataset 한 벌 = Target 1개 × Channel 1개
 │
 ├─ HDF5 attrs                     ← Metadata(메타데이터) (§3)
 ├─ sample_map  (ns, 3)            ← 샘플 → 명령어 역매핑 [1.1, 명령어 축이면 필수] §3.9
 │
 └─ /<subset>/                     ← Subset: 수집 규약이 같은 Record 묶음
      ├─ HDF5 attrs                ← Subset metadata(서브셋 메타데이터) (§4)
      ├─ trace       (n, ns)       ← Trace          [필수]
      ├─ key         (n, kb)       ← Attribute      [필수]
      ├─ plaintext   (n, pb)       ← Attribute      [필수]
      ├─ ciphertext  (n, cb)       ← Attribute      [선택]
      ├─ mask        (n, mb)       ← Attribute      [선택, 대책 난수]
      ├─ exec_time   (n,)          ← Attribute      [1.1, 선택] §4.2
      ├─ trace_repeats (n, r, ns)  ← 평균 전 원 파형 [1.2 power 필수]
      ├─ exec_time_repeats (n, r)  ← 반복별 트리거 길이 [1.2 power 필수]
      ├─ mask_repeats (n, r, 10)   ← 반복별 실제 마스크 [1.2 masked 선택]
      ├─ repeat_group_id (n,)      ← 같은 입력 Execution 묶음 [1.3]
      └─ repeat_index (n,)         ← 묶음 안 실행 순번 [1.3 raw]
```

**행 정렬 규칙:** 한 Subset 안의 모든 배열은 **행 수 n 이 같고, i 번째 행이 같은 Execution
에 대응**한다. 이 규칙이 깨지면 데이터셋 전체가 무효다. 검증기가 가장 먼저 보는 항목이다.

`sample_map` 만 예외로 **루트에 둔다.** 이것은 레코드가 아니라 **샘플 축**을 설명하는
배열이라 행 수가 n 이 아니라 ns 이고, 한 파일의 모든 subset 이 같은 값을 공유하기 때문이다.

한 파일에 **Target 이나 Channel 이 다른 데이터를 섞지 않는다.** 파형 길이·측정 조건이
달라 Metadata 를 파일 단위로 적을 수 없게 되기 때문이다. 다르면 파일을 나눈다.

### 2.1 용어가 저장 위치와 엇갈리는 점 (중요)

| 논리 (GLOSSARY) | HDF5 저장 위치 |
|---|---|
| **Attributes** (trace/key/plaintext/…) | **HDF5 dataset(배열)** |
| **Metadata** | **HDF5 attrs** |

이름이 서로 반대로 걸린다. `GLOSSARY.md` §6.1 을 읽고 문서·주석에서 반드시 구분해 적는다.

---

## 3. Metadata(메타데이터) — 루트 HDF5 attrs

필드마다 **왜 필요한지** 근거를 단다. 근거를 댈 수 없는 필드는 넣지 않는다.

### 3.1 스키마 식별 [필수]

| 필드 | 타입 | 뜻 | 근거 |
|---|---|---|---|
| `schema` | str | 고정값 `"sca-hdf5"` | 파일만 보고 규약을 알 수 있어야 한다 |
| `schema_version` | str | 예 `"1.0"` | OPTIMIST: Backward Compatibility·Extensibility |

### 3.2 Target(타겟) / IUT [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `target_name` | str | 측정 보드 식별자. 예 `"CW308_STM32F3"` |
| `target_device` | str | 피측정 칩. 예 `"STM32F303"` |
| `target_clock_hz` | float | 타겟 동작 클럭 |
| `iut_algorithm` | str | 알고리즘. 예 `"AES-128-ECB"` |
| `iut_implementation` | str | 구현 식별자. 예 `"tiny-AES-c"` |
| `iut_countermeasure` | str | 대책. 없으면 `"none"` |

선택: `iut_version` (구현 버전·커밋).

> 근거 — ISO/IEC 17825 7.3.3 은 시험 기관이 벤더에게 IUT 정보를 받도록 요구한다.
> OPTIMIST 의 Metadata 정의도 device type·algorithm·implementation version·countermeasures
> 를 명시한다. **`iut_countermeasure` 를 `"none"` 이라도 반드시 적는다** — 비워 두면
> "대책이 없음" 과 "기록하지 않음" 을 구분할 수 없다.

### 3.3 Channel(채널) [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `channel_type` | str | 아래 목록 중 하나 |
| `channel_probe` | str | 프로브·션트 구성. 예 `"CW308 SHUNTL, 내장 션트"`. 물리 측정이 아니면 그 사실을 적는다 |

| `channel_type` | 뜻 | 판번호 |
|---|---|---|
| `power` | 전력 소비 | 1.0 |
| `em` | 전자파 방사 | 1.0 |
| **`emulated-power`** | 에뮬레이터가 **계산한** 누설 추정치 | 1.1 |
| **`debug-trace`** | CoreSight 등 디버그 트레이스 이벤트 | 1.1 |

선택: `channel_gain_db`(증폭기 게인), `shunt_ohm`·`shunt_selection_note`(§3.10).

> 근거 — ISO/IEC 17825 는 PA(3.8)와 EMA(3.6)를 다른 공격 클래스로 나눈다. Annex B.5 는
> 전력이면 션트 저항, 전자파면 근접 자기장 프로브를 요구하므로 프로브 구성이 측정의 일부다.

> **`emulated-power` 는 OPTIMIST 의 Channel 정의(물리량의 측정)에서 벗어난다.**
> 그 값은 측정치가 아니라 **누설 모델의 출력**이다. 그럼에도 같은 스키마에 담는 이유는,
> 세 관측(전력·디버그 트레이스·에뮬레이션)이 한 분석기·한 검증기를 통과해야 서로 나란히
> 놓고 볼 수 있기 때문이다. 대신 **모델을 반드시 밝히게** 했다(§3.9) — 모델을 모르면
> "안 샌다" 가 무슨 뜻인지 알 수 없다. 이 확장은 표준이 아니라 **이 저장소가 정한 것**이며,
> 용어상의 어긋남은 `GLOSSARY.md` 의 Channel 항목에 적어 두었다.

### 3.4 측정 [필수]

| 필드 | 타입 | 뜻 | 필수 조건 |
|---|---|---|---|
| `samples_per_trace` | int | `trace` 의 열 수 (= ns) | 항상 |
| `sample_dtype` | str | `trace` 의 dtype. 예 `"int16"` | 항상 |
| `sample_scale` | float | 정규화 나눗수 (§5.2) | 항상 |
| **`sample_axis`** | str | `"time"` \| `"instruction"` — 샘플 축이 무엇인가 | **1.1 부터 항상** |
| `sample_rate_hz` | float | 샘플링 속도 | `sample_axis="time"` 일 때 |
| `sample_resolution_bits` | int | ADC 유효 분해능 | `sample_axis="time"` 일 때 |
| `bandwidth_hz` | float | 측정 또는 명목 대역폭 | **1.1: `channel_type="power"` 일 때** |

선택: `synchronous_sampling`(bool).

> **`sample_axis` 를 왜 새로 두는가.** 에뮬레이션 트레이스에는 **`sample_rate_hz` 가
> 존재하지 않는다.** 축이 시간이 아니라 명령어 순번이기 때문이다. 그렇다고 아무 값이나
> 채우면 §5.3 을 어긴다. 그래서 "이 축이 무엇인지" 를 명시하게 하고, 시간축일 때만
> 속도·분해능을 요구한다. 읽는 쪽은 이 필드를 보고 x 축의 단위를 판단한다.
>
> 1.0 파일에는 이 필드가 없다. 그 파일들은 전부 시간축이므로 읽는 쪽이 `"time"` 으로
> 간주해도 되지만, **검증기는 1.0 파일에 이 필드를 요구하지 않는다.**

> **`bandwidth_hz` 를 1.1 에서 필수로 올린 이유.** ISO/IEC 17825 Annex B.2 가 대역폭을
> 클럭의 50 %(SW) 이상으로, 샘플레이트를 대역폭의 5배로 요구한다. 대역폭을 적지 않으면
> 그 요건을 **만족하는지 판정할 수 없다** — 데이터가 좋고 나쁨을 떠나 판정 자체가 불가능해진다.
> 다만 값을 모를 때는 여전히 비워 둔다(§5.3). 그러면 검증기가 "미기록" 으로 보고하고,
> 요건 대조표에도 "판정 불가" 로 남는다. 지어낸 값보다 낫다.

> 근거 — **ISO/IEC 17825 Annex B.2·B.3** 이 대역폭(SW 는 클럭의 50% 이상)·샘플레이트
> (대역폭의 5배)·분해능(8 bit 이상)을 요구한다. 이 값들이 없으면 데이터셋이 그 요건을
> 만족하는지 **판정할 수 없다.** `synchronous_sampling` 은 타겟 클럭에 동기 샘플링했는지로,
> Annex B.1 이 "동기 샘플링이면 훨씬 낮은 샘플레이트로도 유효하다" 고 적은 예외에 해당한다.

### 3.5 Trigger(트리거) [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `trigger_source` | str | 트리거 채널. 예 `"userio_d0"` |
| `trigger_semantics` | str | 트리거가 감싸는 구간을 사람이 읽을 문장 |

선택: `trigger_samples` (트리거 하이 구간의 실측 샘플 수).

> 근거 — OPTIMIST 는 Trigger 를 "Target 의 특정 연산과 측정을 동기화하는 Channel" 로
> 정의한다. ISO 7.3.6 은 트리거 제공이 정렬의 전제라고 적는다.
> **`trigger_semantics` 가 중요하다** — 트리거가 암호 연산만 감싸는지, 키 스케줄까지
> 포함하는지에 따라 분석 결과의 해석이 완전히 달라진다.

### 3.6 정렬 [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `alignment` | str | `"none"` \| `"static"` \| `"dynamic"` |

`"none"` 은 정렬을 하지 않았다는 뜻이다(트리거 동기만으로 정렬된 경우 포함).

> 근거 — **ISO/IEC 17825 A.2.6·A.3.6** 에서 정렬 여부가 합/부 판정을 직접 바꾼다.
> 저장된 트레이스가 원본인지 후처리본인지 모르면 그 판정을 재현할 수 없다.

### 3.7 이력 [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `acquisition_start` | str | ISO 8601. 예 `"2026-08-09T00:31:01"` |
| `tool_chain` | str | 수집 도구·버전. 예 `"chipwhisperer 6.0.0; python 3.12.13"` |

선택: `acquisition_seconds`, `rng_seed`, `recoveries`(수집 중 자동 복구 이력).

> 근거 — OPTIMIST 의 Reproducibility·Dataset Integrity. 언제 무엇으로 받았는지 모르면
> 재현이 불가능하고, 이상값이 나왔을 때 데이터 탓인지 분석 탓인지 가릴 수 없다.

### 3.8 확장 필드 [선택]

스키마가 요구하지 않지만 이 저장소가 쓰는 필드다. **읽는 쪽은 모르는 필드를 무시해야
한다**(§5.4). 여기 적어 두는 이유는 §6 검증기가 "문서에 없는 필드" 를 만들지 않게 하기
위함이다 — 코드가 쓰는 필드는 전부 문서에 있어야 한다.

| 필드 | 타입 | 뜻 |
|---|---|---|
| `schema_note` | str | 준수와 관련해 사람이 읽어야 할 사정. **부분 준수 파일은 이 필드로 이유를 남긴다** |
| `fixed_key` | uint8[] | 이 데이터셋에서 "고정" 으로 쓴 키. 교육용 채점 기준 |
| `fixed_pt` | uint8[] | 교육용 분석에서 정답 대조에 쓰는 고정 평문 |
| `recoveries` | str[] | 수집 중 자동 복구가 일어난 이력 |

`fixed_key`·`fixed_pt` 는 **평가용 정답**이라 실제 시험 데이터셋이라면 넣지 않는다.
이 저장소는 교육용이므로 채점을 위해 남긴다.

### 3.9 에뮬레이션 [1.1, `channel_type="emulated-power"` 일 때 필수]

에뮬레이션 트레이스의 값은 **측정치가 아니라 누설 모델의 출력**이다. 모델과 빌드를 모르면
"샌다/안 샌다" 가 무슨 뜻인지 알 수 없고 재현도 불가능하므로, 다음을 전부 요구한다.

| 필드 | 타입 | 뜻 |
|---|---|---|
| `leakage_model` | str | 예 `"concat(HW(reg), HD(reg,same), HW(mem), HD(mem,same))"` |
| `leakage_segments` | str | 성분별 샘플 구간. 예 `"hw_reg:0-6051,hd_reg:6051-12102,…"` |
| `emulator` | str | 예 `"unicorn 2.1.4"` |
| `instruction_set` | str | 예 `"ARMv7-M Thumb"` |
| `build_flags` | str | 컴파일·링크 플래그 전문 |
| `binary_sha256` | str | 에뮬레이션한 ELF 의 SHA-256 |
| `window_symbols` | str | 관측 구간 안 주요 심볼의 주소. 예 `"AES_init_ctx:0x822d,AES_ECB_encrypt:0x8299"` |

> **`window_symbols` 가 왜 필요한가.** 분석은 구간을 더 잘게 나눠야 할 때가 있다 —
> 예를 들어 키 스케줄이 끝나고 암호화가 시작되는 지점. 그 경계를 ELF 를 다시 열어
> 찾게 하면 **데이터셋만으로는 분석할 수 없게 된다.** 심볼 주소를 여기 적어 두면
> `sample_map` 의 주소 열에서 그 지점의 명령어 인덱스를 바로 찾을 수 있다.

> **`build_flags` 를 왜 필수로 두는가.** 최적화 수준이 전이 누설을 **만들기도 하고 없애기도
> 한다.** 같은 C 소스라도 `-Os` 와 `-O2` 는 레지스터 할당과 명령어 선택이 달라 서로 다른
> 구현이 된다. 이 값이 없으면 결과를 재현할 수 없고, 실측 타겟과 같은 것을 봤는지도 알 수 없다.

> **HD 는 같은 저장소의 앞뒤 값끼리만 계산한다** — `HD(R2_before, R2_after)`.
> 서로 다른 레지스터 쌍(`HD(R2_before, R5_after)`)은 실제 하드웨어에서 전이 누설이
> 생기는 방식이 아니고, 조합이 폭발해 오탐만 만든다. 모델 문자열에 `same` 을 적어 이
> 규약을 명시한다.

### 3.10 실행시간·전처리·프로브 [1.1, 선택; 1.2 power 조건부 필수]

ISO/IEC 17825 의 요건을 **판정 가능하게** 만드는 값들이다. 없으면 위반이 아니라
"판정 불가(미기록)" 로 보고된다.

| 필드 | 타입 | 뜻 | 관련 요건 |
|---|---|---|---|
| `exec_time_unit` | str | `"instruction"` \| `"adc_sample"` \| `"trace_tick"` | §7.3.4 타이밍 분석 |
| `exec_time_epsilon` | float | 같다고 볼 허용 오차 ε (클럭 1사이클에 해당하는 값) | 판정이 `\|T1−T2\| < ε` 이다 |
| `preprocessing_average_n` | int | 트레이스 1장에 평균한 실행 횟수 (기본 1) | A.2.5 전처리 |
| `shunt_ohm` | float | VCC–IUT 사이 저항값 | Annex B.5 |
| `shunt_selection_note` | str | 그 값을 고른 근거 | Annex B.6 (동작 가능한 최대값) |
| `bandwidth_basis` | str | 대역폭 출처와 측정/명목 구분 | Annex B 판정 근거 |
| `bandwidth_is_nominal` | bool | 교정 실측값이 아닌 공식 부품 명목값인가 | 오인 방지 |
| `shunt_max_verified` | bool | 더 큰 저항과 비교해 동작 가능한 최대값을 확인했는가 | Annex B.6 |
| `platform`·`adc_mul` | str·int | 실제 펌웨어 플랫폼과 동기 ADC 배수 | 재현 조건 |
| `firmware_sha256` | str | 실행한 IUT 펌웨어 ELF의 SHA-256 | 빌드 동일성 |

> `exec_time` 배열(§4.2)만 있고 `exec_time_unit` 이 없으면 그 숫자가 무엇의 개수인지
> 알 수 없다. 단위 없는 물리량 필드는 금지다(§5.1).

### 3.11 원본과 파생 역할 [1.3 필수]

`dataset_role`은 다음 둘 중 하나다.

| 역할 | 필수 Metadata | 의미 |
|---|---|---|
| `raw-acquisition` | `capture_repeats`, `capture_contract_sha256`, `acquisition_status="complete"` | 장비·에뮬레이터가 만든 Execution별 불변 원본 |
| `derived-analysis` | `source_dataset_sha256`, `source_capture_contract_sha256`, `derivation_contract_sha256`, `aggregation_kind="mean"`, `aggregation_n`, `preprocessing_pipeline` | 원본에서 재생성 가능한 분석 입력 |

원본의 `capture_contract_sha256`은 수집 전에 고정한 resolved spec, 실제 IUT 바이너리와
수집 설정의 정규화 JSON을 해시한 값이다. 파생 계약은 원본 SHA-256, 전처리 설정과 구현
버전을 포함한다. 경로나 파일 시각은 계약의 정본이 아니며 hash와 manifest가 정본이다.

---

## 4. Subset metadata(서브셋 메타데이터) — 그룹 HDF5 attrs

| 필드 | 타입 | 필수 | 뜻 |
|---|---|---|---|
| `role` | str | ✔ | §4.1 의 값 중 하나 |
| `n_records` | int | ✔ | 레코드 수 (= 모든 배열의 행 수) |
| `key_mode` | str | ✔ | `"fixed"` \| `"random"` |
| `pt_mode` | str | ✔ | `"fixed"` \| `"random"` |
| `seconds` | float | | 이 subset 수집에 걸린 시간 |
| `mask_seeds` | uint32[] | | 대책 난수 시드 이력 (해당 시) |
| `spa_pair_kind` | str | | 1.1 — `"same-data"` \| `"different-data-fixed"` \| `"different-data-random"` |

### 4.1 `role` 값

| 값 | 뜻 | 판번호 |
|---|---|---|
| `exploration` | 누설 위치·측정 조건 탐색용 | 1.0 |
| `profiling` | 누설 모델 학습용 (키를 안다) | 1.0 |
| `attack` | 키 복구 평가용 (키 고정) | 1.0 |
| `leakage-detection-fixed` | 누설 검출의 고정 입력 집단 | 1.0 |
| `leakage-detection-random` | 누설 검출의 랜덤 입력 집단 | 1.0 |
| **`timing`** | 실행시간 측정 블록 (ISO/IEC 17825 A.2.4) | 1.1 |
| **`simple-analysis`** | 소수 파형의 육안·통계 비교용 쌍 (A.2.2) | 1.1 |

Subset **이름은 자유**지만 `role` 은 이 목록에서 고른다. 프로젝트마다 이름이 달라도
역할로 서로를 알아볼 수 있게 하기 위함이다.

> `role` 이 OPTIMIST 의 *Splitting*(train/valid/test)과 다른 이유는
> `GLOSSARY.md` §5 의 **Subset** 항목에 적어 두었다.

### 4.2 `exec_time` [1.1, 선택]

`exec_time (n,)` 은 **레코드마다의 실행시간**이다. 단위는 루트의 `exec_time_unit` 이 정한다
(§3.10).

| 채널 | 무엇을 재나 |
|---|---|
| `power` | 트리거 하이 구간의 샘플 수 |
| `debug-trace` | 대상 함수 진입~복귀 타임스탬프 차 |
| `emulated-power` | 대상 구간의 명령어 수 |

> **분석 때 만들 수 없는 값이라 수집 때 남겨야 한다.** 트레이스만 저장하고 이 값을 빠뜨리면
> 나중에 타이밍 분석을 하려 해도 **사후 산출이 불가능**하다 — 트레이스는 잘려 있고 트리거
> 구간의 원래 길이는 이미 사라졌기 때문이다. ISO/IEC 17825 A.2.4 는 타이밍 측정 수집을
> Annex A 에서 유일하게 `shall collect` 로 요구한다.

### 4.3 반복 배열 [1.2, 실물 전력]

`r = preprocessing_average_n`이다. `trace`는 `trace_repeats`의 축 1 평균을 반올림한
`int16`, `exec_time`은 `exec_time_repeats`의 평균을 반올림한 `uint32`여야 한다. 논리
레코드는 r회가 모두 성공한 뒤에만 모든 배열에 같은 행으로 추가한다. masked IUT는 각
반복 뒤 트리거 밖에서 실제 회수한 10바이트를 `mask_repeats`에 저장한다. 검증기는 대표값의
평균 일치와 형상을 확인하므로 불완전 평균이나 행 어긋남이 분석으로 넘어갈 수 없다.

### 4.4 실행별 원본과 파생 평균 [1.3]

1.3 원본은 Execution 한 번을 `trace` 한 행으로 저장한다. 같은 key·plaintext·ciphertext의
`capture_repeats`회는 `repeat_group_id`가 같고 `repeat_index`가 0부터 연속이어야 한다.
묶음 전체가 성공한 뒤에만 모든 배열에 행을 추가한다. `mask`와 `exec_time`도 Execution별
한 행이며 서로 다른 마스크는 정상이다.

1.3 파생은 완성된 묶음마다 `trace` 한 행을 저장한다. dtype은 `float64`이고 원본의
`sample_scale`로 정규화한 각 실행을 평균한다. 원본 묶음의 식별자는 `repeat_group_id`로
보존한다. `repeat_index`와 평균 실행시간은 저장하지 않는다.
TA는 파생값이 아니라 원본의 Execution별 `exec_time`을 사용한다.
1.2의 `trace_repeats`·`exec_time_repeats`·`mask_repeats`는 어느 1.3 역할에도 저장하지 않는다.

> 에뮬레이션의 `exec_time` 은 **명령어 수이지 사이클 수가 아니다.** Unicorn 에는 사이클
> 모델이 없다(확인: `Uc` 에 사이클 카운터 API 없음). 명령어 수가 **다르면** 데이터 의존
> 제어흐름이라는 확정 소견이지만, **같아도 constant-time 을 증명하지는 못한다.**
> 그 확정은 실물 `trig_count` 나 디버그 트레이스의 몫이다.

---

## 5. 규약

### 5.1 이름과 단위

- 필드명은 **영문 snake_case**.
- 물리량은 **단위를 접미사로 못박는다** — `_hz` `_db` `_bits` `_seconds`.
  단위 없는 물리량 필드는 금지한다.
- 불리언은 `bool`, 열거형은 소문자 문자열.

### 5.2 `trace` 의 값과 `sample_scale`

`trace` 는 정수형(`int16` 등) 또는 부동소수점(`float32`, `float64`)을 허용한다.

- **정수형이면 `sample_scale` 이 필수다.** 정규화 값 = `trace / sample_scale`.
- 부동소수점이면 `sample_scale = 1.0` 으로 적는다.

정규화 값의 **물리 단위(V 등)는 알 수 있을 때만** 적는다. 션트 저항·증폭기 이득·ADC 기준
전압을 모두 알아야 전압으로 환산할 수 있는데, 대개 그중 일부를 모른다.
**모르면 단위를 적지 않는다. 꾸며 넣지 않는다.**

### 5.3 모르는 값

**추정치로 채우지 않는다.** 필수 필드를 채울 수 없으면 그 데이터셋은 **부분 준수**이며,
검증기가 무엇이 빠졌는지 보고한다. 잘못된 메타데이터는 없는 것보다 나쁘다 — 다음 사람이
그 값을 믿고 판단하기 때문이다.

### 5.4 확장과 판번호

- 필드 **추가**는 자유다. 기존 필드의 **의미를 바꾸면** `schema_version` 을 올린다.
- 읽는 쪽은 모르는 필드를 무시해야 한다(전방 호환).

### 5.5 저장 파라미터

- `trace` 는 **행 방향 청킹**한다(레코드 단위 접근이 지배적이므로).
- 수집 중 확장을 위해 `maxshape=(None, ns)` 로 만든다.
- 압축은 선택이다. 트레이스는 압축률이 낮아 대개 얻는 것이 적다.

---

## 6. 검증

**`workspace/lib/sca_schema.py` 의 `validate_dataset(path=…)` 이 이 문서를 코드로 옮긴 것이다.**
저장소 공용 트리에 있는 이유는 출처가 다른 관측 Dataset이 **같은 검증기**를 통과해야
"준수"의 뜻이 하나로 유지되기 때문이다. 검증기가 프로젝트마다 따로
있으면 준수 여부도 프로젝트마다 달라진다.

`[extra] SCALib/scalib_common.py` 는 이것을 재노출하므로 그 프로젝트의 노트북은
종전대로 `validate_dataset(target=…)` 를 쓸 수 있다.

검사 항목:

1. `schema` · `schema_version` 존재, 판번호가 아는 값인가
2. §3 의 필수 Metadata 존재 — **파일에 적힌 판번호의 규칙으로** 검사한다
3. `channel_type` 이 허용 목록 안 (§3.3)
4. 1.1 이상: `sample_axis` 존재·허용 목록 안, 축에 따른 조건부 필수 (§3.4)
5. 1.1: `sample_axis="instruction"` 이면 §3.9 의 에뮬레이션 필드와 루트 `sample_map` 존재
6. 1.1: `channel_type="power"` 이면 `bandwidth_hz` 존재
7. 1.2 power: 반복 배열·실측/명목 구분 Metadata와 평균 일치
8. 1.3: Dataset 역할별 provenance와 원본 반복 묶음 또는 파생 평균 계약
9. Subset 마다 §4 의 필수 항목 존재, `role` 이 허용 목록 안
10. `trace` · `key` · `plaintext` 존재
11. **행 정렬** — 한 subset 안 모든 배열의 행 수 일치, `n_records` 와도 일치
12. `sample_dtype` · `samples_per_trace` 가 실제 `trace` 와 일치
13. 정수형 `trace` 인데 `sample_scale` 이 없으면 위반

위반 목록을 돌려주며, 비어 있으면 준수다. **수집 직후와 분석 시작 시** 호출한다.

> **이전 판 파일에 1.3 규칙을 적용하지 않는다.** 나중에 만든 규칙으로 옛 파일을 소급
> 위반 처리하면, "부분 준수" 가 *데이터가 부실하다* 는 뜻인지 *스키마가 나중에 바뀌었다* 는
> 뜻인지 구분할 수 없게 된다. 판번호는 그 구분을 위해 있다.

---

## 7. Dataset 생성 경로와 Git 추적 정책

| 경로 | 판번호 | Git 추적 상태 | 생성 후 확인할 조건 |
|---|---|---|---|
| `workspace/[extra] SCALib/traces/scalib_dataset_tiny-AES-c.h5` | 1.0 | `*.h5` 제외 — clone에 포함되지 않음 | 수집 노트북 완료 후 검증기 통과 |
| `workspace/[extra] SCALib/traces/scalib_dataset_masked-aes-c.h5` | 1.0 | `*.h5` 제외 — clone에 포함되지 않음 | `mask` 포함, 수집 노트북 완료 후 검증기 통과 |
| `workspace/traces/20260825_220525_SCA_DB.h5` | 1.0 | 파일 있음 | 1.0 규칙으로 검증기 통과 |
| `workspace/[extra] Physical-AI-SCA/traces/*.h5` | 1.1 | `*.h5` 제외 — clone에 포함되지 않음 | 에뮬레이션이면 `sample_map`·`exec_time` 포함 후 검증기 통과 |

생성 대상 경로가 있다는 사실과 특정 작업 디렉터리에 파일이 존재한다는 사실은 다르다.
위 제외 대상은 로컬에 있을 수도 없을 수도 있으므로 정적 문서에서 존재 여부를 고정하지
않는다. 노트북의 과거 실행 출력만 보고 준수를 주장하지 않으며, 실제 파일을 확인하고
`workspace/lib/sca_schema.py`의 검증기를 통과한 결과만 현재 상태로 보고한다.

> **1.0 Dataset이 1.1의 새 필드를 갖추지 못한 것은 위반이 아니다.** 그 파일들은 1.0
> Dataset이고 1.0을 완전히 지킨다. 다만 ISO/IEC 17825 요건을 판정하려면 1.1이 요구하는
> 값(`bandwidth_hz`·`exec_time`·`shunt_ohm` 등)이 필요하므로, **요건 대조표에서는
> "미기록 → 판정 불가"** 로 보고된다. 스키마 준수와 시험 요건 충족은 다른 축이다.

---

## 8. 구 스키마 → 현 스키마 매핑

이 저장소가 예전에 쓰던 이름과의 대응이다. 옛 파일을 만나면 이 표로 옮긴다.

| 구 | 현 | 위치 |
|---|---|---|
| `i_k` | `key` | HDF5 배열 |
| `i_p` | `plaintext` | HDF5 배열 |
| `o` | `ciphertext` | HDF5 배열 |
| `t` | `trace` | HDF5 배열 |
| `i_m` | `mask` | HDF5 배열 |
| `ns` | `samples_per_trace` | 루트 HDF5 attrs |
| `trig_count` | `trigger_samples` | 루트 HDF5 attrs |
| `adc_freq` | `sample_rate_hz` | 루트 HDF5 attrs |
| `clk_hz` | `target_clock_hz` | 루트 HDF5 attrs |
| `gain_db` | `channel_gain_db` | 루트 HDF5 attrs |
| `trace_scale` | `sample_scale` | 루트 HDF5 attrs |
| `platform` | `target_name` | 루트 HDF5 attrs |
| `cipher` | `iut_algorithm` + `iut_implementation` | 루트 HDF5 attrs |
| `created` | `acquisition_start` | 루트 HDF5 attrs |
| `seed` | `rng_seed` | 루트 HDF5 attrs |
| `python`·`numpy`·`chipwhisperer` | `tool_chain` (한 문자열로 합침) | 루트 attrs |
| `n_traces` | `n_records` | subset attrs |
| (없음) | `role` | subset attrs — 새로 부여 |
| `adc_mul` | (삭제) | `sample_rate_hz` 와 `target_clock_hz` 로 유도 가능 |
| `masks_exported`·`mask_len` | (삭제) | `mask` 배열의 존재·shape 로 알 수 있다 |
| `fixed_key`·`fixed_pt` | 유지 | 이 저장소 고유. 교육용 채점 기준 |

---

## 9. 출처와 근거

- 용어: [`GLOSSARY.md`](GLOSSARY.md)
- OPTIMIST *File Format for Traces: Requirements and Glossary* v0.5 — <https://optimist-ose.org/docs/file-format/intro>
- ISO/IEC 17825:2024 — <https://www.iso.org/standard/86616.html>
  (저작권 보호 문서라 저장소에 넣지 않는다. 로컬 사본은 `gitignore/` 에 둔다 — `GLOSSARY.md` §7 참고)
