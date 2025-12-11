#!/usr/bin/env bash
set -euo pipefail

# Build filing PDFs and package into a zip
ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT_DIR="$ROOT_DIR/docs/legal/filing_package/output"
mkdir -p "$OUT_DIR"

MD_FILES=(
  "$ROOT_DIR/docs/legal/nonprofit_articles.md"
  "$ROOT_DIR/docs/legal/llc_articles.md"
  "$ROOT_DIR/docs/legal/operating_agreement.md"
  "$ROOT_DIR/docs/legal/ip_license_full.md"
)

echo "Converting markdown to PDF (requires pandoc + LaTeX)..."
for md in "${MD_FILES[@]}"; do
  if [ ! -f "$md" ]; then
    echo "Warning: source missing: $md"
    continue
  fi
  base=$(basename "$md" .md)
  out="$OUT_DIR/${base}.pdf"
  pandoc "$md" -o "$out" --pdf-engine=xelatex --metadata title="$base"
  echo "Written $out"
done

# Copy notarization cover
cp "$ROOT_DIR/docs/legal/filing_package/notarization_cover.txt" "$OUT_DIR/"

pushd "$ROOT_DIR/docs/legal/filing_package" > /dev/null
zip -r filing_package.zip output || true
popd > /dev/null

echo "Package created: docs/legal/filing_package/filing_package.zip"
