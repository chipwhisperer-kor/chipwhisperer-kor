# 편의성 도구 - VMware tools 설치 (Ubuntu 터미널 명령어)
```
sudo apt update
sudo apt install open-vm-tools
sudo apt install open-vm-tools-desktop
sudo reboot
```

# 편의성 도구 - 공유 폴더 활성화 (VMware 설정)
 - VMware 메뉴 → VM → Settings → Options → Shared Folders
 - Always enabled 선택
 - 공유할 폴더 추가

# 편의성 도구 - 공유 폴더 활성화 (Ubuntu 터미널 명령어)
```
sudo mkdir -p /mnt/hgfs
sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other
ls /mnt/hgfs
ln -s /mnt/hgfs ~/Desktop/hgfs
```

# 편의성 도구 - 한글 입력기 설치 (Ubuntu 터미널 명령어)
```
sudo apt update
sudo apt install ibus ibus-hangul
ibus restart
```

# 편의성 도구 - 시스템 설정에서 한글 추가 (Ubuntu 설정)
 - 설정(Settings) → 키보드(Keyboard) → 입력 소스(Input Sources)
 - '+' 버튼 클릭
 - Korean → Korean (Hangul) 선택 후 추가
 - 단축키 꼬일 수 있으므로 다 지우고 필수만 남기기 (기본 : Shift + Space)

# (필요 시 사용) 파일 및 폴더 권한 설정 - 홈 폴더 및 하위 폴더 전부 (Ubuntu 터미널 명령어)
```
sudo chmod -R 777 ~
```

# (필요 시 사용) 네트워크 IP 갱신 (Ubuntu 터미널 명령어)
```
sudo dhclient
```

# 도커 설치 - 기존 패키지 제거 (Ubuntu 터미널 명령어)
```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

# 도커 설치 - 필수 패키지 설치 (Ubuntu 터미널 명령어)
```
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
```

# 도커 설치 - Docker 공식 GPG 키 추가 (Ubuntu 터미널 명령어)
```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

# 도커 설치 - Docker 저장소 추가 (Ubuntu 터미널 명령어)
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```  
  
# 도커 설치 - Docker 설치 (Ubuntu 터미널 명령어)
```
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

# 도커 설치 - sudo 없이 Docker 사용 (Ubuntu 터미널 명령어)
```
sudo usermod -aG docker $USER
newgrp docker
```

# 도커 컨테이너 생성
```
cd ~/setup/
docker compose down
docker compose up -d --build
```

# chipwhisperer 하드웨어 udev 규칙 생성 및 그룹 권한 부여
 - ~/setup/50-newae.rules :  칩위스퍼러 깃허브 Commit f618563
```
sudo cp ~/setup/cw-build/50-newae.rules /etc/udev/rules.d/50-newae.rules
sudo udevadm control --reload-rules
sudo groupadd -fr chipwhisperer # new systemd versions require system accounts for udev
sudo usermod -aG chipwhisperer $USER
sudo usermod -aG plugdev $USER
sudo reboot
```


# 브라우저 VS Code 웹 버전 실행
 - App Center → chromium 권장
 - 또는 ```sudo snap install chromium```
 - http://localhost:8080


