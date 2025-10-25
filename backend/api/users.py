from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import User, UserRole, Object
import schemas  # Import the entire schemas module
from schemas import UserCreate, UserResponse
from database import get_db
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

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
    
    # Vérifier la longueur du mot de passe (limite bcrypt)
    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le mot de passe ne peut pas dépasser 72 octets"
        )
    
    # Hasher le mot de passe avec gestion d'erreur détaillée
    try:
        hashed_password = hash_password(user.password)
    except Exception as e:
        error_msg = f"Password hashing error: {str(e)}"
        print(error_msg)  # TODO: Use proper logging
        if "cannot be longer than 72 bytes" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le mot de passe ne peut pas dépasser 72 octets"
            )
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
    
    # Vérifier que le parent existe s'il est spécifié
    if obj.parent_id:
        parent_obj = db.query(Object).filter(Object.id == obj.parent_id).first()
        if not parent_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objet parent non trouvé")
        
        # Vérifier que le parent appartient bien au même utilisateur
        if parent_obj.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="L'objet parent doit appartenir au même utilisateur"
            )
    
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
    
    # Vérifier le parent si spécifié
    if obj_update.parent_id and obj_update.parent_id != db_object.parent_id:
        parent_obj = db.query(Object).filter(Object.id == obj_update.parent_id).first()
        if not parent_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objet parent non trouvé")
        
        if parent_obj.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="L'objet parent doit appartenir au même utilisateur"
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

