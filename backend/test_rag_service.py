from app.services.rag_service import RagService

rag = RagService()
result = rag.ask("What is the Target Architecture?")
print(result["answer"])
print(result["sources"])