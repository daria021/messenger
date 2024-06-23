from fastapi import APIRouter, Depends

from .ChatService import ChatUserService
from .dependencies.services import get_chat_user_service
from .schemas import ChatUserCreate, ChatUserResponse

router = APIRouter(
    prefix="/chat_user",
    tags=["chat_user/"]
)



@router.post("", response_model=ChatUserResponse)
async def add_user_to_chat(chat_user: ChatUserCreate,
                           chat_users: ChatUserService = Depends(get_chat_user_service)):
    chat_user = await chat_users.create(chat_user=chat_user)
    return chat_user

