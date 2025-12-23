#!/usr/bin/env bash
set -euo pipefail

# Prepare a zip archive containing the launch kit, research docs, data, and analysis scripts
# for upload to Zenodo. This script avoids adding large private folders.
# Usage:
#   ./scripts/publish/prepare_zenodo_package.sh --out /tmp/luminai-genesis-zenodo.zip

OUT="${1:-build/luminai-genesis-zenodo.zip}"
ROOT_DIR="$(cd "$(dirname "$0")/../../" && pwd)"

# Files/dirs to include (workspace-relative)
INCLUDE=(
  launch/launch_kit
  docs/research
  docs/research/witness_data
  scripts/analysis
  README.md
  CITATION.cff
  LICENSE
  pyproject.toml
)

# Warn about sensitive drafts
echo "Marking drafts: docs/research/chronology_of_harm.md is kept but flagged DRAFT in metadata"

if [[ "$OUT" = /* ]]; then
  OUT_ABS="$OUT"
else
  OUT_ABS="$ROOT_DIR/$OUT"
fi
mkdir -p "$(dirname "$OUT_ABS")"
cd "$ROOT_DIR"

# Create a temporary directory to stage files
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

for p in "${INCLUDE[@]}"; do
  if [ -e "$p" ]; then
    mkdir -p "$TMPDIR/$(dirname "$p")"
    cp -r "$p" "$TMPDIR/$p"
  fi
done

# Add a small README for the Zenodo package
cat > "$TMPDIR/zenodo_README.txt" <<'EOF'
This archive contains the launch kit, outreach materials, research notes, the witness dataset, 
and analysis scripts for the LuminAI Genesis project. 

Files that may contain sensitive allegations are marked DRAFT (do not publish without legal/ethics review):
 - docs/research/chronology_of_harm.md

If you intend to publish, obtain legal/ethics sign-off first.
EOF

# Create zip using Python's shutil (more portable than system zip)
cd "$TMPDIR"
python3 - <<PYCODE
import shutil, os
tmp = os.getcwd()
out = os.path.abspath(os.environ['OUT_ABS'])
out_dir = os.path.dirname(out)
os.makedirs(out_dir, exist_ok=True)
base = os.path.splitext(os.path.basename(out))[0]
shutil.make_archive(os.path.join(out_dir, base), 'zip', tmp)
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
logger.info('Created package: %s', out)
PYCODE

echo "Created package: $OUT_ABS"
