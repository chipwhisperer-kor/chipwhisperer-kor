# GLOSSARY — 부채널 분석 용어 정본

이 저장소의 모든 문서·주석·설명·식별자는 이 파일의 용어를 따른다.
용어가 이 파일과 어긋나면 **이 파일이 정본**이다.

---

## 1. 이 문서의 규칙

### 1.1 표기

- 표제는 **`English(한글)`** 로 병기한다.
- **정의는 영문으로 쓴다.** 원본 표준의 뉘앙스가 번역에서 깎이지 않게 하기 위함이다.
- **두문자어(acronym)는 영문 원본을 쓴다.** `DPA`, `SNR`, `IUT` 를 한글로 풀지 않는다.
- 고유명사·전문용어로서 한국어 대응어가 없거나 억지스러운 것은 **음역(transliteration)** 한다.
  예: `Trace` → 트레이스 (○), 흔적 (×).
- 한글 표기는 잠정이다. 필요하면 한글 쪽만 고치고 영문 표제·정의는 건드리지 않는다.

### 1.2 파생 문서

이 파일에서 파생되는 문서·주석·설명은 **한글 위주로 작성**한다(독자가 한국인 연구자다).
다만 용어 자체는 이 파일의 표기를 그대로 쓰고, 코드 식별자는 영문 snake_case 를 쓴다.

### 1.3 출처 표기

각 항목 끝에 출처를 단다. **무엇이 표준이고 무엇이 우리가 정한 것인지 반드시 구분한다.**

| 표기 | 뜻 |
|---|---|
| `[OPTIMIST]` | OPTIMIST, *File Format for Traces: Requirements and Glossary*, v0.5 (2025-01-06) |
| `[ISO 17825 3.x]` | ISO/IEC 17825:2024, 해당 조항 |
| `[PROJECT]` | **표준 아님.** 이 저장소가 정한 용어 |

---

## 2. Data model terms (데이터 모델 용어) — OPTIMIST

측정 데이터의 구조를 기술하는 최소 어휘다. 스키마(`SCHEMA.md`)는 전부 이 용어 위에 세운다.

**Channel(채널)**
The source of a measurement of a physical value over time. `[OPTIMIST]`

> **이 저장소는 Channel 을 물리 측정 밖으로 넓혀 쓴다 — 표준 용어가 아니다.**
> OPTIMIST 의 정의는 *physical value* 를 *over time* 으로 측정한 것인데,
> `SCHEMA.md` 1.1 의 `channel_type` 에는 그 정의를 벗어나는 두 값이 있다.
>
> | 값 | 정의에서 벗어나는 점 |
> |---|---|
> | `emulated-power` | **측정이 아니다.** 에뮬레이터가 누설 모델(HW·HD)로 **계산한** 값이고, 축도 시간이 아니라 명령어 순번이다 |
> | `debug-trace` | 물리량이 아니라 프로세서가 **보고한 이벤트**다 |
>
> 왜 그렇게 하는가: 물리 측정, 계산된 누설 모델, 프로세서가 보고한 이벤트처럼 출처가 다른
> 산출물도 **같은 분석기와 같은 판정 기준**으로 읽을 수 있어야 "가장 약한 고리"를 찾을 수
> 있다. 그러려면 같은 스키마를 따라야 한다. 대신 값의 정체를 숨기지 않는다 — 에뮬레이션 채널은
> `leakage_model` 과 `sample_axis` 를 **필수로** 적게 해서, 읽는 사람이 그것을 측정치로
> 오해할 수 없게 했다(`SCHEMA.md` §3.3·§3.4·§3.9).
>
> 문서·주석에서 이 두 값을 가리킬 때는 "측정" 이 아니라 **"관측"** 또는 **"산출"** 이라고
> 적는다. OPTIMIST 의 Channel 을 인용하는 문맥에서는 원 정의를 그대로 쓴다.

**Trigger(트리거)**
A Channel used to synchronize measurements with specific operations in the Target. `[OPTIMIST]`

**Target(타겟)**
The object of side-channel leakage measurements. `[OPTIMIST]`

**Execution(실행)**
The activity of a target associated with a single trigger. `[OPTIMIST]`

**Noise(노이즈)**
Unwanted variations in measurements that can obscure the desired signal in a trace. `[OPTIMIST]`

