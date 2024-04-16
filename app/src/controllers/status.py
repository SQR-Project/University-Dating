from fastapi import APIRouter

from src.dal.database import Database

status_router = APIRouter(
    prefix="/status",
    tags=["status"]
)


@status_router.get("/healthz")  # pragma: no mutate
def check_app_health():
    database = Database()
    return database.check()
