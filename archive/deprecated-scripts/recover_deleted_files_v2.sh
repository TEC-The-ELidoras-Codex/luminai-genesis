#!/usr/bin/env bash
set -euo pipefail

since_date="2025-12-01"

# gather list
git log --diff-filter=D --name-only --since="$since_date" --pretty=format: | sed "/^$/d" | grep -v ":" | sort -u > /tmp/deleted-files.txt

if [ ! -s /tmp/deleted-files.txt ]; then
  echo "No deleted files found since $since_date"
  exit 0
fi

recover_dir="recovery/restored-deleted-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$recover_dir"
report="$recover_dir/restore-report.txt"
echo "Restore report - $(date)" > "$report"

while IFS= read -r f; do
  [ -z "$f" ] && continue
  echo "Processing $f" | tee -a "$report"
  commit_list=$(git rev-list --all -- "$f" 2>/dev/null || true)
  found_commit=""
  for c in $commit_list; do
    if git ls-tree -r "$c" -- "$f" >/dev/null 2>&1; then
      found_commit="$c"
      break
    fi
  done
  if [ -z "$found_commit" ]; then
    echo "No commit with actual blob found for $f, skipping" | tee -a "$report"
    continue
  fi
  out_path="$recover_dir/$f"
  mkdir -p "$(dirname "$out_path")"
  echo "Attempting to extract $f from $found_commit" | tee -a "$report"
  if ! git show "$found_commit":"$f" > "$out_path"; then
    echo "Failed to extract $f from $found_commit" | tee -a "$report"
    continue
  fi
  mode=$(git ls-tree -r "$found_commit" -- "$f" | awk {print
