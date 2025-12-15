#!/usr/bin/env python3
"""Simple LinkedIn token exchange endpoint (Flask).

Usage:
  export LINKEDIN_CLIENT_ID=...
  export LINKEDIN_CLIENT_SECRET=...
  export LINKEDIN_REDIRECT_URI=https://.../linkedin-callback.html
  pip install flask requests
  python scripts/linkedin_exchange.py

This starts a local server that exposes POST /exchange-token to accept JSON {"code": "..."}
and performs the server-to-server token exchange with LinkedIn, returning the JSON response.

Warning: keep client secret in environment and do not commit it. Use HTTPS in production.
"""

import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("LINKEDIN_REDIRECT_URI")

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/exchange-token", methods=["POST"])
def exchange_token():
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        return (
            jsonify(
                {
                    "error": "missing server configuration (set LINKEDIN_CLIENT_ID/SECRET/REDIRECT_URI)"
                }
            ),
            500,
        )
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
    )

    try:
        resp.raise_for_status()
    except Exception:
        return (
            jsonify({"status": "error", "code": resp.status_code, "body": resp.text}),
            resp.status_code,
        )

    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
