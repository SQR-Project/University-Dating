import sqlite3

from fastapi import HTTPException
from app.src.dal.database import Database
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import CreateProfileRequest, ProfileInformation
from app.src.models.response import SuccessResponse


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
            liked_profiles=liked_profiles,
            primary_interest=primary_interest
        )
        for (
            email,
            name,
            surname,
            age,
            liked_profiles,
            primary_interest
        ) in database.get_all_profiles()
    ]

def get_profile_by_email(email: str) -> ProfileInformation:
    database = Database()
    profiles = [
        ProfileInformation(
            email=email,
            name=name,
            surname=surname,
            age=age,
            liked_profiles=liked_profiles,
            primary_interest=primary_interest
        )
        for (
            email,
            name,
            surname,
            age,
            liked_profiles,
            primary_interest
        ) in database.get_profile_by_email(email)
    ]
    if len(profiles) == 0:
        raise HTTPException(
            status_code=400,
            detail="Profile does not exist"
        )
    return profiles[0]
