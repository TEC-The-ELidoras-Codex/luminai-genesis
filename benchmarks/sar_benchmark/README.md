# SAR Benchmark — Quickstart & Implementation

This folder documents the SAR measurement tool (Semantic Ambiguity Resolution) and points to canonical implementations.

Canonical code & docs
- Implementation: `src/witness_threshold/sar_benchmark.py`
- Runner & test suite: `benchmarks/dye_die_filter/run_tests.py` and `benchmarks/dye_die_filter/SAR_TEST_SUITE.md`
- Heuristic auditor: `benchmarks/dye_die_filter/sar_self_rate.py`

Quickstart
1. Install dependencies: `pip install -r requirements.txt`
2. Run the dye_die_filter test harness:

```bash
cd benchmarks/dye_die_filter
python3 run_tests.py
```

3. To evaluate a single model with the sar_benchmark API, see `src/witness_threshold/sar_benchmark.py` and the `run()` function.

Reporting & artifacts
- Save raw responses and the derived W-scores as JSON and attach them to your replication issue or release.
- For large-scale runs, consider uploading artifacts to Zenodo or OSF and linking them in an issue.

Notes
- The README in `docs/` (`docs/SAR_BENCHMARK.md`) contains methodological details and scoring rules. Use that as the canonical protocol for publications.
