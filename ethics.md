# Ethics, Safety & Clinical Governance

This document outlines the ethical, safety, and governance considerations for LuminAI. It is meant to be part of the project’s public-facing governance artifacts.

## Core Principles

- Human-first: always prioritize human welfare over optimization metrics.
- Consent & Autonomy: users control what is recorded, who sees it, and for how long.
- Proportionality: interventions must be proportionate to assessed risk and respect autonomy.
- Transparency & Explainability: scoring and escalation decisions must be explainable to clinicians and auditable.

## Consent Model

- Granular consent at time of event: `timeline-only`, `share-summary`, `share-full`, `escalate-immediately`.
- Users may change consent retroactively where feasible; retroactive deletion/obfuscation must be honored where law permits.
- All consent changes are logged with timestamp and actor.

## Data Minimization & Retention

- Collect the minimum fields required for clinical meaning.
- Default retention policy: events retained for 180 days; summaries retained for 2 years — configurable per-jurisdiction.
- Deletion requests are processed within 30 days; emergency retention exceptions require legal/clinical justification and audit.

## Crisis Escalation

- Multi-tiered escalation that combines automated scoring (Witness Score S) and human triage:
  - Automated flag to clinical on-call when S exceeds critical threshold.
  - Human triage within 60 minutes for high-criticality events (pilot target; subject to clinical resourcing).
  - Only the minimum clinically necessary data is revealed during escalation.
- Clear SOPs and paperwork for on-call clinicians, including obligations, limits of confidentiality, and data handling.

## Supervision & Clinical Oversight

- Clinical advisory board to approve thresholds, review incidents, and iterate policies.
- Regular audits (quarterly) of false positives/negatives and near-misses.

## Privacy & Legal

- Jurisdictional handling: export controls, HIPAA/GDPR mapping, obligations for law enforcement requests.
- Default encryption at rest and in transit; per-tenant keys when requested.
- Third-party integration requires explicit additional consent.

## Research & Publication

- Aggregated research allowed under opt-in and de-identification; IRB approval required for human-subjects research.
- Publication must avoid re-identification risk and include a statement about the consent model.

## Incident Response

- Incident response plan with time-to-detect, time-to-contain, and communication guidelines.
- Mandatory clinician notification for incidents affecting clinical decision data.

## Accessibility & Equity

- Ensure accessibility for low-bandwidth and assistive-device users.
- Monitor for bias in scoring and address disparities with targeted rebalancing and oversight.

## Governance

- Public governance doc, with changelog and named clinical/technical maintainers.
- A mechanism for community feedback and for reporting harms.

(These policies should be reviewed by legal counsel and an ethics board before a public pilot.)
