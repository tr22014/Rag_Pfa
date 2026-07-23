from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.config import settings

class AuthService:

    # ----------------------------  
    # Configuration JWT
    # ----------------------------

    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )

    # ----------------------------
    # Hash Password
    # ----------------------------

    @classmethod
    def hash_password(cls, password: str) -> str:

        return cls.pwd_context.hash(password)

    # ----------------------------
    # Verify Password
    # ----------------------------

    @classmethod
    def verify_password(
        cls,
        plain_password: str,
        hashed_password: str
    ) -> bool:

        return cls.pwd_context.verify(
            plain_password,
            hashed_password
        )

    # ----------------------------
    # Register User
    # ----------------------------

    @classmethod
    def register(
        cls,
        db: Session,
        user: UserCreate
    ) -> User:

        existing_user = UserService.get_user_by_email(
            db,
            user.email
        )

        if existing_user:
            raise ValueError("Email already exists")

        hashed_password = cls.hash_password(
            user.password
        )

        return UserService.create_user(
            db=db,
            user=user,
            hashed_password=hashed_password
        )



    @classmethod
    def authenticate_user(
        cls,
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:

        user = UserService.get_user_by_email(
            db,
            email
        )

        if not user:
            return None

        if not cls.verify_password(
            password,
            user.hashed_password
        ):
            return None

        if not user.is_active:
            return None

        return user

    # ----------------------------
    # Create JWT Token
    # ----------------------------

    @classmethod
    def create_access_token(
        cls,
        user: User
    ) -> str:

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "exp": expire
        }

        return jwt.encode(
            payload,
            cls.SECRET_KEY,
            algorithm=cls.ALGORITHM
        )

    # ----------------------------
    # Decode JWT
    # ----------------------------

    @classmethod
    def decode_token(
        cls,
        token: str
    ) -> dict:

        try:

            payload = jwt.decode(
                token,
                cls.SECRET_KEY,
                algorithms=[cls.ALGORITHM]
            )

            return payload

        except JWTError:

            raise ValueError("Invalid token")