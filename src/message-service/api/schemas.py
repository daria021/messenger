from typing import Optional
from pydantic import BaseModel, ConfigDict


class MessageUpdate(BaseModel):
    text: Optional[str]
    id_sender: Optional[int]
    id_recipient: Optional[int]


class MessageCreate(MessageUpdate):
    text: str
    id_sender: int
    id_recipient: int


class MessageResponse(MessageCreate):
    id: int
    text: str
    id_sender: int
    id_recipient: int
    model_config = ConfigDict(from_attributes=True)


class MessageFilter(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    id_sender: Optional[int] = None
    id_recipient: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)