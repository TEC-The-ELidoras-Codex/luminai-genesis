#!/usr/bin/env bash
# Simple local commit-msg validator for TEC emoji + conventional header
# Usage: copy this to .git/hooks/commit-msg or run as a gate in CI
MSG_FILE="$1"
if [ -z "$MSG_FILE" ]; then
  echo "commit-msg hook: missing message file" >&2
  exit 1
fi
MSG=$(head -n1 "$MSG_FILE" | tr -d '\r')
# Accept: <emoji> <type>(scope): description  — emoji is any char then space
if echo "$MSG" | grep -E "^.\s+(feat|fix|docs|chore|refactor|test|infra|sec|lore|hotfix)(\([^)]+\))?:\s+.+" >/dev/null; then
  exit 0
else
  echo "Invalid commit message format." >&2
  echo "Use: <emoji> <type>(scope): short description" >&2
  echo "Examples: '🧠 feat(api): add /api/resonance' or '🧹 chore: tidy workflows'" >&2
  exit 1
fi
