import uuid
from unittest.mock import patch, MagicMock

import pytest
from fastapi import HTTPException, Response

from app.src.models.auth import AuthWithEmailRequest
from app.src.services import auth_service

VALID_ACCESS_TOKEN = str(uuid.uuid4())
VALID_REFRESH_TOKEN = str(uuid.uuid4())
VALID_EMAIL = "valid@innopolis.university"
VALID_USER_ID = str(uuid.uuid4())


@pytest.fixture
def valid_email_auth_data_response():
    return {
        "idToken": VALID_ACCESS_TOKEN,
        "refreshToken": VALID_REFRESH_TOKEN,
        "email": VALID_EMAIL,
        "localId": VALID_USER_ID
    }


@patch("app.src.services.auth_service.requests.post")
def test_email_auth_call_response_error(mock_post):
    # Arrange
    error_message = str(uuid.uuid4())
    mock_post.return_value.json.return_value = {
        "error": {
            "message": error_message
        }
    }

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.email_auth_call(
            AuthWithEmailRequest(
                email=VALID_EMAIL,
                password=str(uuid.uuid4())
            ),
            "subPath")

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 401
    assert "error" == exc_info.value.detail["status"]
    assert error_message == exc_info.value.detail["message"]


@patch("app.src.services.auth_service.requests.post")
def test_email_auth_call_no_access_token_in_response(mock_post):
    # Arrange
    mock_post.return_value.json.return_value = {
        "email": VALID_EMAIL
    }

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.email_auth_call(
            AuthWithEmailRequest(
                email=VALID_EMAIL,
                password=str(uuid.uuid4())
            ),
            "subPath")

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 404
    assert "error" == exc_info.value.detail["status"]
    assert "Token not found in response" == exc_info.value.detail["message"]


@patch("app.src.services.auth_service.requests.post")
def test_email_auth_call_success(
        mock_post,
        valid_email_auth_data_response
):
    # Arrange
    mock_post.return_value.json.return_value =\
        valid_email_auth_data_response

    # Act
    response = auth_service.email_auth_call(
        AuthWithEmailRequest(
            email=VALID_EMAIL,
            password=str(uuid.uuid4())
        ),
        "subPath"
    )

    # Assert
    assert response.json() is not None
    assert type(response.json()) == dict


def test_set_httponly_cookie():
    # Arrange
    response = Response()

    # Act
    auth_service.set_httponly_cookie(
        VALID_ACCESS_TOKEN,
        VALID_REFRESH_TOKEN,
        response
    )

    # Assert
    assert str(response.raw_headers).count("set-cookie") == 2
    assert str(response.raw_headers).count("HttpOnly") == 2


def test_get_token_from_cookie_success():
    # Arrange
    request = MagicMock()
    request.cookies.get.return_value = f"Bearer {VALID_ACCESS_TOKEN}"

    # Act
    result = auth_service.get_token_from_cookie(request)

    # Assert
    assert result == VALID_ACCESS_TOKEN


