import os

import requests
from fastapi import Request, HTTPException
from fastapi import Response as FastApiResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from requests import Response
from app.src.models.auth import AuthWithEmailRequest, VerifyAccessTokenResult
from app.src.models.response import SuccessResponse

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")  # pragma: no mutate
PROJECT_ID = os.getenv("PROJECT_ID")  # pragma: no mutate
BASE_API_URL = "https://identitytoolkit.googleapis.com/v1/"  # pragma: no mutate  # noqa: E501
ACCESS_TOKEN_NAME = "access_token"  # pragma: no mutate
REFRESH_TOKEN_NAME = "refresh_token"  # pragma: no mutate


def get_token_from_cookie(request: Request):
    authorization = request.cookies.get(ACCESS_TOKEN_NAME)
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization token missing"
        )

    return authorization.split(" ")[1]


def verify_access_token(request: Request):
    token = get_token_from_cookie(request)
    try:
        id_info = id_token.verify_firebase_token(
            token,
            google_requests.Request()
        )
        user_id = id_info["user_id"]  # pragma: no mutate
        email = id_info["email"]  # pragma: no mutate
        return VerifyAccessTokenResult(user_id=user_id, email=email)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid ID token"
        )


def get_refresh_token(request: Request):
    refresh_token = request.cookies.get(REFRESH_TOKEN_NAME)
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )
    return refresh_token


def register(request: AuthWithEmailRequest, fastapi_response: FastApiResponse):
    response = email_auth_call(
        request,
        "accounts:signUp"  # pragma: no mutate
    )
    data = response.json()
    access_token = data["idToken"]  # pragma: no mutate
    refresh_token = data["refreshToken"]  # pragma: no mutate
    set_httponly_cookie(access_token, refresh_token, fastapi_response)
    return SuccessResponse()


def login(request: AuthWithEmailRequest, fastapi_response: FastApiResponse):
    response = email_auth_call(
        request,
        "accounts:signInWithPassword"  # pragma: no mutate
    )
    data = response.json()
    access_token = data["idToken"]  # pragma: no mutate
    refresh_token = data["refreshToken"]  # pragma: no mutate
    set_httponly_cookie(access_token, refresh_token, fastapi_response)
    return SuccessResponse()


def delete_auth_for_user(request: Request):
    verify_access_token(request)
    token = get_token_from_cookie(request)
    url_sub_path = "accounts:delete"  # pragma: no mutate
    details = {
        "idToken": token  # pragma: no mutate
    }  # pragma: no mutate

    response = requests.post(
        f"{BASE_API_URL}{url_sub_path}?key={FIREBASE_API_KEY}",  # pragma: no mutate  # noqa: E501
        data=details,
        timeout=10
    )

    if "error" in response.json().keys():
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": response.json()["error"]["message"]
            }
        )

    return SuccessResponse()


def refresh_auth_tokens(request: Request, fastapi_response: FastApiResponse):
    url_sub_path = "token"  # pragma: no mutate
    details = {
        "grant_type": REFRESH_TOKEN_NAME,  # pragma: no mutate
        "refresh_token": get_refresh_token(request)  # pragma: no mutate
    }  # pragma: no mutate

    response = requests.post(
        f"{BASE_API_URL}{url_sub_path}?key={FIREBASE_API_KEY}",  # pragma: no mutate  # noqa: E501
        data=details,
        timeout=10
    )

    if "error" in response.json().keys():
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": response.json()["error"]["message"]
            }
        )

    data = response.json()
    access_token = data["id_token"]  # pragma: no mutate
    refresh_token = data["refresh_token"]  # pragma: no mutate
    set_httponly_cookie(access_token, refresh_token, fastapi_response)
    return SuccessResponse()


def set_httponly_cookie(
        access_token: str,
        refresh_token: str,
        response: FastApiResponse
):
    response.set_cookie(
        key=ACCESS_TOKEN_NAME,
        value=f"Bearer {access_token}",  # pragma: no mutate
        httponly=True
    )
    response.set_cookie(
        key=REFRESH_TOKEN_NAME,
        value=refresh_token,
        httponly=True
    )


def email_auth_call(
        request: AuthWithEmailRequest,
        url_sub_path: str
) -> Response:
    details = {
        "email": request.email,  # pragma: no mutate
        "password": request.password,  # pragma: no mutate
        "returnSecureToken": True  # pragma: no mutate
    }  # pragma: no mutate

    response = requests.post(
        f"{BASE_API_URL}{url_sub_path}?key={FIREBASE_API_KEY}",  # pragma: no mutate  # noqa: E501
        data=details,
        timeout=10
    )

    if "error" in response.json().keys():
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": response.json()["error"]["message"]
            }
        )

    if "idToken" not in response.json().keys():
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "Token not found in response"
            }
        )

    return response
