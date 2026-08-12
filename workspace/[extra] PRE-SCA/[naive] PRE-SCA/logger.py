"""에뮬레이션 명령어와 실행 전·후 레지스터 상태를 CSV로 기록한다.

`TraceLogger`는 메모리 버퍼와 명령어 캐시를 관리하고, 레거시 호출부를 위해 모듈 수준
함수와 `LOG_MATRIX`를 유지한다. import 시 단일 로거를 생성하며 로그 디렉터리를 만드는
부작용이 있다. CSV 쓰기에 실패하면 오류를 출력하고 다음 실행을 위해 버퍼를
초기화한다.
"""

import os
import csv
import datetime
from typing import List, Any, Dict, Tuple, Optional

from unicorn import Uc
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_FP,
    UC_ARM_REG_IP, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR
)

from config import log_file_name
import setEmulData

# -----------------------------------------------------------------------------
# 모듈 공용 상태 — 레거시 호환용
# -----------------------------------------------------------------------------
# `emul.py`가 정상 실행의 주소 순서를 Faulty 실행 주입점과 대조하므로 전역 이름을 유지한다.
LOG_MATRIX: List[List[Any]] = []

# -----------------------------------------------------------------------------
# 레지스터 트레이스 로거
# -----------------------------------------------------------------------------
class TraceLogger:
    """명령어 흐름과 실행 전·후 레지스터 값을 버퍼에 모아 CSV로 저장한다.

    호출부는 `set_file_index()`로 출력 파일을 정한 뒤 명령어마다 `log_state()`를
    호출한다. 종료 주소에 도달하면 CSV를 쓰고 버퍼를 비운다. 명령어 목록이 없으면
    opcode와 operand는 `UNKNOWN`으로 기록한다.
    """
    
    REGISTERS = [
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_FP,
        UC_ARM_REG_IP, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
        UC_ARM_REG_CPSR
    ]

    HEADER = ['ctr', 'Address', 'Opcode', 'Operands',
              'bR0', 'bR1', 'bR2', 'bR3', 'bR4', 'bR5', 'bR6', 'bR7', 'bR8', 'bR9', 'bR10',
              'bFP', 'bIP', 'bSP', 'bLR', 'bPC', 'bCPSR',
              'aR0', 'aR1', 'aR2', 'aR3', 'aR4', 'aR5', 'aR6', 'aR7', 'aR8', 'aR9', 'aR10',
              'aFP', 'aIP', 'aSP', 'aLR', 'aPC', 'aCPSR']

    def __init__(self):
        """타임스탬프 로그 디렉터리와 빈 레지스터 버퍼를 만든다.

        import 시 단일 인스턴스가 생성되므로 디렉터리 생성이 부작용이다. 권한·경로 오류는
        호출자에게 전파되며 CSV는 아직 만들지 않는다.
        """
        self.ctr: int = 0
        self.current_log_matrix: List[List[Any]] = []
        self.log_file_path: str = ""
        
        # 주소별 조회가 명령어마다 일어나므로 목록을 한 번만 사전으로 바꾼다.
        self._insn_cache: Dict[int, Tuple[str, str]] = {}
        self._is_cache_built: bool = False

        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        self.log_folder = os.path.join("./log", f"{self.timestamp} {log_file_name}")
        os.makedirs(self.log_folder, exist_ok=True)
        
        self.reset_buffer()

    def reset_buffer(self):
        """현재 로그를 헤더 한 행으로 되돌리고 명령어 카운터를 0으로 만든다."""
        self.current_log_matrix = [self.HEADER[:]]
        self.ctr = 0

    def set_file_index(self, index: int):
        """실행 차수 0은 정상, 그 외는 Faulty 레지스터 로그 경로로 선택한다.

        경로 문자열만 바꾸며 파일은 쓰지 않는다.
        """
        filename = f"{self.timestamp} LogReg.csv" if index == 0 else f"{self.timestamp} LogReg_Faulty.csv"
        self.log_file_path = os.path.join(self.log_folder, filename)

    def get_log_file_path(self) -> str:
        """현재 실행 차수에 선택된 레지스터 로그 경로를 반환한다."""
        return self.log_file_path

    def _ensure_insn_cache(self):
        """공용 디스어셈블 목록을 주소별 `(opcode, operands)` 캐시로 한 번 변환한다."""
        if not self._is_cache_built and setEmulData.instructions:
            for item in setEmulData.instructions:
                self._insn_cache[item[0]] = (item[1], item[2])
            self._is_cache_built = True

    def get_instruction_info(self, address: int) -> Tuple[str, str]:
        """주소의 `(opcode, operands)`를 반환하고 캐시에 없으면 UNKNOWN 쌍을 반환한다."""
        self._ensure_insn_cache()
        return self._insn_cache.get(address, ("UNKNOWN", "UNKNOWN"))

    def read_registers(self, uc: Uc) -> List[int]:
        """추적 대상 18개 Unicorn 레지스터 값을 헤더와 같은 순서로 반환한다.

        에뮬레이터를 변경하지 않으며 읽기 실패는 Unicorn 예외로 전파된다.
        """
        return [uc.reg_read(reg) for reg in self.REGISTERS]

    def log_state(self, uc: Uc, address: int):
        """현재 명령어 실행 전 상태를 버퍼에 추가하고 직전 행의 실행 후 값을 완성한다.

        `_exit` 주소에 도달하면 정상 실행 주소 대조용 `LOG_MATRIX`에 복사하고 현재 파일을
        덮어쓴 뒤 버퍼를 초기화한다. CSV 쓰기 실패는 오류를 출력하지만 다음 실행을 위해
        버퍼는 초기화한다. 로거 전역·파일을 변경하고 반환값은 없다.
        """
        global LOG_MATRIX

        regs = self.read_registers(uc)
        opcode, op_str = self.get_instruction_info(address)

        row = [self.ctr, hex(address), opcode, op_str] + regs
        self.current_log_matrix.append(row)

        # 현재 hook의 실행 전 값은 직전 명령어의 실행 후 값이기도 하다.
        if self.ctr >= 1:
            self.current_log_matrix[self.ctr].extend(regs)

        self.ctr += 1

        # Thumb 실행 주소에는 심볼 주소의 모드 비트가 포함되지 않는다.
        target_exit = setEmulData.exit_addr_real - (1 if setEmulData.MODE == 2 else 0)
        
        if address == target_exit:
            LOG_MATRIX.extend(self.current_log_matrix)
            
            try:
                with open(self.log_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(self.current_log_matrix)
            except IOError as e:
                print(f"Error writing log file: {e}")

            self.reset_buffer()


# -----------------------------------------------------------------------------
# 단일 로거 인스턴스
# -----------------------------------------------------------------------------
_logger_instance = TraceLogger()

# -----------------------------------------------------------------------------
# `emul.py`와의 호환을 위한 모듈 API
# -----------------------------------------------------------------------------
def make_log_file(i):
    """호환 API: 실행 차수 0은 정상, 그 외는 Faulty 로그 파일명으로 선택한다."""
    _logger_instance.set_file_index(i)

def get_log_file_name():
    """호환 API: 현재 선택된 레지스터 로그 경로를 반환한다."""
    return _logger_instance.get_log_file_path()

def ret_all_reg(uc):
    """호환 API: Unicorn의 추적 대상 레지스터 값을 정의된 순서로 반환한다."""
    return _logger_instance.read_registers(uc)

def print_instruction(addr):
    """호환 API: 주소의 `(opcode, operands)`를 반환하고 없으면 UNKNOWN을 쓴다."""
    return _logger_instance.get_instruction_info(addr)

def write_log_regs(uc, address, scene_data):
    """호환 API: 현재 명령어 실행 전 CPU 상태를 로거 버퍼에 기록한다.

    `scene_data`는 과거 호출 시그니처를 유지하기 위한 인자이며 사용하지 않는다. 종료
    주소에 도달하면 CSV를 쓰고 버퍼를 초기화한다.
    """
    _logger_instance.log_state(uc, address)
