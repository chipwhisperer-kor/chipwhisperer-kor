"""v2 실험·study 계약 로드와 프로파일 유도값 계산.

YAML은 수집 전에 고정하는 원시 계약이고 ``profiles.py``는 수치 기준의 유일한 정의다.
``load()``는 두 정보를 결합한 실행용 사전을 반환한다. v1을 묵시적으로 보정하지 않는
이유는 어떤 프로파일·단계를 의도했는지 추측하면 기존 결과의 의미가 바뀌기 때문이다.
"""

from copy import deepcopy
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from scipy.stats import norm

from . import paths, profiles
from .algorithms import get as get_algorithm

SCHEMA_PATH = paths.CONTRACTS / "experiment_spec.schema.json"
STUDY_SCHEMA_PATH = paths.CONTRACTS / "study.schema.json"


class SpecError(ValueError):
    """명세 또는 study 계약 위반 전체를 사람이 고칠 수 있는 메시지로 담는다."""


def _validate(document, schema_path, label):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(document),
                    key=lambda e: list(e.absolute_path))
    if errors:
        lines = ["%s: %s" % ("/".join(str(x) for x in e.absolute_path) or "(root)",
                             e.message) for e in errors]
        raise SpecError("%s 계약 위반 %d건:\n  - %s"
                        % (label, len(lines), "\n  - ".join(lines)))


def load(spec_path, defaults=None):
    """v2 experiment YAML을 검증하고 프로파일이 적용된 실행용 명세를 반환한다.

    ``defaults``는 study가 소유한 assessment_profile/campaign_stage/algorithm 세 참조만
    제공한다. experiment가 같은 값을 복제하면 오류를 내지는 않지만 study와 다르면 즉시
    거부한다. 파일 누락, YAML 형식, 계약 또는 교차 필드 위반은 예외로 전파된다.
    """
    p = Path(spec_path)
    if not p.is_file():
        raise FileNotFoundError("spec 이 없다: %s" % p)
    raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SpecError("spec 최상위는 객체여야 한다: %s" % p)
    if raw.get("schema_version") != 2:
        raise SpecError("v1 명세는 지원하지 않는다: %s. schema_version: 2로 명시적으로 마이그레이션한다."
                        % p.name)
    raw = deepcopy(raw)
    for key in ("assessment_profile", "campaign_stage", "algorithm"):
        if defaults and key in defaults:
            if key in raw and raw[key] != defaults[key]:
                raise SpecError("study.%s=%r와 %s의 %s=%r가 다르다"
                                % (key, defaults[key], p.name, key, raw[key]))
            raw[key] = defaults[key]
    _validate(raw, SCHEMA_PATH, p.name)
    get_algorithm(raw["algorithm"])
    _check_cross_field(raw, p.name)
    resolved = profiles.resolve(raw)
    resolved["_spec_path"] = str(p.resolve())
    return resolved


def load_study(study_path):
    """study YAML을 검증하고 참조 experiment 경로를 프로젝트 절대경로로 해석한다."""
    p = Path(study_path)
    if not p.is_file():
        raise FileNotFoundError("study 가 없다: %s" % p)
    study = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(study, dict) or study.get("schema_version") != 2:
        raise SpecError("study는 schema_version: 2 객체여야 한다: %s" % p)
    _validate(study, STUDY_SCHEMA_PATH, p.name)
    get_algorithm(study["algorithm"])
    out = deepcopy(study)
    for item in out["experiments"]:
        candidate = paths.PROJECT / item["spec"]
        if not candidate.is_file():
            raise SpecError("study experiment 파일이 없다: %s" % item["spec"])
        item["spec_path"] = candidate
    return out


def study_experiments(study_path):
    """study 순서를 보존해 ``(experiment metadata, resolved spec)`` 목록을 반환한다."""
    study = load_study(study_path)
    defaults = {k: study[k] for k in ("assessment_profile", "campaign_stage", "algorithm")}
    found, out = set(), []
    for item in study["experiments"]:
        sp = load(item["spec_path"], defaults=defaults)
        sp["_study_path"] = str(Path(study_path).resolve())
        if sp["id"] in found:
            raise SpecError("study 안의 experiment id가 중복된다: %s" % sp["id"])
        found.add(sp["id"])
        out.append((item, sp))
    for item, sp in out:
        other = item.get("compare_with")
        if other and other not in found:
            raise SpecError("%s compare_with 대상이 study에 없다: %s" % (sp["id"], other))
    return study, out


def load_from_study(study_path, experiment_id):
    """study에서 ID가 일치하는 단일 실행용 experiment를 반환한다."""
    _, experiments = study_experiments(study_path)
    for _, sp in experiments:
        if sp["id"] == experiment_id:
            return sp
    raise SpecError("study에 experiment가 없다: %s" % experiment_id)


