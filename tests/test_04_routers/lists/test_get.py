import os
from typing import List

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_lists() -> None:
    DATABASE_URI = str(os.getenv("DATABASE_URI"))
    assert DATABASE_URI == "sqlite:///data/test.db"
    response = client.get(url="/lists/all")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert len(response.json()) == 1
    item_name = response.json()[0]["name"]
    assert isinstance(item_name, str)
