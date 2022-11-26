import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_project() -> None:
    response = client.post("/project", json={"name": "Test Project"})
    assert response.status_code == 200
    assert isinstance(response.json(), str) == True
    assert json.loads(response.json()) == {"id": 2}


def test_get_project() -> None:
    response = client.get("/project/2")
    assert response.status_code == 200
    assert isinstance(response.json(), str) == True
    assert json.loads(response.json()) == {"id": 2, "name": "Test Project", "active": 1}


def test_patch_project() -> None:
    response = client.patch(
        "/project/2", json={"name": "Test Project", "active": "True"}
    )
    assert response.status_code == 200


def test_delete_project() -> None:
    response = client.delete("/project/2")
    assert response.status_code == 200


def test_get_projects() -> None:
    response = client.get("/projects")
    assert response.status_code == 200
