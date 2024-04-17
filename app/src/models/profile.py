from pydantic import BaseModel

from src.enums.interests_enum import Interest


class CreateProfileRequest(BaseModel, validate_assignment=True):
    name: str
    surname: str
    age: int = 0
    primary_interest: Interest = Interest.PROGRAMMING


class ProfileInformation(CreateProfileRequest):
    email: str
