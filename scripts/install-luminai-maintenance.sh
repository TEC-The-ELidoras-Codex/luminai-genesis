#!/usr/bin/env bash
# install-luminai-maintenance.sh
# Run this to install maintenance scripts and systemd units for LuminAI Genesis

set -e

REPO_DIR="/home/elidoras-codex/luminai-genesis"
SCRIPTS=("auto_free_space.sh" "zfs_prune_snapshots.sh" "check_space_and_alert.sh")

echo "=== Installing LuminAI Genesis maintenance scripts and systemd units ==="
echo

# Copy scripts
echo "1. Copying scripts to /usr/local/bin..."
for script in "${SCRIPTS[@]}"; do
  echo "   - Installing $script"
  sudo cp "$REPO_DIR/scripts/$script" /usr/local/bin/
  sudo chmod +x "/usr/local/bin/$script"
done
echo "   ✓ Scripts installed"
echo

# Copy systemd units
echo "2. Copying systemd service and timer units..."
UNITS=("auto-free-space.service" "auto-free-space.timer" "check-space-alert.service" "check-space-alert.timer")
for unit in "${UNITS[@]}"; do
  echo "   - Installing $unit"
  sudo cp "$REPO_DIR/infrastructure/systemd/$unit" /etc/systemd/system/
done
echo "   ✓ Systemd units installed"
echo

# Reload and enable
echo "3. Reloading systemd and enabling timers..."
sudo systemctl daemon-reload
sudo systemctl enable auto-free-space.timer check-space-alert.timer
echo "   ✓ Timers enabled"
echo

# Start timers
echo "4. Starting timers now..."
sudo systemctl start auto-free-space.timer check-space-alert.timer
echo "   ✓ Timers started"
echo

# Show status
echo "=== Status ==="
systemctl status auto-free-space.timer --no-pager
echo
systemctl status check-space-alert.timer --no-pager
echo

echo "✓ Installation complete!"
echo
echo "Next steps:"
echo "  - Monitor logs: tail -f /var/log/auto_free_space.log"
echo "  - Trigger a manual run: /usr/local/bin/auto_free_space.sh"
echo "  - Disable if needed: sudo systemctl stop auto-free-space.timer"
