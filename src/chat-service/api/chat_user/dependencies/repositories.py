from contextlib import asynccontextmanager

from api.db import get_async_session
from api.chat_user.repository import ChatUserRepo


@asynccontextmanager
async def get_chat_user_repo() -> ChatUserRepo:
    async with get_async_session() as session:
        yield ChatUserRepo(session=session)