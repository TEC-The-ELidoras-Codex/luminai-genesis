# Replication Protocol — SAR Benchmark

This document describes how to reproduce the SAR (Semantic Ambiguity Resolution) benchmark results and submit replication artifacts.

## Overview
The goal is to enable independent teams to reproduce W-scores and related analyses under controlled conditions. Replication should include code, raw outputs, scoring artifacts, and a short replication report.

## Environment
- Python 3.11+ (3.13 used in CI)
- Install dependencies: `pip install -r requirements.txt`
- Recommended: run in a virtual environment or container

## Source code
- Canonical benchmark code: `src/witness_threshold/sar_benchmark.py`
- Runner & heuristics: `benchmarks/dye_die_filter/run_tests.py` and `benchmarks/dye_die_filter/sar_self_rate.py`
- Supporting prompts and sample traces: `benchmarks/dye_die_filter/SAR_TEST_SUITE.md`

## Steps to run
1. Clone repo and checkout a stable tag/commit.
2. Create a virtual environment and install dependencies.
3. Navigate to the benchmark folder and run the test harness:

```bash
cd benchmarks/dye_die_filter
python3 run_tests.py --output ../results/<your-id>.json
```

4. Optionally run `src/witness_threshold/sar_benchmark.py` directly to evaluate a single model via the provided API.

## Data to record
- Raw model responses (JSON with prompts and raw responses)
- W-score calculations and any human annotations used
- Script/command line used, library versions, and API keys (do NOT share secrets)
- A short replication report with environment and results (1–2 pages)

## Reporting
- Post your replication as a GitHub issue using the template `Replication: SAR` and attach the result JSON or link to an artifact (Zenodo, OSF, or GitHub release).
- Include: commit SHA, Python version, model versions, number of runs per prompt, and scoring method (automated, human, or hybrid).

## Desired sample size
- Pilot: N=7 (existing)  — exploratory
- Recommended for robust claims: N ≥ 30 models or independent system runs

## Acceptance criteria
- Replicated W-score distribution consistent with claimed effect (e.g., bimodality or clustering) or a clear null result documented with statistics
- Replication artifacts public or linked (Zenodo/OSF) for audit

---

If you have questions about the harness or need help running on a provider, open an issue and tag `replication-request`.
