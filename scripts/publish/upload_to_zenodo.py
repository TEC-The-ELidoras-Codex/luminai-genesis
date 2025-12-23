"""Upload a prepared archive to Zenodo via the REST API.

Usage:
  export ZENODO_TOKEN=your_token_here
  python3 scripts/publish/upload_to_zenodo.py --file /path/to/luminai-genesis-zenodo.zip
    --title "LuminAI Genesis: Witness dataset + analysis"
    --description-file scripts/publish/zenodo_description.md

Notes:
 - This script uses the Zenodo REST API (sandbox or production).
   Set --sandbox to use sandbox.
 - You must set the environment variable ZENODO_TOKEN with a personal access token.
"""

import argparse
import contextlib
import json
import logging
import os
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

ZENODO_API = "https://zenodo.org/api"
ZENODO_SANDBOX = "https://sandbox.zenodo.org/api"


# HTTP status constants
HTTP_BAD_REQUEST = 400


def create_deposition(token: str, *, sandbox: bool = False) -> dict:
    url = (ZENODO_SANDBOX if sandbox else ZENODO_API) + "/deposit/depositions"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, headers=headers, json={}, timeout=10)
    if r.status_code >= HTTP_BAD_REQUEST:
        logger.error("Zenodo API error (create deposition): %s", r.status_code)
        with contextlib.suppress(Exception):
            logger.debug("%s", r.text)
        r.raise_for_status()
    return r.json()


def upload_file(
    deposition: dict,
    filepath: str,
    token: str,
    *,
    _sandbox: bool = False,
) -> dict:
    bucket_url = deposition["links"]["bucket"]
    fname = Path(filepath).name
    with Path(filepath).open("rb") as f:
        # prefer Authorization header to avoid query-encoding and logging tokens
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.put(f"{bucket_url}/{fname}", data=f, headers=headers, timeout=10)
        if r.status_code >= HTTP_BAD_REQUEST:
            logger.error("Zenodo API error (upload file): %s", r.status_code)
            with contextlib.suppress(Exception):
                logger.debug("%s", r.text)
            r.raise_for_status()
    return r.json()


def set_metadata(
    deposition: dict,
    metadata: dict,
    token: str,
    *,
    _sandbox: bool = False,
) -> dict:
    url = (
        ZENODO_SANDBOX if _sandbox else ZENODO_API
    ) + f"/deposit/depositions/{deposition['id']}"
    headers = {"Content-Type": "application/json"}
    data = {"metadata": metadata}
    # prefer Authorization header
    auth_headers = {"Authorization": f"Bearer {token}", **headers}
    r = requests.put(url, data=json.dumps(data), headers=auth_headers, timeout=10)
    if r.status_code >= HTTP_BAD_REQUEST:
        logger.error("Zenodo API error (set metadata): %s", r.status_code)
        with contextlib.suppress(Exception):
            logger.debug("%s", r.text)
        r.raise_for_status()
    return r.json()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, help="Path to zip archive to upload")
    p.add_argument("--title", required=True)
    p.add_argument(
        "--description-file",
        default=None,
        help="Path to markdown description",
    )
    p.add_argument(
        "--authors",
        nargs="*",
        help="Author names (format: 'Family, Given')",
    )
    p.add_argument(
        "--keywords",
        nargs="*",
        default=["LuminAI", "witness", "dataset", "analysis"],
    )
    p.add_argument("--sandbox", action="store_true", help="Use Zenodo sandbox API")
    args = p.parse_args()

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        msg = "Set ZENODO_TOKEN env var before running"
        raise SystemExit(msg)

    desc = ""
    if args.description_file:
        with Path(args.description_file).open(encoding="utf-8") as f:
            desc = f.read()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("Creating deposition...")
    dep = create_deposition(token, sandbox=args.sandbox)
    logger.info("Created deposition id=%s", dep["id"])

    logger.info("Uploading file...")
    upload_file(dep, args.file, token, sandbox=args.sandbox)
    logger.info("File uploaded")

    metadata = {
        "title": args.title,
        "upload_type": "dataset",
        "description": desc,
        "creators": [{"name": a} for a in (args.authors or ["TEC-The-ELidoras-Codex"])],
        "keywords": args.keywords,
    }

    logger.info("Setting metadata...")
    set_metadata(dep, metadata, token, sandbox=args.sandbox)
    logger.info("Metadata set. Visit the deposition in Zenodo to publish and get DOI.")


if __name__ == "__main__":
    main()
