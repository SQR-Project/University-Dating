from sqlite3 import IntegrityError
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.src.enums.interests_enum import Interest
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.like import LikeProfileRequest
from app.src.services import like_service

VALID_TOKEN_DATA = VerifyAccessTokenResult(
    user_id="1",
    email="email"
)
VALID_LIKE_PROFILE_REQUEST = LikeProfileRequest(
    email="email"
)


@patch('app.src.services.like_service.Database')
def test_like_profile_db_throws_integrity_error_http_exception(mock_db):
    # Arrange
    mock_db.return_value.get_profile_likes_by_user_id.side_effect = IntegrityError()
    # Act
    with pytest.raises(Exception) as exc_info:
        like_service.like_profile(VALID_TOKEN_DATA, VALID_LIKE_PROFILE_REQUEST)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "Profile does not exists" == exc_info.value.detail
    mock_db.return_value.get_profile_likes_by_user_id.assert_called_once_with(VALID_TOKEN_DATA.user_id)


@patch('app.src.services.like_service.Database')
def test_like_profile(mock_db):
    # Arrange
    mock_db.return_value.get_profile_likes_by_user_id.return_value = "Masha"

    # Act
    response = like_service.like_profile(VALID_TOKEN_DATA, VALID_LIKE_PROFILE_REQUEST)

    # Assert
    assert isinstance(response, like_service.SuccessResponse)
    assert response.status == "success"
    mock_db.return_value.get_profile_likes_by_user_id.assert_called_once_with(
        VALID_TOKEN_DATA.user_id)


@patch('app.src.services.like_service.Database')
def test_is_matched(mock_db):
    # Arrange

    mock_db.return_value.unsafe_get_profile_by_email.return_value = [("test_id")]
    mock_db.return_value.get_profile_likes_by_user_id.return_value = [("email")]


    # Act
    response = like_service.is_matched(VALID_TOKEN_DATA, VALID_LIKE_PROFILE_REQUEST)

    # Assert
    assert isinstance(response, like_service.MatchingResponse)

    assert response.matched == True

    mock_db.return_value.unsafe_get_profile_by_email.assert_called_once()
    mock_db.return_value.get_profile_likes_by_user_id.assert_called_once()


@patch('app.src.services.like_service.Database')
def test_is_matched_db_throws_integrity_error_http_exception(mock_db):
    # Arrange

    mock_db.return_value.unsafe_get_profile_by_email.side_effect = IntegrityError()

    # Act
    with pytest.raises(Exception) as exc_info:
        like_service.is_matched(VALID_TOKEN_DATA, VALID_LIKE_PROFILE_REQUEST)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "Profile does not exists" == exc_info.value.detail
    mock_db.return_value.unsafe_get_profile_by_email.assert_called_once()
