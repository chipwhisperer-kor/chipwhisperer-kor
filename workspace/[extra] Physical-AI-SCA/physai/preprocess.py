"""Schema 1.3 원본 Execution을 전처리·평균한 파생 분석 Dataset 생성기.

원본은 읽기 전용이다. L3는 같은 입력 10행을 직접 평균하고, L4 전력은 각 행을 필터·정렬한
뒤 평균한다. 파생 경로는 원본 SHA-256과 전처리 계약에서 결정되며 계약과 파일 해시가 같은
기존 파생물만 재사용한다.
"""

import hashlib
import json
from pathlib import Path

import h5py
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfreqz

from . import artifacts, paths
import sca_schema as S  # noqa: E402


class PreprocessError(RuntimeError):
    """L4 전처리 사전조건이나 고정 품질 기준을 만족하지 못했다."""


def _corr(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    finite = np.isfinite(a) & np.isfinite(b)
    if np.count_nonzero(finite) < 8:
        return -1.0
    a, b = a[finite], b[finite]
    a, b = a - a.mean(), b - b.mean()
    den = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / den) if den else -1.0


def _best_shift(reference, trace, limit, lo=0, hi=None):
    """reference 좌표 x와 trace 좌표 x+shift의 정규화 상관이 최대인 정수 이동을 찾는다."""
    hi = len(reference) if hi is None else hi
    best = (None, -2.0)
    for shift in range(-limit, limit + 1):
        beg, end = max(lo, -shift), min(hi, len(trace) - shift)
        if end - beg < 8:
            continue
        corr = _corr(reference[beg:end], trace[beg + shift:end + shift])
        if corr > best[1]:
            best = (shift, corr)
    if best[0] is None:
        raise PreprocessError("정렬 상관을 계산할 공통 구간이 없다")
    return best


