#!/usr/bin/env python3
"""
Convert Markdown to PDF with clean formatting.

Usage:
    python scripts/convert_markdown_to_pdf.py docs/posts/substack_zoho_keyword_fallacy.md

Output:
    Creates PDF in same directory as source file.

Requirements:
    pip install markdown weasyprint
"""

import sys
from pathlib import Path

import markdown
from weasyprint import CSS, HTML


def convert_markdown_to_pdf(md_file_path: str, output_path: str = None):
    """Convert markdown file to PDF with styling."""

    md_path = Path(md_file_path)
    if not md_path.exists():
        print(f"Error: File not found: {md_file_path}")
        sys.exit(1)

    # Read markdown
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert to HTML with extensions
    html_content = markdown.markdown(
        md_content, extensions=["extra", "codehilite", "toc", "tables"]
    )

    # Add CSS styling
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
    """
    )

    # Wrap HTML with proper structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{md_path.stem}</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Determine output path
    if output_path is None:
        output_path = md_path.with_suffix(".pdf")
    else:
        output_path = Path(output_path)

    # Convert to PDF
    HTML(string=full_html).write_pdf(output_path, stylesheets=[css])

    print(f"✅ PDF created: {output_path}")
    print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/convert_markdown_to_pdf.py <markdown_file> [output_pdf]"
        )
        print("\nExample:")
        print(
            "  python scripts/convert_markdown_to_pdf.py "
            "docs/posts/substack_zoho_keyword_fallacy.md"
        )
        sys.exit(1)

    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    convert_markdown_to_pdf(md_file, output_file)
