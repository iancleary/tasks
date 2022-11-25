from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_project() -> None:
    response = client.post("/project", json={"name": "Test Project"})
    assert response.status_code == 200


def test_patch_project() -> None:
    response = client.patch(
        "/project/1", json={"name": "Test Project", "active": "True"}
    )
    assert response.status_code == 200
