#!/usr/bin/env bash
set -euo pipefail

# Prepare an arXiv source tarball for the TGCR paper
# Usage: ./prepare_arxiv_submission.sh

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "1) Compiling PDF via compile.sh (best effort; will continue if LaTeX returns non-zero)"
if [ -x ./compile.sh ]; then
  set +e
  ./compile.sh
  COMP_RC=$?
  set -e
  if [ $COMP_RC -ne 0 ]; then
    echo "[WARN] compile.sh returned non-zero exit code ($COMP_RC). Continuing, but check the PDF after packaging."
  fi
else
  echo "WARN: compile.sh not executable; attempting to run pdflatex directly"
  set +e
  pdflatex -interaction=nonstopmode tgcr.tex
  bibtex tgcr || true
  pdflatex -interaction=nonstopmode tgcr.tex
  pdflatex -interaction=nonstopmode tgcr.tex
  set -e
fi

if [ ! -f tgcr.pdf ]; then
  echo "[ERROR] PDF not found after compile. Please check compilation errors and try again."
  exit 1
fi

PACKAGE_DIR="tgcr_arxiv_package"
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

echo "2) Copying sources into $PACKAGE_DIR"
cp tgcr.tex "$PACKAGE_DIR/"
cp references.bib "$PACKAGE_DIR/" || true
cp tgcr.bbl "$PACKAGE_DIR/" || true
cp tgcr.pdf "$PACKAGE_DIR/" || true
cp -r figures "$PACKAGE_DIR/" || true
cp compile.sh "$PACKAGE_DIR/" || true
cp README.md "$PACKAGE_DIR/" || true

# Remove VCS files and drafts
find "$PACKAGE_DIR" -name ".git" -prune -o -type f -name "*.aux" -delete || true

TARBALL_NAME="tgcr_submission_$(date +%Y%m%d_%H%M%S).tar.gz"
echo "3) Creating tarball: $TARBALL_NAME"
tar -czf "$TARBALL_NAME" -C "$PACKAGE_DIR" .

echo "Done. Tarball created: $ROOT_DIR/$TARBALL_NAME"
echo "Contents:"
tar -tzf "$TARBALL_NAME"

echo "IMPORTANT: Upload this tarball to arXiv via 'Start New Submission' -> Upload Source."
echo "Suggested categories: cs.CE (Primary), cs.AI (Secondary), cs.CY (Tertiary)"
echo "Metadata: Title, Authors, Abstract (see ARXIV_SUBMISSION.md for the recommended fields)."

exit 0
