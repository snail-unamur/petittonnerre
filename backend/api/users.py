from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import User, UserRole
import schemas  # Import the entire schemas module
from schemas import UserCreate, UserResponse
from database import get_db
from passlib.context import CryptContext
import re

# Configuration de bcrypt avec paramètres explicites et identification du backend
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",  # Force l'utilisation de bcrypt moderne ($2b$)
    bcrypt__min_rounds=12,  # Nombre minimum de rounds
    default="bcrypt"  # S'assure que bcrypt est le schéma par défaut
)

router = APIRouter(prefix="/users", tags=["users"])

def validate_password(password: str) -> bool:
    """
    Validate that the password meets security requirements:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Vérifier si le nom d'utilisateur existe déjà
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Valider le mot de passe
    if not validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not meet security requirements"
        )
    
    # Vérifier que les mots de passe correspondent
    if user.password != user.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Vérifier la longueur du mot de passe (limite bcrypt)
    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be longer than 72 bytes"
        )
    
    # Hasher le mot de passe avec gestion d'erreur détaillée
    try:
        # Vérifier que bcrypt est disponible
        if not pwd_context.schemes():
            raise RuntimeError("No hashing schemes available")
            
        hashed_password = pwd_context.hash(user.password)
        if not hashed_password:
            raise ValueError("Password hashing failed - empty hash")
            
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
            detail="An error occurred during password hashing"
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
        raise HTTPException(status_code=404, detail="User not found")
    return user
