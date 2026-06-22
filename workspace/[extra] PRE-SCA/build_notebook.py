# -*- coding: utf-8 -*-
"""PRE-SCA 프로젝트를 학습용 주피터 노트북으로 재구성하는 빌더 스크립트."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))

def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))

# =====================================================================
# 표지
# =====================================================================
md(r"""
# PRE-SCA 에뮬레이터 — 동작 원리 학습용 재구성 노트북

## ARM 바이너리(tiny-AES) 명령어 단위 트레이싱 & 오류주입(Fault Injection) 사전 검증

---

### 🎯 이 노트북의 목표

이 노트북은 **`[extra] PRE-SCA`** 프로젝트(여러 개의 `.py` 모듈)를
**하나의 흐름으로 읽히는 주피터 노트북**으로 재구성한 것입니다.

> **PRE-SCA = Pre-silicon Side-Channel / fault Analysis**
> 실제 칩(실리콘)으로 측정하기 *전에*, **ARM 명령어 셋 에뮬레이터(Unicorn)** 위에서
> 펌웨어를 한 명령어씩 실행하면서 **모든 레지스터 상태를 기록**합니다.
> 이렇게 만든 "가상 부채널(register trace)"은 실측 전력파형/오류주입 실험을 설계하기 위한
> **사전(pre-) 데이터**가 됩니다.

재구성의 목적은 **속도/메모리 최적화가 아니라 "동작 원리의 이해"** 이므로,
이 노트북은 다음을 우선합니다.

- ✅ 원본 로직을 **빠짐없이** 그대로 옮기되, 모듈 경계를 넘어 **위에서 아래로 읽히도록** 재배치
- ✅ 각 단계의 **중간 산출물(메모리맵 · 심볼표 · 디스어셈블리 · 레지스터 트레이스 등)을 시각화**
- ✅ "왜 이 코드가 필요한가"를 markdown으로 설명

| 단계 | 원본 모듈 | 내용 | 핵심 산출물 |
|:----:|:----|:----|:----|
| **0** | (환경) | 라이브러리 임포트 / 경로 설정 | `unicorn`, `capstone`, `lief` |
| **1** | `config.py` | 전역 설정(경로·파라미터) | `BUFFER_BLOCK`, `BUFFER_NUM` |
| **2** | `elfParser.py` | ELF 파싱 → 메모리맵 · 심볼 · 코드 | `ElfParser` |
| **3** | `setEmulData.py` | 에뮬레이션 컨텍스트(주소·모드) 확정 | `MODE`, `START_ADDRESS`, I/O 주소 |
| **4** | `make_TC.py` | 입력 테스트벡터(평문) 생성 | `LogVirIN.csv` |
| **5** | `emul.make_disassembly_file` | Capstone 디스어셈블 | `disassembly.txt`, `instructions` |
| **6** | `logger.py` | 명령어별 레지스터 트레이스 로거 | `TraceLogger`, `LogReg.csv` |
| **7** | `scenario.py` | 오류주입(Fault Injection) 시나리오 | `Scenario`, `LogFI.csv` |
| **8** | `emul.init_emulator` / hooks | 에뮬레이터 구성 + 훅 등록 | `Uc` 인스턴스 |
| **9** | `emul.run` | 정상(Normal) 실행 & 트레이스 수집 | `LogReg.csv`, `LogVirOUT.csv` |
| **10** | (시각화) | 레지스터 트레이스 / 실행흐름 분석 | 히트맵 · PC 흐름 그래프 |
| **11** | `emul.run` (Faulty) | 오류주입 실행 & 정상결과와 비교 | `LogReg_Faulty.csv` |
| **12** | `test_cmp.py` | 재현성(결정성) 검증 | 바이너리 비교 결과 |

---

> ⚠️ **원본과의 단 하나의 의도적 차이**
> 원본 `elfParser.py`는 `lief.parse(파일경로)`를 사용합니다. 그러나 이 노트북이 위치한 경로에는
> **한글이 포함**되어 있어, Windows에서 일부 `lief` 빌드가 한글 경로 파일을 열지 못합니다.
> 따라서 이 노트북은 파일을 **바이트로 먼저 읽어** `lief.parse(list(data))`로 파싱합니다.
> 파싱 결과(섹션·심볼·주소)는 경로 방식과 **완전히 동일**하며, 로직에는 영향이 없습니다.
""")

# =====================================================================
# 0단계 환경
# =====================================================================
md(r"""
---
# 0단계 — 환경 설정 (라이브러리 & 경로)

> **이 단계의 목표**
> 에뮬레이션에 필요한 세 가지 핵심 라이브러리를 불러오고, 원본 프로젝트 폴더를 가리키는 경로를 잡습니다.

| 라이브러리 | 역할 | 원본에서 쓰인 곳 |
|:---|:---|:---|
| **`lief`** | ELF 바이너리 파싱(섹션·심볼·주소) | `elfParser.py` |
| **`capstone`** | 기계어 → 어셈블리 디스어셈블 | `emul.make_disassembly_file` |
| **`unicorn`** | ARM CPU 에뮬레이션(명령어 실행) | `emul.py`, `logger.py`, `scenario.py` |

설치가 안 되어 있다면 아래 한 줄을 실행하세요.
```python
%pip install unicorn capstone lief pandas matplotlib
```
""")

code(r'''
import os, sys, csv, glob, random, datetime
from typing import List, Dict, Tuple, Any, Optional

import lief
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from unicorn import (
    Uc, UcError,
    UC_ARCH_ARM, UC_MODE_ARM, UC_MODE_THUMB, UC_HOOK_CODE,
)
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_FP,
    UC_ARM_REG_IP, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 한글 폰트 깨짐 방지 (Windows: 맑은 고딕)
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False

print('lief    :', lief.__version__)
import capstone, unicorn
print('capstone:', capstone.__version__)
print('unicorn :', unicorn.__version__)
''')

md(r"""
### 경로 설정

이 노트북은 `주피터노트북 형태로 재구성` 폴더 안에 있다고 가정하고,
바로 옆의 원본 프로젝트 폴더를 가리킵니다.
""")

code(r'''
# 원본 프로젝트 폴더 (한글 경로)
PROJECT_DIR = os.path.join(os.getcwd(), "재구성 대상 프로젝트_[extra] PRE-SCA")
if not os.path.isdir(PROJECT_DIR):
    # 노트북을 프로젝트 폴더 안에서 직접 여는 경우의 대비
    PROJECT_DIR = os.getcwd()

print("PROJECT_DIR =", PROJECT_DIR)
assert os.path.isfile(os.path.join(PROJECT_DIR, "source", "tiny-aes")), \
    "source/tiny-aes 바이너리를 찾을 수 없습니다. PROJECT_DIR을 확인하세요."
print("✅ tiny-aes ELF 바이너리 확인 완료")
''')

# =====================================================================
# 1단계 config
# =====================================================================
md(r"""
---
# 1단계 — 전역 설정 (`config.py`)

> **이 단계의 목표**
> 어떤 바이너리를 / 어디서 / 어떤 크기로 다룰지 결정하는 **상수**들을 모읍니다.

원본 `config.py`는 단순한 경로/파라미터 모음입니다. 핵심은 마지막 두 줄입니다.

- `BUFFER_BLOCK = 16` : 입력 데이터 한 블록의 크기(바이트). AES 블록(128bit=16byte)과 일치합니다.
- `BUFFER_NUM   = 10` : 처리할 블록(행) 개수 → 총 입력 버퍼 크기 = `16 × 10 = 160 byte`.

