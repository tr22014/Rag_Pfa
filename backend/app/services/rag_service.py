from rag.retriever import Retriever
from app.services.generator import Generator


class RagService:

    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()


    def ask(
        self,
        question: str,
        history: list = None
    ):

        # ==========================
        # 1. Recherche RAG
        # ==========================

        chunks = self.retriever.retrieve(
            question
        )


        # Aucun résultat trouvé
        if not chunks:
            return {
                "question": question,
                "answer": "Je n'ai trouvé aucune information pertinente.",
                "sources": []
            }


        # ==========================
        # 2. Construire le contexte documentaire
        # ==========================

        context = self.retriever.build_context(
            chunks
        )


        # ==========================
        # 3. Génération avec historique
        # ==========================

        answer = self.generator.generate(
            question=question,
            context=context,
            history=history or []
        )


        # ==========================
        # 4. Sources
        # ==========================

        sources = []

        for chunk in chunks:

            sources.append(
                {
                    "document_id": chunk["document_id"],
                    "page": chunk["page"],
                    "score": round(
                        chunk.get("score", 0),
                        3
                    )
                }
            )


        # ==========================
        # 5. Réponse finale
        # ==========================

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }