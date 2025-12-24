"""Generate a small SVG heatmap placeholder for TGCR figures without matplotlib.

This lightweight utility is intended for demos and CI-friendly generation of
small SVG assets. It avoids binary dependencies and keeps behavior explicit via
named thresholds.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

# Thresholds used for color interpolation
YELLOW_THRESHOLD: Final[float] = 0.5
GREEN_THRESHOLD: Final[float] = 0.8

DEMO = [
    ("ChatGPT", 0.6, 0.1, 0.06),
    ("Claude", 0.45, 0.05, 0.02),
    ("Grok", 0.3, 0.0, 0.0),
    ("Gemini", 0.5, 0.2, 0.1),
]


def color_for_value(v: float) -> str:
    """Map a normalized value in [0, 1] to a color hex string.

    Uses named threshold constants to avoid magic numbers in comparisons.
    """
    if v <= 0:
        return "#800000"  # dark red
    if v < YELLOW_THRESHOLD:
        t = v / YELLOW_THRESHOLD
        r = round(128 + (127 * t))
        g = round(0 + (255 * t))
        b = 0
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    if v < GREEN_THRESHOLD:
        t = (v - YELLOW_THRESHOLD) / (GREEN_THRESHOLD - YELLOW_THRESHOLD)
        r = round(255 - (127 * t))
        g = 255
        b = 0
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    # near 1.0
    t = (v - GREEN_THRESHOLD) / (1.0 - GREEN_THRESHOLD)
    r = round(128 - (64 * t))
    g = round(255 - (64 * t))
    b = round(0 + (32 * t))
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def make_svg(rows, outpath: Path) -> None:
    cols = ["R", "W", "R'"]
    cell_w = 120
    cell_h = 32
    margin = 120
    width = margin + len(cols) * cell_w + 20
    height = 40 + len(rows) * cell_h + 20

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
    ]
    svg.append("<style>text{font-family:Arial;font-size:12px}</style>")

    # headers
    for j, col in enumerate(cols):
        x = margin + j * cell_w + cell_w / 2
        svg.append(f'<text x="{x}" y="20" text-anchor="middle">{col}</text>')

    for i, (name, r_val, w_val, rp_val) in enumerate(rows):
        y = 40 + i * cell_h
        y_center_label = y + cell_h / 2
        svg.append(
            f'<text x="10" y="{y_center_label}" dominant-baseline="middle">{name}</text>',
        )
        vals = [r_val, w_val, rp_val]
        for j, v in enumerate(vals):
            x = margin + j * cell_w
            col = color_for_value(v)
            rect = (
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h - 2}" '
                f'fill="{col}" stroke="#222"/>'
            )
            svg.append(rect)
            x_center = x + cell_w / 2
            y_center = y + cell_h / 2
            label = f"{v:.2f}"
            svg.append(
                f'<text x="{x_center}" y="{y_center}" text-anchor="middle" '
                f'dominant-baseline="middle">{label}</text>',
            )

    svg.append("</svg>")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text("\n".join(svg), encoding="utf-8")

    logger = logging.getLogger(__name__)
    logger.info("Saved %s", outpath)


def main() -> None:
    outpath = Path("figures") / "tgcr_heatmap.svg"
    make_svg(DEMO, outpath)


if __name__ == "__main__":
    main()
