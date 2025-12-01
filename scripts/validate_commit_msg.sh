#!/usr/bin/env bash
# LuminAI Genesis — Commit Message Validator
# Enforces: <emoji> <type>(optional-scope): short description

MSG_FILE="$1"
MSG="$(head -n1 "$MSG_FILE")"

# Allowed types (extend as needed)
TYPE_REGEX='(feat|fix|docs|chore|refactor|perf|test|infra|sec|style|lore|gov|hotfix)'

# Pattern:
#   <emoji> <type>(optional-scope): description
if echo "$MSG" | grep -Eq "^[^[:space:]]+ ${TYPE_REGEX}(\([a-zA-Z0-9_-]+\))?: .+"; then
  exit 0
fi

cat <<EOF

❌ Invalid commit message:

  $MSG

Expected format:

  <emoji> <type>(optional-scope): short description

Examples:
  🧠 feat(api): add /api/resonance endpoint
  🧹 chore(ci): clean up workflows
  📜 docs(memo): add iatrogenic harm memo
  🧬 gov(axioms): update TEC conscience rules

EOF

exit 1
