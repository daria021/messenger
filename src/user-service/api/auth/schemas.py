from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorizationUpdate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class AuthorizationCreate(AuthorizationUpdate):
    user_id: int
    access_token: str
    refresh_token: str


class AuthorizationResponse(AuthorizationCreate):
    id: int
    user_id: int
    created_at: datetime
    access_token: str
    refresh_token: str
    model_config = ConfigDict(from_attributes=True)


