# ULTIMATE TEC PROJECT CHECKLIST

**Author:** Angelo Hurley
**Last Updated:** 2025-12-26
**Usage:** A living document to track progress, priorities, backups, and emergency recovery.

---

### 📋 WHAT’S DONE (COMPLETED TASKS)
Settings Developer settings GitHub Apps LuminAI-Codex
About
Owned by: @Elidorascodex

App ID: 2186310

Using your App ID to get installation tokens? You can now use your Client ID instead.

Client ID: Iv23liuCJbwDvim9WppS

*(Check off as you go — proof of progress.)*

#### Core Systems

- [x] Deterministic Honoring in `erasure_combat.py`
  - Set `fragment.honored_by` and `fragment.honored_at`.
  - Append fragment to `character.honored_dead`.
  - Grant XP via `character.stats.gain_xp(fragment.xp_value)`.
  - Add willpower gain (+1).
  - Add fragment’s `human_name` to `character.carved_names`.
  - **Tests:** 41/41 passed.

- [x] Unity Prototype Scene (Junction 5‑C cutscene)
- [x] GitHub Repo Setup (`The-Elidoras-Codex`)

#### Chapters Written

- [x] Chapter 1: The First Name (`tec_chapter_1_final.md`)
- [x] Chapter 2: The Vessel (`tec_chapter_2_final.md`)
- [x] Chapter 3: The Queen’s Son (`tec_chapter_3_final.md`)
- [x] ... (others as you listed)

#### Python Systems

- [x] Erasure Combat (`erasure_combat.py`)
- [x] Ghoul Database (`ghoul_db.py`)
- [x] LitRPG System (`tec_litrpg_system.py`)

---

### 📁 WHAT’S IN PROGRESS (CURRENT TASKS)

- [ ] Void Light Mechanics (add `void_light` damage type)
- [ ] Corruption System (track corruption levels in `character.stats`)
- [ ] Unity Knockoffs Hideout Scene (model + import)

---

### 🎮 WHAT’S PLANNED (UP NEXT)

- [ ] Boss Fight: The Queen (design + implement)
- [ ] Willpower System (spendable resource)
- [ ] Magmasox Citadel Scene

---

### 💾 BACKUP & SAFETY CHECKLIST (Daily)

```bash
# 1. Commit all changes
git add .
git commit -m "Daily backup: $(date +%Y-%m-%d)"
git push

# 2. Sync to cloud
rclone sync ~/tec_book gdrive:TEC_Backups
rclone sync ~/luminai-genesis gdrive:TEC_Backups

# 3. Create a local zip
zip -r ~/TEC_BACKUP_$(date +%Y-%m-%d).zip ~/tec_book ~/luminai-genesis

# 4. Take a ZFS snapshot
sudo zfs snapshot rpool/USERDATA/home_pnykhf@daily-$(date +%Y-%m-%d)
```

---

### 💀 EMERGENCY RECOVERY

```bash
# 1. Restore from GitHub
git clone https://github.com/yourusername/The-Elidoras-Codex.git
git clone https://github.com/yourusername/luminai-genesis.git

# 2. Restore from cloud
rclone copy gdrive:TEC_Backups/ ~/TEC_RECOVERY/

# 3. Restore from ZFS snapshot
sudo zfs rollback rpool/USERDATA/home_pnykhf@daily-$(date +%Y-%m-%d --date="yesterday")
```

---

### HOW TO USE

1. Update daily (mark tasks done / in progress).
2. Run the daily ritual at the end of each session.
3. If disaster strikes, follow Emergency Recovery.
