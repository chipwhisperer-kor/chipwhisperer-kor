"""에뮬레이션 수집기 — 구현 층의 누설을 명령어 단위로 관측한다.

## 무엇을 왜 만드나

논문이 증명하는 것은 "올바르게 마스킹된 구현에서는 모든 연산의 HW·HD 가 비마스킹
알고리즘의 민감값과 통계적으로 독립" 이라는 명제다. 코딩 과정의 휴먼 에러는 그 고리를
되살린다 — 같은 레지스터에 두 share 를 연달아 쓰면
`HD = HW(share1 ^ share2) = HW(민감값)` 이 되어, **수식은 그대로인데 구현만 새는**
상태가 된다.

이 결함은 실측 파형으로 찾기 어렵다(잡음에 묻히고 명령어 단위로 짚을 수 없다).
에뮬레이션은 정반대 조건을 준다 — **잡음 0, 샘플 하나가 명령어 하나.**
그래서 종속성이 있으면 무조건 보이고, 보이는 즉시 어느 명령어인지 지목할 수 있다.

**이것은 실측의 대용품이 아니다.** HW/HD 모델은 글리치·커플링 같은 물리 효과를 담지
않으므로, 여기서 깨끗해도 실물에서 샐 수 있다. 세 관측은 서로 다른 고리를 본다.

## 누설 벡터

명령어마다 네 성분을 뽑아 **성분별로 연접**한다. 길이 = 4 × L (L = 구간 명령어 수).

    trace = [ hw_reg | hd_reg | hw_mem | hd_mem ]

| 성분 | 정의 | 잡는 것 |
|---|---|---|
| `hw_reg` | 그 명령어가 쓴 레지스터들의 실행 후 값의 HW 합 | 값 자체의 누설 |
| `hd_reg` | **HW(R_before ^ R_after)** — 같은 레지스터의 앞뒤 | 레지스터 전이 누설 |
| `hw_mem` | 그 명령어의 메모리 쓰기 값들의 HW 합 | 메모리 값 누설 |
| `hd_mem` | **HW(old ^ new)** — 같은 주소의 앞뒤 | 메모리 전이 누설 |

**HD 는 같은 저장소의 한 명령어 앞뒤 값끼리만 계산한다.** 서로 다른 레지스터 쌍
(`HD(R2_before, R5_after)`)은 실제 하드웨어에서 전이 누설이 생기는 방식이 아니고,
조합이 폭발해 오탐만 만든다.

메모리 성분을 넣는 이유: tiny-AES 계열은 state 를 메모리 배열에 두고 **in-place 로
갱신**한다. 전이 결함은 레지스터보다 이 state 버퍼에서 더 자주 난다.

## 구현이 기대는 실측 사실 (전부 확인함)

- `UC_HOOK_CODE` 는 명령어 **실행 전**에 걸린다 → 연속한 두 hook 의 같은 레지스터를
  XOR 하면 그 명령어의 전이가 된다. `[extra] PRE-SCA` 의 `logger.py` 도 같은 방식이다.
- `UC_HOOK_MEM_WRITE` 도 **쓰기 전**에 걸린다 → 콜백 안의 `mem_read` 가 이전 값을 준다.
  (`UC_HOOK_MEM_WRITE_AFTER` 는 Unicorn 2.1.4 에 **없다** — 이 방법뿐이다.)
- `capstone` 의 `insn.regs_access()` 가 명령어별 write 레지스터를 준다 → 미리 캐싱해
  hook 에서 17개를 다 읽지 않는다.

## PC 를 레지스터 성분에서 빼는 이유

제어흐름이 데이터 독립이면 PC 는 인덱스마다 상수라 분산이 0 이고 누설 신호가 없다.
데이터 의존이면 그것은 **타이밍 분석(TA)이 잡을 일**이고, 이 벡터에 섞으면 정렬이
무너져 다른 성분까지 오염된다. 그래서 뺀다.
"""

import hashlib
import time

import numpy as np
from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, Cs
from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, UC_MODE_THUMB, Uc
from unicorn.arm_const import (
    UC_ARM_REG_FP, UC_ARM_REG_IP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1,
    UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_SP,
)

from .. import paths
from elfParser import ElfParser                     # noqa: E402  (paths 가 경로를 넣는다)