(`vir_IN` 심볼의 크기가 160바이트인 것과 정확히 맞아떨어집니다 — 3단계에서 확인합니다.)
""")

code(r'''
# ── config.py 재구성 ────────────────────────────────────
BASE_DIR = PROJECT_DIR

log_file_name = "tiny-AES_rand"

# 입력 ELF 및 초기설정(ini_set) 파일 경로
elf_file        = os.path.join(BASE_DIR, "source", "tiny-aes")
log_vir_in_file = os.path.join(BASE_DIR, "ini_set", "LogVirIN.csv")
fault_reg_file  = os.path.join(BASE_DIR, "ini_set", "LogFI.csv")

# 에뮬레이션 파라미터
BUFFER_BLOCK = 16   # 입력 데이터 블록 크기 (Bytes) = AES 블록 크기
BUFFER_NUM   = 10   # 처리할 블록(행)의 개수

# 이 노트북의 산출물은 원본을 건드리지 않도록 별도 폴더에 저장합니다.
OUTPUT_DIR = os.path.join(os.getcwd(), "nb_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("elf_file        :", elf_file)
print("log_vir_in_file :", log_vir_in_file)
print("fault_reg_file  :", fault_reg_file)
print("총 입력 버퍼     :", BUFFER_BLOCK * BUFFER_NUM, "byte")
print("출력 폴더        :", OUTPUT_DIR)
''')

# =====================================================================
# 2단계 ElfParser
# =====================================================================
md(r"""
---
# 2단계 — ELF 파싱 (`elfParser.py`)

> **이 단계의 목표**
> tiny-AES ELF 파일을 해부해서 **에뮬레이터에 올릴 메모리 지도(섹션) · 함수 심볼표 · 시작 주소**를 얻습니다.
> 에뮬레이터는 "어디에 코드를 올리고, 어디서부터 실행하고, 어디서 멈출지"를 알아야 하므로
> 이 정보가 모든 것의 출발점입니다.

`ElfParser` 클래스를 원본 그대로 재구성합니다. 메서드별 역할:

| 메서드 | 역할 |
|:---|:---|
| `_initialize_symbol_table` | 함수 심볼을 추출하고 **주소순 정렬**(중복명은 `name1`, `name2`로) |
| `check_mode` | 시작주소 LSB로 **ARM(4) / Thumb(2) 모드** 판별 |
| `get_func_address` | 함수명 → 주소 |
| `get_code` | 특정 주소부터 파일 끝까지 바이트 읽기 |
| `section_data_list` | 모든 섹션의 `[가상주소, 파일오프셋, 크기, 이름]` + RAM/Flash 분류 |
| `check_list` | 인접 중복(같은 주소) 제거 |
""")

code(r'''
class ElfParser:
    """ELF 바이너리를 파싱하여 메모리맵·함수주소·코드를 제공하는 클래스 (원본 elfParser.py 재구성)."""

    def __init__(self, elf_file_path: str):
        if not os.path.exists(elf_file_path):
            raise FileNotFoundError(f"ELF file not found: {elf_file_path}")

        self.elf_file_path = elf_file_path

        # [원본과의 차이] 원본은 lief.parse(경로)를 사용하지만, 한글 경로 호환을 위해
        # 파일을 바이트로 먼저 읽어 파싱한다. 결과는 동일하다.
        with open(elf_file_path, "rb") as f:
            self._raw = f.read()
        self.elf_binary = lief.parse(list(self._raw))

        if self.elf_binary is None:
            raise ValueError(f"Failed to parse ELF file: {elf_file_path}")

        self.functions: Dict[str, int] = {}
        self.sorted_functions: Dict[str, int] = {}
        self._initialize_symbol_table()

    def _initialize_symbol_table(self) -> None:
        """심볼(함수)을 추출하고 주소순으로 정렬한다. 동일 이름은 name1, name2...로 구분."""
        if not hasattr(self.elf_binary, 'exported_functions'):
            return
        for func in self.elf_binary.exported_functions:
            name, address = func.name, func.address
            unique_name, dup = name, 0
            while unique_name in self.functions:
                dup += 1
                unique_name = f"{name}{dup}"
            self.functions[unique_name] = address
        self.sorted_functions = dict(sorted(self.functions.items(), key=lambda kv: kv[1]))

    def check_mode(self) -> int:
        """시작주소 최하위 비트가 1이면 Thumb(2), 아니면 ARM(4)."""
        return 2 if self.get_start_addr() % 2 == 1 else 4

    def get_start_addr(self) -> int:
        """에뮬레이션 시작 주소(_init)."""
        return self.get_func_address('_init')

    def get_func_address(self, func_name: str) -> int:
        addr = self.sorted_functions.get(func_name)
        if addr is None:
            raise ValueError(f"Function '{func_name}' does not exist in the symbol table.")
        return addr

    def get_code(self, address: int) -> bytes:
        """주소(=파일 오프셋)부터 파일 끝까지 읽는다."""
        return self._raw[address:]

    def get_io_addr_data(self) -> Tuple[int, int]:
        addr_in  = self.elf_binary.get_symbol("vir_IN").value
        addr_out = self.elf_binary.get_symbol("vir_OUT").value
        return addr_in, addr_out

    def get_symbol_len(self, symbol_name: str) -> int:
        sym = self.elf_binary.get_symbol(symbol_name)
        return sym.size if sym else 0

    def get_stack_addr(self) -> int:
        return self.elf_binary.get_symbol("_stack").value

    def section_data_list(self):
        """모든 섹션 정보 + RAM/Flash 분류를 반환."""
        sections_info, ram_addrs, flash_offsets = [], [], []
        total_ram_size = total_flash_size = 0
        for section in self.elf_binary.sections:
            info = [section.virtual_address, section.offset,
                    section.original_size, section.name]
            sections_info.append(info)
            if section.virtual_address != 0 and section.virtual_address != section.offset:
                total_ram_size += section.original_size
                ram_addrs.append(section.virtual_address)
            elif section.virtual_address == section.offset:
                total_flash_size += section.original_size
                flash_offsets.append(section.offset)
        return sections_info, ram_addrs, flash_offsets, total_ram_size, total_flash_size

    @staticmethod
    def check_list(input_list):
        """인접한 항목의 [1]번 요소(주소/오프셋)가 같으면 제거."""
        if not input_list:
            return []
        cleaned = [input_list[0]]
        for item in input_list[1:]:
            if item[1] != cleaned[-1][1]:
                cleaned.append(item)
        return cleaned

print("✅ ElfParser 클래스 정의 완료")
''')

code(r'''
# ELF 파서 인스턴스 생성 (원본에서는 setEmulData.e)
e = ElfParser(elf_file)
print("파싱 성공 — 추출된 함수 심볼 개수:", len(e.sorted_functions))
''')

md(r"""
### 🔎 중간 산출물 ①: 함수 심볼표

ELF에서 추출한 함수 목록을 **주소순**으로 봅니다. AES 관련 함수들(`AES_init_ctx`, `AES_*_encrypt` 등)과
런타임 심볼(`_init`, `main`, `exit`, `_exit`)이 보입니다. 이 주소들이 3단계에서 에뮬레이션의 좌표가 됩니다.
""")

code(r'''
df_funcs = pd.DataFrame(
    [(name, addr, hex(addr)) for name, addr in e.sorted_functions.items()],
    columns=["function", "address(dec)", "address(hex)"]
)
df_funcs
''')

md(r"""
### 🔎 중간 산출물 ②: 섹션(메모리) 정보

각 섹션의 `[가상주소, 파일오프셋, 크기, 이름]`입니다.
- **가상주소 == 파일오프셋** → 그대로 메모리에 매핑되는 **Flash(코드/상수)** 영역
- **가상주소 != 파일오프셋** 이고 둘 다 0이 아님 → 실행 중 별도 주소에 올라가는 **RAM(데이터)** 영역
""")

code(r'''
e_section_list, ram_addr, flash_addr, ram_size, flash_size = e.section_data_list()

df_sec = pd.DataFrame(e_section_list, columns=["virt_addr", "file_offset", "size", "name"])
df_sec["virt(hex)"] = df_sec["virt_addr"].apply(lambda x: hex(x))
df_sec["분류"] = np.where(
    (df_sec.virt_addr != 0) & (df_sec.virt_addr != df_sec.file_offset), "RAM",
    np.where(df_sec.virt_addr == df_sec.file_offset, "Flash", "-")
)
print(f"RAM 총 크기   : {ram_size} byte")
print(f"Flash 총 크기 : {flash_size} byte")
df_sec
''')

md(r"""
### 📈 시각화: 메모리 지도(Memory Map)

