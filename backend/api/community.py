from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/community", tags=["community"])


@router.post("/contributions", response_model=schemas.Contribution)
def create_contribution(
    contribution: schemas.ContributionCreate,
    author_id: int,
    db: Session = Depends(get_db)
):
    # Vérifier que l'auteur existe
    user = db.query(models.User).filter(models.User.id == author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db_contribution = models.Contribution(**contribution.model_dump(), author_id=author_id)
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution


@router.get("/contributions", response_model=List[schemas.Contribution])
def get_contributions(
    category: models.ObjectCategory = None,
    status: models.ContributionStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Contribution)
    if category:
        query = query.filter(models.Contribution.category == category)
    if status:
        query = query.filter(models.Contribution.status == status)
    
    contributions = query.order_by(models.Contribution.upvotes.desc()).offset(skip).limit(limit).all()
    return contributions


@router.get("/contributions/{contribution_id}", response_model=schemas.Contribution)
def get_contribution(contribution_id: int, db: Session = Depends(get_db)):
    contribution = db.query(models.Contribution).filter(models.Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution non trouvée")
    return contribution


@router.patch("/contributions/{contribution_id}", response_model=schemas.Contribution)
def update_contribution_status(
    contribution_id: int,
    contribution_update: schemas.ContributionUpdate,
    db: Session = Depends(get_db)
):
    db_contribution = db.query(models.Contribution).filter(models.Contribution.id == contribution_id).first()
    if not db_contribution:
        raise HTTPException(status_code=404, detail="Contribution non trouvée")
    
    if contribution_update.status:
        db_contribution.status = contribution_update.status
    
    db.commit()
    db.refresh(db_contribution)
    return db_contribution


@router.post("/contributions/{contribution_id}/upvote")
def upvote_contribution(contribution_id: int, db: Session = Depends(get_db)):
    contribution = db.query(models.Contribution).filter(models.Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution non trouvée")
    
    contribution.upvotes += 1
    db.commit()
    db.refresh(contribution)
    return {"upvotes": contribution.upvotes}