COMPONENTS = ("hw_reg", "hd_reg", "hw_mem", "hd_mem")

# capstone 레지스터 이름 → unicorn 상수. **pc 는 일부러 넣지 않는다** (위 설명 참고).
REG_MAP = {
    "r0": UC_ARM_REG_R0, "r1": UC_ARM_REG_R1, "r2": UC_ARM_REG_R2, "r3": UC_ARM_REG_R3,
    "r4": UC_ARM_REG_R4, "r5": UC_ARM_REG_R5, "r6": UC_ARM_REG_R6, "r7": UC_ARM_REG_R7,
    "r8": UC_ARM_REG_R8, "r9": UC_ARM_REG_R9, "r10": UC_ARM_REG_R10,
    "fp": UC_ARM_REG_FP, "ip": UC_ARM_REG_IP, "sp": UC_ARM_REG_SP, "lr": UC_ARM_REG_LR,
}

# 32비트 값의 HW 를 바이트 단위로 더해 얻는다 (파이썬 int.bit_count 보다 빠르지 않지만
# 배열 연산에 쓰기 좋다). 아래 hook 은 int.bit_count() 를 직접 쓴다 — Python 3.10+.
_PAGE = 0x1000
_STOP_ADDR = 0x7000          # 반환 주소로 쓸 미사용 페이지 (.text 0x8000 아래)
_LOW_BASE, _LOW_SIZE = 0x0000, 0x1000
_CODE_BASE, _CODE_SIZE = 0x8000, 0x8000
_STACK_BASE, _STACK_SIZE = 0x7F000, 0x2000
# 하네스가 실제로 쓰는 출력 바이트 수: 암호문 16 + 마스크 10 (main.c 규약).
_VIR_OUT_USED = 26


