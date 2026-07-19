from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def create_user(
        db: Session,
        user: UserCreate,
        hashed_password: str
    ) -> User:
    
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def get_user(
        db: Session,
        user_id: int
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ) -> User | None:


        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def list_users(
        db: Session
    ) -> list[User]:


        return (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    @staticmethod
    def update_user(
        db: Session,
        user: User,
        user_update: UserUpdate
    ) -> User:


        if user_update.full_name is not None:
            user.full_name = user_update.full_name

        if user_update.role is not None:
            user.role = user_update.role

        if user_update.is_active is not None:
            user.is_active = user_update.is_active

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(
        db: Session,
        user: User
    ) -> None:


        db.delete(user)
        db.commit()
    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        return (
        db.query(User)
        .filter(User.email == email)
        .first()
        is not None
    )

    @staticmethod
    def count_users(db: Session) -> int:
         return db.query(User).count()