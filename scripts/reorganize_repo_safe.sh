#!/usr/bin/env bash
set -euo pipefail

# reorganize_repo_safe.sh — SAFE reorganization script
# - Dry-run by default, apply only with --apply
# - Uses `git mv` for tracked files to preserve history
# - Skips files that should remain at repo root (README, LICENSE, Dockerfile, etc.)
# - Provides an explicit commit message when applying

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=1
APPLY=0
CONFIRM=0
MOVE_CODE=0

usage() {
  cat <<EOF
Usage: $(basename "$0") [--apply] [--confirm]
--apply: actually perform moves (dangerous)
--confirm: bypass interactive confirmation when applying
--help: show this message
EOF
}

while test $# -gt 0; do
  case "$1" in
    --apply) APPLY=1; DRY_RUN=0; shift ;;
    --move-code) MOVE_CODE=1; shift ;;
    --confirm) CONFIRM=1; shift ;;
    --help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

# Directories to create
TARGET_DIRS=(
  "$ROOT_DIR/core/src"
  "$ROOT_DIR/core/backend"
  "$ROOT_DIR/core/bots"
  "$ROOT_DIR/core/models"
  "$ROOT_DIR/docs/technical"
  "$ROOT_DIR/docs/legal"
  "$ROOT_DIR/docs/lore"
  "$ROOT_DIR/docs/launch"
  "$ROOT_DIR/private/drafts"
  "$ROOT_DIR/private/worldbuilding"
  "$ROOT_DIR/assets/branding"
  "$ROOT_DIR/assets/audiovisual"
  "$ROOT_DIR/assets/social"
  "$ROOT_DIR/scripts"
  "$ROOT_DIR/.configs"
  "$ROOT_DIR/dist"
  "$ROOT_DIR/build"
)

# Files and folders that should stay at the repository root (do not move)
KEEP_ROOT=(
  README.md
  LICENSE
  .gitignore
  docker-compose.yml
  Dockerfile.ci-example
  Dockerfile.discord
  .github
  .vscode
  .github/workflows
  package.json
  pyproject.toml
)

# Mapping — from -> to
# Use arrays for source pattern and destination
MAP_SRC=(
  "backend"
  "bots"
  "src"
  "models"
  "docs/canonical"
  "docs/evidence"
  "docs/governance"
  "docs/hr"
  "docs/technical"
  "docs/manifesto"
  "docs/lore"
  "docs/operations"
  "docs/streams"
  "docs/quantum-security"
  "docs/launch"
  "docs/posts"
  "private"
  "drafts"
  "assets/branding"
  "assets/audiovisual"
  "assets/social"
  "scripts"
)

MAP_DEST=(
  "core/backend"
  "core/bots"
  "core/src"
  "core/models"
  "docs/technical"
  "docs/technical"
  "docs/technical"
  "docs/technical"
  "docs/technical"
  "docs/lore"
  "docs/lore"
  "docs/technical"
  "docs/launch"
  "docs/launch"
  "docs/launch"
  "docs/launch"
  "private"
  "private/drafts"
  "assets/branding"
  "assets/audiovisual"
  "assets/social"
  "scripts"
)

# Which items in MAP_SRC are code (controversial to move). Controlled by --move-code flag.
CODE_ITEMS=("backend" "bots" "src" "models")

# Config & top-level files to move to .configs (but exclude README.md, LICENSE)
CONFIG_FILES=(
  "CONTRIBUTING.md"
  "DEPLOYMENT_CHECKLIST.md"
  "ENV-README.md"
  "LAUNCH_ACTION_ITEMS.txt"
  "pytest.ini"
  "requirements.txt"
  "setup.sh"
  "setup_amd_pytorch.sh"
  "TEC_STARTER_PACK_INDEX.md"
  "LOCAL_GPU_TRAINING.md"
  "UBUNTU_CHEATSHEET.md"
)

# CLI to produce the dry-run list in a safe way
MOVES=()
SKIPPED=()

# Ensure target directories exist
for d in "${TARGET_DIRS[@]}"; do
  mkdir -p "$d"
done

