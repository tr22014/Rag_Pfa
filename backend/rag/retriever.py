from qdrant_client.models import Filter

from database.qdrant import client, COLLECTION_NAME
from rag.embedder import create_embedding
from rag.keyword_search import keyword_search
from rag.reranker import rerank


class Retriever:

    def __init__(self):
        self.client = client
        self.collection = COLLECTION_NAME

    def retrieve(
        self,
        question: str,
        limit: int = 5,
        query_filter: Filter | None = None,
    ) -> list[dict]:

        # Nombre de candidats avant le re-ranking
        candidate_limit = max(limit * 5, 30)

        # ============================
        # Recherche vectorielle
        # ============================

        query_vector = create_embedding(question)

        vector_results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=candidate_limit,
            query_filter=query_filter,
        ).points

        vector_chunks = []

        for result in vector_results:

            vector_chunks.append(
                {
                    "chunk_id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "document_id": result.payload.get("document_id"),
                    "page": result.payload.get("page"),
                    "source": "vector",
                }
            )

        # ============================
        # Recherche lexicale (FTS)
        # ============================

        keyword_chunks = keyword_search(
            question,
            limit=candidate_limit,
        )

        for chunk in keyword_chunks:
            chunk["source"] = "keyword"

        # ============================
        # Fusion des résultats
        # ============================

        merged = {}

        for chunk in vector_chunks:

            merged[chunk["chunk_id"]] = chunk

        for chunk in keyword_chunks:

            chunk_id = chunk["chunk_id"]

            if chunk_id in merged:

                # Trouvé par les deux méthodes
                merged[chunk_id]["source"] = "hybrid"

            else:

                merged[chunk_id] = chunk

        candidates = list(merged.values())

        # ============================
        # Re-ranking
        # ============================

        ranked_chunks = rerank(
            question,
            candidates,
        )

        # ============================
        # Top K final
        # ============================

        return ranked_chunks[:limit]

    def build_context(
        self,
        chunks: list[dict],
    ) -> str:

        context = []

        for chunk in chunks:

            context.append(
                f"[Document {chunk['document_id']} - Page {chunk['page']}]\n"
                f"{chunk['text']}"
            )

        return "\n\n".join(context)