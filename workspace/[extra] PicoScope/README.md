# PicoScope 3418E

이 서브프로젝트는 Pico Technology **PicoScope 3418E**를 `psospa` API로 열어
식별하고, 전면 LED와 채널 A 블록 캡처를 독립적으로 점검한다. 장비별 시리얼,
교정일, 펌웨어와 드라이버 버전은 저장소에 고정하지 않고 `identify_scope.py`가
연결된 장치에서 읽는다.

## 편입 범위

현재 단계는 외부에서 가져온 PicoScope 도구를 이 저장소 안에서 재현 가능하게
실행하는 데까지만 포함한다. `workspace/3. Release the Husky`의 파일은 변경하지
않으며 두 프로젝트의 캡처 흐름도 아직 연결하지 않는다. 추후 융합은 이 디렉터리에
새 Jupyter 노트북을 추가하여 수행한다.

## 실행 환경 준비

저장소의 기본 Docker 컨테이너 또는 Python 3.10 이상과 해당 Python의 `venv`·`pip`
모듈이 있는 Linux x86-64 환경에서 이 디렉터리로 이동한 뒤 아래 명령을 한 번
실행한다. Debian/Ubuntu 호스트에서 `ensurepip` 오류가 나면 `python3-venv` 패키지가
필요하다. 가상환경과 내려받은 드라이버는 재생성 가능한 로컬 상태이므로 Git에서
제외된다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./scripts/fetch-psospa.sh
```

`fetch-psospa.sh`는 Pico가 배포하는 amd64 Debian 패키지에서 `libpsospa`만
`.vendor/`로 추출하므로 `curl`과 `dpkg-deb`가 필요하다. 설치 중 네트워크 오류,
패키지 형식 변경 또는 x86-64가 아닌 환경에서는 실패한다. 시스템에 PicoSDK가
설치되어 있으면 내려받기를 생략할 수 있다. 실행 코드는 프로젝트 로컬 드라이버를
우선 사용하고, 없으면 시스템 드라이버를 사용하며, 둘 다 없으면 실행 전에 실패한다.

## USB 권한

호스트에서 다음 udev 규칙을 한 번 설치한 뒤 규칙을 다시 읽고 장치를 재연결한다.
이 작업은 호스트 시스템을 변경하며 관리자 권한이 필요하다.

```bash
sudo install -m 0644 95-pico.rules /etc/udev/rules.d/95-pico.rules
sudo udevadm control --reload-rules
```

장치를 재연결할 수 없거나 규칙을 아직 설치하지 못했다면 호스트에서
`./scripts/enable-usb.sh`를 실행할 수 있다. 이 스크립트는 Pico USB 노드만 찾아
일시적으로 모든 사용자에게 쓰기 권한을 주며, 권한이 없을 때는 로컬 Docker를
특권 모드로 실행한다. 장치가 없거나 Docker를 사용할 수 없으면 0이 아닌 코드로
종료한다.

## 점검 순서

```bash
.venv/bin/python identify_scope.py
.venv/bin/python flash_leds.py
.venv/bin/python capture_block.py
```

1. `identify_scope.py`는 연결된 장치의 모델, 시리얼, USB, 교정, 펌웨어와 드라이버
   정보를 출력한다. 열 수 있는 장치가 없거나 권한·드라이버 문제가 있으면 실패한다.
2. `flash_leds.py`는 A, B, C, D, AUX, AWG LED를 차례로 점멸한 뒤 모두 끈다.
   장치를 눈으로 식별하기 위한 절차이며 측정 데이터는 만들지 않는다.
3. `capture_block.py`는 AWG를 활성화하고 채널 A를 한 번 캡처하여
   `captures/chA_block.csv`와 `captures/chA_block.png`를 덮어쓴다. 열린 입력도
   캡처할 수 있지만, 파형 경로까지 확인하려면 짧은 BNC 케이블로 AWG와 채널 A를
   연결한다.

세 명령은 모두 장치를 열고 설정한 뒤 정상·예외 종료 시 닫는다. 캡처 결과는 장비와
배선에 종속되고 다시 만들 수 있으므로 Git에서 제외한다. 장치가 실행 중 사라지거나
캡처가 불안정하면 USB 연결과 별도 전원 상태를 확인한다.
