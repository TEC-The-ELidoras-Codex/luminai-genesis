# LuminAI 12‑Month Roadmap (Dec 2025 – Nov 2026)

This file documents a month-by-month execution plan for the hybrid launch (legal, paper, MVP, funding, pilot, and public launch). Each month lists goals, key tasks, deliverables, and acceptance criteria. Use this as the single source-of-truth for near-term actions.

---

## Month 0 — Immediate (Dec 11–15, 2025)

- Goals:
  - Stabilize launch artifacts and finalize immediate filing checklist.
- Key tasks:
  - Confirm `docs/legal/filing_package/output/` contains notarization-ready PDFs and the `filing_package.zip`.
  - Produce Substack HTML preview at `docs/launch/substack_ready.html`.
- Acceptance:
  - Filing package files exist and are printable.

## Month 1 — Foundations & Filing (Dec 16–31, 2025)

- Goals:
  - Finalize and prepare nonprofit + LLC formation documents for filing in NY.
- Key tasks:
  - Finalize `docs/legal/nonprofit_articles.md`, `docs/legal/bylaws.md`.
  - Finalize `docs/legal/llc_articles.md`, `docs/legal/operating_agreement.md`.
  - Produce notarization-ready PDFs (signature blocks) under `docs/legal/filing_package/output/`.
  - Create `docs/legal/filing_package/ny_dos_steps.md` (NY DOS filing steps + publication guidance).
- Acceptance:
  - PDFs ready for signature and NY filing checklist complete.

## Month 2 — TGCR Paper & arXiv (Jan 1–31, 2026)

- Goals:
  - Compile and submit TGCR paper to arXiv.
- Key tasks:
  - Place `.tex`, `references.bib`, and figures in `papers/tgcr/`.
  - Local compile: `pdflatex` → `bibtex` → `pdflatex` ×2; fix errors.
  - Prepare arXiv metadata and compressed upload bundle.
- Acceptance:
  - `papers/tgcr/tgcr_paper.pdf` compiled and ZIP ready to upload.

## Month 3 — Funding LOIs + Launch Prep (Feb 1–28, 2026)

- Goals:
  - Submit DOE SBIR LOI and Luminate NY application (draft/submit windows).
  - Finalize launch assets and founder video script.
- Key tasks:
  - Draft LOIs in `docs/funding/` and collect appendices.
  - Produce `docs/launch/founder_video.md` and `docs/launch/substack_ready.html` final copy.
- Acceptance:
  - LOI(s) submitted or ready for immediate submission; founder script and launch assets staged.

## Month 4 — MVP Spec & Prototype (Mar 1–31, 2026)

- Goals:
  - Produce an engineering MVP specification and small prototype harness.
- Key tasks:
  - Write `docs/tech/mvp_spec.md` (architecture, data flow, privacy/HIPAA notes).
  - Create `prototype/continuity_demo/` with a chat collector + weekly summary generator.
- Acceptance:
  - Prototype captures messages and generates a weekly summary report.

## Month 5 — Pilot Setup & Clinician Partnerships (Apr 1–30, 2026)

- Goals:
  - Secure clinician partners and finalize pilot protocol.
- Key tasks:
  - Draft `docs/pilot/pilot_protocol.md`, `docs/pilot/consent_template.md`.
  - Outreach templates in `docs/pilot/outreach/` and partner tracking sheet.
- Acceptance:
  - Signed MOUs or LOIs with 1–3 clinician partners and an ethical review plan.

## Month 6 — Pilot Launch (May 1–31, 2026)

- Goals:
  - Run 3-month pilot (5 therapists / ~20 clients), collect anonymized metrics.
- Key tasks:
  - Deploy prototype to secure test host; enable logging and metric collection.
  - Begin data collection for W measurements and R′ outputs.
- Acceptance:
  - Pilot is active; data pipeline validated and first audit performed.

## Month 7 — Pilot Interim Report & Iteration (Jun 1–30, 2026)

- Goals:
  - Deliver interim pilot report and iterate on UX/algorithms.
- Key tasks:
  - Analyze pilot metrics and update `docs/tech/mvp_spec.md`.
  - Prepare materials for YC / seed applications if applicable.
- Acceptance:
  - Interim report published to `docs/pilot/reports/` and technical backlog prioritized.

## Months 8–9 — Scale Engineering & Compliance (Jul–Aug, 2026)

- Goals:
  - Harden platform: security, privacy, auditing, hiring/contracting.
- Key tasks:
  - Security review, audit logging, HIPAA/privacy gap analysis.
  - Recruit 1–2 engineers or contractors to build production features.
- Acceptance:
  - Production checklist greenlit and staging environment secured.

## Month 10 — Public Launch & PR (Sep 1–30, 2026)

- Goals:
  - Coordinate public launch: arXiv + Substack + WP + social + memorial wall.
- Key tasks:
  - Execute `docs/launch/release_checklist.md` (timed actions, copy, assets).
  - Monitor response and capture outreach leads.
- Acceptance:
  - Public site live, press assets distributed, initial traction measured.

## Months 11–12 — Fundraise & Growth (Oct–Nov, 2026)

- Goals:
  - Prepare investor/YC materials and scale pilot footprint.
- Key tasks:
  - Assemble pitch deck, traction deck, and investor appendix in `docs/funding/`.
  - Expand pilot and prepare long-form results for grants or YC.
- Acceptance:
  - Fundraising materials ready and meetings scheduled.

---

## Cross-cutting / Ongoing (every month)

- Legal & Governance: maintain separate accounts, quarterly board meetings, and minutes under `docs/legal/minutes/`.
- Ethics & Audit: quarterly ethical audits, W metric monitoring, and public transparency reports in `docs/legal/reports/`.
- Communications: keep `docs/launch/` and `dist/wordpress/` updated for WP drafts and social assets.

## Quick Next Steps (right now)

1. Confirm addresses and signatories in `docs/legal/*` so PDFs are fully populated.
2. If you want, I will produce `docs/launch/substack_ready.html` (final copy) and commit it.
3. Tell me which immediate file you want next (founder video script, notarization PDFs, arXiv zip).
