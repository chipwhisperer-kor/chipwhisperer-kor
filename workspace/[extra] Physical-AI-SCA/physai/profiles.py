"""ISO/IEC 17825 사전진단 프로파일과 캠페인 단계의 단일 진실 공급원.

원시 v2 명세에는 프로파일 이름만 적는다. 보안 수준, 효과크기, 통계 정책, 시간 제한,
반복 수와 subset 수량은 이 모듈에서만 정의하고 ``resolve()``가 실행용 명세에 채운다.
따라서 기준을 바꿀 때 여러 YAML을 함께 고칠 필요가 없다.
"""

from copy import deepcopy
import math

from scipy.stats import norm


PROFILES = {
    "iso-17825-l3": {
        "security_level": 3,
        "effect_size_d": 0.04,
        "max_acquisition_hours": 6,
        "ta_raw_per_block": 1000,
        "spa_required_traces": 11,
        "spa_points_per_csp_bit": 100,
        "preprocessing": {
            "average_n": 10,
            "alignment": "trigger-checked",
            "filter": None,
        },
    },
    "iso-17825-l4": {
        "security_level": 4,
        "effect_size_d": 0.01,
        "max_acquisition_hours": 24,
        "ta_raw_per_block": 10000,
        "spa_required_traces": 21,
        "spa_points_per_csp_bit": 1000,
        "preprocessing": {
            "average_n": 10,
            "alignment": "static+dynamic",
            "filter": {
                "kind": "butterworth-bandpass",
                "order": 4,
                "low_clock_multiplier": 0.5,
                "high_clock_multiplier": 1.5,
                "zero_phase": True,
                "minimum_inband_prominence_db": 6.0,
            },
            "dynamic_alignment": {
                "reference": "spa_same:0:0",
                "anchors": 8,
                "max_static_shift_cycles": 2.0,
                "max_local_shift_cycles": 1.0,
                "minimum_correlation": 0.8,
                "interpolation": "linear",
                "edge_policy": "common-valid-crop",
            },
        },
    },
}

STATISTICS = {
    "alpha": 1.0e-5,
    "beta": 0.05,
    "multiplicity_correction": "bonferroni",
    "t_threshold": 4.5,
}

# soundness는 ISO 필수 판정이 아니지만 결과를 본 뒤 귀무분포 정밀도를 바꾸지 않도록
# 수집 전 resolved spec에 고정한다. 100회는 CW Lab의 실행시간과 임계 안정성 사이의 계약값이다.
ANALYSIS_PARAMETERS = {"soundness_permutations": 100}


class ProfileError(ValueError):
    """알 수 없는 프로파일·단계 또는 유도할 수 없는 subset 구성을 나타낸다."""


def required_n_from_profile(profile_name):
    """프로파일의 α·β·d로 Formula (1)의 총 논리 트레이스 수를 계산한다."""
    p = PROFILES[profile_name]
    za = norm.ppf(1.0 - STATISTICS["alpha"] / 2.0)
    zb = norm.ppf(1.0 - STATISTICS["beta"])
    return int(round(4.0 * (za + zb) ** 2 / p["effect_size_d"] ** 2))


def _subset_n(stage, role, profile, pair_kind=None):
    """캠페인 단계와 subset 역할에서 논리 레코드 수를 유도한다."""
    if stage == "smoke":
        return {"timing": 4, "simple-analysis": 2, "exploration": 16,
                "leakage-detection-fixed": 8, "leakage-detection-random": 8,
                "profiling": 16, "attack": 16}[role]
    if stage == "cw-lab-pilot":
        return {"timing": 32, "simple-analysis": 4, "exploration": 128,
                "leakage-detection-fixed": 64, "leakage-detection-random": 64,
                "profiling": 128, "attack": 128}[role]
    if stage != "full":
        raise ProfileError("알 수 없는 campaign_stage: %s" % stage)

    repeats = int(profile["preprocessing"]["average_n"])
    need = required_n_from_profile(
        "iso-17825-l%d" % int(profile["security_level"]))
    if role == "timing":
        return int(math.ceil(profile["ta_raw_per_block"] / repeats))
    if role == "simple-analysis":
        # L3는 기존 세 쌍을 각각 4장으로 수집해 최소 11장을 초과 충족한다.
        return 4 if profile["security_level"] == 3 else 7
    if role in ("leakage-detection-fixed", "leakage-detection-random"):
        return int(math.ceil(need / 2.0))
    if role in ("attack", "profiling", "exploration"):
        return need
    raise ProfileError("수량 정책이 없는 subset role: %s" % role)


def resolve(raw):
    """검증된 원시 v2 명세를 기존 수집·분석기가 소비할 실행용 명세로 확장한다.

    입력 사전은 수정하지 않는다. 결과에는 유도된 ``criteria``·subset ``n``과 기존 코드가
    사용하는 ``scope.target_level``·``scope.security_function``이 들어간다. 이 값들은
    원시 계약의 중복 정의가 아니라 프로파일/알고리즘 참조에서 매번 계산한 파생값이다.
    """
    out = deepcopy(raw)
    name = out["assessment_profile"]
    if name not in PROFILES:
        raise ProfileError("알 수 없는 assessment_profile: %s" % name)
    profile = deepcopy(PROFILES[name])
    stage = out["campaign_stage"]
    if stage not in ("smoke", "cw-lab-pilot", "full"):
        raise ProfileError("알 수 없는 campaign_stage: %s" % stage)

    contextual = out.pop("criteria_context")
    out["criteria"] = {
        "security_level": profile["security_level"],
        "effect_size_d": profile["effect_size_d"],
        **STATISTICS,
        "max_acquisition_hours": profile["max_acquisition_hours"],
        "sensitive_leakage_time": contextual["sensitive_leakage_time"],
        "preprocessing": profile["preprocessing"],
        "vendor_info": contextual["vendor_info"],
    }
    out["profile_requirements"] = {
        "ta_raw_per_block": profile["ta_raw_per_block"],
        "spa_required_traces": profile["spa_required_traces"],
        "spa_points_per_csp_bit": profile["spa_points_per_csp_bit"],
    }
    out["analysis_parameters"] = deepcopy(ANALYSIS_PARAMETERS)
    out["scope"]["target_level"] = profile["security_level"]
    out["scope"]["security_function"] = out["algorithm"]
    for subset in out["subsets"]:
        subset["n"] = _subset_n(stage, subset["role"], profile,
                                 subset.get("spa_pair_kind"))
    return out
