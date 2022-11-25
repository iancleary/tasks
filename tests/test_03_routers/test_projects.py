from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# def test_add_project() -> None:
#     response = client.put("/project", json={"name": "Test Project"})
#     assert response.status_code == 200
