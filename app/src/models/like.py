from pydantic import BaseModel


class LikeProfileRequest(BaseModel):
    email: str


class MatchingResponse(BaseModel):
    matched: bool
