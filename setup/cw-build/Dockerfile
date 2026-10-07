# ----------------------------------------------------------------------------
# ChipWhisperer 개발 환경 이미지
#
# 이 이미지는 ChipWhisperer(부채널/오류주입 분석) 작업을 위한 Python 3.12 기반
# 개발 환경이다. 아래 두 가지 방식으로 동시에 접속해 개발할 수 있다.
#
#   1) 웹브라우저 접속
#      - 컨테이너 내부에서 code-server가 0.0.0.0:8080으로 구동된다.
#      - host에 별도 설치 없이 브라우저로 http://<host>:8080에 접속해 개발한다.
#
#   2) host의 VS Code에서 직접 접속 (Dev Containers 확장 사용)
#      - host VS Code에 "Dev Containers" 확장을 설치한 뒤, 명령 팔레트에서
#        "Dev Containers: Attach to Running Container" 를 실행해 이 컨테이너에
#        붙어 개발한다. 원격 세션 사용자는 root다.
#      - 접속 시 VS Code 서버가 컨테이너 내부(/root/.vscode-server)로 주입되어
#        실행되며, 본 파일 하단의 devcontainer.metadata 라벨에 명시된 확장이
#        원격 세션에 자동 설치된다.
#
# USB로 연결된 ChipWhisperer 하드웨어에 접근하기 위해 컨테이너는 root로 동작하며,
# 실행 시 privileged 권한과 USB 장치 매핑(/dev/bus/usb)이 필요하다.
# ----------------------------------------------------------------------------
# 파이썬 버전은 3.12 가 상한이다. chipwhisperer 6.0.0 이 numpy<=1.26.4 를 요구하는데
# numpy 1.26.4 에는 cp313 휠이 없어서, 3.13 이상에서는 설치 자체가 성립하지 않는다.
# (3.9 는 2025-10 EOL. setuptools 는 83 부터 3.10+ 를 요구하는 등 생태계가 이미 이탈했다.)
#
# 3.12 에서 stdlib distutils 가 제거된 것은 이 이미지에 영향이 없다. 런타임에 distutils
# 를 쓰는 곳은 unicorn 의 파이썬 2 전용 모듈뿐이라 py3 에서는 로드되지 않고, sdist 를
# 컴파일해야 하는 패키지는 fastdtw 하나인데 확장 빌드가 실패하면 순수 파이썬으로
# 자동 폴백한다. 아래 build-essential 은 그 폴백 이전 단계를 위해 유지한다.
FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul

# 작업 환경 설정
WORKDIR /workspace

# 필요한 시스템 패키지
# - build-essential, git, make: 펌웨어 빌드와 소스 관리에 쓴다.
# - libusb-1.0-0-dev, udev, usbutils: ChipWhisperer 하드웨어와 USB로 통신한다.
# - gcc-arm-none-eabi, libnewlib-arm-none-eabi, gcc-avr, avr-libc: 타겟 보드 펌웨어를 컴파일한다.
# - fonts-nanum: 한글 폰트다.
# - curl, ca-certificates: 외부 설치 스크립트와 패키지를 HTTPS로 내려받는다.
# - sudo: 컨테이너 안에서 권한을 올릴 때 쓴다.
# - openssh-client: 컨테이너 안에서 git over SSH 등 SSH 클라이언트를 쓴다.
# - procps(ps 명령), less: host VS Code가 주입하는 VS Code 서버의 프로세스 관리와
#                          git/터미널 페이저 동작에 필요하다.
# - libpsospa(/opt/picoscope): PicoScope 3418E 네이티브 드라이버. apt 저장소가 아니라 아래 별도
#                          RUN 에서 .deb 를 풀어 설치한다.
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

