from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================
# Inscription
# ==========================
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.register(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ==========================
# Connexion
# ==========================
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = AuthService.authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    access_token = AuthService.create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ==========================
# Utilisateur connecté
# ==========================
@router.get(
    "/me",
    response_model=UserOut
)
def me(
    current_user: User = Depends(get_current_user)
):
    return current_user