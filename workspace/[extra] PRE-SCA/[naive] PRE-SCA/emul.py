"""단순 PRE-SCA의 ARM 에뮬레이션·오류주입 실행기.

`config.py`의 ELF와 CSV 입력을 읽어 Unicorn으로 실행하고, 명령어·레지스터·가상 I/O
로그를 파일로 쓴다. 파일 생성과 로그 출력이 주요 부작용이며, ELF 심볼이 없거나
입력 형식이 잘못되면 초기화 또는 실행이 실패한다. 동일 입력을 매 명령어에서 다시 읽는
레거시 구조이므로 대량 Dataset(데이터셋) 수집용으로 사용하지 않는다.
"""

import os
import csv
import sys
from typing import List, Tuple, Any, Optional

from unicorn import *
from unicorn.arm_const import *
from capstone import *

import config
import setEmulData
import logger
from scenario import Scenario

# -----------------------------------------------------------------------------
# 공용 도우미
# -----------------------------------------------------------------------------

def get_log_context() -> Tuple[str, str]:
    """현재 레지스터 로그 경로에서 `(디렉터리, 날짜·시간 접두사)`를 반환한다.

    로거 파일이 아직 선택되지 않았으면 `("./log", "")`을 반환해 호출자가 I/O 생성을
    건너뛰게 한다. 파일을 읽거나 쓰지 않는다.
    """
    log_file_path = logger.get_log_file_name()
    if not log_file_path:
        # 로그 파일이 생성되지 않은 초기 상태에 대한 대비
        return "./log", ""
        
    dirname = os.path.dirname(log_file_path)
    basename = os.path.basename(log_file_path)
    # 파일명 형식: "YYYY-MM-DD HH_MM_SS LogReg..."
    # 공백으로 분리하여 날짜+시간 부분을 접두사로 사용
    prefix = " ".join(basename.split(" ")[:2])
    return dirname, prefix

def make_io_data_files(uc: Uc, index: int):
    """에뮬레이션 종료 후 가상 I/O 메모리를 CSV로 저장한다.

    `uc`의 `vir_IN`·`vir_OUT` 영역을 읽으며, `index > 0`이면 오류주입 결과 파일로
    명명한다. 로그 경로가 아직 없으면 아무것도 쓰지 않고, 메모리·파일 I/O 실패는
    출력한 뒤 반환한다.
    """
    log_folder, date_prefix = get_log_context()
    if not date_prefix:
        return

    suffix = "_Faulty" if index > 0 else ""
    
    # 1. LogVirOUT 생성
    out_filename = f"{date_prefix} LogVirOUT{suffix}.csv"
    out_path = os.path.join(log_folder, out_filename)
    
    try:
        out_data = uc.mem_read(setEmulData.vir_out_addr, setEmulData.vir_out_len)
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(out_data))
    except Exception as e:
        print(f"[Error] Failed to write LogVirOUT: {e}")

    # 2. LogVirIN 생성 (입력 데이터 검증용)
    in_filename = f"{date_prefix} LogVirIN.csv"
    in_path = os.path.join(log_folder, in_filename)
    
    try:
        in_data = uc.mem_read(setEmulData.vir_in_addr, setEmulData.vir_in_len)
        with open(in_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(in_data))
    except Exception as e:
        print(f"[Error] Failed to write LogVirIN: {e}")

