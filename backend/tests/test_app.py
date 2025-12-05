from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_ingest_and_fetch_session():
    resp = client.post("/api/ingest", json={"session_id": "s1", "content": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "s1"

    get_resp = client.get("/api/ingest/s1")
    assert get_resp.status_code == 200
    assert get_resp.json()["persona"] == data["persona"]


def test_resonance():
    resp = client.post(
        "/api/resonance",
        json={"session_id": "s1", "structural_resonance": 0.8, "witness": 0.9},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["effective_resonance"] == 0.72
    assert data["classification"] == "high"


def test_personas():
    resp = client.get("/api/personas")
    assert resp.status_code == 200
    personas = resp.json()
    assert any(p["persona"] == "arcadia" for p in personas)
    assert any(p["persona"] == "airth" for p in personas)
