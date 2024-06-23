from AbstractRepository import AbstractRepo
from .models import ChatUser
from .schemas import ChatUserCreate, ChatUserResponse, ChatUserUpdate


class ChatUserRepo(AbstractRepo):
    model = ChatUser
    update_schema = ChatUserUpdate
    create_schema = ChatUserCreate
    get_schema = ChatUserResponse
