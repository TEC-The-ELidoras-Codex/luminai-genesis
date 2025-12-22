#!/usr/bin/env python3
"""CLI helper to exchange a LinkedIn auth code for an access token.

Usage:
  export LINKEDIN_CLIENT_ID=...
  export LINKEDIN_CLIENT_SECRET=...
  export LINKEDIN_REDIRECT_URI=...
  python scripts/get_linkedin_token.py --code AUTH_CODE
"""

import argparse
import os

import requests

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--code", required=True, help="Authorization code from LinkedIn")
    args = p.parse_args()

    cid = os.environ.get("LINKEDIN_CLIENT_ID")
    csec = os.environ.get("LINKEDIN_CLIENT_SECRET")
    ruri = os.environ.get("LINKEDIN_REDIRECT_URI")
    if not cid or not csec or not ruri:
        print(
            "Missing environment variables: set LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI",
        )
        return 2

    payload = {
        "grant_type": "authorization_code",
        "code": args.code,
        "redirect_uri": ruri,
        "client_id": cid,
        "client_secret": csec,
    }
    r = requests.post(TOKEN_URL, data=payload)
    print("Status:", r.status_code)
    print(r.text)


if __name__ == "__main__":
    main()
