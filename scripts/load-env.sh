#!/usr/bin/env bash
# Load variables from .env.local into the current shell (POSIX sh / bash)
# Usage: source scripts/load-env.sh

set -euo pipefail
ENVFILE=".env.local"
if [ ! -f "$ENVFILE" ]; then
  echo "No $ENVFILE found. Copy .env.example to .env.local and fill secrets before sourcing."
  return 1 2>/dev/null || exit 1
fi

# Export everything (skip comments and empty lines)
set -a
while IFS= read -r line || [ -n "$line" ]; do
  # skip comments and blank lines
  case "$line" in
    ''|\#*) continue ;;
  esac
  # only export key=val lines
  if echo "$line" | grep -q '='; then
    # Avoid exporting lines without a key
    key="$(echo "$line" | sed -E 's/=.*$//')"
    val="$(echo "$line" | sed -E 's/^[^=]*=//')"
    export "$key=$val"
  fi
done < "$ENVFILE"
set +a

echo "Loaded environment from $ENVFILE"
