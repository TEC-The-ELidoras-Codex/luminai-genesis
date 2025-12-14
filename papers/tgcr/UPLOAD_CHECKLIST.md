# TGCR Upload Checklist — Final

Use this checklist to complete the manual arXiv submission and to follow the Dual Drop Protocol.

## Local pre-checks

- [ ] Ensure repository is on the intended branch (e.g., `main` or `recovery/restore-deleted-20251213`) and changes are committed.
- [ ] Re-run `./prepare_arxiv_submission.sh` in `papers/tgcr` to generate the latest tarball (note its name).
- [ ] Run `./validate_arxiv_submission.sh` and confirm the following are present:
  - tgcr.tex
  - references.bib
  - tgcr.pdf
  - tgcr.bbl (recommended)

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
