from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from main import app
from database import Base, get_db
import models
from datetime import datetime

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configuration du client de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_db():
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    yield  # Exécuter les tests
    # Nettoyer la base de données
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    """Test la création d'un nouvel utilisateur"""
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "location": "Test City"
        }
    )
    assert response.status_code == 201  # Created
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["location"] == "Test City"
    assert "id" in data
    assert "created_at" in data

def test_create_user_duplicate_email(test_db):
    """Test la tentative de création d'un utilisateur avec un email déjà existant"""
    # Créer le premier utilisateur
    client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "username": "testuser1",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "location": "Test City"
        }
    )
    
    # Tenter de créer un utilisateur avec le même email
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "location": "Another City"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_user_invalid_email(test_db):
    """Test la création d'un utilisateur avec un email invalide"""
    response = client.post(
        "/users/register",
        json={
            "email": "invalid-email",
            "username": "testuser",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "location": "Test City"
        }
    )
    assert response.status_code == 422  # Validation error

def test_get_user(test_db):
    """Test la récupération d'un utilisateur existant"""
    # Créer un utilisateur
    create_response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "location": "Test City"
        }
    )
    user_id = create_response.json()["id"]
    
    # Récupérer l'utilisateur
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["location"] == "Test City"

def test_get_nonexistent_user(test_db):
    """Test la récupération d'un utilisateur qui n'existe pas"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_users_list(test_db):
    """Test la récupération de la liste des utilisateurs"""
    # Créer quelques utilisateurs
    users_data = [
        {"email": "user1@example.com", "username": "user1", "location": "City 1"},
        {"email": "user2@example.com", "username": "user2", "location": "City 2"},
        {"email": "user3@example.com", "username": "user3", "location": "City 3"}
    ]
    
    for user_data in users_data:
        user_data_with_password = user_data.copy()
        user_data_with_password["password"] = "TestPass123!"
        user_data_with_password["password_confirm"] = "TestPass123!"
        client.post("/users/register", json=user_data_with_password)
    
    # Récupérer la liste des utilisateurs
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(user["email"] in [u["email"] for u in users_data] for user in data)

def test_create_user_missing_required_fields(test_db):
    """Test la création d'un utilisateur avec des champs requis manquants"""
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!"
            # username manquant
        }
    )
    assert response.status_code == 422  # Validation error