TGCR — The Theory of General Contextual Resonance

Contents

- `tgcr.tex` — LaTeX source
- `references.bib` — Bibliography file
- `compile.sh` — Compile script (pdflatex/bibtex cycle)
- `figures/` — Figures for the paper

Quick compile

1. Ensure LaTeX is installed (TeXLive or MiKTeX) with `pgfplots`, `tikz`, and `natbib` packages.

Install on Debian/Ubuntu (example):

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-latex-extra texlive-pictures texlive-fonts-recommended latexmk
```

Install on macOS with MacTeX (example):

```bash
brew install --cask mactex-no-gui
# or use MacTeX full installer
```

2. Place high-resolution (300 dpi) PNG images named `tgcr_diagram.png`, `ai_results.png`, and `quantum_setup.png` in the `figures/` directory.

Run the compile script:

```bash
cd papers/tgcr
./compile.sh
```

If you prefer a single command with latexmk (recommended if installed):

````bash
latexmk -pdf tgcr.tex

Author and ORCID
-----------------
Angelo Hurley — https://orcid.org/0009-0000-7615-6990

WordPress (Gutenberg) publishing
---------------------------------
Add a markdown file under `docs/streams/articles/ready/` with the following frontmatter and body, then run `python3 scripts/aqueduct_build_wordpress_html.py` to generate a ready HTML file in `dist/wordpress`:

```yaml
title: "The Theory of General Contextual Resonance (TGCR)"
slug: tgcr
date: 2025-12-11
author: Angelo Hurley
orcid: https://orcid.org/0009-0000-7615-6990
channels: [wordpress]
````

Import `dist/wordpress/tgcr.html` into WordPress via the Gutenberg block editor (HTML or custom HTML block).

```

ArXiv Submission Notes

- ArXiv accepts source TAR/GZ containing `.tex` and `.bib` and a `figures` directory with the image files.
- Figures should be EPS, PDF, PNG, or JPG; PDFs are preferred for vector artwork.
- Optimize images for quality + compact size.

Appendix

- This repo contains a simple fallback rendering in `tgcr.tex` for missing images. Replace the placeholder boxes with real figures to get full-quality output.
```
