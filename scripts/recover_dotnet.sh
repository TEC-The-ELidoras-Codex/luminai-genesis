#!/usr/bin/env bash
# recover_dotnet.sh
# Usage (from a live USB or recovery shell):
#  sudo ./recover_dotnet.sh /mnt/sysroot username [--copy]
# - mountpoint: where the root filesystem is mounted (default /mnt/sysroot)
# - username: username whose $HOME contains .dotnet (default: current user)
# - --copy: copy the dotnet binary into /usr/local/bin on the mounted root (recommended in recovery)

set -euo pipefail
MOUNT=${1:-/mnt/sysroot}
USER=${2:-$(whoami)}
MODE_COPY=false
if [[ ${3-} == "--copy" ]]; then
  MODE_COPY=true
fi

echo "Mountpoint: $MOUNT"
if [[ ! -d "$MOUNT" ]]; then
  echo "Error: mountpoint $MOUNT does not exist." >&2
  exit 2
fi

DOTNET_IN_HOME="$MOUNT/home/$USER/.dotnet/dotnet"
TARGET_BIN="$MOUNT/usr/local/bin/dotnet"
TARGET_DIR="$MOUNT/usr/local/bin"

if [[ ! -f "$DOTNET_IN_HOME" ]]; then
  echo "Could not find $DOTNET_IN_HOME. Make sure you mounted the root filesystem and that the user's home is present." >&2
  exit 3
fi

sudo mkdir -p "$TARGET_DIR"
if $MODE_COPY; then
  echo "Copying $DOTNET_IN_HOME -> $TARGET_BIN"
  sudo cp -f "$DOTNET_IN_HOME" "$TARGET_BIN"
  sudo chmod +x "$TARGET_BIN"
else
  echo "Creating symlink $TARGET_BIN -> /home/$USER/.dotnet/dotnet"
  sudo ln -sf "/home/$USER/.dotnet/dotnet" "$TARGET_BIN"
fi

# Add PATH export to user's .bashrc inside mounted root if missing
BASHRC="$MOUNT/home/$USER/.bashrc"
EXPORT_LINE='export PATH="$HOME/.dotnet:$HOME/.dotnet/tools:$PATH"'
if [[ -f "$BASHRC" ]]; then
  if ! grep -Fq "\.dotnet" "$BASHRC"; then
    echo "Adding PATH export to $BASHRC"
    echo "$EXPORT_LINE" | sudo tee -a "$BASHRC" >/dev/null
    sudo chown "$USER:$USER" "$BASHRC" || true
  else
    echo "PATH export already present in $BASHRC"
  fi
else
  echo "Creating $BASHRC and adding PATH export"
  echo "$EXPORT_LINE" | sudo tee "$BASHRC" >/dev/null
  sudo chown "$USER:$USER" "$BASHRC" || true
fi

echo "Done. You can now chroot into $MOUNT or boot normally; /usr/local/bin/dotnet will be available system-wide."
