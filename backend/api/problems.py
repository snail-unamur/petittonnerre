from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, UTC
from database import get_db
import models
import schemas

router = APIRouter(prefix="/problems", tags=["problems"])


@router.post("/", response_model=schemas.Problem, status_code=status.HTTP_201_CREATED)
def create_problem(
    problem: schemas.ProblemCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Créer un nouveau problème pour un objet"""
    # Vérifier que l'objet existe
    obj = db.query(models.Object).filter(models.Object.id == problem.object_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objet non trouvé"
        )
    
    # Vérifier que l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Créer le problème
    db_problem = models.Problem(
        **problem.model_dump(),
        reported_by=user_id
    )
    
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    return db_problem


@router.get("/", response_model=List[schemas.Problem])
def get_problems(
    object_id: Optional[int] = None,
    category: Optional[models.ProblemCategory] = None,
    status: Optional[models.ProblemStatus] = None,
    severity: Optional[models.ProblemSeverity] = None,
    user_id: Optional[int] = None,
    my_problems: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des problèmes avec filtres optionnels
    
    Args:
        my_problems: Si True et user_id fourni, ne retourne que les problèmes signalés par cet utilisateur
        user_id: ID de l'utilisateur (requis si my_problems=True)
    """
    query = db.query(models.Problem).filter(models.Problem.deleted_at == None)
    
    if object_id:
        query = query.filter(models.Problem.object_id == object_id)
    
    if category:
        query = query.filter(models.Problem.category == category)
    
    if status:
        query = query.filter(models.Problem.status == status)
    
    if severity:
        query = query.filter(models.Problem.severity == severity)
    
    # Filtre "mes problèmes" - ne retourne que ceux signalés par l'utilisateur
    if my_problems and user_id:
        query = query.filter(models.Problem.reported_by == user_id)
    
    problems = query.order_by(models.Problem.created_at.desc()).offset(skip).limit(limit).all()
    return problems


@router.get("/{problem_id}", response_model=schemas.Problem)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    """Récupérer un problème spécifique par son ID"""
    problem = db.query(models.Problem).filter(
        models.Problem.id == problem_id,
        models.Problem.deleted_at == None
    ).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    return problem


@router.patch("/{problem_id}", response_model=schemas.Problem)
def update_problem(
    problem_id: int,
    problem_update: schemas.ProblemUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un problème existant"""
    db_problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if not db_problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = problem_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_problem, key, value)
    
    db.commit()
    db.refresh(db_problem)
    
    return db_problem


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    """Supprimer un problème"""
    db_problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if not db_problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    db.delete(db_problem)
    db.commit()
    
    return None


# Routes pour les résolutions de problèmes
@router.post("/{problem_id}/resolutions", response_model=schemas.ProblemResolution, status_code=status.HTTP_201_CREATED)
def create_resolution(
    problem_id: int,
    resolution: schemas.ProblemResolutionBase,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Ajouter une résolution à un problème"""
    # Vérifier que le problème existe
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    # Si c'est la première résolution et que le problème est "open", passer en "in_progress"
    if problem.status == models.ProblemStatus.OPEN:
        problem.status = models.ProblemStatus.IN_PROGRESS
    
    # Créer la résolution
    db_resolution = models.ProblemResolution(
        **resolution.model_dump(),
        problem_id=problem_id,
        resolved_by=user_id
    )
    
    db.add(db_resolution)
    db.commit()
    db.refresh(db_resolution)
    
    return db_resolution


@router.get("/{problem_id}/resolutions", response_model=List[schemas.ProblemResolution])
def get_resolutions(
    problem_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer toutes les résolutions d'un problème (non supprimées)"""
    # Vérifier que le problème existe
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    resolutions = db.query(models.ProblemResolution)\
        .filter(
            models.ProblemResolution.problem_id == problem_id,
            models.ProblemResolution.deleted_at == None
        )\
        .order_by(models.ProblemResolution.helpfulness_score.desc())\
        .offset(skip).limit(limit).all()
    
    return resolutions


@router.patch("/resolutions/{resolution_id}", response_model=schemas.ProblemResolution)
def update_resolution(
    resolution_id: int,
    resolution_update: schemas.ProblemResolutionUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une résolution"""
    db_resolution = db.query(models.ProblemResolution)\
        .filter(models.ProblemResolution.id == resolution_id).first()
    
    if not db_resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Résolution non trouvée"
        )
    
    # Mettre à jour uniquement les champs fournis
    update_data = resolution_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_resolution, key, value)
    
    db.commit()
    db.refresh(db_resolution)
    
    return db_resolution


@router.post("/resolutions/{resolution_id}/upvote")
def upvote_resolution(resolution_id: int, db: Session = Depends(get_db)):
    """Voter pour l'utilité d'une résolution"""
    resolution = db.query(models.ProblemResolution)\
        .filter(models.ProblemResolution.id == resolution_id).first()
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Résolution non trouvée"
        )
    
    resolution.helpfulness_score += 1
    db.commit()
    db.refresh(resolution)
    
    return {"helpfulness_score": resolution.helpfulness_score}


@router.post("/resolutions/{resolution_id}/mark-successful")
def mark_resolution_successful(
    resolution_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Marquer une résolution comme ayant résolu le problème"""
    resolution = db.query(models.ProblemResolution)\
        .filter(models.ProblemResolution.id == resolution_id).first()
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Résolution non trouvée"
        )
    
    # Récupérer le problème associé
    problem = db.query(models.Problem)\
        .filter(models.Problem.id == resolution.problem_id).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème associé non trouvé"
        )
    
    # Marquer la résolution comme réussie
    resolution.was_successful = True
    
    # Changer le statut du problème en "resolved"
    problem.status = models.ProblemStatus.RESOLVED
    
    db.commit()
    db.refresh(resolution)
    db.refresh(problem)
    
    return {
        "message": "Résolution marquée comme réussie",
        "resolution_id": resolution.id,
        "problem_id": problem.id,
        "problem_status": problem.status
    }


@router.post("/{problem_id}/close")
def close_problem(
    problem_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Fermer définitivement un problème (seulement le créateur)"""
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    # Vérifier que c'est bien le créateur
    if problem.reported_by != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le créateur du problème peut le fermer"
        )
    
    # Empêcher de fermer un problème déjà fermé
    if problem.status == models.ProblemStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le problème est déjà fermé"
        )
    
    problem.status = models.ProblemStatus.CLOSED
    db.commit()
    db.refresh(problem)
    
    return {
        "message": "Problème fermé avec succès",
        "problem_id": problem.id,
        "problem_status": problem.status
    }


@router.post("/{problem_id}/reopen")
def reopen_problem(
    problem_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Rouvrir un problème résolu (seulement le créateur)"""
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    # Vérifier que c'est bien le créateur
    if problem.reported_by != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul le créateur du problème peut le rouvrir"
        )
    
    # On peut rouvrir seulement si resolved ou closed
    if problem.status not in [models.ProblemStatus.RESOLVED, models.ProblemStatus.CLOSED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les problèmes résolus ou fermés peuvent être rouverts"
        )
    
    problem.status = models.ProblemStatus.OPEN
    db.commit()
    db.refresh(problem)
    
    return {
        "message": "Problème rouvert avec succès",
        "problem_id": problem.id,
        "problem_status": problem.status
    }


# ====== ENDPOINTS ADMIN ======

@router.delete("/admin/{problem_id}", status_code=status.HTTP_200_OK)
def admin_soft_delete_problem(
    problem_id: int,
    admin_id: int,
    db: Session = Depends(get_db)
):
    """Soft delete d'un problème (admin uniquement)"""
    # Vérifier que l'admin existe et a le bon rôle
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    if admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    # Récupérer le problème (même s'il est déjà supprimé)
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    # Si déjà supprimé, empêcher une nouvelle suppression
    if problem.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le problème est déjà supprimé"
        )
    
    # Soft delete : mettre la date de suppression
    problem.deleted_at = datetime.now(UTC)
    db.commit()
    db.refresh(problem)
    
    return {
        "message": "Problème supprimé avec succès",
        "problem_id": problem.id,
        "deleted_at": problem.deleted_at
    }


@router.get("/admin/deleted", response_model=List[schemas.Problem])
def admin_get_deleted_problems(
    admin_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer tous les problèmes supprimés (admin uniquement)"""
    # Vérifier que l'admin existe et a le bon rôle
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    if admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    # Récupérer uniquement les problèmes supprimés
    problems = db.query(models.Problem)\
        .filter(models.Problem.deleted_at != None)\
        .order_by(models.Problem.deleted_at.desc())\
        .offset(skip).limit(limit).all()
    
    return problems


@router.post("/admin/{problem_id}/restore", status_code=status.HTTP_200_OK)
def admin_restore_problem(
    problem_id: int,
    admin_id: int,
    db: Session = Depends(get_db)
):
    """Restaurer un problème supprimé (admin uniquement)"""
    # Vérifier que l'admin existe et a le bon rôle
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    if admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    # Récupérer le problème supprimé
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problème non trouvé"
        )
    
    # Vérifier qu'il est bien supprimé
    if problem.deleted_at is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le problème n'est pas supprimé"
        )
    
    # Restaurer : retirer la date de suppression
    problem.deleted_at = None
    db.commit()
    db.refresh(problem)
    
    return {
        "message": "Problème restauré avec succès",
        "problem_id": problem.id
    }


# ====== ENDPOINTS ADMIN RESOLUTIONS ======

@router.delete("/admin/resolutions/{resolution_id}", status_code=status.HTTP_200_OK)
def admin_soft_delete_resolution(
    resolution_id: int,
    admin_id: int,
    db: Session = Depends(get_db)
):
    """Soft delete d'une résolution (admin uniquement)"""
    # Vérifier que l'admin existe et a le bon rôle
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    if admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    # Récupérer la résolution
    resolution = db.query(models.ProblemResolution).filter(
        models.ProblemResolution.id == resolution_id
    ).first()
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Résolution non trouvée"
        )
    
    # Vérifier qu'elle n'est pas déjà supprimée
    if resolution.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La résolution est déjà supprimée"
        )
    
    # Soft delete : marquer avec la date actuelle
    resolution.deleted_at = datetime.now(UTC)
    db.commit()
    db.refresh(resolution)
    
    return {
        "message": "Résolution supprimée avec succès",
        "resolution_id": resolution.id,
        "deleted_at": resolution.deleted_at.isoformat()
    }