def _check_cross_field(raw, name):
    bad = []
    if raw["collector"]["kind"] == "emulation":
        if not raw["collector"].get("components") or not raw["collector"].get("window"):
            bad.append("collector.kind=emulation이면 components와 window가 필요하다")
        if "emulated-power" not in raw["scope"]["channels"]:
            bad.append("emulation 수집기인데 scope.channels에 emulated-power가 없다")
    names = [s["name"] for s in raw["subsets"]]
    if len(set(names)) != len(names):
        bad.append("subset 이름이 중복된다: %s" % names)
    by_name = {s["name"]: s for s in raw["subsets"]}
    need_roles = {"ta": {"timing"}, "spa": {"simple-analysis"},
                  "tvla": {"leakage-detection-fixed", "leakage-detection-random"},
                  "dpa": {"attack"}, "soundness": {"profiling"}, "cpa": {"attack"}}
    roles = {s["role"] for s in raw["subsets"]}
    for analysis in raw["analyses"]:
        missing = need_roles.get(analysis, set()) - roles
        if missing:
            bad.append("analysis %s에 필요한 role이 없다: %s" % (analysis, sorted(missing)))
    ai = raw["analysis_inputs"]
    for analysis, keys in (("tvla", ("fixed", "random")), ("dpa", ("subset",)),
                           ("cpa", ("subset",))):
        if analysis not in raw["analyses"]:
            continue
        for key in keys:
            subset = ai[analysis][key]
            if subset not in by_name:
                bad.append("analysis_inputs.%s.%s가 없는 subset을 가리킨다: %s"
                           % (analysis, key, subset))
    algo = get_algorithm(raw["algorithm"])
    if ai["dpa"]["target"] not in algo.DPA_TARGETS:
        bad.append("알고리즘이 지원하지 않는 DPA target: %s" % ai["dpa"]["target"])
    if "cpa" in raw["analyses"] and not algo.CPA_SUPPORTED:
        bad.append("algorithm %s은 CPA 모델을 제공하지 않는다" % raw["algorithm"])
    if "soundness" in raw["analyses"] and not algo.SOUNDNESS_SUPPORTED:
        bad.append("algorithm %s은 soundness 모델을 제공하지 않는다" % raw["algorithm"])
    if bad:
        raise SpecError("spec 정합성 위반 %d건 (%s):\n  - %s"
                        % (len(bad), name, "\n  - ".join(bad)))


def required_n(criteria):
    """ISO/IEC 17825 Formula (1)의 두 집단 합계 N을 계산한다."""
    a, b, d = criteria["alpha"], criteria["beta"], criteria["effect_size_d"]
    za, zb = norm.ppf(1.0 - a / 2.0), norm.ppf(1.0 - b)
    n = 4.0 * (za + zb) ** 2 / d ** 2
    return {"n_required": int(round(n)), "z_alpha_half": float(za), "z_beta": float(zb),
            "formula": "N = 4 (Z_{alpha/2} + Z_beta)^2 / d^2",
            "source": "ISO/IEC 17825:2024 Formula (1)"}


def corrected_threshold(criteria, n_tests):
    """사전 지정 하한과 Bonferroni 보정 임계 중 더 엄격한 값을 반환한다."""
    t0 = float(criteria["t_threshold"])
    kind = criteria["multiplicity_correction"]
    if kind == "none" or n_tests <= 1:
        return {"threshold": t0, "correction": kind, "n_tests": int(n_tests),
                "alpha_per_test": float(criteria["alpha"])}
    alpha_per = float(criteria["alpha"]) / float(n_tests)
    corrected = float(norm.ppf(1.0 - alpha_per / 2.0))
    return {"threshold": max(corrected, t0), "correction": "bonferroni",
            "n_tests": int(n_tests), "alpha_per_test": alpha_per,
            "threshold_uncorrected": t0}


def summary_lines(spec):
    """수집 전에 프로파일·단계·유도 수량과 주장 제한을 사람이 검토할 줄로 만든다."""
    c, need = spec["criteria"], required_n(spec["criteria"])
    out = [
        "spec         : %s — %s" % (spec["id"], spec["title"]),
        "프로파일     : %s / %s" % (spec["assessment_profile"], spec["campaign_stage"]),
        "알고리즘     : %s" % spec["algorithm"],
        "IUT          : %s (대책: %s)" % (spec["iut"]["name"], spec["iut"]["countermeasure"]),
        "판정 기준    : Level %d, d=%s, α=%s, β=%s, %s, |t|>%s"
        % (c["security_level"], c["effect_size_d"], c["alpha"], c["beta"],
           c["multiplicity_correction"], c["t_threshold"]),
        "Formula (1)  : N = %d 논리 트레이스" % need["n_required"],
        "전처리       : 평균 %d회, 정렬 %s"
        % (c["preprocessing"]["average_n"], c["preprocessing"]["alignment"]),
        "분석         : %s" % ", ".join(spec["analyses"]),
        "주장하지 않음:",
    ]
    out += ["  - %s" % x for x in spec["scope"]["not_claimed"]]
    out.append("Subset:")
    for s in spec["subsets"]:
        out.append("  /%-14s [%-24s] %7d장 키=%s 평문=%s"
                   % (s["name"], s["role"], s["n"], s["key_mode"], s["pt_mode"]))
    return out
