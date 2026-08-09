"""[extra] SCALib 예제 노트북 공용 정의.

Normal AES(tiny-AES-c)와 Masked AES(masked-aes-c) 두 타겟이 같은 AES 상수·
같은 그룹 규약을 쓰고, 데이터셋·POI 경로만 타겟마다 다르다. 그 정의를 노트북에
복사하면 고칠 곳이 폭발하므로 **정의는 여기 한 곳**에 둔다.
(AGENTS.md 원칙 1-2, 원칙 3과의 충돌은 "의미는 반복해도 정의는 반복하지 않는다")

여기 있는 것은 **데이터와 규약**뿐이다. 분석 로직은 각 노트북이 직접 보여준다.

데이터셋의 온디스크 구조는 저장소 루트의 SCHEMA.md 를 따른다. 용어는 GLOSSARY.md 가 정본이다.
필드 이름을 여기 상수로 두는 이유는, 스키마가 바뀌었을 때 고칠 곳이 이 파일 하나가 되게
하기 위함이다 — 노트북은 load_group() 이 돌려주는 dict 키만 알면 된다.
"""

from pathlib import Path

import h5py
import numpy as np

# ── 스키마 (SCHEMA.md) ──────────────────────────────────────
SCHEMA = "sca-hdf5"
SCHEMA_VERSION = "1.0"

# Attributes(OPTIMIST) = HDF5 배열 이름. GLOSSARY.md §6.1 의 용어 충돌에 주의한다.
F_TRACE = "trace"
F_KEY = "key"
F_PLAINTEXT = "plaintext"
F_CIPHERTEXT = "ciphertext"
F_MASK = "mask"

# 루트 Metadata 중 필수 (SCHEMA.md §3)
REQUIRED_METADATA = (
    "schema", "schema_version",
    "target_name", "target_device", "target_clock_hz",
    "iut_algorithm", "iut_implementation", "iut_countermeasure",
    "channel_type", "channel_probe",
    "sample_rate_hz", "sample_resolution_bits", "samples_per_trace",
    "sample_dtype", "sample_scale",
    "trigger_source", "trigger_semantics",
    "alignment",
    "acquisition_start", "tool_chain",
)

# Subset Metadata 중 필수 (SCHEMA.md §4)
REQUIRED_SUBSET_METADATA = ("role", "n_records", "key_mode", "pt_mode")

# 허용되는 subset role (SCHEMA.md §4.1)
SUBSET_ROLES = (
    "exploration", "profiling", "attack",
    "leakage-detection-fixed", "leakage-detection-random",
)

# 이 서브프로젝트의 subset 이름 → role
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

