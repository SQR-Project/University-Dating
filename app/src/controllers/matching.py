from fastapi import APIRouter, Depends
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.response import SuccessResponse
from app.src.models.like import LikeProfileRequest, MatchingResponse
from app.src.services import auth_service
from app.src.services import like_service

matching_router = APIRouter(
    prefix="/matching",  # pragma: no mutate
    tags=["matching"]
)  # pragma: no mutate


@matching_router.post("/like", response_model=SuccessResponse)
def register(request: LikeProfileRequest):
    return like_service.like_profile(request)


@matching_router.post("/is-matched", response_model=MatchingResponse)
def login(
        request: LikeProfileRequest,
        token_data: VerifyAccessTokenResult = Depends(
            auth_service.verify_access_token
        )
):
    return like_service.is_matched(token_data, request)