섹션들이 주소 공간 어디에 놓이는지 한눈에 봅니다.
에뮬레이터가 8단계에서 매핑할 **Flash 영역 / RAM 영역 / 스택**의 위치 관계를 직관적으로 이해할 수 있습니다.
""")

code(r'''
stack_addr_preview = e.get_stack_addr()

fig, ax = plt.subplots(figsize=(11, 5))
colors = {"Flash": "#4C78A8", "RAM": "#F58518", "-": "#BAB0AC"}

for _, rsec in df_sec.iterrows():
    if rsec["size"] == 0 or rsec["virt_addr"] == 0:
        continue
    ax.barh(rsec["name"], rsec["size"], left=rsec["virt_addr"],
            color=colors.get(rsec["분류"], "#BAB0AC"), edgecolor="black")
    ax.text(rsec["virt_addr"], rsec["name"], f"  {hex(rsec['virt_addr'])}",
            va="center", ha="left", fontsize=8)

ax.axvline(stack_addr_preview, color="red", ls="--", lw=1.5)
ax.text(stack_addr_preview, -0.6, f" _stack\n {hex(stack_addr_preview)}",
        color="red", fontsize=9, va="top")
ax.set_xlabel("주소 (Address)")
ax.set_title("tiny-AES 메모리 지도 — 섹션별 배치", fontsize=13)
handles = [plt.Rectangle((0,0),1,1,color=c) for c in [colors['Flash'], colors['RAM']]]
ax.legend(handles, ["Flash (코드/상수)", "RAM (데이터)"], loc="lower right")
plt.tight_layout()
plt.show()
''')

# =====================================================================
# 3단계 setEmulData
# =====================================================================
md(r"""
---
# 3단계 — 에뮬레이션 컨텍스트 확정 (`setEmulData.py`)

> **이 단계의 목표**
> 2단계 파서를 이용해, 에뮬레이션 내내 쓰일 **전역 좌표값**(모드·시작/종료 주소·I/O 주소·코드 바이트)을
> 한 번에 계산해 둡니다. 원본에서 이 모듈은 import 시점에 통째로 실행되는 "컨텍스트 초기화" 역할입니다.

핵심 값:

- `MODE` : 2(Thumb) / 4(ARM). tiny-AES는 **Thumb 모드**입니다.
- `START_ADDRESS` : `_init` 주소(코드 적재 기준).
- `emu_ADDRESS` : `main` 주소(실행 시작점).
- `exit_addr_real` : `_exit` 주소(트레이스를 멈추는 지점).
- `vir_in_addr` / `vir_out_addr` : 펌웨어가 입력을 읽고 출력을 쓰는 **가상 I/O 버퍼** 주소.
""")

code(r'''
# ── setEmulData.py 재구성 ───────────────────────────────
MODE = e.check_mode()                       # 2(Thumb) or 4(ARM)

e_section_list, ram_addr, flash_addr, ram_size, flash_size = e.section_data_list()

START_ADDRESS = e.get_start_addr()          # _init
CODE = e.get_code(START_ADDRESS)            # 실행용 코드 바이트

# 레퍼런스(디스어셈블)용 코드: Thumb이면 시작주소 LSB(=1) 보정
ref_offset = 1 if MODE == 2 else 0
REF_CODE = e.get_code(START_ADDRESS - ref_offset)

# 인접 중복 주소 제거
e_sec     = e.check_list(e_section_list)
func_list = e.check_list(list(e.sorted_functions.items()))

# 주요 심볼 주소
stack_addr      = e.get_stack_addr()
exit_addr       = e.get_func_address('exit')
exit_addr_real  = e.get_func_address('_exit')
emu_ADDRESS     = e.get_func_address('main')

# 데이터 크기 및 I/O 주소
main_len    = e.get_symbol_len('main')
vir_out_len = e.get_symbol_len('vir_OUT')
vir_in_len  = e.get_symbol_len('vir_IN')
vir_in_addr, vir_out_addr = e.get_io_addr_data()

# 디스어셈블 결과 캐시(5단계에서 채움)
instructions: List[list] = []

print(f"MODE           : {MODE}  ({'Thumb' if MODE==2 else 'ARM'})")
print(f"START_ADDRESS  : {hex(START_ADDRESS)}  (_init)")
print(f"emu_ADDRESS    : {hex(emu_ADDRESS)}  (main)")
print(f"exit_addr      : {hex(exit_addr)}  (exit)")
print(f"exit_addr_real : {hex(exit_addr_real)}  (_exit, 트레이스 종료점)")
print(f"stack_addr     : {hex(stack_addr)}  (_stack)")
print(f"main_len       : {main_len} byte")
print(f"vir_IN  주소/크기 : {hex(vir_in_addr)} / {vir_in_len} byte")
print(f"vir_OUT 주소/크기 : {hex(vir_out_addr)} / {vir_out_len} byte")
print(f"CODE 길이      : {len(CODE)} byte")
''')

md(r"""
> 💡 **확인 포인트**
> `vir_IN` 크기가 **160 byte** 로, 1단계에서 계산한 `BUFFER_BLOCK × BUFFER_NUM = 16 × 10 = 160` 과 정확히 일치합니다.
> 즉 4단계에서 만들 입력 테스트벡터의 크기가 펌웨어의 입력 버퍼와 딱 맞물립니다.
""")

# =====================================================================
# 4단계 make_TC
# =====================================================================
md(r"""
---
# 4단계 — 입력 테스트벡터 생성 (`make_TC.py`)

> **이 단계의 목표**
> 펌웨어에 먹일 **입력(평문) 데이터**를 만들어 `LogVirIN.csv`로 저장합니다.

원본 로직 그대로:
- `random.seed(1)` 로 **재현성**을 고정(매번 같은 입력 → 12단계 결정성 검증의 전제).
- 160바이트 버퍼를 0으로 채우고 **앞 64바이트만** 난수(0~255)로 채움.
- 맨 앞에 `ctr`(=0) 컬럼을 붙여 1행으로 기록. (이 `ctr`는 8단계의 입력 주입 시점 매칭에 쓰임)
""")

code(r'''
# ── make_TC.py 재구성 ───────────────────────────────────
def make_TC(out_path: str):
    random.seed(1)  # 재현성 고정
    test_VirIN = [0x0 for _ in range(BUFFER_BLOCK * BUFFER_NUM)]
    ctr = 0
    test_VirIN[0:64] = [random.randint(0, 255) for _ in range(64)]
    with open(out_path, 'w', newline='') as f:
        csv.writer(f).writerow([ctr] + test_VirIN)
    return test_VirIN

# 노트북 산출물 폴더에 입력 벡터 생성
nb_vir_in_file = os.path.join(OUTPUT_DIR, "LogVirIN.csv")
test_VirIN = make_TC(nb_vir_in_file)

# 이후 단계(입력 주입)에서 이 파일을 읽으므로, 노트북용 경로로 교체
log_vir_in_file = nb_vir_in_file

print("입력 벡터 저장:", nb_vir_in_file)
print("앞 16바이트:", test_VirIN[:16])
print("64바이트 이후(전부 0인지 확인):", set(test_VirIN[64:]))
''')

md(r"""
### 📈 시각화: 입력 평문 바이트 맵

