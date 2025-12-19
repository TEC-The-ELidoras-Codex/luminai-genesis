Title: chore(cleanup): archive old drafts and consolidate evidence/media

## Summary

This pull request consolidates old draft artifacts and generated exports into an `archive/` folder, standardizes evidence and media under `docs/evidence/`, and updates `.gitignore` to avoid committing generated PDF exports.

## Why

- Reduces noise in the `docs/` tree and makes canonical artifacts easier to find.
- Ensures launch materials reference a single evidence location (`docs/evidence/`).
- Preserves history by using `git mv` for all relocations.

## What changed (high level)

- Archived chapter drafts: `archive/drafts/tec-chapter-one/`
- Archived generated NSF exports: `archive/nsf/*.md.pdf`
- Moved dye-die evidence to `docs/evidence/`
- Moved ZOHO evidence images to `docs/evidence/media/`
- Moved top-level `docs/PRIVACY_POLICY.md` to `archive/legal/` (canonical: `docs/legal/privacy_policy.md`)
- Added `REPO_CLEANUP.md` documenting the moves
- Updated `.gitignore` to exclude `*.md.pdf` and `*-v*.pdf`

## Files of note (examples)

- `docs/evidence/dye-die-filter-failure.json` (moved from `docs/technical`)
- `docs/evidence/dye-die-filter-failure.md` (moved from `docs/technical`)
- `docs/evidence/media/ZOHO_FAILURE_SENT.jpeg`
- `archive/drafts/tec-chapter-one/tec-chapter-one-v1.md` (and v2/v3)
- `REPO_CLEANUP.md` (new)

## Testing / Validation

1. Confirm branch `maintenance/cleanup-archive` contains these moves (already pushed).
2. Run a local search for the old paths to identify any remaining references:

   - `grep -R "docs/technical/dye-die-filter-failure" -n`

3. Optionally run docs build / GitHub Pages preview to verify links and images render correctly.

## Merge plan

- Target branch: `release/prepare-zenodo` (as discussed). After CI/docs verification, merge into `release/prepare-zenodo` and optionally to `main`.

## Notes

- No files were permanently deleted except `docs/press-kit/press-onepager.pdf` which was outdated; all other items were moved with `git mv` preserving history.
- If you'd like different archive paths (e.g., under `docs/archive/`), I can update before merging.

## Next steps

1. Review changes in this PR and validate links.
2. Merge when satisfied; consider running a docs build post-merge.

Requested reviewers: @TEC-The-ELidoras-Codex (repo admins)
