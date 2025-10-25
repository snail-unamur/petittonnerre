from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import User, UserRole
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
<<<<<<< HEAD
        # Vérifier que bcrypt est disponible
        if not pwd_context.schemes():
            raise RuntimeError("No hashing schemes available")
            
        hashed_password = pwd_context.hash(user.password)
        if not hashed_password:
            raise ValueError("Password hashing failed - empty hash")
            
=======
        hashed_password = hash_password(user.password)
>>>>>>> 573e9ba (feat(US5.1): Améliorer authentification avec design flat et menu utilisateur)
    except Exception as e:
        error_msg = f"Password hashing error: {str(e)}"
        print(error_msg)  # TODO: Use proper logging
        if "cannot be longer than 72 bytes" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be longer than 72 bytes"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
<<<<<<< HEAD
            detail="An error occurred during password hashing"
=======
            detail="Une erreur s'est produite lors du traitement de votre demande"
>>>>>>> 573e9ba (feat(US5.1): Améliorer authentification avec design flat et menu utilisateur)
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
