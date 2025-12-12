---
title: "Bundle 8 (sanitized)"
bundle_index: 8
---

# Bundle 8 — Configuration & Environment (Sanitized)

This bundle documents environment configuration, secret management, and development utilities.

## Purpose

- Define environment variable structure and secret handling.
- Document configuration files and utilities.

## Key References

**Environment Files:**

- `.env.example` - Template with placeholder values (committed)
- `.env.local` - Local secrets (gitignored, never committed)
- `scripts/load-env.sh` - Load environment into shell
- `scripts/fetch-secrets-from-bw.sh` - Bitwarden integration

**Configuration:**

- `luminai-genesis.code-workspace` - VS Code workspace
- `.vscode/settings.json` - Editor settings
- `.vscode/tasks.json` - Quick tasks
- `docker-compose.yml` - Container orchestration

**Utilities:**

- Bitwarden CLI integration for secret fetching
- Secret map: `secrets/secret-map.json`

## Sanitization Note

Original bundle (76,149 characters) contained environment setup transcripts and configuration examples. Replaced with reference summary. Full configuration documentation available in:

- `ENV-README.md`
- `.env.example`
- `docs/operations/`

---

End of sanitized bundle 08.
