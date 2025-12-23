import importlib.util
import logging
from pathlib import Path


def load_module():
    path = (Path(__file__).parent.parent / "scripts" / "post_linkedin.py").resolve()
    spec = importlib.util.spec_from_file_location("post_linkedin", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_get_person_urn_and_create(monkeypatch):
    module = load_module()

    class DummyResp:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            return None

    def fake_get(url, *args, **kwargs):
        if not url.endswith("/me"):
            msg = "Unexpected URL: %s" % url
            raise AssertionError(msg)
        return DummyResp({"id": "ABC123"})

    captured_post = {}

    def fake_post(url, *args, **kwargs):
        if not url.endswith("/ugcPosts"):
            msg = "Unexpected URL: %s" % url
            raise AssertionError(msg)
        captured_post["url"] = url
        captured_post["json"] = kwargs.get("json")
        return DummyResp({"result": "ok", "urn": "urn:li:activity:1"})

    monkeypatch.setattr("requests.get", fake_get)
    monkeypatch.setattr("requests.post", fake_post)

    urn = module.get_person_urn("fake-token")
    assert urn == "urn:li:person:ABC123"

    resp = module.create_ugc_post("token", urn, "hello world")
    assert resp["result"] == "ok"
    assert captured_post["json"]["author"] == urn


def test_main_dry_run(caplog, monkeypatch):
    caplog.set_level(logging.INFO)
    module = load_module()

    def fake_get(url, headers=None, timeout=None):
        class Dummy:
            def json(self):
                return {"id": "XYZ"}

            def raise_for_status(self):
                return None

        return Dummy()

    monkeypatch.setattr("requests.get", fake_get)

    ret = module.main(["--access-token", "t", "--text", "hi", "--dry-run"])
    assert ret == 0
    # Ensure logging contains the dry-run message
    assert any("Dry run" in rec.getMessage() for rec in caplog.records)
