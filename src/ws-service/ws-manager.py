from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from ws.schemas import MessageCreate, ChatMessageCreate
from service import message_create, chat_message_create

router = APIRouter(
    prefix="/ws",
    tags=["ws/"]
)


class ConnectionManager:  # класс хранящий активные ws соединения
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


class WS(BaseModel):
    text: str
    chat_or_recipient_id: int
    is_private: bool


@router.websocket("/ws/{client_id}")
async def websocket_message_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = WS.model_validate(await websocket.receive_json())
            if data.is_private:
                message = MessageCreate(
                    text=data.text,
                    recipient_id=data.chat_or_recipient_id
                )

                await message_create(message)
            else:
                message = ChatMessageCreate(
                text = data.text,
                chat_id = data.chat_or_recipient_id
                )

                await chat_message_create(message)
            await manager.broadcast(f"Client #{client_id} says: {data.text} to {data.recipient_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
