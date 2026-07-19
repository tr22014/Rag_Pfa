from pydantic import BaseModel


class SourceOut(BaseModel):
    id: int
    document_id: int
    chunk_text: str | None
    page_number: int | None
    relevance_score: float | None

    class Config:
        from_attributes = True