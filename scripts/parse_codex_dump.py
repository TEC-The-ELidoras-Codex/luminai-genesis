#!/usr/bin/env python3
"""
Combine a large TEC codex dump into a small set of canonical Markdown bundles.

Usage (example):
  python3 scripts/build_canonical_bundles.py \
    --input TEC_CODEX_DUMP \
    --out docs/canonical \
    --min-level 2 \
    --min-chars 200 \
    --max-chars 80000

What this does:
- Parses the dump into sections at headings with level <= --min-level
- Drops very short sections (--min-chars)
- Deduplicates by content hash
- Sorts remaining sections by length (longest first)
- Packs them into bundles of up to --max-chars characters each
- Writes bundle files + a manifest.json describing what’s where
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import List, Dict, Any

HEADING_RE = re.compile(r"^(#{1,6})\s*(.+)$")


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-\s_]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = s.strip("-")
    return s or "untitled"


def parse_dump(text: str, min_level_for_file: int = 2) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    current = {
        "title": "Document Start",
        "slug": "document-start",
        "heading_level": 0,
        "content": [],
    }

    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            if level <= min_level_for_file:
                if current["content"]:
                    sections.append(
                        {
                            "title": current["title"],
                            "slug": current["slug"],
                            "heading_level": current["heading_level"],
                            "content": "\n".join(current["content"]).rstrip() + "\n",
                        }
                    )
                current = {
                    "title": title,
                    "slug": slugify(title),
                    "heading_level": level,
                    "content": [m.group(0)],
                }
            else:
                current["content"].append(line)
        else:
            current["content"].append(line)

    if current and current["content"]:
        sections.append(
            {
                "title": current["title"],
                "slug": current["slug"],
                "heading_level": current["heading_level"],
                "content": "\n".join(current["content"]).rstrip() + "\n",
            }
        )

    return sections


def dedupe_sections(
    sections: List[Dict[str, Any]], min_chars: int = 0
) -> List[Dict[str, Any]]:
    """Drop sections shorter than min_chars and remove exact duplicates by content."""
    seen_hashes = set()
    unique: List[Dict[str, Any]] = []

    for s in sections:
        content = s["content"]
        if len(content) < min_chars:
            continue
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        unique.append(s)

    return unique


def bundle_sections(
    sections: List[Dict[str, Any]], max_chars: int = 80000
) -> List[list]:
    """
    Greedy pack sections into bundles capped by max_chars total content length.

    Note: If a single section is larger than max_chars, it will be placed
    in its own bundle (it will exceed the cap). This keeps logic simple and
    avoids re-splitting large docs for now.
    """
    bundles: List[list] = []
    current: list = []
    current_chars = 0

    for s in sections:
        content = s["content"]
        length = len(content)

        # If a single big section is larger than max_chars and we don't have
        # anything in the current bundle, put it alone.
        if length > max_chars and not current:
            bundles.append([s])
            continue

        # If adding this section would exceed the limit, close current and start new.
        if current_chars + length > max_chars and current:
            bundles.append(current)
            current = [s]
            current_chars = length
        else:
            current.append(s)
            current_chars += length

    if current:
        bundles.append(current)

    return bundles


def write_bundles(
    bundles: List[list],
    out_dir: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []

    for idx, bundle in enumerate(bundles, start=1):
        filename = f"{idx:02d}-bundle.md"
        path = out_dir / filename

        header_lines = [
            "---",
            f'title: "Bundle {idx}"',
            f"bundle_index: {idx}",
            "---",
            "",
            f"# Bundle {idx}",
            "",
            "## Included Sections",
            "",
        ]

        titles = []
        total_chars = 0

        for s in bundle:
            titles.append(s["title"])
            total_chars += len(s["content"])
            header_lines.append(f"- {s['title']}")

        header_lines.append("")
        body_parts = []

        for s in bundle:
            body_parts.append("\n\n---\n\n")
            body_parts.append(s["content"])

        path.write_text("".join(header_lines) + "".join(body_parts), encoding="utf-8")

        manifest.append(
            {
                "bundle": idx,
                "file": filename,
                "titles": titles,
                "total_chars": total_chars,
            }
        )

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", required=True, help="Path to TEC_CODEX_DUMP")
    ap.add_argument("--out", "-o", required=True, help="Output directory for bundles")
    ap.add_argument(
        "--min-level",
        type=int,
        default=2,
        help="Heading level that starts a new section (default: 2 → # and ##)",
    )
    ap.add_argument(
        "--min-chars",
        type=int,
        default=200,
        help="Drop sections shorter than this many characters (default: 200)",
    )
    ap.add_argument(
        "--max-chars",
        type=int,
        default=80000,
        help="Target max characters per bundle (default: 80000)",
    )
    args = ap.parse_args()

    dump_path = Path(args.input)
    out_dir = Path(args.out)

    text = dump_path.read_text(encoding="utf-8", errors="replace")
    sections = parse_dump(text, min_level_for_file=args.min_level)
    sections = dedupe_sections(sections, min_chars=args.min_chars)

    # Sort longest first so the big docs either get their own bundles
    # or anchor early bundles.
    sections.sort(key=lambda s: len(s["content"]), reverse=True)

    bundles = bundle_sections(sections, max_chars=args.max_chars)
    write_bundles(bundles, out_dir)

    print(f"Wrote {len(bundles)} bundles to {out_dir}")


if __name__ == "__main__":
    main()
