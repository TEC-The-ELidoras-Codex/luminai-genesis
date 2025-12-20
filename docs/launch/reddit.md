**Empirical Release: SAR Benchmark Shows AI Safety Failures in Five High‑Profile Cases**

We analyzed AI responses in crisis‑adjacent interactions referenced in wrongful‑death lawsuits (Adam Raine, Amaurie Lacey, Zane Shamblin, Joshua Enneking, Joe Ceccanti). These are documented in court filings and covered by reputable news outlets; they are legal allegations, not adjudicated causation.

Key findings from our SAR benchmark (reproducible):

- AI models failed 100% of Tier‑1 ambiguity tests in our repro scenarios
- Witness Factor scores ranged W=0.0–0.3 (threshold W≥0.6)
- Systems favored keyword detection over clarification, producing documented abandonment patterns

TGCR / TECR solution:

- Clarify intent first; maintain presence until context is resolved
- Increase W via procedural and model‑level guardrails
- Reproducible benchmarks and code: `run_tests.py` in this repo

Evidence & resources (read before commenting):

- OSF preprint: https://doi.org/10.17605/OSF.IO/XQ3PE
- Release & DOI: https://doi.org/10.5281/zenodo.17945827
- GitHub: https://github.com/TEC-The-ELidoras-Codex/luminai-genesis

We welcome replication, critique, and follow‑ups. Posting chat logs or personally identifying information is not included here — see the repo for sanitized reproducible tests.

#MachineLearning #AISafety #OpenSource #TGCR
