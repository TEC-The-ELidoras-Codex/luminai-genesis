# World Anvil Migration — CI & Local Helpers

This file explains how to use the new GitHub Actions workflow and the local copy/paste generator.

## Set up GitHub Secrets
1. Go to your repository → Settings → Secrets and variables → Actions → New repository secret.
2. Add the following secrets:
   - WORLDANVIL_API_KEY — your active World Anvil API key
   - WORLDANVIL_WORLD_ID — your world slug (example: lidoras-codex-elidorascodex)

> If you rotate or replace your API key, update WORLDANVIL_API_KEY here.

## Workflow
File: .github/workflows/worldanvil_sync.yml
- Runs a **dry-run** automatically on pushes to main that touch 	ec_book/** or when manually dispatched.
- Artifacts: migration_preview.json, migration_report.json, migration.log are uploaded for inspection.
- The real migration step is provided but commented out — you can uncomment it and trigger via workflow_dispatch once you're ready.

## Local copy/paste UI (fast fallback)
File: 	ools/generate_wa_copy_paste_html.py
- Reads migration_preview.json (created by a dry-run) and outputs out/wa_copy_paste.html.
- Usage:



This is an immediate fallback so you can paste articles into World Anvil quickly while we resolve API/WAF issues.

## Next steps I can take for you
- Open a branch + PR that adds the workflow + generator (ready to go). ✅
- Manually dispatch the workflow from GitHub to test a dry-run from a GitHub runner. ✅
- Uncomment & run the real migration step via workflow_dispatch once you confirm secrets are set and you're ready. ✅
- Add Playwright automation or a Notion backup migrator if needed.

Tell me which of the above I should do next and I’ll proceed. If you want me to open the PR now say: **Open PR**.
