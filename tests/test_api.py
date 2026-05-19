from fastapi.testclient import TestClient

from saas.api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True
    assert "service" in body


def test_benchmark_moire():
    r = client.get("/benchmark/moire")
    assert r.status_code == 200
    data = r.json()
    assert "modes" in data
    assert "physics_target" in data["modes"]
    assert "conservative" in data["modes"]
    assert "Medium (16 tiles)" in data["modes"]["physics_target"]["configs"]


def test_physics_sweep():
    r = client.post(
        "/physics/sweep",
        json={"twist_start": 1.0, "twist_end": 1.2, "points": 5},
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("count") == 5
    assert len(data.get("samples", [])) == 5
