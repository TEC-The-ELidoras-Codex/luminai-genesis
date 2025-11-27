ENV setup — secure local secrets (README)
=========================================

This repository keeps an example env file committed and expects local secrets to be stored in a separate, ignored file.

Files

- `.env.example` — Committed example with empty placeholders. Copy this to `.env.local` and fill real secrets.
- `.env.local` — Your local-only file (do NOT commit). This file is in `.gitignore`.
- `scripts/load-env.sh` / `scripts/load-env.ps1` — helpers to load `.env.local` into your shell.
- `secrets/secret-map.json` — mapping of environment variable names to Bitwarden item names and fields.
- `scripts/fetch-secrets-from-bw.sh` / `scripts/fetch-secrets-from-bw.ps1` — helpers to fetch secrets from Bitwarden CLI and write `.env.local` safely.

Quick start (safe, local)

1. Copy the example to a local file:

   cp .env.example .env.local

2. Fill any values you prefer by hand OR fetch from Bitwarden (recommended):

   # Option A: manually edit

   nano .env.local

   # Option B: fetch using Bitwarden CLI (requires `bw` and jq). Export BW_CLIENTID/BW_CLIENTSECRET or set BW_SESSION

   export BW_CLIENTID="<your-client-id>"
   export BW_CLIENTSECRET="<your-client-secret>"
   ./scripts/fetch-secrets-from-bw.sh

3. Load env into your shell for local testing:

   # Bash/WSL

   source scripts/load-env.sh

   # PowerShell

   .\scripts\load-env.ps1

Notes

- Never commit `.env.local` or real tokens. Keep them in Bitwarden and in GitHub Secrets for CI.
- If you accidentally committed secrets previously, rotate them immediately and remove the file from the index:

  git rm --cached .env
  git commit -m "Remove tracked env file"

Security

- The Bitwarden scripts use your Bitwarden session (`BW_SESSION`) or client credentials to log in. They do not echo secrets to the console.
- The generated `.env.local` is created with restricted permissions (600) where possible.
