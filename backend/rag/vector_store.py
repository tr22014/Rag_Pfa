import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "knowledge_base"
VECTOR_SIZE = 384


def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )
    print(f"Collection '{COLLECTION_NAME}' créée.")


def load_and_upsert(file_path=None, batch_size=100):
    if file_path is None:
        file_path = os.path.join(BASE_DIR, "chunks_embeddings.json")

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    points = []
    for i, chunk in enumerate(chunks):
        points.append(
            PointStruct(
                id=i,
                vector=chunk["embedding"],
                payload={
                    "text": chunk["text"],
                    "document_id": chunk.get("document_id"),
                    "page": chunk.get("page_number"),
                }
            )
        )

    for start in range(0, len(points), batch_size):
        batch = points[start:start + batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)

    print(f"{len(points)} chunks insérés dans Qdrant.")


if __name__ == "__main__":
    create_collection()
    load_and_upsert()