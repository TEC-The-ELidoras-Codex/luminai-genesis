#!/usr/bin/env python3
"""Generate platform-specific social drafts from `docs/publish-ready/*.md`.

Creates `docs/publish-ready/social/<platform>_<slug>.md` for each post.
"""
import re
from pathlib import Path


def read_publish_ready(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    # try to get YAML frontmatter title
    title = None
    m = re.search(r"^title:\s*\"?(.*?)\"?\s*$", text, flags=re.M)
    if m:
        title = m.group(1).strip()

    # fallback to first non-empty line
    if not title:
        for line in text.splitlines():
            if line.strip():
                title = line.strip()
                break

    # summary is first paragraph after frontmatter
    parts = re.split(r"^---$|^--$", text, flags=re.M)
    if len(parts) >= 3:
        content = parts[2]
    else:
        content = text

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", content) if p.strip()]
    summary = paragraphs[0] if paragraphs else ""
    return title or md_path.stem, summary


def make_linkedin(title, summary, pdf_path):
    body = f"{title}\n\n{summary}\n\nFull write-up & reproducible artifacts → {pdf_path}\n#AILab #ResponsibleAI #Safety #Research"
    return body


def make_x(title, summary, pdf_path):
    # shorter
    body = f"{title} — {summary[:200]}... Read: {pdf_path} #AI #Safety"
    return body


def make_substack(title, summary, pdf_path):
    body = f"{title}\n\n{summary}\n\nRead the full report (PDF): {pdf_path}\n\n— The Elidoras Codex"
    return body


def main():
    src_dir = Path("docs/publish-ready")
    out_dir = src_dir / "social"
    out_dir.mkdir(parents=True, exist_ok=True)

    for md in sorted(src_dir.glob("*.md")):
        if md.parent.name == "social":
            continue
        title, summary = read_publish_ready(md)
        pdf_rel = Path("docs/pdfs") / (md.stem + ".pdf")

        linkedin = make_linkedin(title, summary, pdf_rel)
        xpost = make_x(title, summary, pdf_rel)
        substack = make_substack(title, summary, pdf_rel)

        (out_dir / f"linkedin_{md.stem}.md").write_text(linkedin, encoding="utf-8")
        (out_dir / f"x_{md.stem}.md").write_text(xpost, encoding="utf-8")
        (out_dir / f"substack_{md.stem}.md").write_text(substack, encoding="utf-8")
        print("Wrote social drafts for", md.stem)


if __name__ == "__main__":
    main()
