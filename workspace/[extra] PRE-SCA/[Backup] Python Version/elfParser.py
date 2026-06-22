import sys
import os
import lief
from typing import List, Dict, Tuple, Any, Optional

class ElfParser:
    """
    ELF 바이너리 파일을 파싱하여 에뮬레이션에 필요한 메모리 맵, 함수 주소,
    코드 세그먼트 정보를 제공하는 클래스입니다.
    """

    def __init__(self, elf_file_path: str):
        if not os.path.exists(elf_file_path):
            raise FileNotFoundError(f"ELF file not found: {elf_file_path}")

        self.elf_file_path: str = elf_file_path
        self.elf_binary: lief.ELF.Binary = lief.parse(self.elf_file_path)
        
        if self.elf_binary is None:
            raise ValueError(f"Failed to parse ELF file: {elf_file_path}")

        self.functions: Dict[str, int] = {}
        self.sorted_functions: Dict[str, int] = {}
        self._initialize_symbol_table()

    def _initialize_symbol_table(self) -> None:
        """ELF 파일에서 심볼(함수) 정보를 추출하고 주소순으로 정렬하여 저장합니다."""
        if not hasattr(self.elf_binary, 'exported_functions'):
            return

        for func in self.elf_binary.exported_functions:
            name = func.name
            address = func.address
            
            # 함수명 충돌 방지 (name, name1, name2...)
            duplicate_count = 0
            unique_name = name
            while unique_name in self.functions:
                duplicate_count += 1
                unique_name = f"{name}{duplicate_count}"
            
            self.functions[unique_name] = address

        self.sorted_functions = dict(sorted(self.functions.items(), key=lambda item: item[1]))

    def check_mode(self) -> int:
        """
        시작 주소를 기반으로 프로세서 모드를 확인합니다.
        Returns:
            int: 2 (Thumb mode) or 4 (ARM mode)
        """
        start_addr = self.get_start_addr()
        # 주소의 최하위 비트가 1이면 Thumb 모드
        return 2 if start_addr % 2 == 1 else 4

    def get_start_addr(self) -> int:
        """에뮬레이션 시작 주소(_init)를 반환합니다."""
        return self.get_func_address('_init')

    def get_func_address(self, func_name: str) -> int:
        """
        특정 함수의 시작 주소를 반환합니다.
        존재하지 않을 경우 ValueError를 발생시킵니다.
        """
        addr = self.sorted_functions.get(func_name)
        if addr is None:
            # 기존 레거시 코드와의 호환성을 위해 sys.stderr 출력 후 종료 패턴 유지 고려
            # 하지만 리팩토링 원칙상 예외 발생이 더 적절함. 
            # 호출부에서 처리를 위해 여기서는 명확한 에러 메시지를 남기고 종료.
            sys.stderr.write(f"Error: Function '{func_name}' does not exist in the symbol table.\n")
            sys.exit(1)
        return addr

    def get_code(self, address: int) -> bytes:
        """
        지정된 주소(파일 오프셋 아님)부터 파일의 끝까지 바이너리 데이터를 읽어옵니다.
        """
        try:
            with open(self.elf_file_path, "rb") as f:
                f.seek(address, 0)
                return f.read()
        except IOError as e:
            sys.stderr.write(f"File I/O Error reading {self.elf_file_path}: {e}\n")
            sys.exit(1)

    def get_io_addr_data(self) -> Tuple[int, int]:
        """가상 I/O 변수(vir_IN, vir_OUT)의 주소를 반환합니다."""
        try:
            addr_in = self.elf_binary.get_symbol("vir_IN").value
            addr_out = self.elf_binary.get_symbol("vir_OUT").value
            return addr_in, addr_out
        except Exception as e:
            sys.stderr.write(f"Symbol Error (vir_IN/vir_OUT): {e}\n")
            sys.exit(1)

    def get_symbol_len(self, symbol_name: str) -> int:
        """심볼의 크기(Size)를 반환합니다."""
        symbol = self.elf_binary.get_symbol(symbol_name)
        if symbol:
            return symbol.size
        return 0

    def get_stack_addr(self) -> int:
        """스택 포인터(_stack)의 초기 주소를 반환합니다."""
        try:
            return self.elf_binary.get_symbol("_stack").value
        except AttributeError:
            sys.stderr.write("Error: '_stack' symbol not found.\n")
            sys.exit(1)

    def section_data_list(self) -> Tuple[List[List[Any]], List[int], List[int], int, int]:
        """
        모든 섹션 정보를 추출합니다.
        Returns:
            (All Sections, RAM Addresses, Flash Offsets, RAM Size, Flash Size)
        """
        sections_info = []
        ram_addrs = []
        flash_offsets = []
        total_ram_size = 0
        total_flash_size = 0

        for section in self.elf_binary.sections:
            # 섹션 정보: [Virtual Address, File Offset, Size, Name]
            info = [
                section.virtual_address,
                section.offset,
                section.original_size,
                section.name
            ]
            sections_info.append(info)

            # RAM 영역 (Virtual Address와 Offset이 다르고, 실제 메모리에 로드되는 영역)
            if section.virtual_address != 0 and section.virtual_address != section.offset:
                total_ram_size += section.original_size
                ram_addrs.append(section.virtual_address)
            
            # Flash 영역 (Virtual Address와 Offset이 같은 영역)
            elif section.virtual_address == section.offset:
                total_flash_size += section.original_size
                flash_offsets.append(section.offset)

        return sections_info, ram_addrs, flash_offsets, total_ram_size, total_flash_size

    def check_list(self, input_list: List[List[Any]]) -> List[List[Any]]:
        """
        리스트 내의 인접한 요소들 중 두 번째 항목(주로 주소)이 중복될 경우 제거합니다.
        (Legacy Logic: Section/Function 리스트 정제용)
        """
        if not input_list:
            return []

        cleaned_list = [input_list[0]]
        
        # 인접 중복 제거 로직 (O(N))
        for item in input_list[1:]:
            # 이전 항목의 두 번째 요소(Address/Offset)와 현재 항목 비교
            if item[1] != cleaned_list[-1][1]:
                cleaned_list.append(item)
        
        return cleaned_list