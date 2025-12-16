# OSF Appendix — TGCR / SAR Appendix (Release)

This directory contains the materials prepared for archival upload (OSF / Zenodo) supporting the TGCR Witness Protocol and SAR Benchmark submission.

Summary

- Archive title: TGCR Witness Protocol — NSF Appendix (2025-12-15)
- Contact / PI: Angelo Hurley (replace-with-email)
- DOI / OSF: (add after upload)
- License: CC-BY 4.0 (recommended) — choose an appropriate license when uploading
- Generated: 2025-12-15

Included files

- Markdown source: `docs/nsf/*.md`
- Portable PDFs: `docs/nsf/*.pdf` (generated with `pandoc --pdf-engine=xelatex`)
- Fonts and header used for PDF rendering: `docs/nsf/fonts/` and `docs/nsf/header.tex`
- Evidence placeholders: `docs/evidence/` (logs + screenshots placeholders)
- Archive package: `docs/nsf/osf_appendix_placeholders_with_pdfs.zip`

Why fonts are included

- The `Noto Serif` TrueType fonts are included in `docs/nsf/fonts/` so PDFs are reproducible and render consistently when reviewers extract the archive locally.

Recommended OSF/Zenodo metadata (fill when uploading)

- Title
- Creators (name, affiliation, ORCID if available)
- Description / Abstract
- Keywords: TGCR, SAR, AI safety, crisis response, benchmark
- Funding: NSF SBIR (if applicable)
- License: CC-BY 4.0 (or your chosen license)
- Related identifiers: GitHub repo URL, OSF or Zenodo DOI for preprint

Upload checklist (quick)

1. Confirm sensitive materials are redacted. Replace placeholder logs with redacted copies, if necessary.
2. Preview the PDFs locally: `open docs/nsf/*.pdf` or on Linux `xdg-open`.
3. Upload `osf_appendix_placeholders_with_pdfs.zip` as the primary supplementary file OR upload the unzipped files and attach the ZIP.
4. Fill metadata (title, creators, abstract, license). Add related GitHub repo link.
5. Add a short README (this file) as `README_APPENDIX.md` in the upload.

How to reproduce PDFs locally

1. Ensure `pandoc` and `xelatex` are installed (TeX Live or similar).
2. Install fonts locally (optional but recommended):
   ```bash
   mkdir -p ~/.local/share/fonts && cp docs/nsf/fonts/*.ttf ~/.local/share/fonts/ && fc-cache -f -v ~/.local/share/fonts
   ```
3. Regenerate PDFs:
   ```bash
   for f in docs/nsf/*.md; do
     pandoc "$f" -o "${f%.md}.pdf" --pdf-engine=xelatex --include-in-header=docs/nsf/header.tex -V geometry:margin=1in
   done
   ```

Notes

- Emoji and color-emoji were replaced with ASCII-safe equivalents to ensure LaTeX/PDF portability.
- Some non-ASCII symbols were normalized to ASCII (`->`, `>=`, `approx`, `'`) to remove LaTeX glyph warnings.

If you want me to also open a draft release or create a GitHub Release entry with these artifacts, tell me and I will prepare it.
