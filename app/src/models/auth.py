from pydantic import BaseModel


class AuthWithEmailRequest(BaseModel):
    email: str
    password: str


class VerifyAccessTokenResult(BaseModel):
    user_id: str
    email: str
