from app.src.dal.database import Database
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.response import SuccessResponse
from app.src.models.like import LikeProfileRequest, MatchingResponse


def like_profile(
        token_data: VerifyAccessTokenResult,
        request: LikeProfileRequest
):
    database = Database()
    profile_likes = database.get_profile_likes(token_data)
    updated_likes = profile_likes + f',{request.email}'
    database.update_profile_likes(token_data, updated_likes)
    return SuccessResponse()


def is_matched(
        token_data: VerifyAccessTokenResult,
        request: LikeProfileRequest
):
    database = Database()
    liked_person_id = database.unsafe_get_profile_by_email(request.email)
    liked_person_likes = database.get_profile_likes_by_user_id(
        liked_person_id).split(',')
    MatchingResponse(token_data.email in liked_person_likes)
