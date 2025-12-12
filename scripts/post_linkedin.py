#!/usr/bin/env python3
"""Post a text-only article to LinkedIn using an access token.

Usage:
  export LINKEDIN_ACCESS_TOKEN="..."
  python3 scripts/post_linkedin.py drafts/linkedin_to_post.txt

The script will call the `v2/me` endpoint to learn the member ID and then create an UGC post.
It requires `requests` to be installed in the venv: `venv/bin/pip install requests`.

Security: keep your access token private. The script will not store it.
"""

import json
import os
import sys

import requests

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
        print("ERROR: Set LINKEDIN_ACCESS_TOKEN environment variable with a valid LinkedIn OAuth access token.")
        sys.exit(2)
    message_file = sys.argv[1]
    message = read_message(message_file)
    print("Obtaining LinkedIn member URN via /me...")
    author = get_member_urn(token)
    print(f"Posting as {author[:40]}...")
    resp = create_ugc_post(token, author, message)
    print("Post created:")
    print(json.dumps(resp, indent=2))
