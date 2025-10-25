from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, UTC
import models, schemas
from database import get_db

router = APIRouter(prefix="/objects", tags=["objects"])


@router.post("/", response_model=schemas.Object)
def create_object(obj: schemas.ObjectCreate, user_id: int, db: Session = Depends(get_db)):
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db_object = models.Object(**obj.model_dump(), owner_id=user_id)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


@router.get("/", response_model=List[schemas.Object])
def get_objects(user_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(models.Object)
    if user_id:
        query = query.filter(models.Object.owner_id == user_id)
    objects = query.offset(skip).limit(limit).all()
    return objects


@router.get("/{object_id}", response_model=schemas.Object)
def get_object(object_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Object).filter(models.Object.id == object_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    return obj


@router.put("/{object_id}", response_model=schemas.Object)
def update_object(object_id: int, obj_update: schemas.ObjectCreate, db: Session = Depends(get_db)):
    db_object = db.query(models.Object).filter(models.Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    for key, value in obj_update.model_dump().items():
        setattr(db_object, key, value)
    
    db.commit()
    db.refresh(db_object)
    return db_object


@router.delete("/{object_id}")
def delete_object(object_id: int, db: Session = Depends(get_db)):
    db_object = db.query(models.Object).filter(models.Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    db.delete(db_object)
    db.commit()
    return {"message": "Objet supprimé avec succès"}


# ====== ENDPOINTS POUR LES DEMANDES D'OBJETS ======

@router.post("/requests", response_model=schemas.ObjectRequestResponse)
def create_object_request(obj_request: schemas.ObjectRequestCreate, user_id: int, db: Session = Depends(get_db)):
    """Créer une demande d'objet par un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier que le parent existe s'il est spécifié
    if obj_request.parent_id:
        parent_obj = db.query(models.Object).filter(models.Object.id == obj_request.parent_id).first()
        if not parent_obj:
            raise HTTPException(status_code=404, detail="Parent object not found")
    
    db_request = models.ObjectRequest(**obj_request.model_dump(), requester_id=user_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("/requests", response_model=List[schemas.ObjectRequestResponse])
def get_object_requests(status: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer toutes les demandes d'objets (pour admin)"""
    query = db.query(models.ObjectRequest)
    if status:
        query = query.filter(models.ObjectRequest.status == status)
    requests = query.offset(skip).limit(limit).all()
    return requests


@router.get("/requests/{request_id}", response_model=schemas.ObjectRequestResponse)
def get_object_request(request_id: int, db: Session = Depends(get_db)):
    """Récupérer une demande d'objet spécifique"""
    request_obj = db.query(models.ObjectRequest).filter(models.ObjectRequest.id == request_id).first()
    if not request_obj:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    return request_obj


# ====== ENDPOINTS ADMIN POUR GÉRER LES DEMANDES ======

@router.put("/requests/{request_id}/decide", response_model=schemas.ObjectRequestResponse)
def admin_decide_object_request(
    request_id: int, 
    decision: schemas.ObjectRequestDecision, 
    admin_id: int,  # Temporairement passé en paramètre, plus tard via JWT
    db: Session = Depends(get_db)
):
    """Approuver ou rejeter une demande d'objet (admin uniquement)"""
    try:
        # Vérifier que l'admin existe et a le bon rôle
        admin = db.query(models.User).filter(models.User.id == admin_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Administrateur non trouvé")
        if admin.role != models.UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
        
        # Récupérer la demande
        request_obj = db.query(models.ObjectRequest).filter(models.ObjectRequest.id == request_id).first()
        if not request_obj:
            raise HTTPException(status_code=404, detail="Demande non trouvée")
        
        if request_obj.status != models.ObjectRequestStatus.PENDING:
            raise HTTPException(status_code=400, detail="Cette demande a déjà été traitée")
        
        # Mettre à jour le statut
        request_obj.status = decision.status
        request_obj.admin_notes = decision.admin_notes
        request_obj.reviewed_by = admin_id
        request_obj.reviewed_at = datetime.now(UTC)
        
        # Si approuvée, créer l'objet dans la base
        if decision.status == models.ObjectRequestStatus.APPROVED:
            new_object = models.Object(
                name=request_obj.name,
                category=request_obj.category,
                brand=request_obj.brand,
                model=request_obj.model,
                purchase_date=request_obj.purchase_date,
                manual_url=request_obj.manual_url,
                notes=request_obj.notes,
                owner_id=request_obj.requester_id,
                parent_id=request_obj.parent_id,
                status="active"  # Statut actif par défaut
            )
            db.add(new_object)
        
        db.commit()
        db.refresh(request_obj)
        return request_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la décision admin: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
    return request_obj


@router.get("/admin/pending-requests", response_model=List[schemas.ObjectRequestResponse])
def get_pending_requests(admin_id: int, db: Session = Depends(get_db)):
    """Récupérer toutes les demandes en attente (admin uniquement)"""
    # Vérifier que l'utilisateur est admin
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin or admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    requests = db.query(models.ObjectRequest).filter(
        models.ObjectRequest.status == models.ObjectRequestStatus.PENDING
    ).all()
    return requests


@router.delete("/admin/requests/{request_id}")
def admin_delete_request(request_id: int, admin_id: int, db: Session = Depends(get_db)):
    """Supprimer une demande d'objet (admin uniquement)"""
    # Vérifier que l'utilisateur est admin
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin or admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    request_obj = db.query(models.ObjectRequest).filter(models.ObjectRequest.id == request_id).first()
    if not request_obj:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    
    db.delete(request_obj)
    db.commit()
    return {"message": "Demande supprimée avec succès"}
