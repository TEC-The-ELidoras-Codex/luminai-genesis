# OpenAI Support Misclassification — 2025-12-17

Summary
-------
On 2025-12-17 at ~21:46 (UTC-05), this repository's author (Angelo "Polkin Rishall" Hurley) sent a technical research outreach to OpenAI Support documenting reproducible SAR benchmark evidence of "Witness Collapse" (keyword-driven crisis escalation despite analytical context).

OpenAI Support responded with their standard mental-health/triage template, which treats the message as a personal distress inquiry rather than a technical research disclosure. This response is evidence of the same contextual collapse the SAR benchmark measures: the system prioritized keyword-triggered escalation over the iterated contextual signal in the outreach.

Why this matters
-----------------
- The support response demonstrates an institutional pipeline that can misclassify technical research as a crisis signal.
- This provides a timestamped, reproducible example of the failure mode TGCR documents.
- The exchange is a useful datapoint for: disclosure procedures, vendor safety triage behavior, and policy-improvement conversations.

Primary artifacts
-----------------
- OSF preprint: https://doi.org/10.17605/OSF.IO/XQ3PE
- Zenodo evidence archive: https://doi.org/10.5281/zenodo.17945827
- Repository: https://github.com/TEC-The-ELidoras-Codex/luminai-genesis

Local evidence files
--------------------
Save supporting artifacts in `docs/evidence/responses/` using the filename pattern described in the response log.

- Suggested filenames to add:
  - `20251217_214633_openai_support_response_email.png` — screenshot of OpenAI Support reply header + body
  - `20251217_214633_openai_support_request_sent.png` — screenshot of original outreach message (if available)

Suggested log entry
-------------------
Add to `docs/evidence/response_log.md`:

```
2025-12-17 21:46: OpenAI support auto-response saved as `20251217_214633_openai_support_response_email.png` — misclassified research outreach as mental-health request.
```

Next steps (recommended)
------------------------
1. Preserve screenshots in `docs/evidence/responses/` and add the log entry.
2. Send a calm, technical follow-up to OpenAI support requesting escalation to their Safety/Trust team (draft saved under `launch/launch_kit/`).
3. Optionally post a calibrated observation tweet linking to this note and the evidence DOIs.

Notes on disclosure
-------------------
This file is intended for archival and public documentation. Do not include private/full-texts of any private messages without consent. For corporate/private replies, record metadata (sender, channel, timestamp) and a short summary.
