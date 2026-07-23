from qdrant_client import QdrantClient

from app.core.config import settings

client = QdrantClient(
    url=settings.qdrant_url
)

COLLECTION_NAME = "knowledge_base"