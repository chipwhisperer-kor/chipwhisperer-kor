import os

# -----------------------------------------------------------------------------
# Path Configuration
# -----------------------------------------------------------------------------
# 현재 파일(config.py)의 위치를 기준으로 프로젝트 루트 디렉토리를 계산합니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------------------------------------------------
# Global Configuration Constants
# -----------------------------------------------------------------------------
# 주의: 아래 변수명들은 elfParser, emul, logger 모듈에서 직접 참조하므로
# 리팩토링 시 이름을 변경하지 마십시오.

log_file_name = "tiny-AES_rand"

# Absolute Paths
# 호환성을 위해 변수명은 snake_case를 유지합니다.
elf_file = os.path.join(BASE_DIR, "source", "tiny-aes")
log_vir_in_file = os.path.join(BASE_DIR, "ini_set", "LogVirIN.csv")
fault_reg_file = os.path.join(BASE_DIR, "ini_set", "LogFI.csv")

# Emulation Parameters
BUFFER_BLOCK = 16   # 입력 데이터 블록 크기 (Bytes)
BUFFER_NUM = 10     # 처리할 블록(행)의 개수