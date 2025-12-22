#!/usr/bin/env python3
"""Generate a simple SVG heatmap placeholder for TGCR figures without matplotlib.

This creates `figures/tgcr_heatmap.svg` with demo data so the exposé can include a visual immediately.
"""

from pathlib import Path

DEMO = [
    ("ChatGPT", 0.6, 0.1, 0.06),
    ("Claude", 0.45, 0.05, 0.02),
    ("Grok", 0.3, 0.0, 0.0),
    ("Gemini", 0.5, 0.2, 0.1),
]


def color_for_value(v: float) -> str:
    # Map 0..1 to red(0) -> yellow(0.5) -> blue(1.0)
    if v <= 0:
        return "#800000"  # dark red
    if v < 0.5:
        # interpolate red to yellow
        t = v / 0.5
        r = int(128 + t * (255 - 128))
        g = int(0 + t * (255 - 0))
        return f"rgb({r},{g},0)"
    t = (v - 0.5) / 0.5
    # yellow to blue
    r = int(255 - t * 255)
    g = int(255 - t * 255)
    b = int(t * 255)
    return f"rgb({r},{g},{b})"


def make_svg(rows, outpath: Path):
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

    for i, (name, R, W, Rp) in enumerate(rows):
        y = 40 + i * cell_h
        svg.append(
            f'<text x="10" y="{y + cell_h/2}" dominant-baseline="middle">{name}</text>',
        )
        vals = [R, W, Rp]
        for j, v in enumerate(vals):
            x = margin + j * cell_w
            col = color_for_value(v)
            svg.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h -2}" fill="{col}" stroke="#222"/>',
            )
            svg.append(
                f'<text x="{x + cell_w/2}" y="{y + cell_h/2}" text-anchor="middle" dominant-baseline="middle">{v:.2f}</text>',
            )

    svg.append("</svg>")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text("\n".join(svg), encoding="utf-8")
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Saved %s", outpath)


def main():
    outpath = Path("figures") / "tgcr_heatmap.svg"
    make_svg(DEMO, outpath)


if __name__ == "__main__":
    main()
