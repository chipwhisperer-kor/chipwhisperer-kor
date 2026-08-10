"""증거 번들 검증 — 제3자가 결과를 믿을 수 있는지 기계적으로 확인한다.

    python3 -m physai.verify --run <spec-id>

검사 항목

1. `manifest.json` 이 있고 읽히는가
2. 목록의 모든 파일이 존재하고 **sha256 이 일치**하는가
3. 데이터셋이 **여전히 `SCHEMA.md` 를 지키는가**
4. 툴체인이 manifest 에 적힌 것과 같은가 (다르면 경고 — 결과가 달라질 수 있다)
5. spec 이 계약을 지키고, `results.json` 이 그 spec 을 가리키는가
6. 보고서 3종이 모두 있는가

**툴체인 불일치는 실패가 아니라 경고다.** 다른 버전에서 결과가 재현되는지는 실제로
다시 돌려 봐야 알 수 있고, 그것은 이 도구가 판단할 일이 아니다. 다만 조용히 넘어가면
"검증됨" 이라는 말이 거짓이 되므로 반드시 보고한다.

종료 코드 0 = 모든 필수 검사 통과.
"""

import argparse
import hashlib
import json
import sys

from . import paths, report as report_mod, spec as spec_mod

import sca_schema as S          # noqa: E402

REQUIRED_DOCS = ("01_experiment_plan.md", "02_analysis_report.md",
                 "03_evidence_manifest.md", "results.json", "manifest.json")


def _sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(run_id):
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
        actual = _sha256(p)
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
    if not spec_path.is_file():
        problems.append("spec 이 없다: %s" % spec_path)
    else:
        try:
            sp = spec_mod.load(spec_path)
        except Exception as e:
            problems.append("spec 계약 위반: %s" % e)

    ds = None
    rpath = out_dir / "results.json"
    if rpath.is_file():
        results = json.loads(rpath.read_text(encoding="utf-8"))
        if results.get("spec_id") != run_id:
            problems.append("results.json 의 spec_id(%s) 가 run(%s) 과 다르다"
                            % (results.get("spec_id"), run_id))
        ds = paths.Path(results["dataset"])

    # 4) 데이터셋이 여전히 스키마를 지키는가
    if ds is None:
        problems.append("results.json 이 없어 데이터셋을 찾을 수 없다")
    elif not ds.is_file():
        problems.append("데이터셋이 없다: %s (용량 때문에 커밋하지 않는다 — "
                        "재현하려면 collect 를 다시 돌린다)" % ds)
    else:
        bad = S.validate_dataset(path=ds)
        if bad:
            problems.append("데이터셋 스키마 위반 %d건: %s" % (len(bad), "; ".join(bad[:3])))

    # 5) 툴체인 (경고)
    now = report_mod._toolchain()
    for k, v in manifest.get("toolchain", {}).items():
        if now.get(k) != v:
            warnings.append("툴체인 다름: %s — 기록 %r, 현재 %r" % (k, v, now.get(k)))

    return {"ok": not problems, "run": run_id, "files_checked": checked,
            "problems": problems, "warnings": warnings,
            "dataset": str(ds) if ds else None}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="physai.verify")
    ap.add_argument("--run", required=True)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    r = verify(a.run)
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
