"""Tests pour l'authentification"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, UserRole
from auth import get_password_hash

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dépendance get_db pour les tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture qui crée et nettoie la base de données pour chaque test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Crée un utilisateur de test dans la base de données"""
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPassword123!"),
        location="Test City",
        role=UserRole.user,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()
    return {"id": user_id, "email": "test@example.com", "password": "TestPassword123!"}


def test_register_user():
    """Test l'inscription d'un nouvel utilisateur"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewPassword123!",
            "password_confirm": "NewPassword123!",
            "location": "New City"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email():
    """Test l'inscription avec un email déjà utilisé"""
    # Créer le premier utilisateur
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "City"
        }
    )
    
    # Tenter de créer un second utilisateur avec le même email
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "City"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username():
    """Test l'inscription avec un username déjà utilisé"""
    # Créer le premier utilisateur
    client.post(
        "/auth/register",
        json={
            "email": "user1@example.com",
            "username": "sameusername",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "City"
        }
    )
    
    # Tenter de créer un second utilisateur avec le même username
    response = client.post(
        "/auth/register",
        json={
            "email": "user2@example.com",
            "username": "sameusername",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "City"
        }
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_success(test_user):
    """Test la connexion avec des identifiants corrects"""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email():
    """Test la connexion avec un email invalide"""
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_invalid_password(test_user):
    """Test la connexion avec un mot de passe incorrect"""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": "WrongPassword123!"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user(test_user):
    """Test la récupération de l'utilisateur connecté"""
    # Se connecter pour obtenir un token
    login_response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Utiliser le token pour récupérer les infos utilisateur
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]


def test_get_current_user_invalid_token():
    """Test la récupération de l'utilisateur avec un token invalide"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_get_current_user_no_token():
    """Test la récupération de l'utilisateur sans token"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_logout(test_user):
    """Test la déconnexion"""
    # Se connecter
    login_response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Se déconnecter
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]
