import sqlite3

from fastapi import HTTPException
from src.dal.database import Database
from src.models.auth import VerifyAccessTokenResult
from src.models.profile import CreateProfileRequest, ProfileInformation
from src.models.response import SuccessResponse


def create_profile(
        token_data: VerifyAccessTokenResult,
        request: CreateProfileRequest
):
    database = Database()
    try:
        database.add_profile(token_data, request)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists"
        )

    return SuccessResponse()


def delete_profile(token_data: VerifyAccessTokenResult):
    database = Database()
    database.delete_profile(token_data)
    return SuccessResponse()


def get_all_profiles() -> list[ProfileInformation]:
    database = Database()
    return [
        ProfileInformation(
            email=email,
            name=name,
            surname=surname,
            age=age,
            primary_interest=primary_interest
        )
        for (email, name, surname, age, primary_interest) in database.get_all_profiles()
    ]
