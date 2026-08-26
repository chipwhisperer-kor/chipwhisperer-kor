# PicoScope 3418E

이 디렉터리는 워크스테이션에 연결된 Pico Technology **PicoScope 3418E**만 다룬다.
시리얼 `10561/0034`, 드라이버 API는 3000E용 **`psospa`**.

| 항목 | 값 |
|------|-----|
| 모델 | PicoScope 3418E (아날로그 4채널, MSO 아님) |
| USB | SuperSpeed 5 Gb/s, `0ce9:1020` |
| 대역폭 | 500 MHz (8-bit) |
| 최대 샘플 | 5 GS/s (1채널 8-bit) / 2.5 GS/s (10-bit) |
| 메모리 | 2 GS (8-bit) / 1 GS (10-bit) |
| 분해능 | 8-bit 또는 10-bit FlexRes |
| AWG | 전면 BNC, 200 MS/s 14-bit |
| 트리거 보조 | 전면 AUX I/O |
| 교정 | 19 Jun 2024 |

전면: 채널 A–D, AUX, AWG. 각 BNC에 RGB LED가 있다.

## 확인된 상태

드라이버로 장치를 열었고, 전면 LED를 쓸 수 있고, 채널 A 블록 캡처가 끝난다.
열린 입력에서 8-bit ±2 V 범위의 LSB(약 15.6 mV) 계단이 보이면 ADC 경로가 살아있는 것이다.

PicoScope 7 GUI **7.2.24.9932** 와 `libpsospa` 1.1.7, USB udev 규칙이 이 호스트에 설치되어 있다.

## 사용

```bash
source .venv/bin/activate          # 최초 1회: uv venv .venv && uv pip install -r requirements.txt
./scripts/enable-usb.sh            # 재연결 직후 USB 쓰기 권한
python identify_scope.py           # 모델·시리얼·펌웨어
python flash_leds.py               # 전면 LED가 A→AWG 순으로 깜빡이면 이 상자
python capture_block.py            # 채널 A 블록 캡처 → captures/chA_block.png
```

USB udev 규칙 `/etc/udev/rules.d/95-pico.rules` 가 이미 설치되어 있어, 재연결 후에도 권한이 유지되어야 한다.
그래도 장치가 안 열리면 `./scripts/enable-usb.sh`.

시스템 드라이버는 `/opt/picoscope/lib/libpsospa.so` 이다. Python 스크립트는 `.vendor` 가 있으면 그쪽을 먼저 쓴다.

## 첫 측정

1. **LED** — `flash_leds.py` 동안 본체의 A, B, C, D, AUX, AWG LED가 차례로 켜지는지 본다.
2. **열린 채널** — 프로브 없이 `capture_block.py`. 수 mV–수십 mV의 양자화 잡음이면 정상.
3. **AWG 루프백** — 짧은 BNC 케이블로 **AWG → 채널 A**. 다시 `capture_block.py`.
   10 kHz, 1 Vpk-pk 정현파가 보여야 한다. AWG 출력은 50 Ω.
4. **프로브** — 채널 A에 패시브 프로브를 꽂고 1×/10× 스위치를 프로브와
   소프트웨어 감쇠가 같게 맞춘다. 3418E 입력은 1 MΩ 또는 50 Ω.

캡처 스크립트는 AWG를 켜 둔 채 채널 A를 10 MS/s, 10 k샘플로 한 번 뜬다.
트리거가 없으면 100 ms 후 강제 캡처한다.

## PicoScope 7 (대화형 GUI)

설치된 버전은 **7.2.24.9932** 이다. 앱 목록의 “PicoScope 7” 또는:

```bash
picoscope
```

apt 저장소는 `/etc/apt/sources.list.d/picoscope7.list` 이다.
Ubuntu 26.04는 Pico 공식 지원 목록(22.04/24.04) 밖이지만, 이 호스트에서는
패키지가 설치되고 GUI 프로세스가 기동했다. GTK 경고가 나와도 창이 뜨면 무시한다.

시작 후에도 장치가 안 보이면 USB를 뽑았다가 꽂고, 후면 USB-C 전원을 연결한 뒤
`./scripts/enable-usb.sh` 를 실행한다.

## 전원

3418E는 USB-C 3 A 또는 동봉 PS017(후면 USB-C 전원)을 권장한다.
지금은 USB 3.0 허브 두 단을 거쳐 SuperSpeed로 열려 있고
`powerErrorLikely=0`이다. 캡처가 끊기거나 장치가 사라지면 후면 전원을 연결한다.
