#!/usr/bin/env python3
"""Check and debug Substack RSS feed URL.

Usage:
  SUBSTACK_RSS_URL=https://polkin.substack.com/feed python scripts/check_substack_feed.py

This helper tries several common feed endpoints, adds a browser-like user agent, and prints
status and sample feed entries. Good for debugging why a feed isn't parsed by your script.
"""

import os

import feedparser
import requests

SUBSTACK_RSS = os.getenv("SUBSTACK_RSS") or os.getenv("SUBSTACK_RSS_URL")

candidates = [
    SUBSTACK_RSS and SUBSTACK_RSS.rstrip("/"),
    SUBSTACK_RSS and f"{SUBSTACK_RSS.rstrip('/')}/feed",
    SUBSTACK_RSS and f"{SUBSTACK_RSS.rstrip('/')}/rss",
    SUBSTACK_RSS and f"{SUBSTACK_RSS.rstrip('/')}/rss.xml",
    SUBSTACK_RSS and f"{SUBSTACK_RSS.rstrip('/')}/feed.xml",
]

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; LuminAI/1.0; +https://github.com/TEC-The-ELidoras-Codex)"
}

print(f"🔎 Debugging SUBSTACK_RSS={SUBSTACK_RSS}")
for c in candidates:
    if not c:
        continue
    try:
        print(f"\nTrying: {c}")
        r = requests.get(c, headers=headers, timeout=10)
        print(f"  Status: {r.status_code}")
        print(f"  Content-Type: {r.headers.get('Content-Type')}")
        print("  Starting content snippet:")
        snippet = r.text[:1000]
        print(snippet)
        if r.status_code == 200 and "<rss" in snippet[:1000]:
            print(f"\n✅ Found likely RSS feed here: {c}")
            feed = feedparser.parse(r.content)
            print(f"  Feed title: {feed.feed.get('title')}")
            print(f"  Entries: {len(feed.entries)}")
            break
    except requests.RequestException as e:
        print(f"  Request failed: {e}")

print("\nDone.")
