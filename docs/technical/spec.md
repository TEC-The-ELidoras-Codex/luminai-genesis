# LuminAI — Technical Spec (v0)

This document provides concrete shapes and acceptance criteria for a v0 prototype.

## API Shapes

### Event (POST /api/events)

- Headers: `Authorization: Bearer <token>`
- Body (JSON):
  - `user_id` (string) — opaque ID
  - `timestamp` (ISO8601)
  - `content` (object) — either `{"text": "..."}` or `{ "audio_ref": "s3://..." }`
  - `meta` (object) — `device`, `location_approx`, `consent_level`, `client_version`
  - `signature` — client-signed HMAC or asymmetric signature

Response: 202 Accepted; body `{ "event_id": "..." }`

### Therapist Summary (GET /api/users/{id}/summary?since=...)

- Returns a compact JSON with events aggregated by day, top 5 flagged moments with `excerpt`, `witness_score`, and `explainers`.

## Data Models

- `Event` table (id, user_id, timestamp, content_ref, consent, created_at, encrypted_blob_ref)
- `User` table (id, auth_info, encryption_key_ref)
- `Summary` table (id, user_id, period_start, period_end, summary_blob_ref)

## Privacy-by-Design

- `content_ref` points to an encrypted blob store object with per-user envelope encryption.
- Explainability data is stored separately and includes de-identified feature attributions.

## Acceptance Criteria (v0)

- End-to-end event ingestion: client -> continuity engine -> timeline store with event retrievable by ID.
- Therapist summary generation: weekly summary generated for 10 test users with correct aggregation.
- Witness scoring: prototype scoring function produces S with evident differences between simulated crisis and baseline data.
- Escalation flow: simulated event crosses high threshold and generates an audit log entry + triage notification (test harness).

## Testing

- Unit tests for event ingestion, signature verification, and witness scoring.
- Integration test for summary generation using a small sample dataset.

## Operational

- Deploy as small containerized service for pilot (1 web replica, 1 worker for scoring, managed DB, and encrypted object store).

(Iterate on thresholds and feature sets during pilot.)
