#!/usr/bin/env bash
set -euo pipefail

# Auto free space script — safe, conservative cleaners for Ubuntu/ZFS systems
# Intended to be installed as /usr/local/bin/auto_free_space.sh and run by systemd timer.
# Actions: apt cache clean, remove old snap revisions, vacuum journal, truncate huge logs,
# and conservative ZFS snapshot pruning (if zfs present).

LOG="/var/log/auto_free_space.log"
MIN_FREE_PERCENT=15  # if root free percent <= this, run aggressive cleanup

timestamp(){ date -Iseconds; }

echo "$(timestamp): auto_free_space starting" >> "$LOG" || true

percent_free(){
  path=${1:-/}
  # df --output=pcent returns the USED percent (e.g. " 23%").
  # Compute FREE percent = 100 - USED. Return 0 on error.
  used=$(df --output=pcent "$path" 2>/dev/null | tail -n1 | tr -dc '0-9' || echo 0)
  if [ -z "$used" ]; then
    echo 0
    return
  fi
  free=$((100 - used))
  echo "$free"
}

clean_apt(){
  if command -v apt-get >/dev/null 2>&1; then
    echo "$(timestamp): cleaning apt cache" >> "$LOG" || true
    apt-get -y clean >> "$LOG" 2>&1 || true
    rm -rf /var/cache/apt/archives/*.deb >> "$LOG" 2>&1 || true
  fi
}

clean_snaps(){
  if command -v snap >/dev/null 2>&1; then
    echo "$(timestamp): pruning old snap revisions" >> "$LOG" || true
    snap list --all | awk '/disabled/{print $1, $3}' | while read -r snapname revision; do
      echo "$(timestamp): removing $snapname rev $revision" >> "$LOG" || true
      snap remove "$snapname" --revision="$revision" >> "$LOG" 2>&1 || true
    done
  fi
}

vacuum_journal(){
  if command -v journalctl >/dev/null 2>&1; then
    echo "$(timestamp): vacuuming journal to 200M" >> "$LOG" || true
    journalctl --vacuum-size=200M >> "$LOG" 2>&1 || true
  fi
}

truncate_big_logs(){
  max=$((100*1024*1024))
  shopt -s globstar 2>/dev/null || true
  for f in /var/log/*.log /var/log/**/*.log; do
    [ -f "$f" ] || continue
    size=$(stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$size" -ge "$max" ]; then
      echo "$(timestamp): truncating $f (size $size)" >> "$LOG" || true
      tail -n 50000 "$f" > "${f}.new" && mv "${f}.new" "$f" || true
    fi
  done
}

prune_zfs_snapshots(){
  if command -v zfs >/dev/null 2>&1; then
    KEEP_DAYS=30
    echo "$(timestamp): pruning zfs snapshots older than ${KEEP_DAYS}d" >> "$LOG" || true
    zfs list -t snapshot -o name,creation -H | while read -r name created; do
      if [ -n "$created" ]; then
        created_ts=$(date -d "$created" +%s 2>/dev/null || echo 0)
        now_ts=$(date +%s)
        age_days=$(( (now_ts - created_ts) / 86400 ))
        if [ "$age_days" -ge "$KEEP_DAYS" ]; then
          # Be conservative: skip snapshots with "@root-" or containing "boot" in name
          if echo "$name" | grep -Eiq "boot|root|esp"; then
            echo "$(timestamp): skipping $name (looks like boot/root snapshot)" >> "$LOG" || true
            continue
          fi
          echo "$(timestamp): destroying snapshot $name (age ${age_days}d)" >> "$LOG" || true
          zfs destroy -r "$name" >> "$LOG" 2>&1 || true
        fi
      fi
    done
  fi
}

ROOT_FREE=$(percent_free /)
echo "$(timestamp): root used percent: ${ROOT_FREE}" >> "$LOG" || true

if [ "$ROOT_FREE" -le "$MIN_FREE_PERCENT" ]; then
  echo "$(timestamp): below threshold (${MIN_FREE_PERCENT}) — running aggressive cleanup" >> "$LOG" || true
  clean_apt
  clean_snaps
  vacuum_journal
  truncate_big_logs
  prune_zfs_snapshots
else
  echo "$(timestamp): above threshold — running light cleanup" >> "$LOG" || true
  clean_apt
  vacuum_journal
fi

echo "$(timestamp): auto_free_space finished" >> "$LOG" || true
