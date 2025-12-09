**System Maintenance**

- **Purpose:** Scripts and systemd units to keep root filesystem and ZFS pools healthy by
  cleaning package caches, pruning old snap revisions, vacuuming the journal, truncating
  large logs, and (optionally) pruning old ZFS snapshots.

- **Files added in this repo:**

  - `scripts/auto_free_space.sh` — main cleanup script (safe defaults)
  - `scripts/zfs_prune_snapshots.sh` — conservative ZFS snapshot pruner
  - `scripts/check_space_and_alert.sh` — lightweight space-check logger
  - `infrastructure/systemd/auto-free-space.service` — systemd unit (oneshot)
  - `infrastructure/systemd/auto-free-space.timer` — systemd timer (daily + on-boot)

- **Install (run on the target machine as root / with sudo):**

```
# copy scripts into /usr/local/bin and make executable
sudo cp scripts/auto_free_space.sh /usr/local/bin/
sudo cp scripts/zfs_prune_snapshots.sh /usr/local/sbin/
sudo cp scripts/check_space_and_alert.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/auto_free_space.sh /usr/local/bin/check_space_and_alert.sh /usr/local/sbin/zfs_prune_snapshots.sh

# install systemd units (copy from repo to /etc/systemd/system)
sudo cp infrastructure/systemd/auto-free-space.service /etc/systemd/system/
sudo cp infrastructure/systemd/auto-free-space.timer /etc/systemd/system/

# reload and enable timer + run once now
sudo systemctl daemon-reload
sudo systemctl enable --now auto-free-space.timer
sudo systemctl start auto-free-space.service

# verify logs
sudo journalctl -u auto-free-space.service --no-pager
tail -n 200 /var/log/auto_free_space.log
```

- **Notes & safety:**
  - This is intentionally conservative: it skips destructive actions on boot snapshots and
    avoids bulk-deleting anything without logs.
  - Do NOT paste your sudo password into chat. Run the commands on your machine.
  - Review `/var/log/auto_free_space.log` after the first run and confirm no important
    files were removed. Keep backups before doing any manual snapshot destruction.
