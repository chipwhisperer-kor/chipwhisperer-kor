#!/usr/bin/env python3
"""List all conversion sources under Papers_pdf (*.pdf only) and md coverage.

Non-PDF files are excluded by design (they must not enter conversion or gap context).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import iter_archive_pdfs, queue_entry, require_root_relative


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventory Papers_pdf/**/*.pdf conversion queue."
    )
    parser.add_argument(
        "--papers-pdf",
        type=Path,
        default=Path("Papers_pdf"),
        help="Archive root (project-root-relative).",
    )
    parser.add_argument(
        "--pending-only",
        action="store_true",
        help="Only PDFs without mirrored Papers_md output.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON (default: human table).",
    )
    args = parser.parse_args()
    require_root_relative(args.papers_pdf)

    entries = [queue_entry(p) for p in iter_archive_pdfs(args.papers_pdf)]
    if args.pending_only:
        entries = [e for e in entries if not e["md_exists"]]

    summary = {
        "papers_pdf": args.papers_pdf.as_posix(),
        "total_pdf": len(list(iter_archive_pdfs(args.papers_pdf))),
        "listed": len(entries),
        "with_md": sum(1 for e in entries if e["md_exists"]),
        "pending": sum(1 for e in entries if not e["md_exists"]),
        "entries": entries,
    }

    if args.json:
        # recompute totals on full set for clarity
        all_entries = [queue_entry(p) for p in iter_archive_pdfs(args.papers_pdf)]
        summary["total_pdf"] = len(all_entries)
        summary["with_md"] = sum(1 for e in all_entries if e["md_exists"])
        summary["pending"] = sum(1 for e in all_entries if not e["md_exists"])
        if args.pending_only:
            summary["entries"] = [e for e in all_entries if not e["md_exists"]]
            summary["listed"] = len(summary["entries"])
        else:
            summary["entries"] = all_entries
            summary["listed"] = len(all_entries)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    all_entries = [queue_entry(p) for p in iter_archive_pdfs(args.papers_pdf)]
    pending_n = sum(1 for e in all_entries if not e["md_exists"])
    print(
        f"Papers_pdf PDFs: {len(all_entries)}  "
        f"with_md: {len(all_entries) - pending_n}  "
        f"pending: {pending_n}"
    )
    print("(non-PDF files under Papers_pdf are ignored)")
    print("")
    show = [e for e in all_entries if not e["md_exists"]] if args.pending_only else all_entries
    for e in show:
        flag = "DONE" if e["md_exists"] else "PENDING"
        print(f"[{flag}] {e['source']}")
        print(f"        -> {e['output_md']}")


if __name__ == "__main__":
    main()
