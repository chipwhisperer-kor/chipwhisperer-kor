# PicoScope 3418E·ChipWhisperer 파형 비교

이 서브프로젝트는 하나의 STM32F303 타겟이 실행하는 AES-128·SHA-256 복합
연산을 **ChipWhisperer-Lite·Husky의 전력 경로**와 **EM 프로브 → LANGER
PA303 → PicoScope 3418E의 근접 자기장 경로**로 측정한다. 노트북은 웹
code-server에서 **Run All**만으로 장비 점검, 타겟 펌웨어 빌드·플래싱,
수집, 시각·통계 비교를 끝내는 독립 실행 문서다.

| 노트북 | 목적 |
|---|---|
| `1.0.Wiretapping4SCA-PicoScope.ipynb` | 세 장비를 같은 sample rate로 맞춰 같은 암호 실행의 전력·EM 파형 관계를 비교 |
| `2.0.MaximumTimeResolution.ipynb` | Lite 1×, Husky 4×, Pico A+B 8-bit·10-bit 최고속으로 시간축·Y축 해상도를 비교 |
| `3.0.ChannelInterleave-MaxRate.ipynb` | 배선을 유지한 채 채널 마스크만 바꿔 1–4채널 최고 sample rate와 점 밀도를 잰다 |
| `3.1.RapidBlock-SegmentedMemory.ipynb` | 같은 A/B 배선에서 rapid block 세그먼트 메모리와 단일 block의 처리량을 비교한다 |
| `3.2.AdvancedTrigger-Wiretap.ipynb` | pulse-width, analog window, trigger delay를 같은 GPIO·EM 선에서 검증한다 |
| `3.3.FrontEnd-BandwidthDownsample.ipynb` | A bandwidth limiter와 온디바이스 AVERAGE, 소프트웨어 분해능 향상을 스윕한다 |

모든 노트북은 같은 `simpleserial_main/` 펌웨어를 사용한다. 펌웨어는 AES와
SHA를 한 트랜잭션 안에서 실행하므로 두 알고리즘이 항상 하나의 캡처 윈도우에
들어간다.

`3.0`–`3.3`은 PicoScope 자체 API가 주인공이다. Lite는 프로그래밍·UART·클럭만
담당하고 Husky USB handle은 열지 않는다. 물리 배선은 1.0·2.0과 같다. 채널
on/off는 소프트웨어만 바꾼다.

## 배선

Lite는 타겟 프로그래밍·UART·클럭 공급을 담당한다. Husky와 PicoScope는 통신에
개입하지 않고 같은 연산을 수동 관측한다. 아래 표가 이 벤치의 **최종 연결**이다.
노트북마다 프로브를 옮기지 않는다.

| 신호 | 연결 |
|---|---|
| 타겟 전력/션트 | Lite 내장 측정 경로 + Husky Measure |
| 근접 자기장 | EM 프로브 → LANGER PA303 → PicoScope A (DC 50 Ω) |
| GPIO4/TRIG 10× | Lite 내장 트리거 + Husky USERIO D0 + PicoScope B (DC 1 MΩ) |
| GPIO4/TRIG 1× | Pico AUX (전면 **왼쪽** 추가 BNC). 약 3.3 V CMOS |
| 타겟 클럭 | Lite HS2→CW308 CLKIN, 같은 신호를 Husky AUX MCX로 분기 |
| Pico C·D | BNC 미연결. 3.0이 소프트웨어로만 켜서 ADC 인터리브 대가를 본다 |
| Pico AWG | 전면 **오른쪽** 추가 BNC. 사용하지 않음 |
| USB | Lite·Husky·PicoScope를 privileged `chipwhisperer-kor` 컨테이너에 노출 |

PicoScope B에는 한 트랜잭션당 두 HIGH 펄스가 보인다. 첫 펄스는 AES 키
확장·10라운드, 두 번째는 SHA-256 연산 구간이다. 노트북은 이 펄스를 실제
시간 구간의 정본으로 사용한다. B의 10× 프로브 때문에 Pico B에서 HIGH는 약
0.35 V다. 같은 GPIO4를 1×로 AUX에 넣으면 약 3.3 V이며, 3418E AUX의 고정
CMOS 임계값(HIGH > 2.3 V)을 넘는다.

1채널 최고속(8-bit 5 GS/s)은 B·C·D를 끄고 A만 켠 뒤 **AUX 상승 에지**로 연다.
2채널 이상은 A+B를 켜고 B 150 mV 에지를 쓴다. 프로브는 꽂아 둔 채 소프트웨어로만
끈다. 전면 오른쪽 BNC는 SIG GEN(AWG) 출력이라 트리거 입력이 아니다.

