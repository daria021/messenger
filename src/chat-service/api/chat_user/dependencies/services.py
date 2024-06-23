from api.chat_user.dependencies.repositories import get_chat_user_repo
from api.chat_user.ChatService import ChatUserService


async def get_chat_user_service() -> ChatUserService:
    async with get_chat_user_repo() as repo:
        yield ChatUserService(repo=repo)