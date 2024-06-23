from sqlalchemy import Integer, String
from api.db import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_sender: Mapped[int] = mapped_column(Integer, nullable=False)
    id_chat: Mapped[int] = mapped_column(Integer, ForeignKey("chat.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

