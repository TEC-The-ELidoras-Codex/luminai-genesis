#!/usr/bin/env python3
"""Build Gutenberg/WordPress-ready HTML from ready memos.

Usage: python3 scripts/aqueduct_build_wordpress_html.py
"""

from pathlib import Path
import sys
import yaml
import markdown
import json

ROOT = Path(__file__).resolve().parents[1]
READY_DIR = ROOT / "docs" / "streams" / "articles" / "ready"
OUT_DIR = ROOT / "dist" / "wordpress"


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
        print("No ready memos found in docs/streams/articles/ready", file=sys.stderr)
        return

    for md_path in files:
        text = md_path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        channels = fm.get("channels") or []
        if "wordpress" not in channels and "both" not in channels:
            # skip if it's not meant for WP
            continue

        slug = fm.get("slug") or md_path.stem
        title = fm.get("title", slug)

        # Convert Markdown to HTML; developers can tweak extensions as needed
        html_body = markdown.markdown(body, extensions=["extra"])

        # Build a simple HTML wrapper so we can preserve metadata like author/orcid
        author = fm.get("author") or ""
        orcid = fm.get("orcid") or ""
        date = fm.get("date") or ""

        # Include frontmatter metadata as JSON for later parsing by the publisher
        meta_json = json.dumps(fm)

        html = """
<article>
  <script type="application/json" id="frontmatter">{meta_json}</script>
  <header>
    <h1>{title}</h1>
    <p class="meta">{date} • {author} {orcid_html}</p>
  </header>
  <section class="content">
{body}
  </section>
</article>
""".format(
            meta_json=meta_json,
            title=title,
            date=date,
            author=author,
            orcid_html=f"<a href=\"{orcid}\">{orcid}</a>" if orcid else "",
            body=html_body,
        )

        out_path = OUT_DIR / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")

        print(f"✨ Built HTML for WordPress: {out_path} (title: {title})")


if __name__ == "__main__":
    main()
