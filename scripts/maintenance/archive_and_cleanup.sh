#!/usr/bin/env bash
set -euo pipefail

# archive_and_cleanup.sh
# Safe archival + cleanup helper.
# Usage:
#   ./archive_and_cleanup.sh --dry-run
#   ./archive_and_cleanup.sh --apply

DRY_RUN=false
APPLY=false
DATE=$(date +"%Y%m%d-%H%M%S")
ARCHIVE_DIR="archive/cleanup-${DATE}"
BRANCH="chore/cleanup-${DATE}"

# Default patterns to archive (tracked files will be git-moved)
declare -a MOVE_PATTERNS=(
  ".venv"
  "assets/audiovisual"
  "assets/branding"
  "docs/technical/ZOHO_*"
)

usage() {
  echo "Usage: $0 [--dry-run|--apply] [--patterns <comma-separated-list>]"
  exit 1
}

# parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --apply) APPLY=true; shift ;;
    --patterns) IFS=',' read -r -a MOVE_PATTERNS <<< "$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

if [ "$DRY_RUN" = false ] && [ "$APPLY" = false ]; then
  echo "One of --dry-run or --apply is required."; usage
fi

mkdir -p "$ARCHIVE_DIR"

# Collect planned moves
REPORT_FILE="${ARCHIVE_DIR}/cleanup_report_${DATE}.txt"
:> "$REPORT_FILE"

echo "Cleanup report: $REPORT_FILE" | tee -a "$REPORT_FILE"

echo "Planned archival directory: $ARCHIVE_DIR" | tee -a "$REPORT_FILE"

echo "Patterns to move:" | tee -a "$REPORT_FILE"
for p in "${MOVE_PATTERNS[@]}"; do echo "  - $p" | tee -a "$REPORT_FILE"; done

echo "\nScanning for matches..." | tee -a "$REPORT_FILE"

# For each pattern, list matching entries
for p in "${MOVE_PATTERNS[@]}"; do
  echo "\nMatches for pattern: $p" | tee -a "$REPORT_FILE"
  # use git ls-files to find tracked files; fallback to find for untracked
  tracked=$(git ls-files -- "$p" 2>/dev/null || true)
  if [ -n "$tracked" ]; then
    echo "Tracked matches:" | tee -a "$REPORT_FILE"
    echo "$tracked" | sed 's/^/  /' | tee -a "$REPORT_FILE"
  else
    echo "No tracked matches. Searching filesystem..." | tee -a "$REPORT_FILE"
    fsmatches=$(find . -maxdepth 4 -path "./$p" -print 2>/dev/null || true)
    if [ -n "$fsmatches" ]; then
      echo "$fsmatches" | sed 's/^/  /' | tee -a "$REPORT_FILE"
    else
      echo "  (none)" | tee -a "$REPORT_FILE"
    fi
  fi
done

if [ "$DRY_RUN" = true ]; then
  echo "\nDry-run complete. Review $REPORT_FILE and run with --apply to perform archival." | tee -a "$REPORT_FILE"
  exit 0
fi

# APPLY mode: perform git moves for tracked files, filesystem moves for untracked

echo "Applying archival..." | tee -a "$REPORT_FILE"

# create branch
git checkout -b "$BRANCH"

for p in "${MOVE_PATTERNS[@]}"; do
  echo "Processing pattern: $p" | tee -a "$REPORT_FILE"
  tracked=$(git ls-files -- "$p" 2>/dev/null || true)
  if [ -n "$tracked" ]; then
    while IFS= read -r file; do
      target_dir="$ARCHIVE_DIR/$(dirname "$file")"
      mkdir -p "$target_dir"
      echo "git mv -- ""$file"" ""$target_dir"/"" | tee -a "$REPORT_FILE"
      git mv "$file" "$target_dir/"
    done <<< "$tracked"
  else
    # find untracked
    fsmatches=$(find . -maxdepth 4 -path "./$p" -print 2>/dev/null || true)
    if [ -n "$fsmatches" ]; then
      while IFS= read -r f; do
        target_dir="$ARCHIVE_DIR/$(dirname "$f")"
        mkdir -p "$target_dir"
        echo "mv ""$f"" ""$target_dir"/"" | tee -a "$REPORT_FILE"
        mv "$f" "$target_dir/"
      done <<< "$fsmatches"
    fi
  fi
done

# Update .gitignore for .venv and archive dir
if ! grep -q "^\.venv\$" .gitignore 2>/dev/null; then
  echo ".venv" >> .gitignore
  echo ".venv added to .gitignore" | tee -a "$REPORT_FILE"
fi
if ! grep -q "^archive/cleanup-" .gitignore 2>/dev/null; then
  echo "archive/cleanup-*" >> .gitignore
  echo "archive/cleanup-* added to .gitignore" | tee -a "$REPORT_FILE"
fi

# Commit changes
git add .gitignore "$ARCHIVE_DIR"
git commit -m "chore(cleanup): archive large/tracked files to $ARCHIVE_DIR and update .gitignore" || true

# Run pre-commit and tests
if command -v pre-commit >/dev/null 2>&1; then
  echo "Running pre-commit hooks..." | tee -a "$REPORT_FILE"
  pre-commit run --all-files | tee -a "$REPORT_FILE" || true
fi

if command -v pytest >/dev/null 2>&1; then
  echo "Running tests (pytest)..." | tee -a "$REPORT_FILE"
  pytest -q | tee -a "$REPORT_FILE" || true
fi

# Push branch and create PR instruction
git push -u origin "$BRANCH"

echo "Archival completed. Report: $REPORT_FILE" | tee -a "$REPORT_FILE"
echo "A PR branch has been pushed: $BRANCH. Please open a PR for review." | tee -a "$REPORT_FILE"

exit 0
