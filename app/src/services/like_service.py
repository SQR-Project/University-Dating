import sqlite3

from fastapi import HTTPException
from app.src.dal.database import Database
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.response import SuccessResponse
from app.src.models.like import LikeProfileRequest, MatchingResponse


def like_profile(
        token_data: VerifyAccessTokenResult,
        request: LikeProfileRequest
):
    database = Database()
    try:
        profile_likes = database.get_profile_likes_by_user_id(token_data.user_id)
        updated_likes = str(profile_likes) + f',{request.email}'
        database.update_profile_likes(token_data, updated_likes)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Profile does not exists"
        )    
    return SuccessResponse()


def is_matched(
        token_data: VerifyAccessTokenResult,
        request: LikeProfileRequest
):
    try:
        database = Database()
        liked_person_id = database.unsafe_get_profile_by_email(request.email)

        liked_person_likes = database.get_profile_likes_by_user_id(
            liked_person_id[0][0])[0].split(',')
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Profile does not exists"
        )        
    return MatchingResponse(matched = token_data.email in liked_person_likes)
