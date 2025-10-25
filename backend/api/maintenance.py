from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from icalendar import Calendar, Event
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


@router.get("/export/ical")
def export_maintenance_to_ical(user_id: int, db: Session = Depends(get_db)):
    """
    Exporte toutes les maintenances d'un utilisateur au format iCalendar (.ics)
    """
    # Récupérer toutes les tâches de maintenance de l'utilisateur
    tasks = db.query(models.MaintenanceTask).filter(
        models.MaintenanceTask.user_id == user_id
    ).all()
    
    if not tasks:
        raise HTTPException(status_code=404, detail="Aucune maintenance trouvée pour cet utilisateur")
    
    # Créer le calendrier
    cal = Calendar()
    cal.add('prodid', '-//Petit Tonnerre//Maintenance Calendar//FR')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Maintenances Petit Tonnerre')
    cal.add('x-wr-timezone', 'Europe/Brussels')
    cal.add('x-wr-caldesc', 'Calendrier des maintenances de vos objets')
    
    # Ajouter chaque tâche comme événement
    for task in tasks:
        # Récupérer les infos de l'objet et du conseil
        obj = db.query(models.Object).filter(models.Object.id == task.object_id).first()
        advice = db.query(models.MaintenanceAdvice).filter(models.MaintenanceAdvice.id == task.advice_id).first()
        
        if not obj or not advice:
            continue
        
        event = Event()
        
        # Informations de base
        event.add('uid', f'maintenance-{task.id}@petit-tonnerre.app')
        
        # Utiliser le nom de la tâche personnalisé s'il existe, sinon le titre du conseil
        if task.name:
            event.add('summary', f'🔧 {task.name}')
        else:
            event.add('summary', f'🔧 {advice.title} - {obj.name}')
        
        # Description détaillée
        description_parts = [
            f"Objet: {obj.name}",
            f"Catégorie: {obj.category.value}",
        ]
        if obj.brand:
            description_parts.append(f"Marque: {obj.brand}")
        if obj.model:
            description_parts.append(f"Modèle: {obj.model}")
        
        # Ajouter les conseils seulement si la tâche est basée sur un conseil (et pas une tâche libre)
        if advice and advice.description and not task.name:
            description_parts.append(f"\nConseils d'entretien:\n{advice.description}")
        
        if task.notes:
            description_parts.append(f"\nNotes:\n{task.notes}")
        
        if task.status == models.MaintenanceStatus.COMPLETED:
            description_parts.append(f"\n✅ Complété le {task.completed_date.strftime('%d/%m/%Y')}")
            if task.was_successful is not None:
                status_text = "Succès" if task.was_successful else "Échec"
                description_parts.append(f"Statut: {status_text}")
            if task.issues_encountered:
                description_parts.append(f"Problèmes rencontrés: {task.issues_encountered}")
        
        event.add('description', '\n'.join(description_parts))
        
        # Dates
        event.add('dtstart', task.scheduled_date)
        # Durée estimée: 1h pour une maintenance
        event.add('dtend', task.scheduled_date + timedelta(hours=1))
        event.add('dtstamp', datetime.utcnow())
        
        # Statut
        if task.status == models.MaintenanceStatus.COMPLETED:
            event.add('status', 'COMPLETED')
        elif task.status == models.MaintenanceStatus.PENDING:
            event.add('status', 'TENTATIVE')
        else:
            event.add('status', 'CONFIRMED')
        
        # Catégorie et priorité
        event.add('categories', [obj.category.value, 'Maintenance'])
        
        # Alarme/rappel (24h avant)
        if task.status == models.MaintenanceStatus.PENDING:
            from icalendar import Alarm
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            # Utiliser le nom de la tâche pour le rappel
            task_title = task.name if task.name else advice.title
            alarm.add('description', f'Rappel: {task_title} pour {obj.name}')
            alarm.add('trigger', timedelta(hours=-24))
            event.add_component(alarm)
        
        # Récurrence si le conseil a une fréquence
        if advice.frequency_days and task.status != models.MaintenanceStatus.COMPLETED:
            from icalendar import vRecur
            # Récurrence tous les X jours, jusqu'à 2 ans dans le futur
            event.add('rrule', vRecur(
                FREQ='DAILY',
                INTERVAL=advice.frequency_days,
                UNTIL=datetime.now() + timedelta(days=730)
            ))
        
        cal.add_component(event)
    
    # Générer le contenu iCalendar
    ical_content = cal.to_ical()
    
    # Retourner le fichier avec les bons headers
    return Response(
        content=ical_content,
        media_type='text/calendar',
        headers={
            'Content-Disposition': f'attachment; filename="maintenances-petit-tonnerre-{user_id}.ics"'
        }
    )

