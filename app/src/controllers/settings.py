from fastapi import APIRouter

settings_router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)


@settings_router.get("/200", response_model=bool)
def get_ok():
    return True
