Repo cleanup checklist — chore/outreach-anthropic

Objective: tidy up temporary files, verify release artifacts, and ensure the outreach branch is clean for publication.

Steps:

1. Run pre-commit hooks and autoformatters (black/isort, markdownlint)
   - `pre-commit run --all-files`
2. Run tests
   - `python -m pytest -q`
3. Remove or move large unused media into `archive/` and annotate origin in `archive/MEDIA_README.md`.
   - e.g., `assets/audiovisual/A_Structural_Insurrection.mp4` appears deleted on some branches — verify intent.
4. Verify DOI and release notes link consistency (CITATION.cff, docs/witness-threshold/RELEASE_NOTES_v5.0.md)
5. Ensure `docs/substack/post-templates/*` includes canonical versions of all chapters
6. Create `docs/substack/PUBLISHING_GUIDE.md` with instructions for Substack posting and canonical captions
7. Update `README.md` and `docs/index.md` to include links to the Replication Hub and Substack posts

If you want, I can run steps 1–3 and open a PR with the cleanup changes; confirm and I'll proceed.
