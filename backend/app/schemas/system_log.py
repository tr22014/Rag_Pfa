from pydantic import BaseModel
from datetime import datetime


class SystemLogOut(BaseModel):
    id: int
    action: str
    detail: str | None
    user_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True