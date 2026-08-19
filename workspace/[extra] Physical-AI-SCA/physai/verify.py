"""증거 번들 검증 — 제3자가 결과를 믿을 수 있는지 기계적으로 확인한다.

    python3 -m physai.verify --run <spec-id>

검사 항목

1. `manifest.json` 이 있고 읽히는가
2. 목록의 모든 파일이 존재하고 **sha256 이 일치**하는가
3. Dataset(데이터셋)이 **여전히 `SCHEMA.md`를 지키는가**
4. 툴체인이 manifest 에 적힌 것과 같은가 (다르면 경고 — 결과가 달라질 수 있다)
5. spec 이 계약을 지키고, `results.json` 이 그 spec 을 가리키는가
6. 보고서 3종이 모두 있는가

**툴체인 불일치는 실패가 아니라 경고다.** 다른 버전에서 결과가 재현되는지는 실제로
다시 돌려 봐야 알 수 있고, 그것은 이 도구가 판단할 일이 아니다. 다만 조용히 넘어가면
"검증됨" 이라는 말이 거짓이 되므로 반드시 보고한다.

종료 코드 0 = 모든 필수 검사 통과.
"""

import argparse
import json
import sys

from . import artifacts, paths, report as report_mod, spec as spec_mod

import sca_schema as S          # noqa: E402

REQUIRED_DOCS = ("01_experiment_plan.md", "02_analysis_report.md",
                 "03_evidence_manifest.md", "01_experiment_plan.html",
                 "02_analysis_report.html", "03_evidence_manifest.html",
                 "results.json", "manifest.json")


def verify(run_id, study_path=None):
    """실행 ID의 증거 번들을 검증하고 문제·경고·확인 수를 사전으로 반환한다.

    파일 존재·크기·SHA-256, 보고서 구성, 명세 연결, Dataset 스키마를 검사한다. 툴체인
    차이는 재현 실패가 확인된 것이 아니므로 경고로 분리한다. 모든 파일은 읽기 전용이며,
    manifest가 없으면 다른 검사를 추측하지 않고 즉시 실패 결과를 반환한다.
    """
    out_dir = paths.run_dir(run_id)
    problems, warnings, checked = [], [], 0

    mpath = out_dir / "manifest.json"
    if not mpath.is_file():
        return {"ok": False, "run": run_id,
                "problems": ["manifest.json 이 없다: %s (report 를 먼저 돌린다)" % mpath],
                "warnings": [], "files_checked": 0}
    manifest = json.loads(mpath.read_text(encoding="utf-8"))

    # 1) 파일 존재와 해시
    for f in manifest["files"]:
        p = out_dir / f["path"]
        if not p.is_file():
            p = paths.PROJECT / f["path"]
        if not p.is_file():
            problems.append("파일 없음: %s" % f["path"])
            continue
        actual = artifacts.sha256_file(p)
        checked += 1
        if actual != f["sha256"]:
            problems.append("해시 불일치: %s\n      기록 %s\n      실제 %s"
                            % (f["path"], f["sha256"], actual))
        if p.stat().st_size != f["bytes"]:
            problems.append("크기 불일치: %s (기록 %d, 실제 %d)"
                            % (f["path"], f["bytes"], p.stat().st_size))

    # 2) 보고서 3종 + 계약 파일
    for name in REQUIRED_DOCS:
        if not (out_dir / name).is_file():
            problems.append("산출물 누락: %s" % name)

    # 3) spec 계약과 results 대응
    spec_path = paths.EXP / ("%s.yaml" % run_id)
    sp = None
    if study_path:
        try:
            sp = spec_mod.load_from_study(study_path, run_id)
        except Exception as e:
            problems.append("study/spec 계약 위반: %s" % e)
    elif not spec_path.is_file():
        problems.append("spec 이 없다: %s" % spec_path)
    else:
        try:
            sp = spec_mod.load(spec_path)
        except Exception as e:
            problems.append("spec 계약 위반: %s" % e)

    datasets = {}
    rpath = out_dir / "results.json"
    if rpath.is_file():
        results = json.loads(rpath.read_text(encoding="utf-8"))
        if results.get("spec_id") != run_id:
            problems.append("results.json 의 spec_id(%s) 가 run(%s) 과 다르다"
                            % (results.get("spec_id"), run_id))
        for role, key in (("raw-acquisition", "source_dataset"),
                          ("derived-analysis", "dataset")):
            if key not in results:
                problems.append("results.json에 %s 경로(%s)가 없다" % (role, key))
            else:
                datasets[role] = paths.Path(results[key])

    # 4) 불변 원본과 파생 분석 Dataset이 모두 존재하고 역할별 스키마를 지키는가
    if not datasets:
        problems.append("results.json이 없어 Dataset을 찾을 수 없다")
    for expected_role, ds in datasets.items():
        if not ds.is_file():
            problems.append("%s Dataset이 없다: %s" % (expected_role, ds))
            continue
        bad = S.validate_dataset(path=ds)
        if bad:
            problems.append("%s Dataset 스키마 위반 %d건: %s"
                            % (expected_role, len(bad), "; ".join(bad[:3])))
            continue
        actual_role = str(S.root_attrs(ds).get("dataset_role", ""))
        if actual_role != expected_role:
            problems.append("Dataset 역할 불일치: %s는 %s여야 하나 %s"
                            % (ds, expected_role, actual_role))

    # 5) 툴체인 (경고)
    now = report_mod._toolchain()
    for k, v in manifest.get("toolchain", {}).items():
        if now.get(k) != v:
            warnings.append("툴체인 다름: %s — 기록 %r, 현재 %r" % (k, v, now.get(k)))

    return {"ok": not problems, "run": run_id, "files_checked": checked,
            "problems": problems, "warnings": warnings,
            "datasets": {role: str(path) for role, path in datasets.items()}}


def main(argv=None):
    """증거 번들 검증 결과를 사람용 로그와 JSON으로 출력한다.

    `--quiet`이면 사람용 로그만 생략한다. 필수 검사가 모두 통과하면 0, 하나라도 실패하면
    1을 반환하며 증거 파일은 변경하지 않는다.
    """
    ap = argparse.ArgumentParser(prog="physai.verify")
    ap.add_argument("--run", required=True)
    ap.add_argument("--study", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    r = verify(a.run, a.study)
    if not a.quiet:
        print("=" * 66)
        print(" 증거 번들 검증 — %s" % a.run)
        print("=" * 66)
        print("  해시 대조한 파일: %d개" % r["files_checked"])
        for w in r["warnings"]:
            print("  [경고] %s" % w)
        for p in r["problems"]:
            print("  [실패] %s" % p)
        print("  결과: %s" % ("통과" if r["ok"] else "**실패**"))
        if r["warnings"] and r["ok"]:
            print("  (경고는 실패가 아니다. 다른 툴체인에서 결과가 재현되는지는 "
                  "실제로 다시 돌려 봐야 안다.)")
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
