from sqlalchemy.orm import Session

from app.models.system_log import SystemLog


class LogService:

    @staticmethod
    def create_log(
        db: Session,
        action: str,
        detail: str | None = None,
        user_id: int | None = None,
    ) -> SystemLog:
        """
        Crée un nouveau log système.
        """

        db_log = SystemLog(
            action=action,
            detail=detail,
            user_id=user_id,
        )

        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        return db_log

    @staticmethod
    def get_log(
        db: Session,
        log_id: int
    ) -> SystemLog | None:
        """
        Retourne un log par son ID.
        """

        return (
            db.query(SystemLog)
            .filter(SystemLog.id == log_id)
            .first()
        )

    @staticmethod
    def list_logs(
        db: Session
    ) -> list[SystemLog]:
        """
        Retourne tous les logs.
        """

        return (
            db.query(SystemLog)
            .order_by(SystemLog.created_at.desc())
            .all()
        )

    @staticmethod
    def list_user_logs(
        db: Session,
        user_id: int
    ) -> list[SystemLog]:
        """
        Retourne tous les logs d'un utilisateur.
        """

        return (
            db.query(SystemLog)
            .filter(SystemLog.user_id == user_id)
            .order_by(SystemLog.created_at.desc())
            .all()
        )

    @staticmethod
    def delete_log(
        db: Session,
        log: SystemLog
    ) -> None:
        """
        Supprime un log.
        """

        db.delete(log)
        db.commit()

    @staticmethod
    def count_logs(
        db: Session
    ) -> int:
        """
        Retourne le nombre total de logs.
        """

        return db.query(SystemLog).count()