def _align(reference, trace, samples_per_cycle, cfg):
    static_limit = max(1, int(round(cfg["max_static_shift_cycles"] * samples_per_cycle)))
    local_limit = max(1, int(round(cfg["max_local_shift_cycles"] * samples_per_cycle)))
    static, static_corr = _best_shift(reference, trace, static_limit)
    x = np.arange(trace.size, dtype=np.float64)
    stat = np.interp(x + static, x, trace, left=np.nan, right=np.nan)

    anchors = int(cfg["anchors"])
    width = max(16, trace.size // anchors)
    centers = np.linspace(width // 2, trace.size - width // 2 - 1, anchors).astype(int)
    shifts, corrs = [], []
    for center in centers:
        lo, hi = center - width // 2, center + width // 2
        local, corr = _best_shift(reference, stat, local_limit, max(0, lo), min(trace.size, hi))
        shifts.append(local)
        corrs.append(corr)
    if min(corrs) < float(cfg["minimum_correlation"]):
        raise PreprocessError("동적 정렬 anchor 상관 %.3f < 기준 %.3f"
                              % (min(corrs), cfg["minimum_correlation"]))
    local_curve = np.interp(x, centers, shifts, left=shifts[0], right=shifts[-1])
    aligned = np.interp(x + local_curve, x, stat, left=np.nan, right=np.nan)
    return aligned, {"static_shift": int(static), "static_correlation": static_corr,
                     "anchor_shifts": [int(v) for v in shifts],
                     "anchor_correlations": [float(v) for v in corrs]}


def _filter_design(sample_rate, target_clock, cfg):
    low = float(cfg["low_clock_multiplier"]) * target_clock
    high = float(cfg["high_clock_multiplier"]) * target_clock
    if not (0 < low < high < sample_rate / 2.0):
        raise PreprocessError("L4 band-pass %.3g–%.3g Hz가 Nyquist %.3g Hz 범위 밖이다"
                              % (low, high, sample_rate / 2.0))
    return butter(int(cfg["order"]), [low, high], btype="bandpass", fs=sample_rate,
                  output="sos"), low, high


def _copy_root(original, derived, spec, source_sha, contract_sha, payload, new_ns, pipeline):
    """수집 Metadata를 복사하고 원본 전용 필드를 제외한 파생 provenance를 기록한다."""
    raw_only = {"dataset_role", "capture_repeats", "capture_contract_sha256",
                "acquisition_status"}
    for key, value in original.attrs.items():
        if key not in raw_only:
            derived.attrs[key] = value
    derived.attrs["schema"] = S.SCHEMA
    derived.attrs["schema_version"] = S.SCHEMA_VERSION
    derived.attrs["dataset_role"] = "derived-analysis"
    derived.attrs["source_dataset_sha256"] = source_sha
    derived.attrs["source_capture_contract_sha256"] = str(
        original.attrs["capture_contract_sha256"])
    derived.attrs["derivation_contract_sha256"] = contract_sha
    derived.attrs["aggregation_kind"] = "mean"
    derived.attrs["aggregation_n"] = int(payload["aggregation_n"])
    derived.attrs["preprocessing_pipeline"] = pipeline
    derived.attrs["samples_per_trace"] = int(new_ns)
    derived.attrs["sample_dtype"] = "float64"
    derived.attrs["sample_scale"] = 1.0
    derived.attrs["alignment"] = spec["criteria"]["preprocessing"]["alignment"]
    if S.F_SAMPLE_MAP in original:
        original.copy(S.F_SAMPLE_MAP, derived)


def _new_derived_group(derived, name, raw, groups, ns):
    group = derived.create_group(name)
    for key, value in raw.attrs.items():
        group.attrs[key] = value
    group.attrs["n_records"] = int(groups)
    group.attrs["n_repeat_groups"] = int(groups)
    group.create_dataset(S.F_TRACE, shape=(groups, ns), dtype=np.float64,
                         chunks=(1, ns))
    repeats = int(raw.file.attrs["capture_repeats"])
    for field in (S.F_KEY, S.F_PLAINTEXT, S.F_CIPHERTEXT):
        group.create_dataset(field, data=raw[field][::repeats])
    group.create_dataset(S.F_REPEAT_GROUP_ID, data=np.arange(groups, dtype=np.uint64))
    return group


def prepare(dataset_path, spec):
    """1.3 원본에서 content-addressed 파생 Dataset을 만들거나 검증된 캐시를 반환한다."""
    source = Path(dataset_path).resolve()
    S.require_schema(source)
    attrs = S.root_attrs(source)
    if str(attrs.get("dataset_role")) != "raw-acquisition":
        raise PreprocessError("파생 입력은 Schema 1.3 raw-acquisition이어야 한다: %s" % source)
    identity = {
        "spec_id": spec["id"],
        "assessment_profile": spec["assessment_profile"],
        "iut_algorithm": spec["scope"]["security_function"],
        "iut_implementation": spec["iut"]["name"],
    }
    for key, expected in identity.items():
        if str(attrs.get(key, "")) != str(expected):
            raise PreprocessError("원본 %s=%r가 현재 명세 %r와 다르다"
                                  % (key, attrs.get(key), expected))
    source_sha = artifacts.sha256_file(source)
    contract_sha, contract_payload = artifacts.derivation_contract(source_sha, spec)
    out = artifacts.derived_path(spec["id"], contract_sha)
    provenance_path = out.with_suffix(".provenance.json")
    if out.is_file() or provenance_path.is_file():
        if out.is_file() and provenance_path.is_file():
            old = json.loads(provenance_path.read_text(encoding="utf-8"))
            if old.get("source_sha256") == source_sha and \
                    old.get("derivation_contract_sha256") == contract_sha and \
                    old.get("derived_sha256") == artifacts.sha256_file(out):
                S.require_schema(out)
                return out
        raise PreprocessError("기존 파생 캐시의 계약 또는 SHA-256이 다르다: %s" % out)

    repeats = int(attrs["capture_repeats"])
    source_scale = float(attrs["sample_scale"])
    if not np.isfinite(source_scale) or source_scale == 0:
        raise PreprocessError("원본 sample_scale은 유한한 0 아닌 값이어야 한다")
    if repeats != int(contract_payload["aggregation_n"]):
        raise PreprocessError("원본 반복 수 %d와 파생 평균 수 %d가 다르다"
                              % (repeats, contract_payload["aggregation_n"]))
    level4 = int(spec["criteria"]["security_level"]) == 4
    if level4 and str(attrs.get("channel_type")) != "power":
        raise PreprocessError("L4 필터·정렬은 power 채널에만 적용한다")

    pipeline = "mean-%d" % repeats
    sos = align_cfg = None
    margin = 0
    l4_evidence = None
    if level4:
        sample_rate = float(attrs.get("sample_rate_hz", 0))
        target_clock = float(attrs.get("target_clock_hz", 0))
        if sample_rate <= 0 or target_clock <= 0:
            raise PreprocessError("L4 필터에 실제 sample_rate_hz와 target_clock_hz가 필요하다")
        filt_cfg = spec["criteria"]["preprocessing"]["filter"]
        align_cfg = spec["criteria"]["preprocessing"]["dynamic_alignment"]
        sos, low, high = _filter_design(sample_rate, target_clock, filt_cfg)
        with h5py.File(source, "r") as original:
            if "spa_same" not in original:
                raise PreprocessError("L4 기준 Subset spa_same이 없다")
            reference_raw = (np.asarray(original["spa_same"][S.F_TRACE][0], dtype=np.float64) /
                             source_scale)
        reference = sosfiltfilt(sos, reference_raw)
        freq = np.fft.rfftfreq(reference.size, 1.0 / sample_rate)
        power = np.abs(np.fft.rfft(reference - reference.mean())) ** 2
        inband = (freq >= low) & (freq <= high)
        outband = ~inband & (freq > 0)
        floor = float(np.median(power[outband])) if np.any(outband) else 0.0
        peak = float(np.max(power[inband])) if np.any(inband) else 0.0
        prominence = 10.0 * np.log10(max(peak, np.finfo(float).tiny) /
                                     max(floor, np.finfo(float).tiny))
        if prominence < float(filt_cfg["minimum_inband_prominence_db"]):
            raise PreprocessError("교정 PSD prominence %.2f dB < 기준 %.2f dB"
                                  % (prominence, filt_cfg["minimum_inband_prominence_db"]))
        samples_per_cycle = sample_rate / target_clock
        margin = int(np.ceil((align_cfg["max_static_shift_cycles"] +
                              align_cfg["max_local_shift_cycles"]) * samples_per_cycle)) + 2
        if reference.size <= 2 * margin + 16:
            raise PreprocessError("파형이 L4 공통 crop에 너무 짧다")
        pipeline = ("4th-order Butterworth zero-phase band-pass; normalized xcorr static; "
                    "8-anchor dynamic linear interpolation; common-valid crop; mean-%d" % repeats)
        l4_evidence = {"sample_rate": sample_rate, "target_clock": target_clock,
                       "low": low, "high": high, "prominence": prominence,
                       "reference_raw": reference_raw, "reference": reference,
                       "frequency": freq, "power": power, "samples_per_cycle": samples_per_cycle}

    with h5py.File(source, "r") as original:
        ns = int(original.attrs["samples_per_trace"]) - 2 * margin
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            with h5py.File(out, "x") as derived:
                _copy_root(original, derived, spec, source_sha, contract_sha,
                           contract_payload, ns, pipeline)
                mapping_hash = hashlib.sha256()
                metrics = {}
                for name, raw in original.items():
                    if not isinstance(raw, h5py.Group):
                        continue
                    if raw[S.F_TRACE].shape[0] % repeats:
                        raise PreprocessError("/%s 원본 행이 완성 반복 묶음이 아니다" % name)
                    groups = raw[S.F_TRACE].shape[0] // repeats
                    group = _new_derived_group(derived, name, raw, groups, ns)
                    summary = {"records": groups, "repeats": repeats}
                    if level4:
                        summary.update(minimum_anchor_correlation=1.0,
                                       maximum_abs_static_shift=0,
                                       maximum_abs_local_shift=0)
                    for row in range(groups):
                        raw_rows = (np.asarray(
                            raw[S.F_TRACE][row * repeats:(row + 1) * repeats],
                            dtype=np.float64) / source_scale)
                        if not level4:
                            group[S.F_TRACE][row] = raw_rows.mean(axis=0)
                            continue
                        processed = np.empty((repeats, ns), dtype=np.float64)
                        for repeat in range(repeats):
                            filtered = sosfiltfilt(sos, raw_rows[repeat])
                            aligned, evidence = _align(
                                l4_evidence["reference"], filtered,
                                l4_evidence["samples_per_cycle"], align_cfg)
                            cropped = aligned[margin:-margin]
                            if not np.all(np.isfinite(cropped)):
                                raise PreprocessError("공통 crop 뒤 비유한 샘플이 남았다")
                            processed[repeat] = cropped
                            mapping_hash.update(json.dumps(evidence, sort_keys=True).encode("utf-8"))
                            summary["minimum_anchor_correlation"] = min(
                                summary["minimum_anchor_correlation"],
                                min(evidence["anchor_correlations"]))
                            summary["maximum_abs_static_shift"] = max(
                                summary["maximum_abs_static_shift"], abs(evidence["static_shift"]))
                            summary["maximum_abs_local_shift"] = max(
                                summary["maximum_abs_local_shift"],
                                max(abs(x) for x in evidence["anchor_shifts"]))
                        group[S.F_TRACE][row] = processed.mean(axis=0)
                    metrics[name] = summary
        except Exception:
            out.unlink(missing_ok=True)
            raise

    S.require_schema(out)
    run_dir = paths.run_dir(spec["id"], create=True)
    evidence_npz = None
    if l4_evidence:
        w, response = sosfreqz(sos, worN=2048, fs=l4_evidence["sample_rate"])
        evidence_npz = run_dir / "l4_preprocessing_evidence.npz"
        np.savez_compressed(
            evidence_npz, frequency_hz=l4_evidence["frequency"],
            calibration_power=l4_evidence["power"], response_frequency_hz=w,
            response_abs=np.abs(response), reference_before=l4_evidence["reference_raw"],
            reference_after=l4_evidence["reference"][margin:-margin])
    provenance = {
        "profile": spec["assessment_profile"], "source": str(source),
        "source_sha256": source_sha, "derived": str(out),
        "derived_sha256": artifacts.sha256_file(out),
        "derivation_contract_sha256": contract_sha,
        "contract": contract_payload, "pipeline": pipeline,
        "metrics": metrics,
        "alignment_mapping_sha256": mapping_hash.hexdigest() if l4_evidence else None,
        "evidence_npz": str(evidence_npz) if evidence_npz else None,
    }
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
