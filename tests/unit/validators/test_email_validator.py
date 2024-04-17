from re import Pattern

import pytest
from fastapi import HTTPException

from app.src.validators import email_validator


def test_correct_pattern_type():
    assert type(email_validator.EMAIL_PATTERN_STR) is str
    assert len(email_validator.EMAIL_PATTERN_STR) > 2
    assert type(email_validator.EMAIL_PATTERN) is Pattern


@pytest.mark.parametrize("valid_email", [
    "example@innopolis.university",
    "test.user@innopolis.ru",
    "another-test@innopolis.university"
])
def test_validate_valid_emails(valid_email):
    assert email_validator.validate(valid_email) is True


@pytest.mark.parametrize("invalid_email", [
    "example@innopolis.com",
    "test.user@gmail.com",
    "plainaddress",
    "@innopolis.university",
    "test@innopolis.university.com",
    "test@innopolis.school"
])
def test_validate_invalid_emails(invalid_email):
    with pytest.raises(HTTPException) as exc_info:
        email_validator.validate(invalid_email)
    assert exc_info.value.status_code == 400
    assert "Email validation error" in str(exc_info.value.detail)
