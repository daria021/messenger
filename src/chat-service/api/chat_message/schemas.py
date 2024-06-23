from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChatMessageCreate(BaseModel):
    text: str
    id_sender: int
    id_chat: int


class ChatMessageResponse(BaseModel):
    id: int
    text: str
    id_sender: int
    id_chat: int

    model_config = ConfigDict(from_attributes=True)

class ChatMessageUpdate(BaseModel):
    text: Optional[str]



