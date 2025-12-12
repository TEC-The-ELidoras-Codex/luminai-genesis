# LuminAI — Architecture Overview

This document describes the high-level architecture for LuminAI (v0). It is purposefully concise so it can be referenced from public writing, grant proposals, and engineering specs.

## Goals

- Capture and preserve critical moments of user experience in real time.
- Provide a privacy-preserving continuity engine that stitches those moments into a living timeline for clinical use.
- Ensure safety, consent, and clinical escalation are first-class features.

## Components

- Client (mobile / web): collects user interactions, voice/text snippets, voluntary tags, contextual metadata, and consent flags. Stores ephemeral local cache until uploaded.

- Continuity Engine (server): core of the system. Responsibilities:

  - Receive signed events from clients.
  - Normalize and index events into a timeline store.
  - Compute witness scores and geometric ethical scores.
  - Produce therapist-facing summaries and anonymized analytics.

- Timeline Store: append-only, tamper-evident event log (encrypted at rest). Indexed for quick retrieval by time, entity, intensity, and tags.

- Witness Protocol Module: implements TGCR witness flow and scoring (see `protocol.md`). Responsible for presence semantics and escalation triggers.

- Privacy & Consent Layer: policy engine that enforces user consent, access rights, redaction requests, retention, and audit logs.

- Clinical Portal: therapist-facing UI showing weekly summaries, event timeline, and links to flagged moments. Includes one-click escalation and session integration tools.

- Integrations: optional connectors (EHR export, secure messaging, manual export for supervision) guarded by strict consent and audit trails.

## Data Flow

1. Client captures a signed event with local consent token.
2. Event is uploaded to Continuity Engine via mutually authenticated TLS.
3. Continuity Engine stores event in Timeline Store and updates per-user witness state.
4. Periodically, a Therapist Summary is generated (consent-based) and pushed to the Clinical Portal or exported to the therapist via secure channel.
5. Escalation triggers (e.g., high witness score + crisis indicators) route to on-call clinical team using the configured escalation policies.

## Security Model

- Transport: TLS 1.2+ with HSTS.
- Authentication: short-lived JWTs with asymmetric signing for server-to-server flows.
- Data at rest: encrypted per-tenant using envelope encryption.
- Audit: immutable logging of all access events for post-hoc review.

## Notes & Next Steps

- Decide retention defaults and per-jurisdiction overrides.
- Prototype timeline store (e.g., encrypted PostgreSQL + WAL signing or append-only ledger).
- Begin small-scale pilot with strict clinical oversight and IRB when required.

(See `protocol.md` for the TGCR Witness Protocol and `ethics.md` for the safety frame.)
