#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "🧹 Cleaning repository root..."
rm -f tgcr.aux tgcr.fdb_latexmk tgcr.fls tgcr.log tgcr.out || true
rm -f bench_report_dry.json || true
rm -f job_*.zip || true

echo "📁 Organizing papers..."
mkdir -p papers/tgcr
if [ -f tgcr.pdf ]; then
  mv tgcr.pdf papers/tgcr/ || true
fi

echo "✅ Cleanup complete"
