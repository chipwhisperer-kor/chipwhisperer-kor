# ----------------------------------------------------------------------------
# ChipWhisperer Dockerfile
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
# - libusb-1.0-0-dev: 칩위스퍼러 하드웨어 통신
# - gcc-arm-none-eabi, avr-libc 등: 타겟 보드 펌웨어 컴파일용
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    make \
    curl \
    sudo \
    udev \
    libusb-1.0-0-dev \
    gcc-arm-none-eabi \
    libnewlib-arm-none-eabi \
    gcc-avr \
    avr-libc \
    usbutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 칩위스퍼러 및 주피터 환경 설치
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && rm requirements.txt

# Code-Server 설치 및 확장 프로그램
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    code-server --install-extension ms-python.python && \
    code-server --install-extension ms-toolsai.jupyter && \
    code-server --install-extension DavidAnson.vscode-markdownlint && \
    code-server --install-extension ms-vscode.cpptools-themes


EXPOSE 8080

CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none", "/workspace"]
