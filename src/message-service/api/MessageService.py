from AbstractService import AbstractService
from users.service import UserService
from .repository import MessageRepo
from .schemas import MessageCreate


class MessageService(AbstractService):
    repo_type = MessageRepo

    async def create(self, message: MessageCreate):
        id_sender = message.id_sender
        id_recipient = message.id_recipient
        try:
            if await UserService.check_user(id_sender):
                print("1 check")
                if await UserService.check_user(id_recipient):
                    print("2 check")
                    message = await super().create(message)
        except Exception as e:
            raise e
        return message
