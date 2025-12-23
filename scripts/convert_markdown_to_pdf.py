#!/usr/bin/env python3
"""
Convert Markdown to Substack-optimized PDF with clean formatting.

Usage:
    python convert_markdown_to_pdf.py input.md [output.pdf]

Example:
    python convert_markdown_to_pdf.py chapter_one.md chapter_one.pdf

Options:
    --preserve-date   Preserve a date found in the markdown (front matter or inline); falls back to file mtime.
    --date DATE       Explicit publication date to use (YYYY-MM-DD, MM/DD/YYYY, or 'December 13, 2025').

Behavior:
    By default, this script uses the current date (the date of conversion) as the publication date. Use
    `--preserve-date` to keep a date embedded in the markdown, or `--date` to set an explicit date.

Requirements:
    pip install markdown weasyprint
"""

import argparse
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import markdown
from weasyprint import CSS, HTML

logger = logging.getLogger(__name__)


def convert_markdown_to_pdf(
    md_file_path: str,
    output_path: str = None,
    pub_date_dt: datetime | None = None,
):
    """Convert markdown file to Substack-friendly PDF with styling."""

    try:
        md_path = Path(md_file_path)
        if not md_path.exists():
            raise FileNotFoundError(f"File not found: {md_file_path}")

        # Read markdown
        with md_path.open(encoding="utf-8") as f:
            md_content = f.read()

        # Convert to HTML with extensions
        html_content = markdown.markdown(
            md_content,
            extensions=["extra", "codehilite", "toc", "tables"],
        )
        # Note: argparse is imported at top-level, not inside this function

        # Substack-optimized CSS
        css = CSS(
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

        h1 {
            font-size: 24pt;
            font-weight: 600;
            margin-top: 24pt;
            margin-bottom: 16pt;
            border-bottom: 2px solid #eaecef;
            padding-bottom: 8pt;
        }

        .substack-header .date {
            color: #6a737d;
            font-size: 9pt;
            margin-top: 4pt;
            margin-bottom: 12pt;
        }

        h2 {
            font-size: 18pt;
            font-weight: 600;
            margin-top: 20pt;
            margin-bottom: 12pt;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 6pt;
        }

        h3 {
            font-size: 14pt;
            font-weight: 600;
            margin-top: 16pt;
            margin-bottom: 10pt;
        }

        p {
            margin-top: 0;
            margin-bottom: 12pt;
        }

        code {
            background-color: #f6f8fa;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 10pt;
        }

        pre {
            background-color: #f6f8fa;
            padding: 12pt;
            border-radius: 6pt;
            overflow-x: auto;
            margin-bottom: 12pt;
        }

        pre code {
            background-color: transparent;
            padding: 0;
        }

        blockquote {
            border-left: 4pt solid #dfe2e5;
            padding-left: 12pt;
            margin-left: 0;
            color: #6a737d;
        }

        a {
            color: #0366d6;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        hr {
            border: none;
            border-top: 2px solid #eaecef;
            margin: 24pt 0;
        }

        ul, ol {
            margin-bottom: 12pt;
            padding-left: 24pt;
        }

        li {
            margin-bottom: 6pt;
        }

        table {
            border-collapse: collapse;
            margin-bottom: 12pt;
            width: 100%;
        }

        th, td {
            border: 1px solid #dfe2e5;
            padding: 8pt;
            text-align: left;
        }

        th {
            background-color: #f6f8fa;
            font-weight: 600;
        }

        strong {
            font-weight: 600;
        }

        em {
            font-style: italic;
        }
    """,
        )

        # Try to extract a publication or front matter date from the markdown
        def try_parse_date(date_text: str):
            """Try parsing a date from a string using a few common formats.

            Return a datetime.date or None if no parse succeded.
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
                    return datetime.strptime(date_text, fmt)
                except ValueError:
                    # Not matching this format, try next
                    pass
            # Last resort: try to parse a year and fallback to a month/day pattern
            m = re.search(r"(\d{4})", date_text)
            if m:
                # return Jan 1st of the year found if we can't be more specific
                return datetime(int(m.group(1)), 1, 1)
            return None

        def extract_date_from_markdown(md_text: str, path: Path):
            # YAML frontmatter first
            m = re.search(
                r"^---\s*(.*?)\s*---",
                md_text,
                flags=re.DOTALL | re.MULTILINE,
            )
            if m:
                front = m.group(1)
                # Look for date: in frontmatter
                fm = re.search(
                    r"^date\s*:\s*(.*)$",
                    front,
                    flags=re.MULTILINE | re.IGNORECASE,
                )
                if fm:
                    parsed = try_parse_date(fm.group(1))
                    if parsed:
                        return parsed

            # Inline patterns e.g., "Next chapter drops 12/20/25" or "November 12th, 2347"
            # We look for common numeric MM/DD/YY or YYYY-MM-DD first
            m2 = re.search(r"(\d{4}-\d{2}-\d{2})", md_text)
            if m2:
                parsed = try_parse_date(m2.group(1))
                if parsed:
                    return parsed

            m3 = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})", md_text)
            if m3:
                parsed = try_parse_date(m3.group(1))
                if parsed:
                    return parsed

            # Match Written dates like "November 12th, 2347" – strip ordinals
            m4 = re.search(
                r"\b([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4})\b",
                md_text,
            )
            if m4:
                dt_text = re.sub(r"(st|nd|rd|th)", "", m4.group(1))
                parsed = try_parse_date(dt_text)
                if parsed:
                    return parsed

            # Fallback to file last modified
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                return mtime
            except OSError:
                return None

        if pub_date_dt is None:
            pub_date_dt = extract_date_from_markdown(md_content, md_path)
        pub_date_str = None
        if pub_date_dt is not None:
            pub_date_str = pub_date_dt.strftime("%B %d, %Y")
        if pub_date_str:
            logger.info("Using publication date: %s", pub_date_str)
            date_html = f'<p class="date">Published: {pub_date_str}</p>'
        else:
            logger.info("No publication date found; continuing without date in header")
            date_html = ""

        # Wrap HTML with Substack-like structure
        full_html = (
            '\n<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8">\n'
            f"    <title>{md_path.stem.replace('_', ' ').title()}</title>\n</head>\n<body>\n"
            '    <div class="substack-header">\n'
            f"        <h1>{md_path.stem.replace('_', ' ').title()}</h1>\n"
            "        <p>By Angelo Hurley | LuminAI Codex</p>\n"
            f"        {date_html}\n"
            "    </div>\n"
            '    <div class="substack-body">\n'
            f"        {html_content}\n"
            "    </div>\n</body>\n</html>\n"
        )

        # Determine output path
        if output_path is None:
            output_path = md_path.with_suffix(".pdf")
        else:
            output_path = Path(output_path)

        # Convert to PDF
        HTML(string=full_html).write_pdf(output_path, stylesheets=[css])

        logger.info("PDF created: %s", output_path)
        logger.info("Size: %.1f KB", output_path.stat().st_size / 1024)
        return output_path

    except Exception as exc:
        logger.exception("Error converting markdown to PDF: %s", exc)
        logger.info("Troubleshooting tips:")
        logger.info("1. Install dependencies: pip install markdown weasyprint")
        logger.info("2. Check file permissions")
        logger.info("3. Try with a simple test file")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Convert a Markdown file to a Substack-styled PDF. By default the "
            "publication date will be the current date unless you pass --preserve-date or --date."
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
            "Accepts common formats (YYYY-MM-DD, MM/DD/YYYY, 'December 13, 2025', etc.)."
        ),
    )
    args = parser.parse_args()

    md_file = args.input
    output_file = args.output

    # Parse explicit date if provided
    pub_date_dt = None
    if args.date:

        def _try_parse_date_local(dt_text: str):
            dt_text = dt_text.strip()
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
                    return datetime.strptime(dt_text, fmt)
                except ValueError:
                    pass
            m = re.search(r"(\d{4})", dt_text)
            if m:
                return datetime(int(m.group(1)), 1, 1)
            return None

        pub_date_dt = _try_parse_date_local(args.date)
        if pub_date_dt is None:
            logger.warning(
                "Could not parse --date value '%s'. Using today's date instead.",
                args.date,
            )

    # If preserve-date was requested and no explicit date passed, set None so converter extracts date
    if args.preserve_date and pub_date_dt is None:
        pub_date_dt = None
    elif pub_date_dt is None:
        # Default: Use today's date
        pub_date_dt = datetime.now()

    convert_markdown_to_pdf(md_file, output_file, pub_date_dt)
