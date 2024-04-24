from unittest.mock import patch

from app.src.controllers import status


def test_router_data():
    assert status.status_router is not None
    assert status.status_router.prefix == "/status"

    assert len(status.status_router.tags) == 1
    assert status.status_router.tags[0] == "status"

    assert status.status_router.routes[0].path == "/status/healthz"


@patch("app.src.controllers.status.Database")
def test_register(mock_db):
    # Arrange
    mock_db.return_value.check.return_value = True

    # Act
    response = status.check_app_health()

    # Assert
    assert response is True