- **Algorithmic noise(알고리즈믹 노이즈)** — Variations in the measured signal caused by the
  internal computations or processes of the device itself. This includes inherent randomness or
  variations due to the algorithm's design, state transitions, or other non-target data
  dependencies. `[OPTIMIST]`
- **Environment noise(환경 노이즈)** — External factors that introduce variability in the
  measurements, unrelated to the device's internal computations. This includes interference from
  the measurement setup, power supply noise, electromagnetic interference, or changes in the
  surrounding environment such as temperature drift. `[OPTIMIST]`

**Sample(샘플)**
A single measurement of a Channel corrupted by Noise. `[OPTIMIST]`

**Trace(트레이스)**
Vector corresponding to a sequence of measurements over time of a Channel during one Execution.
`[OPTIMIST]`

**Metadata(메타데이터)**
Metadata is used to provide context and supplementary information about trace sets, such as type
of device being analyzed, cryptographic algorithm being executed, version of the algorithm
implementation, sampling rate and resolution of the measurement equipment, environmental
conditions during data collection, applied countermeasures, date and time of data acquisition.
`[OPTIMIST]`

**Attributes(어트리뷰트)**
Attributes are named variables to store all data associated with a single execution, including the
Trace. Named variables that apply to a complete dataset are Metadata. `[OPTIMIST]`

> ⚠️ HDF5 의 "attribute" 와 뜻이 다르다. §6.1 을 반드시 읽는다.

**Record(레코드)**
The values of all attributes specific for one execution. `[OPTIMIST]`

**Dataset(데이터셋)**
Sequence of Records with the Attributes, along with Metadata. `[OPTIMIST]`

> ⚠️ HDF5 의 "dataset" 과 뜻이 다르다. §6.2 를 반드시 읽는다.

**File Format(파일 포맷)**
A file format describes how the data is stored on a filesystem. In side-channel analysis, file
formats are essential for managing, organizing, and processing large trace datasets and
accompanying metadata. `[OPTIMIST]`

**Compression(압축)**
A technique used to reduce the size of a file, which can be beneficial for storage, transmission,
and computation. `[OPTIMIST]`

**Alignment(정렬)**
The process of adjusting traces to account for variations in timing or other properties.
`[OPTIMIST]`

**Slicing(슬라이싱)**
Creating a new dataset as a subset of an existing Dataset. `[OPTIMIST]`

- **Record slicing(레코드 슬라이싱)** — taking a subset of the Records of the dataset. `[OPTIMIST]`
- **Vector/Trace slicing(트레이스 슬라이싱)** — taking a subset of the indices in the Vector
  associated to a Variable. `[OPTIMIST]`

**Indexing(인덱싱)**
Selecting a specific record, attribute and/or trace based on their position in the set, leading to
Record Index, Attribute Index and Trace Index. `[OPTIMIST]`

- **Fancy indexing(팬시 인덱싱)** — Indexing by means of an array or list of indices, allowing for
  non-contiguous or non-sequential selection of elements. `[OPTIMIST]`
- **Contiguous indexing(연속 인덱싱)** — Indexing corresponding to an integer interval of indices.
  `[OPTIMIST]`

**Splitting(스플리팅)**
Partitioning the records of a dataset for a specific purpose, such as for machine learning
experiments. `[OPTIMIST]`

- **Training split(트레이닝 스플릿)** — A partition of records used for model training. `[OPTIMIST]`
- **Validating split(밸리데이팅 스플릿)** — A partition of records used for model validation. `[OPTIMIST]`
- **Testing split(테스팅 스플릿)** — An exclusive partition of records used for model testing. `[OPTIMIST]`

**Chunking(청킹)**
Structuring the File Format to optimize for specific access patterns and to align with compression,
such that a selection of the data only requires decompression of selected chunks, as opposed to the
whole data set. `[OPTIMIST]`

---

## 3. File format evaluation criteria (파일 포맷 평가 기준) — OPTIMIST

파일 포맷을 고를 때 따지는 항목이다. `SCHEMA.md` 가 HDF5 를 고른 근거로 이 기준을 쓴다.

