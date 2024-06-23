from fastapi import FastAPI

from api.chat.routes import router as router_chat
from api.chat_message.routes import router as router_chat_message
from api.chat_user.routes import router as router_chat_user

app = FastAPI(
    title="chat"
)

app.include_router(
    router_chat
)

app.include_router(
    router_chat_message
)

app.include_router(
    router_chat_user
)




