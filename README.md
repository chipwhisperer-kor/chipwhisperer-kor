# 🔬 ChipWhisperer-KOR

> ChipWhisperer 분석 플랫폼 한국어 버전

---

## 📋 목차

1. [환경 개요](#-환경-개요)
2. [VMware Tools 설치](#1-vmware-tools-설치)
3. [공유 폴더 설정](#2-공유-폴더-설정)
4. [한글 입력기 설치](#3-한글-입력기-설치)
5. [기타 유틸리티](#4-기타-유틸리티)
6. [Docker 설치](#5-docker-설치)
7. [컨테이너 실행](#6-컨테이너-실행)
8. [ChipWhisperer 하드웨어 설정](#7-chipwhisperer-하드웨어-설정)
9. [VS Code 웹 IDE 실행](#8-vs-code-웹-ide-실행)

---

## 🖥 환경 개요

모든 설정은 Ubuntu 게스트 OS를 기준으로 작성되었습니다. 사용 시 폴더 경로는 수정이 필요합니다.

---

## 1. VMware Tools 설치

호스트-게스트 간 클립보드 공유, 화면 해상도 자동 조정 등 편의 기능을 활성화합니다.

```bash
sudo apt update
sudo apt install open-vm-tools
sudo apt install open-vm-tools-desktop
sudo reboot
```

---

## 2. 공유 폴더 설정

### 2-1. VMware 설정 (GUI)

호스트와 파일을 공유하려면 먼저 VMware에서 공유 폴더를 활성화합니다.

```
VMware 메뉴 → VM → Settings → Options → Shared Folders
→ Always enabled 선택
→ 공유할 폴더 추가
```

### 2-2. Ubuntu 마운트 (터미널)

공유 폴더를 파일시스템에 마운트하고, 바탕화면에 바로가기를 생성합니다.

```bash
sudo mkdir -p /mnt/hgfs
sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other
ls /mnt/hgfs
ln -s /mnt/hgfs ~/Desktop/hgfs
```

---

## 3. 한글 입력기 설치

### 3-1. 패키지 설치 (터미널)

```bash
sudo apt update
sudo apt install ibus ibus-hangul
ibus restart
```

### 3-2. 시스템 설정 (GUI)

```
설정(Settings) → 키보드(Keyboard) → 입력 소스(Input Sources)
→ '+' 버튼 클릭
→ Korean → Korean (Hangul) 선택 후 추가
```

> **💡 Tip:** 단축키 충돌 방지를 위해 기존 입력 소스를 모두 제거하고, 기본 단축키인 `Shift + Space` 만 남기는 것을 권장합니다.

---

## 4. 기타 유틸리티

### 파일 및 폴더 권한 일괄 설정

접근 권한 문제가 발생할 경우에만 사용합니다.

```bash
sudo chmod -R 777 ~
```

### 네트워크 IP 갱신

네트워크 연결이 끊기거나 IP 할당에 문제가 생겼을 때 사용합니다.

```bash
sudo dhclient
```

---

## 5. Docker 설치

### 5-1. 기존 패키지 제거

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### 5-2. 필수 패키지 설치

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
```

### 5-3. Docker 공식 GPG 키 추가

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### 5-4. Docker 저장소 추가

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 5-5. Docker 엔진 설치

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 5-6. sudo 없이 Docker 사용

매번 `sudo`를 입력하지 않아도 되도록 현재 사용자를 docker 그룹에 추가합니다.

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 6. 컨테이너 실행

분석 환경 컨테이너를 빌드하고 백그라운드로 실행합니다.

```bash
cd ~/setup/
docker compose down
docker compose up -d --build
```

---

## 7. ChipWhisperer 하드웨어 설정

ChipWhisperer 장비를 USB로 연결했을 때 권한 없이 접근할 수 있도록 udev 규칙과 그룹 권한을 설정합니다.

> `~/setup/50-newae.rules` 파일은 ChipWhisperer 공식 저장소 Commit `f618563` 기준입니다.

```bash
sudo cp ~/setup/cw-build/50-newae.rules /etc/udev/rules.d/50-newae.rules
sudo udevadm control --reload-rules
sudo groupadd -fr chipwhisperer
sudo usermod -aG chipwhisperer $USER
sudo usermod -aG plugdev $USER
sudo reboot
```

---

## 8. VS Code 웹 IDE 실행

브라우저 기반의 VS Code 환경에 접속합니다. Chromium 브라우저를 권장합니다.

```bash
# Chromium이 설치되어 있지 않은 경우
sudo snap install chromium
```

브라우저 주소창에 아래 URL을 입력합니다.

```
http://localhost:8080
```

---

## 📦 백업

변경 사항을 GitHub에 백업할 때는 아래 명령어를 사용합니다.

```bash
git add . && git commit -m "backup $(date '+%F_%T')" && git push
```
