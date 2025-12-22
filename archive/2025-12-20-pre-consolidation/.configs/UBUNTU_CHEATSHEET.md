# Ubuntu Setup & Open‑Source Developer Cheatsheet

Quick, copyable commands and notes to get an Ubuntu dev box ready for open‑source product work (Firefox, Thunderbird, LibreOffice) and general coding.

Prereqs: run these inside WSL/Ubuntu or on a native Ubuntu install. If you're in PowerShell on Windows and using WSL, prefix with `wsl -d Ubuntu --` or open the WSL terminal.

1) Update system

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove && sudo apt clean
```

2) Core system tools

```bash
sudo apt install build-essential curl wget git unzip zip -y
sudo apt install software-properties-common apt-transport-https ca-certificates -y
```

3) Everyday utilities

```bash
sudo apt install htop neofetch net-tools ufw -y
# Optional GUI firewall helper (on desktop)
sudo apt install gufw -y
```

4) Browsers & media (desktop)

```bash
sudo apt install firefox chromium-browser -y
sudo apt install vlc ffmpeg -y
```

5) Developer runtimes (Python, Node, Rust, Java)

```bash
sudo apt install python3 python3-pip -y
sudo apt install nodejs npm -y
sudo apt install rustc cargo -y
sudo apt install openjdk-17-jdk -y
```

Notes:

- For Python projects prefer using a virtualenv: `python3 -m venv .venv && source .venv/bin/activate`.
- For Node, consider using nvm for per-project Node versions: <https://github.com/nvm-sh/nvm>

6) Docker / containers

```bash
sudo apt install docker.io -y
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Log out & back in for group changes to take effect
sudo apt install docker-compose -y
```

Alternatives: `podman` for rootless containers: `sudo apt install podman -y`

7) Security & maintenance

```bash
sudo apt install fail2ban -y
sudo ufw enable
# Optional GUI: sudo apt install gufw
```

8) Disk checks & cleanup

```bash
df -h
du -sh /* 2>/dev/null | sort -h
sudo apt autoremove && sudo apt clean
```

9) Quick helper: check if upgrades available (one‑liner)

```bash
apt list --upgradable
```

10) Project-specific hints

- Firefox / Thunderbird
  - Rust + C/C++ toolchain required. Use `./mach bootstrap` per Mozilla docs.
  - Clone from Mozilla: `hg clone https://hg.mozilla.org/mozilla-central` (firefox) or the Thunderbird repository.
  - Build: `./mach build` (see project docs)

- LibreOffice
  - Install build deps: `sudo apt install libgtk-3-dev libx11-dev libcairo2-dev libpng-dev openjdk-17-jdk -y`
  - Clone & build: `git clone https://git.libreoffice.org/core.git && cd core && ./autogen.sh && make`

11) Developer productivity tools

```bash
sudo apt install neovim ripgrep clang-format pylint black -y
# VS Code (official) or VSCodium (de-telemetry'd)
```

12) Cheatsheet: Minimal install for open-source dev (single one‑liner)

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install -y build-essential curl wget git unzip zip software-properties-common apt-transport-https ca-certificates htop neofetch net-tools ufw python3 python3-pip nodejs npm rustc cargo openjdk-17-jdk docker.io docker-compose fail2ban neovim ripgrep clang-format
```

13) Containerized dev & CI tips

- Use Docker images to match CI environments (e.g., ubuntu:22.04 or the official project images).
- For reproducible builds, create a `Dockerfile` that installs the exact toolchain your project needs.

14) Mobile & Ubuntu on mobile

- You cannot run full desktop Ubuntu natively on most Android devices, but you can run containers/chroots (Termux, UserLAnd) or use Ubuntu Touch (UBports) on supported hardware.
- If you need mobile development, consider building web/mobile frontends and test using emulators or progressive web apps.

15) Next actions I can do for you (choose one)

- Create a `setup.sh` script in the repo that runs the minimal install for you (interactive / opt‑in installs).
- Produce a 2‑tier roadmap: Local dev setup vs. Containerized deployment (with example Dockerfiles).
- Generate a Day‑by‑Day onboarding (Day 1: clone & build Firefox Nightly; Day 2: patch LibreOffice; Day 3: test Thunderbird builds).

---
Save this file locally or add it to your dotfiles. When you’re ready I can create the `setup.sh` script and commit it to the repo so you can clone and run it on any Ubuntu box.
