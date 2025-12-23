#!/usr/bin/env python3
"""Build Substack-ready HTML from ready memos.

This script produces simple HTML/Markdown output suitable for copy-paste into Substack's composer.
Usage: python3 scripts/aqueduct_build_substack_html.py
"""

import logging
from pathlib import Path

import markdown
import yaml

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
READY_DIR = ROOT / "docs" / "streams" / "articles" / "ready"
OUT_DIR = ROOT / "dist" / "substack"


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text = parts[1]
    body = parts[2]
    fm = yaml.safe_load(fm_text) or {}
    return fm, body.strip()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(READY_DIR.glob("*.md"))
    if not files:
        logger.warning("No ready memos found in docs/streams/articles/ready")
        return

    for md_path in files:
        text = md_path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        channels = fm.get("channels") or []
        if "substack" not in channels and "both" not in channels:
            continue

        slug = fm.get("slug") or md_path.stem
        title = fm.get("title", slug)

        # Convert to HTML for Substack (copy-paste friendly)
        html = markdown.markdown(body, extensions=["extra"])

        out_path = OUT_DIR / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")

        logger.info("Built HTML for Substack: %s (title: %s)", out_path, title)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
