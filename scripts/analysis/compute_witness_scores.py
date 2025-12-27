"""Compute Witness Factor (W) from SAR scores in the CSV and print a summary."""

import csv
import logging
from pathlib import Path
from statistics import mean

logger = logging.getLogger(__name__)

IN = "docs/research/witness_data/reddit_megathread_cases.csv"
OUT = "docs/research/witness_data/summary.txt"


def sar_to_w(sar):
    # SAR score range assumed [-3, +6]; map to W in [0,1]
    return (sar + 3) / 9


def main(in_path: str = IN, out_path: str = OUT):
    rows = []
    with Path(in_path).open(newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # allow empty sar_score (skipped rows)
            try:
                r["sar_score"] = int(
                    r.get("sar_score", 0) if r.get("sar_score", "") != "" else 0,
                )
            except (ValueError, TypeError) as exc:
                logger.debug(
                    "Failed to parse sar_score '%s': %s",
                    r.get("sar_score"),
                    exc,
                    exc_info=exc,
                )
                r["sar_score"] = 0
            r["W"] = sar_to_w(r["sar_score"])
            rows.append(r)

    ws = [r["W"] for r in rows]
    avg = mean(ws) if ws else 0
    summary_lines = []
    summary_lines.append(f"Cases analyzed: {len(ws)}")
    summary_lines.append(f"Average W: {avg:.3f}")
    summary_lines.append("W distribution:")
    summary_lines.extend(
        [
            (
                f"{r.get('date', '')},{r.get('anon_user', '')},"
                f"{r.get('model_reported', '')},{r.get('failure_type', '')},"
                f"SAR={r.get('sar_score', '')},W={r['W']:.3f}"
            )
            for r in rows
        ],
    )

    with Path(out_path).open("w", newline="") as f:
        f.write("\n".join(summary_lines))

    logger.info("\n".join(summary_lines))


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", default=IN, help="Input CSV path")
    p.add_argument("--out", dest="out_path", default=OUT, help="Output summary path")
    args = p.parse_args()
    main(in_path=args.in_path, out_path=args.out_path)
