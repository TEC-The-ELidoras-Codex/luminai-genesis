#!/usr/bin/env python3
"""
Convert Markdown to Substack-optimized PDF with clean formatting.

Usage:
    python convert_markdown_to_pdf.py input.md [output.pdf]

Example:
    python convert_markdown_to_pdf.py chapter_one.md chapter_one.pdf

Options:
    --preserve-date   Preserve a date found in the markdown (front matter or inline);
                      falls back to file mtime.
    --date DATE       Explicit publication date to use (YYYY-MM-DD, MM/DD/YYYY, or
                      'December 13, 2025').

Behavior:
    By default, this script uses the current date (the date of conversion) as the
    publication date. Use `--preserve-date` to keep a date embedded in the markdown,
    or `--date` to set an explicit date.

Requirements:
    pip install markdown weasyprint
"""

import argparse
import logging
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import markdown
from weasyprint import CSS, HTML

logger = logging.getLogger(__name__)


# Date parsing helpers (extracted for testability and reduced complexity)
def try_parse_date(date_text: str) -> datetime | None:
    """Try parsing a date from a string using a few common formats.

    Returns a timezone-aware datetime (UTC) or None.
    """
    date_text = date_text.strip()
    fmt_candidates = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%B %d %Y",
        "%b %d %Y",
    ]
    for fmt in fmt_candidates:
        try:
            return datetime.strptime(date_text, fmt).replace(tzinfo=UTC)
        except ValueError:
            # Not matching this format, try next
            pass
    # Last resort: try to parse a year and fallback to Jan 1st of that year
    m = re.search(r"(\d{4})", date_text)
    if m:
        return datetime(int(m.group(1)), 1, 1, tzinfo=UTC)
    return None


def extract_frontmatter_date(md_text: str) -> datetime | None:
    m = re.search(r"^---\s*(.*?)\s*---", md_text, flags=re.DOTALL | re.MULTILINE)
    if not m:
        return None
    front = m.group(1)
    fm = re.search(r"^date\s*:\s*(.*)$", front, flags=re.MULTILINE | re.IGNORECASE)
    if not fm:
        return None
    return try_parse_date(fm.group(1))


def extract_iso_date(md_text: str) -> datetime | None:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", md_text)
    if not m:
        return None
    return try_parse_date(m.group(1))


def extract_numeric_date(md_text: str) -> datetime | None:
    m = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})", md_text)
    if not m:
        return None
    return try_parse_date(m.group(1))


def extract_written_date(md_text: str) -> datetime | None:
    m = re.search(r"\b([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4})\b", md_text)
    if not m:
        return None
    dt_text = re.sub(r"(st|nd|rd|th)", "", m.group(1))
    return try_parse_date(dt_text)


def extract_date_from_markdown(md_text: str, path: Path) -> datetime | None:
    """Extract a publication date from markdown content or fall back to file mtime."""
    # Frontmatter
    dt = extract_frontmatter_date(md_text)
    if dt:
        return dt
    # ISO
    dt = extract_iso_date(md_text)
    if dt:
        return dt
    # Numeric
    dt = extract_numeric_date(md_text)
    if dt:
        return dt
    # Written
    dt = extract_written_date(md_text)
    if dt:
        return dt
    # Fallback to file last modified (timezone-aware UTC)
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    except OSError:
        return None


def build_css() -> CSS:
    """Return Substack-optimized WeasyPrint CSS object."""
    return CSS(
        string="""
        @page {
            size: A4;
            margin: 2.5cm;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont,
                "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #24292e;
        }

        em {
            font-style: italic;
        }
    """,
    )


def format_pub_date_html(pub_date_dt: datetime | None) -> str:
    """Return rendered date header HTML (or empty string if no date)."""
    if pub_date_dt is None:
        logger.info("No publication date found; continuing without date in header")
        return ""
    pub_date_str = pub_date_dt.strftime("%B %d, %Y")
    logger.info("Using publication date: %s", pub_date_str)
    return f'<p class="date">Published: {pub_date_str}</p>'


