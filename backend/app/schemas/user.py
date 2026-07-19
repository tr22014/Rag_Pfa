from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import RoleEnum


# Ce que le client ENVOIE pour créer un compte
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


# Ce que le client ENVOIE pour se connecter
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Ce que l'API RENVOIE (jamais le mot de passe !)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    role: RoleEnum
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Pour permettre à un admin de modifier un rôle ou statut
class UserUpdate(BaseModel):
    full_name: str | None = None
    role: RoleEnum | None = None
    is_active: bool | None = None