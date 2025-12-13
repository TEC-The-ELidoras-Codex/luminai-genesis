#!/usr/bin/env python3
"""
LinkedIn OAuth helper

Usage:
  1. Create a LinkedIn app at https://www.linkedin.com/developers/apps and set
     your redirect URL to http://localhost:8080/callback
  2. Export these environment variables or pass via CLI args: CLIENT_ID, CLIENT_SECRET
  3. Run: python scripts/linkedin_oauth_helper.py
  4. It will open a browser to the authorization URL and capture the code.
  5. It exchanges the code for an Access Token and displays the `access_token` and
     Person URN (urn:li:person:...)

Note: Tokens must be kept secret. Save them to GitHub repo secrets as LINKEDIN_ACCESS_TOKEN
and LINKEDIN_PERSON_URN.
"""

import argparse
import json
import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import requests

DEFAULT_REDIRECT_HOST = "localhost"
DEFAULT_REDIRECT_PORT = 8080
DEFAULT_REDIRECT_PATH = "/callback"

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
ME_URL = "https://api.linkedin.com/v2/me"


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path != args.redirect_path:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        qs = parse_qs(urlparse(self.path).query)
        self.send_response(200)
        self.end_headers()
        if "error" in qs:
            self.wfile.write(b"OAuth returned error, check the console for details.")
            print("OAuth error:", qs.get("error"), qs.get("error_description"))
            sys.exit(1)
        code = qs.get("code", [None])[0]
        if not code:
            self.wfile.write(b"No authorization code found; aborting.")
            print("No code returned, aborting.")
            sys.exit(1)
        self.wfile.write(b"Authorization received - you may close this browser window.")
        # Store code to the server object so main thread can pick it up
        self.server.auth_code = code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LinkedIn OAuth helper; prints access token and person URN",
    )
    parser.add_argument(
        "--client-id",
        dest="client_id",
        help="LinkedIn App Client ID",
        default=os.getenv("LINKEDIN_CLIENT_ID"),
    )
    parser.add_argument(
        "--client-secret",
        dest="client_secret",
        help="LinkedIn App Client Secret",
        default=os.getenv("LINKEDIN_CLIENT_SECRET"),
    )
    parser.add_argument(
        "--redirect-host",
        dest="redirect_host",
        default=DEFAULT_REDIRECT_HOST,
    )
    parser.add_argument(
        "--redirect-port",
        dest="redirect_port",
        type=int,
        default=DEFAULT_REDIRECT_PORT,
    )
    parser.add_argument(
        "--redirect-path",
        dest="redirect_path",
        default=DEFAULT_REDIRECT_PATH,
    )
    parser.add_argument(
        "--scope",
        dest="scope",
        default="w_member_social r_liteprofile",
    )
    parser.add_argument("--no-open", dest="no_open", action="store_true", default=False)
    args = parser.parse_args()

    if not args.client_id or not args.client_secret:
        print(
            "Please provide --client-id and --client-secret (or set env vars "
            "LINKEDIN_CLIENT_ID/LINKEDIN_CLIENT_SECRET)",
        )
        sys.exit(2)

    redirect_uri = (
        f"http://{args.redirect_host}:{args.redirect_port}{args.redirect_path}"
    )

    params = {
        "response_type": "code",
        "client_id": args.client_id,
        "redirect_uri": redirect_uri,
        "scope": args.scope,
    }

    auth_url = (
        AUTH_URL
        + "?"
        + "&".join([f"{k}={requests.utils.quote(v)}" for k, v in params.items()])
    )

    print(
        "Open the following URL in your browser (or wait; the browser will open automatically):",
    )
    print(auth_url)
    if not args.no_open:
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass

    # start local HTTP server to collect redirect and parse code
    server = HTTPServer((args.redirect_host, args.redirect_port), CallbackHandler)
    server.auth_code = None
    print(f"Listening for OAuth redirect at {redirect_uri} ...")
    while server.auth_code is None:
        server.handle_request()

    code = server.auth_code
    print("Authorization code received. Exchanging for access token ...")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": args.client_id,
        "client_secret": args.client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(TOKEN_URL, data=data, headers=headers, timeout=10)
    if r.status_code != 200:
        print("Failed to get access token:", r.status_code, r.text)
        sys.exit(1)
    token_data = r.json()
    access_token = token_data.get("access_token")
    if not access_token:
        print("No access token returned:", token_data)
        sys.exit(1)

    # Get member id
    me_headers = {"Authorization": f"Bearer {access_token}"}
    me = requests.get(ME_URL, headers=me_headers, timeout=10)
    if me.status_code != 200:
        print("Failed to fetch profile:", me.status_code, me.text)
        sys.exit(1)
    me_json = me.json()
    person_id = me_json.get("id")
    if not person_id:
        print("Could not determine the person URN from profile response:", me_json)
        sys.exit(1)

    urn = f"urn:li:person:{person_id}"

    print("\nSUCCESS — Keep these safe:\n")
    print("ACCESS_TOKEN=", access_token)
    print("PERSON_URN=", urn)
    # optionally write to a file for copy-paste convenience
    out_path = os.getenv("LINKEDIN_OAUTH_OUT") or "linkedin_token.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"access_token": access_token, "urn": urn}, f, indent=2)
        print(f"Wrote token info to {out_path}")

    print(
        "\nAdd the access token and urn to your GitHub repository secrets as "
        "LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN",
    )
