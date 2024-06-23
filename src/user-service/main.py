import asyncio

from fastapi import FastAPI

from api.routes import router as auth_router
from api.auth.routes import router as user_router
from messages import user_request_handler

app = FastAPI(
    title="user"
)

app.include_router(
    user_router
)

app.include_router(auth_router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(user_request_handler())
