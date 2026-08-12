"""부채널 데이터셋 스키마 — 상수·검증기·경로 기반 로더. 저장소 공용.

온디스크 규격의 정본은 저장소 루트의 `SCHEMA.md` 이고, 용어는 `GLOSSARY.md` 다.
이 파일은 그 문서를 **코드로 옮긴 것**이며, 필드 이름을 여기 한 곳에만 두어
스키마가 바뀌었을 때 고칠 곳이 하나가 되게 한다.

왜 프로젝트 밖에 있는가
    세 수집 경로(실물 전력·디버그 트레이스·에뮬레이션)가 **같은 검증기**를 통과해야
    하나의 분석기가 셋을 다 받을 수 있다. 검증기가 프로젝트마다 따로 있으면
    "준수"의 뜻이 프로젝트마다 달라진다.

여기 있는 것은 하드웨어 제어가 없는 스키마 검사와 읽기 전용 HDF5 로더다. Dataset 파일을
읽지만 수정하지 않으며, 파일 생성과 수집은 각 수집기의 책임이다.

판번호
    현재 문서 판번호는 SCHEMA_VERSION = "1.1" 이다.
    **1.0 파일은 1.0 규칙으로, 1.1 파일은 1.1 규칙으로 검사한다.** 1.1 은 필드를
    더하기만 했으므로 기존 1.0 데이터셋은 그대로 유효하다 — 나중에 만든 규칙으로
    옛 파일을 소급 위반 처리하면 "부분 준수"의 뜻이 무너진다.
"""

from pathlib import Path

import h5py
import numpy as np

# ── 스키마 식별 ────────────────────────────────────────────
SCHEMA = "sca-hdf5"
SCHEMA_VERSION = "1.1"
KNOWN_VERSIONS = ("1.0", "1.1")

# ── Attributes(OPTIMIST) = HDF5 배열 이름 ──────────────────
# GLOSSARY.md §6.1 의 용어 충돌에 주의한다: OPTIMIST 의 Attributes 는 HDF5 배열로,
# OPTIMIST 의 Metadata 는 HDF5 attrs 로 저장되어 이름이 서로 엇갈린다.
F_TRACE = "trace"
F_KEY = "key"
F_PLAINTEXT = "plaintext"
F_CIPHERTEXT = "ciphertext"
F_MASK = "mask"
F_EXEC_TIME = "exec_time"          # 1.1 신설 — 레코드별 실행시간 (타이밍 분석 입력)
F_SAMPLE_MAP = "sample_map"        # 1.1 신설 — 루트 배열 (샘플 → 명령어 역매핑)

