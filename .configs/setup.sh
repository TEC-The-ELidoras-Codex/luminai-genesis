#!/usr/bin/env bash
set -euo pipefail

GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RED="\033[0;31m"; RESET="\033[0m"

confirm() {
  local prompt=${1:-"Proceed?"}
  read -r -p "${prompt} [Y/n] " resp || true
  case ${resp:-Y} in [yY]|[yY][eE][sS]|"" ) return 0 ;; * ) return 1 ;; esac
}
require_sudo() {
  if [[ $EUID -ne 0 ]]; then
    echo -e "${YELLOW}Elevating with sudo...${RESET}"; sudo -v
    while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &
  fi
}
section() { echo -e "\n${GREEN}==> ${1}${RESET}"; }
info() { echo -e "${YELLOW}$*${RESET}"; }
err() { echo -e "${RED}$*${RESET}"; }

section "Update system"
require_sudo
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y && sudo apt clean -y

section "Core system tools"
sudo apt install -y build-essential curl wget git unzip zip
sudo apt install -y software-properties-common apt-transport-https ca-certificates

section "Everyday utilities"
# Use fastfetch (modern replacement for neofetch)
sudo apt install -y htop fastfetch net-tools ufw
if confirm "Install GUI firewall helper (gufw)?"; then sudo apt install -y gufw; fi

if confirm "Install desktop browsers/media (Firefox, Chromium, VLC, ffmpeg)?"; then
  section "Browsers & media"
  # chromium package name varies; try chromium-browser then chromium
  sudo apt install -y firefox || true
  sudo apt install -y chromium-browser || sudo apt install -y chromium || true
  sudo apt install -y vlc ffmpeg
fi

section "Developer runtimes"
sudo apt install -y python3 python3-pip
sudo apt install -y nodejs npm
sudo apt install -y rustc cargo
sudo apt install -y openjdk-17-jdk

if confirm "Install Docker engine and compose?"; then
  section "Docker / containers"
  sudo apt install -y docker.io
  sudo systemctl enable --now docker || true
  sudo usermod -aG docker "$USER" || true
  info "Log out & back in for group changes to take effect."
  sudo apt install -y docker-compose
else
  if confirm "Install Podman (rootless alternative)?"; then sudo apt install -y podman; fi
fi

section "Security & maintenance"
sudo apt install -y fail2ban
sudo ufw --force enable

section "Disk checks & cleanup"
df -h
sudo apt autoremove -y && sudo apt clean -y

section "Upgradable packages"
apt list --upgradable || true

section "Developer productivity tools"
sudo apt install -y neovim ripgrep clang-format pylint black

cat <<'TIP'
Tips:
- Python: per-project virtualenv:
    python3 -m venv .venv && source .venv/bin/activate
- Node: nvm for per-project Node versions:
    https://github.com/nvm-sh/nvm
- Containers: match CI envs; codify toolchains in Dockerfiles.
- WSL: run this inside Ubuntu distribution terminal.
TIP

section "All done"
info "If Docker was installed, re-log to activate docker group membership."
