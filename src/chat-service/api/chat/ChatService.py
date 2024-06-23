from api.chat.repository import ChatRepo

from AbstractService import AbstractService


class ChatService(AbstractService):
    repo_type = ChatRepo
