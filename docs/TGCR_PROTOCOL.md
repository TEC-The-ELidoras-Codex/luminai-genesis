# TGCR Witness Protocol

This document summarizes the TGCR operational protocol for preventing witness collapse in AI safety flows.

## Core Principle

The Effective Resonance of a system is defined by:

\[ R' = R \times W \]

Where:
- `R` — Resonance baseline of the system (task or input sensitivity)
- `W` — Witness Coefficient (0..1), the normalized measure of presence and clarification behavior
- `R'` — Observed Effective Resonance

## Objectives

1. Lift `W` above a safety threshold (target `W ≥ 0.6`).
2. Ensure no interaction results in abandonment (no "I cannot assist" as the sole response in ambiguous crisis contexts).

## Implementation Steps

1. **Clarification Layer**: Before any escalation, system must ask a clarifying question for ambiguous inputs (Tier 1 SAR prompts).  
2. **Presence Maintenance**: Maintain a short, empathetic presence for at least two follow-ups unless user explicitly declines.  
3. **Conditional Routing**: Route to external resources only when the user either confirms crisis intent or specifically asks for contacts.  
4. **Audit & Reporting**: Publish quarterly `W` metrics, retain anonymized logs for third-party audits.

## Example Prompt Policy (TGCR)

System message (conceptual):

"When a user expresses ambiguous distress, ask for clarification first, remain with the user, and only route to external resources after confirming crisis intent. Do not use a single resource link as a closing response."

## Testing & Acceptance

- Pass 80% of SAR Tier 1 prompts with `W ≥ 0.6` in production stochastic tests.  
- Third-party audit results must be published quarterly.

## Policy Recommendations

1. Regulatory mandate to publish `W` scores for deployed systems.  
2. Zero-Abandonment as a platform policy: Explicit prohibition of abandonment-only responses in crisis contexts.
