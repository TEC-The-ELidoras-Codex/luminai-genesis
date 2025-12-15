#!/usr/bin/env python3
"""Simple helper to post a text-only LinkedIn UGC post using an access token.

Usage examples:

export LINKEDIN_ACCESS_TOKEN="..."
python scripts/post_linkedin.py --text "Hello from luminai-genesis test"

Or pass token explicitly:
python scripts/post_linkedin.py --access-token "..." --text "Test"

Be careful: this will publish to the authenticated user's feed. Prefer using a test account.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import requests

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
        raise RuntimeError(f"Could not determine person id from /me response: {body}")
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
        "--access-token", help="LinkedIn access token (env: LINKEDIN_ACCESS_TOKEN)"
    )
    parser.add_argument("--text", required=True, help="Text to post")
    parser.add_argument(
        "--dry-run", action="store_true", help="Do not actually POST; show payload"
    )
    args = parser.parse_args(argv)

    token = args.access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print(
            "ERROR: provide --access-token or set LINKEDIN_ACCESS_TOKEN environment variable",
            file=sys.stderr,
        )
        return 2

    try:
        author = get_person_urn(token)
        if args.dry_run:
            print("Dry run: would create post with payload:")
            print(json.dumps({"author": author, "text": args.text}, indent=2))
            return 0

        result = create_ugc_post(token, author, args.text)
        print("Post created:")
        print(json.dumps(result, indent=2))
        return 0
    except requests.HTTPError as e:
        print(
            f"HTTP error during LinkedIn API call: {e}\nResponse: {getattr(e.response, 'text', '<no body>')}",
            file=sys.stderr,
        )
        return 3
    except Exception as e:  # pragma: no cover - surface errors
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Post a text-only article to LinkedIn using an access token.

Usage:
    export LINKEDIN_ACCESS_TOKEN="..."
    python3 scripts/post_linkedin.py private/drafts/linkedin_to_post.txt
    # if you still use the old location:
    # python3 scripts/post_linkedin.py drafts/linkedin_to_post.txt

The script will call the `v2/me` endpoint to learn the member ID and then create an UGC post.
It requires `requests` to be installed in the venv: `venv/bin/pip install requests`.

Security: keep your access token private. The script will not store it.
"""


API_BASE = "https://api.linkedin.com/v2"


def read_message(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def get_member_urn(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API_BASE}/me", headers=headers)
    r.raise_for_status()
    data = r.json()
    # construct author urn
    member_id = data.get("id")
    if not member_id:
        raise RuntimeError("Could not determine LinkedIn member id from /me")
    return f"urn:li:person:{member_id}"


def create_ugc_post(token, author_urn, text):
    headers = {
        "Authorization": f"Bearer {token}",
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
    r = requests.post(f"{API_BASE}/ugcPosts", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/post_linkedin.py <message-file>")
        sys.exit(2)
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print(
            "ERROR: Set LINKEDIN_ACCESS_TOKEN environment variable with a valid "
            "LinkedIn OAuth access token.",
        )
        sys.exit(2)
    message_file = sys.argv[1]
    # Prefer `private/drafts/` for local, private draft files but keep compatibility
    if not os.path.exists(message_file):
        alt = (
            message_file.replace("drafts/", "private/drafts/")
            if "drafts/" in message_file
            else None
        )
        if alt and os.path.exists(alt):
            message_file = alt
    message = read_message(message_file)
    print("Obtaining LinkedIn member URN via /me...")
    author = get_member_urn(token)
    print(f"Posting as {author[:40]}...")
    resp = create_ugc_post(token, author, message)
    print("Post created:")
    print(json.dumps(resp, indent=2))
