# backend/app/services/ingestion_service.py
import uuid

from sqlalchemy.orm import Session
from app.models.document import Document, DocumentStatus
from app.services.document_service import DocumentService
from rag.extractor import extract_pdf_pages, is_scanned_pdf, ExtractionError
from rag.chunker import chunk_pages
from rag.embedder import create_embedding
from database.qdrant import client, COLLECTION_NAME 
from qdrant_client.models import PointStruct


class IngestionError(Exception):
    pass


def run_ingestion_pipeline(db: Session, document: Document) -> None:
    """
    Pipeline complet : extraction -> chunking -> embeddings -> Qdrant.
    Appelé en tâche de fond après l'upload.
    """
    try:
        DocumentService.update_status(db, document, DocumentStatus.processing)

        # 1. Extraction (PDF pour l'instant)
        if document.file_type == "pdf":
            pages = extract_pdf_pages(document.filepath, document_id=document.id)
        else:
            raise IngestionError(f"Format non encore supporté: {document.file_type}")

        if is_scanned_pdf(pages):
            raise IngestionError("PDF scanné détecté — OCR non encore implémenté")

        # 2. Chunking
        chunks = chunk_pages(pages)
        if not chunks:
            raise IngestionError("Aucun chunk généré")

        # 3. Embeddings + upsert Qdrant (IDs uniques par document)
        points = []
        for chunk in chunks:
            vector = create_embedding(chunk["text"])
            point_id = str(uuid.uuid5(
                uuid.NAMESPACE_OID,
                f"{document.id}-{chunk['chunk_id']}"
            ))
            points.append(PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": chunk["text"],
                    "document_id": document.id,
                    "page": chunk["page_number"],
                }
            ))

        # Supprime les anciens points si on ré-indexe le même document
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector={"filter": {"must": [
                {"key": "document_id", "match": {"value": document.id}}
            ]}}
        )
        client.upsert(collection_name=COLLECTION_NAME, points=points)

        # 4. Mise à jour du statut en base
        DocumentService.update_chunk_count(db, document, len(chunks))
        DocumentService.mark_as_indexed(db, document)

    except (ExtractionError, IngestionError) as e:
        DocumentService.update_status(db, document, DocumentStatus.failed)
        print(f"[Ingestion] Échec document {document.id}: {e}")
    except Exception as e:
        DocumentService.update_status(db, document, DocumentStatus.failed)
        print(f"[Ingestion] Erreur inattendue document {document.id}: {e}")