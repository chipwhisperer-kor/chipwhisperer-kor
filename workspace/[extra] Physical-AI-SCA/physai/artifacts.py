"""불변 원본과 재생성 가능한 파생 Dataset의 경로·해시 계약.

경로명은 사람이 고른 시각이 아니라 계약 해시에서 유도한다. 원본 계약은 resolved spec과
실제 IUT 바이너리를, 파생 계약은 원본 파일 해시와 전처리 설정·구현 판번호를 묶는다.
이 모듈은 HDF5 내용을 해석하지 않으며 파일 해시와 작은 JSON manifest만 다룬다.
"""

import hashlib
import json
from pathlib import Path

from . import paths


DERIVATION_PIPELINE_VERSION = 1


def sha256_file(path):
    """파일을 1 MiB씩 읽어 SHA-256을 반환하며 파일을 변경하지 않는다."""
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value):
    """JSON으로 표현 가능한 값의 키 순서·공백과 무관한 SHA-256을 반환한다."""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def resolved_spec_payload(spec):
    """로더가 붙인 설치경로 주석을 제외한 수집 계약용 resolved spec을 반환한다.

    ``_spec_path``와 ``_study_path``는 실행 편의를 위한 provenance이지 실험 조건이 아니다.
    이를 해시에 넣으면 같은 파일을 다른 clone 경로에서 실행했을 때 계약이 달라진다.
    """
    return {key: value for key, value in spec.items() if not str(key).startswith("_")}


def capture_contract(spec, binary_sha256):
    """수집 전에 고정되는 resolved spec과 실제 실행 바이너리의 계약을 만든다."""
    payload = {"schema_version": "1.3", "resolved_spec": resolved_spec_payload(spec),
               "binary_sha256": str(binary_sha256)}
    return canonical_hash(payload)


def raw_path(spec_id, contract_sha256):
    """한 수집 계약의 유일한 원본 경로를 반환한다. 디렉터리는 만들지 않는다."""
    return paths.TRACES / "raw" / spec_id / (contract_sha256 + ".h5")


def derivation_contract(source_sha256, spec):
    """원본·전처리 조건·구현 판번호에서 파생 캐시 계약과 payload를 반환한다."""
    payload = {
        "pipeline_version": DERIVATION_PIPELINE_VERSION,
        "source_dataset_sha256": str(source_sha256),
        "assessment_profile": spec["assessment_profile"],
        "preprocessing": spec["criteria"]["preprocessing"],
        "aggregation_kind": "mean",
        "aggregation_n": int(spec["criteria"]["preprocessing"]["average_n"]),
        "trace_dtype": "float64",
    }
    return canonical_hash(payload), payload


def derived_path(spec_id, contract_sha256):
    """한 파생 계약의 content-addressed HDF5 경로를 반환한다."""
    return paths.TRACES / "derived" / spec_id / (contract_sha256 + ".h5")


def _project_relative(path):
    path = Path(path).resolve()
    try:
        return str(path.relative_to(paths.PROJECT.resolve()))
    except ValueError:
        return str(path)


def capture_manifest_path(spec_id):
    return paths.run_dir(spec_id) / "capture_manifest.json"


def write_capture_manifest(spec, dataset, contract_sha256):
    """봉인된 원본을 가리키는 작은 manifest를 원자 교체 없이 최초 한 번 기록한다."""
    dataset = Path(dataset).resolve()
    manifest = {
        "schema_version": 1,
        "spec_id": spec["id"],
        "capture_contract_sha256": str(contract_sha256),
        "resolved_spec_sha256": canonical_hash(resolved_spec_payload(spec)),
        "dataset": _project_relative(dataset),
        "dataset_bytes": dataset.stat().st_size,
        "dataset_sha256": sha256_file(dataset),
    }
    path = capture_manifest_path(spec["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(manifest, ensure_ascii=False, indent=2)
    if path.is_file():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != manifest:
            raise RuntimeError("기존 capture manifest가 현재 봉인 원본과 다르다: %s" % path)
        return path
    path.write_text(encoded, encoding="utf-8")
    return path


def load_capture_manifest(spec_id, spec=None):
    """manifest·원본 SHA를 검증하고 선택적으로 현재 resolved spec과 대조한다."""
    path = capture_manifest_path(spec_id)
    if not path.is_file():
        raise FileNotFoundError("봉인 원본 manifest가 없다: %s" % path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if spec is not None:
        current = canonical_hash(resolved_spec_payload(spec))
        if manifest.get("resolved_spec_sha256") != current:
            raise RuntimeError("봉인 원본의 resolved spec이 현재 명세와 다르다. "
                               "기준을 바꿨다면 새 experiment id를 사용한다")
    dataset = Path(manifest["dataset"])
    if not dataset.is_absolute():
        dataset = paths.PROJECT / dataset
    if not dataset.is_file():
        raise FileNotFoundError("봉인 원본 Dataset이 없다: %s" % dataset)
    if dataset.stat().st_size != int(manifest["dataset_bytes"]) or \
            sha256_file(dataset) != manifest["dataset_sha256"]:
        raise RuntimeError("봉인 원본 크기 또는 SHA-256이 manifest와 다르다: %s" % dataset)
    return dataset.resolve(), manifest
