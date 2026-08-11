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
# emul.py 등 외부 모듈에서 직접 참조하는 전역 변수(LOG_MATRIX)와의 호환성을 위해 유지합니다.
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
        self.ctr: int = 0
        self.current_log_matrix: List[List[Any]] = []
        self.log_file_path: str = ""
        
        # 명령어 검색 최적화를 위한 캐시 (List -> Dict 변환)
        self._insn_cache: Dict[int, Tuple[str, str]] = {}
        self._is_cache_built: bool = False

        # 로그 디렉토리 생성
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        self.log_folder = os.path.join("./log", f"{self.timestamp} {log_file_name}")
        os.makedirs(self.log_folder, exist_ok=True)
        
        self.reset_buffer()

    def reset_buffer(self):
        """로그 버퍼를 초기화합니다."""
        self.current_log_matrix = [self.HEADER[:]]
        self.ctr = 0

    def set_file_index(self, index: int):
        """실행 차수(Normal/Faulty)에 따라 로그 파일명을 설정합니다."""
        filename = f"{self.timestamp} LogReg.csv" if index == 0 else f"{self.timestamp} LogReg_Faulty.csv"
        self.log_file_path = os.path.join(self.log_folder, filename)

    def get_log_file_path(self) -> str:
        return self.log_file_path

    def _ensure_insn_cache(self):
        """setEmulData의 명령어 리스트를 딕셔너리로 변환하여 검색 성능을 O(N)에서 O(1)로 최적화합니다."""
        if not self._is_cache_built and setEmulData.instructions:
            for item in setEmulData.instructions:
                # 항목 구조: [주소, 명령어, 피연산자 문자열]
                self._insn_cache[item[0]] = (item[1], item[2])
            self._is_cache_built = True

    def get_instruction_info(self, address: int) -> Tuple[str, str]:
        """주소에 해당하는 명령어 정보를 반환합니다."""
        self._ensure_insn_cache()
        return self._insn_cache.get(address, ("UNKNOWN", "UNKNOWN"))

    def read_registers(self, uc: Uc) -> List[int]:
        """모든 타겟 레지스터의 값을 읽어옵니다."""
        return [uc.reg_read(reg) for reg in self.REGISTERS]

    def log_state(self, uc: Uc, address: int):
        """현재 CPU 상태를 버퍼에 기록하고, 종료 조건 시 파일로 저장합니다."""
        global LOG_MATRIX

        # 1. 현재 상태 캡처
        regs = self.read_registers(uc)
        opcode, op_str = self.get_instruction_info(address)

        # 2. 로그 데이터 구성 [ctr, Address, Opcode, Operands, bR0...bCPSR]
        row = [self.ctr, hex(address), opcode, op_str] + regs
        self.current_log_matrix.append(row)

        # 3. 'After' 레지스터 업데이트 로직 (이전 행의 뒷부분에 현재 레지스터 값을 붙임)
        # 현재 단계의 레지스터 값(regs)은 이전 단계(ctr-1)의 '실행 후' 값이다.
        if self.ctr >= 1:
            # 이전 행(self.ctr)에 현재 레지스터 값들을 추가
            # 0번 항목이 헤더이므로 `self.ctr`가 이전 데이터 행의 인덱스와 일치한다.
            self.current_log_matrix[self.ctr].extend(regs)

        self.ctr += 1

        # 4. 종료 지점 도달 시 파일 쓰기 및 전역 매트릭스 백업
        # 주의: Thumb 모드일 경우 exit_addr_real에서 1을 뺀 주소가 실행 주소임
        target_exit = setEmulData.exit_addr_real - (1 if setEmulData.MODE == 2 else 0)
        
        if address == target_exit:
            # 시나리오 검증을 위해 전역 LOG_MATRIX에 백업 (기존 로직 유지)
            LOG_MATRIX.extend(self.current_log_matrix)
            
            try:
                with open(self.log_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(self.current_log_matrix)
            except IOError as e:
                print(f"Error writing log file: {e}")

            # 다음 실행을 위해 초기화
            self.reset_buffer()


# -----------------------------------------------------------------------------
# 단일 로거 인스턴스
# -----------------------------------------------------------------------------
_logger_instance = TraceLogger()

# -----------------------------------------------------------------------------
# `emul.py`와의 호환을 위한 모듈 API
# -----------------------------------------------------------------------------
def make_log_file(i):
    _logger_instance.set_file_index(i)

def get_log_file_name():
    return _logger_instance.get_log_file_path()

def ret_all_reg(uc):
    return _logger_instance.read_registers(uc)

def print_instruction(addr):
    return _logger_instance.get_instruction_info(addr)

def write_log_regs(uc, address, scene_data):
    # scene_data는 현재 로깅 로직 내부에서 직접 사용되지 않으나, 
    # 호출 시그니처 호환성을 위해 유지합니다.
    _logger_instance.log_state(uc, address)
