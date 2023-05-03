import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_database_uri() -> None:
    DATABASE_URI = str(os.getenv("DATABASE_URI"))
    assert DATABASE_URI == "sqlite:///data/test.db"


def test_post_new_list() -> None:
    response = client.post(url="/lists/", json={"name": "new_list"})
    assert response.status_code == 200
    assert isinstance(response.json(), int)
    new_list_id = response.json()
    assert isinstance(new_list_id, int)