PA303 출력은 PicoScope A의 DC 50 Ω 입력으로 종단한다. 노트북은 실제
PA303 출력 파형을 사전 수집해
3418E가 지원하는 가장 작은 안전 input range와 analog offset을 자동 선택하고,
별도 파형으로 rail 여유를 검증한다. 표시되는 PA303 입력 환산 LSB는 nominal
설정 셀의 manufacturer nominal gain만 반영한 참고값이며 EM field strength
보정값은 아니다.

## 실행 조건과 부수 효과

- `setup/docker-compose.yml`로 실행한 기본 컨테이너와 `/dev/bus/usb` 매핑이
  필요하다.
- 첫 실행은 `pypicosdk`와 Pico native driver를 이 디렉터리의 `.runtime/`에
  받으므로 네트워크가 필요하다. 캐시가 있으면 다음 실행은 다시 받지 않는다.
- Run All은 `simpleserial_main/`에서 펌웨어 산출물을 잠시 만들고 STM32F303을
  덮어쓴 뒤 산출물을 정리한다. 장비 핸들은 성공·실패 시 모두 해제한다.
- 파형은 메모리에만 유지한다. 2.0은 두 Pico 해상도의 최고속도 원시 파형을
  모두 보존하므로 실행 중 약 2 GB 이상의 여유 RAM이 필요하다. 3.0의 1채널
  8-bit 최고속과 3.3의 2채널 8-bit 최고속 스윕도 수백 MB를 쓸 수 있다.
- 유사성에 임의 합격선을 적용하거나 Dataset, CPA/DPA 결과를 저장하지 않는다.

각 노트북의 설정 셀이 그 실험의 시리얼, 버전, 캡처 횟수와 샘플링 제약에
대한 단일 정본이다. 값을 바꾸려면 README에 복사하지 말고 실행할 노트북의
설정 셀만 수정한다.

## 이 벤치를 재현하려면

노트북에 박힌 시리얼은 **이 실험실 장비**다. 다른 벤치에서는 설정 셀의
`LITE_SERIAL_NUMBER`를 바꾸고, 1.0·2.0만 추가로 `HUSKY_SERIAL_NUMBER`를
바꾼다. Pico는 시리얼을 하드코드하지 않고 정확히 한 대만 열거한다.

1. 위 배선 표를 그대로 재현한다. Pico 전면 **왼쪽** 추가 BNC가 AUX(트리거
   입력), **오른쪽**은 AWG 출력이라 트리거로 쓰지 않는다.
2. 1.0·2.0은 Lite·Husky·3418E가 모두 USB로 보여야 한다. 3.0–3.3은 Lite와
   Pico만 연다. Husky는 배선에 남아 있어도 된다.
3. 컨테이너는 privileged 와 `/dev/bus/usb` 매핑이 있는 `chipwhisperer-kor`다.
   작업 경로는 `/workspace/[extra] PicoScope`다.
4. 첫 실행은 네트워크로 `.runtime/`에 `pypicosdk==1.7.5`와 libpsospa를 받는다.
   이 핀을 올리면 3.2의 psospa auto-trigger 우회가 다시 깨질 수 있다.
5. STM32 플래시 직후 Pico `Not Found`/`Not Responding` `[!]`가 한두 줄 나온 뒤
   재시도로 열리면 정상이다. 같은 USB 트리에서 프로그래밍이 재열거를 흔든다.
   캡처 중 같은 `[!]`가 나와도 다음 줄에서 열리고 표가 채워지면 실패가 아니다.
6. 노트북은 **하나씩** Run All 한다. 3.1의 rapid bulk 직후 3418E가 수십 초
   USB에서 사라지거나 OpenUnit이 Not Responding일 수 있다. 다음 노트북을 열기
   전에 `lsusb`에 Pico가 다시 보일 때까지 기다린다.
7. code-server에서 **Run All**하면 matplotlib inline이 파형 PNG를 셀에 넣는다.
   밀리볼트·USB 재시도 횟수는 실행마다 달라진다. traceback이 셀을 중단하면
   안 된다. 캡처 횟수, 골든 AES/SHA, 1채널 5 GS/s, pulse-width sha_only의
   B HIGH 1개, 3.3에서 20 kHz·100 kHz·1 MHz가 unsupported, AVERAGE ×4/×8/×16
   점 수가 RAW의 1/4·1/8·1/16인 것처럼 실험이 묻는 칸은 같아야 한다.
   Dataset·CPA는 만들지 않는다.
