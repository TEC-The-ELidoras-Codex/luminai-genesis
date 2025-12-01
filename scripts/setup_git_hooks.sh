#!/usr/bin/env bash
# LuminAI Genesis — Install Git hooks

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$ROOT_DIR/.git/hooks"

mkdir -p "$HOOKS_DIR"

cat > "$HOOKS_DIR/commit-msg" << 'EOF'
#!/usr/bin/env bash
scripts/validate_commit_msg.sh "$@"
EOF

chmod +x "$HOOKS_DIR/commit-msg"

echo "✅ Commit-msg hook installed. All commits will be checked for emoji + type format."

# Also install a pre-commit hook to sanitize docs and scan for secrets
cat > "$HOOKS_DIR/pre-commit" << 'HOOK'
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "🔧 pre-commit: sanitizing canonical bundles (docs/canonical)"
if command -v python3 >/dev/null 2>&1; then
	python3 scripts/sanitize_bundles.py || {
		echo "❌ sanitizer failed"; exit 1;
	}
else
	echo "⚠️ python3 not found — skipping sanitizer"
fi

echo "🔍 pre-commit: secrets scan"
if bash scripts/scan_secrets.sh docs/canonical; then
	echo "✅ secrets scan done"
else
	echo "❌ secrets scan failed"; exit 1;
fi

# Prevent committing backup artifacts
if git diff --cached --name-only | grep -E "\.bak\.[0-9TZ]+$" >/dev/null 2>&1; then
	echo "❌ Backup files (*.bak.*) detected in staging. Please remove or .gitignore them before committing."
	exit 1
fi

exit 0
HOOK

chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Pre-commit hook installed. Sanitizer + secrets scan will run before each commit."
