"""[extra] SCALib 예제 노트북 공용 정의.

Normal AES(tiny-AES-c)와 Masked AES(masked-aes-c) 두 타겟이 같은 AES 상수·
같은 그룹 규약을 쓰고, 데이터셋·POI 경로만 타겟마다 다르다. 그 정의를 노트북에
복사하면 고칠 곳이 폭발하므로 **정의는 여기 한 곳**에 둔다.
(AGENTS.md 원칙 1-2, 원칙 3과의 충돌은 "의미는 반복해도 정의는 반복하지 않는다")

여기 있는 것은 **이 서브프로젝트 고유의 데이터와 규약**뿐이다.
분석 로직은 각 노트북이 직접 보여준다.

## 저장소 공용 정의는 `workspace/lib/` 에 있다

스키마(필드 이름·검증기)와 AES 참조 계산은 이 서브프로젝트만의 것이 아니다.
세 수집 경로(실물 전력·디버그 트레이스·에뮬레이션)가 같은 검증기를 통과하고 같은
중간값을 라벨로 써야 결과를 나란히 놓을 수 있으므로, 그 정의는 저장소 공용 트리에 있다.

    workspace/lib/sca_schema.py   스키마 상수·검증기·경로 기반 로더
    workspace/lib/aes_ref.py      SBOX·HW·중간값 참조 계산

**이 파일이 그것을 그대로 재노출한다.** 그래서 분석 노트북 12개는
`from scalib_common import SBOX, validate_dataset` 처럼 종전과 똑같이 쓰면 된다 —
공용 트리로 옮기면서 노트북을 한 줄도 고치지 않기 위한 장치다. 재노출은 정의를
복제하는 것이 아니라 참조하는 것이므로 "정의는 한 곳" 원칙을 지킨다.

데이터셋의 온디스크 구조는 저장소 루트의 SCHEMA.md 를 따른다. 용어는 GLOSSARY.md 가 정본이다.
"""

import sys
from pathlib import Path

import h5py
import numpy as np

# 공용 트리를 import 경로에 넣는다. 저장소 어디서 실행하든 같은 파일을 집도록
# 이 파일 위치를 기준으로 상대 계산한다 (cwd 에 의존하지 않는다).
_LIB = Path(__file__).resolve().parent.parent / "lib"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

# ── 공용 정의 재노출 (정의는 workspace/lib/ 에 있다) ────────
from sca_schema import (          # noqa: E402
    SCHEMA,
    F_TRACE, F_KEY, F_PLAINTEXT, F_CIPHERTEXT, F_MASK,
    REQUIRED_METADATA_1_0 as REQUIRED_METADATA,
    REQUIRED_SUBSET_METADATA,
    SUBSET_ROLES,
    validate_dataset as _validate_path,
    group_len as _group_len_path,
    load_group as _load_group_path,
)
from aes_ref import SBOX, HW, sbox_out   # noqa: E402

# 이 서브프로젝트의 수집기가 만드는 데이터셋의 판번호.
#
# 공용 스키마 문서는 이미 1.1 이지만, 이 프로젝트의 수집 코드는 1.1 이 요구하는
# 필드(sample_axis·bandwidth_hz·레코드별 exec_time …)를 **기록하지 않는다.**
# 판번호만 올려 적으면 없는 것을 있다고 주장하는 셈이므로 1.0 으로 남긴다.
# 그 값들을 실제로 재게 되면 그때 올린다 — 그때까지는 대조표가 "미기록" 으로 보고한다.
SCHEMA_VERSION = "1.0"

# ── 이 서브프로젝트의 subset 이름 → role ────────────────────
SUBSET_ROLE_MAP = {
    "explore": "exploration",
    "profiling": "profiling",
    "attack": "attack",
    "tvla_fk": "leakage-detection-fixed",
    "tvla_rk": "leakage-detection-random",
}

# ── 경로 루트 ──────────────────────────────────────────────
_ROOT = Path(__file__).parent
TRACES = _ROOT / "traces"
NB_OUTPUT = _ROOT / "nb_output"

# 암호 라이브러리는 이 서브프로젝트 밖 공용 트리에 있다. 펌웨어 makefile 과
# 에뮬레이션 하네스가 같은 파일을 컴파일한다 — workspace/iut/README.md 참고.
IUT_ROOT = _ROOT.parent / "iut"

