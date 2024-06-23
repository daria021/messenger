from typing import Optional
from pydantic import BaseModel, ConfigDict


class ChatUpdate(BaseModel):
    name: Optional[str]
    count_of_people: Optional[int]


class ChatCreate(ChatUpdate):
    name: str
    count_of_people: int


class ChatResponse(ChatCreate):
    id: int
    name: str
    count_of_people: int
    model_config = ConfigDict(from_attributes=True)



class ChatFilters(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    count_of_people: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)



