import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_database_uri() -> None:
    DATABASE_URI = str(os.getenv("DATABASE_URI"))
    assert DATABASE_URI == "sqlite:///data/test.db"


def test_post_new_list() -> None:
    response = client.post(url="/lists/", json={"name": "placeholder_name"})
    assert response.status_code == 200
    assert isinstance(response.json(), int)
    new_list_id = response.json()
    assert isinstance(new_list_id, int)

    UPDATED_NAME = "updated_name"

    assert new_list_id == 2
    assert f"/lists/{new_list_id}" == "/lists/2"

    response = client.patch(url=f"/lists/{new_list_id}", json={"name": UPDATED_NAME})
    assert response.json() == UPDATED_NAME
    assert response.status_code == 200

    response = client.get(url=f"/lists/{new_list_id}")
    assert response.status_code == 200
    list_name = response.json()["name"]
    assert isinstance(list_name, str)
    assert list_name == UPDATED_NAME
