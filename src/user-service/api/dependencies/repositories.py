from contextlib import asynccontextmanager

from api.db import get_async_session
from api.repository import UserRepo


async def get_user_repo() -> UserRepo:
    async with get_async_session() as session:
        yield UserRepo(session=session)


@asynccontextmanager
async def user_repo_context() -> UserRepo:
    async with get_async_session() as session:
        yield UserRepo(session=session)
