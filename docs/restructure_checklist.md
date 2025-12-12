# Repository Reorganization Checklist — LuminAI Genesis

This checklist documents the planned repository reorganization and provides a safe, repeatable migration process.

## Goals

- Move draft/private artifacts into a `private/` folder that is ignored by git
- Keep public documentation and code accessible under `docs/`, `src/`, `mvp/`, etc.
- Avoid losing history — use `git mv` where possible and create a separate branch for the migration
- Provide a dry-run mode that lists candidate moves

## Acceptance Criteria

- All public content remains in existing public folders: `docs/streams/articles/ready`, `docs/manifesto`, `docs/launch`, `papers/`, `mvp/`, `backend/`, `src/` etc.
- All drafts (working copies) are moved into `private/drafts/` and `private/worldbuilding/` as appropriate
- The `private/` folder is included in `.gitignore` and not accidentally pushed to remote
- A migration script `scripts/restructure_repo.sh` exists to automates move in a `--apply` step
- Changes are committed on branch `feature/reorganize` and do not modify other branches

## High-level Steps

1. Create a `feature/reorganize` branch and ensure it is up-to-date with `main`.
2. Add `private/` to `.gitignore` and create the `private/` folder structure.
3. Run the migration script in dry-run mode and review the list of suggested moves.
4. Review moves and, if correct, run the script with `--apply` to move files using `git mv`.
5. Run tests (backend `mvp`, Python CI, lint) to ensure no breakages.
6. Push to a remote branch and open a PR for code review.

## Suggested Candidate Paths to Move

- `drafts/` -> `private/drafts/` (existing root-level `drafts` folder)
- `docs/streams/articles/inbox/` -> `private/drafts/` (new drafts inbox, if exists)
- `parts/papers/*draft*` -> `private/drafts/` (paper drafts with `draft` in filename)
- any `*_draft.md` or `draft_*` files at root or `docs/` -> `private/drafts/`

## Notes

- This checklist is intentionally conservative. The `scripts/restructure_repo.sh` script will produce a dry-run listing by default and will only make changes with `--apply`.
- Files in `private/` should remain local-only; if you want to back them up, consider using an encrypted store or a private Git repository.

## Rollback Plan

1. If updates introduced regressions, revert the branch or use `git mv` to restore original paths.
2. If accidental data was moved, use git history to restore or revert commit(s).

---

Created by automation to help plan a safe repo reorg.
