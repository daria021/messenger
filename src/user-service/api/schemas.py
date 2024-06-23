from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserUpdate(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]


class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    hashed_password: str


class UserResponse(UserCreate):
    id: int
    name: str
    username: str
    email: str
    registered_at: datetime
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)


class UserFilter(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    registered_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


