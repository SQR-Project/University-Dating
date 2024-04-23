from fastapi import APIRouter

from app.src.dal.database import Database

status_router = APIRouter(
    prefix="/status",  # pragma: no mutate
    tags=["status"]
)  # pragma: no mutate


@status_router.get("/healthz")  # pragma: no mutate
def check_app_health():
    database = Database()
    return database.check()
