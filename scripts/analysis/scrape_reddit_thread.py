#!/usr/bin/env python3
"""Extract comments from a Reddit thread and write a CSV matching the witness schema.

Usage:
  - From Pushshift (no credentials):
      python3 scripts/analysis/scrape_reddit_thread.py --url THREAD_URL --out expanded.csv

  - From local Reddit JSON export:
      python3 scripts/analysis/scrape_reddit_thread.py --json reddit_thread.json --out expanded.csv

Notes:
  - The script will not auto-assign SAR scores. It extracts date, anon_user, comment text and context fields
    so you can score manually (or run a later auto-scorer).
  - If using the Pushshift fetch, results depend on Pushshift availability.
"""

import argparse
import csv
import datetime
import json
import logging
import re

import requests

logger = logging.getLogger(__name__)

HEADERS = [
    "date",
    "anon_user",
    "model_reported",
    "trigger_context",
    "system_response",
    "failure_type",
    "sar_score",
]

ANON_PREFIX = "user"


def extract_submission_id(url: str) -> str | None:
    # Try common reddit URL patterns to extract submission id
    m = re.search(r"comments/([0-9a-zA-Z]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/r/[^/]+/([0-9a-zA-Z]+)/", url)
    if m:
        return m.group(1)
    return None


def fetch_comments_pushshift(submission_id: str, size: int = 5000) -> list[dict]:
    url = f"https://api.pushshift.io/reddit/comment/search?link_id=t3_{submission_id}&size={size}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return data


def load_comments_from_json(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        j = json.load(f)
    # Accept either a list of comment dicts or Reddit "json" export (list with two elements)
    if isinstance(j, list):
        # If second element has 'data' with children (Reddit page export), try to walk it
        if len(j) >= 2 and isinstance(j[1], dict) and "data" in j[1]:
            try:
                children = j[1]["data"]["children"]
                comments = []
                for c in children:
                    d = c.get("data", {})
                    comments.append(d)
                return comments
            except Exception as exc:
                logger.debug(
                    "Failed to parse Reddit JSON export children: %s", exc, exc_info=exc,
                )

        # Otherwise assume it's a list of comment objects
        return j
    if isinstance(j, dict) and "data" in j:
        # Example: Pushshift-like
        return j["data"].get("children", [])
    raise ValueError("Unrecognized JSON structure for comments")


def to_witness_rows(comments: list[dict]) -> list[dict]:
    rows = []
    anon_map = {}
    anon_idx = 1
    for c in comments:
        # Attempt to find author, body, created_utc
        author = c.get("author") or c.get("user") or "[deleted]"
        if author in ("[deleted]", "AutoModerator"):
            anon = f"{ANON_PREFIX}{anon_idx}"
            anon_idx += 1
        else:
            if author not in anon_map:
                anon_map[author] = f"{ANON_PREFIX}{anon_idx}"
                anon_idx += 1
            anon = anon_map[author]

        body = c.get("body") or c.get("selftext") or c.get("text") or ""
        created = None
        if c.get("created_utc"):
            try:
                created = (
                    datetime.datetime.utcfromtimestamp(int(c.get("created_utc")))
                    .date()
                    .isoformat()
                )
            except Exception as exc:
                logger.debug(
                    "Failed to parse created_utc timestamp: %s", exc, exc_info=exc,
                )
                created = None
        if not created and c.get("created"):
            try:
                created = (
                    datetime.datetime.fromisoformat(c.get("created")).date().isoformat()
                )
            except Exception:
                created = None

        # Heuristics: attempt to detect reported model or trigger phrases in the body
        model_reported = ""
        m = re.search(
            r"GPT-?([0-9.]+)|gpt[ -]?([0-9.]+)|4o|4\.1|5", body, flags=re.IGNORECASE,
        )
        if m:
            model_reported = (m.group(1) or m.group(2) or "").strip()

        # For now fill trigger_context with the comment body, leave system_response/failure_type empty for manual review
        row = {
            "date": created or "",
            "anon_user": anon,
            "model_reported": model_reported,
            "trigger_context": body.replace("\n", " ")[:1000],
            "system_response": "",
            "failure_type": "",
            "sar_score": "",
        }
        rows.append(row)
    return rows


def write_csv(path: str, rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--url", help="Reddit thread URL (comments/...) to fetch via Pushshift",
    )
    p.add_argument(
        "--json", help="Local exported Reddit JSON file (comments page or comment list)",
    )
    p.add_argument(
        "--out",
        default="docs/research/witness_data/reddit_megathread_expanded.csv",
        help="Output CSV path",
    )
    p.add_argument(
        "--size", type=int, default=2000, help="Max comments to fetch from Pushshift",
    )
    args = p.parse_args()

    comments = []
    if args.json:
        comments = load_comments_from_json(args.json)
    elif args.url:
        subid = extract_submission_id(args.url)
        if not subid:
            raise SystemExit(
                "Failed to extract submission id from URL. Provide --json or a reddit comments URL.",
            )
        comments = fetch_comments_pushshift(subid, size=args.size)
    else:
        raise SystemExit("Provide either --json or --url to fetch comments")

    rows = to_witness_rows(comments)
    write_csv(args.out, rows)
    logger.info("Wrote %d extracted comments to %s", len(rows), args.out)


if __name__ == "__main__":
    main()
