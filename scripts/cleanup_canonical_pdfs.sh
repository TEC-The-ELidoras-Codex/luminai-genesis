#!/usr/bin/env bash
set -euo pipefail

# Move canonical PDF artifacts into private/archives unless they're TEC chapter PDFs.
# Default to dry-run. Use --apply to move files.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=1
APPLY=0

usage() {
  cat <<EOF
Usage: $(basename "$0") [--apply] [--confirm]
--apply: Actually move files using git mv (default is dry-run – recommended)
--confirm: Bypass interactive confirmation when applying
EOF
}

while test $# -gt 0; do
  case "$1" in
    --apply) APPLY=1; DRY_RUN=0; shift ;;
    --confirm) CONFIRM=1; shift ;;
    --help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

ARCHIVE_DIR="$ROOT_DIR/private/archives/canonical_pdf_backup"
mkdir -p "$ARCHIVE_DIR"

# Find canonical PDFs in repo
mapfile -t PDFs < <(cd "$ROOT_DIR" && git ls-files "docs/canonical/*.pdf")

if [ ${#PDFs[@]} -eq 0 ]; then
  echo "No PDF files found under docs/canonical"
  exit 0
fi

# Filter out TEC chapter PDFs (keep them in place) and leave TEC_CODEX_* files as needed
TO_MOVE=()

for f in "${PDFs[@]}"; do
  base=$(basename "$f")
  # Skip TEC chapter PDFs, and skip TEC_CODEX_DUMP.* files
  case "$base" in
    tec-chapter-one*.pdf|TEC_CODEX_DUMP*|tec-chapter-one-refined*.pdf)
      echo "Keeping: $f"
      ;;
    *)
      TO_MOVE+=("$f")
      ;;
  esac
done

if [ ${#TO_MOVE[@]} -eq 0 ]; then
  echo "No canonical PDFs to move. Nothing to do."
  exit 0
fi

echo "Found ${#TO_MOVE[@]} canonical PDFs to move to private/archives:"
for p in "${TO_MOVE[@]}"; do echo "  $p"; done

if [ "$APPLY" -eq 0 ]; then
  echo "Dry-run only. To actually move files, pass --apply (this uses 'git mv' to preserve history where possible)."
  exit 0
fi

# Confirm
if [ -z "${CONFIRM:-}" ]; then
  echo "Are you sure you want to move these files? (y/N)"
  read -r answer
  if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
    echo "Cancelled by user."
    exit 0
  fi
fi

# Move files preserving git history when tracked
for p in "${TO_MOVE[@]}"; do
  src="$ROOT_DIR/$p"
  tgt="$ARCHIVE_DIR/$(basename "$p")"
  mkdir -p "$(dirname "$tgt")"
  # Use git mv when file is tracked
  if git ls-files --error-unmatch "$p" >/dev/null 2>&1; then
    git mv "$src" "$tgt"
  else
    mv "$src" "$tgt"
  fi
  echo "Moved: $p -> $tgt"
done

# Stage the changes
cd "$ROOT_DIR"
if git status --porcelain; then
  git add -A
  git commit -m "chore: move non-TEC canonical PDFs to private/archives to reduce repo noise"
  echo "Committed moves"
else
  echo "No changes to commit"
fi

exit 0
