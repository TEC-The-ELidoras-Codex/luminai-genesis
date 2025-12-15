#!/usr/bin/env python3
"""
Render `docs/press-kit/press-onepager.html` to `docs/press-kit/press-onepager.pdf`.

Requires: WeasyPrint (pip install weasyprint) and system deps (cairo, pango, gdk-pixbuf).

Usage:
  python3 scripts/render_press_pdf.py

This script is included so CI or maintainers can reproducibly generate the press PDF.
"""
from pathlib import Path

try:
    from weasyprint import HTML
except Exception:
    raise SystemExit(
        "WeasyPrint is required. Install with `pip install weasyprint` and ensure system libs are available."
    )

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "docs" / "press-kit" / "press-onepager.html"
OUT = BASE / "docs" / "press-kit" / "press-onepager.pdf"

if not SRC.exists():
    raise SystemExit(f"Source {SRC} not found")

print(f"Rendering {SRC} → {OUT}")
HTML(filename=str(SRC)).write_pdf(str(OUT))
print("Done.")
