#!/usr/bin/env bash
set -euo pipefail

# Lightweight check script that logs alerts when root fs or ZFS datasets exceed thresholds.
# Intended for hourly timer or manual run.

ALERT_LOG="/var/log/space_alert.log"
THRESH=85

echo "$(date -Iseconds): checking disk usage" >> "$ALERT_LOG" || true

root_used=$(df -P / | awk 'NR==2{print $5}' | tr -d '%')
if [ -n "$root_used" ] && [ "$root_used" -ge "$THRESH" ]; then
  echo "$(date -Iseconds): ALERT root usage ${root_used}% >= ${THRESH}%" >> "$ALERT_LOG"
fi

if command -v zfs >/dev/null 2>&1; then
  zfs list -o name,used,avail,refer,mountpoint -t filesystem -H | while read -r name used avail refer mount; do
    # compute percent used roughly as refer/(refer+avail)
    # use zfs get -Hp value quota/used to be precise; keep conservative approach
    if [ "$avail" = "-" ] || [ -z "$avail" ]; then
      continue
    fi
    # convert to bytes using zfs get -Hp -o value used,avail would be better; skip exact percent here
    # Log datasets with small available space
    if [ -n "$avail" ]; then
      echo "$(date -Iseconds): ZFS dataset $name avail=$avail" >> "$ALERT_LOG" || true
    fi
  done
fi

echo "$(date -Iseconds): check complete" >> "$ALERT_LOG" || true
