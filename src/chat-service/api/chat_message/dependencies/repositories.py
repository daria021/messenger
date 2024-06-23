from contextlib import asynccontextmanager

from api.db import get_async_session
from api.chat_message.repository import ChatMessageRepo


@asynccontextmanager
async def get_chat_message_repo() -> ChatMessageRepo:
    async with get_async_session() as session:
        yield ChatMessageRepo(session=session)


