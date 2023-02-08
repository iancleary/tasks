from typing import List

from fastapi.testclient import TestClient

from app.main import app
from app.models.items import Status
from app.models.items import Pinned
from app.models.items import Active
from app.models.items import Order

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


def test_patch_item_pinned_yes() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/pinned/yes")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES


def test_patch_item_pinned_no() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/pinned/no")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")

    assert response.json()["id"] == item_id

    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.NO
    assert response.json()["order_"] == Order.IGNORE

def test_patch_item_order() -> None:
    response = client.get("/items")

    item_id = response.json()[-1]["id"]

    response = client.patch(f"/item/{item_id}/pinned/no")
    assert response.status_code == 200

    response = client.get(f"/item/{item_id}")
    assert response.json()["id"] == item_id

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 409

    response = client.patch(f"/item/{item_id}/pinned/yes")
    assert response.status_code == 200
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.IGNORE

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN + 1

    response = client.patch(f"/item/{item_id}/order/decrease")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN

    # test you bottom out at Order.MIN
    response = client.patch(f"/item/{item_id}/order/decrease")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN

    # Start to go up to max
    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN + 1

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN + 2

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN + 3

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN + 4

    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MIN + 5
    assert response.json()["order_"] == Order.MAX

     # test you top out at Order.MAX
    response = client.patch(f"/item/{item_id}/order/increase")
    assert response.status_code == 200
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["pinned"] == Pinned.YES
    assert response.json()["order_"] == Order.MAX
