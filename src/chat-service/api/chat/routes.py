from .dependencies.repositories import get_chat_repo
from .repository import ChatRepo
from .schemas import ChatUpdate, ChatFilters

from fastapi import APIRouter, Depends

from .schemas import ChatCreate, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat/"]
)


@router.post("")
async def create_chat(chat: ChatCreate, chats: ChatRepo = Depends(get_chat_repo)) -> ChatResponse:
    chat = await chats.create(schema=chat)
    return chat



@router.get("")
async def get_all_chats(
        chats: ChatRepo = Depends(get_chat_repo)
) -> list[ChatResponse]:
    res = await chats.get_all()
    return res


@router.get("/filter")
async def get_filter_chat(filters: ChatFilters = Depends(), chats: ChatRepo = Depends(get_chat_repo)
                          ) -> list[ChatResponse]:
    clean_filters = {key: value for key, value in filters.model_dump().items() if value is not None}
    res = await chats.get_filtered_by(**clean_filters)
    return res


@router.get("/{chat_id}")
async def get_one_chat(chat_id: int, chats: ChatRepo = Depends(get_chat_repo))-> ChatResponse:
    res = await chats.get(record_id=chat_id)
    return res



@router.put("/{chat_id}")
async def update_chat(chat_id: int,
                      update: ChatUpdate,
                      chats: ChatRepo = Depends(get_chat_repo)) -> ChatResponse:
    chat = await chats.update(record_id=chat_id, schema=update)
    return chat


@router.delete("")
async def delete_chat(chat_id: int,
                    chats: ChatRepo = Depends(get_chat_repo)):
    await chats.delete(record_id=chat_id)
    return


