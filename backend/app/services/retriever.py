from qdrant_client.models import Filter
from database.qdrant import client, COLLECTION_NAME
from rag.embedder import create_embedding


class Retriever:

    def __init__(self):
        self.client = client
        self.collection = COLLECTION_NAME

    def retrieve(
        self,
        question: str,
        limit: int = 5,
        query_filter: Filter | None = None
    ):

        query_vector = create_embedding(question)

        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=limit,
            query_filter=query_filter
        ).points

        chunks = []

        for result in results:
            chunks.append(
                {
                    "chunk_id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "document_id": result.payload.get("document_id"),
                    "page": result.payload.get("page")
                }
            )

        return chunks

    def build_context(self, chunks: list[dict]) -> str:

        context = []

        for chunk in chunks:
            context.append(
                f"[Document {chunk['document_id']} - Page {chunk['page']}]\n"
                f"{chunk['text']}"
            )

        return "\n\n".join(context)