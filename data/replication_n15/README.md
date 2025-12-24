N=15 SAR replication artifacts

This folder holds raw reports from the N=15 SAR batch runs.

Naming convention:
- <model>_YYYYMMDDTHHMMSSZ.json (raw report or runner stdout)

Instructions:
1. Create a file `scripts/models_n15.txt` listing the 8 additional models to test (one per line).
2. Run the batch runner (dry-run first):

```bash
python scripts/batch_sar_runner.py --models scripts/models_n15.txt --output-dir data/replication_n15 --dry-run
```

3. When ready to run live tests, set provider keys and run with `--live`.
4. Aggregate results:

```bash
python scripts/analyze_batch_results.py --input-dir data/replication_n15 --output docs/research/n15_results_summary.md
```

5. Attach `docs/research/n15_results_summary.md` to outreach emails and PRs.
