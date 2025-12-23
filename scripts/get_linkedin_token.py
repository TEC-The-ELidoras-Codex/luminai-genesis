"""CLI helper to exchange a LinkedIn auth code for an access token.

Usage:
  export LINKEDIN_CLIENT_ID=...
  export LINKEDIN_CLIENT_SECRET=...
  export LINKEDIN_REDIRECT_URI=...
  python scripts/get_linkedin_token.py --code AUTH_CODE
"""

import argparse
import logging
import os

import requests

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"  # noqa: S105 - OAuth endpoint, not password


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--code", required=True, help="Authorization code from LinkedIn")
    args = p.parse_args()

    cid = os.environ.get("LINKEDIN_CLIENT_ID")
    csec = os.environ.get("LINKEDIN_CLIENT_SECRET")
    ruri = os.environ.get("LINKEDIN_REDIRECT_URI")

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if not cid or not csec or not ruri:
        msg = (
            "Missing env vars: LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, "
            "LINKEDIN_REDIRECT_URI"
        )
        logger.error(msg)
        return 2

    payload = {
        "grant_type": "authorization_code",
        "code": args.code,
        "redirect_uri": ruri,
        "client_id": cid,
        "client_secret": csec,
    }
    r = requests.post(TOKEN_URL, data=payload, timeout=10)
    logger.info("Status: %s", r.status_code)
    logger.info("%s", r.text)
    return 0


if __name__ == "__main__":
    main()
