from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db

from app.core.dependencies import get_current_admin
from app.schemas.system_log import SystemLogOut
from app.services.log_service import LogService


router = APIRouter(
    prefix="/logs",
    tags=["System Logs"],
)


# ======================================================
# Liste de tous les logs
# ======================================================

@router.get(
    "/",
    response_model=list[SystemLogOut],
)
def list_logs(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Retourne tous les logs du système.
    """
    return LogService.list_logs(db)


# ======================================================
# Récupérer un log
# ======================================================

@router.get(
    "/{log_id}",
    response_model=SystemLogOut,
)
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Retourne un log par son ID.
    """

    log = LogService.get_log(db, log_id)

    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log introuvable."
        )

    return log


# ======================================================
# Logs d'un utilisateur
# ======================================================

@router.get(
    "/user/{user_id}",
    response_model=list[SystemLogOut],
)
def list_user_logs(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Retourne tous les logs d'un utilisateur.
    """

    return LogService.list_user_logs(
        db,
        user_id,
    )


# ======================================================
# Nombre total de logs
# ======================================================

@router.get("/count")
def count_logs(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Retourne le nombre total de logs.
    """

    return {
        "total_logs": LogService.count_logs(db)
    }


# ======================================================
# Supprimer un log
# ======================================================

@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Supprime un log.
    """

    log = LogService.get_log(
        db,
        log_id,
    )

    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log introuvable."
        )

    LogService.delete_log(
        db,
        log,
    )

    return None