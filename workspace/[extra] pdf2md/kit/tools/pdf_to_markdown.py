#!/usr/bin/env python3
"""Deterministic born-digital PDF to Markdown sidecar converter.

This tool uses only Poppler pdftotext bbox coordinates and Python's standard
library. It never repairs, summarizes, translates, or invents source text.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import html
import json
import re
import subprocess
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path


XHTML = "http://www.w3.org/1999/xhtml"
NS = {"x": XHTML}
# Figure captions only (pixels omitted by policy). Table / Algorithm are text objects — not figures.
FIGURE_CAPTION_RE = re.compile(
    r"^(?:Fig(?:ure)?\.?\s*[\dA-Za-z().-]+|그림\s*[\dA-Za-z().-]+)\b",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(?:[IVXLCDM]+\.\s+|\d+(?:\.\d+)+\s+)")
SPECIAL_HEADINGS = {
    "요 약",
    "요약",
    "ABSTRACT",
    "REFERENCES",
    "References",
    "참고문헌",
}


@dataclasses.dataclass(frozen=True)
class Block:
    x0: float
    y0: float
    x1: float
    y1: float
    lines: tuple[str, ...]
    source_block_count: int
    word_count: int
    numeric_token_count: int

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def text(self) -> str:
        return " ".join(self.lines)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tool_version() -> str:
    proc = subprocess.run(
        ["pdftotext", "-v"],
        check=True,
        capture_output=True,
        text=True,
    )
    first = (proc.stderr or proc.stdout).splitlines()[0]
    return first.strip()


def raster_images_by_page(source: Path) -> dict[int, int]:
    """Optional diagnostic only — never stores pixels. Missing pdfimages → empty."""
    try:
        proc = subprocess.run(
            ["pdfimages", "-list", str(source)],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return {}
    if proc.returncode != 0:
        return {}
    counts: dict[int, int] = {}
    for line in proc.stdout.splitlines():
        fields = line.split()
        if fields and fields[0].isdigit():
            page = int(fields[0])
            counts[page] = counts.get(page, 0) + 1
    return counts


def pdfinfo_preflight(source: Path) -> dict[str, object]:
    """Confirm born-digital text layer expectations via pdfinfo (step 2a)."""
    proc = subprocess.run(
        ["pdfinfo", str(source)],
        check=True,
        capture_output=True,
        text=True,
    )
    info: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip().lower()] = value.strip()
    encrypted = (info.get("encrypted") or "").lower()
    if encrypted and not encrypted.startswith("no"):
        raise RuntimeError(f"Encrypted PDF is outside this profile: {encrypted}")
    pages_raw = info.get("pages")
    if not pages_raw or not pages_raw.isdigit():
        raise RuntimeError("pdfinfo did not report page count.")
    # Poppler may omit "optimized"; treat missing text-related clues as soft.
    return {
        "pages": int(pages_raw),
        "encrypted": info.get("encrypted", ""),
        "page_size": info.get("page size", ""),
        "pdf_version": info.get("pdf version", ""),
    }


_XML_ILLEGAL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufffe\uffff]")


def sanitize_poppler_bbox_xml(raw: str) -> str:
    """Strip characters illegal in XML 1.0 (Poppler sometimes emits them)."""
    return _XML_ILLEGAL.sub("", raw)


def parse_bbox(source: Path) -> tuple[list[tuple[float, list[Block]]], int, int]:
    with tempfile.TemporaryDirectory(prefix="pdf-md-") as temp_dir:
        bbox_path = Path(temp_dir) / "bbox.html"
        subprocess.run(
            ["pdftotext", "-bbox-layout", str(source), str(bbox_path)],
            check=True,
        )
        raw = bbox_path.read_text(encoding="utf-8", errors="replace")
        root = ET.fromstring(sanitize_poppler_bbox_xml(raw))

    pages: list[tuple[float, list[Block]]] = []
    total_words = 0
    total_numeric_tokens = 0
    for page in root.findall(".//x:page", NS):
        width = float(page.attrib["width"])
        blocks: list[Block] = []
        for node in page.findall(".//x:block", NS):
            lines: list[str] = []
            block_words = 0
            block_numeric_tokens = 0
            for line in node.findall("./x:line", NS):
                words = [
                    (word.text or "")
                    for word in line.findall("./x:word", NS)
                    if word.text
                ]
                if words:
                    lines.append(" ".join(words))
                    block_words += len(words)
                    block_numeric_tokens += sum(
                        1 for word in words if any(char.isdigit() for char in word)
                    )
            if not lines:
                continue
            blocks.append(
                Block(
                    x0=float(node.attrib["xMin"]),
                    y0=float(node.attrib["yMin"]),
                    x1=float(node.attrib["xMax"]),
                    y1=float(node.attrib["yMax"]),
                    lines=tuple(lines),
                    source_block_count=1,
                    word_count=block_words,
                    numeric_token_count=block_numeric_tokens,
                )
            )
            total_words += block_words
            total_numeric_tokens += block_numeric_tokens
        pages.append((width, blocks))
    return pages, total_words, total_numeric_tokens


def ordered_blocks(width: float, blocks: list[Block]) -> list[Block]:
    """Order two-column pages without interpreting their content."""
    midpoint = width / 2
    full: list[Block] = []
    side: list[Block] = []
    for block in blocks:
        spans_center = block.x0 < width * 0.42 and block.x1 > width * 0.58
        very_wide = (block.x1 - block.x0) > width * 0.78
        (full if spans_center or very_wide else side).append(block)

    full.sort(key=lambda item: (item.y0, item.x0))
    remaining = set(range(len(side)))
    result: list[Block] = []
    lower_y = float("-inf")

    def emit_band(upper_y: float) -> None:
        band = [
            index
            for index in remaining
            if lower_y <= side[index].cy < upper_y
        ]
        left = sorted(
            (side[index] for index in band if side[index].cx < midpoint),
            key=lambda item: (round(item.y0 / 2), item.x0),
        )
        right = sorted(
            (side[index] for index in band if side[index].cx >= midpoint),
            key=lambda item: (round(item.y0 / 2), item.x0),
        )
        result.extend(left)
        result.extend(right)
        remaining.difference_update(band)

    for separator in full:
        emit_band(separator.cy)
        result.append(separator)
        lower_y = separator.cy
    emit_band(float("inf"))

    if remaining:
        result.extend(sorted((side[index] for index in remaining), key=lambda b: (b.y0, b.x0)))
    return merge_inline_blocks(width, result)


def merge_inline_blocks(width: float, blocks: list[Block]) -> list[Block]:
    """Join split fragments on the same visual line without crossing columns."""
    if not blocks:
        return []
    midpoint = width / 2
    merged: list[Block] = [blocks[0]]
    for block in blocks[1:]:
        previous = merged[-1]
        same_half = (previous.cx < midpoint) == (block.cx < midpoint)
        aligned = abs(previous.y0 - block.y0) < 2 and abs(previous.y1 - block.y1) < 2
        adjacent = previous.x1 <= block.x0 and (block.x0 - previous.x1) < width * 0.08
        single_line = len(previous.lines) == 1 and len(block.lines) == 1
        if same_half and aligned and adjacent and single_line:
            merged[-1] = Block(
                x0=previous.x0,
                y0=min(previous.y0, block.y0),
                x1=block.x1,
                y1=max(previous.y1, block.y1),
                lines=(f"{previous.text} {block.text}",),
                source_block_count=(
                    previous.source_block_count + block.source_block_count
                ),
                word_count=previous.word_count + block.word_count,
                numeric_token_count=(
                    previous.numeric_token_count + block.numeric_token_count
                ),
            )
        else:
            merged.append(block)
    return merged


def format_source_block(block: Block) -> str:
    text = html.escape(block.text.strip(), quote=False)
    compact = re.sub(r"\s+", " ", text)
    if len(compact) <= 100 and compact in SPECIAL_HEADINGS:
        return f"### {compact}"
    if len(compact) <= 120 and HEADING_RE.match(compact):
        return f"### {compact}"
    return text


def page_issues(blocks: list[Block]) -> tuple[list[str], int]:
    """Issues that block verification. Figure pixels are omitted by policy — not an issue.

    Table / Algorithm text is preserved via the text layer; they are not treated as figures.
    Raster counts are diagnostic only (metadata), never conversion issues.
    """
    text = "\n".join(block.text for block in blocks)
    private_chars = sum(1 for char in text if unicodedata.category(char) == "Co")
    replacement_chars = text.count("\ufffd")
    issues: list[str] = []
    if private_chars or replacement_chars:
        issues.append(
            "GLYPH_MAPPING — 수식·기호 손상 가능성; "
            f"private-use={private_chars}, replacement={replacement_chars}"
        )
    return issues, private_chars + replacement_chars


def format_block_with_figure_policy(block: Block, page_number: int) -> list[str]:
    """Emit text blocks; for figure captions, keep caption + page cite (no image file)."""
    formatted = format_source_block(block)
    lines = [formatted, ""]
    compact = re.sub(r"\s+", " ", block.text.strip())
    if FIGURE_CAPTION_RE.match(compact):
        lines.extend(
            [
                f"> [FIGURE omitted — image not stored; caption/text above; "
                f"cite source PDF page {page_number}]",
                "",
            ]
        )
    return lines


def render_markdown(
    source: Path,
    source_rel: str,
    source_asset_id: str,
    derived_asset_id: str,
    conversion_date: str,
) -> tuple[str, dict[str, object]]:
    preflight = pdfinfo_preflight(source)
    pages, total_words, total_numeric_tokens = parse_bbox(source)
    if not pages or total_words == 0:
        raise RuntimeError("No text layer found; OCR is outside this conversion profile.")
    if len(pages) != preflight["pages"]:
        raise RuntimeError(
            "pdfinfo page count and bbox page count differ: "
            f"{preflight['pages']} vs {len(pages)}"
        )

    source_hash = sha256(source)
    version = tool_version()
    raster_images = raster_images_by_page(source)
    body: list[str] = []
    emitted_block_count = 0
    source_block_count = sum(len(blocks) for _, blocks in pages)
    consumed_source_blocks = 0
    consumed_words = 0
    consumed_numeric_tokens = 0
    issue_count = 0
    glyph_issue_chars = 0
    page_summaries: list[dict[str, object]] = []

    for page_number, (width, raw_blocks) in enumerate(pages, start=1):
        blocks = ordered_blocks(width, raw_blocks)
        page_raster_images = raster_images.get(page_number, 0)
        issues, glyph_chars = page_issues(blocks)
        issue_count += len(issues)
        glyph_issue_chars += glyph_chars
        emitted_block_count += len(blocks)
        consumed_source_blocks += sum(block.source_block_count for block in blocks)
        consumed_words += sum(block.word_count for block in blocks)
        consumed_numeric_tokens += sum(block.numeric_token_count for block in blocks)
        body.extend([f"<!-- PDF_PAGE: {page_number} -->", "", f"## PDF page {page_number}", ""])
        for issue in issues:
            body.extend([f"> CONVERSION-ISSUE: {issue}", ""])
        for block in blocks:
            body.extend(format_block_with_figure_policy(block, page_number))
        page_summaries.append(
            {
                "page": page_number,
                "blocks": len(blocks),
                "issues": len(issues),
                "raster_images": page_raster_images,
                "figure_captions": sum(
                    1
                    for b in blocks
                    if FIGURE_CAPTION_RE.match(re.sub(r"\s+", " ", b.text.strip()))
                ),
            }
        )

    verification = "partial" if issue_count else "verified"
    if consumed_source_blocks != source_block_count:
        raise RuntimeError("Block consumption validation failed.")
    if consumed_words != total_words:
        raise RuntimeError("Word consumption validation failed.")
    if consumed_numeric_tokens != total_numeric_tokens:
        raise RuntimeError("Numeric-token consumption validation failed.")
    metadata = {
        "converter": "kit/tools/pdf_to_markdown.py",
        "profile": "deterministic-bbox-v1",
        "figure_policy": "omit-pixels-keep-caption-and-pdf-page",
        "pdftotext": version,
        "pdfinfo_pages": preflight["pages"],
        "converted_at": conversion_date,
        "source_asset_id": source_asset_id,
        "derived_asset_id": derived_asset_id,
        "source_path": source_rel,
        "source_sha256": source_hash,
        "pages": len(pages),
        "bbox_words": total_words,
        "consumed_bbox_words": consumed_words,
        "numeric_tokens": total_numeric_tokens,
        "consumed_numeric_tokens": consumed_numeric_tokens,
        "source_blocks": source_block_count,
        "consumed_source_blocks": consumed_source_blocks,
        "emitted_blocks": emitted_block_count,
        "embedded_raster_images": sum(raster_images.values()),
        "images_stored": 0,
        "conversion_issues": issue_count,
        "glyph_issue_chars": glyph_issue_chars,
        "verification": verification,
    }
    metadata_lines = "\n".join(
        f"{key}: {json.dumps(value, ensure_ascii=False)}"
        for key, value in metadata.items()
    )
    title = source.stem
    markdown = (
        f"# {title}\n\n"
        "> 기계적 PDF 파생본입니다. **단일 PDF → 단일 MD**. "
        "그림(픽셀)은 저장하지 않으며, 캡션 등 텍스트 층 내용과 "
        "페이지 표식(PDF_PAGE) 및 figure-omission 표기로 source PDF 페이지를 가리킵니다. "
        "표·알고리즘 등 복사 가능 객체는 텍스트로 유지합니다. "
        "요약·교정·보완·해석·이미지 AI 분석을 포함하지 않습니다. "
        "최종 인용 기준은 source PDF 페이지입니다.\n\n"
        "<!-- PDF_TO_MARKDOWN_METADATA\n"
        f"{metadata_lines}\n"
        "-->\n\n"
        + "\n".join(body).rstrip()
        + "\n"
    )

    if markdown.count("<!-- PDF_PAGE:") != len(pages):
        raise RuntimeError("Page marker validation failed.")
    if source_hash not in markdown or source_rel not in markdown:
        raise RuntimeError("Provenance validation failed.")

    report: dict[str, object] = dict(metadata)
    report["page_summaries"] = page_summaries
    return markdown, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-asset-id", required=True)
    parser.add_argument("--derived-asset-id", required=True)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()

    if args.source.resolve() == args.output.resolve():
        raise SystemExit("Source and output must differ.")
    if args.source.suffix.lower() != ".pdf" or args.output.suffix.lower() != ".md":
        raise SystemExit("Expected a .pdf source and .md output.")
    if args.source.stem != args.output.stem:
        raise SystemExit("Source and output must use the same file stem.")

    source_rel = args.source.as_posix()
    output_rel = args.output.as_posix()
    if source_rel.startswith("/") or output_rel.startswith("/"):
        raise SystemExit("Use project-root-relative paths (no host absolute paths).")
    # Archive convention: Papers_pdf/**/*.pdf → Papers_md/**/*.md (same relative key).
    if source_rel.startswith("Papers_pdf/") and output_rel.startswith("Papers_md/"):
        src_key = source_rel[len("Papers_pdf/") : -len(".pdf")]
        out_key = output_rel[len("Papers_md/") : -len(".md")]
        if src_key != out_key:
            raise SystemExit(
                "Papers_pdf ↔ Papers_md paths must mirror: "
                f"expected Papers_md/{src_key}.md, got {output_rel}"
            )
    elif source_rel.startswith("Papers_pdf/") and not output_rel.startswith("Papers_md/"):
        # Temporary outputs (e.g. kit/.tmp) are allowed for re-runs.
        pass

    markdown, report = render_markdown(
        source=args.source,
        source_rel=source_rel,
        source_asset_id=args.source_asset_id,
        derived_asset_id=args.derived_asset_id,
        conversion_date=args.date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = args.output.with_suffix(args.output.suffix + ".tmp")
    temp_output.write_text(markdown, encoding="utf-8")
    temp_output.replace(args.output)
    report["output_path"] = args.output.as_posix()
    report["output_bytes"] = args.output.stat().st_size
    report["output_sha256"] = sha256(args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
