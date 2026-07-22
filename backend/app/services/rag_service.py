from app.services.retriever import Retriever
from app.services.generator import Generator


class RagService:

    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def ask(self, question: str):

        # 1. Recherche des chunks les plus pertinents
        chunks = self.retriever.retrieve(question)

        # Si aucun résultat
        if not chunks:
            return {
                "question": question,
                "answer": "Je n'ai trouvé aucune information pertinente.",
                "sources": []
            }

        # 2. Construire le contexte
        context = self.retriever.build_context(chunks)

        # 3. Générer la réponse avec Ollama
        answer = self.generator.generate(
            question=question,
            context=context
        )

        # 4. Préparer les sources
        sources = []

        for chunk in chunks:
            sources.append({
                "document_id": chunk["document_id"],
                "page": chunk["page"],
                "score": round(chunk["score"], 3)
            })

        # 5. Retourner la réponse complète
        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }