#!/usr/bin/env bash
# LuminAI Genesis — Lightweight Secrets Scan
# Requires: ripgrep (rg)

set -euo pipefail

ROOT_DIR="${1:-.}"

if ! command -v rg >/dev/null 2>&1; then
  echo "❌ ripgrep (rg) is not installed. Please install it and re-run."
  exit 1
fi

echo "🔍 Running secrets scan on: $ROOT_DIR"
echo

PATTERNS=(
  "AKIA[0-9A-Z]{16}"
  "ASIA[0-9A-Z]{16}"
  "ghp_[0-9A-Za-z]{36}"
  "github_pat_[0-9A-Za-z_]{80,}"
  "xox[baprs]-[0-9A-Za-z-]{10,48}"
  "BEGIN RSA PRIVATE KEY"
  "BEGIN OPENSSH PRIVATE KEY"
  "BEGIN EC PRIVATE KEY"
  "AIza[0-9A-Za-z_-]{35}"
  "sk-[A-Za-z0-9]{20,}"
)

for pat in "${PATTERNS[@]}"; do
  echo "Pattern: /$pat/"
  rg --line-number --hidden --glob '!.git' -P "$pat" "$ROOT_DIR" || true
  echo
done

echo "✅ Secrets scan complete (manual review recommended)."
