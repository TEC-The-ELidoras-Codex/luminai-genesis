## Meta-Documentation: Gatekeeping Case Study & Research Log

## Summary

This document records a short, important sequence of events around the publication and dissemination of the "Witness Collapse" research (Dec 17–18, 2025). It documents three rejections/blocks, explains why they matter for reproducible research, and links the public evidence required to validate the work.

## Key events

- arXiv: Rejected due to lack of institutional cosigner.
- LessWrong: Post flagged by AI-assistance detection and rejected.
- Claude (AI chat): Safety filter triggered on research text, demonstrating the exact contextual-abandonment failure mode the research documents.

## Why this matters

- The rejections illustrate a structural problem: platforms and venues can (and do) reject reproducible, evidence-based independent research on the basis of tool-use signals or credentialism rather than scientific merit.
- This meta-failure is itself empirical evidence of the core claim: policy and tooling often prioritize liability/aesthetics over contextual presence and real-world safety.

## Repository actions taken

- Consolidated evidence into `docs/evidence/` for reproducible access.
- Archived draft materials under `archive/` to reduce noise and preserve provenance.
- Canonicalized contact info to `KaznakAlpha@elidorascodex.com`.
- Added `REPO_CLEANUP.md` logging all moves and rationale.
- Opened PR: maintenance/cleanup-archive → release/prepare-zenodo (PR #54) with these changes.

## Primary evidence & links

- GitHub repository (code + tests): https://github.com/TEC-The-ELidoras-Codex/luminai-genesis
- OSF preprint: https://doi.org/10.17605/OSF.IO/XQ3PE
- Zenodo archive (snapshot): https://doi.org/10.5281/zenodo.17945827
- Substack posts (published Dec 17–18, 2025):
  - When Safety Filters Abandon Users: https://open.substack.com/pub/polkin/p/when-safety-filters-abandon-users
  - The Tools That Made This Post: https://open.substack.com/pub/polkin/p/the-tools-that-made-this-post-and

## Next steps (recommended)

1. Keep changes on `maintenance/cleanup-archive` until final review and docs build verification.
2. Run a link-check and docs build (local or CI) before merging to `main`/release branch.
3. Solicit independent replications of the SAR benchmark (open an issue labeling `replication-request`).
4. Use this meta-documentation in release notes and the DOI deposit to preserve the publication trail.

## Suggested commit message for merge

`feat(meta): add publication case study & meta-documentation (gatekeeping log)`

## Contact

Angelo "Polkin Rishall" Hurley — KaznakAlpha@elidorascodex.com
ORCID: https://orcid.org/0009-0000-7615-6990

## License & provenance

This file is part of the LuminAI Genesis project and is released under the project's MIT-compatible license. It records factual events and public links for reproducibility and historical record.
