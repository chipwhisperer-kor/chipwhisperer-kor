# [extra] SCALib — Normal AES ∥ Masked AES 비교 예제

[SCALib](https://github.com/simple-crypto/SCALib) 0.6.4 기능을 **기능 하나당 노트북 하나**로 익히되,
**비마스킹 AES**(`tiny-AES-c`)와 **마스킹 AES**(`masked-aes-c`)를 **같은 단계에서 나란히** 비교한다.

공식 ChipWhisperer 튜토리얼(`workspace/1.`~`3.`)과는 별개의 연구용 자료다.

---

## 1. 실행 순서

```text
0.0.Dataset_Collect_tiny-AES-c.ipynb    ← 하드웨어 (Normal)
0.1.Dataset_Collect_masked-aes-c.ipynb  ← 하드웨어 (Masked, mask 포함)
        │
        ├─→ traces/scalib_dataset_tiny-AES-c.h5
        └─→ traces/scalib_dataset_masked-aes-c.h5
                    │
                    └─→ 1.0 … 6.0  (단계마다 Normal ∥ Masked, 하드웨어 불필요)
```

`traces/*.h5` 는 GB 단위라 저장소에 넣지 않는다.

분석 노트북 `1.0`–`6.0` 은 **하드웨어 없이** 돌아간다. h5 두 개만 있으면 된다.
`1.0` 이 `nb_output/poi_*.npz` 를 만들고 나머지가 그것을 읽으므로 **번호 순서로 실행**한다.

```bash
docker exec -it chipwhisperer-kor bash
cd "/workspace/[extra] SCALib"
for f in 1.0.SNR 1.1.Quantizer 2.0.Ttest 2.1.MTtest 3.0.CPA \
         4.0.LDAClassifier 4.1.MultiLDA 4.2.RLDA 5.0.SASCA 6.0.KeyRank; do
    jupyter nbconvert --to notebook --execute --inplace "$f.ipynb"
done
```

수집 노트북(`0.0`/`0.1`)은 하드웨어가 있을 때만 돌아간다. 장시간 수집 중의 사고는
스스로 복구하므로 사람이 지켜볼 필요가 없다 — §8 참고.

---

## 2. 이름 체계 (단일 축)

| 계층 | Normal | Masked |
|------|--------|--------|
| 라이브러리 | `tiny-AES-c/` | `masked-aes-c/` |
| 펌웨어 | `simpleserial_tiny-AES-c/` | `simpleserial_masked-aes-c/` |
| 수집 | `0.0.…_tiny-AES-c` | `0.1.…_masked-aes-c` |
| 데이터셋 | `scalib_dataset_tiny-AES-c.h5` | `scalib_dataset_masked-aes-c.h5` |
| POI | `poi_tiny-AES-c.npz` | `poi_masked-aes-c.npz` |

경로·라벨 정의의 정본은 `scalib_common.py` 의 `TARGETS` 다.

---

## 3. 기능 ↔ 노트북

| 노트북 | SCALib API | 비교 초점 |
|--------|-----------|-----------|
| `1.0.SNR` | `metrics.SNR` | 1차 SBox SNR·POI, **암호화 구간 경계 `enc_start`** 산출 |
| `1.1.Quantizer` | `preprocessing.Quantizer` | 동일 양자화 파이프라인 |
| `2.0.Ttest` | `metrics.Ttest` | TVLA — 전 구간 vs 암호화 구간 |
| `2.1.MTtest` | `metrics.MTtest` | 시점 조합(2차) t-test |
| `3.0.CPA` | `attacks.Cpa` | 1차 CPA — 암호화 구간 전체 스캔 |
| `4.0.LDAClassifier` | `modeling.LDAClassifier` | 템플릿 1바이트 |
| `4.1.MultiLDA` | `modeling.MultiLDA` | 16바이트 동시 |
| `4.2.RLDA` | `modeling.RLDAClassifier` + `metrics.RLDAInformationEstimator` | 회귀 LDA·정보량(비트) |
| `5.0.SASCA` | `attacks.FactorGraph` / `BPState` | 정보 결합 |
| `6.0.KeyRank` | `postprocessing.rank_*` | 전역 키 순위 (시리즈 결론) |

분석 노트북 패턴: **단계 → 의도 → Normal → Masked(공격자) → Masked(연구자) → 비교**
(타겟 전체를 직렬로 끝내지 않음).

### 세 가지 관점

| 관점 | 아는 것 | `mask` 사용 |
|------|---------|:----------:|
| 공격자 | 평문(+암호문) | **안 씀** |
| 평가자 | 평문 + 키 (누설 진단용) | 안 씀 |
| 연구자 | 평문 + 키 + **마스크 값** | 씀 |

연구자 절은 언제나 제목으로 분리한다. 공격 셀이 `mask` 를 참조하면 비교의 의미가 무너진다.

### 비교는 왜 "암호화 구간" 에서만 하는가

`masked-aes-c` 는 `CipherMasked` 안만 보호하고 **`KeyExpansion` 은 벤더 원본 비마스킹**이다.
그런데 이 저장소의 펌웨어는 키 스케줄을 트리거 **안**에서 수행하므로, 파형 앞부분은
두 타겟이 똑같이 무방비다. 전 구간으로 비교하면 그 공통 누설이 마스킹 효과를 가린다
(전 구간 TVLA `|t|`: Normal 114 / Masked 116 — 차이가 없어 보인다).

그래서 `1.0` 이 **평문 의존 누설이 시작되는 샘플**(`enc_start`)을 실측해 `poi_*.npz` 에
저장하고, `2.0`–`6.0` 이 그 이후 구간에서만 비교한다. 이 데이터셋 기준
Normal 5093 / Masked 5089 이며, 암호화 구간의 1차 TVLA 임계 초과율은 45.3% vs 0.9% 로 갈린다.

키 스케줄 누설은 마스킹의 실패가 아니라 이 PoC 의 **보호 범위 밖**이다.

---

## 4. 하드웨어 (수집만)

| 구성 | 역할 |
|------|------|
| ChipWhisperer-Lite | 통신·플래시·HS2 클럭 |
| ChipWhisperer-Husky | TRIG / AUX 클럭 / 션트 관측 |
| CW308 + STM32F3 | 타겟 |

```text
호스트
  ├─ Lite ──20pin── CW308
  └─ Husky USERIO D0←TRIG, AUX←CLKIN, Measure←SHUNTL
```

Husky 는 AUX 로 타겟 클럭을 받아 **동기 샘플링**한다(`clkgen_src = "extclk_aux_io"`).
그래서 Lite 가 HS2 로 타겟에 클럭을 공급하기 전에는 Husky 설정이 lock 되지 않는다.

### 펌웨어 빌드

수집 노트북이 자동으로 호출하지만, 손으로 확인할 때는 이렇게 한다(컨테이너 안).

```bash
cd "simpleserial_tiny-AES-c"      # 또는 simpleserial_masked-aes-c
make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1 clean
make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1
```

`SS_VER_2_1` 만 지원한다. 두 트리는 `TARGET`·`SRC` 만 다르고 상위
`workspace/base/Makefile.inc` 를 공유한다.

### 프로토콜 (SimpleSerial 2.1)

| cmd | scmd | 의미 |
|-----|------|------|
| `0x81` | `k`/`p`/`l` | 키 / 평문 / 길이 |
| `0x81` | `s` | **Masked만** 마스크 난수 시드 4B (little-endian) |
| `0x82` | `c` | 트리거 구간에서 `MY_AES_ECB` |
| `0x83` | `r` | 암호문 16B |
| `0x83` | `m` | **Masked만** 마스크 10B (트리거 **이후**) |

파형 길이는 `scope.adc.trig_count` 실측. 마스킹 AES 는 비마스킹보다 길다.

### 마스크 시드 규약 (Masked 수집 시 필수)

STM32F303 에는 TRNG 가 없고 스택·전역 주소는 매 부팅 같은 값이라, 타겟이 스스로
쓸 만한 시드를 만들 수 없다. 그래서 **호스트가 `0x81 's'` 로 시드를 준다.**

`dataset_collect_lib` 의 `collect_group` / `resume_group` 이 그룹을 채우기 직전에,
그리고 자동 복구(§8) 직후에 `set_mask_seed()` 를 부르고 쓴 시드를 그룹 attrs
`mask_seeds` 에 남긴다. 라운드 번호는 프로세스 변수가 아니라 **이미 기록된 시드 개수**
에서 세므로, 이어받기 스크립트를 껐다 켜도 같은 수열이 재생되지 않는다.

실기 확인: 같은 시드를 심으면 마스크 수열이 그대로 재현되고, 다른 시드면 달라진다.
즉 시드가 수열을 결정하므로 라운드마다 새 시드를 주면 재시작이 구조적으로 불가능하다.


---

## 5. 데이터셋 규격

**저장 구조의 정본은 저장소 루트의 [`SCHEMA.md`](../../SCHEMA.md) 다.** 용어는
[`GLOSSARY.md`](../../GLOSSARY.md) 를 따른다. 여기에는 이 서브프로젝트 고유 부분만 적는다.

### Subset 구성

| Subset | `role` | 키 | 평문 |
|---|---|---|---|
| `/explore` | `exploration` | 랜덤 | 랜덤 |
| `/profiling` | `profiling` | 랜덤 | 랜덤 |
| `/attack` | `attack` | **고정** | 랜덤 |
| `/tvla_rk` | `leakage-detection-random` | 랜덤 | 고정 |
| `/tvla_fk` | `leakage-detection-fixed` | **고정** | 고정 |

배열은 스키마대로 `trace`·`key`·`plaintext`·`ciphertext` 이며, Masked 만 `mask` 가 더 있다.

### `mask` — 이 서브프로젝트 고유

| | Normal | Masked |
|--|--------|--------|
| `mask` | 없음 | `(n, 10) uint8` |
| `iut_countermeasure` | `"none"` | `"1st-order Boolean masking …"` |

레이아웃: `M1 M2 M3 M4 M' M M1' M2' M3' M4'`
난수 6바이트 + MixColumns 유도 4바이트. **공격 분석 셀은 `mask` 를 쓰지 않는다.**
연구자 절에서만 사용한다.

구현에서 유도한 마스킹된 중간값 (`1.0` §10 에 유도 과정이 있다):

```text
SubBytes 입력 레지스터 = p ^ k ^ mask[4]
SubBytes 출력 레지스터 = SBOX[p ^ k] ^ mask[5]
```

### 준수 확인

```python
from scalib_common import validate_dataset
validate_dataset("masked-aes-c")     # 빈 리스트면 준수
```

수집 직후 자동으로 호출된다. 두 데이터셋 모두 현재 **완전 준수**다.

### 장수

| 그룹 | 장수 (두 타겟 동일) |
|------|------|
| explore | 5,000 |
| profiling | 100,000 |
| attack | 10,000 |
| tvla_rk / tvla_fk | 1,000 each |

두 타겟이 같은 시드·같은 장수를 쓰므로 입력 벡터가 정렬된다. 다만 분석 노트북은
목표치 상수(`N_PROFILING`)가 아니라 `group_len(group, target)` 으로 **실보유 장수**를
읽는다. 수집이 중간에 끊긴 파일을 그대로 분석하면 조용히 어긋나기 때문이다.

수집 로직 정본: `dataset_collect_lib.py`.  
장수·시드 정본: `scalib_common.py` (`SEED=1234` 등).

---

## 6. `masked-aes-c` 패치 — 최소 수정 3건

원본은 마스크가 스택 지역변수라 외부 판독이 불가능하다. 이 서브프로젝트는 최소 패치를 둔다.

1. `AES_get_last_masks()` 로 마지막 `mask[10]` 제공 (연구용 export)
2. 내부 per-encrypt `srand(time(NULL))` 제거 → 시드는 호스트가 `0x81 's'` 로 준다
3. **`rand() % 0xFF` → `rand() & 0xFF`**

3번은 벤더 원본의 명백한 실수다. `% 0xFF` 는 0–254 만 내놓아 `0xFF` 가 한 번도 나오지 않고
분포도 균일하지 않다. 마스킹의 안전성 논거가 마스크의 **균일성**을 전제로 하므로 이 편향은
그대로 1차 잔여 누설이 된다. 암호·마스킹 **공식 자체는 변경하지 않았다.**

> 실기 확인 완료: 빌드·플래시·통신·골든 AES 일치, `0x81 's'` 에코, `0x83 'm'` 회수,
> 120장 수집에서 고유 마스크 120/120, 난수부 최댓값 **255**(수정 전 254).

---

## 7. `nb_output/`

- `poi_*.npz` — `1.0` 이 타겟별로 저장, `2.0` 이후가 읽음

  | 키 | 내용 |
  |---|---|
  | `poi`, `poi_windows`, `snr_peak` | 공격자 관점 POI (SBox 출력 라벨) |
  | `enc_start` | 암호화 구간 시작 샘플 |
  | `poi_research`, `poi_research_windows`, `snr_peak_research`, `poi_mask` | **연구자 관점** POI (Masked 전용) |

- `tvla_ref_py39.*` — Python 3.9→3.12 회귀 레퍼런스(역사 자료)

---

## 8. 장시간 수집의 자동 복구

수십만 장을 몇 시간 받는 동안 USB 는 끊기고 Husky 는 먹통이 된다. 사람이 지켜보다
다시 눌러 줄 수 없으므로 `Bench.capture()`(`dataset_collect_lib.py`)가 스스로 회복한다.
수집 노트북은 이 함수만 쓰며, `capture_retry` 를 직접 부르지 않는다.

| 단계 | 하는 일 | 최대 |
|:----:|---------|:----:|
| 1 | 단순 재시도 | 3회 |
| 2 | 재연결 — 장비를 다시 열고 클럭·게인·`adc.samples` 복원 | 2회 |
| 3 | **Husky 펌웨어 재기록** — `0x22 0x03` 소거 → SAM-BA → `program_sam_firmware` | 1회 |

성공하면 그 자리에서 수집을 이어간다. 전부 실패하면 예외로 멈추며, 이미 저장된 그룹은
유효하므로 노트북의 이어받기 셀로 재개한다. 복구 이력은 h5 의 `recoveries` attr 에 남고
`dataset_summary()` 가 출력한다.

> 이 저장소의 Masked 데이터셋(117,000장)이 실제로 이 경로를 탔다. 수집 중 세 번 깨졌고
> (`reflash`, `reconnect`, `reconnect`) 사람 개입 없이 전부 회복해 목표 장수를 채웠다.
> `profiling` 그룹의 `mask_seeds` 가 네 개인 것이 그 흔적이다 — 최초 1회 + 복구 3회.

복구 뒤에는 반드시 두 가지를 되돌린다. 빠뜨리면 파형이 조용히 어긋난다.

- **측정 설정 복원** — `setup_husky` 재실행 후 처음 실측한 `ns` 를 그대로 다시 넣는다.
  여기서 `trig_count` 를 다시 재면 값이 달라져 행마다 길이가 맞지 않는다.
- **마스크 시드 재주입** — 복구 중 타겟이 전원을 잃었으면 `rand()` 수열이 처음부터
  재생된다. 새 시드를 심고 `mask_seeds` attr 에 누적 기록한다.

### 3단계가 왜 필요한가

Husky 펌웨어가 손상되면 **버전은 정상값(1.5.0)으로 보고하면서** FPGA 레지스터 읽기만
어긋난다 — 모든 `FPGA_READ` 응답 앞에 `0xff` 한 바이트가 더 붙어 `cw.scope()` 가
`Unknown hwInfoVer: Default/Unknown` 으로 실패한다. 버전 비교로는 발견할 수 없다.

이 고장은 USB 포트 전원 차단·허브 재열거·**물리적 재삽입 어느 것으로도 낫지 않고**
재기록만 듣는다. 실패해도 벽돌이 되지 않는다 — SAM 의 하드웨어 부트로더는 지울 수 없어,
소거 뒤 재기록이 실패해도 장치는 SAM-BA(`03eb:6124`)로 USB 에 남아 재시도할 수 있다.

> 컨테이너의 `/dev` 는 호스트와 분리된 tmpfs 이고 `/dev/bus/usb` 만 bind-mount 라
> 새 tty 노드가 안 보일 수 있다. `_samba_port()` 가 `/sys/class/tty` 에서 major:minor 를
> 읽어 `mknod` 로 만든다. 별도 설정이 필요 없다.

---

## 9. 참고

- SCALib <https://scalib.readthedocs.io/> · <https://github.com/simple-crypto/SCALib>
- tiny-AES-c <https://github.com/kokke/tiny-AES-c>
- masked-aes-c <https://github.com/CENSUS/masked-aes-c> (MELITY boolean masking PoC)

링크는 보조다. 각 노트북은 그 하나만으로 해당 단계를 따라갈 수 있게 작성한다.
