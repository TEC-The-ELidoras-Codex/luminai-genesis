#!/usr/bin/env bash
# Helper: attempt to capture a full-screen screenshot and save to docs/evidence/responses/
# Usage: ./scripts/capture_twitter_thread.sh [optional-filename-suffix]

set -euo pipefail

OUTDIR="$(dirname "${BASH_SOURCE[0]}")/../docs/evidence/responses"
mkdir -p "$OUTDIR"

SUFFIX="${1:-thread}"
TS=$(date +%Y%m%d_%H%M%S)
OUTFILE="$OUTDIR/${TS}_twitter_${SUFFIX}.png"

if command -v import >/dev/null 2>&1; then
  import -window root "$OUTFILE" && echo "Saved $OUTFILE"
  exit 0
fi

if command -v gnome-screenshot >/dev/null 2>&1; then
  gnome-screenshot -f "$OUTFILE" && echo "Saved $OUTFILE"
  exit 0
fi

echo "No supported screenshot tool found. Please take a screenshot manually and save to: $OUTFILE" >&2
exit 2
