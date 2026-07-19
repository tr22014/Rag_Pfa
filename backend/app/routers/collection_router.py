from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from app.core.dependencies import get_current_user, get_current_admin

from app.schemas.collection import CollectionCreate, CollectionUpdate, CollectionOut
from app.services.collection_service import CollectionService

router = APIRouter(
    prefix="/collections",
    tags=["Collections"]
)


@router.post("/", response_model=CollectionOut, status_code=status.HTTP_201_CREATED)
def create_collection(
    collection: CollectionCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return CollectionService.create_collection(db, collection)


@router.get("/", response_model=list[CollectionOut])
def list_collections(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return CollectionService.list_collections(db)


@router.get("/{collection_id}", response_model=CollectionOut)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    collection = CollectionService.get_collection(db, collection_id)

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection introuvable")

    return collection


@router.put("/{collection_id}", response_model=CollectionOut)
def update_collection(
    collection_id: int,
    collection_update: CollectionUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    collection = CollectionService.get_collection(db, collection_id)

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection introuvable")

    return CollectionService.update_collection(db, collection, collection_update)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    collection = CollectionService.get_collection(db, collection_id)

    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection introuvable")

    CollectionService.delete_collection(db, collection)
    return None