from sqlalchemy.orm import Session

from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate


class CollectionService:

    @staticmethod
    def create_collection(db: Session, collection: CollectionCreate) -> Collection:
        db_collection = Collection(
            name=collection.name,
            description=collection.description,
        )
        db.add(db_collection)
        db.commit()
        db.refresh(db_collection)
        return db_collection

    @staticmethod
    def get_collection(db: Session, collection_id: int) -> Collection | None:
        return db.query(Collection).filter(Collection.id == collection_id).first()

    @staticmethod
    def list_collections(db: Session) -> list[Collection]:
        return db.query(Collection).order_by(Collection.created_at.desc()).all()

    @staticmethod
    def update_collection(
        db: Session, collection: Collection, collection_update: CollectionUpdate
    ) -> Collection:
        if collection_update.name is not None:
            collection.name = collection_update.name
        if collection_update.description is not None:
            collection.description = collection_update.description

        db.commit()
        db.refresh(collection)
        return collection

    @staticmethod
    def delete_collection(db: Session, collection: Collection) -> None:
        db.delete(collection)
        db.commit()