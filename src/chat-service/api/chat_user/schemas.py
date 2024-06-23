from pydantic import BaseModel, ConfigDict


class ChatUserCreate(BaseModel):
    id_user: int
    id_chat: int


class ChatUserResponse(BaseModel):
    id: int
    id_user: int
    id_chat: int

    model_config = ConfigDict(from_attributes=True)


class ChatUserUpdate(BaseModel):
    ...