160바이트 입력을 `10 × 16` 격자로 그립니다(AES 블록 = 한 줄 16바이트).
**앞 4줄(64바이트)만 난수**로 채워지고 나머지는 0(짙은색)임을 직관적으로 확인할 수 있습니다.
""")

code(r'''
grid = np.array(test_VirIN).reshape(BUFFER_NUM, BUFFER_BLOCK)

fig, ax = plt.subplots(figsize=(9, 5.5))
im = ax.imshow(grid, cmap="viridis", aspect="auto")
for i in range(BUFFER_NUM):
    for j in range(BUFFER_BLOCK):
        ax.text(j, i, grid[i, j], ha="center", va="center",
                color="white" if grid[i, j] < 128 else "black", fontsize=7)
ax.set_xlabel("블록 내 바이트 위치 (0~15)")
ax.set_ylabel("블록 번호")
ax.set_title("입력 평문 테스트벡터 (vir_IN, 160 byte)", fontsize=12)
ax.set_xticks(range(BUFFER_BLOCK)); ax.set_yticks(range(BUFFER_NUM))
fig.colorbar(im, ax=ax, label="byte value (0~255)")
plt.tight_layout(); plt.show()
''')

# =====================================================================
# 5단계 disassembly
# =====================================================================
md(r"""
---
# 5단계 — 디스어셈블 (`emul.make_disassembly_file`)

> **이 단계의 목표**
> Capstone으로 바이너리를 **사람이 읽는 어셈블리**로 풀어내고(`disassembly.txt`),
> 동시에 `{주소 → (니모닉, 피연산자)}` 캐시(`instructions`)를 만듭니다.
> 이 캐시는 6단계에서 트레이스 로그에 "이 주소에서 무슨 명령이 실행됐는지"를 붙일 때 쓰입니다.

원본 로직의 까다로운 부분을 그대로 살립니다.
- Thumb 모드면 시작주소를 1 보정해 **짝수 주소**에서 디스어셈블 시작.
- 코드 사이에 섹션/함수 경계가 오면 헤더 라인 삽입.
- `.data` 섹션은 명령이 아니라 **헥사 바이트**로 출력.
- 해석 불가능한 바이트(데이터/패딩)를 만나면 `MODE` 크기만큼 건너뛰고 **계속 진행**(Resume).
""")

code(r'''
# ── emul.make_disassembly_file 재구성 ───────────────────
def make_disassembly_file(out_path: str):
    if os.path.exists(out_path):
        os.remove(out_path)

    cs_mode = CS_MODE_THUMB if MODE == 2 else CS_MODE_ARM
    md_engine = Cs(CS_ARCH_ARM, cs_mode)
    md_engine.detail = True

    addr_offset = 1 if MODE == 2 else 0
    start_addr  = START_ADDRESS - addr_offset
    code_data   = REF_CODE
    end_addr    = start_addr + len(code_data)

    curr_addr = start_addr
    sec_idx, func_idx = 1, 0
    e_secs, funcs = e_sec, func_list
    virtual_addr, current_sec_name = 0, ""

    instructions.clear()  # 중복 실행 방지

    with open(out_path, 'w', encoding='utf-8') as f:
        while curr_addr < end_addr:
            offset = curr_addr - start_addr
            if offset >= len(code_data):
                break

            # 1) 섹션 헤더
            if sec_idx < len(e_secs):
                sec_info = e_secs[sec_idx]           # [Addr, Offset, Size, Name]
                sec_start = sec_info[1]
                if sec_start - 2 == curr_addr or sec_start == curr_addr:
                    f.write(f"\nsection\t\t : {sec_info[3]}\n")
                    if sec_info[0] != 0:
                        f.write(f"REAL ADDRESS : {hex(sec_info[0])}\n\n")
                        virtual_addr = sec_info[0]
                        current_sec_name = sec_info[3]
                    sec_idx += 1

            # 2) 함수 헤더
            if func_idx < len(funcs):
                func_start = funcs[func_idx][1]
                if func_start == curr_addr + addr_offset:
                    f.write(f"\nfunction\t : {funcs[func_idx][0]}\n\n")
                    func_idx += 1

            # 3) 한 명령어 디스어셈블
            insns = list(md_engine.disasm(code_data[offset:], curr_addr, count=1))
            if insns:
                insn = insns[0]
                if virtual_addr != 0 and current_sec_name == '.data':
                    hex_bytes = "".join([f"\\x{b:x}" for b in insn.bytes])
                    f.write(f"0x{insn.address:x}:[0x{virtual_addr:x}] {hex_bytes}")
                else:
                    f.write(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}\n")
                instructions.append([insn.address, insn.mnemonic, insn.op_str])
                curr_addr += insn.size
                if virtual_addr != 0:
                    virtual_addr += MODE
            else:
                # 디스어셈블 실패(데이터/패딩) → 건너뛰고 계속
                curr_addr += MODE
                if virtual_addr != 0:
                    virtual_addr += MODE

nb_disasm_file = os.path.join(OUTPUT_DIR, "disassembly.txt")
make_disassembly_file(nb_disasm_file)
print(f"디스어셈블 명령어 수: {len(instructions)}")
print("저장:", nb_disasm_file)
''')

md(r"""
### 🔎 중간 산출물: 디스어셈블리 미리보기 (`main` 함수 도입부)
""")

code(r'''
with open(nb_disasm_file, encoding="utf-8") as f:
    lines = f.read().splitlines()

# 'function : main' 위치를 찾아 그 부분을 보여준다
start = next((i for i, ln in enumerate(lines) if "main" in ln and "function" in ln), 0)
print("\n".join(lines[start:start + 30]))
''')

md(r"""
### 📈 시각화: 명령어 니모닉 빈도

디스어셈블된 코드에서 어떤 명령이 많이 쓰였는지 상위 15개를 봅니다.
`ldr/str`(메모리 접근), `mov`, `bl`(함수호출) 등의 분포로 코드 성격을 가늠할 수 있습니다.
""")

code(r'''
from collections import Counter
mnem_counts = Counter(insn[1] for insn in instructions)
top = mnem_counts.most_common(15)

fig, ax = plt.subplots(figsize=(10, 4.5))
names = [t[0] for t in top][::-1]
vals  = [t[1] for t in top][::-1]
ax.barh(names, vals, color="#4C78A8")
for i, v in enumerate(vals):
    ax.text(v, i, f" {v}", va="center", fontsize=8)
ax.set_title("명령어 니모닉 빈도 (상위 15개)", fontsize=12)
ax.set_xlabel("등장 횟수")
plt.tight_layout(); plt.show()
''')

# =====================================================================
# 6단계 logger
# =====================================================================
md(r"""
---
# 6단계 — 레지스터 트레이스 로거 (`logger.py`)

> **이 단계의 목표**
> 에뮬레이터가 명령어 하나를 실행할 때마다 호출되어, **17개 레지스터의 값**을 기록하는 로거를 만듭니다.
> 이 트레이스가 바로 PRE-SCA의 핵심 산출물 — **"가상 부채널 데이터"** 입니다.

기록 구조(헤더):
`[ctr, Address, Opcode, Operands] + bR0..bCPSR(실행 전 17개) + aR0..aCPSR(실행 후 17개)`