# ── 타겟 레지스트리 (단일 공급원) ───────────────────────────
# 키 = 라이브러리 디렉터리 이름. 펌웨어·수집 노트북·h5·POI 파일명과 같은 축.
TARGETS = {
    "tiny-AES-c": {
        "label": "Normal AES (tiny-AES-c)",
        "short": "Normal",
        "dataset": TRACES / "scalib_dataset_tiny-AES-c.h5",
        "poi": NB_OUTPUT / "poi_tiny-AES-c.npz",
        "has_masks": False,
        "cipher_attr": "AES-128-ECB (tiny-AES-c)",
    },
    "masked-aes-c": {
        "label": "Masked AES (masked-aes-c)",
        "short": "Masked",
        "dataset": TRACES / "scalib_dataset_masked-aes-c.h5",
        "poi": NB_OUTPUT / "poi_masked-aes-c.npz",
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

# ── AES-128 상수 ────────────────────────────────────────────
# SubBytes 치환표. 양 타겟 펌웨어가 쓰는 것과 같은 표준 S-box 다.
SBOX = np.array([
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
], dtype=np.uint8)

# 해밍 가중치표. HW[v] = v 의 1비트 개수. 전력 누설 모델의 기본형이다.
HW = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)


def require_target(target):
    """타겟 id 를 검사하고 TARGETS 항목(dict)을 돌려준다.

    실패 조건: 모르는 id 이면 KeyError. 기본값으로 조용히 한 타겟만 도는
    함정을 막기 위해 호출측이 target 을 반드시 넘기게 한다.
    """
    if target not in TARGETS:
        raise KeyError(
            "알 수 없는 target=%r. 사용 가능: %s" % (target, list(TARGETS)))
    return TARGETS[target]


def sbox_out(plaintext, key):
    """1라운드 SBox 출력 = SBOX[plaintext XOR key].

    입력: 각각 (n, 16) 또는 (16,) uint8 배열. 브로드캐스트된다.
    출력: 입력과 같은 shape 의 uint8 배열.

    부채널 공격이 겨냥하는 가장 흔한 중간값이다. 평문 한 바이트와 키 한 바이트에만
    의존하므로, 키를 바이트 단위로 나누어 추측할 수 있다(분할 정복).
    Masked 구현에서도 **공격자 관점** 라벨은 이 값이다(마스크는 모른다).
    """
    return SBOX[np.bitwise_xor(np.asarray(plaintext, dtype=np.uint8),
                               np.asarray(key, dtype=np.uint8))]


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

    실패 조건: 그룹 이름이 틀리면 KeyError.
    """
    spec = require_target(target)
    with open_dataset(target) as h5:
        if group not in h5:
            raise KeyError("그룹 '%s' 가 없다. 사용 가능: %s" % (group, list(h5)))
        g = h5[group]
        sl = slice(None) if n is None else slice(0, n)
        ssl = samples if samples is not None else slice(None)
        # 반환 dict 의 짧은 키(k/p/o/t/m)는 노트북 편의를 위한 것이고,
        # 온디스크 이름은 SCHEMA.md 를 따른다. 둘을 잇는 곳이 여기 한 군데다.
        out = {
            "k": g[F_KEY][sl],
            "p": g[F_PLAINTEXT][sl],
            "o": g[F_CIPHERTEXT][sl],
            "t": g[F_TRACE][sl, ssl],
            "m": None,
            "attrs": {key: h5.attrs[key] for key in h5.attrs},
            "target": target,
            "label": spec["label"],
        }
        if F_MASK in g:
            out["m"] = g[F_MASK][sl]
        return out


def group_len(group, target):
    """그룹이 실제로 보유한 트레이스 장수. 파형은 읽지 않는다.

    N_PROFILING 같은 목표치를 노트북에 박으면 Masked 처럼 목표에 못 미친 데이터셋에서
    조용히 IndexError 나 빈 슬라이스가 난다. "있는 만큼" 을 물어보는 창구다.

    실패 조건: 그룹 이름이 틀리면 KeyError.
    """
    require_target(target)
    with open_dataset(target) as h5:
        if group not in h5:
            raise KeyError("그룹 '%s' 가 없다. 사용 가능: %s" % (group, list(h5)))
        return int(h5[group][F_TRACE].shape[0])


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

    왜 예외가 아니라 목록인가: 위반이 여러 개일 때 첫 번째만 보고 고치면 다음 것이
    또 나온다. 한 번에 다 보여 주는 편이 고치기 쉽다. 그리고 "부분 준수" 를 오류로
    취급하면 튜토리얼 파형처럼 복원 불가능한 파일을 아예 못 쓰게 된다(SCHEMA.md §5.3).
    """
    p = Path(path) if path is not None else require_target(target)["dataset"]
    if not Path(p).is_file():
        return ["파일이 없다: %s" % p]

    bad = []
    with h5py.File(p, "r") as h5:
        a = h5.attrs
        if a.get("schema") != SCHEMA:
            bad.append("루트 attrs: schema 가 %r 이어야 한다 (현재 %r)"
                       % (SCHEMA, a.get("schema")))
        for key in REQUIRED_METADATA:
            if key not in a:
                bad.append("루트 attrs 누락: %s" % key)

        subsets = [n for n in h5 if isinstance(h5[n], h5py.Group)]
        if not subsets:
            bad.append("subset 그룹이 하나도 없다")

        for name in subsets:
            g = h5[name]
            for key in REQUIRED_SUBSET_METADATA:
                if key not in g.attrs:
                    bad.append("/%s attrs 누락: %s" % (name, key))
            role = g.attrs.get("role")
            if role is not None and role not in SUBSET_ROLES:
                bad.append("/%s role 이 허용 목록 밖: %r" % (name, role))

            for field in (F_TRACE, F_KEY, F_PLAINTEXT):
                if field not in g:
                    bad.append("/%s 필수 배열 누락: %s" % (name, field))
            if F_TRACE not in g:
                continue

            # 행 정렬 — 이 규칙이 깨지면 레코드 대응이 무너져 데이터셋 전체가 무효다.
            rows = {f: g[f].shape[0] for f in g}
            if len(set(rows.values())) != 1:
                bad.append("/%s 행 수 불일치: %s" % (name, rows))
            n_rec = g.attrs.get("n_records")
            if n_rec is not None and int(n_rec) != g[F_TRACE].shape[0]:
                bad.append("/%s n_records=%s 인데 trace 는 %d 행"
                           % (name, n_rec, g[F_TRACE].shape[0]))

            # 루트 Metadata 와 실제 배열이 어긋나면 둘 중 하나가 거짓말이다.
            if "samples_per_trace" in a and \
                    int(a["samples_per_trace"]) != g[F_TRACE].shape[1]:
                bad.append("/%s trace 열 수 %d ≠ samples_per_trace %s"
                           % (name, g[F_TRACE].shape[1], a["samples_per_trace"]))
            if "sample_dtype" in a and str(a["sample_dtype"]) != str(g[F_TRACE].dtype):
                bad.append("/%s trace dtype %s ≠ sample_dtype %s"
                           % (name, g[F_TRACE].dtype, a["sample_dtype"]))
            if np.issubdtype(g[F_TRACE].dtype, np.integer) and "sample_scale" not in a:
                bad.append("/%s trace 가 정수형인데 sample_scale 이 없다 (SCHEMA.md §5.2)"
                           % name)
    return bad


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
