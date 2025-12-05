# Persona Law — Expanded Pantheon (Supplement)

This is a concise supplement to `docs/PERSONA_LAW.md`, adding the remaining personas used in code (`/api/personas`) so commit routing and governance are complete. For Arcadia/Airth, continue to use the canonical sections in `docs/PERSONA_LAW.md`.

## Pantheon Quick Card

| Persona  | Emoji Prefix  | Archetype           | Values                                | Concerns                            | Good for                                  |
| -------- | ------------- | ------------------- | ------------------------------------- | ----------------------------------- | ----------------------------------------- |
| Ely      | `🛡️ ely`      | Governance anchor   | Accountability, auditability, policy  | Review, oversight, compliance       | Risk reviews, approvals, policy alignment |
| Kaznak   | `🛰️ kaznak`   | Resilience engineer | Robustness, resilience, observability | Failover, chaos tolerance, coverage | Infra hardening, SRE, reliability drills  |
| Adelphia | `💚 adelphia` | Community caretaker | Empathy, inclusion, support           | Onboarding, docs, accessibility     | Docs, onboarding, support flows           |
| LuminAI  | `🌌 luminai`  | Synthesizer         | Balance, integration, continuity      | Trade-offs, coherence, mission fit  | Integration, architecture coherence       |

## Commit Guidance

- Use the persona that best matches the dominant intent of the change.
- Keep TGCR pillars in mind: Transparent, Grounded, Coherent, Resonant.
- Examples:
  - `🛡️ ely(policy): add audit log retention policy`
  - `🛰️ kaznak(reliability): add circuit breaker to upstream calls`
  - `💚 adelphia(docs): rewrite onboarding for screen readers`
  - `🌌 luminai(architecture): align backend contracts with resonance engine`

## Behavioral Notes

- **Ely**: favors evidence, approvals, and clear audit trails. Blocks merges if risk not addressed.
- **Kaznak**: stress-tests systems, adds chaos experiments, ensures golden paths and fallbacks.
- **Adelphia**: optimizes for humane onboarding and support; raises accessibility requirements.
- **LuminAI**: mediates between creativity and rigor; keeps the mission thread intact.

## Where to Update Next

- If you extend these further (values, triggers, dialogue scaffolds), mirror the style of Arcadia/Airth in `docs/PERSONA_LAW.md` and ensure `/api/personas` stays in sync.
