from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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
