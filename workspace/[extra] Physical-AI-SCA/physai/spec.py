"""실험 명세(spec) 로드·검증, 그리고 명세에서 유도되는 값 계산.

spec 은 **AI 와 도구 사이의 유일한 접점**이다. AI 가 실험을 설계해 YAML 로 쓰고,
collect·analyze 가 그것만 읽는다. 사람이 손으로 써도 똑같이 동작한다.

여기서 계산하는 유도값(필요 장수 N, 보정 임계)은 spec 에 적지 않는다 —
파라미터의 **결과**이지 판단이 아니기 때문이다. 적어 두면 파라미터와 어긋날 수 있다.
"""

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from scipy.stats import norm

from . import paths

SCHEMA_PATH = paths.CONTRACTS / "experiment_spec.schema.json"


class SpecError(ValueError):
    """spec 이 계약을 어겼다. 메시지에 위반 목록을 담는다."""


def load(spec_path):
    """spec YAML 을 읽고 계약(JSON Schema)에 맞는지 검사한다.

    출력: dict
    실패 조건: 파일이 없으면 FileNotFoundError, 계약 위반이면 SpecError(전체 목록).

    위반을 하나씩 던지지 않고 모아서 던지는 이유는 검증기와 같다 — 첫 번째만 고치면
    다음 것이 또 나온다.
    """
    p = Path(spec_path)
    if not p.is_file():
        raise FileNotFoundError("spec 이 없다: %s" % p)
    spec = yaml.safe_load(p.read_text(encoding="utf-8"))

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(spec),
                    key=lambda e: list(e.absolute_path))
    if errors:
        lines = ["%s: %s" % ("/".join(str(x) for x in e.absolute_path) or "(root)", e.message)
                 for e in errors]
        raise SpecError("spec 계약 위반 %d건 (%s):\n  - %s"
                        % (len(lines), p.name, "\n  - ".join(lines)))

    _check_cross_field(spec, p.name)
    return spec


def _check_cross_field(spec, name):
    """JSON Schema 로 표현할 수 없는 규칙 — 필드끼리의 정합성."""
    bad = []
    c = spec["criteria"]
    if c["security_level"] != spec["scope"]["target_level"]:
        bad.append("criteria.security_level(%s) 과 scope.target_level(%s) 이 다르다"
                   % (c["security_level"], spec["scope"]["target_level"]))

    # Annex A.2.3 / A.3.3 이 정한 표준 effect size. 다른 값을 쓰는 것 자체는 막지 않되,
    # 표준값과 다르면 대조표에서 근거를 대야 하므로 여기서 경고 대신 오류로 잡는다.
    expected_d = {3: 0.04, 4: 0.01}[c["security_level"]]
    if abs(c["effect_size_d"] - expected_d) > 1e-12:
        bad.append("effect_size_d=%s 인데 Level %d 의 표준값은 %s 다 "
                   "(ISO/IEC 17825 A.%d.3). 의도한 값이면 rationale 에 근거를 적고 이 검사를 지운다."
                   % (c["effect_size_d"], c["security_level"], expected_d,
                      2 if c["security_level"] == 3 else 3))

    if spec["collector"]["kind"] == "emulation":
        if not spec["collector"].get("components"):
            bad.append("collector.kind=emulation 이면 components 가 필요하다")
        if not spec["collector"].get("window"):
            bad.append("collector.kind=emulation 이면 window 가 필요하다")
        if "emulated-power" not in spec["scope"]["channels"]:
            bad.append("collector.kind=emulation 인데 scope.channels 에 emulated-power 가 없다")

    names = [s["name"] for s in spec["subsets"]]
    if len(set(names)) != len(names):
        bad.append("subset 이름이 중복된다: %s" % names)

    # 필수 시험(ta·spa·dpa)에 필요한 subset 이 실제로 있는가.
    roles = {s["role"] for s in spec["subsets"]}
    need = {"ta": {"timing"},
            "spa": {"simple-analysis"},
            "dpa": {"leakage-detection-fixed", "leakage-detection-random"},
            "soundness": {"profiling"},
            "cpa": {"attack"}}
    for a in spec["analyses"]:
        missing = need.get(a, set()) - roles
        if missing:
            bad.append("analyses 에 '%s' 가 있는데 role %s 인 subset 이 없다"
                       % (a, sorted(missing)))

    if bad:
        raise SpecError("spec 정합성 위반 %d건 (%s):\n  - %s"
                        % (len(bad), name, "\n  - ".join(bad)))


