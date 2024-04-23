import re

from fastapi import HTTPException

from app.src.models.profile import CreateProfileRequest

NAME_PATTERN_STR = r"^[\w.'-]+$"  # pragma: no mutate
NAME_PATTERN = re.compile(NAME_PATTERN_STR)


def validate(request: CreateProfileRequest) -> bool:
    if request.age <= 10 or request.age > 100:
        raise HTTPException(
            status_code=400,
            detail="CreateProfileRequest validation error. "
                   "Age should be greater than 10 amd less than 100"
        )
    match_name = re.match(NAME_PATTERN, request.name)
    match_surname = re.match(NAME_PATTERN, request.surname)
    if match_name is None or match_surname is None:
        raise HTTPException(
            status_code=400,
            detail="CreateProfileRequest validation error. "
                   "Name and surname should consist of: letters, -, ., and '"
        )
    return True
