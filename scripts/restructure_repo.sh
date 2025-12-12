#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=1
APPLY=0

usage() {
  cat <<EOF
Usage: $(basename "$0") [--apply] [--quiet]
--apply: Actually move files using git mv (dangerous) — default is dry-run
--quiet: Only output JSON list of candidate moves
EOF
}

while test $# -gt 0; do
  case "$1" in
    --apply) APPLY=1; DRY_RUN=0; shift ;;
    --quiet) QUIET=1; shift ;;
    --help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

PRIVATE_DIR="$ROOT_DIR/private"
mkdir -p "$PRIVATE_DIR/drafts" "$PRIVATE_DIR/worldbuilding" "$PRIVATE_DIR/characters"

# Candidate patterns (augment this list as needed)
PATTERNS=(
  "$ROOT_DIR/drafts/*"
  "$ROOT_DIR/docs/streams/articles/inbox/*"
  "$ROOT_DIR/docs/drafts/*"
  "$ROOT_DIR/docs/streams/drafts/*"
  "$ROOT_DIR/papers/*draft*"
)

MOVES=()

for p in "${PATTERNS[@]}"; do
  # expand the glob safely
  for f in $p; do
    if [ -e "$f" ]; then
      # Determine target (by default, everything goes to private/drafts)
      base=$(basename "$f")
      if [[ "$f" =~ \.(md|txt|tex|texi)$ || -d "$f" ]]; then
        target="$PRIVATE_DIR/drafts/$base"
        MOVES+=("$f|$target")
      fi
    fi
  done
done

if [ ${#MOVES[@]} -eq 0 ]; then
  if [ "${QUIET:-0}" -ne 1 ]; then
    echo "No candidate moves found. If you have new draft paths, please add them to PATTERNS in this script."
  fi
  exit 0
fi

if [ "${QUIET:-0}" -eq 1 ]; then
  for m in "${MOVES[@]}"; do
    echo "$m"
  done
  exit 0
fi

echo "Found ${#MOVES[@]} candidate moves:" >&2
for m in "${MOVES[@]}"; do
  IFS='|' read -r src tgt <<< "$m"
  echo "  $src -> $tgt"
done

if [ "$APPLY" -eq 1 ]; then
  echo "Applying moves (git mv) — make sure you're on branch 'feature/reorganize' and have committed local changes first." >&2
  for m in "${MOVES[@]}"; do
    IFS='|' read -r src tgt <<< "$m"
    mkdir -p "$(dirname "$tgt")"
    # If the source is tracked by git, use git mv to preserve history.
    if git ls-files --error-unmatch "${src#"${ROOT_DIR}"/}" >/dev/null 2>&1; then
      git mv "$src" "$tgt"
    else
      # Source is untracked — do plain move but do not add to git (private files)
      mv "$src" "$tgt"
    fi
  done
  echo "Applied ${#MOVES[@]} moves. Please review, run tests, and then push." >&2
  exit 0
else
  echo "Dry-run only. To apply moves, run this script with --apply (dangerous)." >&2
fi