class EmulationTarget:
    """ELF 하나를 열어 두고 입력을 바꿔 가며 반복 실행한다.

    ELF 파싱·디스어셈블은 생성자에서 한 번만 한다. 트레이스마다 다시 하면
    수천 장 수집이 불가능해진다.

    실패 조건
        ELF 가 없으면 FileNotFoundError (빌드 방법을 알려 준다).
        필요한 심볼이 없으면 elfParser 가 종료시킨다.
    """

    def __init__(self, iut_name, window=None, components=COMPONENTS):
        self.iut = iut_name
        self.path = paths.harness_elf(iut_name)
        self.components = tuple(components)
        for c in self.components:
            if c not in COMPONENTS:
                raise ValueError("모르는 성분 %r (사용 가능 %s)" % (c, list(COMPONENTS)))

        e = ElfParser(str(self.path))
        self.elf = e
        self.mode = e.check_mode()                       # 2 = Thumb
        self.sections = e.check_list(e.section_data_list()[0])
        self.stack = e.get_stack_addr()
        self.main = e.get_func_address("main") & ~1
        self.vir_in, self.vir_out = e.get_io_addr_data()
        # 하네스 규약(main.c)이 요구하는 최소 크기. 심볼이 그보다 작으면 규약이 어긋난
        # ELF 를 읽고 있다는 뜻이므로 조용히 잘못된 값을 회수하기 전에 멈춘다.
        self.vir_in_len = e.get_symbol_len("vir_IN")
        self.vir_out_len = e.get_symbol_len("vir_OUT")
        if self.vir_in_len < 36 or self.vir_out_len < 26:
            raise RuntimeError(
                "하네스 버퍼가 규약보다 작다: vir_IN=%d(≥36), vir_OUT=%d(≥26). "
                "emul_harness/main.c 의 입출력 규약과 ELF 가 어긋난다."
                % (self.vir_in_len, self.vir_out_len))

        w = window or {"from_symbol": "AES_init_ctx", "to_symbol": "AES_ECB_encrypt"}
        self.win_from = e.get_func_address(w["from_symbol"]) & ~1
        # 구간의 끝. to_symbol 이 **복귀**하는 지점에서 관측을 닫는다 —
        # 진입 시점의 LR 이 호출자로 돌아갈 주소이므로 기록기가 그것을 기억한다.
        # 이것이 없으면 관측이 main 끝까지 이어져, 마스킹 타겟에서는
        # AES_get_last_masks() 가 비밀인 마스크를 트레이스 안으로 끌고 들어온다.
        self.win_to = e.get_func_address(w["to_symbol"]) & ~1
        self.win_to_sym = w["to_symbol"]
        self.window = w

        with open(self.path, "rb") as f:
            self.sha256 = hashlib.sha256(f.read()).hexdigest()

        self._image = self._read_image()
        self.wr_cache = self._build_write_reg_cache()

        # 관측 구간의 명령어 수. 첫 실행에서 정하고 이후 모든 트레이스가 같아야 한다.
        self.n_instr = None
        self.addr_seq = None

    # ── 준비 ────────────────────────────────────────────────
    def _read_image(self):
        """섹션을 (va, bytes) 목록으로 읽어 둔다. 트레이스마다 파일을 다시 열지 않는다."""
        out = []
        with open(self.path, "rb") as f:
            for va, off, size, name in self.sections:
                if va == 0 or size == 0 or name == ".bss":
                    continue
                f.seek(off)
                out.append((va, f.read(size)))
        return out

    def _build_write_reg_cache(self):
        """주소 → 그 명령어가 쓰는 레지스터의 unicorn 상수 목록.

        hook 에서 매번 디스어셈블하거나 17개 레지스터를 다 읽는 대신 이 표를 본다.
        """
        md = Cs(CS_ARCH_ARM, CS_MODE_THUMB if self.mode == 2 else CS_MODE_ARM)
        md.detail = True
        cache = {}
        for va, off, size, name in self.sections:
            if name != ".text" or va == 0:
                continue
            with open(self.path, "rb") as f:
                f.seek(off)
                blob = f.read(size)
            for insn in md.disasm(blob, va):
                try:
                    _, wr = insn.regs_access()
                except Exception:
                    wr = []
                regs = [REG_MAP[insn.reg_name(r)] for r in wr
                        if insn.reg_name(r) in REG_MAP]
                cache[insn.address] = tuple(regs)
        return cache

    def _new_uc(self):
        uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB if self.mode == 2 else UC_MODE_ARM)
        uc.mem_map(_LOW_BASE, _LOW_SIZE)
        uc.mem_map(_STOP_ADDR, _PAGE)
        uc.mem_map(_CODE_BASE, _CODE_SIZE)
        uc.mem_map(_STACK_BASE, _STACK_SIZE)
        for va, blob in self._image:
            uc.mem_write(va, blob)
        uc.reg_write(UC_ARM_REG_SP, self.stack)
        uc.reg_write(UC_ARM_REG_LR, _STOP_ADDR | 1)
        return uc

    # ── 실행 ────────────────────────────────────────────────
    def run(self, key, plaintext, seed=0, trace=True):
        """한 번 암호화하고 (암호문, 마스크, 트레이스, 실행시간) 을 돌려준다.

        입력
            key, plaintext : 16바이트
            seed           : 마스크 난수 시드 (Masked 빌드만 쓴다)
            trace          : False 면 누설을 모으지 않고 명령어만 센다 (TA·검증용, 빠름)

        출력
            ct        : bytes(16)
            masks     : bytes(10) 또는 None
            trace_arr : int16 (4L,) 또는 None
            exec_time : int — 관측 구간의 명령어 수

        실패 조건
            구간 명령어 수가 첫 실행과 다르면 RuntimeError.
            **조용히 자르지 않는다** — 자르면 sample_map 이 어긋나 엉뚱한 명령어를
            결함으로 지목하게 되고, 이 도구에서 가장 나쁜 실패 모드다.
        """
        uc = self._new_uc()
        uc.mem_write(self.vir_in,
                     bytes(key) + bytes(plaintext) + int(seed).to_bytes(4, "little"))

        if trace:
            rec = _TraceRecorder(self, uc)
        else:
            rec = _CountRecorder(self)
        rec.attach(uc)
        uc.emu_start(self.main | 1, _STOP_ADDR)
        rec.finish(uc)

        raw = bytes(uc.mem_read(self.vir_out, _VIR_OUT_USED))
        ct = raw[:16]
        masks = raw[16:26] if _has_masks(self.iut) else None

        if self.n_instr is None:
            self.n_instr = rec.n
            self.addr_seq = np.asarray(rec.addrs, dtype=np.uint32) if trace else None
        elif rec.n != self.n_instr:
            raise RuntimeError(
                "관측 구간 명령어 수가 달라졌다: 처음 %d → 이번 %d.\n"
                "  제어흐름이 데이터에 의존한다는 뜻이며, 그 자체가 타이밍 누설 소견이다.\n"
                "  다만 sample_map(샘플↔명령어 대응)이 무너지므로 누설 검정은 진행할 수 없다.\n"
                "  타이밍 분석(ta)은 exec_time 만 쓰므로 그대로 유효하다."
                % (self.n_instr, rec.n))
        if trace and self.addr_seq is None:
            self.addr_seq = np.asarray(rec.addrs, dtype=np.uint32)

        return ct, masks, (rec.vector(self.components) if trace else None), rec.n

    # ── 메타데이터 ──────────────────────────────────────────
    def leakage_segments(self):
        """성분별 샘플 구간. `[("hw_reg", 0, L), ("hd_reg", L, 2L), …]`"""
        if self.n_instr is None:
            raise RuntimeError("먼저 한 번 실행해야 구간 길이를 안다.")
        out, off = [], 0
        for c in self.components:
            out.append((c, off, off + self.n_instr))
            off += self.n_instr
        return out

    def sample_map(self):
        """(ns, 3) uint32 — (segment_id, instruction_index, address).

        누설이 검출된 샘플을 명령어로 되짚는 유일한 수단이다. 이것이 없으면
        "샌다" 까지만 말할 수 있고 "여기서 샌다" 를 말할 수 없다.
        """
        if self.addr_seq is None:
            raise RuntimeError("먼저 trace=True 로 한 번 실행해야 한다.")
        L = self.n_instr
        idx = np.arange(L, dtype=np.uint32)
        blocks = []
        for seg_id in range(len(self.components)):
            blocks.append(np.stack([np.full(L, seg_id, dtype=np.uint32),
                                    idx, self.addr_seq], axis=1))
        return np.concatenate(blocks, axis=0)

    def build_flags(self):
        """이 ELF 를 만든 실제 컴파일 플래그를 **make 에게 물어** 가져온다.

        Makefile 을 텍스트로 파싱하지 않는다. 조건부 블록(`ifeq (MASKED)`)까지 긁어
        비마스킹 빌드에 `-DMASKED=1` 이 있다고 기록하는 버그가 실제로 있었다.
        **거짓 메타데이터는 없는 것보다 나쁘다** — 다음 사람이 그 값을 믿고 재현을
        시도하면 다른 바이너리가 나온다.

        실패 조건: make 를 부를 수 없으면 RuntimeError. 지어낸 값으로 대체하지 않는다.
        """
        import subprocess
        r = subprocess.run(["make", "-s", "IUT=%s" % self.iut, "flags"],
                           cwd=str(paths.HARNESS), capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(
                "build_flags 를 확인할 수 없다 (make -s IUT=%s flags → rc=%d).\n%s\n"
                "추정치로 채우지 않는다 — 재현의 고정점이기 때문이다."
                % (self.iut, r.returncode, r.stderr.strip()))
        return " ".join(r.stdout.split())

    def metadata(self):
        """SCHEMA.md §3.9 가 요구하는 에뮬레이션 Metadata."""
        import unicorn
        model = "concat(%s)" % ", ".join(
            {"hw_reg": "HW(reg)", "hd_reg": "HD(reg,same)",
             "hw_mem": "HW(mem)", "hd_mem": "HD(mem,same)"}[c] for c in self.components)
        # 관측 구간 안의 주요 심볼 주소. 분석기가 이것으로 구간 경계(예: 키 스케줄이
        # 끝나고 암호화가 시작되는 명령어 인덱스)를 sample_map 에서 찾는다.
        # 데이터셋만으로 경계를 알 수 있어야 분석이 ELF 에 의존하지 않는다.
        syms = {}
        for s in (self.window["from_symbol"], self.window["to_symbol"]):
            try:
                syms[s] = self.elf.get_func_address(s) & ~1
            except SystemExit:
                continue
        return {
            "leakage_model": model,
            "leakage_segments": ",".join("%s:%d-%d" % s for s in self.leakage_segments()),
            "emulator": "unicorn %s" % unicorn.__version__,
            "instruction_set": "ARMv7-M Thumb" if self.mode == 2 else "ARMv7 ARM",
            "build_flags": self.build_flags(),
            "binary_sha256": self.sha256,
            "window_symbols": ",".join("%s:0x%x" % (k, v) for k, v in syms.items()),
        }


def _has_masks(iut_name):
    """이 IUT 가 마스크를 export 하는가. 이름이 아니라 규약으로 정한다."""
    return iut_name == "masked-aes-c"


# ─────────────────────────────────────────────────────────────
# 기록기
# ─────────────────────────────────────────────────────────────
class _CountRecorder:
    """명령어만 센다. 타이밍 분석과 자가검사에 쓰며 누설을 모으지 않아 빠르다."""

    def __init__(self, tgt):
        self.win_from = tgt.win_from
        self.win_to = tgt.win_to
        self.n = 0
        self.addrs = None
        self._in = False
        self._ret = None

    def attach(self, uc):
        uc.hook_add(UC_HOOK_CODE, self._on_code)

    def _on_code(self, uc, address, size, ud):
        if address == self.win_from:
            self._in = True
        if address == self.win_to and self._ret is None:
            self._ret = uc.reg_read(UC_ARM_REG_LR) & ~1
        if self._in and self._ret is not None and address == self._ret:
            self._in = False
            return
        if self._in:
            self.n += 1

    def finish(self, uc):
        pass

    def vector(self, components):
        return None


class _TraceRecorder:
    """네 성분을 모은다.

    `UC_HOOK_CODE` 가 실행 **전**에 걸리므로 한 스텝 지연이 필요하다.
    hook i 에서 (a) 직전 명령어가 쓴 레지스터를 지금 읽어 '실행 후' 값을 확정하고,
    (b) 이번 명령어가 쓸 레지스터의 현재 값을 '실행 전' 으로 저장한다.
    """

    def __init__(self, tgt, uc):
        self.win_from = tgt.win_from
        self.win_to = tgt.win_to
        self._ret = None
        self.wr_cache = tgt.wr_cache
        self.n = 0
        self.addrs = []
        self.hw_reg, self.hd_reg = [], []
        self.hw_mem, self.hd_mem = [], []
        self._in = False
        self._pending = None          # (regs, before_values)

    def attach(self, uc):
        uc.hook_add(UC_HOOK_CODE, self._on_code)
        uc.hook_add(UC_HOOK_MEM_WRITE, self._on_write)

    def _flush_pending(self, uc):
        regs, before = self._pending
        hw = hd = 0
        for r, b in zip(regs, before):
            a = uc.reg_read(r)
            hw += a.bit_count()
            hd += (a ^ b).bit_count()
        self.hw_reg[-1] = hw
        self.hd_reg[-1] = hd
        self._pending = None

    def _on_code(self, uc, address, size, ud):
        if address == self.win_from:
            self._in = True
        # 구간의 끝 — to_symbol 이 **복귀**하는 지점에서 닫는다.
        # 진입 시점의 LR 이 곧 호출자(main)로 돌아갈 주소이므로 그것을 기억해 둔다.
        if address == self.win_to and self._ret is None:
            self._ret = uc.reg_read(UC_ARM_REG_LR) & ~1
        if self._in and self._ret is not None and address == self._ret:
            if self._pending is not None:
                self._flush_pending(uc)     # 마지막 명령어의 '실행 후' 값을 확정한다
            self._in = False
            return
        if not self._in:
            return
        if self._pending is not None:
            self._flush_pending(uc)

        self.addrs.append(address)
        self.hw_reg.append(0)
        self.hd_reg.append(0)
        self.hw_mem.append(0)
        self.hd_mem.append(0)
        self.n += 1

        regs = self.wr_cache.get(address, ())
        if regs:
            self._pending = (regs, [uc.reg_read(r) for r in regs])

    def _on_write(self, uc, access, address, size, value, ud):
        if not self._in or not self.hw_mem:
            return
        # 콜백은 쓰기 **전**에 걸리므로 mem_read 가 이전 값을 준다 (실측 확인).
        old = int.from_bytes(uc.mem_read(address, size), "little")
        new = value & ((1 << (8 * size)) - 1)
        self.hw_mem[-1] += new.bit_count()
        self.hd_mem[-1] += (old ^ new).bit_count()

    def finish(self, uc):
        # 마지막 명령어의 '실행 후' 값은 에뮬레이션이 끝난 뒤에 읽는다.
        if self._pending is not None:
            self._flush_pending(uc)

    def vector(self, components):
        parts = {"hw_reg": self.hw_reg, "hd_reg": self.hd_reg,
                 "hw_mem": self.hw_mem, "hd_mem": self.hd_mem}
        return np.concatenate([np.asarray(parts[c], dtype=np.int16) for c in components])


# ─────────────────────────────────────────────────────────────
# 자가검사 — 계획의 PoC 게이트를 언제든 다시 돌릴 수 있게 남긴다
# ─────────────────────────────────────────────────────────────
def selftest(iut_name, n=10, seed=1234):
    """골든 AES·마스크·명령어 수·속도를 확인하고 결과 dict 를 돌려준다.

    수집 전에 이것부터 통과해야 한다. 골든이 어긋나면 에뮬레이션 환경이 잘못된
    것이고, 명령어 수가 변동하면 sample_map 이 성립하지 않는다.
    """
    from aes_ref import aes_ecb_encrypt

    tgt = EmulationTarget(iut_name)
    rng = np.random.RandomState(seed)
    bad, masks, counts = 0, [], []
    t0 = time.time()
    for _ in range(n):
        k = bytes(rng.randint(0, 256, 16, dtype=np.uint8))
        p = bytes(rng.randint(0, 256, 16, dtype=np.uint8))
        sd = int(rng.randint(0, 2 ** 31))
        ct, m, tr, et = tgt.run(k, p, sd, trace=True)
        if ct != aes_ecb_encrypt(k, p):
            bad += 1
        if m is not None:
            masks.append(bytes(m))
        counts.append(et)
    dt = (time.time() - t0) / n

    return {
        "iut": iut_name,
        "elf": str(tgt.path),
        "sha256": tgt.sha256,
        "golden_ok": bad == 0,
        "golden_fail": bad,
        "n": n,
        "masks_len": (len(masks[0]) if masks else 0),
        "masks_unique": (len(set(masks)) if masks else None),
        "instr_min": int(min(counts)),
        "instr_max": int(max(counts)),
        "instr_fixed": min(counts) == max(counts),
        "seconds_per_trace": dt,
        "samples_per_trace": len(tgt.components) * tgt.n_instr,
        "metadata": tgt.metadata(),
    }


def _cli():
    import argparse
    import json

    ap = argparse.ArgumentParser(description="에뮬레이션 수집기 자가검사")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--iut", default=None, help="생략하면 workspace/iut/ 전부")
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()

    names = [a.iut] if a.iut else sorted(p.name for p in paths.IUT.iterdir() if p.is_dir())
    out = []
    for name in names:
        try:
            r = selftest(name, n=a.n)
        except FileNotFoundError as e:
            print("[건너뜀] %s — %s" % (name, e))
            continue
        out.append(r)
        print("=" * 66)
        print(" %s   sha256 %s…" % (r["iut"], r["sha256"][:12]))
        print("=" * 66)
        print("  ① 골든 AES 일치   : %s (%d/%d)"
              % ("예" if r["golden_ok"] else "**아니오**", r["n"] - r["golden_fail"], r["n"]))
        print("  ② 마스크          : %s"
              % ("해당없음" if not r["masks_len"]
                 else "%d바이트, 고유 %d/%d" % (r["masks_len"], r["masks_unique"], r["n"])))
        print("  ③ 명령어 수       : %d–%d → %s"
              % (r["instr_min"], r["instr_max"], "고정" if r["instr_fixed"] else "**변동**"))
        print("  ④ 1장당 시간      : %.1f ms (%.0f tr/s)"
              % (r["seconds_per_trace"] * 1000, 1 / r["seconds_per_trace"]))
        print("  ⑤ 샘플/트레이스   : %d" % r["samples_per_trace"])
        print("     leakage_model  : %s" % r["metadata"]["leakage_model"])
        print("     build_flags    : %s" % r["metadata"]["build_flags"])
    ok = all(r["golden_ok"] and r["instr_fixed"] for r in out)
    print(json.dumps({"selftest_ok": ok, "results": [
        {k: v for k, v in r.items() if k != "metadata"} for r in out]},
        ensure_ascii=False))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    _cli()
