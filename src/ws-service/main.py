from fastapi import FastAPI

from ws.router import router

app = FastAPI()

app.include_router(router)
