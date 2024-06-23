from AbstractRepository import AbstractRepo
from .schemas import MessageUpdate, MessageCreate, MessageResponse
from .models import Message


class MessageRepo(AbstractRepo):
    model = Message
    update_schema = MessageUpdate
    create_schema = MessageCreate
    get_schema = MessageResponse