| Term | Definition | |
|---|---|---|
| **Access Speed(액세스 속도)** | Speed by which consecutive or non-consecutive traces can be loaded | `[OPTIMIST]` |
| **Backward Compatibility(하위 호환성)** | The ability of tools or systems to support older versions of a file format. | `[OPTIMIST]` |
| **Batching(배칭)** | Ability to store a dataset in multiple files, in order to not exceed a maximal file size. | `[OPTIMIST]` |
| **Interoperability(상호운용성)** | The ability of tools or systems to read and process a file format created by a different tool or system. | `[OPTIMIST]` |
| **Dataset Integrity(데이터셋 무결성)** | Ensuring the accuracy and unaltered nature of the collected records and metadata. | `[OPTIMIST]` |
| **Extensibility(확장성)** | The ability of a file format to accommodate new features and extensions without requiring major changes to the tools that process the file format. | `[OPTIMIST]` |
| **Flexibility(유연성)** | The ability of a file format to support new use cases. | `[OPTIMIST]` |
| **Network Friendliness(네트워크 친화성)** | Ability of the file format to support access to partial datasets (batches and slices). | `[OPTIMIST]` |
| **Open(개방성)** | The availability of an openly published file format specification. | `[OPTIMIST]` |
| **Reproducibility(재현성)** | The ability of a file format to support replication of measurements. | `[OPTIMIST]` |
| **Resiliency(복원력)** | Capability to detect and recover from file corruption (e.g. after an interrupted acquisition). | `[OPTIMIST]` |
| **Scalability(스케일러빌리티)** | The ability of the file format to handle increasing amounts of data effectively. | `[OPTIMIST]` |
| **Simplicity(단순성)** | Ease of implementation to read, write and process the file format. | `[OPTIMIST]` |
| **Storage density(저장 밀도)** | File size as a function of the amount of data stored. | `[OPTIMIST]` |
| **Support(지원 범위)** | The number of tools that can read or write the file format. | `[OPTIMIST]` |
| **Versatility(다목적성)** | Ability to perform a variety of functions or adapt to different tasks and environments. | `[OPTIMIST]` |

---

## 4. Attack and test terms (공격·시험 용어) — ISO/IEC 17825:2024

### 4.1 Terms and definitions (3절)

**Advanced side-channel analysis / ASCA(어드밴스드 부채널 분석)**
Advanced exploitation of the instantaneous side-channels emitted by a cryptographic device that
depends on the data it processes and on the operation it performs to retrieve secret parameters.
`[ISO 17825 3.1]`

**Correlation power analysis / CPA(상관 전력 분석)**
Analysis where the correlation coefficient is used as the statistical method. `[ISO 17825 3.2]`

**Critical security parameter class / CSP class(CSP 클래스)**
Class into which a critical security parameter is categorised.
EXAMPLE — Cryptographic keys, authentication data such as passwords, PINs, biometric
authentication data. `[ISO 17825 3.3]`

**Differential electromagnetic analysis / DEMA(차분 전자파 분석)**
Analysis of the variations of the electromagnetic field emanated from a cryptographic module,
using statistical methods on a large number of measured electromagnetic emanations values for
determining whether the assumption of the divided subsets of a secret parameter is correct, for the
purpose of extracting information correlated to security function operation. `[ISO 17825 3.4]`

**Differential power analysis / DPA(차분 전력 분석)**
Analysis of the variations of the electrical power consumption of a cryptographic module, for the
purpose of extracting information correlated to cryptographic operation. `[ISO 17825 3.5]`

**Electromagnetic analysis / EMA(전자파 분석)**
Analysis of the electromagnetic field emanated from a cryptographic module as the result of its
logic circuit switching, for the purpose of extracting information correlated to security function
operation and subsequently the values of secret parameters such as cryptographic keys.
`[ISO 17825 3.6]`

**Implementation under test / IUT(테스트 대상 구현)**
Implementation which is tested based on non-invasive methods. `[ISO 17825 3.7]`

**Power analysis / PA(전력 분석)**
Analysis of the electric power consumption of a cryptographic module, for the purpose of extracting
information correlated to the security function operation and subsequently the values of secret
parameters such as cryptographic keys. `[ISO 17825 3.8]`

**Side-channel analysis / SCA(부채널 분석)**
Exploitation of the fact that the instantaneous side-channels emitted by a cryptographic device
depends on the data it processes and on the operation it performs to retrieve secret parameters.
`[ISO 17825 3.9]`

**Side-channel collision attack(부채널 충돌 공격)**
Powerful category of side-channel analysis that usually combines leakage from distinct points in
time, making them inherently bivariate. `[ISO 17825 3.10]`

**Simple electromagnetic analysis / SEMA(단순 전자파 분석)**
Direct (primarily visual) analysis of patterns of instruction execution or logic circuit
activities, obtained through monitoring the variations in the electromagnetic field emanated from a
cryptographic module, for the purpose of revealing the features and implementations of
cryptographic algorithms and subsequently the values of secret parameters. `[ISO 17825 3.11]`

