#!/bin/bash
# mega_cleanup.sh - Comprehensive repository cleanup for luminai-genesis
# Run from repo root: ./mega_cleanup.sh

set -e  # Exit on error
trap 'echo "❌ Error on line $LINENO"' ERR

REPO_ROOT="/home/elidoras-codex/luminai-genesis"
BACKUP_DIR="$HOME/luminai-genesis-backup-$(date +%Y%m%d-%H%M%S)"

cd "$REPO_ROOT"

# Non-interactive: confirm automatically
confirm="yes"

# 1) Create backup
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/pre-cleanup.tar.gz" \
    --exclude='.venv*' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='.ruff_cache' \
    --exclude='.git' \
    . || true

# 2) Remove build artifacts and temp files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
rm -f tgcr.aux tgcr.log tgcr.fdb_latexmk tgcr.fls 2>/dev/null || true
rm -f reddit1.json reddit2.json 2>/dev/null || true
find . -type f -name ".DS_Store" -delete 2>/dev/null || true
find . -type f -name "Thumbs.db" -delete 2>/dev/null || true

# 3) Fix Codex encoding in-place if script exists
if [ -f "scripts/codex_encoding_fixer.py" ]; then
  python3 scripts/codex_encoding_fixer.py docs/lore/entries --in-place || true
fi

# Consolidate codex_fixed if present
if [ -d "docs/codex_fixed" ]; then
  rm -rf docs/codex.bak 2>/dev/null || true
  [ -d "docs/codex" ] && mv docs/codex docs/codex.bak || true
  mv docs/codex_fixed docs/codex || true
fi

# Rebuild structured codex
if [ -f "scripts/codex_structurer.py" ] && [ -d "docs/codex" ]; then
  python3 scripts/codex_structurer.py docs/codex -o codex_structured || true
fi

# 4) Consolidate archives
mkdir -p archive/historical-cleanups 2>/dev/null || true
for cleanup_dir in archive/cleanup-*; do
  [ -d "$cleanup_dir" ] && mv "$cleanup_dir" archive/historical-cleanups/ 2>/dev/null || true
done

# 5) Remove temp venvs
rm -rf .venv_temp 2>/dev/null || true

# 6) Move site files into docs/site
if [ -d "site" ]; then
  mkdir -p docs/site
  mv site/* docs/site/ 2>/dev/null || true
  rmdir site 2>/dev/null || true
fi

# 7) Archive deprecated scripts
mkdir -p archive/deprecated-scripts
DEPRECATED=(
  "recover_deleted_files.sh"
  "recover_deleted_files_v2.sh"
  "fix_e501.py"
  "fix_e501_enhanced.py"
  "rebuild_codex_dump.sh"
  "parse_codex_dump.py"
  "sanitize_codex_dump.py"
)
for script in "${DEPRECATED[@]}"; do
  [ -f "scripts/$script" ] && mv "scripts/$script" archive/deprecated-scripts/ || true
done

# 8) Update .gitignore
if ! grep -q "__pycache__/" .gitignore 2>/dev/null; then
  cat >> .gitignore <<'EOF'

# Build artifacts
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.ruff_cache/

# LaTeX artifacts
*.aux
*.log
*.fdb_latexmk
*.fls

# Virtual environments
.venv*/

# OS files
.DS_Store
Thumbs.db

# Temp files
*.tmp
*.temp
EOF
fi

# End
echo "CLEANUP: backup saved to $BACKUP_DIR/pre-cleanup.tar.gz"
echo "DONE"
