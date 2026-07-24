from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import RagService
from database.database import SessionLocal
from app.models.message import Message, MessageRole


router = APIRouter()

rag_service = RagService()  # chargé une seule fois au démarrage


class ChatRequest(BaseModel):
    conversation_id: int
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    db = SessionLocal()

    try:

        print("Question reçue :", request.question)
        print("Conversation ID :", request.conversation_id)


        # ==========================
        # 1. Récupérer l'historique
        # ==========================

        messages = (
            db.query(Message)
            .filter(
                Message.conversation_id == request.conversation_id
            )
            .order_by(Message.created_at)
            .all()
        )


        history = [
            {
                "role": message.role.value,
                "content": message.content
            }
            for message in messages
        ]


        # ==========================
        # 2. Sauvegarder question user
        # ==========================

        user_message = Message(
            conversation_id=request.conversation_id,
            role=MessageRole.user,
            content=request.question
        )

        db.add(user_message)
        db.commit()


        # ==========================
        # 3. Appeler le RAG avec mémoire
        # ==========================

        response = rag_service.ask(
            question=request.question,
            history=history
        )


        # ==========================
        # 4. Sauvegarder réponse IA
        # ==========================

        assistant_message = Message(
            conversation_id=request.conversation_id,
            role=MessageRole.assistant,
            content=response["answer"]
        )

        db.add(assistant_message)
        db.commit()


        return response


    finally:
        db.close()