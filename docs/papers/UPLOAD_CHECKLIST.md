# Upload Checklist — Consolidated

**This upload checklist has been consolidated into the unified master checklist.**

For the authoritative upload and arXiv submission steps, please see `docs/launch/UNIFIED_MASTER_CHECKLIST.md` (see Phase 7: Validation & Expansion). This file is retained for historical reference.

## arXiv submission

- [ ] Log in to https://arxiv.org and click "Start New Submission".
- [ ] Choose the correct paper source as "LaTeX".
- [ ] Upload `tgcr_submission_*.tar.gz` (or the tarball you created in the previous step).
- [ ] Paste the metadata from `ARXIV_SUBMISSION.md` into the appropriate fields (Title, Authors, Abstract, Categories).
- [ ] Preview the compiled PDF on arXiv (verify figures and formatting look correct).
  - If the preview fails or looks wrong, re-run compile locally, verify `tgcr.pdf`, and upload `tgcr.pdf` as well.
- [ ] Submit and wait for the arXiv confirmation email.

## After Acceptance

- [ ] When arXiv sends the confirmation email with the arXiv ID, paste that ID into `papers/tgcr/ARXIV_SUBMISSION_ID.txt`.
- [ ] Create a GitHub release for the paper and attach the tarball as an artifact (tag name suggestion: `v1.0.0-arxiv-<ID>`).
- [ ] Update the `RELEASE_DRAFT.md` description with the arXiv ID and attach the tarball + `tgcr.pdf` as assets.
- [x] OSF preprint DOI assigned: https://doi.org/10.17605/OSF.IO/XQ3PE (CC-BY 4.0). Include this DOI in release notes and exposé while arXiv/Zenodo IDs are pending.

## Exposé release (Dual Drop protocol)

- [ ] Replace `[ARXIV_ID]` in `EXPOSE_DRAFT.md` with the assigned arXiv ID and finalize the article copy.
- [ ] Publish the exposé (Substack/Medium) and link to the arXiv paper.
- [ ] Post social messages (Twitter/X, LinkedIn) with the suggested short copy in `EXPOSE_DRAFT.md`.

## Audit & Procedure

- [ ] Keep a copy of all uploaded files and tarball locally for audit.
- [ ] If arXiv rejects the compile, re-run the compilation locally on a clean TeX environment and attach `tgcr.pdf` if necessary.
- [ ] Consider re-creating the tarball with fewer LaTeX package dependencies (use precompiled PDF and fewer style packages) if arXiv's compilers still fail.

---

When the arXiv ID exists, notify the team and I'll complete any automation tasks (release, social copy PR, etc.) you request.
