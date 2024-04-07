from fastapi.testclient import TestClient

from app.main import app


def test_endpoint_get_ok():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/settings/200")

    assert response.status_code == 200
    assert response.json() is True
