#!/usr/bin/env bash
set -euo pipefail

# Simple, safe CI/fix helper for repository hygiene
# - Dry-run by default
# - Does not rewrite history (no BFG or filter-branch)
# - Does not force-push unless --apply is set
# - Adds safe .gitignore entries, removes common secret files from index
# - Runs `ruff` auto-fixes if available
# - Commits changes with a TGCR-style message if changes exist
# Usage:
#   ./fix-ci.sh           # dry-run, shows what would be done
#   ./fix-ci.sh --apply   # perform actions and push (no history rewrite)

DRY_RUN=true
APPLY=false
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
AUTO_PUSH=false

usage() {
  cat <<EOF
Usage: $0 [--apply] [--push]
  --apply    : perform changes (otherwise dry-run)
  --push     : push branch to origin after commit (only when --apply used)
  -h,--help  : show this help
EOF
}

for arg in "$@"; do
  case "$arg" in
    --apply) DRY_RUN=false; APPLY=true ;;
    --push) AUTO_PUSH=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $arg"; usage; exit 1 ;;
  esac
done

echo "Fix script: dry-run=$DRY_RUN, apply=$APPLY, push=$AUTO_PUSH, branch=$BRANCH"

# Safety check: require explicit apply to do destructive actions
if $DRY_RUN; then
  echo "Running in dry-run mode. No commits or pushes will be made."
fi

# Step 1: remove secret files from index (safe: only unstages, does not rewrite history)
SECRET_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  "*.pem"
  "*.key"
  "*secret*"
  "*credential*"
  "config/secrets.yml"
)

echo "\n== Step 1: Unstage common secret files (no history rewrite) =="
for p in "${SECRET_PATTERNS[@]}"; do
  # find matches and show them
  matches=$(git ls-files -- "${p}" || true)
  if [[ -n "$matches" ]]; then
    echo "Matches for pattern '$p':"
    echo "$matches"
    if ! $DRY_RUN; then
      git rm --cached -r --ignore-unmatch $p || true
    fi
  fi
done

# Add safe .gitignore entries if missing (append only)
GITIGNORE_ADD='\n# Repository secret patterns (managed by fix-ci.sh)\n.env\n.env.*\n*.pem\n*.key\n*secret*\n*credential*\nconfig/secrets.yml\n'

if ! grep -q "Repository secret patterns (managed by fix-ci.sh)" .gitignore 2>/dev/null || true; then
  echo "\n== Step 1b: Update .gitignore (append safe defaults) =="
  echo -e "$GITIGNORE_ADD"
  if ! $DRY_RUN; then
    printf "%s" "$GITIGNORE_ADD" >> .gitignore
    git add .gitignore
  fi
fi

# Step 2: Run ruff auto-fixes if ruff exists
echo "\n== Step 2: Run ruff auto-fix (if available) =="
if command -v ruff >/dev/null 2>&1; then
  echo "ruff found: running 'ruff check --fix' (targets: src scripts)
"
  if ! $DRY_RUN; then
    ruff check --fix --quiet src/ scripts/ || true
    ruff format src/ scripts/ || true
    git add -A || true
  fi
else
  echo "ruff not found in PATH. To install, run: python -m pip install --upgrade ruff"
fi

# Step 3: Minimal safe lint patches (non-destructive and conservative)
# We avoid aggressive sed modifications by default. If users request --aggressive, we can add more.

# Step 4: Commit changes with TGCR-style message if any changes
echo "\n== Step 3: Commit staged changes (if any) =="
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Staged or unstaged changes detected."
  if $DRY_RUN; then
    git status --porcelain
    echo "(dry-run) Would commit: ⚙️ airth(ci): apply safe repo hygiene fixes"
  else
    # derive scope from branch, default to 'ci'
    SCOPE="ci"
    if [[ "$BRANCH" == */* ]]; then
      SCOPE="$(echo "$BRANCH" | cut -d'/' -f2)"
    fi
    git add -A
    git commit --no-verify -m "⚙️ airth($SCOPE): apply safe repo hygiene fixes"
    echo "Committed changes."
    if $AUTO_PUSH; then
      echo "Pushing branch $BRANCH to origin (non-forced)..."
      git push origin "$BRANCH"
    else
      echo "Not pushing; use --push with --apply to push changes."
    fi
  fi
else
  echo "No changes detected; nothing to commit."
fi

# Step 5: Optional pre-commit hook install
echo "\n== Step 4: Optional pre-commit hook to prevent future secret commits =="
if $DRY_RUN; then
  echo "(dry-run) Would offer to install pre-commit hook that blocks common secret filenames."
else
  read -p "Install pre-commit hook to block common secret filenames? (y/N) " -r
  if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -e
SECRET_PATTERNS=(".env" "*.pem" "*.key" "*secret*" "*credential*")
for p in "${SECRET_PATTERNS[@]}"; do
  if git diff --cached --name-only | grep -qE "$p"; then
    echo "ERROR: Attempting to commit a file matching: $p"
    echo "Add to .gitignore or use 'git rm --cached' to untrack it."
    exit 1
  fi
done
exit 0
HOOK
    chmod +x .git/hooks/pre-commit
    echo "Pre-commit hook installed at .git/hooks/pre-commit"
  else
    echo "Pre-commit hook not installed."
  fi
fi

# Final summary
echo "\n== Summary =="
if $DRY_RUN; then
  echo "Dry-run complete. No changes made. To apply changes, run: $0 --apply [--push]"
else
  echo "Apply run complete. Review git status and run CI."
fi

exit 0
