"""ELF에서 에뮬레이션에 필요한 심볼·섹션·메모리 배치를 읽는 모듈.

`ElfParser`는 LIEF가 파싱한 ELF 객체를 보관하며 파일 자체는 변경하지 않는다. 파일이
없거나 LIEF가 파싱하지 못하면 초기화가 실패한다. 일부 레거시 메서드는 호출부 호환을
위해 실패 시 프로세스를 종료한다.
"""

import sys
import os
import lief
from typing import List, Dict, Tuple, Any, Optional

class ElfParser:
    """ELF 메모리 배치와 함수·I/O 심볼 주소를 제공한다.

    입력은 ELF 파일 경로이다. 초기화 과정에서 파일을 읽고 주소순 함수 표를 메모리에
    구축한다. 파일이 없으면 `FileNotFoundError`, 파싱 결과가 없으면 `ValueError`가
    발생한다. ELF 파일에는 부작용이 없다.
    """

    def __init__(self, elf_file_path: str):
        """ELF 경로를 읽어 LIEF 객체와 주소순 함수 심볼 캐시를 만든다.

        파일이 없으면 `FileNotFoundError`, LIEF가 파싱하지 못하면 `ValueError`가 발생한다.
        ELF 파일은 읽기 전용이며 변경하지 않는다.
        """
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
        """export 함수 심볼을 중복 없는 이름으로 수집해 주소순 캐시에 저장한다.

        export 목록이 없는 ELF는 빈 캐시로 둔다. ELF 객체와 인스턴스 메모리만 읽고
        호스트 파일은 변경하지 않는다.
        """
        if not hasattr(self.elf_binary, 'exported_functions'):
            return

        for func in self.elf_binary.exported_functions:
            name = func.name
            address = func.address
            
            # LIEF가 같은 이름을 두 번 줄 수 있어 뒤 항목에 숫자를 붙여 유실을 막는다.
            duplicate_count = 0
            unique_name = name
            while unique_name in self.functions:
                duplicate_count += 1
                unique_name = f"{name}{duplicate_count}"
            
            self.functions[unique_name] = address

        self.sorted_functions = dict(sorted(self.functions.items(), key=lambda item: item[1]))

    def check_mode(self) -> int:
        """`_init` 주소의 하위 비트로 Thumb이면 2, ARM이면 4를 반환한다.

        `_init` 심볼이 없으면 `get_func_address()`의 레거시 동작에 따라 프로세스를 종료한다.
        """
        start_addr = self.get_start_addr()
        # 주소의 최하위 비트가 1이면 Thumb 모드
        return 2 if start_addr % 2 == 1 else 4

    def get_start_addr(self) -> int:
        """`_init` 심볼의 시작 주소를 반환하고 없으면 프로세스를 종료한다."""
        return self.get_func_address('_init')

    def get_func_address(self, func_name: str) -> int:
        """함수 시작 주소를 반환하고, 심볼이 없으면 오류를 출력한 뒤 프로세스를 종료한다."""
        addr = self.sorted_functions.get(func_name)
        if addr is None:
            # 호출부가 종료 동작에 의존하므로 레거시 실패 방식을 유지한다.
            sys.stderr.write(f"Error: Function '{func_name}' does not exist in the symbol table.\n")
            sys.exit(1)
        return addr

    def get_code(self, address: int) -> bytes:
        """`address`를 파일 오프셋으로 사용해 ELF 끝까지 읽고, 실패하면 프로세스를 종료한다."""
        try:
            with open(self.elf_file_path, "rb") as f:
                f.seek(address, 0)
                return f.read()
        except IOError as e:
            sys.stderr.write(f"File I/O Error reading {self.elf_file_path}: {e}\n")
            sys.exit(1)

    def get_io_addr_data(self) -> Tuple[int, int]:
        """가상 I/O 심볼 `vir_IN`·`vir_OUT`의 주소를 반환하고, 실패하면 종료한다."""
        try:
            addr_in = self.elf_binary.get_symbol("vir_IN").value
            addr_out = self.elf_binary.get_symbol("vir_OUT").value
            return addr_in, addr_out
        except Exception as e:
            sys.stderr.write(f"Symbol Error (vir_IN/vir_OUT): {e}\n")
            sys.exit(1)

    def get_symbol_len(self, symbol_name: str) -> int:
        """심볼 크기를 바이트 단위로 반환하며, 심볼이 없으면 0을 반환한다."""
        symbol = self.elf_binary.get_symbol(symbol_name)
        if symbol:
            return symbol.size
        return 0

    def get_stack_addr(self) -> int:
        """스택 포인터 `_stack`의 초기 주소를 반환하고, 심볼이 없으면 종료한다."""
        try:
            return self.elf_binary.get_symbol("_stack").value
        except AttributeError:
            sys.stderr.write("Error: '_stack' symbol not found.\n")
            sys.exit(1)

    def section_data_list(self) -> Tuple[List[List[Any]], List[int], List[int], int, int]:
        """ELF 섹션 배치와 RAM·Flash 크기 합계를 반환한다.

        반환 순서는 `(섹션 [가상주소, 오프셋, 크기, 이름], RAM 주소, Flash 오프셋,
        RAM 크기 합, Flash 크기 합)`이다. `가상주소 != 오프셋`을 RAM으로 분류하는 레거시
        규칙을 유지하며 파일을 변경하지 않는다.
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
        """두 번째 값이 같은 인접 항목에서 첫 항목만 남긴 새 목록을 반환한다.

        비어 있으면 빈 목록이다. 인접 중복만 제거하므로 호출자는 두 번째 값을 기준으로
        정렬된 입력을 제공해야 하며 원본 목록은 변경하지 않는다.
        """
        if not input_list:
            return []

        cleaned_list = [input_list[0]]
        
        # 인접 중복만 제거하므로 입력은 두 번째 값을 기준으로 미리 정렬되어야 한다.
        for item in input_list[1:]:
            # 이전 항목의 두 번째 요소(Address/Offset)와 현재 항목 비교
            if item[1] != cleaned_list[-1][1]:
                cleaned_list.append(item)
        
        return cleaned_list
