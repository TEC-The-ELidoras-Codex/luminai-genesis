#!/usr/bin/env bash
# Compile script for tgcr.tex
# Usage: ./compile.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# Check for figure files
MISSING=0
for f in figures/tgcr_diagram.png figures/ai_results.png figures/quantum_setup.png; do
  if [ ! -f "$f" ]; then
    echo "[WARN] Figure not found: $f"
    MISSING=1
  fi
done

if [ $MISSING -eq 1 ]; then
  echo "\nMake sure all figures are in the 'figures/' directory. See figures/README.md for details."
fi

# Check for key tools
if ! command -v pdflatex >/dev/null 2>&1; then
  echo "[ERROR] pdflatex not found. Install a TeX distribution (TeX Live/MiKTeX) or use latexmk."
  exit 1
fi

# Use latexmk if available to run the full cycle, otherwise run the pdflatex/bibtex/pdflatex cycle
if command -v latexmk >/dev/null 2>&1; then
  echo "Found latexmk, using it to build the PDF (fast & robust)."
  latexmk -pdf -quiet tgcr.tex
else
  pdflatex -interaction=nonstopmode tgcr.tex
  bibtex tgcr || true
  pdflatex -interaction=nonstopmode tgcr.tex
  pdflatex -interaction=nonstopmode tgcr.tex
fi

echo "Compiled tgcr.pdf; check the output above for warnings or missing figures."