def build_full_html(title: str, date_html: str, body_html: str) -> str:
    """Compose a full HTML document for the given pieces."""
    return (
        '\n<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8">\n'
        f"    <title>{title}</title>\n</head>\n<body>\n"
        '    <div class="substack-header">\n'
        f"        <h1>{title}</h1>\n"
        "        <p>By Angelo Hurley | LuminAI Codex</p>\n"
        f"        {date_html}\n"
        "    </div>\n"
        '    <div class="substack-body">\n'
        f"        {body_html}\n"
        "    </div>\n</body>\n</html>\n"
    )


def render_pdf(html: str, css: CSS, output_path: Path) -> None:
    """Render HTML to PDF using WeasyPrint (writes to `output_path`)."""
    HTML(string=html).write_pdf(output_path, stylesheets=[css])


def convert_markdown_to_pdf(
    md_file_path: str,
    output_path: str | None = None,
    pub_date_dt: datetime | None = None,
):
    """Convert markdown file to Substack-friendly PDF with styling."""

    try:
        md_path = Path(md_file_path)
        if not md_path.exists():
            msg = f"File not found: {md_file_path}"
            raise FileNotFoundError(msg)

        # Read markdown
        with md_path.open(encoding="utf-8") as f:
            md_content = f.read()

        # Convert to HTML with extensions
        html_content = markdown.markdown(
            md_content,
            extensions=["extra", "codehilite", "toc", "tables"],
        )
        # Note: argparse is imported at top-level, not inside this function

        css = build_css()

        # Try to extract a publication or front matter date from the markdown
        date_html = format_pub_date_html(pub_date_dt)

        # Wrap HTML with Substack-like structure
        title = md_path.stem.replace("_", " ").title()
        full_html = build_full_html(title, date_html, html_content)

        # Determine output path
        if output_path is None:
            output_path = md_path.with_suffix(".pdf")
        else:
            output_path = Path(output_path)

        # Convert to PDF
        render_pdf(full_html, css, output_path)

        logger.info("PDF created: %s", output_path)
        logger.info("Size: %.1f KB", output_path.stat().st_size / 1024)

    except (OSError, RuntimeError):
        logger.exception("Error converting markdown to PDF")
        logger.info("Troubleshooting tips:")
        logger.info("1. Install dependencies: pip install markdown weasyprint")
        logger.info("2. Check file permissions")
        logger.info("3. Try with a simple test file")
        sys.exit(1)

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Convert a Markdown file to a Substack-styled PDF. By default the "
            "publication date will be the current date unless you pass "
            "--preserve-date or --date."
        ),
    )
    parser.add_argument("input", help="Path to the input Markdown file")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Optional path for output PDF",
    )
    parser.add_argument(
        "--preserve-date",
        action="store_true",
        help=(
            "Preserve a date found in the markdown (front matter or inline). "
            "If not found, falls back to file mtime."
        ),
    )
    parser.add_argument(
        "--date",
        "-d",
        help=(
            "Explicit publication date to use instead of today's date. "
            "Accepts common formats (YYYY-MM-DD, MM/DD/YYYY, "
            "'December 13, 2025', etc.)."
        ),
    )
    args = parser.parse_args()

    md_file = args.input
    output_file = args.output

    # Parse explicit date if provided
    pub_date_dt = None
    if args.date:
        pub_date_dt = try_parse_date(args.date)
        if pub_date_dt is None:
            logger.warning(
                "Could not parse --date value '%s'. Using today's date instead.",
                args.date,
            )

    # If preserve-date was requested and no explicit date passed,
    # set None so converter extracts date
    if args.preserve_date and pub_date_dt is None:
        pub_date_dt = None
    elif pub_date_dt is None:
        # Default: Use today's date (UTC)
        pub_date_dt = datetime.now(tz=UTC)

    convert_markdown_to_pdf(md_file, output_file, pub_date_dt)
