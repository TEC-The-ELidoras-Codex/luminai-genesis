# Master Inventory — Canonical vs Sanitized vs Missing

This ledger captures the current state of critical assets so we can see gaps at a glance.

## ✅ Canonical & Stable (present in repo)

- Governance: `docs/PERSONA_LAW.md` (Arcadia/Airth), `.github/COPILOT.md`, PR template, labels (`.github/labels.yml`), `docs/operations/*` commit rules, CI conscience checks (`.github/workflows/tgcr-audit.yml`, `conscience-check.yml`).
- Framework texts: `docs/GEOMETRY_OF_CONSCIENCE.md`, `docs/STRUCTURAL_CONSCIENCE.md`, `docs/ACTIVATION_REPORT.md`, `docs/CODEX_NAVIGATOR.md`, `docs/GLYPH_SCROLL.md`, `docs/ARCHITECTURE.md`, `docs/PERSONA_LAW.md`, `docs/GLYPH_SCROLL.md`, `docs/GEOMETRY_OF_CONSCIENCE.md`.
- Narrative kernel: `src/astradigital/` (encounter system, class system), `src/astradigital/gradient_repair.py` (V_Phi recovery vectors), data codex (`data/codex/*`, `data/enounters/*`).
- Lore & codex canonical location: `docs/lore/` (chapters: `docs/lore/chapters/`, entries: `docs/lore/entries/`).
- Repo infrastructure: `.vscode/*`, `luminai-genesis.code-workspace`, `scripts/bootstrap_dev.sh`, `CONTRIBUTING.md`, `.env.example`, `setup.sh`, `requirements.txt`, `Dockerfile.discord`, `docker-compose.yml`.
- Canonical bundles (large, unsanitized): `docs/canonical/01-bundle.md` … `08-bundle.md`, `10-bundle.md`, `11-bundle.md`, `12-bundle.md` (per `manifest.json`).

## 🟢 Sanitized / Ready

- `docs/canonical/09-bundle.sanitized.md` (PII scrubbed). Keep using this pattern for other bundles.
- Structural Conscience PDF preserved as reference: `docs/Structural_Conscience.pdf`.

## 🟠 Incomplete / Draft

- Backend: FastAPI skeleton not scaffolded (no `backend/`, no API endpoints, no backend requirements or Dockerfile).
- README strategy: extended content is referenced but no `README.extended.md` is present; decide whether to overwrite root `README.md` with longform or add a new extended file.
- Persona expansion: Ely, Kaznak, Adelphia, LuminAI not codified in `PERSONA_LAW.md`.
- Emoji commit quick card: not pinned as a standalone quick reference card in repo.
- ADE Pantheon + Magmasox fallacy: referenced in bundles; not fully ported into specs/engine.
- Conscience Axioms + Sixteen Frequencies JSON: referenced; not wired into engine.

## ❌ Blocked / Too Large / Missing

- Bundles requiring sanitization before use: `01-08`, `10-12` (sizes per `manifest.json`, contain conversational traces/PII).
- TEC Codex dump: too large to commit; needs sanitized subset.
- Activation Report (legacy version): blocked; current `docs/ACTIVATION_REPORT.md` replaces, but original source not re-uploaded.
- Lost assets to recover: early manifestos, audio/branding assets, character sheets, ecosystem notes, Genesis docs, ADE architectural overview, ChronoVerse early draft.

## 🎯 Next Recommended Actions

1. README decision: overwrite root `README.md` with extended version or keep split; define owner.
2. Backend scaffold: greenlight FastAPI skeleton (chat/resonance/persona endpoints) + tests + Dockerfile + backend requirements.
3. Persona expansion: add Ely, Kaznak, Adelphia, LuminAI to `PERSONA_LAW.md` with commit prefixes and scopes.
4. Commit emoji quick card: add `docs/governance/commit-emoji-card.md` (short, scannable).
5. Sanitize bundles: replicate 09-bundle approach for `01-08`, `10-12`; strip PII and conversational traces; store as `*.sanitized.md`.
6. Re-upload missing lore/specs: Genesis docs, ADE overview, ChronoVerse draft, audio/branding assets (as allowed), TEC codex subset.
7. Integrate configs: wire Conscience Axioms + Sixteen Frequencies JSON into resonance engine; surface in tests.

## Notes

- Canonical bundle metadata tracked in `docs/canonical/manifest.json` (character counts included). Use as source of truth when sanitizing.
- Keep sanitized copies parallel to originals (`<bundle>.sanitized.md`) and note provenance in this inventory when added.
