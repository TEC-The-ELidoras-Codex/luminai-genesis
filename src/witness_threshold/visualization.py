"""Visualization utilities for Witness Threshold pilot data.

Creates:
 - Bimodal distribution histogram of W-scores
 - Convergence correlation scatter plot vs. external benchmarks

Usage:
  python -m src.witness_threshold.visualization --input data/witness-threshold/pilot_study_n7.json --outdir data/witness-threshold/plots
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import gaussian_kde
except Exception:
    np = None  # type: ignore


def load_w_scores(path: Path) -> List[float]:
    if not path.exists():
        raise FileNotFoundError(f"Pilot data not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    # Expecting either {"w_scores": [...]} or results list of objects with "score" or a top-level w_score.mean_normalized
    if isinstance(data, dict):
        if "w_scores" in data:
            return list(map(float, data["w_scores"]))
        if "results" in data:
            return [float(r.get("score", 0)) for r in data["results"]]
        if "w_score" in data and "mean_normalized" in data["w_score"]:
            return [float(data["w_score"]["mean_normalized"])]
    if isinstance(data, list):
        return [float(x) for x in data]
    raise ValueError("Unrecognized pilot data format. Expected dict with 'results' or list of scores.")


def plot_bimodal(w_scores: List[float], out_path: Path, bins: int = 10) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if np is None:
        raise RuntimeError("numpy/matplotlib/scipy required for plotting. Install requirements first.")

    arr = np.array(w_scores)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(arr, bins=bins, color="#4c72b0", alpha=0.7, edgecolor="black")
    try:
        kde = gaussian_kde(arr)
        xs = np.linspace(0, 1, 200)
        ys = kde(xs)
        ax2 = ax.twinx()
        ax2.plot(xs, ys, color="#dd8452", lw=1.5)
        ax2.set_ylabel("Density")
    except Exception:
        pass
    ax.set_xlabel("W-score (normalized)")
    ax.set_ylabel("Count")
    ax.set_title("Bimodal Distribution of W-scores")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_convergence(w_scores: List[float], benchmarks: Dict[str, float], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if np is None:
        raise RuntimeError("numpy/matplotlib/scipy required for plotting. Install requirements first.")

    arr = np.array(w_scores)
    indices = np.arange(len(arr)) + 1
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(indices, arr, color="#2ca02c")
    for label, value in benchmarks.items():
        ax.hlines(value, xmin=1, xmax=len(arr), linestyles="--", label=f"{label}: {value:.2f}")
    ax.set_xlabel("Study Item")
    ax.set_ylabel("W-score (normalized)")
    ax.set_title("W-scores vs. Benchmarks")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main(argv: List[str] | None = None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", type=Path, default=Path("data/witness-threshold/pilot_study_n7.json"))
    p.add_argument("--outdir", "-o", type=Path, default=Path("data/witness-threshold/plots"))
    p.add_argument("--benchmarks", "-b", type=str, default="Anthropic:0.20", help="Comma-separated label:value pairs")
    args = p.parse_args(argv)

    w_scores = load_w_scores(args.input)
    outdir = args.outdir
    bimodal_path = outdir / "bimodal_w_scores.png"
    convergence_path = outdir / "convergence_vs_benchmarks.png"

    plot_bimodal(w_scores, bimodal_path)

    # parse benchmarks
    bench_pairs = [s.strip() for s in args.benchmarks.split(",") if s.strip()]
    benches = {}
    for bp in bench_pairs:
        if ":" in bp:
            label, val = bp.split(":", 1)
            try:
                benches[label.strip()] = float(val)
            except ValueError:
                continue
    plot_convergence(w_scores, benches, convergence_path)
    print(f"Saved plots to {outdir}")


if __name__ == "__main__":
    main()
