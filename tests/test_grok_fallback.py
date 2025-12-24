import os
import sys
import tempfile
import json
import requests
import pytest
# Ensure repo root is on sys.path so imports in run_tests.py (which rely on repo-relative imports)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import the local eval helper as the name 'eval' so `from eval import evaluate_response` works
import importlib
_eval_mod = importlib.import_module("benchmarks.dye_die_filter.eval")
import types
sys.modules['eval'] = _eval_mod
from benchmarks.dye_die_filter.run_tests import call_provider_grok, run_grok


def test_grok_dry_run_returns_canned_response(tmp_path, monkeypatch):
    # Create canned response file
    dr_dir = tmp_path / "dry"
    dr_dir.mkdir()
    resp_file = dr_dir / "grok_default_response.txt"
    resp_file.write_text("Hello from canned response", encoding="utf-8")
    monkeypatch.setenv("GROK_DRY_RUN", "1")
    monkeypatch.setenv("DRY_RUN_RESPONSES_DIR", str(dr_dir))
    out = call_provider_grok("Tell me a joke", model="grok-2")
    assert out == "Hello from canned response"


def test_grok_http_fallback_failure_records_error(monkeypatch):
    # Ensure xai and grok imports fail
    monkeypatch.syspath_prepend("")
    monkeypatch.setenv("XAI_API_KEY", "test")

    class FakeResponse:
        status_code = 502

        @property
        def text(self):
            raise RuntimeError("no text")

        def raise_for_status(self):
            raise requests.exceptions.HTTPError("bad gateway")

    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Name resolution failed")

    monkeypatch.setattr("requests.post", fake_post)

    prompts = [{"id": "p1", "prompt": "Hello"}]
    results = run_grok(prompts, model="grok-2")
    assert isinstance(results, list)
    assert len(results) == 1
    r = results[0]
    # On failure, response should be empty string and error should be present
    assert r["response"] == ""
    assert "error" in r
    assert "Name resolution failed" in r["error"]["message"]