# ── 타겟 레지스트리 (단일 공급원) ───────────────────────────
# 키 = 라이브러리 디렉터리 이름. 펌웨어·수집 노트북·h5·POI 파일명과 같은 축.
TARGETS = {
    "tiny-AES-c": {
        "label": "Normal AES (tiny-AES-c)",
        "short": "Normal",
        "dataset": TRACES / "scalib_dataset_tiny-AES-c.h5",
        "poi": NB_OUTPUT / "poi_tiny-AES-c.npz",
        "source": IUT_ROOT / "tiny-AES-c",
        "has_masks": False,
        "cipher_attr": "AES-128-ECB (tiny-AES-c)",
    },
    "masked-aes-c": {
        "label": "Masked AES (masked-aes-c)",
        "short": "Masked",
        "dataset": TRACES / "scalib_dataset_masked-aes-c.h5",
        "poi": NB_OUTPUT / "poi_masked-aes-c.npz",
        "source": IUT_ROOT / "masked-aes-c",
        "has_masks": True,
        "cipher_attr": "AES-128-ECB (masked-aes-c, MASKED=1)",
    },
}

TARGET_IDS = tuple(TARGETS.keys())

# 수집 프로토콜 상수 — 0.0 / 0.1 이 같은 시드·장수를 쓰도록 한곳에 둔다.
# 기존 Normal 데이터셋과 같은 입력 벡터를 쓰려면 이 값을 바꾸지 않는다.
#
# N_* 는 **수집 목표치**다. 실제로 파일에 몇 장이 들어 있는지의 정본은 h5 자신이며,
# 분석 노트북은 이 상수가 아니라 group_len() 으로 실보유 장수를 읽는다.
# 수집이 중간에 끊겨 목표에 못 미치는 파일이 있을 수 있기 때문이다.
SEED = 1234
N_EXPLORE = 5000
N_PROFILING = 100000
N_ATTACK = 10000
N_TVLA = 1000
BATCH = 500  # HDF5 스트리밍 배치 크기
AES_BLOCK = 16
MASK_LEN = 10  # mask[0..9]; Masked i_m 한 행


def require_target(target):
    """타겟 id 를 검사하고 TARGETS 항목(dict)을 돌려준다.

    실패 조건: 모르는 id 이면 KeyError. 기본값으로 조용히 한 타겟만 도는
    함정을 막기 위해 호출측이 target 을 반드시 넘기게 한다.
    """
    if target not in TARGETS:
        raise KeyError(
            "알 수 없는 target=%r. 사용 가능: %s" % (target, list(TARGETS)))
    return TARGETS[target]


def open_dataset(target):
    """타겟 데이터셋을 열어 h5py.File 을 돌려준다 (with 문으로 쓴다).

    실패 조건: 파일이 없으면 FileNotFoundError 와 수집 노트북 안내.
    """
    spec = require_target(target)
    p = spec["dataset"]
    if not p.is_file():
        collect = ("0.0.Dataset_Collect_tiny-AES-c.ipynb"
                   if target == "tiny-AES-c"
                   else "0.1.Dataset_Collect_masked-aes-c.ipynb")
        raise FileNotFoundError(
            "데이터셋이 없다: %s\n"
            "먼저 %s 를 실행해 트레이스를 수집한다 "
            "(ChipWhisperer 하드웨어 필요)." % (p, collect))
    return h5py.File(p, "r")


def load_group(group, target, n=None, samples=None):
    """데이터셋의 한 그룹을 메모리로 읽는다.

    입력
        group   : 'explore' | 'profiling' | 'attack' | 'tvla_rk' | 'tvla_fk'
        target  : 'tiny-AES-c' | 'masked-aes-c'  (필수)
        n       : 앞에서 몇 장만. None 이면 전부.
        samples : 샘플 축 슬라이스. POI 구간만 읽을 때.

    출력 (dict)
        k, p, o : (n, 16) uint8
        t       : (n, ns) int16
        m       : (n, 10) uint8 또는 None
                  Masked 데이터셋의 i_m. Normal 이거나 없으면 None.
                  공격자 관점 분석에서는 쓰지 않는다.
        attrs   : dict  파일 단위 측정 조건
        target  : str   호출에 쓴 target id
        label   : str   표시용 이름

    짧은 키(k/p/o/t/m)는 노트북 편의를 위한 것이고 온디스크 이름은 SCHEMA.md 를
    따른다. 둘을 잇는 곳이 여기 한 군데다.

    실패 조건: 그룹 이름이 틀리면 KeyError.
    """
    spec = require_target(target)
    if not spec["dataset"].is_file():
        open_dataset(target)          # 안내 문구를 담은 FileNotFoundError 를 그대로 올린다
    raw = _load_group_path(spec["dataset"], group, n=n, samples=samples)
    return {
        "k": raw[F_KEY],
        "p": raw[F_PLAINTEXT],
        "o": raw.get(F_CIPHERTEXT),
        "t": raw[F_TRACE],
        "m": raw.get(F_MASK),
        "attrs": raw["attrs"],
        "target": target,
        "label": spec["label"],
    }


