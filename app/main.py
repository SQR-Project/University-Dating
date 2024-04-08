from fastapi import FastAPI
from src.controllers.settings import settings_router
from src.controllers.auth import auth_router

app = FastAPI()

app.include_router(settings_router)
app.include_router(auth_router)
