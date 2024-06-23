from api.chat_message.ChatMessageService import ChatMessageService
from api.chat_message.dependencies.repositories import get_chat_message_repo


async def get_chat_message_service() -> ChatMessageService:
    async with get_chat_message_repo() as repo:
        yield ChatMessageService(repo=repo)