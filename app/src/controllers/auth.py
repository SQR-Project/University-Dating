from fastapi import APIRouter, Response, Request, Depends
from src.models.auth import AuthWithEmailRequest
from src.services import auth_service
from src.validators import email_validator


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/register")
def register(request: AuthWithEmailRequest, response: Response):
    email_validator.validate(request)
    return auth_service.register(request, response)


@auth_router.post("/login")
def login(request: AuthWithEmailRequest, response: Response):
    email_validator.validate(request)
    return auth_service.login(request, response)


@auth_router.post("/refresh")
def refresh_tokens(request: Request, response: Response):
    return auth_service.refresh_auth_tokens(request, response)


@auth_router.get("/data-from-token")
def refresh_tokens(decoded_token: dict = Depends(auth_service.verify_access_token)):
    return decoded_token
