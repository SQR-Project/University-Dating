from sqlite3 import IntegrityError
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.src.enums.interests_enum import Interest
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import CreateProfileRequest
from app.src.services import profile_service

VALID_TOKEN_DATA = VerifyAccessTokenResult(
    user_id="1",
    email="email"
)
VALID_CREATE_PROFILE_REQUEST = CreateProfileRequest(
    email="email",
    name="Name",
    surname="Surname",
    age=30
)


@patch('app.src.services.profile_service.Database')
def test_create_profile(mock_db):
    # Arrange
    mock_db.return_value.add_profile.return_value = None
    request = VALID_CREATE_PROFILE_REQUEST

    # Act
    response = profile_service.create_profile(VALID_TOKEN_DATA, request)

    # Assert
    assert isinstance(response, profile_service.SuccessResponse)
    assert response.status == "success"
    mock_db.return_value.add_profile.assert_called_once_with(
        VALID_TOKEN_DATA, request)


@patch('app.src.services.profile_service.Database')
def test_create_profile_db_throws_integrity_error_http_exception(mock_db):
    # Arrange
    request = VALID_CREATE_PROFILE_REQUEST
    mock_db.return_value.add_profile.side_effect = IntegrityError()

    # Act
    with pytest.raises(Exception) as exc_info:
        profile_service.create_profile(VALID_TOKEN_DATA, request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "Profile already exists" == exc_info.value.detail
    mock_db.return_value.add_profile.assert_called_once_with(
        VALID_TOKEN_DATA, request)


@patch('app.src.services.profile_service.Database')
def test_delete_profile(mock_db):
    # Arrange
    mock_db.return_value.delete_profile.return_value = None

    # Act
    response = profile_service.delete_profile(VALID_TOKEN_DATA)

    # Assert
    assert isinstance(response, profile_service.SuccessResponse)
    assert response.status == "success"
    mock_db.return_value.delete_profile.assert_called_once_with(
        VALID_TOKEN_DATA)


@patch('app.src.services.profile_service.Database')
def test_get_all_profiles(mock_db):
    # Arrange
    profiles_data = [
        ("user@innopolis.ru", "Name", "Surname", 25, "aboba", Interest.MUSIC.value),
        ("user@innopolis.university", "Name2",
         "Surname2", 28, "aboba", Interest.SPORT.value)
    ]
    mock_db.return_value.get_all_profiles.return_value = profiles_data

    # Act
    response = profile_service.get_all_profiles()

    # Assert
    assert len(response) == 2
    assert all(isinstance(p, profile_service.ProfileInformation)
               for p in response)

    assert response[0].email == "user@innopolis.ru"
    assert response[0].name == "Name"
    assert response[0].surname == "Surname"
    assert response[0].age == 25
    assert response[0].liked_profiles == "aboba"
    assert response[0].primary_interest.value == Interest.MUSIC.value

    assert response[1].email == "user@innopolis.university"
    assert response[1].name == "Name2"
    assert response[1].surname == "Surname2"
    assert response[1].age == 28
    assert response[1].liked_profiles == "aboba"
    assert response[1].primary_interest.value == Interest.SPORT.value

    mock_db.return_value.get_all_profiles.assert_called_once()
