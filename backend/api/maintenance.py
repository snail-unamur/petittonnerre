from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


# Routes pour les conseils d'entretien
@router.post("/advice", response_model=schemas.MaintenanceAdvice)
def create_maintenance_advice(advice: schemas.MaintenanceAdviceCreate, db: Session = Depends(get_db)):
    db_advice = models.MaintenanceAdvice(**advice.model_dump())
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice


@router.get("/advice", response_model=List[schemas.MaintenanceAdvice])
def get_maintenance_advice(
    category: models.ObjectCategory = None,
    validated_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.MaintenanceAdvice)
    if category:
        query = query.filter(models.MaintenanceAdvice.category == category)
    if validated_only:
        query = query.filter(models.MaintenanceAdvice.is_validated == True)
    advice_list = query.offset(skip).limit(limit).all()
    return advice_list


@router.get("/advice/{advice_id}", response_model=schemas.MaintenanceAdvice)
def get_advice(advice_id: int, db: Session = Depends(get_db)):
    advice = db.query(models.MaintenanceAdvice).filter(models.MaintenanceAdvice.id == advice_id).first()
    if not advice:
        raise HTTPException(status_code=404, detail="Conseil non trouvé")
    return advice


# Routes pour les tâches de maintenance
@router.post("/tasks", response_model=schemas.MaintenanceTask)
def create_maintenance_task(task: schemas.MaintenanceTaskCreate, user_id: int, db: Session = Depends(get_db)):
    # Vérifier que l'objet et le conseil existent
    obj = db.query(models.Object).filter(models.Object.id == task.object_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    advice = db.query(models.MaintenanceAdvice).filter(models.MaintenanceAdvice.id == task.advice_id).first()
    if not advice:
        raise HTTPException(status_code=404, detail="Conseil non trouvé")
    
    db_task = models.MaintenanceTask(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=List[schemas.MaintenanceTask])
def get_maintenance_tasks(
    user_id: int = None,
    object_id: int = None,
    status: models.MaintenanceStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.MaintenanceTask)
    if user_id:
        query = query.filter(models.MaintenanceTask.user_id == user_id)
    if object_id:
        query = query.filter(models.MaintenanceTask.object_id == object_id)
    if status:
        query = query.filter(models.MaintenanceTask.status == status)
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=schemas.MaintenanceTask)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.MaintenanceTask).filter(models.MaintenanceTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task


@router.patch("/tasks/{task_id}", response_model=schemas.MaintenanceTask)
def update_maintenance_task(
    task_id: int,
    task_update: schemas.MaintenanceTaskUpdate,
    db: Session = Depends(get_db)
):
    db_task = db.query(models.MaintenanceTask).filter(models.MaintenanceTask.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task