# Function to check if file should be kept in root
should_keep_root() {
  local f="$1"
  for k in "${KEEP_ROOT[@]}"; do
    if [[ "$f" == "$k" || "$f" == "$k"/* ]]; then
      return 0
    fi
  done
  return 1
}

# Build moves mapping based on MAP_SRC / MAP_DEST
  for i in "${!MAP_SRC[@]}"; do
  src="${MAP_SRC[$i]}"
  dst="${MAP_DEST[$i]}"
    # Skip moving code directories unless MOVE_CODE is enabled
    if [[ "$MOVE_CODE" -eq 0 ]]; then
      skip=0
      for c in "${CODE_ITEMS[@]}"; do
        if [[ "$src" == "$c" ]]; then
          skip=1
          break
        fi
      done
      if [[ "$skip" -eq 1 ]]; then
        # Keep code entries unchanged and add to skipped list
        if [ -e "$ROOT_DIR/$src" ]; then
          for path in "$ROOT_DIR/$src"/*; do
            if [ -e "$path" ]; then
              name="$(basename "$path")"
              rel="$src/$name"
              SKIPPED+=("$rel")
            fi
          done
        fi
        continue
      fi
    fi

  if [ -e "$ROOT_DIR/$src" ]; then
    for path in "$ROOT_DIR/$src"/*; do
      if [ -e "$path" ]; then
        name="$(basename "$path")"
        # don't move if the file should be kept at root
        rel="$src/$name"
        if should_keep_root "$name"; then
          SKIPPED+=("$rel")
          continue
        fi
        MOVES+=("$rel|$dst/$name")
      fi
    done
  fi
done

# Add config file moves
for cf in "${CONFIG_FILES[@]}"; do
  if [ -e "$ROOT_DIR/$cf" ]; then
    # allow keeping certain root files that are required (e.g., README.md)
    if should_keep_root "$cf"; then
      SKIPPED+=("$cf")
    else
      MOVES+=("$cf|.configs/$cf")
    fi
  fi
done

# Scripts in root and top-level scripts directory
for p in "$ROOT_DIR"/*.sh "$ROOT_DIR"/*.py; do
  if [ -e "$p" ]; then
    b="$(basename "$p")"
    if should_keep_root "$b"; then
      SKIPPED+=("$b")
    else
      MOVES+=("$b|scripts/$b")
    fi
  fi
done

# Deduplicate MOVES and SKIPPED
unique() {
  awk '!x[$0]++'
}

MOVES=( $(printf "%s\n" "${MOVES[@]}" | unique) )
SKIPPED=( $(printf "%s\n" "${SKIPPED[@]}" | unique) )

if [ ${#MOVES[@]} -eq 0 ]; then
  echo "No candidate moves found"
  exit 0
fi

# Print summary
cat <<EOF
Reorganize repo dry-run summary:

Found ${#MOVES[@]} paths to move:
EOF
for m in "${MOVES[@]}"; do
  IFS='|' read -r s t <<< "$m"
  echo "  $s -> $t"
done

if [ ${#SKIPPED[@]} -gt 0 ]; then
  echo "\nSkipped (kept at repo root):"
  for s in "${SKIPPED[@]}"; do echo "  $s"; done
fi

# Show stats
echo "\nTo apply the changes run: $0 --apply"

if [ "$APPLY" -eq 0 ]; then
  exit 0
fi

# Confirm before applying
if [ "$CONFIRM" -eq 0 ]; then
  read -p "Apply these moves? (y/N): " reply
  if [[ "$reply" != "y" && "$reply" != "Y" ]]; then
    echo "Cancelled by user"
    exit 0
  fi
fi

# Now apply moves using git mv when possible
cd "$ROOT_DIR"
for m in "${MOVES[@]}"; do
  IFS='|' read -r s t <<< "$m"
  src="$ROOT_DIR/$s"
  tgt="$ROOT_DIR/$t"
  mkdir -p "$(dirname "$tgt")"
  if [ "$src" == "$tgt" ]; then
    echo "Skipping move because source and target are identical: $src"
    continue
  fi
  if [ ! -e "$src" ]; then
    echo "Source missing (skipping): $src"
    continue
  fi
  if git ls-files --error-unmatch "$s" >/dev/null 2>&1; then
    git mv "$s" "$tgt"
  else
    mv "$s" "$tgt"
  fi
done

# Move config files into .configs if any
if [ -e ".configs" ]; then
  git add -A || true
  git commit -m "chore: reorganize repo into core/docs/.configs structure" || true
  echo "Committed reorganization. Review changes locally and push when ready"
fi

exit 0
