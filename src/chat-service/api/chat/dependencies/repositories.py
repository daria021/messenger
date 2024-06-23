from contextlib import asynccontextmanager

from api.db import get_async_session
from api.chat.repository import ChatRepo


async def get_chat_repo() -> ChatRepo:
    async with get_async_session() as session:
        yield ChatRepo(session=session)