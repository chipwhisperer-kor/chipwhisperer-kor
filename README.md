# 🔬 ChipWhisperer-KOR

> [ChipWhisperer](https://www.chipwhisperer.com/) 분석 플랫폼 한국어 학습·실습 환경

ChipWhisperer-KOR은 부채널 분석(SCA)과 오류주입(FA) 실습을 위한 **한국어 Jupyter 노트북**, **Docker 기반 개발 환경**, **펌웨어·HAL 공통 자료**를 한 저장소에 모아 둔 프로젝트입니다. VMware Ubuntu 게스트 OS에서 ChipWhisperer 하드웨어를 연결하고, 브라우저 기반 VS Code(code-server)로 노트북을 실행하는 워크플로를 기준으로 구성되어 있습니다.

> **📌 `[extra]` 폴더:** 이름에 `[extra]`가 붙은 디렉터리는 공식 ChipWhisperer 튜토리얼과 무관한 **연구·실험 프로젝트**입니다. 학습 경로와 구분하여 참고하세요.

**저장소:** [github.com/chipwhisperer-kor/chipwhisperer-kor](https://github.com/chipwhisperer-kor/chipwhisperer-kor)

---

## 📋 목차

1. [주요 구성](#-주요-구성)
2. [사전 요구사항](#-사전-요구사항)
3. [빠른 시작](#-빠른-시작)
4. [저장소 구조](#-저장소-구조)
5. [튜토리얼 안내](#-튜토리얼-안내)
6. [컨테이너 환경](#-컨테이너-환경)
7. [환경 설정](#-환경-설정)
   - [VMware Tools 설치](#1-vmware-tools-설치)
   - [공유 폴더 설정](#2-공유-폴더-설정)
   - [한글 입력기 설치](#3-한글-입력기-설치)
   - [기타 유틸리티](#4-기타-유틸리티)
   - [Docker 설치](#5-docker-설치)
   - [ChipWhisperer 하드웨어 설정](#6-chipwhisperer-하드웨어-설정)
   - [컨테이너 실행](#7-컨테이너-실행)
   - [VS Code 웹 IDE 접속](#8-vs-code-웹-ide-접속)
8. [컨테이너 운영](#-컨테이너-운영)
9. [문제 해결](#-문제-해결)
10. [보안 주의사항](#-보안-주의사항)
11. [Git 동기화](#-git-동기화)
12. [라이선스 및 참고 자료](#-라이선스-및-참고-자료)

---

## ✨ 주요 구성

| 구성 요소 | 설명 |
|-----------|------|
| **한국어 튜토리얼** | SCA·FA·TraceWhisperer·Husky 와이어태핑 등 단계별 Jupyter 노트북 |
| **Docker 환경** | Python 3.9 + ChipWhisperer + Jupyter + code-server 일괄 제공 |
| **펌웨어·HAL** | `workspace/base/` — STM32F3, XMEGA, AVR 등 타겟 보드 빌드 자료 |
| **발표 자료** | `Marp with LaTeX.css/` — Marp + LaTeX.css 기반 한국어 슬라이드 |
| **연구 프로젝트** | `[extra] PRE-SCA/` — 사전(pre-silicon) 부채널·오류 분석 실험 |

---

## 🧰 사전 요구사항

- **호스트:** VMware Workstation/Player (또는 호환 가상화 환경)
- **게스트 OS:** Ubuntu (README의 명령어는 Ubuntu 기준)
- **하드웨어:** ChipWhisperer 장비 (Lite, Husky, CW308 타겟 보드 등 — 튜토리얼별 상이)
- **USB 패스스루:** 가상 머신에 ChipWhisperer USB 장치가 연결되어야 함
- **네트워크:** Docker 이미지 빌드·패키지 설치를 위한 인터넷 연결

> 모든 상대경로 명령어(`./setup/` 등)는 **저장소 루트 디렉터리**에서 실행합니다.

---

## 🚀 빠른 시작

전체 환경이 처음이라면 아래 순서를 따릅니다. 상세 절차는 [환경 설정](#-환경-설정)을 참고하세요.

```text
1. 저장소 클론
2. VMware Tools · 공유 폴더 · 한글 입력기 설정 (선택)
3. Docker 설치
4. udev 규칙 적용 + chipwhisperer/plugdev 그룹 추가 → 재부팅
5. ChipWhisperer USB 연결 (VMware USB 패스스루 확인)
6. docker compose up -d --build
7. 브라우저에서 http://localhost:8080 접속
8. workspace/ 튜토리얼 노트북 실행
```

```bash
git clone https://github.com/chipwhisperer-kor/chipwhisperer-kor.git
cd chipwhisperer-kor

# udev + 그룹 설정 (1회)
sudo cp ./setup/50-newae.rules /etc/udev/rules.d/50-newae.rules
sudo udevadm control --reload-rules
sudo groupadd -fr chipwhisperer
sudo usermod -aG chipwhisperer,plugdev,docker $USER
sudo reboot

# 컨테이너 빌드·실행 (재부팅 후)
cd ./setup/
docker compose up -d --build
```

---

## 📁 저장소 구조

```text
chipwhisperer-kor/
├── README.md
├── LICENSE
├── setup/                          # 환경 구성
│   ├── docker-compose.yml
│   ├── 50-newae.rules              # ChipWhisperer USB udev 규칙
│   └── cw-build/
│       ├── Dockerfile
│       ├── requirements.txt        # Python 패키지 (chipwhisperer, jupyter 등)
│       └── extensions.txt          # code-server VS Code 확장 목록
├── workspace/                      # 실습 작업 공간 (컨테이너에 마운트)
│   ├── base/                       # HAL, crypto, simpleserial, 공통 셋업 노트북
│   ├── 1. SCA and FA/              # 부채널 분석·오류주입 입문
│   ├── 2. TraceWhisperer/          # Husky + STM32F3 TraceWhisperer 실습
│   ├── 3. Release the Husky/       # Husky 와이어태핑 실험
│   ├── [extra] PRE-SCA/            # 연구 프로젝트 (공식 튜토리얼과 무관)
│   └── traces/                     # 측정 trace 데이터 (*.h5)
└── Marp with LaTeX.css/            # 발표 슬라이드 템플릿·자료
    ├── 0. Template/
    ├── cw kor/
    └── cffi pytest/
```

---

## 📚 튜토리얼 안내

튜토리얼은 **권장 학습 순서**대로 배열되어 있습니다. 각 노트북은 셀 단위로 순차 실행하도록 작성되었습니다.

### 1. SCA and FA — 입문

| 노트북 | 주제 | 대상 |
|--------|------|------|
| `1.0.SCA_main.ipynb` | 부채널 분석(SCA) — 파형 수집부터 HDF5 저장까지 | ChipWhisperer 초심자 |
| `2.0.FA_main.ipynb` | 오류주입 공격(Fault Injection) 입문 | SCA 1강 완료 후 |

**핵심 흐름:** SimpleSerial 통신 검증 → 트리거·샘플 설정 → 파형 수집 → `*.h5` DB 저장·분석

### 2. TraceWhisperer

| 노트북 | 주제 | 대상 |
|--------|------|------|
| `1.0.TraceWhisperer_main.ipynb` | TraceWhisperer 종합 실습 | ChipWhisperer Husky + CW308/STM32F3 |

**핵심 흐름:** Husky 기반 하드웨어 트레이스 캡처·분석 (TraceWhisperer 도구 활용)

### 3. Release the Husky — 와이어태핑

| 노트북 | 주제 | 대상 |
|--------|------|------|
| `1.0.Wiretapping4SCA.ipynb` | 와이어태핑을 통한 SCA 파형 수집 | ChipWhisperer 2대 (Lite + Husky) |
| `2.0.Wiretapping4FA .ipynb` | 와이어태핑을 통한 FIA 파형 수집 | 1.0 완료 후 |

**핵심 흐름:** Lite(통신·프로그래밍) + Husky(수동 관측) 역할 분리 실험

### base/ — 공통 자료

| 경로 | 설명 |
|------|------|
| `Setup_Generic.ipynb` | scope·target 연결 및 기본 설정 |
| `My_Setup.ipynb` | 타겟 보드 바이너리 빌드 환경 초기화 |
| `hal/`, `crypto/`, `simpleserial/` | 펌웨어 컴파일용 HAL·암호 라이브러리 |

### [extra] PRE-SCA — 연구 프로젝트

| 노트북 | 설명 |
|--------|------|
| `PRE-SCA.ipynb` | Unicorn 기반 ARM 펌웨어 명령어 단위 트레이싱 및 오류주입 실험 (tiny-AES 대상) |

> 공식 ChipWhisperer 학습 경로와 별도입니다. `nb_output/`에 실험 결과 CSV가 저장됩니다.

### Marp with LaTeX.css/ — 발표 자료

Marp + LaTeX.css + Noto Serif KR 폰트로 작성한 한국어 슬라이드입니다. VS Code의 Marp 확장 또는 code-server에서 미리보기·PDF보내기가 가능합니다.

- `cw kor/presentation_SCA.md` — 부채널 분석 개요 발표
- `0. Template/presentation.md` — 슬라이드 작성 템플릿

---

## 🐳 컨테이너 환경

`setup/docker-compose.yml`이 정의하는 분석 환경입니다.

| 항목 | 값 |
|------|-----|
| 컨테이너 이름 | `chipwhisperer-kor` |
| 베이스 이미지 | `python:3.9-bookworm` |
| 웹 IDE | code-server (`http://localhost:8080`) |
| 작업 디렉터리 | `/workspace` ← `../workspace` 볼륨 마운트 |
| USB | `/dev/bus/usb` 직접 매핑 (`privileged: true`) |

**주요 Python 패키지** (`setup/cw-build/requirements.txt`):

`chipwhisperer`, `jupyter`, `numpy`, `matplotlib`, `h5py`, `pandas`, `phoenixAES`, `unicorn`, `capstone`, `lief`, `pyserial`, `libusb1` 등

**펌웨어 빌드 도구** (Dockerfile 내 apt):

`gcc-arm-none-eabi`, `gcc-avr`, `avr-libc`, `libusb-1.0-0-dev`, `build-essential`

**VS Code 확장** (`setup/cw-build/extensions.txt`):

Python, Jupyter, Pylance, 한국어 언어 팩, Marp, Draw.io, Docker, C/C++ 도구 등

---

## 🖥 환경 설정

모든 설정은 Ubuntu 게스트 OS를 기준으로 작성되었습니다. 경로·패키지명은 사용 환경에 맞게 조정할 수 있습니다.

---

### 1. VMware Tools 설치

호스트-게스트 간 클립보드 공유, 화면 해상도 자동 조정 등 편의 기능을 활성화합니다.

```bash
sudo apt update
sudo apt install open-vm-tools
sudo apt install open-vm-tools-desktop
sudo reboot
```

---

### 2. 공유 폴더 설정

#### 2-1. VMware 설정 (GUI)

```
VMware 메뉴 → VM → Settings → Options → Shared Folders
→ Always enabled 선택
→ 공유할 폴더 추가
```

#### 2-2. Ubuntu 마운트 (터미널)

```bash
sudo mkdir -p /mnt/hgfs
sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other
ls /mnt/hgfs
ln -s /mnt/hgfs ~/Desktop/hgfs
```

> **⚠️ 주의:** 위 마운트 명령어는 재부팅 시 초기화됩니다. 재부팅 후에는 `sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other` 를 다시 실행해야 합니다.

---

### 3. 한글 입력기 설치

#### 3-1. 패키지 설치 (터미널)

```bash
sudo apt update
sudo apt install ibus ibus-hangul
ibus restart
```

#### 3-2. 시스템 설정 (GUI)

```
설정(Settings) → 키보드(Keyboard) → 입력 소스(Input Sources)
→ '+' 버튼 클릭
→ Korean → Korean (Hangul) 선택 후 추가
```

> **💡 Tip:** 단축키 충돌 방지를 위해 기존 입력 소스를 모두 제거하고, 기본 단축키인 `Shift + Space` 만 남기는 것을 권장합니다.

---

### 4. 기타 유틸리티

#### 파일 및 폴더 권한 일괄 설정

접근 권한 문제가 발생할 경우에만 사용합니다.

> **⚠️ 주의:** 홈 디렉터리 전체의 권한을 777로 변경합니다. SSH 키·인증 파일 등 민감한 파일도 포함되므로 꼭 필요한 경우에만 사용하십시오.

```bash
sudo chmod -R 777 ~
```

#### 네트워크 IP 갱신

네트워크 연결이 끊기거나 IP 할당에 문제가 생겼을 때 사용합니다.

```bash
sudo dhclient
```

---

### 5. Docker 설치

#### 5-1. 기존 패키지 제거

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

#### 5-2. 필수 패키지 설치

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
```

#### 5-3. Docker 공식 GPG 키 추가

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### 5-4. Docker 저장소 추가

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### 5-5. Docker 엔진 설치

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 5-6. sudo 없이 Docker 사용

```bash
sudo usermod -aG docker $USER
newgrp docker
```

> **💡 참고:** `newgrp docker` 는 현재 터미널 세션에만 즉시 적용됩니다. 모든 터미널에서 적용되려면 로그아웃 후 재로그인이 필요합니다.

---

### 6. ChipWhisperer 하드웨어 설정

ChipWhisperer 장비를 USB로 연결했을 때 권한 없이 접근할 수 있도록 udev 규칙과 그룹 권한을 설정합니다. **컨테이너 실행 전에 먼저 적용해야 합니다.**

> `./setup/50-newae.rules` 파일은 ChipWhisperer 공식 저장소 Commit `f618563` 기준입니다.

```bash
sudo cp ./setup/50-newae.rules /etc/udev/rules.d/50-newae.rules
sudo udevadm control --reload-rules
sudo groupadd -fr chipwhisperer
sudo usermod -aG chipwhisperer $USER
sudo usermod -aG plugdev $USER
sudo reboot
```

재부팅 후 USB 장치 인식을 확인합니다.

```bash
lsusb | grep -i "2b3e\|NewAE"
ls -l /dev/cw_serial* 2>/dev/null
```

---

### 7. 컨테이너 실행

분석 환경 컨테이너를 빌드하고 백그라운드로 실행합니다.

```bash
cd ./setup/
docker compose down
docker compose up -d --build
```

첫 빌드는 패키지·확장 설치로 **수 분 이상** 소요될 수 있습니다.

---

### 8. VS Code 웹 IDE 접속

브라우저 기반 VS Code 환경에 접속합니다. Chromium 브라우저를 권장합니다.

```bash
# Chromium이 설치되어 있지 않은 경우
sudo snap install chromium
```

브라우저 주소창에 아래 URL을 입력합니다.

```
http://localhost:8080
```

접속 후 `workspace/` 폴더에서 튜토리얼 노트북(`.ipynb`)을 열고, 상단의 **Run All** 또는 셀 단위로 실행합니다.

---

## ⚙️ 컨테이너 운영

```bash
cd ./setup/

# 상태 확인
docker compose ps

# 로그 확인 (실시간)
docker compose logs -f

# 중지
docker compose down

# 재시작 (이미지 재빌드 없이)
docker compose restart

# 설정·패키지 변경 후 재빌드
docker compose up -d --build

# 컨테이너 내부 셸 접속
docker exec -it chipwhisperer-kor bash
```

`requirements.txt` 또는 `extensions.txt`를 수정한 경우 `docker compose up -d --build`로 이미지를 다시 빌드해야 변경 사항이 반영됩니다.

---

## 🔧 문제 해결

### ChipWhisperer가 인식되지 않음

1. VMware에서 USB 장치가 게스트 OS에 연결되어 있는지 확인합니다.
2. udev 규칙과 그룹 멤버십을 확인합니다.

```bash
groups | grep -E 'chipwhisperer|plugdev'
lsusb | grep 2b3e
```

3. 규칙 재적용 후 USB를 다시 연결합니다.

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 컨테이너 내부에서 USB 접근 실패

- 컨테이너가 `privileged: true`로 실행 중인지 확인합니다.
- 호스트(게스트 OS)에서 먼저 `lsusb`로 장치가 보이는지 확인한 뒤 컨테이너를 재시작합니다.

```bash
cd ./setup/ && docker compose restart
```

### `http://localhost:8080` 접속 불가

```bash
docker compose ps          # 포트 8080 매핑 확인
docker compose logs        # code-server 기동 오류 확인
ss -tlnp | grep 8080       # 포트 점유 여부 확인
```

### 노트북에서 `scope` 연결 오류

- `workspace/base/Setup_Generic.ipynb`의 연결 셀을 먼저 실행합니다.
- USB가 일시적으로 끊긴 경우, 노트북에 안내된 대로 scope를 재연결합니다.

```python
import chipwhisperer as cw
scope = cw.scope()
```

### 공유 폴더가 재부팅 후 사라짐

[2-2. Ubuntu 마운트](#2-2-ubuntu-마운트-터미널) 명령을 다시 실행하거나, `/etc/fstab`에 영구 마운트 설정을 추가합니다.

---

## 🔒 보안 주의사항

| 항목 | 설명 |
|------|------|
| **code-server 인증 없음** | `--auth none`으로 실행됩니다. **로컬 개발·실습 환경 전용**이며, 외부 네트워크에 노출하지 마세요. |
| **privileged 컨테이너** | USB 접근을 위해 호스트 장치에 대한 광범위한 권한을 사용합니다. |
| **chmod 777** | [4. 기타 유틸리티](#4-기타-유틸리티)의 권한 일괄 변경은 보안상 위험하므로 최후의 수단으로만 사용합니다. |

---

## 📦 Git 동기화

### 백업 (Push)

로컬 변경 사항을 GitHub에 업로드합니다.

```bash
git add . && git commit -m "backup $(date '+%F_%T')" && git push
```

### 복원 (Pull)

GitHub의 최신 내용을 로컬로 내려받습니다.

```bash
git pull
```

> `workspace/traces/`의 대용량 `.h5` 파일이나 `[extra]` 실험 출력물은 저장소 크기에 영향을 줄 수 있습니다. 필요 시 `.gitignore`로 제외하는 것을 권장합니다.

---

## 📄 라이선스 및 참고 자료

- **이 저장소:** [Apache License 2.0](LICENSE)
- **ChipWhisperer 공식:** [chipwhisperer.com](https://www.chipwhisperer.com/) · [GitHub — newaetech/chipwhisperer](https://github.com/newaetech/chipwhisperer)
- **TraceWhisperer:** [GitHub — newaetech/chipwhisperer-trace](https://github.com/newaetech/chipwhisperer-trace)
- **udev 규칙 출처:** ChipWhisperer 공식 저장소 Commit `f618563`