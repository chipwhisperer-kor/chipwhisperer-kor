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
        """`config.fault_reg_file`을 읽어 유효한 Fault injection 행을 캐시한다.

        파일이 없거나 행이 잘못돼도 가능한 항목만 보존하며 호스트 파일은 변경하지 않는다.
        """
        self.fault_list: List[Dict[str, Any]] = []
        self._load_scenario_data()

    @property
    def Fault_list(self) -> List[Dict[str, Any]]:
        """레거시 외부 모듈이 사용하는 시나리오 목록 속성을 반환한다."""
        return self.fault_list

    def _load_scenario_data(self):
        """시나리오 CSV를 읽어 에뮬레이션용 정수·불리언 값으로 캐시한다.

        파일이 없으면 알림을 출력하고 빈 시나리오를 유지한다. 헤더 여부를 판별한 뒤 유효한
        행만 추가하며 파싱·I/O 실패는 오류를 출력하고 지금까지 읽은 항목을 보존한다. 파일은
        변경하지 않는다.
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
        """CSV 한 행을 실행 가능한 시나리오 사전으로 변환한다.

        `ctr`이 정수가 아니면 빈 사전을 반환해 행 전체를 무시한다. 각 레지스터는 `None`,
        `Flip`, 정수 중 하나로 정규화하며 입력 사전은 변경하지 않는다.
        """
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
        """유효한 인덱스의 시나리오가 명령어 건너뛰기이면 `True`를 반환한다."""
        if 0 <= index < len(self.fault_list):
            return self.fault_list[index]['isNOP']
        return False

    def nop(self, uc: Uc):
        """현재 실행 모드의 명령어 폭만큼 PC를 증가시켜 명령어를 건너뛴다.

        Unicorn PC를 변경하는 Fault injection이다. 레지스터 접근 실패는 오류를 출력하고
        반환하며 예외를 다시 발생시키지 않는다.
        """
        try:
            pc = uc.reg_read(UC_ARM_REG_PC)
            # 현재 모드(Thumb/ARM)에 맞춰 PC 증가
            next_pc = pc + setEmulData.MODE
            uc.reg_write(UC_ARM_REG_PC, next_pc)
        except UcError as e:
            print(f"Error executing NOP: {e}")

    def _flip_register(self, uc: Uc, reg_const: int):
        """지정 레지스터를 ARM이면 32비트, Thumb이면 16비트 마스크로 반전한다.

        Unicorn 레지스터를 변경하며 접근 실패는 레거시 호환을 위해 조용히 무시한다.
        """
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
        """시나리오 인덱스가 지정한 모든 레지스터 쓰기·반전을 적용한다.

        범위 밖 인덱스는 아무 작업도 하지 않는다. 값이 `None`인 레지스터는 보존하며 Unicorn
        쓰기 실패는 호출자에게 전파된다. 에뮬레이터 상태를 변경하고 반환값은 없다.
        """
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
