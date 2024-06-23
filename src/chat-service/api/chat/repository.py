from AbstractRepository import AbstractRepo
from .schemas import ChatUpdate, ChatCreate, ChatResponse
from .models import Chat


class ChatRepo(AbstractRepo):
    model = Chat
    update_schema = ChatUpdate
    create_schema = ChatCreate
    get_schema = ChatResponse

