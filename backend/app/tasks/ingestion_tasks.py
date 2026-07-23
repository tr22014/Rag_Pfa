from app.core.celery_app import celery_app

from database.database import SessionLocal

from app.services.document_service import DocumentService
from app.services.ingestion_service import run_ingestion_pipeline


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def ingest_document(self, document_id: int):

    db = SessionLocal()

    try:

        document = DocumentService.get_document(db, document_id)

        if document is None:
            return

        run_ingestion_pipeline(db, document)

    finally:
        db.close()