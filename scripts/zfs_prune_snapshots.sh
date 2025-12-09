#!/usr/bin/env bash
set -euo pipefail

# Conservative ZFS snapshot prune helper
# Use with care. This script targets non-boot snapshots older than KEEP_DAYS.

KEEP_DAYS=${KEEP_DAYS:-30}
LOG="/var/log/zfs_prune_snapshots.log"

echo "$(date -Iseconds): zfs_prune_snapshots starting (KEEP_DAYS=${KEEP_DAYS})" >> "$LOG" || true

if ! command -v zfs >/dev/null 2>&1; then
  echo "zfs not present, exiting" >> "$LOG" || true
  exit 0
fi

zfs list -t snapshot -o name,creation -H | while read -r name created; do
  if [ -n "$created" ]; then
    created_ts=$(date -d "$created" +%s 2>/dev/null || echo 0)
    now_ts=$(date +%s)
    age_days=$(( (now_ts - created_ts) / 86400 ))
    if [ "$age_days" -ge "$KEEP_DAYS" ]; then
      # skip snapshots that look like boot or contain common boot labels
      if echo "$name" | grep -Eiq "boot|root|esp|autosnap"; then
        echo "$(date -Iseconds): skipping $name (looks like boot/root/autosnap)" >> "$LOG" || true
        continue
      fi
      echo "$(date -Iseconds): destroying $name (age ${age_days}d)" >> "$LOG" || true
      zfs destroy -r "$name" >> "$LOG" 2>&1 || true
    fi
  fi
done

echo "$(date -Iseconds): zfs_prune_snapshots finished" >> "$LOG" || true
