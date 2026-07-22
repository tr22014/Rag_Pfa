from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import RagService

router = APIRouter()

rag_service = RagService()  # chargé une seule fois au démarrage

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(request: ChatRequest):
    print("Question reçue :", request.question)
    return rag_service.ask(request.question)