# ── 루트 Metadata(메타데이터) (SCHEMA.md §3) ────────────────────────
# 1.0 의 필수 목록. 1.1 도 이 항목을 그대로 요구한다.
REQUIRED_METADATA_1_0 = (
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

# 1.1 에서 축과 무관하게 요구하는 것 (= 1.0 필수에서 시간축 전용 두 개를 뺀 것)
REQUIRED_METADATA_1_1 = tuple(
    f for f in REQUIRED_METADATA_1_0
    if f not in ("sample_rate_hz", "sample_resolution_bits")
) + ("sample_axis",)

# 시간축일 때만 의미가 있는 필드. 에뮬레이션 트레이스에는 존재하지 않으므로
# 필수에서 뺀다 — 없는 값을 지어내지 않기 위한 분기다 (SCHEMA.md §5.3).
REQUIRED_METADATA_TIME_AXIS = ("sample_rate_hz", "sample_resolution_bits")

# 에뮬레이션 트레이스 전용. 값이 모델의 출력이므로 모델을 모르면 해석할 수 없다.
REQUIRED_METADATA_EMULATED = (
    "leakage_model", "leakage_segments",
    "emulator", "instruction_set", "build_flags", "binary_sha256",
)

# 전력 채널의 측정 장비 요건 판정에 필요한 값 (ISO/IEC 17825 Annex B).
# 1.1 에서 선택 → 필수로 올렸다. 없으면 대역폭 요건을 **판정할 수 없다**.
REQUIRED_METADATA_POWER_1_1 = ("bandwidth_hz",)

# ── Subset metadata(서브셋 메타데이터) (SCHEMA.md §4) ─────────────────
REQUIRED_SUBSET_METADATA = ("role", "n_records", "key_mode", "pt_mode")

SUBSET_ROLES = (
    "exploration", "profiling", "attack",
    "leakage-detection-fixed", "leakage-detection-random",
    "timing",                       # 1.1 신설 — ISO/IEC 17825 A.2.4 타이밍 측정 블록
    "simple-analysis",              # 1.1 신설 — A.2.2 SPA 파형쌍
)

CHANNEL_TYPES = ("power", "em", "emulated-power", "debug-trace")
SAMPLE_AXES = ("time", "instruction")
EXEC_TIME_UNITS = ("instruction", "adc_sample", "trace_tick")


# ─────────────────────────────────────────────────────────────
# 검증
# ─────────────────────────────────────────────────────────────
def validate_dataset(path=None):
    """데이터셋이 `SCHEMA.md` 를 지키는지 검사하고 위반 목록을 돌려준다.

    입력
        path : h5 파일 경로.

    출력
        위반 문자열 리스트. **비어 있으면 준수**다.

    왜 예외가 아니라 목록인가: 위반이 여러 개일 때 첫 번째만 보고 고치면 다음 것이
    또 나온다. 한 번에 다 보여 주는 편이 고치기 쉽다. 그리고 "부분 준수" 를 오류로
    취급하면 복원 불가능한 옛 파일을 아예 못 쓰게 된다 (SCHEMA.md §5.3).

    파일에 적힌 `schema_version` 에 따라 규칙이 갈린다. 모르는 판번호면 그 사실만
    보고하고 1.0 규칙으로 검사한다 — 미래 파일을 무조건 위반 처리하지 않기 위함이다.
    """
    if path is None:
        raise ValueError("path 를 넘겨야 한다.")
    p = Path(path)
    if not p.is_file():
        return ["파일이 없다: %s" % p]

    bad = []
    with h5py.File(p, "r") as h5:
        a = h5.attrs
        if a.get("schema") != SCHEMA:
            bad.append("루트 attrs: schema 가 %r 이어야 한다 (현재 %r)"
                       % (SCHEMA, a.get("schema")))

        ver = str(a.get("schema_version", "1.0"))
        if ver not in KNOWN_VERSIONS:
            bad.append("모르는 schema_version %r — 1.0 규칙으로 검사했다" % ver)
            ver = "1.0"

        bad += _check_root_metadata(a, ver)
        bad += _check_sample_map(h5, a, ver)

        subsets = [n for n in h5 if isinstance(h5[n], h5py.Group)]
        if not subsets:
            bad.append("subset 그룹이 하나도 없다")
        for name in subsets:
            bad += _check_subset(h5, name, a)
    return bad


def _check_root_metadata(a, ver):
    """루트 HDF5 attrs를 판번호별 Metadata 규칙과 대조해 위반 목록을 반환한다.

    ``a``는 h5py attrs 매핑이고 ``ver``는 알려진 판번호여야 한다. 채널·축별 조건부
    필드와 허용값도 검사한다. 입력이나 파일은 변경하지 않으며, attrs 값의 형식이
    예상과 다르면 변환 과정의 예외가 호출자에게 전달될 수 있다.
    """
    bad = []
    required = REQUIRED_METADATA_1_0 if ver == "1.0" else REQUIRED_METADATA_1_1
    for key in required:
        if key not in a:
            bad.append("루트 attrs 누락: %s" % key)

    ch = a.get("channel_type")
    if ch is not None and str(ch) not in CHANNEL_TYPES:
        bad.append("channel_type 이 허용 목록 밖: %r (허용 %s)" % (ch, list(CHANNEL_TYPES)))

    if ver == "1.0":
        return bad

    # ── 아래는 1.1 전용 분기 ──────────────────────────────
    axis = str(a.get("sample_axis", ""))
    if axis and axis not in SAMPLE_AXES:
        bad.append("sample_axis 가 허용 목록 밖: %r (허용 %s)" % (axis, list(SAMPLE_AXES)))

    if axis == "time":
        for key in REQUIRED_METADATA_TIME_AXIS:
            if key not in a:
                bad.append("루트 attrs 누락 (sample_axis=time): %s" % key)

    # 에뮬레이션 필수 메타데이터(SCHEMA.md §3.9)는 **채널로** 정해진다.
    # 축으로만 분기하면 `channel_type=emulated-power` 인데 `sample_axis=time` 인 파일이
    # leakage_model 도 binary_sha256 도 없이 통과한다 — 값이 무엇인지 알 수 없는
    # 데이터셋이 "준수" 로 보고되는 셈이다.
    if str(ch) == "emulated-power":
        for key in REQUIRED_METADATA_EMULATED:
            if key not in a:
                bad.append("루트 attrs 누락 (channel_type=emulated-power): %s" % key)
        if axis and axis != "instruction":
            bad.append("channel_type=emulated-power 인데 sample_axis=%r 다 — "
                       "에뮬레이션 트레이스의 축은 명령어여야 한다" % axis)

    if str(ch) == "power":
        for key in REQUIRED_METADATA_POWER_1_1:
            if key not in a:
                bad.append("루트 attrs 누락 (channel_type=power): %s "
                           "— 없으면 ISO/IEC 17825 Annex B 대역폭 요건을 판정할 수 없다" % key)

    unit = a.get("exec_time_unit")
    if unit is not None and str(unit) not in EXEC_TIME_UNITS:
        bad.append("exec_time_unit 이 허용 목록 밖: %r (허용 %s)"
                   % (unit, list(EXEC_TIME_UNITS)))
    return bad


def _check_sample_map(h5, a, ver):
    """샘플 → 명령어 역매핑 검사.

    명령어 축 데이터셋에서 이 배열이 없으면 "어디서 새는가" 를 말할 수 없다.
    누설 지점을 명령어로 지목하는 것이 에뮬레이션 채널의 존재 이유이므로 필수다.
    ``h5``와 루트 attrs ``a``를 읽어 위반 문자열 목록을 반환한다. 파일을 변경하지 않으며,
    손상된 HDF5 객체 접근 오류는 호출자에게 전달된다.
    """
    bad = []
    if ver == "1.0":
        return bad
    if str(a.get("sample_axis", "")) != "instruction" and \
            str(a.get("channel_type", "")) != "emulated-power":
        return bad
    if F_SAMPLE_MAP not in h5:
        bad.append("루트 배열 누락: %s (sample_axis=instruction 이면 필수)" % F_SAMPLE_MAP)
        return bad
    sm = h5[F_SAMPLE_MAP]
    if sm.ndim != 2 or sm.shape[1] != 3:
        bad.append("%s 는 (ns, 3) 이어야 한다 — (segment_id, instruction_index, address). 현재 %s"
                   % (F_SAMPLE_MAP, sm.shape))
    elif "samples_per_trace" in a and int(a["samples_per_trace"]) != sm.shape[0]:
        bad.append("%s 행 수 %d ≠ samples_per_trace %s"
                   % (F_SAMPLE_MAP, sm.shape[0], a["samples_per_trace"]))
    return bad


def _check_subset(h5, name, a):
    """한 Subset의 배열·HDF5 attrs·행 정렬 위반을 문자열 목록으로 반환한다.

    ``name``이 가리키는 그룹의 필수 배열, 역할, Record 수, Trace 형상·dtype을 루트
    Metadata ``a``와 대조한다. 읽기 전용이며 파일을 변경하지 않는다. 그룹이 아니거나
    배열 형식이 손상됐으면 h5py 또는 형상 접근 예외가 호출자에게 전달될 수 있다.
    """
    bad = []
    g = h5[name]
    for key in REQUIRED_SUBSET_METADATA:
        if key not in g.attrs:
            bad.append("/%s attrs 누락: %s" % (name, key))
    role = g.attrs.get("role")
    if role is not None and str(role) not in SUBSET_ROLES:
        bad.append("/%s role 이 허용 목록 밖: %r" % (name, role))

    for field in (F_TRACE, F_KEY, F_PLAINTEXT):
        if field not in g:
            bad.append("/%s 필수 배열 누락: %s" % (name, field))
    if F_TRACE not in g:
        return bad

    # 행 정렬 — 이 규칙이 깨지면 레코드 대응이 무너져 데이터셋 전체가 무효다.
    rows = {f: g[f].shape[0] for f in g}
    if len(set(rows.values())) != 1:
        bad.append("/%s 행 수 불일치: %s" % (name, rows))
    n_rec = g.attrs.get("n_records")
    if n_rec is not None and int(n_rec) != g[F_TRACE].shape[0]:
        bad.append("/%s n_records=%s 인데 trace 는 %d 행"
                   % (name, n_rec, g[F_TRACE].shape[0]))

    # 루트 Metadata 와 실제 배열이 어긋나면 둘 중 하나가 거짓말이다.
    if "samples_per_trace" in a and int(a["samples_per_trace"]) != g[F_TRACE].shape[1]:
        bad.append("/%s trace 열 수 %d ≠ samples_per_trace %s"
                   % (name, g[F_TRACE].shape[1], a["samples_per_trace"]))
    if "sample_dtype" in a and str(a["sample_dtype"]) != str(g[F_TRACE].dtype):
        bad.append("/%s trace dtype %s ≠ sample_dtype %s"
                   % (name, g[F_TRACE].dtype, a["sample_dtype"]))
    if np.issubdtype(g[F_TRACE].dtype, np.integer) and "sample_scale" not in a:
        bad.append("/%s trace 가 정수형인데 sample_scale 이 없다 (SCHEMA.md §5.2)" % name)

    if F_EXEC_TIME in g and g[F_EXEC_TIME].ndim != 1:
        bad.append("/%s %s 는 (n,) 이어야 한다. 현재 %s"
                   % (name, F_EXEC_TIME, g[F_EXEC_TIME].shape))
    return bad


def require_schema(path):
    """Dataset(데이터셋)을 검증하고 위반이 없으면 `True`를 반환한다.

    수집 직후와 분석 시작 시 잘못된 Dataset이 다음 단계로 넘어가지 않게 하는 경계다.
    파일이 없으면 `validate_dataset()`의 위반을 담은 `RuntimeError`가 발생하며 파일은
    변경하지 않는다.
    """
    bad = validate_dataset(path=path)
    if bad:
        raise RuntimeError("SCHEMA.md 위반 %d건:\n  - %s" % (len(bad), "\n  - ".join(bad)))
    return True


# ─────────────────────────────────────────────────────────────
# 경로 기반 로더 — 어느 프로젝트의 h5 든 읽는다
# ─────────────────────────────────────────────────────────────
def group_len(path, group):
    """그룹이 실제로 보유한 레코드 수. 파형은 읽지 않는다.

    목표 트레이스 수를 분석에 박으면 수집이 중간에 끊긴 파일에서 조용히 어긋난다.
    "있는 만큼" 을 물어보는 창구다.

    실패 조건: 파일이 없으면 FileNotFoundError, 그룹 이름이 틀리면 KeyError.
    """
    with h5py.File(_must_exist(path), "r") as h5:
        if group not in h5:
            raise KeyError("그룹 '%s' 가 없다. 사용 가능: %s" % (group, list(h5)))
        return int(h5[group][F_TRACE].shape[0])


def load_group(path, group, n=None, samples=None, fields=None):
    """데이터셋의 한 그룹을 메모리로 읽는다.

    입력
        path    : h5 경로
        group   : subset 이름
        n       : 앞에서 몇 레코드만. None 이면 전부
        samples : 샘플 축 슬라이스. POI 구간만 읽을 때
        fields  : 읽을 배열 이름 목록. None 이면 그룹의 전부

    출력 (dict)
        배열 이름 → numpy 배열, 그리고
        "attrs"       : 루트 Metadata (dict)
        "subset_attrs": 그 subset 의 Metadata (dict)

    반환 키가 온디스크 이름 그대로인 이유: 이름을 바꿔 주면 그 대응표가 또 하나의
    고칠 곳이 된다. SCHEMA.md 를 읽은 사람이 그대로 쓸 수 있게 둔다.

    실패 조건: 그룹 이름이 틀리면 KeyError.
    """
    with h5py.File(_must_exist(path), "r") as h5:
        if group not in h5:
            raise KeyError("그룹 '%s' 가 없다. 사용 가능: %s" % (group, list(h5)))
        g = h5[group]
        sl = slice(None) if n is None else slice(0, n)
        want = list(g) if fields is None else list(fields)
        out = {}
        for f in want:
            if f not in g:
                raise KeyError("/%s 에 배열 '%s' 가 없다. 사용 가능: %s" % (group, f, list(g)))
            if f == F_TRACE and samples is not None:
                out[f] = g[f][sl, samples]
            else:
                out[f] = g[f][sl]
        out["attrs"] = {k: h5.attrs[k] for k in h5.attrs}
        out["subset_attrs"] = {k: g.attrs[k] for k in g.attrs}
        return out


def load_sample_map(path):
    """루트 `sample_map` 을 (ns, 3) uint32 배열로 읽는다.

    열: (segment_id, instruction_index, address)
    실패 조건: 배열이 없으면 KeyError — 명령어 축 데이터셋이 아니라는 뜻이다.
    """
    with h5py.File(_must_exist(path), "r") as h5:
        if F_SAMPLE_MAP not in h5:
            raise KeyError("%s 가 없다 — sample_axis=instruction 데이터셋이 아니다: %s"
                           % (F_SAMPLE_MAP, path))
        return h5[F_SAMPLE_MAP][:]


def instruction_window_columns(path, lo, hi):
    """명령어 인덱스 구간 `[lo, hi)` 에 해당하는 **샘플 열 인덱스**를 돌려준다.

    왜 필요한가: 명령어 축 데이터셋의 trace 는 성분을 **연접**한 것이라
    `trace[:, lo:hi]` 로 자르면 **첫 성분만** 잘린다 — `hw_reg` 의 1000번 샘플과
    `hd_reg` 의 1000번 샘플은 서로 다른 명령어다. 구간을 명령어 기준으로 다루려면
    `sample_map` 의 명령어 인덱스 열로 골라야 한다.

    이 변환이 분석 모듈마다 따로 있으면 한 곳만 고쳤을 때 조용히 어긋난다. 스키마의
    의미를 해석하는 일이므로 정의를 여기 둔다.

    출력: 열 인덱스 (1차원 배열). `sample_map` 이 없으면 **None** — 명령어 축
    데이터셋이 아니라는 뜻이며, 호출측은 구간 제한 없이 전 구간을 보면 된다.
    """
    with h5py.File(_must_exist(path), "r") as h5:
        if F_SAMPLE_MAP not in h5:
            return None
        idx = h5[F_SAMPLE_MAP][:, 1]
    return np.flatnonzero((idx >= lo) & (idx < hi))


def root_attrs(path):
    """루트 HDF5 attrs를 Metadata 사전으로 읽고 배열 본문은 읽지 않는다.

    파일이 없으면 `FileNotFoundError`, HDF5가 손상됐으면 h5py 예외가 발생한다. 읽기
    전용으로 열기 때문에 파일을 변경하지 않는다.
    """
    with h5py.File(_must_exist(path), "r") as h5:
        return {k: h5.attrs[k] for k in h5.attrs}


def subset_names(path):
    """루트에 있는 HDF5 그룹 이름을 Subset 목록으로 반환한다.

    루트 배열은 제외한다. 파일이 없거나 읽을 수 없으면 `_must_exist()` 또는 h5py의
    예외가 발생하며 파일을 변경하지 않는다.
    """
    with h5py.File(_must_exist(path), "r") as h5:
        return [n for n in h5 if isinstance(h5[n], h5py.Group)]


def _must_exist(path):
    """기존 Dataset 파일 경로를 ``Path``로 반환한다.

    ``path``가 파일이 아니면 경로를 포함한 ``FileNotFoundError``를 발생시킨다. 경로를
    확인하기만 하며 파일이나 디렉터리를 만들지 않는다.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError("데이터셋이 없다: %s" % p)
    return p
