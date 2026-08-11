"""CSV로 정의한 Fault injection(오류주입) 시나리오를 적용한다.

`Scenario`는 레지스터 변경·비트 반전·명령어 건너뛰기 정보를 CSV에서 읽어 메모리에
보관한다. 시나리오 파일이 없으면 정상 모드로 계속하고, 파싱 오류는 출력한 뒤 읽은
항목만 유지한다. 실행 중 Unicorn 레지스터를 변경하는 것이 주요 부작용이다.
"""

import csv
import os
from typing import List, Dict, Any, Optional, Union

from unicorn import Uc, UcError
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_FP,
    UC_ARM_REG_IP, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR
)

import config
import setEmulData

class Scenario:
    """CSV 시나리오를 읽어 Unicorn 레지스터와 PC에 적용한다.

    초기화 시 `config.fault_reg_file`을 읽고 각 행을 실행 가능한 값으로 변환한다. 유효하지
    않은 행은 무시하며, 파일이 없으면 빈 시나리오를 만든다.
    """

    # CSV 컬럼 순서 및 레지스터 키 정의
    FIELD_NAMES = [
        'ctr', 'isNOP',
        'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10',
        'fp', 'ip', 'sp', 'lr', 'pc', 'cpsr'
    ]

    # 레지스터 이름과 Unicorn 상수 매핑
    REG_MAP = {
        'r0': UC_ARM_REG_R0, 'r1': UC_ARM_REG_R1, 'r2': UC_ARM_REG_R2, 'r3': UC_ARM_REG_R3,
        'r4': UC_ARM_REG_R4, 'r5': UC_ARM_REG_R5, 'r6': UC_ARM_REG_R6, 'r7': UC_ARM_REG_R7,
        'r8': UC_ARM_REG_R8, 'r9': UC_ARM_REG_R9, 'r10': UC_ARM_REG_R10,
        'fp': UC_ARM_REG_FP, 'ip': UC_ARM_REG_IP, 'sp': UC_ARM_REG_SP,
        'lr': UC_ARM_REG_LR, 'pc': UC_ARM_REG_PC, 'cpsr': UC_ARM_REG_CPSR
    }

    def __init__(self):
        self.fault_list: List[Dict[str, Any]] = []
        self._load_scenario_data()

    @property
    def Fault_list(self) -> List[Dict[str, Any]]:
        """레거시 외부 모듈이 사용하는 시나리오 목록 속성을 반환한다."""
        return self.fault_list

    def _load_scenario_data(self):
        """
        CSV 파일에서 오류 주입 시나리오를 로드하고 전처리합니다.
        문자열 데이터를 에뮬레이션 중에 즉시 사용할 수 있는 형태(int, bool)로 변환합니다.
        """
        if not os.path.exists(config.fault_reg_file):
            print("Notice: Fault injection file not found. Running in normal mode.")
            return

        try:
            with open(config.fault_reg_file, 'r', encoding='utf-8-sig') as f:
                # 레거시 파일 형식을 준수하기 위해 fieldnames 명시 (헤더 무시/재정의)
                # 첫 줄(헤더)은 건너뛰거나 DictReader의 특성을 고려하여 처리
                # 여기서는 레거시와 동일하게 첫 줄이 헤더임을 가정하고 strict parsing
                
                # 먼저 헤더를 읽어 넘김
                has_header = csv.Sniffer().has_header(f.read(1024))
                f.seek(0)
                
                if has_header:
                    next(f) # 헤더 스킵

                reader = csv.DictReader(f, fieldnames=self.FIELD_NAMES)

                for row in reader:
                    processed_row = self._preprocess_row(row)
                    if processed_row:
                        self.fault_list.append(processed_row)

        except Exception as e:
            print(f"Error loading fault scenario: {e}")

    def _preprocess_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """CSV 행 데이터를 파싱하여 최적화된 형태로 변환합니다."""
        processed = {}
        
        # 1. Counter & NOP Flag
        try:
            processed['ctr'] = int(row['ctr'])
        except (ValueError, TypeError):
            return {} # 유효하지 않은 행 무시

        processed['isNOP'] = (row.get('isNOP', '').strip().upper() == 'TRUE')

        # 2. Registers
        # 값이 'NaN'이면 None으로, 'Flip'이면 'Flip' 마커 유지, 숫자는 int로 변환
        for reg_name in self.REG_MAP.keys():
            val = row.get(reg_name, 'NaN').strip()
            
            if val == 'NaN' or val == '':
                processed[reg_name] = None
            elif val == 'Flip':
                processed[reg_name] = 'Flip'
            else:
                try:
                    processed[reg_name] = int(val, 0) # 10진수 및 16진수 지원
                except ValueError:
                    processed[reg_name] = None
        
        return processed

    def check_nop(self, index: int) -> bool:
        """해당 인덱스의 시나리오가 NOP 수행인지 확인합니다."""
        if 0 <= index < len(self.fault_list):
            return self.fault_list[index]['isNOP']
        return False

    def nop(self, uc: Uc):
        """PC를 증가시켜 현재 명령어를 건너뜁니다 (NOP 효과)."""
        try:
            pc = uc.reg_read(UC_ARM_REG_PC)
            # 현재 모드(Thumb/ARM)에 맞춰 PC 증가
            next_pc = pc + setEmulData.MODE
            uc.reg_write(UC_ARM_REG_PC, next_pc)
        except UcError as e:
            print(f"Error executing NOP: {e}")

    def _flip_register(self, uc: Uc, reg_const: int):
        """비트 반전(Bit Flip)을 수행합니다."""
        try:
            val = uc.reg_read(reg_const)
            
            # 레거시 로직 유지: 모드에 따른 마스크 적용
            if setEmulData.MODE == 4: # ARM Mode
                flipped_val = val ^ 0xFFFFFFFF
            else: # Thumb Mode
                flipped_val = val ^ 0xFFFF
            
            uc.reg_write(reg_const, flipped_val)
        except UcError:
            pass

    def modify_regs(self, uc: Uc, index: int):
        """시나리오에 정의된 대로 레지스터 값을 수정하거나 Flip합니다."""
        if not (0 <= index < len(self.fault_list)):
            return

        scenario_data = self.fault_list[index]

        for reg_name, reg_const in self.REG_MAP.items():
            val = scenario_data.get(reg_name)

            if val is None:
                continue
            
            if val == 'Flip':
                self._flip_register(uc, reg_const)
            else:
                # 정수형 값 직접 쓰기
                uc.reg_write(reg_const, val)
