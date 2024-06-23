from fastapi import APIRouter, Depends

from .ChatMessageService import ChatMessageService
from .dependencies.services import get_chat_message_service
from .schemas import ChatMessageCreate
from .schemas import ChatMessageResponse

router = APIRouter(
    prefix="/chat_message",
    tags=["chat_message/"]
)

@router.get("/last_messages")
async def get_last_messages(
        chat_messages: ChatMessageService = Depends(get_chat_message_service)
) -> list[ChatMessageResponse]:
    res = await chat_messages.get_last_messages(amount=10)
    return res



@router.post("", response_model=ChatMessageResponse)
async def create_chat_message(chat_message: ChatMessageCreate,
                      chat_messages: ChatMessageService = Depends(get_chat_message_service)):
    chat_message = await chat_messages.create(chat_message=chat_message)
    return chat_message




@router.post("", response_model=ChatMessageResponse)
async def create_message(message: ChatMessageCreate,
                   chat_messages: ChatMessageService = Depends(get_chat_message_service)):
    message = await chat_messages.create(chat_message=message)
    return message
