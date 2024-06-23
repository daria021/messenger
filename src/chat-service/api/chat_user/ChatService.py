from AbstractService import AbstractService
from users.service import UserService
from users.exception import ServerError
from .repository import ChatUserRepo
from .schemas import ChatUserCreate


class ChatUserService(AbstractService):
    repo_type = ChatUserRepo

    async def create(self, chat_user: ChatUserCreate):
        id_user = chat_user.id_user
        try:
            if await UserService.check_user(id_user):
                chat_user = await super().create(schema=chat_user)
        except Exception as e:
            raise ServerError

        return chat_user
