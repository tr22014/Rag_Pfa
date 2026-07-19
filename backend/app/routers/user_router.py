from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from app.core.dependencies import get_current_user, get_current_admin

from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ==========================
# Profil de l'utilisateur connecté
# ==========================

@router.get("/profile",response_model=UserOut,summary="Afficher mon profil")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# ==========================
# Modifier son profil
# ==========================

@router.put(
    "/profile",
    response_model=UserOut, 
    summary="Modifier mon profil"
)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    updated_user = UserService.update_user(
        db=db,
        user=current_user,
        user_update=user_update
    )

    return updated_user


# ==========================
# Liste des utilisateurs (Admin)
# ==========================

@router.get(
    "/",
    response_model=list[UserOut],
    summary="Lister tous les utilisateurs"
)
def list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    return UserService.list_users(db)


# ==========================
# Obtenir un utilisateur par ID (Admin)
# ==========================

@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Afficher un utilisateur"
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    user = UserService.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )

    return user


# ==========================
# Modifier un utilisateur (Admin)
# ==========================

@router.put(
    "/{user_id}",
    response_model=UserOut,
    summary="Modifier un utilisateur"
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    user = UserService.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )

    return UserService.update_user(
        db=db,
        user=user,
        user_update=user_update
    )


# ==========================
# Supprimer un utilisateur (Admin)
# ==========================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un utilisateur"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    user = UserService.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )

    UserService.delete_user(
        db=db,
        user=user
    )

    return None