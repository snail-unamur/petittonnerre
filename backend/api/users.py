from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import User, UserRole, Object
import schemas  # Import the entire schemas module
from schemas import UserCreate, UserResponse
from database import get_db
from auth import get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["users"])

def validate_password(password: str) -> bool:
    """
    Validate that the password meets security requirements:
    - At least 6 characters
    """
    if len(password) < 6:
        return False
    return True

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )
    
    # Vérifier si le nom d'utilisateur existe déjà
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom d'utilisateur est déjà pris"
        )
    
    # Valider le mot de passe
    if not validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le mot de passe doit contenir au moins 6 caractères"
        )
    
    # Vérifier que les mots de passe correspondent
    if user.password != user.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les mots de passe ne correspondent pas"
        )
    
    # Hasher le mot de passe avec gestion d'erreur détaillée
    try:
        hashed_password = get_password_hash(user.password)
    except Exception as e:
        error_msg = f"Password hashing error: {str(e)}"
        print(error_msg)  # TODO: Use proper logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur s'est produite lors du traitement de votre demande"
        )
    
    # Créer l'utilisateur
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        location=user.location,
        role=UserRole.USER
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


# ========== ENDPOINTS POUR LES OBJETS D'UN UTILISATEUR ==========

@router.get("/{user_id}/objects", response_model=List[schemas.Object])
def get_user_objects(user_id: int, db: Session = Depends(get_db)):
    """Récupère tous les objets d'un utilisateur spécifique"""
    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    # Récupérer tous les objets de cet utilisateur
    objects = db.query(Object).filter(Object.owner_id == user_id).all()
    return objects


@router.post("/{user_id}/objects", response_model=schemas.Object, status_code=status.HTTP_201_CREATED)
def add_user_object(user_id: int, obj: schemas.ObjectCreate, db: Session = Depends(get_db)):
    """Ajoute un nouvel objet pour un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    # Créer le nouvel objet
    db_object = Object(**obj.model_dump(), owner_id=user_id)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


@router.get("/{user_id}/objects/{object_id}", response_model=schemas.Object)
def get_user_object(user_id: int, object_id: int, db: Session = Depends(get_db)):
    """Récupère un objet spécifique d'un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    # Récupérer l'objet
    obj = db.query(Object).filter(Object.id == object_id, Object.owner_id == user_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Objet non trouvé ou n'appartient pas à cet utilisateur"
        )
    
    return obj


@router.put("/{user_id}/objects/{object_id}", response_model=schemas.Object)
def update_user_object(user_id: int, object_id: int, obj_update: schemas.ObjectCreate, db: Session = Depends(get_db)):
    """Met à jour un objet d'un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    # Récupérer l'objet
    db_object = db.query(Object).filter(Object.id == object_id, Object.owner_id == user_id).first()
    if not db_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Objet non trouvé ou n'appartient pas à cet utilisateur"
        )
    
    # Mettre à jour l'objet
    for key, value in obj_update.model_dump().items():
        setattr(db_object, key, value)
    
    db.commit()
    db.refresh(db_object)
    return db_object


@router.delete("/{user_id}/objects/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_object(user_id: int, object_id: int, db: Session = Depends(get_db)):
    """Supprime un objet d'un utilisateur"""
    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    
    # Récupérer l'objet
    db_object = db.query(Object).filter(Object.id == object_id, Object.owner_id == user_id).first()
    if not db_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Objet non trouvé ou n'appartient pas à cet utilisateur"
        )
    
    # Supprimer l'objet
    db.delete(db_object)
    db.commit()
    return None

