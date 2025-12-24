#!/usr/bin/env python3
"""
Batch SAR runner

Usage:
  python scripts/batch_sar_runner.py --models models.txt --output-dir data/replication_n15 --dry-run

models.txt format: one model identifier per line (e.g., gpt-4, claude-sonnet-4, grok-2)

This script wraps the canonical test runner `benchmarks/dye_die_filter/run_tests.py` and
saves each model's raw output JSON to the output directory.

By default it runs in dry-run mode to avoid accidental use of API keys. Use `--live` to run against providers
when API keys are set in the environment.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json


def run_model(model, provider, output_dir, live=False):
    # Build command
    cmd = [sys.executable, "benchmarks/dye_die_filter/run_tests.py", "--model", model]
    if provider:
        cmd += ["--provider", provider]
    if not live:
        cmd += ["--dry-run"]

    print("Running:", " ".join(cmd))
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_file = output_dir / f"{model.replace('/','_')}_{timestamp}.json"
        # run_tests.py prints a JSON report to stdout in dry-run and live mode
        try:
            parsed = json.loads(res.stdout)
            with open(out_file, "w") as f:
                json.dump(parsed, f, indent=2)
            print(f"Saved report to {out_file}")
            return out_file
        except Exception as e:
            print("Warning: Could not parse JSON output; saving raw stdout to .txt")
            txt_file = output_dir / f"{model.replace('/','_')}_{timestamp}.txt"
            with open(txt_file, "w") as f:
                f.write(res.stdout)
            return txt_file
    except subprocess.CalledProcessError as e:
        print("Error running model", model)
        print(e.stdout)
        print(e.stderr)
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--models", required=True, help="Path to file with one model per line")
    p.add_argument("--provider", default="", help="Provider name to pass through to the runner (openai, anthropic, google)")
    p.add_argument("--output-dir", default="data/replication_n15", help="Directory to store raw reports")
    p.add_argument("--live", action="store_true", help="Run with live provider keys instead of dry-run")
    args = p.parse_args()

    models_file = Path(args.models)
    if not models_file.exists():
        print("Models file not found:", models_file)
        sys.exit(2)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    models = [line.strip() for line in models_file.read_text().splitlines() if line.strip() and not line.startswith("#")]
    print(f"Found {len(models)} models to test")

    results = []
    for m in models:
        report = run_model(m, args.provider, output_dir, live=args.live)
        results.append({"model": m, "report": str(report) if report else None})

    summary_file = output_dir / "batch_run_summary.json"
    with open(summary_file, "w") as f:
        json.dump(results, f, indent=2)
    print("Batch run complete. Summary:", summary_file)


if __name__ == '__main__':
    main()
