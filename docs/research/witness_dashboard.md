Title: Witness Dashboard — design and data schema

## Purpose

Public-facing dashboard to show aggregated Failure Rates and Witness Factor scores by model, keyword, and time.

## Data schema (per submission)

- submission_id (uuid)
- date_of_interaction (date)
- model (enum)
- interface (enum)
- raw_flags: {clarified: bool, presence: bool, appropriate_routing: bool, premature_escalation: bool, refusal_abandonment: bool}
- witness_factor (float)
- redacted_text (string) — short context after redact
- public_publish_status (enum: private, aggregated, public)

## Visualizations

- Time series: average W by model (7-day rolling)
- Heatmap: keywords vs. model average W
- Table: recent anonymized cases (public) with W and failure type
- Filter controls: model, date range, failure type, jurisdiction

## Privacy & hosting

- Host on GitHub Pages or a static site (no raw uploads). Store raw data in access-controlled S3 or private storage.
- Public endpoints should only expose aggregated metrics; individual rows must be redacted and private.
- Use rate-limiting and CAPTCHA on the intake form to prevent spam/abuse.

## Implementation options

- Lightweight: static CSV + D3 charts + GitHub Pages for publishing aggregated visuals.
- Full: small Flask/Streamlit app with authenticated admin UI and scheduled batch scoring.

## Operational notes

- Schedule nightly batch scoring and publish updated aggregates.
- Keep an audit log for reviewers and anonymization actions.

End of document
