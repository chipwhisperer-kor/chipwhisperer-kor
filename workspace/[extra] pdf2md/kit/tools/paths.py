#!/usr/bin/env python3
"""Package-root path helpers for Papers_pdf ↔ Papers_md mirroring.

All paths are project-root-relative POSIX strings. Absolute host paths are rejected.
Only ``.pdf`` under ``Papers_pdf/`` are conversion sources; non-PDF files are ignored.
"""

from __future__ import annotations

from pathlib import Path


PAPERS_PDF = "Papers_pdf"
PAPERS_MD = "Papers_md"


def require_root_relative(path: Path) -> str:
    text = path.as_posix()
    if text.startswith("/"):
        raise SystemExit("Use project-root-relative paths (no host absolute paths).")
    return text


def under_papers_pdf(source: Path) -> bool:
    return source.as_posix().startswith(f"{PAPERS_PDF}/") or source.as_posix() == PAPERS_PDF


def pdf_rel_key(source: Path) -> str:
    """Stable key for a PDF: path under Papers_pdf without .pdf, else stem.

    Examples:
      Papers_pdf/Foo.pdf -> Foo
      Papers_pdf/Foo/[1] Bar.pdf -> Foo/[1] Bar
    """
    rel = require_root_relative(source)
    if rel.startswith(f"{PAPERS_PDF}/"):
        body = rel[len(PAPERS_PDF) + 1 :]
        if body.lower().endswith(".pdf"):
            body = body[: -len(".pdf")]
        return body
    return source.stem


def mirror_md_path(source: Path) -> Path:
    """Papers_pdf/<rel>.pdf → Papers_md/<rel>.md"""
    key = pdf_rel_key(source)
    if not under_papers_pdf(source) and source.suffix.lower() == ".pdf":
        # allow temp non-archive paths: same directory policy not enforced
        return Path(f"{PAPERS_MD}/{source.stem}.md")
    return Path(f"{PAPERS_MD}/{key}.md")


def mirror_asset_dir(source: Path) -> Path:
    """Legacy sidecar path next to mirrored md (path without .md).

    Text-only policy does **not** store images here. Kept for purge/cleanup of
    old visual-assets trees and queue_entry diagnostics only.
    """
    md = mirror_md_path(source)
    return md.with_suffix("")


def iter_archive_pdfs(papers_pdf: Path = Path(PAPERS_PDF)) -> list[Path]:
    """All conversion sources: every ``*.pdf`` under Papers_pdf (recursive).

    Non-PDF files (README.md, csv, …) are never returned.
    """
    if not papers_pdf.is_dir():
        return []
    return sorted(
        p
        for p in papers_pdf.rglob("*.pdf")
        if p.is_file() and p.suffix.lower() == ".pdf"
    )


def queue_entry(source: Path) -> dict:
    """Describe one archive PDF and whether its mirrored md exists."""
    rel = require_root_relative(source)
    md = mirror_md_path(source)
    return {
        "source": rel,
        "key": pdf_rel_key(source),
        "output_md": md.as_posix(),
        "md_exists": md.is_file(),
        "bytes": source.stat().st_size if source.is_file() else None,
    }
