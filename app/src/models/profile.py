from pydantic import BaseModel

from app.src.enums.interests_enum import Interest


class CreateProfileRequest(BaseModel):
    name: str
    surname: str
    age: int
    primary_interest: Interest = Interest.PROGRAMMING


class ProfileInformation(CreateProfileRequest):
    email: str
    liked_profiles: str
