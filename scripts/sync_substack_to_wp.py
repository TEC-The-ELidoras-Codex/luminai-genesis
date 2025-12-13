#!/usr/bin/env python3
"""
Sync Substack RSS to WordPress via XML-RPC
Keeps a tracking file (.published_posts.txt) to avoid duplicates
"""

import argparse
import os
import re
import xmlrpc.client

import feedparser
import requests
from requests.exceptions import RequestException
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

SUBSTACK_RSS = os.getenv("SUBSTACK_RSS") or os.getenv("SUBSTACK_RSS_URL")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

TRACK_FILE = ".published_posts.txt"


def load_published():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE) as f:
            return set(line.strip() for line in f)
    return set()


def save_published(url):
    with open(TRACK_FILE, "a") as f:
        f.write(url + "\n")


def html_to_plain(html: str) -> str:
    return re.sub("<[^<]+?>", "", html)


def resolve_feed_url(base: str) -> str | None:
    """Try a few common variations of RSS feed paths and return a URL that returns an RSS XML (status 200).

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
        "User-Agent": "Mozilla/5.0 (compatible; LuminAI/1.0; +https://github.com/TEC-The-ELidoras-Codex)"
    }
    for c in candidates:
        try:
            resp = requests.get(c, timeout=10, headers=headers)
            if resp.status_code == 200 and "xml" in (
                resp.headers.get("Content-Type") or ""
            ):
                return c
            # Sometimes the server returns HTML but the content itself contains <rss
            # so we still want to accept it.
            if resp.status_code == 200 and "<rss" in resp.text[:1000]:
                return c
        except Exception:
            continue
    return None


def fetch_feed(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LuminAI/1.0; +https://github.com/TEC-The-ELidoras-Codex)"
    }
    try:
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        return feedparser.parse(r.content)
    except Exception:
        # Fallback: let feedparser attempt to parse the URL directly
        return feedparser.parse(url)


def publish_to_wordpress(debug: bool = False):
    published = load_published()
    resolved = resolve_feed_url(SUBSTACK_RSS)
    if not resolved:
        print(
            "❌ Could not find a valid RSS feed at the configured URL. Tried common endpoints."
        )
        return
    if debug:
        print(f"ℹ️ Using feed URL: {resolved}")
    feed = fetch_feed(resolved)
    client = Client(WP_URL, WP_USERNAME, WP_PASSWORD)
    new_count = 0
    for entry in feed.entries:
        url = entry.link
        if url in published:
            print(f"⏭️ Skipping already published: {entry.title}")
            continue
        content = entry.content[0].value if hasattr(entry, "content") else entry.summary
        post = WordPressPost()
        post.title = entry.title
        post.content = content
        post.post_status = "publish"
        try:
            client.call(NewPost(post))
            save_published(url)
            new_count += 1
            print(f"✅ Published to WordPress: {entry.title}")
        except (
            xmlrpc.client.Fault,
            xmlrpc.client.ProtocolError,
            RequestException,
        ) as e:
            print(f"❌ Failed to publish to WordPress: {e}")
    if new_count == 0:
        print("ℹ️ No new posts to publish")
    else:
        print(f"🎉 Published {new_count} new posts to WordPress")


if __name__ == "__main__":
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
        missing_msg = "❌ Missing required environment variables: " + ", ".join(missing)
        print(missing_msg)
        exit(1)
    publish_to_wordpress(debug=args.debug)
