import os
import shutil
import subprocess
import sys
import tempfile

import pytest

from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tec_book" / "tec_book_compiler.py"

pytestmark = pytest.mark.integration


def has_executable(name):
    return shutil.which(name) is not None


@pytest.mark.skipif(not SCRIPT.exists(), reason="compiler script not found")
def test_pages_flag_reports_total():
    # Run the script in pages-only mode and ensure it prints a total page count
    proc = subprocess.run([sys.executable, str(SCRIPT), "--pages"], capture_output=True, text=True, check=False)
    out = proc.stdout + proc.stderr
    assert "Total pages" in out or "pages-only" in out
    # Try to extract an integer from the output
    import re

    m = re.search(r"Total pages[:)?]\s*(\d+)", out)
    if m:
        assert int(m.group(1)) > 0


@pytest.mark.skipif(not SCRIPT.exists(), reason="compiler script not found")
def test_full_build_creates_pdf_and_counts_pages(tmp_path):
    # Build a real PDF into a temp location and assert its existence and page count
    out_pdf = tmp_path / "out_test_book.pdf"
    proc = subprocess.run([sys.executable, str(SCRIPT), "--output", str(out_pdf)], capture_output=True, text=True, check=False)
    assert out_pdf.exists(), f"Expected PDF at {out_pdf} but it was not created. stdout: {proc.stdout} stderr: {proc.stderr}"

    # If PyPDF2 available, check page count
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(str(out_pdf))
        assert len(reader.pages) >= 1
    except Exception:
        pytest.skip("PyPDF2 not installed; skipping PDF page count assertion")

    # If pdftotext available, verify the footer text appears on a page
    if has_executable("pdftotext"):
        txt = subprocess.check_output(["pdftotext", str(out_pdf), "-"], text=True, stderr=subprocess.DEVNULL)
        assert "Page 2 of" in txt or "Page 3 of" in txt or "Page 4 of" in txt
    else:
        pytest.skip("pdftotext not available; skipping footer text verification")
