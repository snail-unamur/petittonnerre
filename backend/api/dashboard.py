"""Routes pour les statistiques du dashboard"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
def get_dashboard_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les statistiques pour le dashboard de l'utilisateur"""
    
    # Nombre total d'objets de l'utilisateur
    total_objects = db.query(func.count(models.Object.id)).filter(
        models.Object.owner_id == user_id
    ).scalar()
    
    # Nombre de tâches de maintenance en attente
    pending_tasks = db.query(func.count(models.MaintenanceTask.id)).filter(
        models.MaintenanceTask.user_id == user_id,
        models.MaintenanceTask.status == models.MaintenanceStatus.PENDING
    ).scalar()
    
    # Nombre de tâches terminées
    completed_tasks = db.query(func.count(models.MaintenanceTask.id)).filter(
        models.MaintenanceTask.user_id == user_id,
        models.MaintenanceTask.status == models.MaintenanceStatus.COMPLETED
    ).scalar()
    
    # Nombre de problèmes ouverts
    open_problems = db.query(func.count(models.Problem.id)).join(
        models.Object, models.Problem.object_id == models.Object.id
    ).filter(
        models.Object.owner_id == user_id,
        models.Problem.status == models.ProblemStatus.OPEN
    ).scalar()
    
    # Nombre de problèmes résolus
    resolved_problems = db.query(func.count(models.Problem.id)).join(
        models.Object, models.Problem.object_id == models.Object.id
    ).filter(
        models.Object.owner_id == user_id,
        models.Problem.status == models.ProblemStatus.RESOLVED
    ).scalar()
    
    # Tâches à venir dans les 7 prochains jours
    from datetime import datetime, timedelta, UTC
    upcoming_tasks = db.query(func.count(models.MaintenanceTask.id)).filter(
        models.MaintenanceTask.user_id == user_id,
        models.MaintenanceTask.status == models.MaintenanceStatus.PENDING,
        models.MaintenanceTask.scheduled_date <= datetime.now(UTC) + timedelta(days=7),
        models.MaintenanceTask.scheduled_date >= datetime.now(UTC)
    ).scalar()
    
    return {
        "total_objects": total_objects or 0,
        "pending_tasks": pending_tasks or 0,
        "completed_tasks": completed_tasks or 0,
        "open_problems": open_problems or 0,
        "resolved_problems": resolved_problems or 0,
        "upcoming_tasks": upcoming_tasks or 0
    }
