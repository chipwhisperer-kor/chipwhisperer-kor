# [extra] SCALib — 기능별 예제 노트북

[SCALib](https://github.com/simple-crypto/SCALib) 0.6.4가 제공하는 부채널 분석 기능을 **기능 하나당 노트북 하나**로 익히는 서브프로젝트다. 모든 예제는 시뮬이 아니라 **ChipWhisperer로 실측한 AES-128 전력 파형**을 쓴다.

공식 ChipWhisperer 튜토리얼(`workspace/1.`~`3.`)과는 별개의 연구용 자료다.

---

## 1. 실행 순서

**`0.0.Dataset_Collect.ipynb`를 먼저 한 번 실행해야 한다.** 나머지 노트북은 그 결과 파일을 읽을 뿐이므로 **하드웨어 없이** 돌아간다.

```text
0.0.Dataset_Collect.ipynb   ← 하드웨어 필요 (실험대 1회 점유)
        │
        └─→ traces/scalib_dataset.h5
                    │
                    ├─→ 1.0.SNR         1.1.Quantizer
                    ├─→ 2.0.Ttest       2.1.MTtest
                    ├─→ 3.0.CPA
                    ├─→ 4.0.LDAClassifier  4.1.MultiLDA  4.2.RLDA
                    ├─→ 5.0.SASCA
                    └─→ 6.0.KeyRank
```

`traces/*.h5`는 GB 단위라 저장소에 포함되지 않는다. 노트북을 받은 뒤 `0.0`을 실행해 직접 만든다.

## 2. 기능 ↔ 노트북 대응

| 노트북 | SCALib API | 무엇을 하는가 |
|--------|-----------|---------------|
| `1.0.SNR` | `metrics.SNR` | 시점별 신호대잡음비로 **누설 지점(POI)** 을 찾는다. 이후 모든 노트북의 전제 |
| `1.1.Quantizer` | `preprocessing.Quantizer`, `QuantFitMethod` | float 파형을 SCALib이 요구하는 `int16`으로 변환한다 |
| `2.0.Ttest` | `metrics.Ttest` | TVLA — 두 집단 파형이 통계적으로 다른지 본다 (누설 **진단**) |
| `2.1.MTtest` | `metrics.MTtest` | 여러 시점의 **곱**에 대한 t-test. 한 시점만으로 부족할 때 |
| `3.0.CPA` | `attacks.Cpa` | 상관 전력 분석. **프로파일링 없이** 키를 복구한다 |
| `4.0.LDAClassifier` | `modeling.LDAClassifier` | 템플릿 공격. 한 바이트를 프로파일링해 확률을 얻는다 |
| `4.1.MultiLDA` | `modeling.MultiLDA` | 16바이트를 한 번에 프로파일링한다 |
| `4.2.RLDA` | `modeling.RLDAClassifier`, `metrics.RLDAInformationEstimator` | 회귀 기반 LDA와 **정보량 추정** |
| `5.0.SASCA` | `attacks.FactorGraph`, `BPState`, `GenFactor` | 신뢰 전파로 여러 중간값 정보를 합쳐 키를 복구한다 |
| `6.0.KeyRank` | `postprocessing.rank_accuracy`, `rank_nbin` | 공격 점수로 **전체 키의 순위**를 추정한다 |

## 3. 하드웨어 전제 (`0.0` 에만 해당)

부채널 **수집**만 필요하다. 오류주입 장비는 쓰지 않는다.

| 구성 | 역할 |
|------|------|
| ChipWhisperer-Lite | 타겟과 SimpleSerial2 통신, 펌웨어 플래시, 시스템 클럭(HS2) 공급 |
| ChipWhisperer-Husky | 트리거·클럭·션트를 **와이어태핑**으로 측정 (통신에 개입하지 않음) |
| CW308 + STM32F3 | 타겟 MCU |
| `simpleserial_main/` + `tiny-AES-c/` | 타겟 펌웨어. AES-128 **ECB** 한 블록 |

```text
호스트 PC
  ├─ USB ─ ChipWhisperer-Lite  ──20pin── CW308 (UART, HS2 클럭, 프로그래밍)
  └─ USB ─ ChipWhisperer-Husky
              ├─ USERIO D0  ←  CW308 TRIG (GPIO4)
              ├─ AUX MCX    ←  CW308 CLKIN (클럭 분기)
              └─ Measure    ←  CW308 SHUNTL
```

### 타겟이 무엇을 계산하는가

`simpleserial-base.c`의 `0x82 'c'` 명령이 트리거를 올리고 `MY_AES_ECB()`를 호출한 뒤 내린다.

```c
trigger_high();
MY_AES_ECB(global_ret, global_k, global_p, global_len);
trigger_low();
```

`MY_AES_ECB`는 `AES_init_ctx()`(키 스케줄)와 `AES_ECB_encrypt()`(10라운드)를 **모두** 수행한다. 즉 트리거 구간 = **AES 연산 전체**다.

파형 길이는 상수로 정하지 않고 `scope.adc.trig_count`(트리거가 올라가 있던 실제 샘플 수)로 정한다. 저장소의 `workspace/base/My_Setup.ipynb`에 있는 `my_setting_num_samples()`와 같은 방식이다. 임의의 길이를 쓰면 AES 뒷부분이 잘려 마지막 라운드 기반 분석이 불가능해진다.

## 4. 데이터셋 규격 (`traces/scalib_dataset.h5`)

저장소의 기존 HDF5 규약(`workspace/traces/*.h5`)을 그대로 따른다. 그룹마다 4개 데이터셋:

| 데이터셋 | shape | 내용 |
|----------|-------|------|
| `i_k` | `(n, 16)` `uint8` | 키 |
| `i_p` | `(n, 16)` `uint8` | 평문 |
| `o` | `(n, 16)` `uint8` | 타겟이 돌려준 암호문 |
| `t` | `(n, ns)` `int16` | 전력 파형 |

| 그룹 | 키 | 평문 | 목표 장수 | 쓰는 노트북 |
|------|----|------|------|-------------|
| `/explore` | 랜덤 | 랜덤 | 5,000 | 1.0, 1.1 |
| `/profiling` | 랜덤 | 랜덤 | 100,000 | 4.0, 4.1, 4.2, 5.0 |
| `/attack` | **고정** | 랜덤 | 10,000 | 3.0, 4.x, 5.0, 6.0 |
| `/tvla_rk` | 랜덤 | 고정 | 1,000 | 2.0, 2.1 |
| `/tvla_fk` | **고정** | 고정 | 1,000 | 2.0, 2.1 |

측정은 타겟 클럭당 4샘플(`adc_mul=4`)이고, 파형 길이는 `trig_count` 실측으로 정해
AES 연산 전체(키 스케줄 + 10라운드, 약 8,293 사이클 = 33,172 샘플)를 담는다.
전량 수집 시 약 8 GB, 약 80분이 걸린다.

> **수집이 중간에 끊길 수 있다.** 이 실험대에서는 장시간 캡처 중 USB 가 끊기는 일이 있다
> (`LIBUSB_ERROR_IO`, `LIBUSB_ERROR_NO_DEVICE`). `0.0` 은 그룹을 작은 것부터 모으고
> 배치마다 디스크에 flush 하므로 사고가 나도 그때까지 모은 것은 남는다.
> `0.0` **§8.1 이어받기**를 실행하면 모자란 만큼만 채운다 — 키·평문이 시드로 결정되므로
> 이어붙인 데이터는 한 번에 모은 것과 구별되지 않는다.
>
> 프로파일링은 클래스가 256개라 **클래스당 표본 수**가 관건이다. 100,000장이면 390장,
> 40,000장이면 152장꼴이다. 1,000장(클래스당 3.9장) 수준에서는 LDA 학습 자체가 실패한다
> (4.2 노트북이 그 경계를 보인다).

전 그룹이 동일한 측정 설정으로 수집되므로 노트북 간 결과를 서로 대조할 수 있다. 측정 조건(`trig_count`, `adc_mul`, `adc_freq`, 정답 키 등)은 파일 attrs에 기록된다.

수집 중 매 트레이스마다 타겟 암호문을 호스트 AES 결과와 대조하며, 하나라도 어긋나면 즉시 중단한다. **수집이 끝났다는 것 자체가 데이터 무결성의 증거다.**

## 5. `nb_output/` — 역사 자료

`tvla_ref_py39.*`는 2026-08-06 Python 3.9 → 3.12 전환 때 회귀를 검증한 레퍼런스다(당시 `adc_mul=4`, 10,000 샘플). 이 서브프로젝트의 데이터셋은 측정 설정이 달라 그 값과 직접 비교되지 않는다. 전환 검증 기록으로만 보존한다.

## 6. 참고

- SCALib 문서 <https://scalib.readthedocs.io/> · 저장소 <https://github.com/simple-crypto/SCALib>
- tiny-AES-c <https://github.com/kokke/tiny-AES-c> (Unlicense, 커밋 `2385675`)

링크는 보조 자료이며, 각 노트북은 그 하나만 읽어도 해당 기능을 쓸 수 있도록 작성되어 있다.
