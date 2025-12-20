PR: maintenance/cleanup-archive → release/prepare-zenodo

## Summary

This PR consolidates archival and launch preparation work, documents provenance and verification steps, and normalizes repository assets to improve reproducibility and discoverability.

## Key changes

- Moved draft/auxiliary files into `archive/` to reduce noise and preserve provenance.
- Consolidated evidence into `docs/evidence/` and standardized media under `docs/evidence/media/`.
- Normalized image filenames (e.g., `efficiency-safety-matrix.png`) and added a placeholder banner (`docs/TEC_BANNER.png`).
- Canonicalized contact information to `KaznakAlpha@elidorascodex.com` across the repo.
- Added `docs/meta-documentation.md` (publication case study) and `docs/PROVENANCE.md` (commit/DOI metadata).
- Updated `README.md` with Quick Start and Evidence-at-a-Glance.

## Verification performed

- Branch: `maintenance/cleanup-archive` (current)
- Commit checksum: `747c11d` (earlier) — latest tip contains subsequent commits up to this PR.
- External link-check: DOIs, GitHub, ORCID, Creative Commons, Calendly, and Substack links successfully resolved (DOIs redirect as expected).
- Local checks: all relative links and images referenced from `README.md` and `docs/meta-documentation.md` verified present.

## Suggested merge message

`chore(cleanup): archive drafts, consolidate evidence, normalize assets, add provenance & verification`

## Reviewer notes

- This PR is intended to be merged as a single unit to preserve a clear provenance snapshot for the Zenodo/OSF deposition flow.
- After merge: (1) run CI/docs build if available; (2) tag a release for Zenodo snapshot (if desired); (3) open `replication-request` issues for public validation.

## Files of interest for quick review

- `docs/meta-documentation.md` — narrative of publication attempts and gatekeeping events
- `docs/PROVENANCE.md` — branch, commit, DOIs, and reproduction steps
- `REPO_CLEANUP.md` — detailed log of file moves and rationale
- `README.md` — Quick Start and Evidence-at-a-Glance

If you'd like, I can add a short CI job to run link-checks on PRs and a release automation step for tagging/Zenodo deposition.