> 🧩 **"실행 전(before) / 실행 후(after)"를 한 줄에 담는 트릭**
> 훅은 명령어 실행 *직전*에 호출됩니다. 따라서 지금 읽은 레지스터 값은
> **이번 명령의 before**이면서 동시에 **직전 명령의 after**입니다.
> 그래서 현재 값을 이번 행의 앞부분(b\*)에 쓰고, **이전 행의 뒷부분(a\*)에 덧붙이는** 방식으로
> 한 번의 읽기로 before/after를 모두 채웁니다.
""")

code(r'''
# 시나리오 검증용 전역 매트릭스 (원본 logger.LOG_MATRIX 호환)
LOG_MATRIX: List[List[Any]] = []

class TraceLogger:
    """명령어별 레지스터 상태/명령 흐름을 기록하는 로거 (원본 logger.py 재구성)."""

    REGISTERS = [
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_FP,
        UC_ARM_REG_IP, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
        UC_ARM_REG_CPSR,
    ]
    HEADER = ['ctr', 'Address', 'Opcode', 'Operands',
              'bR0','bR1','bR2','bR3','bR4','bR5','bR6','bR7','bR8','bR9','bR10',
              'bFP','bIP','bSP','bLR','bPC','bCPSR',
              'aR0','aR1','aR2','aR3','aR4','aR5','aR6','aR7','aR8','aR9','aR10',
              'aFP','aIP','aSP','aLR','aPC','aCPSR']

    def __init__(self, log_folder: str):
        self.ctr = 0
        self.current_log_matrix: List[List[Any]] = []
        self.log_file_path = ""
        self._insn_cache: Dict[int, Tuple[str, str]] = {}
        self._is_cache_built = False

        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        self.log_folder = os.path.join(log_folder, f"{self.timestamp} {log_file_name}")
        os.makedirs(self.log_folder, exist_ok=True)
        self.reset_buffer()

    def reset_buffer(self):
        self.current_log_matrix = [self.HEADER[:]]
        self.ctr = 0

    def set_file_index(self, index: int):
        fn = f"{self.timestamp} LogReg.csv" if index == 0 else f"{self.timestamp} LogReg_Faulty.csv"
        self.log_file_path = os.path.join(self.log_folder, fn)

    def get_log_file_path(self):
        return self.log_file_path

    def _ensure_insn_cache(self):
        """instructions 리스트를 dict로 변환해 주소 검색을 O(1)로."""
        if not self._is_cache_built and instructions:
            for addr, mnem, ops in instructions:
                self._insn_cache[addr] = (mnem, ops)
            self._is_cache_built = True

    def get_instruction_info(self, address: int):
        self._ensure_insn_cache()
        return self._insn_cache.get(address, ("UNKNOWN", "UNKNOWN"))

    def read_registers(self, uc: Uc):
        return [uc.reg_read(r) for r in self.REGISTERS]

    def log_state(self, uc: Uc, address: int):
        global LOG_MATRIX
        regs = self.read_registers(uc)
        opcode, op_str = self.get_instruction_info(address)

        # 이번 명령의 before 부분 기록
        row = [self.ctr, hex(address), opcode, op_str] + regs
        self.current_log_matrix.append(row)

        # 직전 행의 after 부분에 현재 값을 덧붙임
        if self.ctr >= 1:
            self.current_log_matrix[self.ctr].extend(regs)

        self.ctr += 1

        # 종료 지점(_exit) 도달 → 파일 저장 + 전역 백업 + 버퍼 리셋
        target_exit = exit_addr_real - (1 if MODE == 2 else 0)
        if address == target_exit:
            LOG_MATRIX.extend(self.current_log_matrix)
            with open(self.log_file_path, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerows(self.current_log_matrix)
            self.reset_buffer()

print("✅ TraceLogger 클래스 정의 완료")
print("기록 컬럼 수:", len(TraceLogger.HEADER), "(ctr/addr/opcode/operands + before17 + after17)")
''')

# =====================================================================
# 7단계 scenario
# =====================================================================
md(r"""
---
# 7단계 — 오류주입 시나리오 (`scenario.py`)

> **이 단계의 목표**
> `LogFI.csv`에 정의된 **오류주입(Fault Injection) 시나리오**를 로드하는 `Scenario`를 만듭니다.
> 오류주입은 "특정 명령 시점(`ctr`)에서 레지스터를 강제로 바꾸거나(NOP/Flip/대입) 명령을 건너뛰는" 행위로,
> 칩에 글리치를 가했을 때의 효과를 에뮬레이터에서 흉내 냅니다.

`LogFI.csv` 형식 (한 행 = 한 개의 오류주입):

| 컬럼 | 의미 |
|:---|:---|
| `ctr` | 몇 번째 실행 명령에서 주입할지 |
| `isNOP` | TRUE면 그 명령을 NOP 처리(PC만 전진, 명령 무효화) |
| `r0`~`cpsr` | `NaN`=변경없음 / `Flip`=비트반전 / 숫자=그 값으로 대입 |

> 본 프로젝트의 `ini_set/LogFI.csv`는 **헤더만 있고 비어 있어**, 기본 실행은 **정상(Normal) 1회**만 돕니다.
> 11단계에서 예제 시나리오를 채워 오류주입 동작을 직접 확인합니다.
""")

code(r'''
class Scenario:
    """오류주입 시나리오 로드/실행 (원본 scenario.py 재구성)."""

    FIELD_NAMES = ['ctr', 'isNOP',
                   'r0','r1','r2','r3','r4','r5','r6','r7','r8','r9','r10',
                   'fp','ip','sp','lr','pc','cpsr']
    REG_MAP = {
        'r0': UC_ARM_REG_R0, 'r1': UC_ARM_REG_R1, 'r2': UC_ARM_REG_R2, 'r3': UC_ARM_REG_R3,
        'r4': UC_ARM_REG_R4, 'r5': UC_ARM_REG_R5, 'r6': UC_ARM_REG_R6, 'r7': UC_ARM_REG_R7,
        'r8': UC_ARM_REG_R8, 'r9': UC_ARM_REG_R9, 'r10': UC_ARM_REG_R10,
        'fp': UC_ARM_REG_FP, 'ip': UC_ARM_REG_IP, 'sp': UC_ARM_REG_SP,
        'lr': UC_ARM_REG_LR, 'pc': UC_ARM_REG_PC, 'cpsr': UC_ARM_REG_CPSR,
    }

    def __init__(self, fault_file: str):
        self.fault_list: List[Dict[str, Any]] = []
        self._load(fault_file)

    @property
    def Fault_list(self):
        return self.fault_list

    def _load(self, fault_file: str):
        if not os.path.exists(fault_file):
            print("Notice: Fault injection file not found. Running in normal mode.")
            return
        # 원본과 동일하게 전체를 try/except로 감싼다.
        # 비어 있거나 구분자가 없는 LogFI.csv는 csv.Sniffer가 예외를 던지는데,
        # 이때 조용히 normal 모드로 폴백하는 것이 원본 동작이다.
        try:
            with open(fault_file, 'r', encoding='utf-8-sig') as f:
                has_header = csv.Sniffer().has_header(f.read(1024))
                f.seek(0)
                if has_header:
                    next(f)
                reader = csv.DictReader(f, fieldnames=self.FIELD_NAMES)
                for row in reader:
                    p = self._preprocess(row)
                    if p:
                        self.fault_list.append(p)
        except Exception as ex:
            print(f"Error loading fault scenario: {ex}")

    def _preprocess(self, row: Dict[str, str]) -> Dict[str, Any]:
        processed = {}
        try:
            processed['ctr'] = int(row['ctr'])
        except (ValueError, TypeError):
            return {}
        processed['isNOP'] = (row.get('isNOP', '').strip().upper() == 'TRUE')
        for reg_name in self.REG_MAP:
            val = row.get(reg_name, 'NaN')
            val = (val or 'NaN').strip()
            if val in ('NaN', ''):
                processed[reg_name] = None
            elif val == 'Flip':
                processed[reg_name] = 'Flip'
            else:
                try:
                    processed[reg_name] = int(val, 0)
                except ValueError:
                    processed[reg_name] = None
        return processed

    def check_nop(self, index: int) -> bool:
        if 0 <= index < len(self.fault_list):
            return self.fault_list[index]['isNOP']
        return False

    def nop(self, uc: Uc):
        """PC를 한 명령어만큼 전진시켜 현재 명령을 건너뜀."""
        pc = uc.reg_read(UC_ARM_REG_PC)
        uc.reg_write(UC_ARM_REG_PC, pc + MODE)

    def _flip_register(self, uc: Uc, reg_const: int):
        val = uc.reg_read(reg_const)
        mask = 0xFFFFFFFF if MODE == 4 else 0xFFFF
        uc.reg_write(reg_const, val ^ mask)

    def modify_regs(self, uc: Uc, index: int):
        if not (0 <= index < len(self.fault_list)):
            return
        data = self.fault_list[index]
        for reg_name, reg_const in self.REG_MAP.items():
            val = data.get(reg_name)
            if val is None:
                continue
            if val == 'Flip':
                self._flip_register(uc, reg_const)
            else:
                uc.reg_write(reg_const, val)

print("✅ Scenario 클래스 정의 완료")
''')

# =====================================================================
# 8단계 init_emulator + hooks
# =====================================================================
md(r"""
---
# 8단계 — 에뮬레이터 구성 & 훅 (`emul.init_emulator`, hooks)

