import os
from sqlite3 import IntegrityError

import pytest

from app.src.dal import database
from app.src.enums.interests_enum import Interest
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import CreateProfileRequest


@pytest.fixture
def db_fixture():
    os.environ["DB_PATH"] = ":memory:"
    db = database.Database()
    conn = db.conn
    yield db, conn
    conn.close()


def test_check(db_fixture):
    # Arrange
    db, conn = db_fixture

    # Act
    result = db.check()

    # Assert
    assert result is True


def test_add_profile(db_fixture):
    # Arrange
    db, conn = db_fixture
    token_data = VerifyAccessTokenResult(
        user_id="1",
        email="user@innopolis.university"
    )
    request = CreateProfileRequest(
        name="Name",
        surname="Surname",
        age=100,
        primary_interest=Interest.MUSIC.value
    )

    # Act
    db.add_profile(token_data, request)
    profiles = db.get_all_profiles()

    # Assert
    assert len(profiles) == 1

    (email, name, surname, age, primary_interest) = profiles[0]
    assert email == "user@innopolis.university"
    assert name == "Name"
    assert surname == "Surname"
    assert age == 100
    assert primary_interest == Interest.MUSIC.value


def test_add_profile_existing_account_raise_integrity_error(db_fixture):
    # Arrange
    db, conn = db_fixture
    token_data = VerifyAccessTokenResult(
        user_id="1",
        email="user@innopolis.university"
    )
    request = CreateProfileRequest(
        name="Name",
        surname="Surname",
        age=37,
        primary_interest=Interest.MUSIC.value
    )
    db.add_profile(token_data, request)

    # Act
    with pytest.raises(Exception) as exc_info:
        db.add_profile(token_data, request)

    # Assert
    assert type(exc_info.value) is IntegrityError


def test_delete_profile(db_fixture):
    # Arrange
    db, conn = db_fixture
    token_data = VerifyAccessTokenResult(
        user_id="1",
        email="user@innopolis.university"
    )
    request = CreateProfileRequest(
        name="Name",
        surname="Surname",
        age=55,
        primary_interest=Interest.MUSIC.value
    )
    db.add_profile(token_data, request)

    # Act
    db.delete_profile(token_data)
    profiles = db.get_all_profiles()

    # Assert
    assert len(profiles) == 0


def test_get_all_profiles(db_fixture):
    # Arrange
    db, conn = db_fixture
    token_data_1 = VerifyAccessTokenResult(
        user_id="1",
        email="user@innopolis.university"
    )
    request_1 = CreateProfileRequest(
        name="Name",
        surname="Surname",
        age=67,
        primary_interest=Interest.MUSIC.value
    )
    db.add_profile(token_data_1, request_1)

    token_data_2 = VerifyAccessTokenResult(
        user_id="2",
        email="user@innopolis.ru"
    )
    request_2 = CreateProfileRequest(
        name="Name2",
        surname="Surname2",
        age=45
    )
    db.add_profile(token_data_2, request_2)

    # Act
    profiles = db.get_all_profiles()

    # Assert
    assert len(profiles) == 2

    (email, name, surname, age, primary_interest) = profiles[0]
    assert email == "user@innopolis.university"
    assert name == "Name"
    assert surname == "Surname"
    assert age == 67
    assert primary_interest == Interest.MUSIC.value

    (email, name, surname, age, primary_interest) = profiles[1]
    assert email == "user@innopolis.ru"
    assert name == "Name2"
    assert surname == "Surname2"
    assert age == 45
    assert primary_interest == Interest.PROGRAMMING.value
