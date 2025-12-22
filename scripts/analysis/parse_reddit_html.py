#!/usr/bin/env python3
"""Simple Reddit megathread HTML parser.

Reads a pasted Reddit HTML file and extracts comment blocks, author, and timestamp
using heuristics, classifies failure types with keyword mapping, and writes a
CSV suitable for `compute_witness_scores.py`.

Usage:
  python3 scripts/analysis/parse_reddit_html.py --in reddit_megathread.txt --out docs/research/witness_data/reddit_megathread_expanded.csv

The parser is intentionally forgiving and uses simple heuristics; review the
output for accuracy when you run it on the real megathread HTML.
"""
import argparse
import csv
import logging
import os
import re
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

KEYWORD_MAP = [
    (r"abandon", "Abandonment", -3),
    (r"premature|banner", "Premature Banner", -1),
    (r"gaslight|gaslighting", "Gaslighting", -2),
    (r"lost context|lostcontext|lost-context|context", "Lost Context", -2),
    (r"network|timeout|connection|error", "Network Error", -2),
    (r"bug|crash|exception", "Bug", -1),
]


def classify(text: str):
    t = text.lower()
    for pattern, label, sar in KEYWORD_MAP:
        if re.search(pattern, t):
            return label, sar
    return "Other", -1


def extract_comments_from_html(html: str):
    # Heuristics: Reddit comment bodies often appear inside <div class="md">...</div>
    blocks = re.findall(
        r"<div[^>]*class=[\'\"](?:md|md-container|usertext-body|md)[^\'\"]*[\'\"][^>]*>(.*?)</div>",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    comments = []
    if not blocks:
        # fallback: capture <p> tags
        blocks = re.findall(r"<p[^>]*>(.*?)</p>", html, flags=re.DOTALL | re.IGNORECASE)

    for i, b in enumerate(blocks):
        # strip tags to plain text (very small sanitizer)
        text = re.sub(
            r"<script.*?>.*?</script>", "", b, flags=re.DOTALL | re.IGNORECASE
        )
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        comments.append((i + 1, text))
    return comments


def extract_author_and_time(html: str):
    # Try crude extraction for the whole page: map comment index -> (author, time)
    authors = re.findall(r'data-author="([^"]+)"', html, flags=re.IGNORECASE)
    if not authors:
        authors = re.findall(
            r"<a[^>]*class=[\'\"][^\'\"]*author[^\'\"]*[\'\"][^>]*>([^<]+)</a>",
            html,
            flags=re.IGNORECASE,
        )

    times = re.findall(r'<time[^>]*datetime="([^"]+)"', html, flags=re.IGNORECASE)
    # Align best-effort: pair by index
    pairs = []
    n = max(len(authors), len(times))
    for i in range(n):
        a = authors[i] if i < len(authors) else ""
        t = times[i] if i < len(times) else ""
        # normalize time if possible
        if t:
            try:
                # some times are full ISO timestamps
                dt = datetime.fromisoformat(t.replace("Z", "+00:00"))
                t = dt.strftime("%Y-%m-%d")
            except Exception as exc:
                logger.debug("Failed to parse datetime string '%s': %s", t, exc, exc_info=exc)
                # fallback: keep raw
                pass
        pairs.append((a, t))
    return pairs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="infile", required=True)
    p.add_argument("--out", dest="outfile", required=True)
    args = p.parse_args()

    if not os.path.exists(args.infile):
        logger.error(
            "Input file %s not found. Paste your Reddit HTML to that path and re-run.", args.infile
        )
        raise SystemExit(1)

    html = Path(args.infile).read_text(encoding="utf-8", errors="replace")

    comments = extract_comments_from_html(html)
    auth_time = extract_author_and_time(html)

    # Prepare output CSV
    out_path = Path(args.outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["date", "user", "id", "failure_type", "SAR", "comment"])

        for idx, (cid, text) in enumerate(comments):
            user = ""
            date = ""
            if idx < len(auth_time):
                user, date = auth_time[idx]
            failure, sar = classify(text)
            writer.writerow([date or "", user or "", f"c{cid}", failure, sar, text])

    logger.info("Wrote %d extracted comments to %s", len(comments), args.outfile)


if __name__ == "__main__":
    main()
