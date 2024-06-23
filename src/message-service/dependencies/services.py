from api.MessageService import MessageService
from dependencies.repositories import get_message_repo


async def get_message_service() -> MessageService:
    async with get_message_repo() as repo:
        yield MessageService(repo=repo)