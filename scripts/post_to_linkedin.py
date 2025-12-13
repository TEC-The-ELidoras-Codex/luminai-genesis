#!/usr/bin/env python3
"""
Auto-post Substack articles to LinkedIn
Monitors RSS feed and creates LinkedIn posts with teasers
"""

import argparse
import os
import re

import feedparser
import requests
from requests.exceptions import RequestException

# LinkedIn API credentials
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")  # e.g., 'urn:li:person:ABC123'
SUBSTACK_RSS = os.getenv("SUBSTACK_RSS") or os.getenv("SUBSTACK_RSS_URL")

# Track posted articles
POSTED_FILE = ".linkedin_posted.txt"


def load_posted_articles():
    """Load list of already-posted article URLs"""
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE) as f:
            return set(line.strip() for line in f)
    return set()


def save_posted_article(url):
    """Mark article as posted"""
    with open(POSTED_FILE, "a") as f:
        f.write(f"{url}\n")


def create_linkedin_post(title, excerpt, url):
    """Create a LinkedIn post using the v2 API"""
    tags = "#SciFi #AIEthics #LuminAI #TheElidorasCodex #WritingCommunity"
    post_text_parts = [
        "📖 New from The Elidoras Codex:",
        title,
        excerpt,
        f"Read more: {url}",
        tags,
    ]
    post_text = "\n\n".join(part for part in post_text_parts if part)

    api_url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": LINKEDIN_PERSON_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "originalUrl": url,
                        "title": {"text": title},
                    },
                ],
            },
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 201:
        return True, response.json()
    return False, response.text


def extract_excerpt(content, max_length=200):
    """Extract first N characters as excerpt, breaking at word boundary"""
    if len(content) <= max_length:
        return content
    excerpt = content[:max_length]
    last_space = excerpt.rfind(" ")
    if last_space > 0:
        excerpt = excerpt[:last_space]
    return excerpt + "..."


def post_new_articles():
    """Check RSS feed and post new articles to LinkedIn"""
    posted_urls = load_posted_articles()

    # If SUBSTACK_RSS is a webroot, try common feed endpoints and use a browser-like UA
    def resolve_feed(base: str) -> str:
        base = base.rstrip("/")
        candidates = [
            base,
            f"{base}/feed",
            f"{base}/rss",
            f"{base}/rss.xml",
            f"{base}/feed.xml",
        ]
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; LuminAI/1.0; +https://github.com/TEC-The-ELidoras-Codex)",
        }
        for c in candidates:
            try:
                r = requests.get(c, timeout=10, headers=headers)
                if r.status_code == 200 and "xml" in (
                    r.headers.get("Content-Type") or ""
                ):
                    return c
                if r.status_code == 200 and "<rss" in r.text[:1000]:
                    return c
            except Exception:
                continue
        return base

    resolved_url = resolve_feed(SUBSTACK_RSS)
    feed = feedparser.parse(resolved_url)
    new_posts_count = 0
    for entry in feed.entries:
        article_url = entry.link
        if article_url in posted_urls:
            print(f"⏭️  Skipping (already posted): {entry.title}")
            continue
        print(f"📝 Posting to LinkedIn: {entry.title}")
        title = entry.title
        content = entry.content[0].value if hasattr(entry, "content") else entry.summary
        content_text = re.sub("<[^<]+?>", "", content)
        excerpt = extract_excerpt(content_text, max_length=200)
        try:
            success, result = create_linkedin_post(title, excerpt, article_url)
            if success:
                print(f"✅ Posted to LinkedIn: {title}")
                save_posted_article(article_url)
                new_posts_count += 1
            else:
                print(f"❌ Failed to post '{title}': {result}")
        except RequestException as e:
            print(f"❌ Error posting '{title}': {e}")
    if new_posts_count == 0:
        print("ℹ️  No new articles to post")
    else:
        print(f"\n🎉 Successfully posted {new_posts_count} article(s) to LinkedIn")
    return new_posts_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post Substack articles to LinkedIn")
    parser.add_argument("--debug", action="store_true", help="Show feed debug output")
    args = parser.parse_args()
    if not all([LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN, SUBSTACK_RSS]):
        missing = []
        for name, value in (
            ("LINKEDIN_ACCESS_TOKEN", LINKEDIN_ACCESS_TOKEN),
            ("LINKEDIN_PERSON_URN", LINKEDIN_PERSON_URN),
            ("SUBSTACK_RSS", SUBSTACK_RSS),
        ):
            if not value:
                missing.append(name)
        print("❌ Missing required environment variables:")
        for m in missing:
            print(f"   - {m}")
        exit(1)
    if args.debug:
        print(f"ℹ️ Using feed URL: {SUBSTACK_RSS}")
    post_new_articles()
