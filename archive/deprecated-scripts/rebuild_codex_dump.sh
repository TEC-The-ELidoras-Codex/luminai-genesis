#!/usr/bin/env bash
# LuminAI Genesis — Rebuild TEC_CODEX_DUMP from canonical bundles

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL_DIR="$ROOT_DIR/docs/canonical"

BUNDLES=(
  "01-bundle.md"
  "02-bundle.md"
  "03-bundle.md"
  "04-bundle.md"
  "05-bundle.md"
  "06-bundle.md"
  "07-bundle.md"
  "08-bundle.md"
  "09-bundle.md"
  "10-bundle.md"
  "11-bundle.md"
  "12-bundle.md"
)

OUT="$CANONICAL_DIR/TEC_CODEX_DUMP.md"

echo "📜 Rebuilding TEC_CODEX_DUMP.md from bundles..."
: > "$OUT"

for f in "${BUNDLES[@]}"; do
  if [[ -f "$CANONICAL_DIR/$f" ]]; then
    cat "$CANONICAL_DIR/$f" >> "$OUT"
    printf "\n\n" >> "$OUT"
  else
    echo "⚠️ Missing bundle: $f (skipping)"
  fi
done

echo "✅ Wrote $OUT"
