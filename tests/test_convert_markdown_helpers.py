import importlib
import sys
from datetime import UTC, datetime
from pathlib import Path


def load_module():
    # Insert minimal stubs for optional third-party deps so module can import
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

    return importlib.import_module("scripts.convert_markdown_to_pdf")


def test_build_full_html_contains_title_and_body():
    conv = load_module()
    title = "My Post"
    date_html = '<p class="date">Published: May 1, 2025</p>'
    body = "<p>Hello world</p>"

    html = conv.build_full_html(title, date_html, body)
    assert "<title>My Post</title>" in html
    assert date_html in html
    assert body in html


def test_format_pub_date_html_with_and_without_date():
    conv = load_module()
    dt = datetime(2025, 5, 1, tzinfo=UTC)
    html = conv.format_pub_date_html(dt)
    assert "Published: May 01, 2025" in html or "Published: May 1, 2025" in html

    html_none = conv.format_pub_date_html(None)
    assert html_none == ""


def test_render_pdf_uses_weasy(monkeypatch, tmp_path: Path):
    conv = load_module()
    captured = {}

    class FakeHTML:
        def __init__(self, string: str):
            captured["html"] = string

        def write_pdf(self, out_path, stylesheets=None):
            captured["out_path"] = Path(out_path)
            captured["stylesheets"] = stylesheets
            # Create a dummy file so callers can stat it
            Path(out_path).write_bytes(b"PDF")

    monkeypatch.setattr(conv, "HTML", FakeHTML)

    css = conv.build_css()
    html = conv.build_full_html("T", "", "<p>x</p>")
    out = tmp_path / "out.pdf"

    conv.render_pdf(html, css, out)

    assert captured["out_path"] == out
    assert captured["stylesheets"] == [css]
    assert out.exists()