**Simple power analysis / SPA(단순 전력 분석)**
Direct (primarily visual) analysis of patterns of instruction execution (or execution of individual
instructions), in relation to the electrical power consumption of a cryptographic module, for the
purpose of extracting information correlated to a cryptographic operation. `[ISO 17825 3.12]`

**Timing analysis / TA(타이밍 분석)**
Analysis of the variations of the response or execution time of an operation in a security
function, which can reveal knowledge of or about a security parameter such as a cryptographic key
or PIN. `[ISO 17825 3.13]`

### 4.2 Abbreviated terms (4절)

두문자어는 풀어 쓰지 않고 그대로 쓴다.

| | | | |
|---|---|---|---|
| ASCA | advanced side-channel analysis | MAC | message authentication code |
| AES | advanced encryption standard | PA | power analysis |
| CPA | correlation power analysis | PC | personal computer |
| CSP | critical security parameter | PCB | printed circuit board |
| DEMA | differential electromagnetic analysis | PKCS | public-key cryptography standards |
| DES | data encryption standard | RBG | random bit generator |
| DLC | discrete logarithm cryptography | RNG | random number generator |
| DPA | differential power analysis | RSA | Rivest Shamir Adleman |
| DSA | digital signature algorithm | SCA | side-channel analysis |
| ECC | elliptic curve cryptography | SEMA | simple electromagnetic analysis |
| ECDSA | elliptic curve digital signature algorithm | SHA | secure hash algorithm |
| EM | electromagnetic | SNR | signal to noise ratio |
| EMA | electromagnetic analysis | SPA | simple power analysis |
| HMAC | keyed-hashing message authentication code | TA | timing analysis |
| IFC | integer factorization cryptography | USB | universal serial bus |
| IUT | implementation under test | | |

`[ISO 17825 4]`

### 4.3 Measurement requirements (Annex B) — 값이 아니라 요건

스키마가 측정 메타데이터를 요구하는 근거다. 값 자체는 데이터셋마다 다르다.

- Bandwidth shall be at least **50 %** of the device clock rate for software implementations and at
  least **80 %** for hardware implementations. `[ISO 17825 B.2]`
- There shall be a capability to capture samples at **5 ×** the bandwidth. `[ISO 17825 B.2]`
- There shall be a minimum of **8 bits** of sampling resolution. `[ISO 17825 B.3]`
- If the used side-channel is power consumption, a **resistor** shall be placed between the VCC line
  and the IUT; if electromagnetic emanations, a **near-field magnetic probe** shall be used.
  `[ISO 17825 B.5]`

---

## 5. Project-defined terms (프로젝트 정의 용어) — 표준 아님

아래는 **표준 문서에 정의가 없는데 이 저장소가 쓰는** 용어다. 표준인 것처럼 인용하면 안 된다.

**Subset(서브셋)**
A named group of Records within one Dataset that share an acquisition protocol — that is, the same
rule for generating the key and plaintext of each Execution. Distinct from OPTIMIST's *Splitting*,
which partitions records for machine-learning purposes only. `[PROJECT]`

> 이 구분이 필요한 이유: OPTIMIST 의 Splitting 은 같은 모집단을 학습/검증/시험으로 나누는
> 것이지만, 우리의 subset 은 **애초에 다른 규약으로 수집된** 별개의 모집단이다.

**Subset role(서브셋 역할)**
The purpose a Subset serves in an evaluation. This project uses:
`exploration`, `profiling`, `attack`, `leakage-detection-fixed`, `leakage-detection-random`.
`[PROJECT]`

**Profiling set(프로파일링 세트)**
A Subset acquired with known key material, used to build a leakage model of the Target.
`[PROJECT]`

**Attack set(어택 세트)**
A Subset acquired with a fixed unknown-to-the-attacker key, used to evaluate key recovery.
`[PROJECT]`

**TVLA (Test Vector Leakage Assessment)(TVLA)**
A leakage-detection methodology comparing two Subsets acquired under contrasting input regimes
(e.g. fixed versus random key) with Welch's t-test. Not defined in ISO/IEC 17825:2024; the standard
refers to Welch's test as *a* statistical test without naming the methodology. `[PROJECT]`

**POI (Point of Interest)(POI)**
A sample index at which a chosen intermediate value produces measurable leakage, typically selected
by SNR. `[PROJECT]`

