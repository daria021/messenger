from AbstractService import AbstractService
from users.exception import ServerError
from .repository import ChatMessageRepo
from .schemas import ChatMessageCreate
from users.service import UserService


class ChatMessageService(AbstractService):
    repo_type = ChatMessageRepo

    async def create(self, chat_message: ChatMessageCreate) -> repo_type.get_schema:
        id_sender = chat_message.id_sender
        try:
            if await UserService.check_user(id_sender):
                chat_message = await super().create(schema=chat_message)
        except Exception as e:
            raise ServerError(e)

        return chat_message

    async def get_last_messages(self, amount: int) -> list[repo_type.get_schema]:
        return await self.repository.get_last_messages(amount=amount)