def get_input_data() -> List[List[int]]:
    """`config.log_vir_in_file`의 비어 있지 않은 CSV 행을 정수 목록으로 읽는다.

    파일이 없으면 빈 목록을 반환한다. 파싱·I/O 실패는 경고를 출력하고 지금까지 읽은
    행만 반환하며 파일을 변경하지 않는다.
    """
    input_data_list = []
    if not os.path.exists(config.log_vir_in_file):
        return []

    try:
        with open(config.log_vir_in_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    input_data_list.append(list(map(int, row)))
    except Exception as e:
        print(f"[Warning] Failed to read input data: {e}")
    
    return input_data_list

def inject_input_data(uc: Uc, data_row: List[int]):
    """정수 바이트 행을 `vir_IN` 시작 주소에 연속으로 기록한다.

    값이 0–255 범위를 벗어나면 `bytes()`의 `ValueError`, 매핑되지 않은 주소면 Unicorn
    예외가 발생한다. 에뮬레이터 메모리를 변경하고 반환값은 없다.
    """
    # 데이터는 바이트 단위로 기록됨
    packed_data = bytes(data_row)
    uc.mem_write(setEmulData.vir_in_addr, packed_data)

# -----------------------------------------------------------------------------
# 디스어셈블리 생성
# -----------------------------------------------------------------------------
def make_disassembly_file():
    """
    Capstone으로 바이너리를 해석해 `disassembly.txt`를 생성한다.
    해석할 수 없는 데이터·패딩은 실행 모드 단위로 건너뛴다. 기존 파일은 덮어쓰며,
    파일 I/O 또는 Capstone 초기화 실패는 호출자에게 전파된다.
    """
    ref_file_path = 'disassembly.txt'
    if os.path.exists(ref_file_path):
        os.remove(ref_file_path)

    # 모드 설정
    cs_mode = CS_MODE_THUMB if setEmulData.MODE == 2 else CS_MODE_ARM
    md = Cs(CS_ARCH_ARM, cs_mode)
    md.detail = True

    # 데이터 준비
    # Thumb 모드일 경우 시작 주소 오프셋 보정 (홀수 주소 -> 짝수 주소)
    addr_offset = 1 if setEmulData.MODE == 2 else 0
    start_addr = setEmulData.START_ADDRESS - addr_offset
    
    # 전체 코드 데이터
    code_data = setEmulData.REF_CODE
    end_addr = start_addr + len(code_data)
    
    # 순회 제어 변수
    curr_addr = start_addr
    sec_idx = 1
    func_idx = 0
    e_secs = setEmulData.e_sec
    funcs = setEmulData.func_list
    
    # 가상 주소 (Data Section 추적용)
    virtual_addr = 0
    current_sec_name = ""

    # setEmulData.instructions 초기화 (중복 실행 방지)
    setEmulData.instructions.clear()

    with open(ref_file_path, 'w', encoding='utf-8') as f:
        while curr_addr < end_addr:
            # 현재 처리할 데이터 오프셋 계산
            offset = curr_addr - start_addr
            if offset >= len(code_data):
                break

            # 1. 섹션 헤더 처리
            if sec_idx < len(e_secs):
                sec_info = e_secs[sec_idx] # [Addr, Offset, Size, Name]
                sec_start = sec_info[1]
                
                # 주소 매칭 (Thumb 모드 고려하여 -2 범위 체크)
                if sec_start - 2 == curr_addr or sec_start == curr_addr:
                    f.write(f"\nsection\t\t : {sec_info[3]}\n")
                    if sec_info[0] != 0:
                        f.write(f"REAL ADDRESS : {hex(sec_info[0])}\n\n")
                        virtual_addr = sec_info[0]
                        current_sec_name = sec_info[3]
                    sec_idx += 1

            # 2. 함수 헤더 처리
            if func_idx < len(funcs):
                func_start = funcs[func_idx][1]
                # Thumb 모드일 경우 함수 주소는 홀수(LSB=1)지만 실행 주소는 짝수
                if func_start == curr_addr + addr_offset:
                    f.write(f"\nfunction\t : {funcs[func_idx][0]}\n\n")
                    func_idx += 1

            # 3. 디스어셈블리 시도 (1개 명령어)
            # count=1로 설정하여 한 번에 하나씩 처리
            insns = list(md.disasm(code_data[offset:], curr_addr, count=1))
            
            if insns:
                insn = insns[0]
                
                # .data 섹션은 헥사 바이트로 출력, 코드는 니모닉 출력
                if virtual_addr != 0 and current_sec_name == '.data':
                    hex_bytes = "".join([f"\\x{b:x}" for b in insn.bytes])
                    f.write(f"0x{insn.address:x}:[0x{virtual_addr:x}] {hex_bytes}")
                else:
                    f.write(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}\n")
                
                # 명령어 캐싱 (Logger 사용)
                setEmulData.instructions.append([insn.address, insn.mnemonic, insn.op_str])
                
                # 다음 주소로 이동
                curr_addr += insn.size
                
                # 가상 주소 업데이트
                if virtual_addr != 0:
                    virtual_addr += setEmulData.MODE
            else:
                # 디스어셈블리 실패 (데이터, 패딩, 또는 Junk)
                # 레거시 로직과 동일하게 MODE 크기만큼 건너뛰고 다시 시도 (Resume Logic)
                curr_addr += setEmulData.MODE
                if virtual_addr != 0:
                    virtual_addr += setEmulData.MODE

# -----------------------------------------------------------------------------
# 에뮬레이션 핵심 로직
# -----------------------------------------------------------------------------
sync_ctr = 0  # 입력 주입 순서를 맞추는 공용 카운터

def hook_code_trace(uc: Uc, address: int, size: int, user_data: Any):
    """명령어 실행 전 레지스터 상태를 기록하고 `_exit` 주소에서 실행을 멈춘다.

    로거 버퍼·CSV와 Unicorn 실행 상태를 변경한다. 로깅 또는 에뮬레이터 오류는 호출자에게
    전파되며 반환값은 없다.
    """
    logger.write_log_regs(uc, address, user_data)
    
    # 종료 주소 도달 시 에뮬레이션 중단
    # Thumb 모드 보정 (PC는 홀수 주소를 가질 수 없음)
    exit_target = setEmulData.exit_addr_real - (1 if setEmulData.MODE == 2 else 0)
    if address == exit_target:
        uc.emu_stop()

def hook_scene_injection(uc: Uc, address: int, size: int, scene: Scenario):
    """명령어 순서에 맞춰 입력 바이트와 Fault injection(오류주입)을 적용한다.

    현재 `sync_ctr`와 정상 실행의 `LOG_MATRIX` 주소를 기준으로 입력 메모리·레지스터·PC를
    변경한다. 잘못된 시나리오 인덱스는 건너뛰며 `_exit`에서 카운터를 0으로 되돌린다.
    입력 CSV를 매 hook마다 다시 읽는 레거시 동작 때문에 대량 실행에는 적합하지 않다.
    """
    global sync_ctr
    
    # 1. 입력 데이터 주입 (Sync Counter 기반)
    # 성능을 위해 전체 데이터를 매번 순회하지 않고 필요한 시점에만 주입하는 것이 좋으나,
    # 기존 로직과의 정확한 호환성을 위해 순회 방식 유지
    all_input_data = get_input_data()
    for row in all_input_data:
        if row and row[0] == sync_ctr:
            inject_input_data(uc, row[1:])

    # 2. 오류 주입 (Fault Injection)
    if scene.Fault_list and logger.LOG_MATRIX:
        # LOG_MATRIX 참조를 통해 현재 실행 흐름과 매칭되는지 확인
        # 주의: 첫 번째 실행(Normal)이 완료된 후 생성된 LOG_MATRIX를 기준으로
        # 두 번째 실행(Faulty)에서 주입 시점을 결정함.
        
        # logger 모듈의 인스턴스에서 현재까지 기록된 로그의 길이를 알 수 없으므로
        # Scenario 내부 로직이나 단순 주소 비교에 의존해야 함.
        # 여기서는 주소 매칭 방식을 사용.
        
        for i, fault in enumerate(scene.Fault_list):
            try:
                target_ctr = int(fault['ctr'])
                # LOG_MATRIX 범위 체크 (Header 제외 +1)
                if target_ctr + 1 < len(logger.LOG_MATRIX):
                    log_addr_str = logger.LOG_MATRIX[target_ctr + 1][1] # Address column
                    
                    if hex(address) == log_addr_str:
                        if scene.check_nop(i):
                            scene.nop(uc)
                        else:
                            scene.modify_regs(uc, i)
            except (ValueError, IndexError):
                continue

    sync_ctr += 1
    
    # 다음 실행을 위해 입력 순서 카운터를 초기화한다.
    exit_target = setEmulData.exit_addr_real - (1 if setEmulData.MODE == 2 else 0)
    if address == exit_target:
        sync_ctr = 0

def init_emulator() -> Uc:
    """새 Unicorn 인스턴스에 ELF 메모리와 초기 레지스터를 설정해 반환한다.

    Flash·RAM을 페이지 단위로 매핑하고 ELF 섹션을 읽어 메모리에 쓴다. 호스트 파일은
    변경하지 않는다. 일부 겹친 매핑·쓰기 오류는 레거시 호환을 위해 무시하지만, ELF I/O와
    인스턴스 생성 실패는 호출자에게 전파된다.
    """
    arch = UC_ARCH_ARM
    mode = UC_MODE_THUMB if setEmulData.MODE == 2 else UC_MODE_ARM
    uc = Uc(arch, mode)

    PAGE_SIZE = 4 * 1024

    # 1. Flash Memory Mapping
    flash_start = setEmulData.START_ADDRESS
    flash_end = flash_start + setEmulData.flash_size
    flash_base = (flash_start // PAGE_SIZE) * PAGE_SIZE
    flash_size_aligned = ((flash_end - flash_base + PAGE_SIZE - 1) // PAGE_SIZE) * PAGE_SIZE
    uc.mem_map(flash_base, flash_size_aligned)

    # 2. RAM Memory Mapping
    ram_start = setEmulData.ram_addr[0]
    ram_end = setEmulData.stack_addr
    ram_base = (ram_start // PAGE_SIZE) * PAGE_SIZE
    ram_size_aligned = ((ram_end - ram_base + PAGE_SIZE - 1) // PAGE_SIZE) * PAGE_SIZE
    
    # 겹침 방지 매핑
    try:
        uc.mem_map(ram_base, ram_size_aligned)
    except UcError:
        pass 

    # 3. 레지스터 초기화
    uc.reg_write(UC_ARM_REG_SP, setEmulData.stack_addr)
    uc.reg_write(UC_ARM_REG_FP, setEmulData.stack_addr)
    uc.reg_write(UC_ARM_REG_LR, setEmulData.exit_addr)

    # 4. 바이너리 로드
    with open(config.elf_file, "rb") as f:
        for section in setEmulData.e_sec:
            virt_addr = section[0]
            offset = section[1]
            size = section[2]
            
            if virt_addr != 0:
                f.seek(offset)
                content = f.read(size)
                try:
                    uc.mem_write(virt_addr, content)
                except UcError:
                    pass # 읽기 전용 영역 쓰기 시도 등 무시

    return uc

def run():
    """디스어셈블을 만들고 정상·오류주입 에뮬레이션을 순서대로 실행한다.

    오류주입 시나리오가 있으면 정상 실행 뒤 Faulty 실행을 한 번 수행한다. 실행별 레지스터
    로그와 가상 I/O CSV를 만들고 `disassembly.txt`를 덮어쓴다. ELF·Unicorn·파일 I/O 오류는
    호출자에게 전파되며 반환값은 없다.
    """
    print("Emulating the code..")
    
    # 1. disassembly 파일 생성 (디스어셈블리)
    make_disassembly_file()

    # 2. 시나리오 준비
    scene = Scenario()
    
    # 시나리오가 있으면 정상 실행 후 오류주입 항목별로 한 번씩 실행한다.
    run_count = 2 if scene.Fault_list else 1

    for i in range(run_count):
        # 로거 파일 설정
        logger.make_log_file(i)
        
        # 에뮬레이터 초기화
        mu = init_emulator()

        # 훅 등록
        code_end = setEmulData.START_ADDRESS + len(setEmulData.CODE)
        mu.hook_add(UC_HOOK_CODE, hook_scene_injection, scene, begin=setEmulData.START_ADDRESS, end=code_end)
        mu.hook_add(UC_HOOK_CODE, hook_code_trace, scene, begin=setEmulData.START_ADDRESS, end=code_end)

        try:
            # 실행
            mu.emu_start(setEmulData.emu_ADDRESS, setEmulData.emu_ADDRESS + setEmulData.main_len)
            print(">>> Emulation done.")
            
            # 결과 저장
            make_io_data_files(mu, i)
            
        except UcError as e:
            # 에러 발생 시 현재까지의 로그 덤프
            with open(logger.get_log_file_name(), 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(logger._logger_instance.current_log_matrix)
            make_io_data_files(mu, i)
            print(f"ERROR: {e}")
