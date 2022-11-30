import json
from typing import List

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_project() -> None:
    response = client.post("/project", json={"name": "Test Project"})
    assert response.status_code == 200


def test_get_projects() -> None:
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert len(response.json()) == 1


def test_get_project() -> None:
    _ = client.post("/project", json={"name": "Test Get Project"})
    response = client.get("/projects")

    project_id = json.loads(response.json()[-1])["id"]
    response = client.get(f"/project/{project_id}")

    assert response.status_code == 200
    assert json.loads(response.json())["name"] == "Test Get Project"


def test_patch_project() -> None:
    response = client.get("/projects")

    project_id = json.loads(response.json()[-1])["id"]

    response = client.patch(
        f"/project/{project_id}", json={"name": "Gary Project", "active": "True"}
    )
    assert response.status_code == 200

    response = client.get(f"/project/{project_id}")

    assert json.loads(response.json())["id"] == project_id

    assert response.status_code == 200
    assert json.loads(response.json())["name"] == "Patched Project"


# def test_delete_project() -> None:
#     response = client.delete("/project/2")
#     assert response.status_code == 200


# def test_get_projects() -> None:
#     response = client.get("/projects")
#     assert response.status_code == 200
