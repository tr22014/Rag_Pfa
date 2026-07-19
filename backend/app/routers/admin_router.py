from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from app.core.dependencies import get_current_admin

from app.services.user_service import UserService
from app.services.document_service import DocumentService
from app.services.conversation_service import ConversationService
from app.services.log_service import LogService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard", summary="Vue d'ensemble pour l'admin")
def dashboard(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return {
        "total_users": UserService.count_users(db),
        "total_documents": DocumentService.count_documents(db),
        "total_conversations": ConversationService.count_conversations(db),
        "total_logs": LogService.count_logs(db),
    }