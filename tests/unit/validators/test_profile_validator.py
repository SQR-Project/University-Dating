import pytest
from fastapi import HTTPException

from app.src.models.profile import CreateProfileRequest
from app.src.validators import profile_validator


def test_validate_success():
    # Arrange
    request = CreateProfileRequest(
        name="Name",
        surname="Sur'Name",
        age=25
    )

    # Act
    response = profile_validator.validate(request)

    # Assert
    assert response is True


def test_validate_invalid_age_too_young():
    # Arrange
    request = CreateProfileRequest(
        name="Name",
        surname="Surname",
        age=10
    )

    # Act
    with pytest.raises(Exception) as exc_info:
        profile_validator.validate(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "Age should be greater than 10" in exc_info.value.detail


def test_validate_invalid_age_too_old():
    # Arrange
    request = CreateProfileRequest(
        name="Name",
        surname="Surname",
        age=101
    )

    # Act
    with pytest.raises(Exception) as exc_info:
        profile_validator.validate(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "less than 100" in exc_info.value.detail


def test_validate_invalid_name():
    # Arrange
    request = CreateProfileRequest(
        name="Name*",
        surname="Surname",
        age=30
    )

    # Act
    with pytest.raises(Exception) as exc_info:
        profile_validator.validate(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "Name and surname should consist of" in exc_info.value.detail


def test_validate_invalid_surname():
    # Arrange
    request = CreateProfileRequest(
        name="Name",
        surname="Surname%",
        age=30
    )

    # Act
    with pytest.raises(Exception) as exc_info:
        profile_validator.validate(request)

    # Assert
    assert type(exc_info.value) is HTTPException
    assert exc_info.value.status_code == 400
    assert "Name and surname should consist of" in exc_info.value.detail
