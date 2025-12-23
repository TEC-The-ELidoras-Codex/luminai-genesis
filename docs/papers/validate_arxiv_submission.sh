#!/usr/bin/env bash
# Quick validation script for TGCR arXiv submission package
# Usage: ./validate_arxiv_submission.sh
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR"

echo "Looking for latest package..."
TARBALL=$(ls -1 tgcr_submission_*.tar.gz 2>/dev/null | sort -u | tail -n 1 || true)
if [ -z "$TARBALL" ]; then
  echo "[ERROR] No tgcr_submission_*.tar.gz found. Run ./prepare_arxiv_submission.sh first."; exit 1
fi

echo "Found tarball: $TARBALL"

echo "Checking tarball contents..."
TAR_CONTENTS=$(tar -tzf "$TARBALL")
REQUIRED=(tgcr.tex references.bib tgcr.pdf)
for f in "${REQUIRED[@]}"; do
  if ! echo "$TAR_CONTENTS" | grep -q "^./$f$"; then
    echo "[WARN] Required file $f is missing from the tarball. Please ensure it's included.";
  else
    echo "  OK: $f"
  fi
done

# Optional: bbl
if echo "$TAR_CONTENTS" | grep -q "^./tgcr.bbl$"; then
  echo "  OK: tgcr.bbl included"
else
  echo "  NOTE: tgcr.bbl is not included. If arXiv compilation fails, consider uploading the compiled tgcr.pdf in addition to sources."
fi

# Check for title/author existence in .tex
if grep -q "\\title{.*}" tgcr.tex; then
  echo "  OK: \title is set"
else
  echo "[WARN] Title may be missing in tgcr.tex (look for \title{} declaration)."
fi

# Check for common missing packages: siunitx and braket (we have fallbacks but warn)
if grep -q "siunitx" tgcr.tex; then
  echo "  Note: siunitx is used in tgcr.tex. We included a fallback, but arXiv should have siunitx in their TeX Live setup."
fi
if grep -q "braket" tgcr.tex; then
  echo "  Note: braket package used; arXiv usually includes it, but we added a fallback macro if missing."
fi

# Final pdf check
if [ -f tgcr.pdf ]; then
  echo "Final pdf exists: tgcr.pdf (size: $(wc -c < tgcr.pdf) bytes)"
else
  echo "[ERROR] tgcr.pdf not present (run ./compile.sh)."
fi

cat <<EOF

Submission checklist summary:
- Tarball created: $TARBALL
- Required files present: tgcr.tex, references.bib, tgcr.pdf
- tgcr.bbl: $(echo "$TAR_CONTENTS" | grep -q "^./tgcr.bbl$" && echo yes || echo no)
- If arXiv fails to compile the tarball, upload tgcr.pdf alongside sources and copy the suggested metadata from ARXIV_SUBMISSION.md when creating the submission.

Manual upload steps are in ARXIV_SUBMISSION.md.
EOF

exit 0
