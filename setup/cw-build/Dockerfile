# ----------------------------------------------------------------------------
# ChipWhisperer 개발 환경 이미지
#
# 이 이미지는 ChipWhisperer(부채널/오류주입 분석) 작업을 위한 Python 3.9 기반
# 개발 환경이며, 아래 두 가지 방식으로 동시에 접속하여 개발할 수 있습니다.
#
#   1) 웹브라우저 접속
#      - 컨테이너 내부에서 code-server가 0.0.0.0:8080 으로 구동됩니다.
#      - host에 별도 설치 없이 브라우저로 http://<host>:8080 에 접속해 개발합니다.
#
#   2) host의 VS Code에서 직접 접속 (Dev Containers 확장 활용)
#      - host VS Code에 "Dev Containers" 확장을 설치한 뒤, 명령 팔레트에서
#        "Dev Containers: Attach to Running Container" 를 실행해 이 컨테이너에
#        붙어 개발합니다. (원격 세션 사용자: root)
#      - 접속 시 VS Code 서버가 컨테이너 내부(/root/.vscode-server)로 주입되어
#        실행되며, 본 파일 하단의 devcontainer.metadata 라벨에 명시된 확장이
#        원격 세션에 자동 설치됩니다.
#
# USB로 연결된 ChipWhisperer 하드웨어에 접근하기 위해 컨테이너는 root로 동작하며,
# 실행 시 privileged 권한과 USB 장치 매핑(/dev/bus/usb)이 필요합니다.
# ----------------------------------------------------------------------------
FROM python:3.9-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul

# 작업 환경 설정
WORKDIR /workspace

# 필수 시스템 의존성
# - build-essential, git, make: 빌드 및 소스 관리
# - libusb-1.0-0-dev, udev, usbutils: 칩위스퍼러 하드웨어(USB) 통신
# - gcc-arm-none-eabi, libnewlib-arm-none-eabi, gcc-avr, avr-libc: 타겟 보드 펌웨어 컴파일용
# - fonts-nanum: 한글 폰트
# - curl, ca-certificates: 외부 설치 스크립트/패키지의 HTTPS 다운로드
# - sudo: 컨테이너 내부에서의 권한 상승
# - openssh-client: 컨테이너 안에서 git over SSH 등 SSH 클라이언트 사용
# - procps(ps 명령), less: host VS Code가 주입하는 VS Code 서버의 프로세스 관리 및
#                          git/터미널 페이저 동작에 필요
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-nanum \
    build-essential \
    git \
    make \
    curl \
    ca-certificates \
    sudo \
    udev \
    libusb-1.0-0-dev \
    gcc-arm-none-eabi \
    libnewlib-arm-none-eabi \
    gcc-avr \
    avr-libc \
    usbutils \
    openssh-client \
    procps \
    less \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 칩위스퍼러 및 주피터 환경 설치
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && rm requirements.txt

# Code-Server 설치
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Code-Server 확장 프로그램 설치
# - extensions.txt 의 목록을 순회하며 설치 (requirements.txt 방식과 유사)
# - '#' 주석/빈 줄은 무시하고, CRLF(\r) 줄바꿈도 처리
# - 개별 확장 설치 실패 시 빌드를 중단하지 않고 경고만 출력
COPY extensions.txt .
RUN sed -e 's/\r$//' extensions.txt | while IFS= read -r ext; do \
        case "$ext" in \
            ''|\#*) continue ;; \
        esac; \
        echo ">>> Installing extension: $ext"; \
        code-server --install-extension "$ext" \
            || echo "!!! WARNING: failed to install extension: $ext"; \
    done \
    && rm extensions.txt

# ----------------------------------------------------------------------------
# host VS Code (Dev Containers) 접속 지원
# - "Attach to Running Container" 로 접속하면 VS Code 서버가
#   /root/.vscode-server 에 주입되어 동작하므로 해당 디렉터리를 미리 생성합니다.
# - /workspace 는 host의 디렉터리를 마운트해 사용하므로 파일 소유자(UID)가
#   컨테이너의 root와 달라, Git이 'dubious ownership' 으로 동작을 거부할 수
#   있습니다. 이를 방지하기 위해 모든 경로를 Git 신뢰 디렉터리로 등록합니다.
# ----------------------------------------------------------------------------
RUN mkdir -p /root/.vscode-server \
    && git config --global --add safe.directory '*'

# Dev Containers 확장이 컨테이너에 붙을 때 병합·적용하는 메타데이터.
# - remoteUser: 원격 세션 사용자 (root)
# - customizations.vscode.extensions: 원격 세션에 자동 설치할 확장 목록
#     (Python/Jupyter/C·C++/문서 작성 등 컨테이너 내부 개발용 확장 중심.
#      Docker·Containers 관리나 Remote-* 계열 등 host VS Code UI 전용 확장은
#      컨테이너 내부 세션에서 의미가 없으므로 제외)
# - customizations.vscode.settings: 원격 세션 기본 설정(파이썬 인터프리터, 터미널)
LABEL devcontainer.metadata='[{"remoteUser":"root","customizations":{"vscode":{"extensions":["bioinfo.markitdown-vscode","davidanson.vscode-markdownlint","hediet.vscode-drawio","marp-team.marp-vscode","moshfeu.compare-folders","ms-ceintl.vscode-language-pack-ko","ms-python.debugpy","ms-python.python","ms-python.vscode-pylance","ms-python.vscode-python-envs","ms-toolsai.jupyter","ms-toolsai.jupyter-keymap","ms-toolsai.jupyter-renderers","ms-toolsai.vscode-jupyter-cell-tags","ms-toolsai.vscode-jupyter-slideshow","ms-vscode.cmake-tools","ms-vscode.cpptools","ms-vscode.cpptools-extension-pack","ms-vscode.cpptools-themes","mushan.vscode-paste-image","naumovs.color-highlight","pranaygp.vscode-css-peek","saoudrizwan.claude-dev","tomoki1207.pdf","usernamehw.errorlens","yzane.markdown-pdf","yzhang.markdown-all-in-one"],"settings":{"python.defaultInterpreterPath":"/usr/local/bin/python","terminal.integrated.defaultProfile.linux":"bash"}}}}]'

EXPOSE 8080

CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none", "/workspace"]
