import os
import shutil
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from database.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentOut, DocumentUpdate
from app.services.document_service import DocumentService
from app.tasks.ingestion_tasks import ingest_document
from app.core.config import settings

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = settings.upload_dir
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/upload",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED
)
def upload_document(
    file: UploadFile = File(...),
    collection_id: int | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Format non supporté : {ext}"
        )

    stored_filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, stored_filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = DocumentService.create_document(
        db=db,
        filename=file.filename,
        filepath=filepath,
        file_type=ext.lstrip("."),
        uploaded_by_id=current_user.id,
        collection_id=collection_id,
    )

    # Envoie le document dans la file Celery
    ingest_document.delay(document.id)

    return document


@router.get(
    "/",
    response_model=list[DocumentOut],
    summary="Lister les documents"
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value == "admin":
        return DocumentService.list_documents(db)

    return DocumentService.list_documents_by_user(db, current_user.id)


@router.get(
    "/{document_id}",
    response_model=DocumentOut,
    summary="Afficher un document"
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentService.get_document(db, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document introuvable"
        )

    if (
        current_user.role.value != "admin"
        and document.uploaded_by_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )

    return document


@router.put(
    "/{document_id}",
    response_model=DocumentOut,
    summary="Modifier un document"
)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentService.get_document(db, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document introuvable"
        )

    if (
        current_user.role.value != "admin"
        and document.uploaded_by_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )

    return DocumentService.update_document(db, document, document_update)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un document"
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = DocumentService.get_document(db, document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document introuvable"
        )

    if (
        current_user.role.value != "admin"
        and document.uploaded_by_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )

    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    DocumentService.delete_document(db, document)

    return None