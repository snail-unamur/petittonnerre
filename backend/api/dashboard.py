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
    
    # Import de la table d'association
    from models import user_objects
    
    # Nombre total d'objets de l'utilisateur (via user_objects)
    total_objects = db.query(func.count(user_objects.c.object_id)).filter(
        user_objects.c.user_id == user_id
    ).scalar()
    
    # Nombre de tâches de maintenance en attente (via user_id)
    pending_tasks = db.query(func.count(models.MaintenanceTask.id)).filter(
        models.MaintenanceTask.user_id == user_id,
        models.MaintenanceTask.status == models.MaintenanceStatus.PENDING
    ).scalar()
    
    # Nombre de tâches terminées (via user_id)
    completed_tasks = db.query(func.count(models.MaintenanceTask.id)).filter(
        models.MaintenanceTask.user_id == user_id,
        models.MaintenanceTask.status == models.MaintenanceStatus.COMPLETED
    ).scalar()
    
    # Nombre de problèmes ouverts (signalés par l'utilisateur via reported_by)
    open_problems = db.query(func.count(models.Problem.id)).filter(
        models.Problem.reported_by == user_id,
        models.Problem.status == models.ProblemStatus.OPEN
    ).scalar()
    
    # Nombre de problèmes résolus (signalés par l'utilisateur via reported_by)
    resolved_problems = db.query(func.count(models.Problem.id)).filter(
        models.Problem.reported_by == user_id,
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
