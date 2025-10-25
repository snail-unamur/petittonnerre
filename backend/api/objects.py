from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, UTC
import models, schemas
from database import get_db

router = APIRouter(prefix="/objects", tags=["objects"])


@router.post("/", response_model=schemas.Object)
def create_object(obj: schemas.ObjectCreate, user_id: int, db: Session = Depends(get_db)):
    """Créer un nouvel objet et l'associer à l'utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Créer l'objet avec created_by au lieu de owner_id
    db_object = models.Object(**obj.model_dump(), created_by=user_id)
    db.add(db_object)
    db.flush()  # Pour avoir l'ID de l'objet
    
    # Ajouter l'utilisateur comme propriétaire via la table d'association
    db_object.owners.append(user)
    
    db.commit()
    db.refresh(db_object)
    return db_object


@router.get("/", response_model=List[schemas.Object])
def get_objects(user_id: int = None, skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    """Récupérer les objets, filtrés par utilisateur si user_id fourni"""
    if user_id:
        # Récupérer seulement les objets de l'utilisateur via la relation many-to-many
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        if limit:
            objects = user.objects[skip:skip+limit]
        else:
            objects = user.objects[skip:]
        return objects
    else:
        # Récupérer tous les objets (pour admin)
        query = db.query(models.Object)
        if limit:
            objects = query.offset(skip).limit(limit).all()
        else:
            objects = query.offset(skip).all()
        return objects


@router.get("/search", response_model=List[schemas.Object])
def search_objects(
    name: str = "",
    category: str = "",
    brand: str = "",
    model: str = "",
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Rechercher des objets existants par critères"""
    query = db.query(models.Object)
    
    if name:
        query = query.filter(models.Object.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Object.category == category)
    if brand:
        query = query.filter(models.Object.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(models.Object.model.ilike(f"%{model}%"))
    
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
def delete_object(object_id: int, user_id: int, db: Session = Depends(get_db)):
    """Retirer un objet de la liste de l'utilisateur (sans supprimer l'objet de la BD)"""
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier que l'objet existe
    db_object = db.query(models.Object).filter(models.Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    # Vérifier que l'utilisateur est bien propriétaire
    if user not in db_object.owners:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas propriétaire de cet objet")
    
    # Retirer l'utilisateur de la liste des propriétaires
    db_object.owners.remove(user)
    db.commit()
    
    # Ne PAS supprimer l'objet de la BD même s'il n'a plus de propriétaires
    # Cela permet de le retrouver via la recherche et de le lier à nouveau
    if len(db_object.owners) == 0:
        return {"message": "Objet retiré de votre liste. L'objet reste disponible dans la base pour être lié à nouveau."}
    
    return {"message": "Objet retiré de votre liste avec succès"}


# ====== ENDPOINTS POUR LES OBJETS PARTAGÉS (MANY-TO-MANY) ======

@router.post("/link", response_model=schemas.Object)
def link_object_to_user(link_data: schemas.ObjectLink, user_id: int, db: Session = Depends(get_db)):
    """Lier un objet existant à un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier que l'objet existe
    obj = db.query(models.Object).filter(models.Object.id == link_data.object_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    # Vérifier si l'objet n'est pas déjà lié à l'utilisateur
    if user in obj.owners:
        raise HTTPException(status_code=400, detail="Cet objet est déjà lié à votre compte")
    
    # Ajouter l'utilisateur aux propriétaires
    obj.owners.append(user)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/unlink/{object_id}")
def unlink_object_from_user(object_id: int, user_id: int, db: Session = Depends(get_db)):
    """Délier un objet d'un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier que l'objet existe
    obj = db.query(models.Object).filter(models.Object.id == object_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    
    # Vérifier que l'objet est bien lié à l'utilisateur
    if user not in obj.owners:
        raise HTTPException(status_code=400, detail="Cet objet n'est pas lié à votre compte")
    
    # Empêcher de délier si c'est le seul propriétaire
    if len(obj.owners) <= 1:
        raise HTTPException(status_code=400, detail="Impossible de délier : vous êtes le seul propriétaire de cet objet")
    
    # Retirer l'utilisateur des propriétaires
    obj.owners.remove(user)
    db.commit()
    return {"message": "Objet délié avec succès"}


# ====== ENDPOINTS POUR LES DEMANDES D'OBJETS ======

@router.post("/requests", response_model=schemas.ObjectRequestResponse)
def create_object_request(obj_request: schemas.ObjectRequestCreate, user_id: int, db: Session = Depends(get_db)):
    """Créer une demande d'objet par un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
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
                created_by=request_obj.requester_id,
                status="active"  # Statut actif par défaut
            )
            db.add(new_object)
            db.flush()  # Pour avoir l'ID de l'objet
            
            # Ajouter le demandeur comme propriétaire
            requester = db.query(models.User).filter(models.User.id == request_obj.requester_id).first()
            if requester:
                new_object.owners.append(requester)
        
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
