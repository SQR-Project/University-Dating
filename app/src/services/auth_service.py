import os

import requests
from fastapi import Request, HTTPException
from fastapi import Response as FastApiResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from requests import Response
from src.models.auth import AuthWithEmailRequest

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
BASE_API_URL = "https://identitytoolkit.googleapis.com/v1/"
ACCESS_TOKEN_NAME = "access_token"
REFRESH_TOKEN_NAME = "refresh_token"


def verify_access_token(request: Request):
    authorization = request.cookies.get(ACCESS_TOKEN_NAME)
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    token = authorization.split(" ")[1]
    try:
        id_info = id_token.verify_firebase_token(token, google_requests.Request())
        user_id = id_info['user_id']
        email = id_info['email']
        return {"user_id": user_id, "email": email}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid ID token")


def get_refresh_token(request: Request):
    refresh_token = request.cookies.get(REFRESH_TOKEN_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    return refresh_token


def register(request: AuthWithEmailRequest, fastapi_response: FastApiResponse):
    response = email_auth_call(request, "accounts:signUp")
    data = response.json()
    access_token = data["idToken"]
    refresh_token = data["refreshToken"]
    set_httponly_cookie(access_token, refresh_token, fastapi_response)
    return {"status": "success"}


def login(request: AuthWithEmailRequest, fastapi_response: FastApiResponse):
    response = email_auth_call(request, "accounts:signInWithPassword")
    data = response.json()
    access_token = data["idToken"]
    refresh_token = data["refreshToken"]
    set_httponly_cookie(access_token, refresh_token, fastapi_response)
    return {"status": "success"}


def refresh_auth_tokens(request: Request, fastapi_response: FastApiResponse):
    url_sub_path = "token"
    details = {
        "grant_type": REFRESH_TOKEN_NAME,
        "refresh_token": get_refresh_token(request)
    }

    response = requests.post(f"{BASE_API_URL}{url_sub_path}?key={FIREBASE_API_KEY}", data=details)

    if "error" in response.json().keys():
        raise HTTPException(status_code=401, detail={"status": "error", "message": response.json()["error"]["message"]})

    data = response.json()
    access_token = data["id_token"]
    refresh_token = data["refresh_token"]
    set_httponly_cookie(access_token, refresh_token, fastapi_response)
    return {"status": "success"}


def set_httponly_cookie(access_token: str, refresh_token: str, response: FastApiResponse):
    response.set_cookie(key=ACCESS_TOKEN_NAME, value=f"Bearer {access_token}", httponly=True)
    response.set_cookie(key=REFRESH_TOKEN_NAME, value=refresh_token, httponly=True)


def email_auth_call(request: AuthWithEmailRequest, url_sub_path: str) -> Response:
    details = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    response = requests.post(f"{BASE_API_URL}{url_sub_path}?key={FIREBASE_API_KEY}", data=details)

    if "error" in response.json().keys():
        raise HTTPException(status_code=401, detail={"status": "error", "message": response.json()["error"]["message"]})

    if "idToken" not in response.json().keys():
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Token not found in response"})

    return response
