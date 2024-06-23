from sqlalchemy import select

from AbstractRepository import AbstractRepo
from .models import ChatMessage

from .schemas import ChatMessageUpdate, ChatMessageCreate, ChatMessageResponse


class ChatMessageRepo(AbstractRepo):
    model = ChatMessage
    update_schema = ChatMessageUpdate
    create_schema = ChatMessageCreate
    get_schema = ChatMessageResponse

    async def get_last_messages(self, amount: int) -> list[get_schema]:
        query = select(self.model).order_by(self.model.id.desc()).limit(amount)
        messages = await self.session.execute(query)
        res = messages.scalars().all()

        return [self.get_schema.model_validate(message) for message in res]
