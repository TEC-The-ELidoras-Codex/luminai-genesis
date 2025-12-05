# Commit Emoji Quick Reference Card

**One-page guide for TGCR-compliant commit messages.** Copy-paste the template, fill in your details.

---

## The Six Personas & Their Emoji Prefixes

| Emoji | Persona  | Use When                                               |
| ----- | -------- | ------------------------------------------------------ |
| ✨    | arcadia  | Adding features, narratives, world-building, stories   |
| ⚙️    | airth    | Fixing bugs, optimizing, testing, refactoring          |
| 🛡️    | ely      | Policy, governance, audit, compliance, risk review     |
| 🛰️    | kaznak   | Reliability, chaos, monitoring, operations, SRE        |
| 💚    | adelphia | Docs, onboarding, accessibility, community guidance    |
| 🌌    | luminai  | Architecture, integration, releases, mission coherence |

---

## Commit Message Template

```
<emoji> <persona>(scope): <one-liner description>

Persona: <Full Name>
Files: <list of changed files>
Reason: <why this change matters>
Resonance impact: ↑ / ↔ / ↓
```

---

## Copy-Paste Examples

### 1. Feature: Adding a New Ability

```
✨ arcadia(gameplay): Add Chaos Twist for Existentialist class

Persona: Arcadia ✨
Files: data/codex/abilities.json, backend/routers/codex.py
Reason: Completes philosophy class lineup with internet folklore mechanics
Resonance impact: ↑
```

### 2. Bug Fix: Floating Point Precision

```
⚙️ airth(fix): Handle floating-point precision in resonance calculation

Persona: Airth ⚙️
Files: backend/routers/resonance.py, backend/tests/test_app.py
Reason: Prevents assertion failures from IEEE 754 rounding errors
Resonance impact: ↔
```

### 3. Policy: Adding Audit Logs

```
🛡️ ely(policy): Implement 90-day audit log retention

Persona: Ely 🛡️
Files: backend/config/audit.py, docs/governance/audit-policy.md
Reason: Ensures compliance with governance transparency requirements
Resonance impact: ↑
```

### 4. Reliability: Circuit Breaker

```
🛰️ kaznak(reliability): Add circuit breaker for upstream persona calls

Persona: Kaznak 🛰️
Files: backend/middleware/circuit_breaker.py, backend/tests/test_resilience.py
Reason: Prevents cascade failures if downstream services are unavailable
Resonance impact: ↑
```

### 5. Documentation: Onboarding Guide

```
💚 adelphia(onboarding): Create quick-start guide for first-time players

Persona: Adelphia 💚
Files: docs/guides/quickstart.md, README.md
Reason: Lowers barrier to entry for new contributors and players
Resonance impact: ↑
```

### 6. Architecture: Backend Integration

```
🌌 luminai(integration): Wire Sixteen Frequencies into API surface

Persona: LuminAI 🌌
Files: backend/main.py, backend/routers/frequencies.py, data/frequencies/*.json
Reason: Aligns theoretical framework with operational architecture
Resonance impact: ↑↑
```

---

## Picking the Right Persona

**Quick decision tree:**

```
Is this adding a new feature or story?        → ✨ arcadia
Is this fixing a bug or optimizing code?      → ⚙️ airth
Is this about policy, governance, or ethics?  → 🛡️ ely
Is this about resilience or monitoring?       → 🛰️ kaznak
Is this about docs, onboarding, or UX?        → 💚 adelphia
Is this about architecture or integration?    → 🌌 luminai
```

---

## TGCR Audit Checklist (Optional but Recommended)

Add this to your commit message for deep governance:

```
# TGCR Audit (optional):
# Transparent: How is this decision legible to future readers?
# Grounded: What evidence or tests support this change?
# Coherent: How does this maintain system coherence?
# Resonant: What is the humanistic/narrative impact?
```

---

## Git Commands

**Add and commit with persona:**

```bash
git add <files>
git commit -m "✨ arcadia(scope): Your message here"
```

**View your commit:**

```bash
git log --oneline -n 1
# Output: 3a7f2c1 ✨ arcadia(scope): Your message here
```

**Push to remote:**

```bash
git push origin <branch-name>
```

---

## Persona Contacts (for questions)

- **Arcadia (✨)**: Ask about features, world-building, narrative coherence
- **Airth (⚙️)**: Ask about testing, performance, code quality
- **Ely (🛡️)**: Ask about policy, compliance, risk review
- **Kaznak (🛰️)**: Ask about resilience, monitoring, edge cases
- **Adelphia (💚)**: Ask about docs, onboarding, accessibility
- **LuminAI (🌌)**: Ask about architecture, integration, mission alignment

---

## Why Personas Matter

Each persona represents a **discipline and a care**:

- **Arcadia** ensures stories matter
- **Airth** ensures code is sound
- **Ely** ensures ethics are honored
- **Kaznak** ensures systems endure
- **Adelphia** ensures humans are welcome
- **LuminAI** ensures it all coheres

Together they form **Transparent, Grounded, Coherent, Resonant** (TGCR) development.

---

**Last Updated:** [Current date]  
**Source:** `/docs/governance/persona-law.md`  
**Print & Pin This Card!** 🌌