**Encryption region(암호화 구간)**
The interval of a Trace that covers the cipher proper, excluding preceding key schedule or setup
work that shares the same trigger window. Recorded as a sample index. `[PROJECT]`

> 이 개념이 필요한 이유: 트리거가 키 스케줄까지 감싸면 보호되지 않은 구간이 비교를 지배해
> 대책의 효과가 가려진다. `[extra] SCALib`은 이 구분을 적용해 Encryption region을
> 먼저 실측하고, 이후 분석을 그 구간으로 제한한다.

**Mask share(마스크 셰어)**
One of the random values a masking countermeasure uses to split a sensitive intermediate value.
Recorded only for research purposes; attacker-perspective analysis must not read it. `[PROJECT]`

**Golden model(골든 모델)**
A host-side reference implementation of the cryptographic algorithm, used to verify that the Target
computed the expected ciphertext for each Execution. `[PROJECT]`

---

## 6. Terminology collisions (용어 충돌) — 반드시 지킬 것

같은 낱말이 두 체계에서 다른 뜻으로 쓰인다. 구분하지 않으면 문장이 두 가지로 읽힌다.

### 6.1 Attributes

| | 뜻 |
|---|---|
| OPTIMIST **Attributes** | 실행 하나에 딸린 명명 변수 전체. **Trace 를 포함한다** |
| HDF5 **attribute** | 객체에 붙는 소량 메타데이터 (`h5py` 의 `.attrs`) |

**규칙:** 문서에서 "attribute" 는 **OPTIMIST 의 뜻**으로 쓴다.
HDF5 쪽을 가리킬 때는 반드시 **"HDF5 attrs"** 라고 적는다.
따라서 OPTIMIST 의 Attributes 는 HDF5 에서 **배열(HDF5 dataset)** 로 저장되고,
OPTIMIST 의 Metadata 가 **HDF5 attrs** 로 저장된다. 이름과 저장 위치가 엇갈리므로 주의한다.

### 6.2 Dataset

| | 뜻 |
|---|---|
| OPTIMIST **Dataset** | 레코드 수열 + Attributes + Metadata = **파일 한 벌** |
| HDF5 **dataset** | 배열 객체 하나 (`h5py.Dataset`) |

**규칙:** "데이터셋" 은 **OPTIMIST 의 뜻**으로 쓴다.
HDF5 쪽은 **"HDF5 dataset(배열)"** 로 적는다.

### 6.3 Sample

| | 뜻 |
|---|---|
| OPTIMIST **Sample** | 채널을 한 번 측정한 값 = 트레이스의 한 점 |
| 통계 일반 | 표본(= 관측 하나, 여기서는 트레이스 한 장에 해당) |

**규칙:** "샘플" 은 **OPTIMIST 의 뜻**(트레이스의 한 점)으로 쓴다.
통계적 표본 수를 말할 때는 "트레이스 수" 또는 "레코드 수" 라고 적고 "샘플 수" 라고 하지 않는다.

### 6.4 Trace

`Trace` 는 한 실행의 측정 벡터 하나다. 여러 장을 묶은 것은 **trace set** 이 아니라
**Dataset** 또는 **Subset** 이라고 부른다(OPTIMIST 는 Metadata 정의에서 "trace sets" 라는
표현을 쓰지만 별도 용어로 정의하지 않았다).

---

## 7. Sources

| | |
|---|---|
| OPTIMIST | *Open Tools, Interfaces and Metrics for Implementation Security Testing — File Format for Traces: Requirements and Glossary*, Working Document v0.5, 2025-01-06. <https://optimist-ose.org/docs/file-format/intro> |
| ISO/IEC 17825:2024 | *Information technology — Security techniques — Testing methods for the mitigation of non-invasive attack classes against cryptographic modules*, Second edition, 2024-01. <https://www.iso.org/standard/86616.html> |

> ISO/IEC 17825:2024 원문은 **저작권 보호 문서라 저장소에 포함하지 않는다.** 로컬에
> 사본이 있다면 `gitignore/ISO_IEC17825_2024_EN.pdf` 에 둔다(그 디렉터리는 git 에서
> 통째로 제외된다). 사본이 없어도 이 용어집만으로 용어의 뜻은 파악할 수 있게 썼다.

관련 문서: 데이터셋 스키마는 [`SCHEMA.md`](SCHEMA.md) 를 본다.
