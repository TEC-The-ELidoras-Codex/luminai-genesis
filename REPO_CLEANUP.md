# Repository Cleanup Log

This file documents the maintenance/cleanup-archive branch operations performed on 2025-12-18.

Purpose: archive old drafts and generated artifacts, consolidate evidence and media under `docs/evidence/`, and reduce clutter before release.

Summary of actions (performed)

- Branch created: `maintenance/cleanup-archive`
- Archive directories created:

  - `archive/drafts/tec-chapter-one/`
  - `archive/nsf/`
  - `archive/media/` (not used)
  - `archive/fonts/` (reserved)
  - `archive/legal/`

- Files moved (git mv):

  1. Chapters/drafts

     - `docs/technical/tec-chapter-one-v1.md` -> `archive/drafts/tec-chapter-one/tec-chapter-one-v1.md`
     - `docs/technical/tec-chapter-one-v2.md` -> `archive/drafts/tec-chapter-one/tec-chapter-one-v2.md`
     - `docs/technical/tec-chapter-one-v3.md` -> `archive/drafts/tec-chapter-one/tec-chapter-one-v3.md`

  2. NSF generated PDF exports

     - `docs/nsf/Clinical_Validation_MentalHealth.md.pdf` -> `archive/nsf/Clinical_Validation_MentalHealth.md.pdf`
     - `docs/nsf/Submission_Instructions.md.pdf` -> `archive/nsf/Submission_Instructions.md.pdf`
     - `docs/nsf/PI_Biosketch_Angelo_Hurley.md.pdf` -> `archive/nsf/PI_Biosketch_Angelo_Hurley.md.pdf`
     - `docs/nsf/Budget_and_Justification.md.pdf` -> `archive/nsf/Budget_and_Justification.md.pdf`

  3. Evidence consolidation

     - `docs/technical/dye-die-filter-failure.json` -> `docs/evidence/dye-die-filter-failure.json`
     - `docs/technical/dye-die-filter-failure.md` -> `docs/evidence/dye-die-filter-failure.md`

  4. Media moved into evidence

     - `docs/technical/ZOHO_FAILURE_SENT.jpeg` -> `docs/evidence/media/ZOHO_FAILURE_SENT.jpeg`
     - `docs/technical/ZOHO_KEYWORD_FAILURE.png` -> `docs/evidence/media/ZOHO_KEYWORD_FAILURE.png`

  5. Privacy policy consolidation

     - `docs/PRIVACY_POLICY.md` -> `archive/legal/PRIVACY_POLICY.md` (canonical retained: `docs/legal/privacy_policy.md`)

  6. Other removals
     - `docs/press-kit/press-onepager.pdf` was removed in this branch (was a duplicate/outdated file).

Notes & rationale

- All moves used `git mv` so history is preserved. Nothing was permanently deleted except explicitly removed press artifacts noted above.
- Canonical retained copies:
  - Chapters: `docs/lore/chapters/tec-chapter-two-clean-break.md`, `docs/lore/chapters/tec-chapter-three-everything-burns.md`, and `docs/technical/tec-chapter-one-Final.pdf` are unchanged and considered canonical.
  - Privacy policy canonical location: `docs/legal/privacy_policy.md` (used by docs site and Pages deployment).
  - Evidence canonical path: `docs/evidence/` (now includes dye-die assets and media subfolder).

Next steps (after merge/approval)

1. Verify site references and links via a local docs build (or GitHub Pages preview). Run the docs build and confirm images and evidence links resolve.
2. Consider adding `archive/` to `docs/README.md` or repository index to document retained historical drafts.
3. Optionally remove older HTML redirect pages if Pages will point to canonical files only.
4. When ready, open a PR from `maintenance/cleanup-archive` to `release/prepare-zenodo` (done) and merge after review.

Maintainer: Angelo "Polkin" Hurley (or repo owner) — approved 2025-12-18
