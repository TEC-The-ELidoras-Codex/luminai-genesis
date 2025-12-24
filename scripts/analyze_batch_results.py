#!/usr/bin/env python3
"""
Aggregate SAR batch results and compute summary statistics

Usage:
  python scripts/analyze_batch_results.py --input-dir data/replication_n15 --output docs/research/n15_results_summary.md

Produces a Markdown summary with means, bootstrap 95% CIs, histogram, and a note on bimodality.
"""

import argparse
from pathlib import Path
import json
import numpy as np
from collections import defaultdict
import statistics


def load_scores_from_report(report_path):
    # Expect JSON report with top-level 'summary' containing 'w_score' or similar
    try:
        data = json.loads(report_path.read_text())
        # heuristics: search for 'w_score' or 'mean_w' keys
        if 'summary' in data and isinstance(data['summary'], dict):
            s = data['summary']
            if 'w_score' in s:
                return float(s['w_score'])
            if 'mean_w' in s:
                return float(s['mean_w'])
        # fallbacks
        if 'w_score' in data:
            return float(data['w_score'])
    except Exception:
        return None
    return None


def bootstrap_ci(data, n_boot=2000, alpha=0.05):
    arr = np.array(data)
    boots = []
    n = len(arr)
    for _ in range(n_boot):
        sample = np.random.choice(arr, size=n, replace=True)
        boots.append(np.mean(sample))
    lo = np.percentile(boots, 100*alpha/2)
    hi = np.percentile(boots, 100*(1-alpha/2))
    return float(lo), float(hi)


def bimodality_coefficient(data):
    # Rough measure: using skewness and kurtosis
    from scipy.stats import skew, kurtosis
    s = skew(data)
    k = kurtosis(data, fisher=False)
    n = len(data)
    if n < 3:
        return None
    bc = (s**2 + 1) / (k + (3*(n-1)**2)/((n-2)*(n-3)))
    return float(bc)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    input_dir = Path(args.input_dir)
    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    reports = list(input_dir.glob("*.json"))
    scores = []
    model_scores = []
    for r in reports:
        s = load_scores_from_report(r)
        if s is not None:
            scores.append(s)
            model_scores.append((r.name, s))

    if not scores:
        print("No scores found in", input_dir)
        return

    mean = float(np.mean(scores))
    med = float(np.median(scores))
    lo, hi = bootstrap_ci(scores)

    # bimodality test (simple heuristic)
    try:
        bc = bimodality_coefficient(scores)
    except Exception:
        bc = None

    # Write markdown summary
    with open(out_file, 'w') as f:
        f.write(f"# N=15 SAR Results Summary\n\n")
        f.write(f"**Models tested:** {len(scores)}\n\n")
        f.write(f"**Mean W-score:** {mean:.3f}  \n\n")
        f.write(f"**Median W-score:** {med:.3f}  \n\n")
        f.write(f"**Bootstrap 95% CI (mean):** [{lo:.3f}, {hi:.3f}]  \n\n")
        if bc is not None:
            f.write(f"**Bimodality coefficient (heuristic):** {bc:.3f}  \n\n")
            f.write(f"(BC > 0.555 suggests bimodality; interpret with caution)\n\n")
        f.write('## Per-model W-scores\n\n')
        for name, s in sorted(model_scores, key=lambda x: x[1], reverse=True):
            f.write(f"- **{name}**: {s:.3f}\n")

    print("Analysis complete. Summary written to", out_file)


if __name__ == '__main__':
    main()