# PicoScope 3418E 네이티브 드라이버 libpsospa. requirements.txt 의 pypicosdk 가 /opt/picoscope/lib 를
# 기본 경로로 찾으므로 별도 경로 설정이 필요 없다.
# - dpkg -i 대신 dpkg-deb -x 로 푸는 이유: 이 .deb 의 postinst 가 `set -e` 아래에서
#   `udevadm control --reload-rules && udevadm trigger` 를 실행하는데, 이미지 빌드 중에는 udevd 가
#   없어 빌드가 실패한다. udev 규칙은 컨테이너가 아니라 host 의 몫이고(컨테이너는 privileged root 로
#   /dev/bus/usb 를 그대로 쓴다), 패키지 내용물은 /opt/picoscope 와 /usr/share/doc 뿐이라 풀기만 하면
#   같은 결과가 된다. ld.so.conf.d 등록은 postinst 가 하던 일을 그대로 옮긴 것이다.
# - 의존 패키지 중 libc6·libgcc-s1·libstdc++6 은 python:3.12-bookworm 에 이미 있고, libusb-1.0-0 은 위 apt 단계의
#   libusb-1.0-0-dev 가 함께 설치한다. 그래서 이 RUN 은 apt 단계 뒤에 온다.
# - 1.1.7 에 고정하는 이유: 노트북이 검증한 조합이 pypicosdk 1.7.5 + libpsospa 1.1.7 이다.
#   sha256 은 내려받은 파일이 바뀌지 않았는지 확인한다.
ARG LIBPSOSPA_DEB=libpsospa_1.1.7-0r5994_amd64.deb
RUN curl -fsSL -o /tmp/${LIBPSOSPA_DEB} \
        "https://labs.picotech.com/picoscope7/debian/pool/main/libp/libpsospa/${LIBPSOSPA_DEB}" \
    && echo "d26636136cdbe1ac389243a1a014951f5f838f57e77d64cbed37bbb00a137473  /tmp/${LIBPSOSPA_DEB}" | sha256sum -c - \
    && dpkg-deb -x /tmp/${LIBPSOSPA_DEB} / \
    && echo /opt/picoscope/lib > /etc/ld.so.conf.d/picoscope.conf \
    && ldconfig \
    && rm /tmp/${LIBPSOSPA_DEB}

# ChipWhisperer와 Jupyter 환경 설치
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && rm requirements.txt

# Code-Server 설치
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Code-Server 확장 프로그램 설치
# - extensions.txt의 목록을 순회하며 설치한다 (requirements.txt와 같은 방식이다).
# - '#' 주석과 빈 줄은 무시하고, CRLF(\r) 줄바꿈도 처리한다.
# - 개별 확장 설치가 실패해도 빌드를 중단하지 않고 경고만 출력한다.
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
#   /root/.vscode-server에 주입되어 동작하므로 해당 디렉터리를 미리 만든다.
# - /workspace 는 host의 디렉터리를 마운트해 사용하므로 파일 소유자(UID)가
#   컨테이너의 root와 달라, Git이 'dubious ownership'으로 동작을 거부할 수
#   있다. 이를 막기 위해 모든 경로를 Git 신뢰 디렉터리로 등록한다.
# ----------------------------------------------------------------------------
RUN mkdir -p /root/.vscode-server \
    && git config --global --add safe.directory '*'

# Dev Containers 확장이 컨테이너에 붙을 때 병합·적용하는 메타데이터.
# - remoteUser: 원격 세션 사용자다 (root).
# - customizations.vscode.extensions: 원격 세션에 자동 설치할 확장 목록이다.
#     Python/Jupyter/C·C++/문서 작성 등 컨테이너 내부 개발용 확장 중심이다.
#     Docker·Containers 관리나 Remote-* 계열 등 host VS Code UI 전용 확장은
#     컨테이너 내부 세션에서 의미가 없으므로 뺐다.
# - customizations.vscode.settings: 원격 세션 기본 설정이다 (파이썬 인터프리터, 터미널).
LABEL devcontainer.metadata='[{"remoteUser":"root","customizations":{"vscode":{"extensions":["bioinfo.markitdown-vscode","davidanson.vscode-markdownlint","hediet.vscode-drawio","moshfeu.compare-folders","ms-ceintl.vscode-language-pack-ko","ms-python.debugpy","ms-python.python","ms-python.vscode-pylance","ms-python.vscode-python-envs","ms-toolsai.jupyter","ms-toolsai.jupyter-keymap","ms-toolsai.jupyter-renderers","ms-toolsai.vscode-jupyter-cell-tags","ms-toolsai.vscode-jupyter-slideshow","ms-vscode.cmake-tools","ms-vscode.cpptools","ms-vscode.cpptools-extension-pack","ms-vscode.cpptools-themes","mushan.vscode-paste-image","naumovs.color-highlight","pranaygp.vscode-css-peek","saoudrizwan.claude-dev","tomoki1207.pdf","usernamehw.errorlens","yzane.markdown-pdf","yzhang.markdown-all-in-one"],"settings":{"python.defaultInterpreterPath":"/usr/local/bin/python","terminal.integrated.defaultProfile.linux":"bash"}}}}]'

EXPOSE 8080

CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none", "/workspace"]
