## Provenance and Build Metadata

This file records the provenance for the current state of the repository and the publication materials associated with the LuminAI Genesis project.

## Commit / branch

- Branch: `maintenance/cleanup-archive`
- Commit (short): `747c11d`
- Date (UTC): 2025-12-18

## Canonical identifiers

- OSF preprint: https://doi.org/10.17605/OSF.IO/XQ3PE
- Zenodo snapshot: https://doi.org/10.5281/zenodo.17945827

## Tools and environment (high level)

- Git (commit history records edits)
- Python 3.x (scripts and tests)
- curl (link verification)
- Substack / OSF / Zenodo (publication & archiving)

## Provenance notes

- `docs/evidence/` contains the canonical evidence artifacts used for replication and the SAR benchmark.
- `docs/meta-documentation.md` documents publication attempts and gatekeeping events.
- All contact information has been canonicalized to `KaznakAlpha@elidorascodex.com` in this branch.

## How to reproduce this build/verification

1. Check out the branch: `git checkout maintenance/cleanup-archive`
2. Confirm commit: `git rev-parse --short HEAD` (expected `747c11d`)
3. Run the SAR benchmark: `benchmarks/dye_die_filter/run_tests.py`
4. Run link-checks: see `scripts/link_check.sh` (or use the commands in the repo README)

## Notes

This file is intentionally minimal; it provides a snapshot of key identifiers and high-level steps to reproduce verification activities. For a full audit trail, inspect the repository commit history and `REPO_CLEANUP.md`.