def group_len(group, target):
    """그룹이 실제로 보유한 트레이스 장수. 파형은 읽지 않는다.

    N_PROFILING 같은 목표치를 노트북에 박으면 목표에 못 미친 데이터셋에서
    조용히 IndexError 나 빈 슬라이스가 난다. "있는 만큼" 을 물어보는 창구다.

    실패 조건: 그룹 이름이 틀리면 KeyError.
    """
    spec = require_target(target)
    if not spec["dataset"].is_file():
        open_dataset(target)
    return _group_len_path(spec["dataset"], group)


def load_poi(target):
    """1.0.SNR 이 저장한 타겟별 POI npz 를 연다.

    출력: np.load 결과 (poi, poi_windows, ...). 파일이 없으면 FileNotFoundError.
    """
    spec = require_target(target)
    p = spec["poi"]
    if not p.is_file():
        raise FileNotFoundError(
            "POI 파일이 없다: %s\n"
            "1.0.SNR.ipynb 를 먼저 실행한다 (target=%s)." % (p, target))
    return np.load(p)


def validate_dataset(target=None, path=None):
    """데이터셋이 SCHEMA.md 를 지키는지 검사하고 위반 목록을 돌려준다.

    입력
        target : 등록된 타겟 id. path 를 주면 무시된다.
        path   : 임의의 h5 경로. 저장소 밖 파일이나 튜토리얼 파형을 검사할 때 쓴다.

    출력
        위반 문자열 리스트. **비어 있으면 준수**다.

    검증 규칙 자체는 workspace/lib/sca_schema.py 에 있다 — 세 수집 경로가 같은
    검증기를 통과해야 "준수" 의 뜻이 하나로 유지되기 때문이다.
    """
    p = path if path is not None else require_target(target)["dataset"]
    return _validate_path(path=p)


def require_schema(target=None, path=None):
    """준수하지 않으면 예외를 던진다. 수집 직후·분석 시작 시 쓴다."""
    bad = validate_dataset(target, path)
    if bad:
        raise RuntimeError(
            "SCHEMA.md 위반 %d건:\n  - %s" % (len(bad), "\n  - ".join(bad)))
    return True


def dataset_summary(target=None):
    """측정 조건과 그룹 구성을 문자열로 돌려준다.

    target 이 None 이면 등록된 모든 타겟을 순서대로 요약한다.
    각 노트북 첫머리에서 '무엇을 분석하는 중인지'를 보여 줄 때 쓴다.
    """
    ids = TARGET_IDS if target is None else (target,)
    blocks = []
    for tid in ids:
        spec = require_target(tid)
        try:
            with open_dataset(tid) as h5:
                lines = ["[%s] %s" % (spec["short"], spec["label"]),
                         "  path         %s" % spec["dataset"]]
                for key in ("schema_version", "acquisition_start",
                            "iut_algorithm", "iut_implementation",
                            "iut_countermeasure", "target_name",
                            "target_clock_hz", "channel_type", "channel_probe",
                            "sample_rate_hz", "sample_resolution_bits",
                            "samples_per_trace", "sample_dtype", "sample_scale",
                            "trigger_semantics", "alignment"):
                    if key in h5.attrs:
                        lines.append("  %-22s %s" % (key, h5.attrs[key]))
                rec = list(h5.attrs.get("recoveries", []))
                if rec:
                    # 수집 중 자동 복구가 있었다는 뜻. 데이터를 의심할 때 첫 단서다.
                    lines.append("  %-22s %s" % (
                        "자동복구",
                        ", ".join(r.decode() if isinstance(r, bytes) else str(r)
                                  for r in rec)))
                problems = validate_dataset(tid)
                lines.append("  %-22s %s" % (
                    "스키마 준수",
                    "예" if not problems else "**부분** (%d건) — validate_dataset() 참고"
                    % len(problems)))
                lines.append("  Subset")
                for name in h5:
                    g = h5[name]
                    extra = ""
                    if F_MASK in g:
                        extra = "  %s%s" % (F_MASK, g[F_MASK].shape)
                    # 결측을 '?' 로 조용히 넘기지 않는다. 빠진 것은 빠졌다고 읽히게 한다.
                    missing = [a for a in ("key_mode", "pt_mode") if a not in g.attrs]
                    mode = ("키=%s 평문=%s" % (g.attrs["key_mode"], g.attrs["pt_mode"])
                            if not missing
                            else "!! attrs 없음: %s" % ", ".join(missing))
                    lines.append(
                        "    /%-10s [%-24s] %6d 장 x %d 샘플   %s%s"
                        % (name, g.attrs.get("role", "role 없음"),
                           g[F_TRACE].shape[0], g[F_TRACE].shape[1], mode, extra))
                blocks.append("\n".join(lines))
        except FileNotFoundError as e:
            blocks.append("[%s] %s\n  (없음) %s" % (
                spec["short"], spec["label"], e))
    return "\n\n".join(blocks)
