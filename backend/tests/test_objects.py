from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

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
    yield
    # Nettoyer la base de données
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(test_db):
    """Crée un utilisateur de test et retourne ses données"""
    db = TestingSessionLocal()
    # Create user directly in the database
    db_user = models.User(
        email="test@example.com",
        username="testuser",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYpAQAMwiDpZGiW",  # Test123!
        location="Test City",
        role=models.UserRole.USER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    user_data = {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "location": db_user.location,
        "role": db_user.role.value,
        "is_active": db_user.is_active,
        "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
        "last_login": db_user.last_login.isoformat() if db_user.last_login else None
    }
    
    db.close()
    return user_data

@pytest.mark.skip(reason="Feature parent-child relationship removed from Object model")
def test_create_object_with_parent(test_user):
    """Test la création d'objets avec une relation parent-enfant"""
    # Créer l'objet parent
    parent_data = {
        "name": "Chaudière Test",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC",
        "notes": "Objet parent"
    }
    parent_response = client.post(f"/objects/?user_id={test_user['id']}", json=parent_data)
    assert parent_response.status_code == 200
    parent_object = parent_response.json()
    assert parent_object["name"] == parent_data["name"]
    
    # Créer l'objet enfant
    child_data = {
        "name": "Thermostat",
        "category": "heating",
        "brand": "Nest",
        "model": "T3007ES",
        "notes": "Objet enfant",
        "parent_id": parent_object["id"]
    }
    child_response = client.post(f"/objects/?user_id={test_user['id']}", json=child_data)
    assert child_response.status_code == 200
    child_object = child_response.json()
    assert child_object["name"] == child_data["name"]
    assert child_object["parent_id"] == parent_object["id"]

@pytest.mark.skip(reason="Feature parent-child relationship removed from Object model")
def test_get_object_with_children(test_user):
    """Test la récupération d'un objet avec ses enfants"""
    # Créer l'objet parent
    parent_data = {
        "name": "Chaudière Test",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC"
    }
    parent_response = client.post(f"/objects/?user_id={test_user['id']}", json=parent_data)
    parent_object = parent_response.json()
    
    # Créer deux objets enfants
    child_objects = [
        {
            "name": "Thermostat",
            "category": "heating",
            "brand": "Nest",
            "model": "T3007ES",
            "parent_id": parent_object["id"]
        },
        {
            "name": "Sonde température",
            "category": "heating",
            "brand": "Vaillant",
            "model": "VR 920",
            "parent_id": parent_object["id"]
        }
    ]
    
    for child_data in child_objects:
        child_response = client.post(f"/objects/?user_id={test_user['id']}", json=child_data)
        assert child_response.status_code == 200
    
    # Récupérer l'objet parent et vérifier ses enfants
    response = client.get(f"/objects/{parent_object['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == parent_data["name"]
    assert len(data["children"]) == 2
    assert any(child["name"] == "Thermostat" for child in data["children"])
    assert any(child["name"] == "Sonde température" for child in data["children"])

@pytest.mark.skip(reason="Feature parent-child relationship removed from Object model")
def test_create_object_with_nonexistent_parent(test_user):
    """Test la création d'un objet avec un parent inexistant"""
    child_data = {
        "name": "Thermostat",
        "category": "heating",
        "brand": "Nest",
        "model": "T3007ES",
        "parent_id": 9999  # ID inexistant
    }
    response = client.post(f"/objects/?user_id={test_user['id']}", json=child_data)
    assert response.status_code == 404
    assert "Parent object not found" in response.json()["detail"]

@pytest.mark.skip(reason="Feature parent-child relationship removed from Object model")
def test_delete_parent_object(test_user):
    """Test la suppression d'un objet parent (doit supprimer les enfants en cascade)"""
    # Créer l'objet parent
    parent_data = {
        "name": "Chaudière Test",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC"
    }
    parent_response = client.post(f"/objects/?user_id={test_user['id']}", json=parent_data)
    parent_object = parent_response.json()
    
    # Créer un objet enfant
    child_data = {
        "name": "Thermostat",
        "category": "heating",
        "brand": "Nest",
        "model": "T3007ES",
        "parent_id": parent_object["id"]
    }
    child_response = client.post(f"/objects/?user_id={test_user['id']}", json=child_data)
    child_object = child_response.json()
    
    # Supprimer l'objet parent (avec user_id)
    delete_response = client.delete(f"/objects/{parent_object['id']}?user_id={test_user['id']}")
    assert delete_response.status_code == 200
    
    # Vérifier que l'enfant a été supprimé aussi
    child_get_response = client.get(f"/objects/{child_object['id']}")
    assert child_get_response.status_code == 404

@pytest.mark.skip(reason="Feature parent-child relationship removed from Object model")
def test_update_object_parent(test_user):
    """Test la mise à jour du parent d'un objet"""
    # Créer deux objets parents
    parent1_data = {
        "name": "Chaudière 1",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC"
    }
    parent2_data = {
        "name": "Chaudière 2",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC plus"
    }
    
    parent1_response = client.post(f"/objects/?user_id={test_user['id']}", json=parent1_data)
    parent1_object = parent1_response.json()
    
    parent2_response = client.post(f"/objects/?user_id={test_user['id']}", json=parent2_data)
    parent2_object = parent2_response.json()
    
    # Créer un objet enfant lié au parent 1
    child_data = {
        "name": "Thermostat",
        "category": "heating",
        "brand": "Nest",
        "model": "T3007ES",
        "parent_id": parent1_object["id"]
    }
    child_response = client.post(f"/objects/?user_id={test_user['id']}", json=child_data)
    child_object = child_response.json()
    
    # Mettre à jour le parent de l'enfant
    update_data = child_data.copy()
    update_data["parent_id"] = parent2_object["id"]
    update_response = client.put(f"/objects/{child_object['id']}", json=update_data)
    assert update_response.status_code == 200
    updated_child = update_response.json()
    assert updated_child["parent_id"] == parent2_object["id"]

@pytest.mark.skip(reason="Feature parent-child relationship removed from Object model")
def test_get_objects_hierarchy(test_user):
    """Test la récupération de la hiérarchie complète des objets"""
    # Créer un objet parent
    parent_data = {
        "name": "Maison",
        "category": "other",
        "notes": "Objet racine"
    }
    parent_response = client.post(f"/objects/?user_id={test_user['id']}", json=parent_data)
    parent_object = parent_response.json()
    
    # Créer des objets enfants
    children_data = [
        {
            "name": "Étage",
            "category": "other",
            "parent_id": parent_object["id"]
        },
        {
            "name": "Rez-de-chaussée",
            "category": "other",
            "parent_id": parent_object["id"]
        }
    ]
    
    for child_data in children_data:
        response = client.post(f"/objects/?user_id={test_user['id']}", json=child_data)
        assert response.status_code == 200
    
    # Récupérer tous les objets
    response = client.get(f"/objects/?user_id={test_user['id']}")
    assert response.status_code == 200
    objects = response.json()
    
    # Vérifier la structure
    root_objects = [obj for obj in objects if obj["parent_id"] is None]
    assert len(root_objects) == 1
    assert root_objects[0]["name"] == "Maison"
    
    child_objects = [obj for obj in objects if obj["parent_id"] == parent_object["id"]]
    assert len(child_objects) == 2
    assert {"Étage", "Rez-de-chaussée"} == {obj["name"] for obj in child_objects}