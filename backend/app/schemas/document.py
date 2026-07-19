from pydantic import BaseModel
from datetime import datetime
from app.models.document import DocumentStatus


# Pas de "DocumentCreate" classique ici : la création se fait
# généralement via upload de fichier (UploadFile), pas via JSON pur.
# On garde un schéma pour la métadonnée si besoin de la modifier.
class DocumentUpdate(BaseModel):
    filename: str | None = None
    collection_id: int | None = None


class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: str | None
    status: DocumentStatus
    chunk_count: int
    collection_id: int | None
    uploaded_by_id: int
    uploaded_at: datetime
    indexed_at: datetime | None

    class Config:
        from_attributes = True