#!/usr/bin/env python3
"""
Render `docs/press-kit/press-onepager.html` to `docs/press-kit/press-onepager.pdf`.

Requires: WeasyPrint (pip install weasyprint) and system deps (cairo, pango, gdk-pixbuf).

Usage:
  python3 scripts/render_press_pdf.py

This script is included so CI or maintainers can reproducibly generate the press PDF.
"""

import logging
from pathlib import Path

try:
    from weasyprint import HTML
except ImportError:
    raise SystemExit(
        "WeasyPrint is required. Install with `pip install weasyprint` and ensure system libs are available.",
    )

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "docs" / "press-kit" / "press-onepager.html"
OUT = BASE / "docs" / "press-kit" / "press-onepager.pdf"

if not SRC.exists():
    raise SystemExit(f"Source {SRC} not found")

logger.info("Rendering %s → %s", SRC, OUT)
HTML(filename=str(SRC)).write_pdf(str(OUT))
logger.info("Done.")
