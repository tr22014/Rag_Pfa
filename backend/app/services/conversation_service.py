from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
)


class ConversationService:

    @staticmethod
    def create_conversation(
        db: Session,
        conversation: ConversationCreate
    ) -> Conversation:
        """
        Créer une nouvelle conversation.
        """

        db_conversation = Conversation(
            title=conversation.title,
            user_id=conversation.user_id
        )

        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)

        return db_conversation

    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int
    ) -> Conversation | None:
        """
        Retourner une conversation par son ID.
        """

        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    @staticmethod
    def list_conversations(
        db: Session
    ) -> list[Conversation]:
        """
        Retourner toutes les conversations.
        """

        return (
            db.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .all()
        )

    @staticmethod
    def list_user_conversations(
        db: Session,
        user_id: int
    ) -> list[Conversation]:
        """
        Retourner toutes les conversations d'un utilisateur.
        """

        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

    @staticmethod
    def update_conversation(
        db: Session,
        conversation: Conversation,
        conversation_update: ConversationUpdate
    ) -> Conversation:
        """
        Modifier une conversation.
        """

        if conversation_update.title is not None:
            conversation.title = conversation_update.title

        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def delete_conversation(
        db: Session,
        conversation: Conversation
    ) -> None:
        """
        Supprimer une conversation.
        """

        db.delete(conversation)
        db.commit()

    @staticmethod
    def conversation_exists(
        db: Session,
        conversation_id: int
    ) -> bool:
        """
        Vérifier si une conversation existe.
        """

        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
            is not None
        )

    @staticmethod
    def count_conversations(
        db: Session
    ) -> int:
        """
        Retourner le nombre total de conversations.
        """

        return db.query(Conversation).count()