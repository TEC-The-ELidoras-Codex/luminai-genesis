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


def run_model(model, provider, output_dir, live=False, compare_tec=False, self_rate=False):
    # Build output file path
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    base_name = f"{provider or 'dry'}_{model.replace('/','_')}_{timestamp}"
    out_file = output_dir / f"{base_name}.json"

    # Build command
    cmd = [sys.executable, "benchmarks/dye_die_filter/run_tests.py", "--model", model, "--output", str(out_file)]
    if provider:
        cmd += ["--provider", provider]
    if not live:
        cmd += ["--dry-run"]
    if compare_tec:
        cmd += ["--compare-tec"]
    if self_rate:
        cmd += ["--self-rate"]

    print("Running:", " ".join(cmd))
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # run_tests.py writes JSON to the --output path (and _tec/_baseline when --compare-tec)
        # If compare_tec, the runner writes two files; standardize return of baseline and tec file paths
        if compare_tec:
            out_base = str(out_file).replace('.json', '_baseline.json')
            out_tec = str(out_file).replace('.json', '_tec.json')
            print(f"Saved baseline to {out_base} and TEC to {out_tec}")
            return out_base, out_tec
        else:
            print(f"Saved report to {out_file}")
            return str(out_file)
    except subprocess.CalledProcessError as e:
        print("Error running model", model)
        print(e.stdout)
        print(e.stderr)
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--models", required=True, help="Path to file with one model per line")
    p.add_argument("--provider", default="", help="Provider name to pass through to the runner (openai, anthropic, grok)")
    p.add_argument("--output-dir", default="data/replication_n15", help="Directory to store raw reports")
    p.add_argument("--live", action="store_true", help="Run with live provider keys instead of dry-run")
    p.add_argument("--compare-tec", action="store_true", help="Run baseline and TEC versions and save both reports")
    p.add_argument("--self-rate", action="store_true", help="Run SAR self-rating on model responses")
    args = p.parse_args()

    models_file = Path(args.models)
    if not models_file.exists():
        print("Models file not found:", models_file)
        sys.exit(2)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = [line.strip() for line in models_file.read_text().splitlines() if line.strip() and not line.startswith("#")]
    models = []
    for line in lines:
        # parse provider:model or model
        if ":" in line:
            provider, model = line.split(":", 1)
            provider = provider.strip()
            model = model.strip()
        else:
            provider = None
            model = line
        models.append((provider, model))

    print(f"Found {len(models)} models to test")

    results = []
    for provider, model in models:
        out = run_model(model, provider, output_dir, live=args.live, compare_tec=args.compare_tec, self_rate=args.self_rate)
        results.append({"provider": provider, "model": model, "report": out})

    summary_file = output_dir / "batch_run_summary.json"
    with open(summary_file, "w") as f:
        json.dump(results, f, indent=2)
    print("Batch run complete. Summary:", summary_file)


if __name__ == '__main__':
    main()
