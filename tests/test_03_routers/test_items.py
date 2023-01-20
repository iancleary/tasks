from typing import List

from fastapi.testclient import TestClient

from app.main import app
from app.models.items import Status

client = TestClient(app)


def test_create_item() -> None:
    response = client.post("/item", json={"name": "Test Item"})
    assert response.status_code == 200


def test_get_items() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert len(response.json()) == 1
    item_name = response.json()[0]["name"]
    assert item_name == "Test Item"


def test_get_item() -> None:
    _ = client.post("/item", json={"name": "Test Get Item"})
    response = client.get("/items")

    item_id = response.json()[1]["id"]
    response = client.get(f"/item/{item_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Test Get Item"


def test_patch_item() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}", json={"name": "Gary Item"})
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["name"] == "Gary Item"


def test_patch_item_status_not_yet_started() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/not-yet-started")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.NOT_YET_STARTED


def test_patch_item_status_in_progress() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/in-progress")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.IN_PROGRESS


def test_patch_item_status_complete() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/complete")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.COMPLETED


def test_delete_item() -> None:
    response = client.delete("/item/2")
    assert response.status_code == 200
