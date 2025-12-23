"""Simple LinkedIn token exchange endpoint (Flask).

Usage:
  export LINKEDIN_CLIENT_ID=...
  export LINKEDIN_CLIENT_SECRET=...
  export LINKEDIN_REDIRECT_URI=https://.../linkedin-callback.html
  pip install flask requests
  python scripts/linkedin_exchange.py

Starts a local server exposing POST /exchange-token. The endpoint accepts JSON
payloads like {"code": "..."} and returns the token exchange JSON from
LinkedIn.

Warning: keep client secret in env and do not commit it. Use HTTPS in production.
"""

import logging
import os

import requests
from flask import Flask, jsonify, request

logger = logging.getLogger(__name__)

app = Flask(__name__)

CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("LINKEDIN_REDIRECT_URI")

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"  # noqa: S105 - OAuth endpoint, not password


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/exchange-token", methods=["POST"])
def exchange_token():
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        msg = (
            "missing server configuration (set LINKEDIN_CLIENT_ID, "
            "LINKEDIN_CLIENT_SECRET and LINKEDIN_REDIRECT_URI)"
        )
        return jsonify({"error": msg}), 500
    data = request.get_json(force=True)
    code = data.get("code")
    if not code:
        return jsonify({"error": "missing code"}), 400

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    resp = requests.post(
        TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )

    try:
        resp.raise_for_status()
    except requests.HTTPError:
        logger.exception("LinkedIn token exchange failed")
        return (
            jsonify({"status": "error", "code": resp.status_code, "body": resp.text}),
            resp.status_code,
        )

    return jsonify(resp.json())


if __name__ == "__main__":
    # Bind to localhost by default for development safety
    app.run(host="127.0.0.1", port=8080)
