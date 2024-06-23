from sqlalchemy import Integer, String
from api.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    count_of_people: Mapped[int] = mapped_column(Integer, nullable=False)

    users = relationship("ChatUser", back_populates="chat", cascade="all, delete-orphan")