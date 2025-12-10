#!/usr/bin/env python3
from pathlib import Path
import re


def extract_title_and_summary(md_text: str):
    # Strip YAML frontmatter
    if md_text.strip().startswith("---") or md_text.strip().startswith("--"):
        parts = re.split(r"^---$|^--$", md_text, flags=re.M)
        if len(parts) >= 3:
            # parts[1] is frontmatter, parts[2] is content
            content = parts[2]
        else:
            content = md_text
    else:
        content = md_text

    # Find first H1 or H2
    m = re.search(r"^#\s+(.*)$", content, flags=re.M)
    if not m:
        m = re.search(r"^##\s+(.*)$", content, flags=re.M)

    title = m.group(1).strip() if m else None

    # Find first paragraph (non-heading, non-empty)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", content) if p.strip()]
    summary = None
    for p in paragraphs:
        if not p.startswith("#") and len(p) > 20:
            summary = p.replace("\n", " ").strip()
            break

    return title or "", summary or ""


def main():
    posts_dir = Path("docs/posts")
    out_dir = Path("docs/publish-ready")
    out_dir.mkdir(parents=True, exist_ok=True)

    for md in sorted(posts_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        title, summary = extract_title_and_summary(text)
        if not title:
            title = md.stem.replace("_", " ").title()

        pdf_path = Path("docs/pdfs") / (md.stem + ".pdf")
        excerpt = f'---\ntitle: "{title}"\nsource: {md}\npdf: {pdf_path}\n---\n\n'
        excerpt += f"{summary}\n\n[Read full post]({pdf_path})\n"

        out_file = out_dir / (md.stem + ".md")
        out_file.write_text(excerpt, encoding="utf-8")
        print("Wrote", out_file)


if __name__ == "__main__":
    main()
