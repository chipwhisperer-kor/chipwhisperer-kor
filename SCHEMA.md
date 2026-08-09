# SCHEMA — 부채널 신호 데이터셋 스키마

이 저장소가 만드는 모든 파형 데이터셋은 이 스키마를 따른다.
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

`schema_version` 은 이 문서의 판번호다. 현재 **1.0**.

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
 ├─ HDF5 attrs                     ← Metadata (§3)
 │
 └─ /<subset>/                     ← Subset: 수집 규약이 같은 Record 묶음
      ├─ HDF5 attrs                ← Subset Metadata (§4)
      ├─ trace       (n, ns)       ← Trace          [필수]
      ├─ key         (n, kb)       ← Attribute      [필수]
      ├─ plaintext   (n, pb)       ← Attribute      [필수]
      ├─ ciphertext  (n, cb)       ← Attribute      [선택]
      └─ mask        (n, mb)       ← Attribute      [선택, 대책 난수]
```

**행 정렬 규칙:** 한 Subset 안의 모든 배열은 **행 수 n 이 같고, i 번째 행이 같은 Execution
에 대응**한다. 이 규칙이 깨지면 데이터셋 전체가 무효다. 검증기가 가장 먼저 보는 항목이다.

한 파일에 **Target 이나 Channel 이 다른 데이터를 섞지 않는다.** 파형 길이·측정 조건이
달라 Metadata 를 파일 단위로 적을 수 없게 되기 때문이다. 다르면 파일을 나눈다.

### 2.1 용어가 저장 위치와 엇갈리는 점 (중요)

| 논리 (GLOSSARY) | HDF5 저장 위치 |
|---|---|
| **Attributes** (trace/key/plaintext/…) | **HDF5 dataset(배열)** |
| **Metadata** | **HDF5 attrs** |

이름이 서로 반대로 걸린다. `GLOSSARY.md` §6.1 을 읽고 문서·주석에서 반드시 구분해 적는다.

---

## 3. Metadata — 루트 HDF5 attrs

필드마다 **왜 필요한지** 근거를 단다. 근거를 댈 수 없는 필드는 넣지 않는다.

### 3.1 스키마 식별 [필수]

| 필드 | 타입 | 뜻 | 근거 |
|---|---|---|---|
| `schema` | str | 고정값 `"sca-hdf5"` | 파일만 보고 규약을 알 수 있어야 한다 |
| `schema_version` | str | 예 `"1.0"` | OPTIMIST: Backward Compatibility·Extensibility |

### 3.2 Target / IUT [필수]

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

### 3.3 Channel [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `channel_type` | str | `"power"` \| `"em"` |
| `channel_probe` | str | 프로브·션트 구성. 예 `"CW308 SHUNTL, 내장 션트"` |

선택: `channel_gain_db` (증폭기 게인).

> 근거 — ISO/IEC 17825 는 PA(3.8)와 EMA(3.6)를 다른 공격 클래스로 나눈다. Annex B.5 는
> 전력이면 션트 저항, 전자파면 근접 자기장 프로브를 요구하므로 프로브 구성이 측정의 일부다.

### 3.4 측정 [필수]

| 필드 | 타입 | 뜻 |
|---|---|---|
| `sample_rate_hz` | float | 샘플링 속도 |
| `sample_resolution_bits` | int | ADC 유효 분해능 |
| `samples_per_trace` | int | `trace` 의 열 수 (= ns) |
| `sample_dtype` | str | `trace` 의 dtype. 예 `"int16"` |
| `sample_scale` | float | 정규화 나눗수 (§5.2) |

선택: `bandwidth_hz`, `synchronous_sampling`(bool).

> 근거 — **ISO/IEC 17825 Annex B.2·B.3** 이 대역폭(SW 는 클럭의 50% 이상)·샘플레이트
> (대역폭의 5배)·분해능(8 bit 이상)을 요구한다. 이 값들이 없으면 데이터셋이 그 요건을
> 만족하는지 **판정할 수 없다.** `synchronous_sampling` 은 타겟 클럭에 동기 샘플링했는지로,
> Annex B.1 이 "동기 샘플링이면 훨씬 낮은 샘플레이트로도 유효하다" 고 적은 예외에 해당한다.

### 3.5 Trigger [필수]

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
> 저장된 파형이 원본인지 후처리본인지 모르면 그 판정을 재현할 수 없다.

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
| `fixed_pt` | uint8[] | 위와 같은 목적의 고정 평문 |
| `recoveries` | str[] | 수집 중 자동 복구가 일어난 이력 |

`fixed_key`·`fixed_pt` 는 **평가용 정답**이라 실제 시험 데이터셋이라면 넣지 않는다.
이 저장소는 교육용이므로 채점을 위해 남긴다.

---

## 4. Subset Metadata — 그룹 HDF5 attrs

| 필드 | 타입 | 필수 | 뜻 |
|---|---|---|---|
| `role` | str | ✔ | §4.1 의 값 중 하나 |
| `n_records` | int | ✔ | 레코드 수 (= 모든 배열의 행 수) |
| `key_mode` | str | ✔ | `"fixed"` \| `"random"` |
| `pt_mode` | str | ✔ | `"fixed"` \| `"random"` |
| `seconds` | float | | 이 subset 수집에 걸린 시간 |
| `mask_seeds` | uint32[] | | 대책 난수 시드 이력 (해당 시) |

### 4.1 `role` 값

| 값 | 뜻 |
|---|---|
| `exploration` | 누설 위치·측정 조건 탐색용 |
| `profiling` | 누설 모델 학습용 (키를 안다) |
| `attack` | 키 복구 평가용 (키 고정) |
| `leakage-detection-fixed` | 누설 검출의 고정 입력 집단 |
| `leakage-detection-random` | 누설 검출의 랜덤 입력 집단 |

Subset **이름은 자유**지만 `role` 은 이 목록에서 고른다. 프로젝트마다 이름이 달라도
역할로 서로를 알아볼 수 있게 하기 위함이다.

> `role` 이 OPTIMIST 의 *Splitting*(train/valid/test)과 다른 이유는
> `GLOSSARY.md` §5 의 **Subset** 항목에 적어 두었다.

---

## 5. 규약

### 5.1 이름과 단위

- 필드명은 **영문 snake_case**.
- 물리량은 **단위를 접미사로 못박는다** — `_hz` `_db` `_bits` `_seconds`.
  단위 없는 물리량 필드는 금지한다.
- 불리언은 `bool`, 열거형은 소문자 문자열.

### 5.2 `trace` 의 값과 `sample_scale`

`trace` 는 정수형(`int16` 등) 또는 부동소수점(`float32`)을 허용한다.

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
- 압축은 선택이다. 파형은 압축률이 낮아 대개 얻는 것이 적다.

---

## 6. 검증

`workspace/[extra] SCALib/scalib_common.py` 의 `validate_dataset()` 이 이 문서를 코드로
옮긴 것이다. 검사 항목:

1. `schema` · `schema_version` 존재
2. §3 의 필수 Metadata 존재
3. Subset 마다 §4 의 필수 항목 존재, `role` 이 허용 목록 안
4. `trace` · `key` · `plaintext` 존재
5. **행 정렬** — 한 subset 안 모든 배열의 행 수 일치, `n_records` 와도 일치
6. `sample_dtype` · `samples_per_trace` 가 실제 `trace` 와 일치
7. 정수형 `trace` 인데 `sample_scale` 이 없으면 위반

위반 목록을 돌려주며, 비어 있으면 준수다. **수집 직후와 분석 시작 시** 호출한다.

---

## 7. 이 저장소의 데이터셋

| 파일 | 준수 | 비고 |
|---|---|---|
| `workspace/[extra] SCALib/traces/scalib_dataset_tiny-AES-c.h5` | 완전 | 비마스킹 AES |
| `workspace/[extra] SCALib/traces/scalib_dataset_masked-aes-c.h5` | 완전 | 마스킹 AES, `mask` 포함 |
| `workspace/traces/*.h5` (튜토리얼 1강) | **부분** | §7.1 |

### 7.1 튜토리얼 데이터셋이 부분 준수인 이유

`workspace/traces/20260427_143337_SCA_DB.h5` 는 스키마를 세우기 전에 다른 사람이 받은
파일이다. 레이아웃과 필드명은 맞췄지만 **당시 기록되지 않은 측정 메타데이터는 복원할 수
없다** — 게인, 프로브 구성, 분해능 등. §5.3 대로 **추정해서 채우지 않고 비워 두었다.**

튜토리얼 수집 코드는 스키마를 따르도록 고쳤으므로, **앞으로 받는 파형은 완전 준수**다.

---

## 8. 구 스키마 → 현 스키마 매핑

이 저장소가 예전에 쓰던 이름과의 대응이다. 옛 파일을 만나면 이 표로 옮긴다.

| 구 | 현 | 위치 |
|---|---|---|
| `i_k` | `key` | HDF5 dataset |
| `i_p` | `plaintext` | HDF5 dataset |
| `o` | `ciphertext` | HDF5 dataset |
| `t` | `trace` | HDF5 dataset |
| `i_m` | `mask` | HDF5 dataset |
| `ns` | `samples_per_trace` | 루트 attrs |
| `trig_count` | `trigger_samples` | 루트 attrs |
| `adc_freq` | `sample_rate_hz` | 루트 attrs |
| `clk_hz` | `target_clock_hz` | 루트 attrs |
| `gain_db` | `channel_gain_db` | 루트 attrs |
| `trace_scale` | `sample_scale` | 루트 attrs |
| `platform` | `target_name` | 루트 attrs |
| `cipher` | `iut_algorithm` + `iut_implementation` | 루트 attrs |
| `created` | `acquisition_start` | 루트 attrs |
| `seed` | `rng_seed` | 루트 attrs |
| `python`·`numpy`·`chipwhisperer` | `tool_chain` (한 문자열로 합침) | 루트 attrs |
| `n_traces` | `n_records` | subset attrs |
| (없음) | `role` | subset attrs — 새로 부여 |
| `adc_mul` | (삭제) | `sample_rate_hz` 와 `target_clock_hz` 로 유도 가능 |
| `masks_exported`·`mask_len` | (삭제) | `mask` 배열의 존재·shape 로 알 수 있다 |
| `fixed_key`·`fixed_pt` | 유지 | 이 저장소 고유. 교육용 채점 기준 |

---

## 9. 참고

- 용어: [`GLOSSARY.md`](GLOSSARY.md)
- OPTIMIST *File Format for Traces: Requirements and Glossary* v0.5 — <https://optimist-ose.org/docs/file-format/intro>
- ISO/IEC 17825:2024 — <https://www.iso.org/standard/86616.html>
  (저작권 보호 문서라 저장소에 넣지 않는다. 로컬 사본은 `gitignore/` 에 둔다 — `GLOSSARY.md` §7 참고)
