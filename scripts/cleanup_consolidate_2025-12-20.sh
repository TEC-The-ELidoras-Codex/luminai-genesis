#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
ARCHIVE_DIR="$ROOT_DIR/archive/2025-12-20-pre-consolidation"

echo "Creating archive dir: $ARCHIVE_DIR"
mkdir -p "$ARCHIVE_DIR"

move_if_exists() {
  local src="$1"
  local dest="$2"
  if [ -e "$src" ]; then
    echo "Moving $src -> $dest"
    mkdir -p "$(dirname "$dest")"
    mv -v "$src" "$dest"
  else
    echo "Skipping missing: $src"
  fi
}

# 1) Archive cruft (safe: only if exists)
move_if_exists "$ROOT_DIR/recovery" "$ARCHIVE_DIR/recovery"
move_if_exists "$ROOT_DIR/private" "$ARCHIVE_DIR/private"
move_if_exists "$ROOT_DIR/build" "$ARCHIVE_DIR/build"
move_if_exists "$ROOT_DIR/.configs" "$ARCHIVE_DIR/.configs"
move_if_exists "$ROOT_DIR/k8s" "$ARCHIVE_DIR/k8s"
move_if_exists "$ROOT_DIR/infrastructure" "$ARCHIVE_DIR/infrastructure"

# 2) Consolidate scattered content into docs/
mkdir -p "$ROOT_DIR/docs/launch"
if [ -d "$ROOT_DIR/announcements" ]; then
  echo "Moving announcements -> docs/launch/"
  mv -v "$ROOT_DIR/announcements"/* "$ROOT_DIR/docs/launch/" || true
fi

if [ -d "$ROOT_DIR/launch/launch_kit" ]; then
  echo "Moving launch/launch_kit -> docs/launch/"
  mv -v "$ROOT_DIR/launch/launch_kit"/* "$ROOT_DIR/docs/launch/" || true
fi

mkdir -p "$ROOT_DIR/docs/papers"
if [ -d "$ROOT_DIR/papers/tgcr" ]; then
  echo "Moving papers/tgcr -> docs/papers/"
  mv -v "$ROOT_DIR/papers/tgcr"/* "$ROOT_DIR/docs/papers/" || true
fi

# 3) Ensure site/ exists (public-facing)
mkdir -p "$ROOT_DIR/site"

echo "Cleanup script finished. Review git status and commit changes."