> **이 단계의 목표**
> Unicorn ARM 에뮬레이터를 만들고, **메모리 매핑 → 레지스터 초기화 → 바이너리 적재**를 한 뒤,
> 명령어마다 불릴 **두 개의 훅**을 정의합니다.

### 8.1 `init_emulator` — 가상 머신 준비
1. **Flash 매핑**: `START_ADDRESS`부터 `flash_size`만큼, 4KB 페이지 경계로 정렬해 매핑.
2. **RAM 매핑**: RAM 시작 ~ 스택 끝까지 정렬해 매핑.
3. **레지스터 초기화**: `SP/FP = _stack`, `LR = exit` (리턴 시 종료되도록).
4. **바이너리 적재**: 각 섹션을 가상주소에 기록.
""")

code(r'''
def init_emulator() -> Uc:
    arch = UC_ARCH_ARM
    mode = UC_MODE_THUMB if MODE == 2 else UC_MODE_ARM
    uc = Uc(arch, mode)

    PAGE = 4 * 1024

    # 1) Flash 매핑
    flash_start = START_ADDRESS
    flash_end   = flash_start + flash_size
    flash_base  = (flash_start // PAGE) * PAGE
    flash_aligned = ((flash_end - flash_base + PAGE - 1) // PAGE) * PAGE
    uc.mem_map(flash_base, flash_aligned)

    # 2) RAM 매핑
    ram_start = ram_addr[0]
    ram_end   = stack_addr
    ram_base  = (ram_start // PAGE) * PAGE
    ram_aligned = ((ram_end - ram_base + PAGE - 1) // PAGE) * PAGE
    try:
        uc.mem_map(ram_base, ram_aligned)
    except UcError:
        pass  # 겹침 방지

    # 3) 레지스터 초기화
    uc.reg_write(UC_ARM_REG_SP, stack_addr)
    uc.reg_write(UC_ARM_REG_FP, stack_addr)
    uc.reg_write(UC_ARM_REG_LR, exit_addr)

    # 4) 바이너리 적재 (섹션별)
    with open(elf_file, "rb") as f:
        for section in e_sec:
            virt_addr, offset, size, _name = section
            if virt_addr != 0:
                f.seek(offset)
                content = f.read(size)
                try:
                    uc.mem_write(virt_addr, content)
                except UcError:
                    pass
    return uc

print("✅ init_emulator 정의 완료")
''')

md(r"""
### 8.2 두 개의 명령어 훅 (`UC_HOOK_CODE`)

에뮬레이터는 명령어를 실행하기 **직전**마다 등록된 훅을 호출합니다. 원본은 두 훅을 씁니다.

| 훅 | 역할 |
|:---|:---|
| `hook_scene_injection` | ① `sync_ctr`에 맞는 **입력 데이터 주입** ② 시나리오 조건에 맞으면 **오류주입** |
| `hook_code_trace` | 매 명령마다 **레지스터 트레이스 기록**, `_exit` 도달 시 `emu_stop()` |

> 🧭 **오류주입 시점 매칭 원리**
> 1차(Normal) 실행에서 만든 `LOG_MATRIX`에는 "몇 번째 ctr에서 어떤 주소가 실행됐는지"가 들어 있습니다.
> 2차(Faulty) 실행 때, 시나리오의 `ctr`에 대응하는 **주소**가 현재 실행 주소와 같아지는 순간 오류를 주입합니다.
> 그래서 오류주입은 **정상 실행을 한 번 마친 뒤**에야 정확한 시점을 알 수 있습니다.
""")

code(r'''
# 입력 주입 동기 카운터 (원본 emul.sync_ctr 전역)
sync_ctr = 0
# 현재 활성 로거 (run에서 매 실행마다 교체)
active_logger: Optional[TraceLogger] = None

def get_input_data() -> List[List[int]]:
    """LogVirIN.csv 로드."""
    rows = []
    if not os.path.exists(log_vir_in_file):
        return []
    with open(log_vir_in_file, newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            if row:
                rows.append(list(map(int, row)))
    return rows

def inject_input_data(uc: Uc, data_row: List[int]):
    uc.mem_write(vir_in_addr, bytes(data_row))

def hook_code_trace(uc: Uc, address: int, size: int, user_data: Any):
    """명령어 실행 추적 + 종료 처리."""
    active_logger.log_state(uc, address)
    exit_target = exit_addr_real - (1 if MODE == 2 else 0)
    if address == exit_target:
        uc.emu_stop()

def hook_scene_injection(uc: Uc, address: int, size: int, scene: "Scenario"):
    """입력 주입 + 오류주입."""
    global sync_ctr

    # 1) 입력 데이터 주입 (sync_ctr 매칭)
    for row in get_input_data():
        if row and row[0] == sync_ctr:
            inject_input_data(uc, row[1:])

    # 2) 오류 주입 (정상 실행으로 만들어진 LOG_MATRIX 기반 주소 매칭)
    if scene.Fault_list and LOG_MATRIX:
        for i, fault in enumerate(scene.Fault_list):
            try:
                target_ctr = int(fault['ctr'])
                if target_ctr + 1 < len(LOG_MATRIX):
                    log_addr_str = LOG_MATRIX[target_ctr + 1][1]  # Address 컬럼
                    if hex(address) == log_addr_str:
                        if scene.check_nop(i):
                            scene.nop(uc)
                        else:
                            scene.modify_regs(uc, i)
            except (ValueError, IndexError):
                continue

    sync_ctr += 1
    exit_target = exit_addr_real - (1 if MODE == 2 else 0)
    if address == exit_target:
        sync_ctr = 0

print("✅ 훅 함수 정의 완료")
''')

# =====================================================================
# 9단계 run (Normal)
# =====================================================================
md(r"""
---
# 9단계 — 정상(Normal) 실행 & 트레이스 수집 (`emul.run`)

> **이 단계의 목표**
> 지금까지 만든 부품을 조립해 **실제로 에뮬레이션을 돌리고**, 명령어별 레지스터 트레이스(`LogReg.csv`)와
> 가상 I/O 메모리(`LogVirIN/OUT.csv`)를 저장합니다.

원본 `run()`은 시나리오에 오류가 있으면 **2회(Normal→Faulty)**, 없으면 **1회**만 실행합니다.
여기서는 단계를 나눠 이해하기 위해, 먼저 **정상 1회**만 실행하는 함수를 정의합니다.
(오류주입 2회 실행은 11단계에서 다룹니다.)
""")

code(r'''
def make_io_data_files(uc: Uc, logger_obj: TraceLogger, index: int):
    """가상 I/O 메모리(VirIN/VirOUT)를 CSV로 저장."""
    log_folder = logger_obj.log_folder
    date_prefix = logger_obj.timestamp
    suffix = "_Faulty" if index > 0 else ""

    out_path = os.path.join(log_folder, f"{date_prefix} LogVirOUT{suffix}.csv")
    out_data = uc.mem_read(vir_out_addr, vir_out_len)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(list(out_data))

    in_path = os.path.join(log_folder, f"{date_prefix} LogVirIN.csv")
    in_data = uc.mem_read(vir_in_addr, vir_in_len)
    with open(in_path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(list(in_data))
    return out_data, in_data


def run_once(scene: "Scenario", logger_obj: TraceLogger, index: int):
    """에뮬레이터 1회 실행."""
    global active_logger, sync_ctr
    active_logger = logger_obj
    sync_ctr = 0
    logger_obj.set_file_index(index)

    mu = init_emulator()

    code_end = START_ADDRESS + len(CODE)
    mu.hook_add(UC_HOOK_CODE, hook_scene_injection, scene,
                begin=START_ADDRESS, end=code_end)
    mu.hook_add(UC_HOOK_CODE, hook_code_trace, scene,
                begin=START_ADDRESS, end=code_end)

    ok = True
    try:
        mu.emu_start(emu_ADDRESS, emu_ADDRESS + main_len)
    except UcError as err:
        # 원본 run()의 에러 처리: 오류주입이 잘못된 메모리 접근을 유발하면
        # 부분 로그를 저장하고 계속 진행한다(크래시 그 자체도 하나의 fault 결과).
        ok = False
        with open(logger_obj.get_log_file_path(), 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(logger_obj.current_log_matrix)
        print(f"ERROR: {err}")
    out_data, in_data = make_io_data_files(mu, logger_obj, index)
    return mu, out_data, in_data, ok

print("✅ run_once 정의 완료")
''')

code(r'''
# ── 정상 실행 ───────────────────────────────────────────
print("Emulating the code..")

LOG_MATRIX.clear()                       # 전역 트레이스 초기화
scene_normal = Scenario(fault_reg_file)  # LogFI.csv (기본은 비어 있음 → 정상 모드)
logger_normal = TraceLogger(OUTPUT_DIR)

mu, out_data, in_data, _ok = run_once(scene_normal, logger_normal, index=0)
print(">>> Emulation done.")
print("트레이스된 명령어 수 :", len(LOG_MATRIX) - 1, "(헤더 제외)")
print("LogReg 저장 경로     :", logger_normal.get_log_file_path())
''')

md(r"""
### 🔎 중간 산출물: 레지스터 트레이스 (`LogReg`) 앞부분

