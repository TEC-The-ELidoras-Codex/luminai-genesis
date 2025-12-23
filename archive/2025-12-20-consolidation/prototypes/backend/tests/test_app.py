from backend.main import app
from fastapi.testclient import TestClient

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
    assert abs(data["effective_resonance"] - 0.72) < 0.001
    assert data["classification"] == "high"


def test_personas():
    resp = client.get("/api/personas")
    assert resp.status_code == 200
    personas = resp.json()
    assert any(p["persona"] == "arcadia" for p in personas)
    assert any(p["persona"] == "airth" for p in personas)


def test_frequencies():
    resp = client.get("/api/frequencies")
    assert resp.status_code == 200
    data = resp.json()
    assert "frequencies" in data
    assert len(data["frequencies"]) == 16


def test_frequency_by_id():
    resp = client.get("/api/frequencies/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Curiosity"


def test_axioms():
    resp = client.get("/api/axioms")
    assert resp.status_code == 200
    data = resp.json()
    assert "axioms" in data
    assert len(data["axioms"]) == 12


def test_witness_protocol_bindings():
    resp = client.get("/api/axioms/witness-protocol/bindings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["binding_count"] > 0
    assert all(a["witness_protocol_binding"] for a in data["axioms"])


def test_codex_classes():
    resp = client.get("/api/codex/classes")
    assert resp.status_code == 200
    data = resp.json()
    assert "classes" in data
    assert "Pacifist" in data["classes"]


def test_codex_abilities():
    resp = client.get("/api/codex/abilities/Pacifist")
    assert resp.status_code == 200
    data = resp.json()
    assert "Pacifist" in data
