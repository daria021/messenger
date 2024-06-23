from pydantic import BaseModel, ConfigDict


class MessagesModel(BaseModel):
    id: int
    message: str

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    text: str
    id_sender: int
    id_recipient: int


class MessageResponse(MessageCreate):
    id: int
    text: str
    id_sender: int
    id_recipient: int
    model_config = ConfigDict(from_attributes=True)


class ChatMessageCreate(BaseModel):
    text: str
    id_sender: int
    id_chat: int


class ChatMessageResponce(BaseModel):
    id: int
    text: str
    id_sender: int
    id_chat: int