각 행은 명령어 1개의 실행 기록입니다. `b*`는 실행 전, `a*`는 실행 후 레지스터 값입니다.
""")

code(r'''
df_trace = pd.DataFrame(LOG_MATRIX[1:], columns=LOG_MATRIX[0])
print("트레이스 shape:", df_trace.shape)
df_trace.head(12)[['ctr','Address','Opcode','Operands','bR0','bR1','bR2','bR3','bSP','bPC','aPC']]
''')

# =====================================================================
# 10단계 시각화
# =====================================================================
md(r"""
---
# 10단계 — 트레이스 분석 & 시각화

> **이 단계의 목표**
> 수집한 레지스터 트레이스를 **그림으로** 살펴보며, PRE-SCA가 만들어내는 "가상 부채널"이
> 어떤 정보를 담는지 직관적으로 이해합니다.
""")

md(r"""
### 📈 ① PC(프로그램 카운터) 실행 흐름

x축은 실행 순서(ctr), y축은 실행 주소입니다.
**평평한 톱니 구간**은 루프(AES 라운드 반복), **계단 점프**는 함수 호출/리턴을 나타냅니다.
""")

code(r'''
pc_before = df_trace['bPC'].astype(np.int64)

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.plot(df_trace['ctr'].astype(int), pc_before, lw=0.6, color="#4C78A8")
ax.set_xlabel("실행 순서 (ctr)")
ax.set_ylabel("실행 주소 (PC)")
ax.set_title("실행 흐름 — PC over time (AES 암호화 트레이스)", fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: hex(int(v))))
ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()
''')

md(r"""
### 📈 ② 레지스터 활동(activity) 히트맵

각 명령 실행 후 레지스터 값이 **이전 대비 바뀌었는지**를 0/1로 표시해, 시간에 따른 레지스터 사용 패턴을 봅니다.
실제 부채널 분석에서 "어느 시점에 어떤 레지스터가 데이터를 운반하는가"를 가늠하는 것과 같은 관점입니다.
(명령 수가 많으므로 앞부분 일부 구간만 표시)
""")

code(r'''
after_cols = ['aR0','aR1','aR2','aR3','aR4','aR5','aR6','aR7','aR8','aR9','aR10',
              'aFP','aIP','aSP','aLR','aPC','aCPSR']
seg = df_trace.iloc[:400].copy()
A = seg[after_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(np.int64).to_numpy()

# 직전 행 대비 변화 여부 (변화=1)
changed = (np.diff(A, axis=0) != 0).astype(int)

fig, ax = plt.subplots(figsize=(12, 5))
im = ax.imshow(changed.T, aspect="auto", cmap="magma", interpolation="nearest")
ax.set_yticks(range(len(after_cols)))
ax.set_yticklabels([c[1:] for c in after_cols])
ax.set_xlabel("실행 순서 (ctr, 앞 400개)")
ax.set_ylabel("레지스터")
ax.set_title("레지스터 변화 히트맵 (밝을수록 그 시점에 값이 바뀜)", fontsize=12)
fig.colorbar(im, ax=ax, label="변화 여부 (0/1)")
plt.tight_layout(); plt.show()
''')

md(r"""
### 🔎 ③ AES 암호화 결과 (`vir_OUT`)

펌웨어가 출력 버퍼에 쓴 결과입니다. 입력 64바이트(4블록)에 대응하는 **암호문**이 앞부분에 채워집니다.
""")

code(r'''
out_list = list(out_data)
print("VirOUT 앞 16바이트(첫 블록 암호문):")
print(" ".join(f"{b:02x}" for b in out_list[:16]))

og = np.array(out_list).reshape(BUFFER_NUM, BUFFER_BLOCK)
fig, ax = plt.subplots(figsize=(9, 5.5))
im = ax.imshow(og, cmap="cividis", aspect="auto")
for i in range(BUFFER_NUM):
    for j in range(BUFFER_BLOCK):
        ax.text(j, i, og[i, j], ha="center", va="center",
                color="white" if og[i, j] < 128 else "black", fontsize=7)
ax.set_title("AES 출력 버퍼 (vir_OUT, 160 byte)", fontsize=12)
ax.set_xlabel("블록 내 바이트 위치"); ax.set_ylabel("블록 번호")
ax.set_xticks(range(BUFFER_BLOCK)); ax.set_yticks(range(BUFFER_NUM))
fig.colorbar(im, ax=ax, label="byte value")
plt.tight_layout(); plt.show()
''')

# =====================================================================
# 11단계 Fault Injection
# =====================================================================
md(r"""
---
# 11단계 — 오류주입(Fault Injection) 실행 & 비교

> **이 단계의 목표**
> 9단계의 정상 트레이스를 기준으로, **예제 오류주입 시나리오**를 만들어 2차 실행을 돌리고,
> 정상 결과와 **무엇이 달라졌는지** 비교합니다.

원본은 `ini_set/LogFI.csv`가 채워져 있으면 `run()`이 자동으로 2회(Normal→Faulty) 실행합니다.
여기서는 학습을 위해 시나리오를 **직접 한 줄 생성**합니다.

예제: 정상 트레이스의 중간 지점 명령에서 **레지스터 하나를 비트반전(Flip)** 시켜 1바이트 오류를 유도합니다.
(`Flip`은 DFA(차분오류분석) 키복원 공격의 전형적 오류 모델입니다.)
""")

code(r'''
# ── 예제 시나리오 작성 ──────────────────────────────────
# 정상 트레이스에서 'AES 연산 중반'에 해당하는 ctr 하나를 골라 R0를 Flip 한다.
# (이 시점은 데이터 레지스터를 다루는 구간이라 크래시 없이 출력만 오염시키는,
#  DFA(차분오류분석)에 적합한 깨끗한 예제가 된다.)
target_ctr = int(len(df_trace) * 0.5)   # 트레이스 중반 지점
example_fault_file = os.path.join(OUTPUT_DIR, "LogFI_example.csv")

header = ['ctr','isNOP','R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','FP','IP','SP','LR','PC','CPSR']
row    = [target_ctr,'FALSE'] + ['NaN']*17
row[2] = 'Flip'   # R0 컬럼(인덱스 2)을 Flip

with open(example_fault_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(header); w.writerow(row)

print(f"오류주입 시점 ctr = {target_ctr}")
print(f"해당 명령        : {df_trace.iloc[target_ctr]['Address']} "
      f"{df_trace.iloc[target_ctr]['Opcode']} {df_trace.iloc[target_ctr]['Operands']}")
print("→ R0 레지스터를 Flip(비트반전) 합니다.")
''')

md(r"""
### 정상 → 오류 2회 실행 (원본 `run()`과 동일한 흐름)

