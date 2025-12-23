import importlib.util
import os
from datetime import datetime
from pathlib import Path

MODULE_PATH = Path("scripts/convert_markdown_to_pdf.py")


def load_module():
    import sys
    # Insert light-weight stubs for optional dependencies to allow importing module
    if "markdown" not in sys.modules:
        class _md:
            @staticmethod
            def markdown(text, **kwargs):
                return text
        sys.modules["markdown"] = _md()
    if "weasyprint" not in sys.modules:
        class _CSS:
            def __init__(self, *args, **kwargs):
                pass
        class _HTML:
            def __init__(self, *args, **kwargs):
                pass
            def write_pdf(self, *args, **kwargs):
                return None
        weasy = type("weasy", (), {"CSS": _CSS, "HTML": _HTML})
        sys.modules["weasyprint"] = weasy

    spec = importlib.util.spec_from_file_location("convert_md", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_frontmatter_date():
    mod = load_module()
    md = """---
date: 2025-12-20
---
Hello"""
    dt = mod.extract_date_from_markdown(md, MODULE_PATH)
    assert dt is not None
    assert dt.date() == datetime(2025, 12, 20, tzinfo=mod.UTC).date()


def test_iso_date():
    mod = load_module()
    md = "Release on 2025-12-20"
    dt = mod.extract_date_from_markdown(md, MODULE_PATH)
    assert dt is not None
    assert dt.date() == datetime(2025, 12, 20, tzinfo=mod.UTC).date()


def test_numeric_date():
    mod = load_module()
    md = "Next chapter 12/20/2025"
    dt = mod.extract_date_from_markdown(md, MODULE_PATH)
    assert dt is not None
    assert dt.date() == datetime(2025, 12, 20, tzinfo=mod.UTC).date()


def test_written_date():
    mod = load_module()
    md = "Published November 12th, 2347"
    dt = mod.extract_date_from_markdown(md, MODULE_PATH)
    assert dt is not None
    assert dt.date() == datetime(2347, 11, 12, tzinfo=mod.UTC).date()


def test_mtime_fallback(tmp_path):
    mod = load_module()
    p = tmp_path / "sample.md"
    p.write_text("No dates here", encoding="utf-8")
    # set mtime to a known timestamp
    ts = 1609459200  # 2021-01-01 00:00:00 UTC
    os.utime(p, (ts, ts))
    dt = mod.extract_date_from_markdown("", p)
    assert dt is not None
    assert int(dt.timestamp()) == ts
