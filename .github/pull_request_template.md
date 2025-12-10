# 🔁 LuminAI Genesis — Pull Request

> **Title format (commit-style)**
> Use:
> `EMOJI type(scope): short description`
> Examples:
> - `🧠 feat(core): add TGCR resonance engine`
> - `🏗 chore(ci): add CodeQL + CI workflows`
> - `📜 docs(governance): add Witness Protocol memo`

---

## 1️⃣ What does this PR do?

<!-- High-level summary in plain language. What changed and why? -->

- [ ] Core functionality
- [ ] Infra / CI
- [ ] Docs / Governance
- [ ] UI / UX
- [ ] Tests only
- [ ] Other

**Summary:**

- …

---

## 2️⃣ Commit Axioms (must be true)

For each **commit in this PR**, the body should include:

- **Persona** responsible
- **Files / area** touched
- **Reason** for change
- **Resonance impact** (↑ / ↓ / neutral)

Example commit body:

```text
Persona: Airth 📚
Files: backend/app/api/resonance.py, resonance/engine.py
Reason: Implement TGCR triple product and wire to /api/resonance.
Resonance impact: ↑
```

> ✅ Before merging, confirm:
>
> * [ ] Every commit **has** Persona / Files / Reason / Resonance in the body
> * [ ] Title follows `EMOJI type(scope): description` format

---

## 3️⃣ Emoji Legend (quick brain card)

Use **one main emoji** in the title to signal what this PR *is*:

* 🧠 **feat** — Core features / resonance engine / personas
* 🐛 **fix** — Bug fixes, regressions, broken behavior
* 📜 **docs** — README, memos, governance, comments
* 🧪 **test** — Tests only (unit/integration)
* 🏗 **chore/infra** — CI, workflows, tooling, repo plumbing
* 🎨 **ui** — Frontend, styling, UX
* 🔐 **sec** — Security fixes, hardening, secret handling
* 🧹 **ref** — Refactors, cleanups, no behavior change

Pick the closest one. If in doubt, default to:

* **🧠 feat** for new capabilities
* **🏗 chore** for infra / yml / wiring
* **📜 docs** for words + diagrams

---

## 4️⃣ Persona & Scope

**Primary Persona for this PR (pick one):**

* [ ] 📚 **Airth** — engineering, correctness, architecture
* [ ] 🛠 **Ely** — infra, CI, ops, safety rails
* [ ] 🎭 **Arcadia** — narrative, README top sections, framing
* [ ] 🧠 **LuminAI** — onboarding, guides, examples
* [ ] 🦅 **Kaznak** — compression, simplification, pruning

> Optional note (1–2 sentences) on why this persona is primary:

…

---

## 5️⃣ Resonance & Risk

**Resonance impact:**

* [ ] ↑ Increases coherence / safety / clarity
* [ ] ↓ Removes something harmful / noisy / confusing
* [ ] ⬜ Neutral (no real impact on resonance, just wiring)

**Risk level:**

* [ ] 🟢 Low — tests pass, scoped change
* [ ] 🟡 Medium — touches core paths (engine, auth, CI)
* [ ] 🔴 High — migrations, secrets, or production infra

---

## 6️⃣ Checklist (Steward sanity)

* [ ] 🔍 I ran tests locally (or explained why not)
* [ ] 🧪 I added / updated tests where behavior changed
* [ ] 📜 I updated docs / memos if behavior, API, or contracts changed
* [ ] 🔐 I did **not** commit secrets; env stays in `.env.local` / Bitwarden
* [ ] 🧠 I followed the commit axiom pattern for each commit body

---

## 7️⃣ Links / Context (optional)

* Related Issues:

  * Closes #… / Relates to #…
* Related Memos / Docs:

  * `docs/...`
* Screenshots / logs (if helpful):

…
