#!/usr/bin/env python3
"""
Post to LinkedIn UGC endpoint.

Example:
    LINKEDIN_ACCESS_TOKEN=xxx LINKEDIN_PERSON_URN=urn:li:person:abc \
        python scripts/post_to_linkedin.py --text "Hello world" --url "https://example.com/article"

Options:
  --text: The text to post (required)
  --url: optional URL to include
  --dry-run: don't actually POST to LinkedIn
"""

import argparse
import json
import os
import sys

import requests

UGC_ENDPOINT = "https://api.linkedin.com/v2/ugcPosts"


def build_ugc_payload(author_urn: str, text: str, url: str | None = None):
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
    if url:
        payload["specificContent"]["com.linkedin.ugc.ShareContent"][
            "shareMediaCategory"
        ] = "ARTICLE"
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {
                "status": "READY",
                "originalUrl": url,
                "title": {"text": text[:200]},
            },
        ]
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post to LinkedIn using UGC API")
    parser.add_argument(
        "--text",
        dest="text",
        required=True,
        help="Text content to post",
    )
    parser.add_argument(
        "--url",
        dest="url",
        default=None,
        help="Optional URL to attach to the post",
    )
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False)
    args = parser.parse_args()

    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN") or os.getenv("LINKEDIN_ORG_URN")

    if not access_token or not person_urn:
        print(
            "Please set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN environment variables.",
        )
        sys.exit(2)

    payload = build_ugc_payload(person_urn, args.text, args.url)

    print("---- POST PAYLOAD ----")
    print(json.dumps(payload, indent=2))

    if args.dry_run:
        print("Dry-run mode; not actually posting to LinkedIn")
        sys.exit(0)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    r = requests.post(UGC_ENDPOINT, headers=headers, json=payload, timeout=10)
    if r.status_code not in (200, 201):
        print("Failed to create UGC post; status:", r.status_code)
        print(r.text)
        sys.exit(1)

    print("Success! LinkedIn response:")
    print(r.text)
