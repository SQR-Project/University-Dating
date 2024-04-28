from fastapi import APIRouter, Depends

from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import CreateProfileRequest, ProfileInformation
from app.src.models.response import SuccessResponse
from app.src.services import auth_service, profile_service
from app.src.validators import profile_validator

profile_router = APIRouter(
    prefix="/profile",  # pragma: no mutate
    tags=["profile"]
)  # pragma: no mutate


@profile_router.post("/create", response_model=SuccessResponse)
def create_profile(
        request: CreateProfileRequest,
        token_data: VerifyAccessTokenResult = Depends(
            auth_service.verify_access_token
        )
):
    profile_validator.validate(request)
    return profile_service.create_profile(token_data, request)


@profile_router.delete("/", response_model=SuccessResponse)
def delete_profile(
        token_data: VerifyAccessTokenResult = Depends(
            auth_service.verify_access_token
        )
):
    return profile_service.delete_profile(token_data)


@profile_router.get("/all", response_model=list[ProfileInformation])
def get_all_profiles(
        _: VerifyAccessTokenResult = Depends(auth_service.verify_access_token)
):
    return profile_service.get_all_profiles()
