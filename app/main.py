import logging

import fastapi
from fastapi import responses
from app.src.controllers.auth import auth_router
from app.src.controllers.profile import profile_router
from app.src.controllers.status import status_router
from app.src.controllers.matching import matching_router

application = fastapi.FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@application.exception_handler(Exception)
async def exception_handler(request, err):
    base_error_message = f'Failed to execute: {request.method}: {request.url}'
    return responses.JSONResponse(
        status_code=500,
        content={'message': f'{base_error_message}. Detail: {err}'}
    )

application.include_router(auth_router)
application.include_router(profile_router)
application.include_router(status_router)
application.include_router(matching_router)
