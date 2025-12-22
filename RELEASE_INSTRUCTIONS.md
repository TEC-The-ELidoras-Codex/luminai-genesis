Release instructions — TGCR (Zenodo integration)

1. Verify the `dist/tgcr_release_20251216.tar.gz` and `papers/tgcr/tgcr.pdf` files are present.
2. On GitHub, create a new Release:
   - Tag: `v1.0.0-arxiv` (or similar)
   - Target: `release/nsf-appendix-2025-12-15` (or `main`)
   - Title: `TGCR: The Theory of General Contextual Resonance — release`
   - Attach `dist/tgcr_release_20251216.tar.gz` and `papers/tgcr/tgcr.pdf` if you prefer manual attachment.
3. Publish the release. Zenodo (if installed) will archive the release and mint a DOI automatically.
4. Once Zenodo creates the DOI, copy it into `papers/tgcr/OSF_DOI.txt` and `papers/tgcr/RELEASE_DRAFT.md` and push a small commit.

Notes:

- The included GitHub Action will attach `dist/tgcr_release_*.tar.gz` and `papers/tgcr/tgcr.pdf` automatically to the GitHub release when it fires (release published event). The action requires `GITHUB_TOKEN` (present by default in GitHub Actions).
- If Zenodo is not already installed, go to https://zenodo.org/account/settings/github/ to enable the GitHub integration and install it for `TEC-The-ELidoras-Codex/luminai-genesis`.
