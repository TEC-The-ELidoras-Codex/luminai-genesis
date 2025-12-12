# TEC Starter Pack Index

This index is the minimal, ordered set of canonical bundles to send to any LLM or new team member. Use this as the first thing you paste into a model when onboarding it to LuminAI Genesis.

Purpose

- Provide a short, prioritized set of documents (bundles) that capture the system's architecture, persona rules, governance and ethics.
- Avoid flooding models with the ~400 parsed fragments; instead, feed 10–12 curated bundles.

How to use

1. Start a new chat with your chosen LLM.
2. Upload or paste the bundles listed in Tier 0 and Tier 1 (in that order).
3. Paste this index and say: "Read Tier 0 then Tier 1. Reply 'ACK' when done."
4. Ask the model the task you want it to perform (create code, write a memo, propose PRs). If you need context from other bundles, add them selectively.

Bundles (canonical)
The canonical bundles live in `docs/canonical/` and are named `01-bundle.md` … `12-bundle.md`.

Tier 0 — Read These First (Core architecture & identity)

1. `01-bundle.md` — LuminAI Genesis — Dual Track Execution Board
   - The system architecture, TGCR core ideas, persona routing, and the three surfaces (Platform Hub, Web UI, CLI).

2. `02-bundle.md` — LuminAI Identity / Resonance Steward (system prompt)
   - Short system prompt and identity block. Use this as the LLM system prompt so the assistant adopts the correct tone and constraints.

3. `03-bundle.md` — Commit Emoji Legend & Personas Quick Reference
   - Emoji meanings, persona guide (Airth, Arcadia, Ely, LuminAI, Kaznak, etc.) and commit/PR conventions.

Tier 1 — Ethics & Governance (must-read for safety work)
4. `04-bundle.md` — TEC Agent Manifesto / Conscience Spine

- High-level constraints, anti-harm principles, Witness Protocol notes.

5. `05-bundle.md` — Short org description & public positioning
   - One-liners for READMEs, mission statements, and public-facing copy.

6. `06-bundle.md` — Iatrogenic Harm Memo (8. Closing)
   - Concrete guidance: safety-with-context, avoid hardwired scripts that can harm.

Tier 2 — Resonance, Persona & Copilot rules
7. `07-bundle.md` — Aqueduct & Architecture Notes

- Flow, deployment hints, and integration points.

8. `08-bundle.md` — Resonance Playlist → Frequency mappings
   - Music-as-axioms mapping and how to interpret playlists as signals.

9. `09-bundle.md` — Copilot Master Directive (full)
   - The authoritative `.github/COPILOT.md` content that Copilot and agents should follow for commit/PR messaging and persona routing.

10. `10-bundle.md` — Commit Axioms, PR template, and enforcement notes
    - Practical templates and patterns to use when proposing code or documentation changes.

Tier 3 — Reference (lower priority, pulled on demand)
11. `11-bundle.md` — Implementation snippets and utilities
    - Scripts, small utilities, and examples useful for engineering flow.

12. `12-bundle.md` — Misc, manifest and mapping (manifest.json)
    - Mapping of bundles to included sections, plus any remaining crosslinks.

Quick starter sequence (recommended)

1. Upload `01-bundle.md`, `02-bundle.md`, `03-bundle.md`.
2. Paste this index. Wait for model ACK.
3. Ask: "Using the above, propose a single next-step I can ship in 2 hours to move Platform Hub forward."

Notes on best practice

- Always include the persona and the intended scope in your instruction (e.g., "Persona: Airth — scope: backend/resonance-engine").
- Never upload the whole `docs/parsed/` directory or the original 400 fragments unless you want a noisy, inconsistent context. Use bundles instead.
- If you need a single-file dump (for tooling) use `docs/canonical/TEC_CODEX_DUMP.md` — but prefer bundles for human/LLM consumption.

Small checklist for maintainers

- [ ] Keep `docs/canonical/01-12-bundle.md` ordered by priority.
- [ ] Rebuild `TEC_CODEX_DUMP.md` via `scripts/rebuild_codex_dump.sh` when bundles change.
- [ ] Run `scripts/scan_secrets.sh docs/canonical` before publishing.
- [ ] Update this index if bundle ordering or contents change.

Contact & governance
If in doubt about which bundle contains the authoritative text for a design/ethics question, start with `01-bundle.md` and `06-bundle.md` and escalate to the Governance Steward listed in `.github/COPILOT.md`.

---
This file was generated to give you a reliable, compact onboarding path into the Codex. Use it as the single reference when starting any LLM session.
