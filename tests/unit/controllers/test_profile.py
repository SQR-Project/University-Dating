from unittest.mock import patch, MagicMock

from app.src.controllers import profile
from app.src.enums.interests_enum import Interest
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import ProfileInformation
from app.src.models.response import SuccessResponse


def test_router_data():
    assert profile.profile_router is not None
    assert profile.profile_router.prefix == "/profile"

    assert len(profile.profile_router.tags) == 1
    assert profile.profile_router.tags[0] == "profile"

    assert profile.profile_router.routes[0].path == "/profile/create"
    assert profile.profile_router.routes[1].path == "/profile/"
    assert profile.profile_router.routes[2].path == "/profile/all"


@patch("app.src.controllers.profile.auth_service.verify_access_token")
@patch("app.src.controllers.profile.profile_validator.validate")
@patch("app.src.controllers.profile.profile_service.create_profile")
def test_create_profile(
        mock_create_profile,
        mock_validate,
        mock_verify_access_token
):
    # Arrange
    mock_verify_access_token.return_value = VerifyAccessTokenResult(
        user_id="UserId", email="Email")
    mock_validate.return_value = True
    mock_create_profile.return_value = SuccessResponse()
    request = MagicMock()

    # Act
    response = profile.create_profile(request)

    # Assert
    assert isinstance(response, SuccessResponse)
    assert response.status == "success"


@patch("app.src.controllers.profile.auth_service.verify_access_token")
@patch("app.src.controllers.profile.profile_service.delete_profile")
def test_delete_profile(mock_delete_profile, mock_verify_access_token):
    # Arrange
    mock_verify_access_token.return_value = VerifyAccessTokenResult(
        user_id="UserId", email="Email")
    mock_delete_profile.return_value = SuccessResponse()

    # Act
    response = profile.delete_profile()

    # Assert
    assert isinstance(response, SuccessResponse)
    assert response.status == "success"


@patch("app.src.controllers.profile.auth_service.verify_access_token")
@patch("app.src.controllers.profile.profile_service.get_all_profiles")
def test_get_all_profiles(mock_get_all_profiles, mock_verify_access_token):
    # Arrange
    mock_verify_access_token.return_value = VerifyAccessTokenResult(
        user_id="UserId", email="Email")
    mock_get_all_profiles.return_value = [ProfileInformation(
        email="Email",
        name="Name",
        surname="Surname",
        age=11
    )]

    # Act
    response = profile.get_all_profiles()

    # Assert
    assert len(response) == 1
    assert response[0].name == "Name"
    assert response[0].surname == "Surname"
    assert response[0].email == "Email"
    assert response[0].age == 11
    assert response[0].primary_interest.value == Interest.PROGRAMMING.value
