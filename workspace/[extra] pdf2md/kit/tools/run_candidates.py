#!/usr/bin/env python3
"""Run allowlist classic PDF text extractors as conversion candidates (step 2b).

No local OCR. No generative AI. Does not write the canonical Papers_md mirror.
See kit/TOOL_ALLOWLIST.md and kit/PDF_TO_MARKDOWN.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from paths import pdf_rel_key, require_root_relative


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_page_count(source: Path) -> int | None:
    if not shutil.which("pdfinfo"):
        return None
    proc = subprocess.run(
        ["pdfinfo", str(source)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    for line in proc.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def wrap_pages(text: str, page_count: int | None) -> str:
    """Split on form feeds when present; otherwise single blob with note."""
    parts = re.split(r"\f", text)
    # pdftotext often ends with a trailing empty part after final form feed
    while parts and parts[-1] == "":
        parts.pop()
    if len(parts) <= 1:
        body = text.strip("\n")
        header = (
            "<!-- candidate extract; page boundaries may be incomplete -->\n\n"
            "<!-- PDF_PAGE: 1 -->\n\n## PDF page 1\n\n"
        )
        if page_count and page_count > 1:
            header = (
                f"<!-- candidate extract; form-feed page split unavailable; "
                f"pdfinfo pages={page_count} -->\n\n"
                "<!-- PDF_PAGE: 1 -->\n\n## PDF page 1\n\n"
            )
        return header + body + "\n"

    lines: list[str] = [
        "<!-- candidate extract; pages split on form feed -->",
        "",
    ]
    for index, part in enumerate(parts, start=1):
        lines.extend(
            [
                f"<!-- PDF_PAGE: {index} -->",
                "",
                f"## PDF page {index}",
                "",
                part.strip("\n"),
                "",
            ]
        )
    if page_count is not None and page_count != len(parts):
        lines.extend(
            [
                f"> CROSSCHECK-NOTE: pdfinfo pages={page_count}, "
                f"form-feed parts={len(parts)}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def poppler_version() -> str | None:
    if not shutil.which("pdftotext"):
        return None
    proc = subprocess.run(
        ["pdftotext", "-v"],
        check=False,
        capture_output=True,
        text=True,
    )
    first = (proc.stderr or proc.stdout).splitlines()
    return first[0].strip() if first else None


def run_poppler(source: Path, mode: str) -> tuple[str, list[str], str | None]:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext not found")
    cmd = ["pdftotext"]
    if mode == "layout":
        cmd.append("-layout")
    cmd.extend([str(source), "-"])
    proc = subprocess.run(cmd, check=False, capture_output=True)
    if proc.returncode != 0:
        err = (proc.stderr or b"").decode("utf-8", errors="replace")
        raise RuntimeError(f"pdftotext failed: {err.strip()}")
    text = proc.stdout.decode("utf-8", errors="replace")
    return text, cmd, poppler_version()


def run_pymupdf(source: Path) -> tuple[str, list[str], str | None]:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pymupdf not installed") from exc
    version = getattr(fitz, "VersionBind", None) or getattr(fitz, "__doc__", "pymupdf")
    doc = fitz.open(source)
    try:
        chunks: list[str] = []
        for page in doc:
            # Text layer only — do not use OCR APIs.
            chunks.append(page.get_text("text"))
        text = "\f".join(chunks)
    finally:
        doc.close()
    return text, ["pymupdf", "page.get_text(text)", str(source)], str(version)


def run_pdfminer(source: Path) -> tuple[str, list[str], str | None]:
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        import pdfminer  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pdfminer.six not installed") from exc
    text = extract_text(str(source)) or ""
    version = getattr(pdfminer, "__version__", "pdfminer")
    return text, ["pdfminer.high_level.extract_text", str(source)], str(version)


EXTRACTORS = {
    "poppler-layout": lambda source: run_poppler(source, "layout"),
    "poppler-raw": lambda source: run_poppler(source, "raw"),
    "pymupdf-text": run_pymupdf,
    "pdfminer-text": run_pdfminer,
}


def write_candidate(
    out_dir: Path,
    tool_id: str,
    source_rel: str,
    source_hash: str,
    page_count: int | None,
    raw_text: str,
    command: list[str],
    tool_version: str | None,
    status: str,
    error: str | None = None,
) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    extract_path = out_dir / "extract.md"
    meta_path = out_dir / "META.json"
    payload: dict = {
        "tool_id": tool_id,
        "bucket": "A",
        "status": status,
        "source_path": source_rel,
        "source_sha256": source_hash,
        "pdfinfo_pages": page_count,
        "command": command,
        "tool_version": tool_version,
        "converted_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ocr": False,
        "profile": "classic-candidate-v1",
        "error": error,
    }
    if status == "ok":
        wrapped = wrap_pages(raw_text, page_count)
        data = wrapped.encode("utf-8")
        extract_path.write_bytes(data)
        payload["extract_path"] = extract_path.as_posix()
        payload["extract_bytes"] = len(data)
        payload["extract_sha256"] = sha256_bytes(data)
        payload["extract_chars"] = len(wrapped)
    else:
        if extract_path.exists():
            extract_path.unlink()
        payload["extract_path"] = None
    meta_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    payload["meta_path"] = meta_path.as_posix()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run classic allowlist PDF extractors (step 2b candidates)."
    )
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument(
        "--tools",
        default="all",
        help="Comma-separated tool_ids or 'all' (default).",
    )
    parser.add_argument(
        "--candidates-root",
        type=Path,
        default=Path("kit/candidates"),
        help="Root for candidate outputs (project-root-relative).",
    )
    args = parser.parse_args()

    source_rel = require_root_relative(args.source)
    candidates_root = args.candidates_root
    require_root_relative(candidates_root)

    if not args.source.is_file() or args.source.suffix.lower() != ".pdf":
        raise SystemExit("Source must be an existing .pdf path.")

    source_hash = sha256_file(args.source)
    page_count = pdf_page_count(args.source)
    rel_key = pdf_rel_key(args.source)

    if args.tools.strip().lower() == "all":
        tool_ids = list(EXTRACTORS.keys())
    else:
        tool_ids = [item.strip() for item in args.tools.split(",") if item.strip()]
        unknown = [item for item in tool_ids if item not in EXTRACTORS]
        if unknown:
            raise SystemExit(f"Unknown tool_id(s): {', '.join(unknown)}")

    reports: list[dict] = []
    for tool_id in tool_ids:
        out_dir = candidates_root / Path(rel_key) / tool_id
        try:
            raw_text, command, version = EXTRACTORS[tool_id](args.source)
            if not raw_text.strip():
                report = write_candidate(
                    out_dir,
                    tool_id,
                    source_rel,
                    source_hash,
                    page_count,
                    raw_text,
                    command,
                    version,
                    status="empty",
                    error="No text extracted (scan PDF or empty text layer?).",
                )
            else:
                report = write_candidate(
                    out_dir,
                    tool_id,
                    source_rel,
                    source_hash,
                    page_count,
                    raw_text,
                    command,
                    version,
                    status="ok",
                )
        except Exception as exc:  # noqa: BLE001 — per-tool skip is intentional
            report = write_candidate(
                out_dir,
                tool_id,
                source_rel,
                source_hash,
                page_count,
                "",
                [],
                None,
                status="skipped",
                error=str(exc),
            )
        reports.append(report)

    summary = {
        "source_path": source_rel,
        "source_sha256": source_hash,
        "key": rel_key,
        "stem": args.source.stem,
        "pdfinfo_pages": page_count,
        "candidates_root": candidates_root.as_posix(),
        "tools": reports,
        "ok": sum(1 for item in reports if item["status"] == "ok"),
        "skipped": sum(1 for item in reports if item["status"] != "ok"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["ok"] == 0:
        sys.exit(2)


if __name__ == "__main__":
    main()