원본 `run()`을 그대로 따라, `LOG_MATRIX`를 비우고 **Normal → Faulty** 순서로 실행합니다.
- 1차(Normal): 오류 없이 실행하며 `LOG_MATRIX`(시점 매칭표)를 채움.
- 2차(Faulty): 1차의 시점 정보를 보고 `target_ctr` 시점에 R0를 Flip.
""")

code(r'''
def run_full(fault_file: str):
    """원본 emul.run() 재구성 — Fault 있으면 Normal→Faulty 2회."""
    global LOG_MATRIX
    make_disassembly_file(nb_disasm_file)   # instructions 재생성(원본 run 첫 단계)
    scene = Scenario(fault_file)
    run_count = 2 if scene.Fault_list else 1

    logger_obj = TraceLogger(OUTPUT_DIR)
    LOG_MATRIX.clear()
    results = []
    for i in range(run_count):
        mu_i, out_i, in_i, ok_i = run_once(scene, logger_obj, index=i)
        label = "Normal" if i == 0 else "Faulty"
        print(f">>> [{label}] done. (저장: {os.path.basename(logger_obj.get_log_file_path())})")
        results.append((label, list(out_i)))
    return logger_obj, results

logger_fi, fi_results = run_full(example_fault_file)
''')

md(r"""
### 📈 정상 출력 vs 오류주입 출력 비교

두 실행의 `vir_OUT`(첫 64바이트)을 나란히 비교합니다. **빨간색 칸이 오류로 값이 달라진 바이트**입니다.
오류주입이 암호문에 어떻게 전파(diffusion)되는지 눈으로 확인할 수 있습니다.
""")

code(r'''
normal_out = np.array(fi_results[0][1][:64])
faulty_out = np.array(fi_results[1][1][:64]) if len(fi_results) > 1 else normal_out
diff_mask  = (normal_out != faulty_out)

print(f"달라진 바이트 수 : {int(diff_mask.sum())} / 64")

fig, axes = plt.subplots(3, 1, figsize=(13, 6), constrained_layout=True)
for ax, data, title in zip(
        axes, [normal_out, faulty_out, diff_mask.astype(int)],
        ["정상(Normal) 출력", "오류주입(Faulty) 출력", "차이(diff) — 노란 칸이 달라진 바이트"]):
    g = data.reshape(4, 16)
    cmap = "viridis" if "diff" not in title else "hot"
    ax.imshow(g, cmap=cmap, aspect="auto")
    for i in range(4):
        for j in range(16):
            ax.text(j, i, g[i, j], ha="center", va="center", fontsize=6,
                    color="white" if g[i, j] < 128 else "black")
    ax.set_title(title, fontsize=11); ax.set_yticks(range(4)); ax.set_xticks(range(16))
plt.show()
''')

# =====================================================================
# 12단계 test_cmp
# =====================================================================
md(r"""
---
# 12단계 — 재현성(결정성) 검증 (`test_cmp.py`)

> **이 단계의 목표**
> 같은 입력으로 여러 번 실행했을 때 **결과가 매번 비트 단위로 동일한지**(결정성)를 확인합니다.
> PRE-SCA는 사전 분석 도구이므로, 같은 조건이면 항상 같은 트레이스가 나와야 신뢰할 수 있습니다.

원본 `test_cmp.py`는 `./log` 폴더 안의 여러 실행 결과 폴더를 골라
`LogReg / LogVirIN / LogVirOUT` 및 `disassembly.txt`를 **바이너리 비교**합니다.
여기서는 정상 실행을 **두 번** 돌려 두 결과가 동일한지 직접 검증합니다.
""")

code(r'''
def compare_files_binary(a: str, b: str) -> bool:
    with open(a, 'rb') as fa, open(b, 'rb') as fb:
        return fa.read() == fb.read()

def get_file_by_suffix(folder: str, suffix: str):
    found = glob.glob(os.path.join(folder, "*" + suffix))
    return found[0] if len(found) == 1 else None

# 정상 실행을 한 번 더 수행 (새 타임스탬프 폴더 생성)
import time; time.sleep(1.1)
LOG_MATRIX.clear()
logger_run2 = TraceLogger(OUTPUT_DIR)
run_once(Scenario(fault_reg_file), logger_run2, index=0)

folder_a = logger_normal.log_folder
folder_b = logger_run2.log_folder

print("기준 폴더 :", os.path.basename(folder_a))
print("비교 폴더 :", os.path.basename(folder_b))
print("-" * 60)
all_matched = True
for suffix in ["LogReg.csv", "LogVirIN.csv", "LogVirOUT.csv"]:
    fa = get_file_by_suffix(folder_a, suffix)
    fb = get_file_by_suffix(folder_b, suffix)
    if fa and fb:
        same = compare_files_binary(fa, fb)
        all_matched &= same
        print(f"  [{'일치' if same else '불일치!'}] {suffix}")
    else:
        all_matched = False
        print(f"  [파일없음] {suffix}")

print("=" * 60)
print("결과:", "✅ 두 실행 결과가 완전히 동일합니다 (결정적)."
      if all_matched else "⚠️ 일부 파일이 다릅니다.")
''')

# =====================================================================
# 요약
# =====================================================================
md(r"""
---
## 📝 전체 요약

| 단계 | 한 일 | 핵심 산출물 |
|:----:|:---|:---|
| 0~1 | 라이브러리/경로/상수 설정 | `BUFFER_BLOCK·BUFFER_NUM`, 입력 160byte |
| 2 | ELF 파싱 | 심볼표·섹션표·**메모리 지도** |
| 3 | 컨텍스트 확정 | `MODE=2(Thumb)`, `main`/`_exit` 주소, I/O 주소 |
| 4 | 입력 평문 생성 | `LogVirIN.csv`, **바이트 맵** |
| 5 | 디스어셈블 | `disassembly.txt`, **니모닉 빈도** |
| 6~8 | 로거·시나리오·에뮬레이터·훅 | `TraceLogger`, `Scenario`, `init_emulator` |
| 9 | 정상 실행 | `LogReg.csv` (명령어별 레지스터 트레이스) |
| 10 | 시각화 | **PC 실행흐름 · 레지스터 히트맵 · 출력 맵** |
| 11 | 오류주입 | `LogReg_Faulty.csv`, **정상 vs 오류 비교** |
| 12 | 재현성 검증 | 바이너리 동일성 확인 |

### ✅ PRE-SCA의 핵심 동작 원리 (한 문장 요약)

> **"ARM 펌웨어를 에뮬레이터 위에서 한 명령씩 실행하며 모든 레지스터 상태를 기록(트레이스)하고,
> 원하는 시점에 레지스터를 조작(오류주입)해 그 효과를 사전에 분석하는 도구"**

- **부채널(SCA) 관점**: 명령어별 레지스터 트레이스 = 실측 전력파형 이전의 "가상 누설" 데이터.
- **오류주입(FIA) 관점**: `ctr` 시점 + 레지스터 조작 = 글리치 효과의 사전 시뮬레이션.
- **결정성**: `random.seed` 고정 + 동일 바이너리 → 항상 동일 트레이스 → 분석 신뢰성 확보.

### 🔁 원본 모듈 ↔ 노트북 대응표

| 원본 파일 | 노트북 단계 |
|:---|:---|
| `config.py` | 1단계 |
| `elfParser.py` | 2단계 (`ElfParser`) |
| `setEmulData.py` | 3단계 |
| `make_TC.py` | 4단계 (`make_TC`) |
| `emul.make_disassembly_file` | 5단계 |
| `logger.py` | 6단계 (`TraceLogger`) |
| `scenario.py` | 7단계 (`Scenario`) |
| `emul.init_emulator` / 훅 | 8단계 |
| `emul.run` | 9·11단계 (`run_once` / `run_full`) |
| `main.py` | 9단계 실행 셀 |
| `test_cmp.py` | 12단계 |
""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}

out = "PRE-SCA_재구성.ipynb"
with open(out, "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("notebook written:", out, "cells:", len(cells))
