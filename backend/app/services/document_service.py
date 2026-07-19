from datetime import datetime

from sqlalchemy.orm import Session

from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentUpdate


class DocumentService:

    @staticmethod
    def create_document(
        db: Session,
        filename: str,
        filepath: str,
        file_type: str | None,
        uploaded_by_id: int,
        collection_id: int | None = None,
    ) -> Document:
        """
        Enregistre les métadonnées d'un document après son upload.
        """

        db_document = Document(
            filename=filename,
            filepath=filepath,
            file_type=file_type,
            uploaded_by_id=uploaded_by_id,
            collection_id=collection_id,
            status=DocumentStatus.pending,
        )

        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        return db_document

    @staticmethod
    def get_document(
        db: Session,
        document_id: int
    ) -> Document | None:

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    @staticmethod
    def get_document_by_filename(
        db: Session,
        filename: str
    ) -> Document | None:

        return (
            db.query(Document)
            .filter(Document.filename == filename)
            .first()
        )

    @staticmethod
    def list_documents(
        db: Session
    ) -> list[Document]:

        return (
            db.query(Document)
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    @staticmethod
    def list_documents_by_user(
        db: Session,
        user_id: int
    ) -> list[Document]:

        return (
            db.query(Document)
            .filter(Document.uploaded_by_id == user_id)
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    @staticmethod
    def update_document(
        db: Session,
        document: Document,
        document_update: DocumentUpdate
    ) -> Document:

        if document_update.filename is not None:
            document.filename = document_update.filename

        if document_update.collection_id is not None:
            document.collection_id = document_update.collection_id

        if document_update.status is not None:
            document.status = document_update.status

        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def update_status(
        db: Session,
        document: Document,
        status: DocumentStatus
    ) -> Document:

        document.status = status

        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def update_chunk_count(
        db: Session,
        document: Document,
        chunk_count: int
    ) -> Document:

        document.chunk_count = chunk_count

        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def mark_as_indexed(
        db: Session,
        document: Document
    ) -> Document:

        document.status = DocumentStatus.indexed
        document.indexed_at = datetime.utcnow()

        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def delete_document(
        db: Session,
        document: Document
    ) -> None:

        db.delete(document)
        db.commit()

    @staticmethod
    def document_exists(
        db: Session,
        filename: str
    ) -> bool:

        return (
            db.query(Document)
            .filter(Document.filename == filename)
            .first()
            is not None
        )

    @staticmethod
    def count_documents(
        db: Session
    ) -> int:

        return db.query(Document).count()