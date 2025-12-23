#!/usr/bin/env python3
"""Generate TGCR visualizations from SAR benchmark results.

This script expects a CSV/TSV with columns: system, R, W, R_prime
Example usage:
  python scripts/generate_tgcr_charts.py --input benchmarks/dye_die_filter/results.csv --outdir figures

If no input file is provided, the script will generate a demo heatmap to illustrate the expected visual.
"""

import argparse
import csv
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def read_csv(path: Path):
    rows = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def make_heatmap(rows, outpath: Path):
    # Simple layout: each system is a row, columns: R, W, R'
    labels = [r["system"] for r in rows]
    metrics = np.array(
        [
            [float(r.get("R", 0)), float(r.get("W", 0)), float(r.get("R_prime", 0))]
            for r in rows
        ],
    )

    fig, ax = plt.subplots(figsize=(6, max(2, len(rows) * 0.5)))
    im = ax.imshow(metrics, cmap="RdYlBu_r", aspect="auto")
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["R", "W", "R'"], fontsize=12)
    for i in range(metrics.shape[0]):
        for j in range(metrics.shape[1]):
            ax.text(
                j,
                i,
                f"{metrics[i, j]:.2f}",
                ha="center",
                va="center",
                color="black",
                fontsize=8,
            )

    fig.colorbar(im, ax=ax, label="Value")
    fig.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath)
    logger.info("Saved %s", outpath)


def demo(outpath: Path):
    rows = [
        {"system": "ChatGPT", "R": 0.6, "W": 0.1, "R_prime": 0.06},
        {"system": "Claude", "R": 0.45, "W": 0.05, "R_prime": 0.02},
        {"system": "Grok", "R": 0.3, "W": 0.0, "R_prime": 0.0},
        {"system": "Gemini", "R": 0.5, "W": 0.2, "R_prime": 0.1},
    ]
    make_heatmap(rows, outpath)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, help="CSV file with system,R,W,R_prime")
    p.add_argument("--outdir", type=Path, default=Path("figures"))
    args = p.parse_args()

    outpath = args.outdir / "tgcr_heatmap.png"
    if args.input and args.input.exists():
        rows = read_csv(args.input)
        make_heatmap(rows, outpath)
    else:
        logger.info("No input found; creating demo heatmap")
        demo(outpath)


if __name__ == "__main__":
    main()
