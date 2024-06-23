from fastapi import APIRouter, Depends

from dependencies.services import get_message_service
from .MessageService import MessageService
from .models import Message
from .schemas import MessageResponse, MessageCreate, MessageUpdate, MessageFilter

router = APIRouter(
    prefix="/message",
    tags=["message/"]
)


@router.post("", response_model=MessageResponse)
async def create_message(message: MessageCreate,
                         messages: MessageService = Depends(get_message_service)):
    message = await messages.create(message=message)
    return message


@router.get("/all", response_model=list[MessageResponse])
async def get_all_messages(messages: MessageService = Depends(get_message_service)
                           ) -> list[Message]:
    res = await messages.get_all()
    return res


@router.get("/filter", response_model=list[MessageResponse])
async def get_filter_message(filters: MessageFilter = Depends(),
                             messages: MessageService = Depends(get_message_service)
                             ) -> Message:
    clean_filters = {key: value for key, value in filters.model_dump().items() if value is not None}
    res = await messages.get_filtered_by(**clean_filters)
    return res



@router.get("/{message_id}", response_model=MessageResponse)
async def get_one_message(message_id: int, messages: MessageService = Depends(get_message_service)):
    res = await messages.get(record_id=message_id)
    return res



@router.put("", response_model=MessageResponse)
async def update_message(message_id: int,
                         update: MessageUpdate,
                         messages: MessageService = Depends(get_message_service)):
    user = await messages.update(record_id=message_id, schema=update)
    return user


@router.delete("")
async def delete_message(message_id: int,
                         messages: MessageService = Depends(get_message_service)):
    await messages.delete(record_id=message_id)