import re

from fastapi import HTTPException

EMAIL_PATTERN_STR = r"^[-\w\.]+@innopolis\.(university|ru)$"
EMAIL_PATTERN = re.compile(EMAIL_PATTERN_STR)


def validate(email: str) -> bool:
    match = re.match(EMAIL_PATTERN, email)
    if match is None:
        raise HTTPException(status_code=400, detail="Email validation error. Use Innopolis university email")
    return True
