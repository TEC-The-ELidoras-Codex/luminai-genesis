"""
Sync Substack RSS to WordPress via XML-RPC
Keeps a tracking file (.published_posts.txt) to avoid duplicates
"""

import argparse
import logging
import os
import re
import sys
from http import HTTPStatus
from pathlib import Path

import feedparser
import requests

logger = logging.getLogger(__name__)

SUBSTACK_RSS = os.getenv("SUBSTACK_RSS") or os.getenv("SUBSTACK_RSS_URL")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

TRACK_FILE = ".published_posts.txt"


def load_published():
    track = Path(TRACK_FILE)
    if track.exists():
        with track.open(encoding="utf-8") as f:
            return {line.strip() for line in f}
    return set()


def save_published(url):
    track = Path(TRACK_FILE)
    with track.open("a", encoding="utf-8") as f:
        f.write(url + "\n")


def html_to_plain(html: str) -> str:
    return re.sub("<[^<]+?>", "", html)


def resolve_feed_url(base: str) -> str | None:
    """Try a few common variations of RSS feed paths and return a URL
    that returns an RSS XML (status 200).

    This helps with sites that use /feed, /rss, /rss.xml, or redirect.
    """
    if not base:
        return None
    base = base.rstrip("/")
    candidates = [
        base,
        f"{base}/feed",
        f"{base}/rss",
        f"{base}/rss.xml",
        f"{base}/feed.xml",
    ]
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; LuminAI/1.0; "
            "+https://github.com/TEC-The-ELidoras-Codex)"
        ),
    }
    for c in candidates:
        try:
            resp = requests.get(c, timeout=10, headers=headers)
            if resp.status_code == HTTPStatus.OK and "xml" in (
                (resp.headers.get("Content-Type") or "").lower()
            ):
                return c
            # Sometimes the server returns HTML but the content itself contains <rss
            # so we still want to accept it.
            if resp.status_code == HTTPStatus.OK and "<rss" in resp.text[:1000]:
                return c
        except requests.RequestException as exc:
            logger.debug("Failed to fetch %s: %s", c, exc)
            continue
    return None


def fetch_feed(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LuminAI/1.0; +https://github.com/TEC-The-ELidoras-Codex)",
    }
    try:
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        return feedparser.parse(r.content)
    except requests.RequestException:
        logger.exception("Error fetching feed %s", url)
        # Fallback: let feedparser attempt to parse the URL directly
        return feedparser.parse(url)


def publish_to_wordpress(*, debug: bool = False):
    _published = load_published()
    _resolved = resolve_feed_url(SUBSTACK_RSS)
    if debug:
        logger.debug("Resolved feed URL: %s", _resolved)


if __name__ == "__main__":
    # Configure lightweight CLI logging so messages are visible by default
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(description="Sync Substack RSS to WordPress")
    parser.add_argument("--debug", action="store_true", help="Show feed debug output")
    args = parser.parse_args()
    if not all([SUBSTACK_RSS, WP_URL, WP_USERNAME, WP_PASSWORD]):
        missing = []
        for name, value in (
            ("SUBSTACK_RSS", SUBSTACK_RSS),
            ("WP_URL", WP_URL),
            ("WP_USERNAME", WP_USERNAME),
            ("WP_PASSWORD", WP_PASSWORD),
        ):
            if not value:
                missing.append(name)
        missing_msg = "Missing required environment variables: " + ", ".join(missing)
        logger.error(missing_msg)
        sys.exit(1)
    publish_to_wordpress(debug=args.debug)
