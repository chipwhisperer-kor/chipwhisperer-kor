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
# Helper Functions
# -----------------------------------------------------------------------------

def get_log_context() -> Tuple[str, str]:
    """
    logger 모듈에서 생성한 로그 파일 경로를 기반으로
    디렉토리 경로와 파일명 접두사(타임스탬프)를 추출합니다.
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
    """
    에뮬레이션 종료 후 가상 I/O 메모리(VirIN, VirOUT) 내용을 CSV로 저장합니다.
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
    """입력 데이터(LogVirIN.csv)를 로드합니다."""
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
    """메모리에 입력 데이터를 주입합니다."""
    # 데이터는 바이트 단위로 기록됨
    packed_data = bytes(data_row)
    uc.mem_write(setEmulData.vir_in_addr, packed_data)

# -----------------------------------------------------------------------------
# disassembly Generator (Restored Logic)
# -----------------------------------------------------------------------------
def make_disassembly_file():
    """
    Capstone 엔진을 사용하여 바이너리를 디스어셈블하고 disassembly.txt를 생성합니다.
    중간에 해석 불가능한 데이터가 있어도 건너뛰고 끝까지 생성하도록 로직을 강화했습니다.
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
# Emulation Core Logic
# -----------------------------------------------------------------------------
sync_ctr = 0  # Global sync counter for input injection

def hook_code_trace(uc: Uc, address: int, size: int, user_data: Any):
    """
    명령어 실행 추적 훅
    """
    logger.write_log_regs(uc, address, user_data)
    
    # 종료 주소 도달 시 에뮬레이션 중단
    # Thumb 모드 보정 (PC는 홀수 주소를 가질 수 없음)
    exit_target = setEmulData.exit_addr_real - (1 if setEmulData.MODE == 2 else 0)
    if address == exit_target:
        uc.emu_stop()

def hook_scene_injection(uc: Uc, address: int, size: int, scene: Scenario):
    """
    입력 데이터 주입 및 오류 주입(Fault Injection) 훅
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
    
    # Loop Reset
    exit_target = setEmulData.exit_addr_real - (1 if setEmulData.MODE == 2 else 0)
    if address == exit_target:
        sync_ctr = 0

def init_emulator() -> Uc:
    """Unicorn 에뮬레이터 인스턴스 생성 및 메모리 매핑"""
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
    """메인 실행 함수"""
    print("Emulating the code..")
    
    # 1. disassembly 파일 생성 (디스어셈블리)
    make_disassembly_file()

    # 2. 시나리오 준비
    scene = Scenario()
    
    # Fault List 존재 여부에 따라 실행 횟수 결정 (Normal -> Faulty)
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