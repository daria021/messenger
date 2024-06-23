from fastapi import FastAPI

from api.routes import router as message_router

app = FastAPI(
    title="messenger"
)


app.include_router(
    message_router
)


