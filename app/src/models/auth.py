from pydantic import BaseModel


class AuthWithEmailRequest(BaseModel):
    email: str
    password: str
