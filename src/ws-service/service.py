from httpx import AsyncClient
from ws.schemas import MessageCreate, MessageResponse, ChatMessageCreate, ChatMessageResponce


async def message_create(message: MessageCreate):
    async with AsyncClient() as client:
        response = await client.post(
            "http://app_message:8000/message/",
            json=message.model_dump(),
        )

    if response.status_code == 200:
        return MessageResponse.model_validate_json(response.json())


async def chat_message_create(message: ChatMessageCreate):
    async with AsyncClient() as client:
        response = await client.post(
            "http://app_chat:8000/chat/",
            json=message.model_dump(),
        )

    if response.status_code == 200:
        return ChatMessageResponce.model_validate_json(response.json())
