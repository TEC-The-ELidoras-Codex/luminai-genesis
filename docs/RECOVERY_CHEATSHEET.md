# System Recovery & ZFS Root-Space Cheatsheet

Short, copy-pasteable commands and concise guidance you can follow during a root-space emergency. Keep this file handy; automation can be added later once there's sustained free space.

**Quick Checklist**

- **Identify space pressure:** `df -h /` and `zfs list -o name,used,available -r`.
- **Find big consumers:** `du -sh /home/* /var/* 2>/dev/null | sort -h` and `du -sh /path/to/project/* | sort -h`.
- **Prefer conservative actions first** (apt cache, journals, logs) before deleting data or destroying snapshots.

**Immediate Safe Cleanup (low-risk)**

```bash
# 1) Clean package cache
sudo apt-get clean

# 2) Remove old snap revisions (list then remove; be careful)
snap list --all
# Remove a specific old revision, example:
sudo snap remove <snap-name> --revision=<rev>

# 3) Free journal logs (keeps the most recent)
sudo journalctl --vacuum-size=200M

# 4) Truncate very large logs (example)
sudo truncate -s 0 /var/log/syslog /var/log/kern.log || true

# 5) Remove or compress large caches (pip, docker, etc.)
sudo du -sh /var/cache /home/*/.cache 2>/dev/null
# Manually inspect and remove safe caches, e.g. pip cache:
pip cache purge  # if safe for your dev workflow
```

**Move Large Data Off ZFS Root (safe, recommended)**

- Format + mount the spare partition (example used in session):

```bash
sudo mkfs.ext4 /dev/sdb3
sudo mkdir -p /mnt/extra
sudo mount /dev/sdb3 /mnt/extra
sudo blkid /dev/sdb3   # get UUID for fstab
```

- Rsync large folders (keeps ownership & perms, shows progress):

```bash
sudo rsync -aP --info=progress2 /home/you/luminai-genesis/models/ /mnt/extra/luminai-models/
sudo rsync -aP --info=progress2 /home/you/ollama_models/ /mnt/extra/ollama_models/
# Optionally remove source files only after verifying data
sudo rsync -aP --remove-source-files /home/you/luminai-genesis/models/ /mnt/extra/luminai-models/
```

- Bind-mount into original paths and persist in `/etc/fstab` with UUID:

```bash
# /etc/fstab line examples
UUID=<UUID-from-blkid>  /mnt/extra   ext4   defaults  0 2
/mnt/extra/ollama_models  /home/you/ollama_models  none  bind  0  0
/mnt/extra/luminai-models /home/you/luminai-genesis/models none bind 0 0
```

**ZFS Snapshots: check before destroying (careful)**

- List snapshots sorted by space used:

```bash
sudo zfs list -t snapshot -o name,used,creation -S used
```

- If you identify a large snapshot that must be destroyed (confirm first), preview then destroy:

```bash
# Dry-run preview (shows what would be destroyed)
sudo zfs destroy -n pool/dataset@snapshot-name

# When you are 100% sure:
sudo zfs destroy pool/dataset@snapshot-name
```

- Note: destroying snapshots reclaims blocks but only after snapshots that reference the same blocks are removed — double-check related snapshots.

**Useful ZFS & verification commands**

```bash
df -h /
zfs list -r
zfs list -t snapshot -o name,used,refer,creation -r
zpool list
zpool status -v
du -sh /home/* | sort -h
```

**When you still have "No space left" errors**

- Pause and avoid writing large files. Work through safe cleanups above. If you must, remove unneeded large files from non-system-critical locations (e.g., downloads, old tarballs) only after verifying they are not needed.
- If moving files to a spare disk, do not delete the original until you have fully verified the copy is complete and intact.

**Short-term policy notes (for later automation)**

- Add an exclude for large home datasets in `zfs-auto-snapshot` (or reduce `--keep` values) rather than destroying snapshots ad-hoc.
- Automate safe cleanups (apt, journal) and low-risk cache pruning via a systemd timer.
- Add a small alert script that emails or logs when free space drops below a threshold (e.g., 15%).

**If you want me to do automation later**

- I can: tune `zfs-auto-snapshot`, add an hourly `check_space_and_alert.sh` timer, and keep the `auto_free_space.sh` systemd timer but only enable more aggressive actions when free < X%.

**Final Safety Tips**

- Always `zfs list -t snapshot` and inspect before running `zfs destroy`.
- Prefer rsync and bind-mount approach over moving critical system directories into a different pool unless you plan a full, tested migration.
- Keep a tested recovery plan (this cheatsheet) and update it after each change.

---

File created to help you remember recovery steps. If you want, I can also add a one-page printable checklist, or convert this into a single one-shot script (run with caution).
