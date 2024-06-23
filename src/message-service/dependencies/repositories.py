from contextlib import asynccontextmanager

from api.db import get_async_session
from api.repository import MessageRepo


@asynccontextmanager
async def get_message_repo() -> MessageRepo:
    async with get_async_session() as session:
        yield MessageRepo(session=session)