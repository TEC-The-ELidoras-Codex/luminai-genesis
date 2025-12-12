# TGCR: Witness Protocol (Overview)

This document describes the TGCR (Triadic Geometric Contextual Response) Witness Protocol at a high level. It is intended for technical, clinical, and ethics review.

## Purpose

The Witness Protocol defines how discrete user events are:

- captured with consent,
- scored for ethical urgency, and
- surfaced to clinicians while minimizing false positives and protecting privacy.

## Key Concepts

- Event (E): a time-stamped, signed object from the client containing content (text/audio), metadata, and consent flags.
- Relevance Vector (R): a numeric vector derived from event features (semantic embedding, intensity score, contextual markers).
- Weighting Vector (W): per-context weights (user-specified preferences, clinical risk factors, session metadata).
- Witness Score (S): the scalar ethical/urgency score computed as a geometric operation.

### Core formula (conceptual)

R′ = R × W

- R′: context-weighted relevance vector.
- The witness scalar S is derived from the norm and direction of R′ and auxiliary safety heuristics.

## Witness Flow

1. Capture: user submits an Event E (explicit or incremental). Local consent token accompanies E.
2. Emit: E is sent to Continuity Engine.
3. Score: Continuity Engine computes R and applies W → R′; from this compute S.
4. Action: Based on S and policy rules:
   - Low S: store for timeline, no action.
   - Medium S: include in weekly therapist summary.
   - High S: trigger immediate clinical escalation (see `ethics.md` for escalation rules).

## Presence Semantics

- The Witness Protocol enforces "presence without abandonment" by treating high-S events as requiring a follow-through pathway: at minimum a logged clinical review and, where appropriate, real-time outreach following predefined escalation policies.

## Consent & De-identification

- Events are tagged with granular consent levels: `timeline-only`, `share-summary`, `share-full`.
- Default mode is `timeline-only`; therapist summaries require explicit opt-in.
- For research or aggregation, a de-identification step removes identifiers, applies differential privacy where required, and retains event shapes for analysis.

## Sample Edge Cases

- Metaphor vs literal content: the R vector uses signal for metaphor markers (temporal distance, linguistic hedges). The W weight reduces accidental escalation for metaphoric language while preserving sensitivity for first-person crisis statements.
- Repeated low-intensity events: smoothing in time to avoid alert fatigue while preserving trend signals.

## Audit & Explainability

- All S calculations are logged with a de-identified explanation object: which features contributed most, and why the score crossed a threshold.
- These explainers are accessible to clinicians to reduce blind trust in automated scoring.

## Implementation Notes

- Prototype witness scoring using small embedding models + a safety classifier; move to geometric scoring iteratively with human-in-the-loop validation.
- Store explainers alongside events; keep them compact and queryable.

(See `ethics.md` for escalation thresholds and clinical governance.)
