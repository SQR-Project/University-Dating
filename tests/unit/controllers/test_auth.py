import uuid
from unittest.mock import patch, MagicMock

from app.src.controllers import auth


@patch("app.src.controllers.auth.email_validator.validate")
@patch("app.src.controllers.auth.auth_service.register")
def test_register(mock_register, mock_validate):
    # Arrange
    mock_validate.return_value = True
    mock_register.return_value = {"status": "success"}
    request = MagicMock()
    request.email = str(uuid.uuid4())

    # Act
    response = auth.register(request, MagicMock())

    # Assert
    assert response == {"status": "success"}


@patch("app.src.controllers.auth.email_validator.validate")
@patch("app.src.controllers.auth.auth_service.login")
def test_login(mock_login, mock_validate):
    # Arrange
    mock_validate.return_value = True
    mock_login.return_value = {"status": "success"}
    request = MagicMock()
    request.email = str(uuid.uuid4())

    # Act
    response = auth.login(request, MagicMock())

    # Assert
    assert response == {"status": "success"}


@patch("app.src.controllers.auth.auth_service.refresh_auth_tokens")
def test_refresh_tokens(mock_refresh_auth_tokens):
    # Arrange
    mock_refresh_auth_tokens.return_value = {"status": "success"}

    # Act
    response = auth.refresh_tokens(MagicMock(), MagicMock())

    # Assert
    assert response == {"status": "success"}


@patch("app.src.controllers.auth.auth_service.verify_access_token")
@patch("app.src.controllers.auth.auth_service.delete_auth_for_user")
def test_delete_auth_data(
        mock_delete_auth_for_user,
        mock_verify_access_token
):
    # Arrange
    mock_delete_auth_for_user.return_value = {"status": "success"}
    mock_verify_access_token.return_value = {
        "user_id": "UserId",
        "email": "Email"
    }

    # Act
    response = auth.delete_auth_data(MagicMock(), MagicMock())

    # Assert
    assert response == {"status": "success"}