# ─────────────────────────────────────────────────────────────
# spec 에서 유도되는 값
# ─────────────────────────────────────────────────────────────
def required_n(criteria):
    """ISO/IEC 17825 Formula (1) — DPA 에 필요한 총 트레이스 수.

        N = 4 (Z_{α/2} + Z_β)² / d²

    두 subset 을 합친 수다(N = N_A + N_B). 장수는 판단이 아니라 α·β·d 의 **결과**이므로
    spec 에 적지 않고 여기서 계산해 계획 보고서에 근거와 함께 싣는다.
    """
    a, b, d = criteria["alpha"], criteria["beta"], criteria["effect_size_d"]
    z_a = norm.ppf(1.0 - a / 2.0)
    z_b = norm.ppf(1.0 - b)
    n = 4.0 * (z_a + z_b) ** 2 / (d ** 2)
    return {"n_required": int(round(n)), "z_alpha_half": float(z_a), "z_beta": float(z_b),
            "formula": "N = 4 (Z_{alpha/2} + Z_beta)^2 / d^2",
            "source": "ISO/IEC 17825:2024 Formula (1)"}


def corrected_threshold(criteria, n_tests):
    """다중비교 보정 후의 t 임계.

    §8.4 `shall [08.03]` 이 보정을 요구한다. 샘플이 수만 개인 파형에서 보정 없이
    |t| > 4.5 를 쓰면 귀무가설이 참이어도 수십 개가 우연히 넘는다.

    Bonferroni: per-test 유의수준 α/m 에 해당하는 정규분포 양측 임계를 쓴다.
    (자유도가 큰 t 분포는 정규분포에 수렴하므로 정규 근사로 충분하다. 표본이
     수천 이상인 이 시험의 조건에서 그렇다.)
    """
    t0 = float(criteria["t_threshold"])
    kind = criteria["multiplicity_correction"]
    if kind == "none" or n_tests <= 1:
        return {"threshold": t0, "correction": kind, "n_tests": int(n_tests),
                "alpha_per_test": float(criteria["alpha"])}
    alpha_per = float(criteria["alpha"]) / float(n_tests)
    t_corr = float(norm.ppf(1.0 - alpha_per / 2.0))
    return {"threshold": max(t_corr, t0), "correction": "bonferroni",
            "n_tests": int(n_tests), "alpha_per_test": alpha_per,
            "threshold_uncorrected": t0,
            "note": "보정 임계와 spec 의 t_threshold 중 큰 값을 쓴다 — 둘 다 하한이다."}


def subset_by_role(spec, role):
    """해당 role 인 subset 정의 목록."""
    return [s for s in spec["subsets"] if s["role"] == role]


def summary_lines(spec):
    """사람이 읽을 요약. collect 가 시작할 때 찍는다."""
    c = spec["criteria"]
    n = required_n(c)
    out = [
        "spec         : %s — %s" % (spec["id"], spec["title"]),
        "IUT          : %s (대책: %s)" % (spec["iut"]["name"], spec["iut"]["countermeasure"]),
        "수집기       : %s" % spec["collector"]["kind"],
        "채널         : %s" % ", ".join(spec["scope"]["channels"]),
        "판정 기준    : Level %d, d=%s, α=%s, β=%s, %s 보정, |t|>%s"
        % (c["security_level"], c["effect_size_d"], c["alpha"], c["beta"],
           c["multiplicity_correction"], c["t_threshold"]),
        "Formula (1)  : N = %d 장 필요 (Z_α/2=%.4f, Z_β=%.4f)"
        % (n["n_required"], n["z_alpha_half"], n["z_beta"]),
        "전처리       : 평균 %d회, 정렬 %s"
        % (c["preprocessing"]["average_n"], c["preprocessing"]["alignment"]),
        "분석         : %s" % ", ".join(spec["analyses"]),
        "주장하지 않음:",
    ]
    out += ["  - %s" % s for s in spec["scope"]["not_claimed"]]
    out.append("Subset       :")
    for s in spec["subsets"]:
        out.append("  /%-14s [%-24s] %7d 장  키=%s 평문=%s"
                   % (s["name"], s["role"], s["n"], s["key_mode"], s["pt_mode"]))
    return out
