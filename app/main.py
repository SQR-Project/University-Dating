from fastapi import FastAPI
from src.controllers.settings import settings_router

app = FastAPI()

app.include_router(settings_router)
