from pydantic import BaseModel
from datetime import datetime
from app.models.message import MessageRole
from app.schemas.source import SourceOut


# Ce que l'utilisateur envoie pour poser une question
class MessageCreate(BaseModel):
    content: str


# Ce que l'API renvoie (question ou réponse, avec ses sources si assistant)
class MessageOut(BaseModel):
    id: int
    conversation_id: int
    role: MessageRole
    content: str
    created_at: datetime
    sources: list[SourceOut] = []

    class Config:
        from_attributes = True