from pydantic import BaseModel
from datetime import datetime


class ConversationCreate(BaseModel):
    title: str | None = None


class ConversationUpdate(BaseModel):
    title: str | None = None


class ConversationOut(BaseModel):
    id: int
    title: str | None
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True