def test_get_token_from_cookie_no_token_in_cookie():
    # Arrange
    request = MagicMock()
    request.cookies.get.return_value = None

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.get_token_from_cookie(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 401
    assert "Authorization token missing" == exc_info.value.detail


def test_get_token_from_cookie_invalid_token_format_in_cookie():
    # Arrange
    request = MagicMock()
    request.cookies.get.return_value = VALID_ACCESS_TOKEN

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.get_token_from_cookie(request)

    # Assert
    assert type(exc_info.value) is IndexError


@patch("app.src.services.auth_service.id_token")
@patch("app.src.services.auth_service.get_token_from_cookie")
def test_verify_access_token_token_verification_error(
        mock_get_token_from_cookie,
        mock_id_token
):
    # Arrange
    request = MagicMock()
    mock_get_token_from_cookie.return_value = f"Bearer {VALID_ACCESS_TOKEN}"
    mock_id_token.verify_firebase_token.side_effect = ValueError()

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.verify_access_token(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 401
    assert "Invalid ID token" == exc_info.value.detail
    mock_get_token_from_cookie.assert_called_once_with(request)


@patch("app.src.services.auth_service.id_token")
@patch("app.src.services.auth_service.get_token_from_cookie")
def test_verify_access_token_success(mock_get_token_from_cookie, mock_id_token):
    # Arrange
    request = MagicMock()
    mock_get_token_from_cookie.return_value = f"Bearer {VALID_ACCESS_TOKEN}"
    mock_id_token.verify_firebase_token.return_value = {
        "user_id": VALID_USER_ID,
        "email": VALID_EMAIL
    }

    # Act
    result = auth_service.verify_access_token(request)

    # Assert
    assert result is not None
    assert type(result) is auth_service.VerifyAccessTokenResult
    assert result.user_id == VALID_USER_ID
    assert result.email == VALID_EMAIL
    mock_get_token_from_cookie.assert_called_once_with(request)


def test_get_refresh_token_no_token_in_cookie():
    # Arrange
    request = MagicMock()
    request.cookies.get.return_value = None

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.get_refresh_token(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 401
    assert "Refresh token missing" == exc_info.value.detail


def test_get_refresh_token_success():
    # Arrange
    request = MagicMock()
    request.cookies.get.return_value = VALID_REFRESH_TOKEN

    # Act
    result = auth_service.get_refresh_token(request)

    # Assert
    assert result == VALID_REFRESH_TOKEN


@patch("app.src.services.auth_service.get_refresh_token")
@patch("app.src.services.auth_service.requests.post")
def test_refresh_auth_tokens_response_error(mock_post, mock_get_refresh_token):
    # Arrange
    mock_get_refresh_token.return_value = VALID_REFRESH_TOKEN
    error_message = str(uuid.uuid4())
    mock_post.return_value.json.return_value = {
        "error": {
            "message": error_message
        }
    }
    request = MagicMock()

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.refresh_auth_tokens(request, MagicMock())

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 401
    assert "error" == exc_info.value.detail["status"]
    assert error_message == exc_info.value.detail["message"]
    mock_get_refresh_token.assert_called_once_with(request)


@patch("app.src.services.auth_service.get_refresh_token")
@patch("app.src.services.auth_service.requests.post")
def test_refresh_auth_tokens_success(mock_post, mock_get_refresh_token):
    # Arrange
    mock_get_refresh_token.return_value = VALID_REFRESH_TOKEN
    new_refresh_token = str(uuid.uuid4())
    mock_post.return_value.json.return_value = {
        "id_token": VALID_ACCESS_TOKEN,
        "refresh_token": new_refresh_token
    }
    request = MagicMock()

    # Act
    result = auth_service.refresh_auth_tokens(request, MagicMock())

    # Assert
    assert isinstance(result, auth_service.SuccessResponse)
    assert result.status == "success"
    mock_get_refresh_token.assert_called_once_with(request)


@patch("app.src.services.auth_service.verify_access_token")
@patch("app.src.services.auth_service.get_token_from_cookie")
@patch("app.src.services.auth_service.requests.post")
def test_delete_auth_for_user_response_error(
        mock_post,
        mock_get_token_from_cookie,
        mock_verify_access_token
):
    # Arrange
    mock_verify_access_token.return_value = {
        "user_id": VALID_USER_ID,
        "email": VALID_EMAIL
    }
    mock_get_token_from_cookie.return_value = f"Bearer {VALID_ACCESS_TOKEN}"
    error_message = str(uuid.uuid4())
    mock_post.return_value.json.return_value = {
        "error": {
            "message": error_message
        }
    }
    request = MagicMock()

    # Act
    with pytest.raises(Exception) as exc_info:
        auth_service.delete_auth_for_user(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 401
    assert "error" == exc_info.value.detail["status"]
    assert error_message == exc_info.value.detail["message"]
    mock_verify_access_token.assert_called_once_with(request)
    mock_get_token_from_cookie.assert_called_once_with(request)


@patch("app.src.services.auth_service.verify_access_token")
@patch("app.src.services.auth_service.get_token_from_cookie")
@patch("app.src.services.auth_service.requests.post")
def test_delete_auth_for_user_success(
        mock_post,
        mock_get_token_from_cookie,
        mock_verify_access_token
):
    # Arrange
    mock_verify_access_token.return_value = {
        "user_id": VALID_USER_ID,
        "email": VALID_EMAIL
    }
    mock_get_token_from_cookie.return_value = f"Bearer {VALID_ACCESS_TOKEN}"
    mock_post.return_value.json.return_value = {
        "success": True
    }
    request = MagicMock()

    # Act
    result = auth_service.delete_auth_for_user(request)

    # Assert
    assert isinstance(result, auth_service.SuccessResponse)
    assert result.status == "success"
    mock_verify_access_token.assert_called_once_with(request)
    mock_get_token_from_cookie.assert_called_once_with(request)


@patch("app.src.services.auth_service.email_auth_call")
def test_register(
        mock_email_auth_call,
        valid_email_auth_data_response
):
    # Arrange
    auth_service.set_httponly_cookie = MagicMock()
    mock_email_auth_call.return_value.json.return_value = \
        valid_email_auth_data_response

    # Act
    result = auth_service.register(
        AuthWithEmailRequest(
            email=VALID_EMAIL,
            password=str(uuid.uuid4())
        ),
        MagicMock()
    )

    # Assert
    assert isinstance(result, auth_service.SuccessResponse)
    assert result.status == "success"
    mock_email_auth_call.return_value.json.assert_called_once()


@patch("app.src.services.auth_service.email_auth_call")
def test_login(
        mock_email_auth_call,
        valid_email_auth_data_response
):
    # Arrange
    auth_service.set_httponly_cookie = MagicMock()
    mock_email_auth_call.return_value.json.return_value = \
        valid_email_auth_data_response

    # Act
    result = auth_service.login(
        AuthWithEmailRequest(
            email=VALID_EMAIL,
            password=str(uuid.uuid4())
        ),
        MagicMock()
    )

    # Assert
    assert isinstance(result, auth_service.SuccessResponse)
    assert result.status == "success"
    mock_email_auth_call.return_value.json.assert_called_once()
