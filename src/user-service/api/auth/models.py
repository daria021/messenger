from datetime import datetime

from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs

from api.db import Base


class Authorization(Base, AsyncAttrs):
    __tablename__ = 'authorizations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    access_token = Column(String)
    refresh_token = Column(String)
    created_at = Column(DateTime, default=datetime.now)