#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
ARCHIVE_ROOT="$ROOT_DIR/archive/2025-12-20-consolidation"

echo "Archive root: $ARCHIVE_ROOT"
mkdir -p "$ARCHIVE_ROOT/dev-tools" "$ARCHIVE_ROOT/outreach" "$ARCHIVE_ROOT/prototypes" "$ARCHIVE_ROOT/research"

move_if_exists() {
  src="$1"
  dest="$2"
  if [ -e "$src" ]; then
    echo "Moving $src -> $dest"
    mkdir -p "$(dirname "$dest")"
    mv -v "$src" "$dest"
  else
    echo "Not present, skipping: $src"
  fi
}

# Dev tools
move_if_exists "$ROOT_DIR/.github" "$ARCHIVE_ROOT/dev-tools/.github"
move_if_exists "$ROOT_DIR/.vscode" "$ARCHIVE_ROOT/dev-tools/.vscode"
move_if_exists "$ROOT_DIR/.configs" "$ARCHIVE_ROOT/dev-tools/.configs"

# Outreach / launch materials
move_if_exists "$ROOT_DIR/announcements" "$ARCHIVE_ROOT/outreach/announcements"
move_if_exists "$ROOT_DIR/launch" "$ARCHIVE_ROOT/outreach/launch"

# Prototypes and apps
move_if_exists "$ROOT_DIR/backend" "$ARCHIVE_ROOT/prototypes/backend"
move_if_exists "$ROOT_DIR/bots" "$ARCHIVE_ROOT/prototypes/bots"
move_if_exists "$ROOT_DIR/mvp" "$ARCHIVE_ROOT/prototypes/mvp"
move_if_exists "$ROOT_DIR/infrastructure" "$ARCHIVE_ROOT/prototypes/infrastructure"

# Research archives (papers)
move_if_exists "$ROOT_DIR/papers" "$ARCHIVE_ROOT/research/papers"

echo "Consolidation script finished. Review changes and commit."
