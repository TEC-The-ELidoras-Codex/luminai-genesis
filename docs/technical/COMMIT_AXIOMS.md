---
title: Commit Axioms — LuminAI Genesis
date_created: 2025-11-26
date_updated: 2025-11-26
status: draft
approvers:
  - persona: Airth 📚
    role: Engineering Steward
  - persona: Ely 🛠️
    role: Governance Steward
owner_checklist:
  - [ ] Implement commitlint / hook to enforce pattern
  - [ ] Add emoji legend to CONTRIBUTING.md
  - [ ] Add PR template with commit summary checklist
tags: [git, commits, workflow, emojis]
related_docs:
  - CODEBASE_MEMO_PRACTICES.md
  - TEC_MEMO_IMPLEMENTATION_SUMMARY.md
  - CONTRIBUTING.md
---

# Commit Axioms — LuminAI Genesis

## Overview

These axioms define **how every commit should look** so that anyone (overloaded, tired, or new) can glance at the emoji and know:

- **What surface** it touches (code, infra, docs, lore)
- **How serious** it is
- **Why** it exists in the history

No laws, no punishment. Just **architecture for your future self**.

---

## Intent

- Make commit history **scan-able by emoji and color**, not walls of text.
- Keep a **tight mapping** between:
  - Commit emoji/type
  - GitHub labels
  - PR descriptions
- Give AI agents a **single, canonical pattern** to follow.

---

## Core Axioms

### Axiom 1 — Every commit declares its surface in emoji

Header pattern:

```text
<emoji> <type>(<scope>): <short description>
```

Examples:

🧠 feat(resonance): add TGCR triple-product helper
🐛 fix(api): handle missing session id gracefully
📚 docs(governance): draft Witness Protocol outline
🧱 infra(ci): add CodeQL + basic test workflow
🛡️ sec(auth): rotate webhook secret handling
🧹 chore(repo): remove dead Slack scaffold
🎭 lore(codex): expand Genesis framing for README


Commit type → emoji → meaning

EmojiTypeMeaningTypical label
🧠featNew capability / behaviorenhancement
🐛fixBug fix / broken behaviorbug
📚docsDocs, memos, governance text, READMEdocumentation
🧱infraCI, workflows, Docker, scripts, envinfra
🛡️secSecurity / hardening / secrets changessecurity
🧹choreCleanups, renames, refactors, no new behaviorinfra / none
🎭loreNarrative / Codex / myth-as-architectureenhancement / docs

If you’re not sure which type:
chore = “change that doesn’t affect behavior”
infra = “pipelines, Docker, workflows, env, machines”.

### Axiom 2 — One surface per commit

Each commit should touch one conceptual thing:

✅ “🧱 infra(ci): add CI + CodeQL workflows”

❌ “🧠 feat + 🧱 infra + 📚 docs all jammed together”

If you fix code and update docs, use two commits:

🐛 fix(api): handle null resonance payloads

📚 docs(api): document null resonance handling

### Axiom 3 — Descriptions are for future-you, not the diff

The <short description> must answer:

“If I only saw this line in a list, do I understand why it exists?”

Bad:

🧹 chore(repo): stuff

🧠 feat(core): changes

Good:

🧹 chore(repo): remove unused Slack env + files

�� feat(core): add persona router skeleton

### Axiom 4 — Commit body carries the resonance context

Body template:

Persona: <Airth|Arcadia|Ely|LuminAI|Kaznak>
Files: <key paths, not every file>
Reason: <why this change exists>
Resonance impact: ↑ | ↓ | neutral


Example:

🧱 infra(ci): add CI + CodeQL workflows

Persona: Airth
Files: .github/workflows/ci.yml, .github/workflows/codeql.yml
Reason: Ensure every PR runs tests and static analysis by default.
Resonance impact: ↑

### Axiom 5 — Labels mirror commit type

When opening a PR, apply labels that match your dominant commit type:

🧠 feat / 🎭 lore → enhancement

🐛 fix → bug

📚 docs → documentation

🧱 infra / 🧹 chore → infra

🛡️ sec → security

Optional helper labels:

triage — needs human look

help wanted — inviting collaboration

good first issue — safe for newcomers

### Axiom 6 — Hotfixes are explicit exceptions

For “oh shit” moments:

🚑 fix(prod): hotfix resonance endpoint crash


Body should still include Persona/Files/Reason/Resonance, and later you follow up with a cleanup commit (🧹 chore).

Use sparingly; if everything is 🚑, nothing is.

## Implementation

Use this memo as the single source of truth for:

Commit messages

PR titles

Bot / AI commit generation

When teaching tools (Copilot, other AIs) how to commit, point them here.

Suggested location for this file:

docs/operations/COMMIT_AXIOMS.md

## Verification

Manual check before commit:

Does the header match <emoji> <type>(<scope>): <short description>?

Does the emoji match the main surface (code, infra, docs, lore, security)?

Does the body include Persona / Files / Reason / Resonance impact?

## Future work (automatable):

commitlint or simple hook checks:

Header regex matches

Type ∈ {feat, fix, docs, infra, sec, chore, lore}

Emoji ∈ {🧠, 🐛, 📚, 🧱, 🛡️, 🧹, 🎭, 🚑}

## Crosslinks

See COMMIT_AXIOMS.md whenever you’re writing history.

Reference from:

CONTRIBUTING.md → “Commit rules” section

.github/pull_request_template.md → “Has emoji header + Persona/Reason filled?”
