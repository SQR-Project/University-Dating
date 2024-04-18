import pytest
from fastapi import HTTPException

from app.src.models.profile import CreateProfileRequest
from app.src.validators import profile_validator


@pytest.mark.parametrize("valid_age", [
    11, 26, 100
])
def test_validate_success(valid_age):
    # Arrange
    request = CreateProfileRequest(
        name="Name",
        surname="Sur'Name",
        age=valid_age
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
    assert (("CreateProfileRequest validation error. "
            "Age should be greater than 10 amd less than 100")
            == exc_info.value.detail)


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
    assert (("CreateProfileRequest validation error. "
            "Age should be greater than 10 amd less than 100")
            == exc_info.value.detail)


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
    assert (("CreateProfileRequest validation error. "
            "Name and surname should consist of: letters, -, ., and '")
            == exc_info.value.detail)


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
    assert (("CreateProfileRequest validation error. "
            "Name and surname should consist of: letters, -, ., and '")
            == exc_info.value.detail)
