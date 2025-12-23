#!/usr/bin/env python3
"""Check Zenodo for a DOI for the TGCR GitHub release and update repo files when found.

Behavior:
 - Query Zenodo API for records referencing the GitHub release URL
 - If a DOI (record['doi'] or record['conceptdoi']) is found and not yet recorded in repo files,
   update `papers/tgcr/RELEASE_DRAFT.md`, `papers/tgcr/EXPOSE_DRAFT.md`, and
   `papers/tgcr/ARXIV_SUBMISSION_ID.txt` by appending the Zenodo DOI line and commit the change
   directly to the `main` branch (via git) so the repository reflects permanence.

Run locally for testing or run in CI with `GITHUB_TOKEN` available.
"""

import json
import logging
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

REPO = "https://github.com/TEC-The-ELidoras-Codex/luminai-genesis"
ZENODO_SEARCH = "https://zenodo.org/api/records/?q={}&size=20"  # URL-encoded query


def query_zenodo(term: str):
    q = urllib.parse.quote_plus(term)
    url = ZENODO_SEARCH.format(q)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "luminai-zenodo-check/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data


def extract_doi_from_results(data, repo_url: str):
    hits = data.get("hits", {}).get("hits", [])
    for hit in hits:
        metadata = hit.get("metadata", {})
        # Check for direct doi fields first
        doi = metadata.get("doi") or hit.get("doi") or hit.get("conceptdoi")
        # Inspect related identifiers or links to find a matching GitHub repo/release
        rel = metadata.get("related_identifiers", []) or []
        urls = []
        for r in rel:
            urls.append(r.get("identifier", ""))
        # Also check 'urls' field
        for link in metadata.get("urls", []):
            urls.append(link.get("url", ""))

        if any(repo_url in u for u in urls):
            return doi

    return None


def already_recorded(doi: str) -> bool:
    files = [
        Path("papers/tgcr/RELEASE_DRAFT.md"),
        Path("papers/tgcr/EXPOSE_DRAFT.md"),
        Path("papers/tgcr/ARXIV_SUBMISSION_ID.txt"),
    ]
    for f in files:
        if f.exists():
            text = f.read_text(encoding="utf-8")
            if doi in text:
                return True
    return False


def append_doi(doi: str):
    note = f"\n- Zenodo DOI: https://doi.org/{doi}\n"
    rd = Path("papers/tgcr/RELEASE_DRAFT.md")
    ed = Path("papers/tgcr/EXPOSE_DRAFT.md")
    idf = Path("papers/tgcr/ARXIV_SUBMISSION_ID.txt")

    if rd.exists():
        rd.write_text(
            rd.read_text(encoding="utf-8")
            + "\n"
            + f"Zenodo DOI: https://doi.org/{doi}\n",
        )
    if ed.exists():
        ed.write_text(
            ed.read_text(encoding="utf-8")
            + "\n"
            + f"Zenodo DOI: https://doi.org/{doi}\n",
        )
    if idf.exists():
        idf.write_text(
            idf.read_text(encoding="utf-8")
            + "\n"
            + f"Zenodo DOI: https://doi.org/{doi}\n",
        )


def git_commit_and_push(doi: str):
    msg = f"chore(tgcr): add Zenodo DOI https://doi.org/{doi}"
    subprocess.run(
        [
            "git",
            "add",
            "papers/tgcr/RELEASE_DRAFT.md",
            "papers/tgcr/EXPOSE_DRAFT.md",
            "papers/tgcr/ARXIV_SUBMISSION_ID.txt",
        ],
        check=False,
    )
    subprocess.run(["git", "commit", "-m", msg], check=False)
    # Push directly to main (the workflow will run with a token that has write access)
    subprocess.run(["git", "push", "origin", "main"], check=False)


def main():
    try:
        data = query_zenodo("luminai-genesis")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        logger.exception("Error querying Zenodo: %s", e)
        sys.exit(1)
    doi = extract_doi_from_results(data, REPO)
    if not doi:
        logger.info("No Zenodo DOI found yet; will check again later.")
        return 0

    doi = doi.replace("https://doi.org/", "").strip()
    logger.info("Found DOI: %s", doi)
    if already_recorded(doi):
        logger.info("DOI already recorded in repository files.")
        return 0

    append_doi(doi)
    git_commit_and_push(doi)
    logger.info(
        "Added Zenodo DOI https://doi.org/%s to release & exposé files and pushed to main.",
        doi,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
