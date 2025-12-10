Launch bundle for publishing

This folder contains a lightweight manifest and instructions for publishing the Substack post and associated audit artifacts.

Contents:

- `launch_manifest.csv` — CSV listing core artifacts and file paths.
- `README.md` — this file.

Guidance:

1. Review `launch_manifest.csv` for the canonical PDF (Substack draft) and the audit bundle path.
2. When publishing, reference the `audit/evidence_bundle.zip` to provide reproducible artifacts (checksums are in `audit/hashes.txt`).
3. If you need to host the audit bundle externally, upload `audit/evidence_bundle.zip` to your storage and update the `url` field in `launch_manifest.csv`.