@router.get("/admin/resolutions/deleted", response_model=List[schemas.ProblemResolution])
def admin_get_deleted_resolutions(
    admin_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lister toutes les résolutions supprimées (admin uniquement)"""
    # Vérifier que l'admin existe et a le bon rôle
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    if admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    # Récupérer uniquement les résolutions supprimées
    resolutions = db.query(models.ProblemResolution)\
        .filter(models.ProblemResolution.deleted_at != None)\
        .order_by(models.ProblemResolution.deleted_at.desc())\
        .offset(skip).limit(limit).all()
    
    return resolutions


@router.post("/admin/resolutions/{resolution_id}/restore", status_code=status.HTTP_200_OK)
def admin_restore_resolution(
    resolution_id: int,
    admin_id: int,
    db: Session = Depends(get_db)
):
    """Restaurer une résolution supprimée (admin uniquement)"""
    # Vérifier que l'admin existe et a le bon rôle
    admin = db.query(models.User).filter(models.User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Administrateur non trouvé")
    if admin.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    # Récupérer la résolution supprimée
    resolution = db.query(models.ProblemResolution).filter(
        models.ProblemResolution.id == resolution_id
    ).first()
    
    if not resolution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Résolution non trouvée"
        )
    
    # Vérifier qu'elle est bien supprimée
    if resolution.deleted_at is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La résolution n'est pas supprimée"
        )
    
    # Restaurer : retirer la date de suppression
    resolution.deleted_at = None
    db.commit()
    db.refresh(resolution)
    
    return {
        "message": "Résolution restaurée avec succès",
        "resolution_id": resolution.id
    }
