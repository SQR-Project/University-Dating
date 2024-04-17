from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.controllers.auth import auth_router
from src.controllers.profile import profile_router

app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request, err):
    base_error_message = f'Failed to execute: {request.method}: {request.url}'
    return JSONResponse(
        status_code=500,
        content={'message': f'{base_error_message}. Detail: {err}'}
    )

app.include_router(auth_router)
app.include_router(profile_router)
