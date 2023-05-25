from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_openapi_json_check() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_docs_check() -> None:
    response = client.get("/docs")
    assert response.status_code == 200


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert list(response.json().keys()) == ["status", "details", "env"]
