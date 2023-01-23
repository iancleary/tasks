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


def test_patch_item_status_backlog() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/backlog")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.BACKLOG


def test_patch_item_status_not_yet_started() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/ready-for-work")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.READY_FOR_WORK


def test_patch_item_status_in_progress() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/in-progress")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.IN_PROGRESS


def test_patch_item_status_completed() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/completed")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.COMPLETED


def test_delete_item() -> None:
    response = client.delete("/item/2")
    assert response.status_code == 200


def test_get_completed_items() -> None:
    response = client.post("/item", json={"name": "Completed Item"})
    response = client.post("/item", json={"name": "Open Item 1"})
    response = client.post("/item", json={"name": "Open Item 2"})
    response = client.get("/items")
    completed_item_id = response.json()[-3]["id"]
    open_item_id = response.json()[-2]["id"]
    open_item_two_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{completed_item_id}/completed")
    response = client.patch(f"/item/{open_item_id}/not-yet-started")
    response = client.patch(f"/item/{open_item_two_id}/in-progress")

    response = client.get("/items/completed")

    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert len(response.json()) == 1
    for item in response.json():
        assert item["status"] == Status.COMPLETED


def test_get_open_items() -> None:
    response = client.get("/items/open")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    for item in response.json():
        assert item["status"] != Status.COMPLETED
