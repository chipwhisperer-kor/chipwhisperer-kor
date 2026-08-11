"""ELF에서 공용 에뮬레이션 문맥을 초기화한다.

이 모듈은 import 시 ELF를 읽어 프로세서 모드, 섹션 배치, 함수·I/O 심볼 주소를 모듈
속성으로 공개한다. 호출부가 이 식별자를 이름으로 참조하므로 변수명을 바꾸지 않는다.
ELF 파싱이나 필수 심볼 조회가 실패하면 오류를 출력하고 프로세스를 종료한다.
"""

import sys
from config import elf_file
from elfParser import ElfParser

# -----------------------------------------------------------------------------
# 공용 에뮬레이션 문맥 초기화
# -----------------------------------------------------------------------------
# 이 모듈은 에뮬레이션 환경(메모리 맵, 섹션 정보, 심볼 주소 등)을 초기화하여
# 전역 변수(Context)로 제공합니다.

try:
    # 1. ELF 파서 초기화
    # (기존 레거시 코드와의 호환성을 위해 인스턴스명 'e' 유지)
    e = ElfParser(elf_file)

    # 2. 프로세서 모드 설정 (2: Thumb mode, 4: ARM mode)
    MODE = e.check_mode()

    # 3. 섹션 정보 및 메모리 레이아웃 로드
    # 반환값 구조: (전체 섹션 리스트, RAM 주소, Flash 오프셋, RAM 크기, Flash 크기)
    e_section_list, ram_addr, flash_addr, ram_size, flash_size = e.section_data_list()

    # 4. 시작 주소 및 바이너리 코드 로드
    START_ADDRESS = e.get_start_addr()
    
    # 실행용 코드 로드
    CODE = e.get_code(START_ADDRESS)
    
    # 레퍼런스 생성용 코드 로드 (Thumb 모드일 경우 오프셋 1 보정)
    ref_offset = 1 if MODE == 2 else 0
    REF_CODE = e.get_code(START_ADDRESS - ref_offset)

    # 5. 리스트 정제 (중복 주소 제거)
    # 인접한 항목의 1번 값(주소/오프셋)이 같으면 중복을 제거한다.
    e_sec = e.check_list(e_section_list)
    
    # 함수 리스트 정제 (v3.0 API: func_sort -> sorted_functions)
    func_list = e.check_list(list(e.sorted_functions.items()))

    # 6. 주요 시스템 심볼 주소 매핑
    stack_addr = e.get_stack_addr()
    exit_addr = e.get_func_address('exit')
    exit_addr_real = e.get_func_address('_exit')
    emu_ADDRESS = e.get_func_address('main')

    # 7. 데이터 크기 및 I/O 주소 매핑
    main_len = e.get_symbol_len('main')
    vir_out_len = e.get_symbol_len('vir_OUT')
    vir_in_len = e.get_symbol_len('vir_IN')
    vir_in_addr, vir_out_addr = e.get_io_addr_data()

    # 8. 에뮬레이션 상태 변수 초기화
    refsIdx = 1
    reffIdx = 0
    instructions = []
    insn_cnt = 0
    insn_size = 0

except Exception as err:
    sys.stderr.write(f"[Fatal Error] Failed to initialize emulation data: {err}\n")
    sys.exit(1)
