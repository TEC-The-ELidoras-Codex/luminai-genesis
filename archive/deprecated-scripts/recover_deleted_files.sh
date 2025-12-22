#!/usr/bin/env bash
set -euo pipefail

since_date="2025-12-01"
# Get unique file list of deleted files (skip Windows Zone.Identifier altstreams)
git log --diff-filter=D --name-only --since="$since_date" --pretty=format: | sed "/^$/d" | grep -v ":" | sort -u > /tmp/deleted-files.txt

if [ ! -s /tmp/deleted-files.txt ]; then
  echo "No deleted files found since $since_date"
  exit 0
fi

echo "Found deleted files:"
cat /tmp/deleted-files.txt

# Create recovery dir
recover_dir="recovery/restored-deleted-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$recover_dir"

# Prepare report
report="$recover_dir/restore-report.txt"
echo "Restore report - $(date)" > "$report"

while IFS= read -r f; do
  [ -z "$f" ] && continue
  commit=$(git rev-list -n 1 --all -- "$f" || true)
  if [ -z "$commit" ]; then
    echo "No commit found for $f, skipping" | tee -a "$report"
    continue
  fi
  out_path="$recover_dir/$f"
  mkdir -p "$(dirname "$out_path")"
  echo "Restoring $f from commit $commit to $out_path" | tee -a "$report"
  # Extract
  git show "$commit":"$f" > "$out_path" || {
    echo "Failed to extract $f from $commit" | tee -a "$report"
    continue
  }
  mode=$(git ls-tree -r "$commit" -- "$f" | awk {print
