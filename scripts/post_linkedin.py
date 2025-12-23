"""Simple helper to post a text-only LinkedIn UGC post using an access token.

Usage examples:

export LINKEDIN_ACCESS_TOKEN="..."
python scripts/post_linkedin.py --text "Hello from luminai-genesis test"

Or pass token explicitly:
python scripts/post_linkedin.py --access-token "..." --text "Test"

Be careful: this will publish to the authenticated user's feed.
Prefer using a test account.
"""

from __future__ import annotations

import argparse
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

API_ME = "https://api.linkedin.com/v2/me"
API_UGC_POSTS = "https://api.linkedin.com/v2/ugcPosts"


def get_person_urn(access_token: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    resp = requests.get(API_ME, headers=headers, timeout=10)
    resp.raise_for_status()
    body = resp.json()
    person_id = body.get("id")
    if not person_id:
        msg = f"Could not determine person id from /me response: {body}"
        raise RuntimeError(msg)
    return f"urn:li:person:{person_id}"


def create_ugc_post(access_token: str, author_urn: str, text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            },
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    resp = requests.post(API_UGC_POSTS, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--access-token",
        help="LinkedIn access token (env: LINKEDIN_ACCESS_TOKEN)",
    )
    parser.add_argument("--text", required=True, help="Text to post")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not actually POST; show payload",
    )
    args = parser.parse_args(argv)

    token = args.access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        logger.error(
            "Provide --access-token or set LINKEDIN_ACCESS_TOKEN environment variable",
        )
        return 2

    try:
        author = get_person_urn(token)
    except requests.HTTPError:
        logger.exception("HTTP error while fetching LinkedIn person URN")
        return 3
    except Exception:
        logger.exception("Unexpected error while fetching LinkedIn person URN")
        return 1

    if args.dry_run:
        payload = json.dumps({"author": author, "text": args.text}, indent=2)
        logger.info("Dry run: would create post with payload:")
        logger.info(payload)
        return 0

    try:
        result = create_ugc_post(token, author, args.text)
    except requests.HTTPError:
        logger.exception("HTTP error during LinkedIn API call")
        return 3
    except Exception:
        logger.exception("Unexpected error while posting to LinkedIn")
        return 1

    logger.info("Post created: %s", json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
