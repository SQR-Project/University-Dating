from fastapi import APIRouter, Response, Request, Depends
from src.models.auth import AuthWithEmailRequest, VerifyAccessTokenResult
from src.models.response import SuccessResponse
from src.services import auth_service
from src.validators import email_validator

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/register", response_model=SuccessResponse)
def register(request: AuthWithEmailRequest, response: Response):
    email_validator.validate(request.email)
    return auth_service.register(request, response)


@auth_router.post("/login", response_model=SuccessResponse)
def login(request: AuthWithEmailRequest, response: Response):
    email_validator.validate(request.email)
    return auth_service.login(request, response)


@auth_router.post("/refresh", response_model=SuccessResponse)
def refresh_tokens(request: Request, response: Response):
    return auth_service.refresh_auth_tokens(request, response)


@auth_router.delete("/auth-data", response_model=SuccessResponse)
def delete_auth_data(
        request: Request,
        _: VerifyAccessTokenResult = Depends(auth_service.verify_access_token)
):
    return auth_service.delete_auth_for_user(request)
