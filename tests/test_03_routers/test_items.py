from typing import List

from fastapi.testclient import TestClient

from app.main import app
from app.models.items import Status
from app.models.items import Active

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

    NAME = "New name for task"
    # Test Description
    DESCRIPTION = "New description for task"
    response = client.patch(
        f"/item/{item_id}", json={"name": NAME, "description": DESCRIPTION}
    )
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["name"] == NAME
    assert response.json()["description"] == DESCRIPTION


def test_patch_item_status_open() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/status/open")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["status"] == Status.OPEN


def test_patch_item_status_completed() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/status/completed")
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
    response = client.post("/item", json={"name": "Open Item"})
    response = client.get("/items")
    completed_item_id = response.json()[-2]["id"]
    open_item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{completed_item_id}/status/completed")
    response = client.patch(f"/item/{open_item_id}/status/open")

    response = client.get("/items/completed")

    assert response.status_code == 200
    assert isinstance(response.json(), List)
    for item in response.json():
        assert item["status"] == Status.COMPLETED


def test_get_deleted_items() -> None:
    response = client.post("/item", json={"name": "Item to be deleted"})
    response = client.post("/item", json={"name": "Another deletion"})
    response = client.get("/items")
    deleted_item_id_1 = response.json()[-2]["id"]
    deleted_item_id_2 = response.json()[-1]["id"]

    response = client.delete(f"/item/{deleted_item_id_1}")
    response = client.delete(f"/item/{deleted_item_id_2}")

    response = client.get("/items/deleted")

    assert response.status_code == 200
    assert isinstance(response.json(), List)
    for item in response.json():
        assert item["active"] == Active.NO


def test_get_open_items() -> None:
    response = client.get("/items/open")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    for item in response.json():
        assert item["status"] != Status.COMPLETED


def test_patch_item_priority_yes() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/priority/yes")
    assert response.status_code == 200


def test_patch_item_priority_no() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/priority/no")
    assert response.status_code == 200

    response = client.get("/items/priority")
    priority_items = response.json()
    assert isinstance(priority_items, List)

    priority_list = [x["id"] for x in priority_items]

    assert item_id not in priority_list


def test_patch_item_order() -> None:
    response = client.get("/items")

    # ensure no items are priority
    for item in response.json():
        item_id = item["id"]
        response = client.patch(f"/item/{item_id}/priority/no")
        assert response.status_code == 200

    response = client.post("/item", json={"name": "Priority Item 1"})
    response = client.get("/items")
    priority_item_1_id = response.json()[-1]["id"]

    # 1
    response = client.patch(f"/item/{priority_item_1_id}/priority/yes")
    assert response.status_code == 200

    response = client.get("/items/priority")
    priority_items = response.json()
    assert isinstance(priority_items, List)
    assert len(priority_items) == 1

    response = client.post("/item", json={"name": "Priority Item 2"})
    response = client.get("/items")
    priority_item_2_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{priority_item_2_id}/priority/yes")
    assert response.status_code == 200

    response = client.get("/items/priority")
    priority_items = response.json()
    assert isinstance(priority_items, List)
    assert len(priority_items) == 2

    priority_list = [x["id"] for x in priority_items]

    assert priority_list == [priority_item_2_id, priority_item_1_id]

    response = client.patch(f"/item/{priority_item_2_id}/priority/decrease")
    assert response.status_code == 200

    response = client.get("/items/priority")
    priority_items = response.json()
    assert isinstance(priority_items, List)
    assert len(priority_items) == 2

    priority_list = [x["id"] for x in priority_items]

    assert priority_list == [priority_item_1_id, priority_item_2_id]

    response = client.patch(f"/item/{priority_item_2_id}/priority/decrease")
    assert response.status_code == 409

    response = client.get("/items/priority")
    priority_items = response.json()
    assert isinstance(priority_items, List)
    assert len(priority_items) == 2

    priority_list = [x["id"] for x in priority_items]

    assert priority_list == [priority_item_1_id, priority_item_2_id]

    response = client.patch(f"/item/{priority_item_1_id}/priority/increase")
    assert response.status_code == 409

    response = client.get("/items/priority")
    priority_items = response.json()
    assert isinstance(priority_items, List)
    assert len(priority_items) == 2

    priority_list = [x["id"] for x in priority_items]

    assert priority_list == [priority_item_1_id, priority_item_2_id]

    response = client.get("/items/priority?limit=1")
    priority_items = response.json()
    assert isinstance(priority_items, List)
    assert len(priority_items) == 1

    priority_list = [x["id"] for x in priority_items]

    assert priority_list == [priority_item_1_id]
