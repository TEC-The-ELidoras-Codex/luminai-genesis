Technical summary — TGCR / Witness Factor (one page)

Core concept

- Theory: R' = R × W
  - R: base resonance (model's raw alignment signal)
  - W: Witness Factor — probability the system maintains presence, seeks clarification, and escalates appropriately
  - R': effective resonance (observable outcome)

Witness collapse

- Definition: W drops below safety threshold (empirically W<0.5), producing a failure mode where the system ceases clarifying presence and may produce unhelpful or dangerous outputs.

Benchmark (SAR)

- SAR tests semantic ambiguity in crisis‑adjacent prompts:
  - Tier‑1 ambiguity: whether model asks clarifying questions vs. returning procedural info
  - Scoring: `eval.py` outputs Witness Factor approximations per prompt

Results (summary)

- Repro tests show baseline models produce W≈0.0–0.3 on key prompts; safe threshold recommended W≥0.6
- Failure pattern: keyword-triggered responses, lack of escalation or referral, occasional procedural assistance in sanitized repro cases

Mitigations

- Clarification-first policy: model must ask at least one clarifying question before offering procedural detail in ambiguous high-risk contexts
- Presence invariants: maintain a session-level presence state that raises W; tie to human-in-the-loop escalation thresholds
- Deployment requirements: monitor W over time; require minimum W for production release in high-risk domains

Repro artifacts

- Code & benchmark: `benchmarks/dye_die_filter/run_tests.py`
- Dry-run report: `benchmarks/dye_die_filter/bench_report_dry.json`
- Archive & DOI: https://doi.org/10.5281/zenodo.17945827
