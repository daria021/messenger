from sqlalchemy import Integer
from api.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class ChatUser(Base):
    __tablename__ = "chat_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_chat: Mapped[int] = mapped_column(Integer, ForeignKey("chat.id"))
    id_user: Mapped[int] = mapped_column(Integer, nullable=False)

    chat = relationship("Chat", back_populates="users")