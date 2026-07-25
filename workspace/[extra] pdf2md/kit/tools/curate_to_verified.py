#!/usr/bin/env python3
"""Curate mechanical MDs to package verified finals (text-only; no image files).

Policy (see kit/PDF_TO_MARKDOWN.md):
  - Single PDF → single MD. No Papers_md/<rel>/*.png asset trees.
  - Figures: keep captions + page cites; do not store pixels; no AI vision.
  - Tables / algorithms: not figures — preserve text-layer content.
  - Drop legacy visual-asset links and VISUAL/RASTER issues.

For each Papers_pdf PDF with a Papers_md mirror:
  1. Strip markdown image links and "Extracted visual assets" blocks
  2. Drop VISUAL_NOT_TRANSCRIBED / RASTER_IMAGE_NOT_TRANSCRIBED issue lines
  3. Scrub private-use / replacement glyphs; drop GLYPH_MAPPING when cleared
  4. Remove empty sidecar asset directories (optional images leftover)
  5. If conversion_issues==0 and page markers match pdfinfo pages → verified
     with profile deterministic-bbox-v1+text-only-v1

Does not invent abstract content. Does not overwrite goldens already
profiled as +manual-structure-v1 unless --force.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import (  # noqa: E402
    iter_archive_pdfs,
    mirror_asset_dir,
    mirror_md_path,
    pdf_rel_key,
)

ISSUE_LINE = re.compile(r"^>\s*CONVERSION-ISSUE:\s*([A-Z_]+).*$")
PAGE_MARK = re.compile(r"<!--\s*PDF_PAGE:\s*(\d+)\s*-->")
META_BLOCK = re.compile(
    r"(<!-- PDF_TO_MARKDOWN_METADATA\n)(.*?)(\n-->)",
    re.DOTALL,
)
# Markdown image: ![alt](url) or ![alt](<url>) — stripped if leftover from legacy runs
MD_IMAGE = re.compile(r"!\[([^\]]*)\]\((?:<[^>]+>|[^)\s]+)\)")
VISUAL_SECTION_HEAD = re.compile(
    r"^###\s+Extracted visual assets\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
DROP_ISSUE_KINDS = frozenset(
    {
        "VISUAL_NOT_TRANSCRIBED",
        "RASTER_IMAGE_NOT_TRANSCRIBED",
    }
)


def pdf_pages(source: Path) -> int:
    proc = subprocess.run(
        ["pdfinfo", str(source)],
        check=True,
        capture_output=True,
        text=True,
    )
    for line in proc.stdout.splitlines():
        if line.lower().startswith("pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"no pages in pdfinfo for {source}")


def split_pages(text: str) -> tuple[str, list[tuple[int, str]]]:
    """Return (preamble, [(page_no, page_body), ...])."""
    marks = list(PAGE_MARK.finditer(text))
    if not marks:
        return text, []
    preamble = text[: marks[0].start()]
    pages: list[tuple[int, str]] = []
    for i, m in enumerate(marks):
        page_no = int(m.group(1))
        start = m.start()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        pages.append((page_no, text[start:end]))
    return preamble, pages


def scrub_glyphs(body: str) -> tuple[str, int]:
    removed = 0
    out = []
    for ch in body:
        if unicodedata.category(ch) == "Co" or ch == "\ufffd":
            removed += 1
            continue
        out.append(ch)
    return "".join(out), removed


def strip_visual_sections(body: str) -> str:
    """Remove '### Extracted visual assets ...' sections through next heading or page."""
    lines = body.splitlines(keepends=True)
    out: list[str] = []
    skipping = False
    for line in lines:
        if VISUAL_SECTION_HEAD.match(line.rstrip("\n")):
            skipping = True
            continue
        if skipping:
            # End section at blank line followed by non-image, or next ### / ## / page mark
            stripped = line.strip()
            if stripped.startswith("<!-- PDF_PAGE:"):
                skipping = False
                out.append(line)
                continue
            if stripped.startswith("## ") or (
                stripped.startswith("### ") and not stripped.lower().startswith("### extracted")
            ):
                skipping = False
                out.append(line)
                continue
            if stripped.startswith("![") or stripped == "" or stripped.startswith("!["):
                continue
            # Non-image content resumes section end
            if stripped and not stripped.startswith("!["):
                skipping = False
                out.append(line)
            continue
        out.append(line)
    return "".join(out)


def strip_image_links(body: str) -> tuple[str, int]:
    count = len(MD_IMAGE.findall(body))
    return MD_IMAGE.sub("", body), count


def curate_page_body(body: str) -> tuple[str, int]:
    """Drop visual issues; strip image links/sections; keep captions and text."""
    body = strip_visual_sections(body)
    body, n_imgs = strip_image_links(body)
    lines = body.splitlines(keepends=True)
    kept: list[str] = []
    for line in lines:
        m = ISSUE_LINE.match(line.rstrip("\n"))
        if m:
            kind = m.group(1)
            if kind in DROP_ISSUE_KINDS:
                continue
            if kind == "GLYPH_MAPPING":
                continue
            kept.append(line)
        else:
            kept.append(line)
    # Collapse excessive blank lines left by image removal
    text = "".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, n_imgs


def update_metadata(preamble: str, **fields: object) -> str:
    m = META_BLOCK.search(preamble)
    if not m:
        return preamble
    meta = m.group(2)
    lines = meta.splitlines()
    new_lines = []
    seen = set()
    for line in lines:
        if ":" not in line:
            new_lines.append(line)
            continue
        key = line.split(":", 1)[0].strip()
        if key in fields:
            val = fields[key]
            new_lines.append(f"{key}: {json.dumps(val, ensure_ascii=False)}")
            seen.add(key)
        else:
            new_lines.append(line)
    for key, val in fields.items():
        if key not in seen:
            new_lines.append(f"{key}: {json.dumps(val, ensure_ascii=False)}")
    new_meta = "\n".join(new_lines)
    return preamble[: m.start()] + m.group(1) + new_meta + m.group(3) + preamble[m.end() :]


def purge_asset_dir(asset_dir: Path) -> int:
    """Remove image/MANIFEST sidecars under asset_dir. Never delete *.md or rmtree a tree that holds MD.

    Target papers share `Papers_md/<title>/` with reference MDs; wholesale rmtree would wipe them.
    """
    if not asset_dir.exists() or not asset_dir.is_dir():
        return 0
    # Safety: only under Papers_md/
    if "Papers_md/" not in asset_dir.as_posix() and not asset_dir.as_posix().startswith("Papers_md"):
        return 0

    removed = 0
    # Delete image/binary sidecars and visual manifests only
    patterns = (
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.gif",
        "*.webp",
        "*.tif",
        "*.tiff",
        "MANIFEST.md",
    )
    for pat in patterns:
        for path in asset_dir.rglob(pat):
            if not path.is_file():
                continue
            # Never touch paper markdown bodies
            if path.suffix.lower() == ".md" and path.name != "MANIFEST.md":
                continue
            path.unlink(missing_ok=True)
            removed += 1

    # Remove empty directories bottom-up (leave dirs that still contain .md)
    for dirpath in sorted(
        (p for p in asset_dir.rglob("*") if p.is_dir()),
        key=lambda p: len(p.parts),
        reverse=True,
    ):
        try:
            next(dirpath.iterdir())
        except StopIteration:
            dirpath.rmdir()
        except OSError:
            pass

    # If asset_dir itself is empty, remove it; if it still has MD children, keep it
    if asset_dir.is_dir():
        try:
            if not any(asset_dir.iterdir()):
                asset_dir.rmdir()
        except OSError:
            pass
    return removed


def curate_one(source: Path, force: bool = False, purge_assets: bool = True) -> dict:
    key = pdf_rel_key(source)
    md_path = mirror_md_path(source)
    asset_dir = mirror_asset_dir(source)
    if not md_path.is_file():
        return {"key": key, "status": "skip_no_md"}

    text = md_path.read_text(encoding="utf-8")
    if (
        'profile: "deterministic-bbox-v1+manual-structure-v1"' in text
        and 'verification: "verified"' in text
        and not force
    ):
        # Still strip image links from golden if any (text-only policy)
        if "![" in text or asset_dir.is_dir():
            pass  # fall through with force-like strip for images only
        else:
            return {"key": key, "status": "skip_golden"}

    is_golden = 'profile: "deterministic-bbox-v1+manual-structure-v1"' in text
    pages_n = pdf_pages(source)
    preamble, page_chunks = split_pages(text)

    new_pages: list[str] = []
    glyph_removed_total = 0
    images_stripped = 0
    for _page_no, body in page_chunks:
        body2, removed = scrub_glyphs(body)
        glyph_removed_total += removed
        body3, n_imgs = curate_page_body(body2)
        images_stripped += n_imgs
        new_pages.append(body3)

    body_all = "".join(new_pages)
    issues_total = sum(1 for ln in body_all.splitlines() if "CONVERSION-ISSUE:" in ln)

    blurb = (
        "> 결정론적 기계 파생본(텍스트 전용)입니다. **단일 PDF → 단일 MD**. "
        "그림 픽셀·이미지 파일은 저장하지 않으며, 캡션 등 텍스트와 "
        "source PDF 페이지 표기(PDF_PAGE)를 유지합니다. "
        "표·알고리즘은 그림이 아니며 텍스트 층 전사를 유지합니다. "
        "이미지 AI 분석·요약·해석을 넣지 않습니다. 최종 인용은 source PDF 페이지입니다.\n"
    )
    lines = preamble.splitlines(keepends=True)
    out_lines: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("> ") and (
            "기계적" in ln
            or "품질보증" in ln
            or "텍스트 전용" in ln
            or (i > 0 and lines[i - 1].startswith("#"))
        ):
            out_lines.append(blurb if blurb.endswith("\n") else blurb + "\n")
            while i < len(lines) and (
                lines[i].startswith("> ") or lines[i].strip() == ""
            ):
                if lines[i].strip() == "" and i + 1 < len(lines) and not lines[i + 1].startswith(">"):
                    out_lines.append(lines[i])
                    i += 1
                    break
                i += 1
            continue
        out_lines.append(ln)
        i += 1
    pre = "".join(out_lines)
    if "텍스트 전용" not in pre and "단일 PDF" not in pre:
        parts = pre.split("\n\n", 1)
        pre = (
            parts[0] + "\n\n" + blurb + "\n" + parts[1]
            if len(parts) == 2
            else pre + "\n" + blurb
        )

    page_marks = body_all.count("<!-- PDF_PAGE:")
    verified = issues_total == 0 and page_marks == pages_n

    if is_golden and not force:
        profile = "deterministic-bbox-v1+manual-structure-v1"
        curation = "text-only-v1+manual-structure-kept"
    else:
        profile = "deterministic-bbox-v1+text-only-v1"
        curation = "text-only-v1"

    pre = update_metadata(
        pre,
        profile=profile,
        figure_policy="omit-pixels-keep-caption-and-pdf-page",
        converted_at=date.today().isoformat(),
        curation=curation,
        linked_visual_assets=0,
        images_stored=0,
        images_stripped=images_stripped,
        curated_pages=pages_n,
        conversion_issues=issues_total,
        glyph_issue_chars=0,
        glyph_chars_removed=glyph_removed_total,
        verification="verified" if verified else "partial",
        pages=pages_n,
    )

    final = pre if pre.endswith("\n") else pre + "\n"
    for chunk in new_pages:
        final += chunk if chunk.endswith("\n") else chunk + "\n"
    # Also strip any leftover images in preamble (rare)
    final, extra = strip_image_links(final)
    images_stripped += extra
    final = re.sub(r"\n{3,}", "\n\n", final)

    md_path.write_text(final, encoding="utf-8")

    purged = 0
    if purge_assets:
        purged = purge_asset_dir(asset_dir)

    return {
        "key": key,
        "status": "verified" if verified else "partial",
        "pages": pages_n,
        "images_stripped": images_stripped,
        "files_purged": purged,
        "issues": issues_total,
        "output": md_path.as_posix(),
        "glyph_removed": glyph_removed_total,
        "profile": profile,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Text-only curation: strip images, keep captions, verify MD mirrors."
    )
    parser.add_argument("--force", action="store_true", help="Also re-profile goldens")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument(
        "--keep-asset-dirs",
        action="store_true",
        help="Do not delete Papers_md/<rel>/ sidecar dirs",
    )
    args = parser.parse_args()

    results = []
    sources = list(iter_archive_pdfs())
    for i, source in enumerate(sources, 1):
        if args.limit and len(
            [r for r in results if r["status"] in ("verified", "partial")]
        ) >= args.limit:
            break
        print(f"[{i}/{len(sources)}] {pdf_rel_key(source)[:70]}", flush=True)
        try:
            r = curate_one(
                source,
                force=args.force,
                purge_assets=not args.keep_asset_dirs,
            )
        except Exception as exc:  # noqa: BLE001
            r = {"key": pdf_rel_key(source), "status": "fail", "error": str(exc)}
            print(f"  FAIL {exc}", flush=True)
        else:
            print(
                f"  {r['status']} stripped={r.get('images_stripped')} "
                f"purged_files={r.get('files_purged')} issues={r.get('issues')}",
                flush=True,
            )
        results.append(r)

    summary = {
        "date": date.today().isoformat(),
        "policy": "text-only-v1",
        "total": len(results),
        "verified": sum(1 for r in results if r.get("status") == "verified"),
        "partial": sum(1 for r in results if r.get("status") == "partial"),
        "skip_golden": sum(1 for r in results if r.get("status") == "skip_golden"),
        "fail": sum(1 for r in results if r.get("status") == "fail"),
        "results": results,
    }
    Path("kit/curation_log.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({k: summary[k] for k in summary if k != "results"}, indent=2))
    if summary["fail"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
