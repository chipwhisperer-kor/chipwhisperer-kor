#!/usr/bin/env python3
"""Cross-check canonical Markdown against classic candidate extracts (step 3B).

Produces kit/candidates/<stem>/CROSSCHECK.md with review hints only.
Does not merge bodies, does not call AI/OCR, does not mark verified.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from paths import pdf_rel_key, require_root_relative


PAGE_RE = re.compile(r"<!--\s*PDF_PAGE:\s*(\d+)\s*-->")
WS_RE = re.compile(r"\s+")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_pages(text: str) -> dict[int, str]:
    matches = list(PAGE_RE.finditer(text))
    if not matches:
        return {1: text}
    pages: dict[int, str] = {}
    for index, match in enumerate(matches):
        page_no = int(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages[page_no] = text[start:end]
    return pages


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "")  # soft hyphen
    text = WS_RE.sub(" ", text).strip().lower()
    return text


def tokenize_alnum(text: str) -> list[str]:
    return re.findall(r"[0-9A-Za-z\uac00-\ud7a3]+", normalize(text))


def numeric_tokens(text: str) -> list[str]:
    return NUM_RE.findall(text)


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 1.0


def page_hints(canonical: str, candidate: str) -> list[str]:
    hints: list[str] = []
    c_tokens = set(tokenize_alnum(canonical))
    k_tokens = set(tokenize_alnum(candidate))
    sim = jaccard(c_tokens, k_tokens)
    if sim < 0.55:
        hints.append(
            f"low token overlap vs canonical (jaccard={sim:.2f}); "
            "check column order or missing blocks"
        )
    c_nums = set(numeric_tokens(canonical))
    k_nums = set(numeric_tokens(candidate))
    only_c = sorted(c_nums - k_nums)
    only_k = sorted(k_nums - c_nums)
    if only_c[:12]:
        hints.append(
            "numeric tokens in canonical not in candidate (sample): "
            + ", ".join(only_c[:12])
        )
    if only_k[:12]:
        hints.append(
            "numeric tokens in candidate not in canonical (sample): "
            + ", ".join(only_k[:12])
        )
    if "conversion-issue" in canonical.lower():
        # surface that human still owns issues on this page
        issue_lines = [
            line.strip()
            for line in canonical.splitlines()
            if "CONVERSION-ISSUE" in line
        ]
        if issue_lines:
            hints.append(
                f"canonical already has {len(issue_lines)} CONVERSION-ISSUE line(s)"
            )
    # Caption-like cues (avoid single Hangul syllables — too many false positives)
    cue_patterns = (
        r"\btable\s+\d",
        r"\bfig(?:ure)?\.?\s*\d",
        r"\balgorithm\s+\d",
        r"표\s*\d",
        r"그림\s*\d",
    )
    for pattern in cue_patterns:
        c_has = re.search(pattern, canonical, re.IGNORECASE) is not None
        k_has = re.search(pattern, candidate, re.IGNORECASE) is not None
        if c_has != k_has:
            hints.append(f"caption-like cue mismatch for /{pattern}/")
    return hints


def load_meta(tool_dir: Path) -> dict:
    meta_path = tool_dir / "META.json"
    if not meta_path.is_file():
        return {}
    return json.loads(meta_path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diff canonical md against candidate extracts (step 3B)."
    )
    parser.add_argument("--source", required=True, type=Path, help="Source PDF path")
    parser.add_argument(
        "--canonical",
        required=True,
        type=Path,
        help="Canonical or working Markdown (2a output; may be temp path)",
    )
    parser.add_argument(
        "--candidates-root",
        type=Path,
        default=Path("kit/candidates"),
    )
    args = parser.parse_args()

    require_root_relative(args.source)
    require_root_relative(args.canonical)
    require_root_relative(args.candidates_root)

    if not args.source.is_file():
        raise SystemExit("Source PDF not found.")
    if not args.canonical.is_file():
        raise SystemExit("Canonical Markdown not found.")

    rel_key = pdf_rel_key(args.source)
    cand_root = args.candidates_root / Path(rel_key)
    if not cand_root.is_dir():
        raise SystemExit(
            f"No candidates at {cand_root.as_posix()}; run run_candidates.py first."
        )

    canonical_text = args.canonical.read_text(encoding="utf-8")
    canonical_pages = split_pages(canonical_text)
    source_hash = sha256_file(args.source)

    tool_dirs = sorted(
        path
        for path in cand_root.iterdir()
        if path.is_dir() and (path / "extract.md").is_file()
    )
    if not tool_dirs:
        raise SystemExit("No successful candidate extract.md files found.")

    lines: list[str] = [
        f"# CROSSCHECK — `{rel_key}`",
        "",
        "Step **3B** machine cross-check. Hints only — do not treat as verified.",
        "Does not merge candidate text into the canonical body.",
        "",
        f"- source: `{args.source.as_posix()}`",
        f"- key: `{rel_key}`",
        f"- source_sha256: `{source_hash}`",
        f"- canonical: `{args.canonical.as_posix()}`",
        f"- canonical_sha256: `{sha256_file(args.canonical)}`",
        f"- generated_at: `{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        f"- profile: `classic-crosscheck-v1`",
        "",
        "## Summary",
        "",
    ]

    summary_rows: list[str] = [
        "| tool_id | status | pages compared | pages with hints |",
        "|---------|--------|----------------|------------------|",
    ]
    detail_sections: list[str] = []
    total_hint_pages = 0

    for tool_dir in tool_dirs:
        tool_id = tool_dir.name
        meta = load_meta(tool_dir)
        extract = (tool_dir / "extract.md").read_text(encoding="utf-8")
        cand_pages = split_pages(extract)
        page_nos = sorted(set(canonical_pages) | set(cand_pages))
        hinted = 0
        page_blocks: list[str] = []
        for page in page_nos:
            c_body = canonical_pages.get(page, "")
            k_body = cand_pages.get(page, "")
            if page not in canonical_pages:
                hints = ["page missing from canonical markers"]
            elif page not in cand_pages:
                hints = [
                    "page missing from candidate (no form-feed split or extract gap)"
                ]
            else:
                hints = page_hints(c_body, k_body)
            if not hints:
                continue
            hinted += 1
            page_blocks.append(f"### Page {page}")
            page_blocks.append("")
            for hint in hints:
                page_blocks.append(f"- REVIEW-HINT: {hint}")
            page_blocks.append("")
        total_hint_pages += hinted
        status = meta.get("status", "ok")
        summary_rows.append(
            f"| `{tool_id}` | {status} | {len(page_nos)} | {hinted} |"
        )
        detail_sections.append(f"## `{tool_id}`")
        detail_sections.append("")
        if meta:
            detail_sections.append(
                f"- tool_version: `{meta.get('tool_version')}`  "
            )
            detail_sections.append(
                f"- extract_sha256: `{meta.get('extract_sha256')}`  "
            )
            detail_sections.append("")
        if page_blocks:
            detail_sections.extend(page_blocks)
        else:
            detail_sections.append(
                "No automatic REVIEW-HINT for compared pages "
                "(still run step 4–5 against source PDF)."
            )
            detail_sections.append("")

    lines.extend(summary_rows)
    lines.extend(
        [
            "",
            f"Pages with at least one hint (sum over tools, not unique): "
            f"**{total_hint_pages}**",
            "",
            "## Next steps",
            "",
            "1. Promote useful hints to `CONVERSION-ISSUE` on the working Markdown (step 4).",
            "2. Resolve only by source PDF page comparison (step 5).",
            "3. Optional: Grok PDF assist for issue triage / page review "
            "(`kit/tools/GROK_REVIEW_PROMPTS.md`) — not for bulk rewrite.",
            "",
        ]
    )
    lines.extend(detail_sections)

    out_path = cand_root / "CROSSCHECK.md"
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    report = {
        "source_path": args.source.as_posix(),
        "canonical_path": args.canonical.as_posix(),
        "crosscheck_path": out_path.as_posix(),
        "tools_compared": [path.name for path in tool_dirs],
        "hint_page_events": total_hint_pages,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
