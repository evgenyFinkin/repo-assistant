from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_repository_rejects_invalid_url() -> None:
    resp = client.post("/api/repositories", json={"url": "not-a-url"})
    assert resp.status_code == 400


def test_create_repository_accepts_valid_url() -> None:
    resp = client.post("/api/repositories", json={"url": "https://github.com/owner/repo"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "pending"
    assert "id" in body
