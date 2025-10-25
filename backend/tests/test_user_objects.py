"""
Tests pour les endpoints de gestion des objets d'un utilisateur
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

from database import Base, get_db
from main import app
from models import User, Object, ObjectCategory, UserRole
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
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Créer les tables et nettoyer après chaque test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(setup_database):
    """Créer un utilisateur de test"""
    db = TestingSessionLocal()
    password = "testpass123"
    hashed_password = get_password_hash(password)
    
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hashed_password,
        role=UserRole.user,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@pytest.fixture
def other_user(setup_database):
    """Créer un second utilisateur de test"""
    db = TestingSessionLocal()
    password = "otherpass123"
    hashed_password = get_password_hash(password)
    
    user = User(
        email="other@example.com",
        username="otheruser",
        hashed_password=hashed_password,
        role=UserRole.user,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@pytest.fixture
def test_object(setup_database, test_user):
    """Créer un objet de test"""
    db = TestingSessionLocal()
    obj = Object(
        name="Chaudière Test",
        category=ObjectCategory.HEATING,
        brand="TestBrand",
        model="Model123",
        owner_id=test_user.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    db.close()
    return obj


# ========== TESTS GET /users/{user_id}/objects ==========

def test_get_user_objects_empty(test_user):
    """Test: récupérer les objets d'un utilisateur (liste vide)"""
    response = client.get(f"/users/{test_user.id}/objects")
    assert response.status_code == 200
    assert response.json() == []


def test_get_user_objects_with_objects(test_user, test_object):
    """Test: récupérer les objets d'un utilisateur (avec objets)"""
    response = client.get(f"/users/{test_user.id}/objects")
    assert response.status_code == 200
    objects = response.json()
    assert len(objects) == 1
    assert objects[0]["name"] == "Chaudière Test"
    assert objects[0]["category"] == "heating"
    assert objects[0]["owner_id"] == test_user.id


def test_get_user_objects_user_not_found(setup_database):
    """Test: récupérer les objets d'un utilisateur inexistant"""
    response = client.get("/users/99999/objects")
    assert response.status_code == 404
    assert "Utilisateur non trouvé" in response.json()["detail"]


def test_get_user_objects_only_own_objects(test_user, other_user):
    """Test: un utilisateur ne voit que ses propres objets"""
    db = TestingSessionLocal()
    
    # Créer des objets pour chaque utilisateur
    obj1 = Object(name="Objet User1", category=ObjectCategory.HEATING, owner_id=test_user.id)
    obj2 = Object(name="Objet User2", category=ObjectCategory.KITCHEN, owner_id=other_user.id)
    db.add(obj1)
    db.add(obj2)
    db.commit()
    db.close()
    
    # Vérifier que chaque utilisateur ne voit que ses objets
    response1 = client.get(f"/users/{test_user.id}/objects")
    assert response1.status_code == 200
    objects1 = response1.json()
    assert len(objects1) == 1
    assert objects1[0]["name"] == "Objet User1"
    
    response2 = client.get(f"/users/{other_user.id}/objects")
    assert response2.status_code == 200
    objects2 = response2.json()
    assert len(objects2) == 1
    assert objects2[0]["name"] == "Objet User2"


# ========== TESTS POST /users/{user_id}/objects ==========

def test_add_user_object_success(test_user):
    """Test: ajouter un objet à un utilisateur"""
    object_data = {
        "name": "Nouveau Four",
        "category": "kitchen",
        "brand": "Bosch",
        "model": "HBA5360S0",
        "notes": "Four encastrable"
    }
    
    response = client.post(f"/users/{test_user.id}/objects", json=object_data)
    assert response.status_code == 201
    
    created_object = response.json()
    assert created_object["name"] == "Nouveau Four"
    assert created_object["category"] == "kitchen"
    assert created_object["owner_id"] == test_user.id
    assert "id" in created_object


def test_add_user_object_user_not_found(setup_database):
    """Test: ajouter un objet à un utilisateur inexistant"""
    object_data = {
        "name": "Test Object",
        "category": "heating"
    }
    
    response = client.post("/users/99999/objects", json=object_data)
    assert response.status_code == 404
    assert "Utilisateur non trouvé" in response.json()["detail"]


def test_add_user_object_with_parent(test_user, test_object):
    """Test: ajouter un objet avec un parent"""
    object_data = {
        "name": "Brûleur de chaudière",
        "category": "heating",
        "parent_id": test_object.id
    }
    
    response = client.post(f"/users/{test_user.id}/objects", json=object_data)
    assert response.status_code == 201
    
    created_object = response.json()
    assert created_object["parent_id"] == test_object.id


def test_add_user_object_parent_not_found(test_user):
    """Test: ajouter un objet avec un parent inexistant"""
    object_data = {
        "name": "Test Object",
        "category": "heating",
        "parent_id": 99999
    }
    
    response = client.post(f"/users/{test_user.id}/objects", json=object_data)
    assert response.status_code == 404
    assert "Objet parent non trouvé" in response.json()["detail"]


def test_add_user_object_parent_different_owner(test_user, other_user):
    """Test: ajouter un objet avec un parent qui appartient à un autre utilisateur"""
    db = TestingSessionLocal()
    parent_obj = Object(
        name="Parent Object",
        category=ObjectCategory.HEATING,
        owner_id=other_user.id
    )
    db.add(parent_obj)
    db.commit()
    db.refresh(parent_obj)
    parent_id = parent_obj.id
    db.close()
    
    object_data = {
        "name": "Child Object",
        "category": "heating",
        "parent_id": parent_id
    }
    
    response = client.post(f"/users/{test_user.id}/objects", json=object_data)
    assert response.status_code == 403
    assert "appartenir au même utilisateur" in response.json()["detail"]


# ========== TESTS GET /users/{user_id}/objects/{object_id} ==========

def test_get_user_object_success(test_user, test_object):
    """Test: récupérer un objet spécifique"""
    response = client.get(f"/users/{test_user.id}/objects/{test_object.id}")
    assert response.status_code == 200
    
    obj = response.json()
    assert obj["id"] == test_object.id
    assert obj["name"] == test_object.name
    assert obj["owner_id"] == test_user.id


def test_get_user_object_not_found(test_user):
    """Test: récupérer un objet inexistant"""
    response = client.get(f"/users/{test_user.id}/objects/99999")
    assert response.status_code == 404
    assert "Objet non trouvé" in response.json()["detail"]


def test_get_user_object_wrong_owner(test_user, other_user):
    """Test: récupérer un objet qui appartient à un autre utilisateur"""
    db = TestingSessionLocal()
    obj = Object(
        name="Other User Object",
        category=ObjectCategory.HEATING,
        owner_id=other_user.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    obj_id = obj.id
    db.close()
    
    response = client.get(f"/users/{test_user.id}/objects/{obj_id}")
    assert response.status_code == 404
    assert "n'appartient pas" in response.json()["detail"]


# ========== TESTS PUT /users/{user_id}/objects/{object_id} ==========

def test_update_user_object_success(test_user, test_object):
    """Test: mettre à jour un objet"""
    update_data = {
        "name": "Chaudière Mise à Jour",
        "category": "heating",
        "brand": "NewBrand",
        "model": "NewModel",
        "notes": "Notes mises à jour"
    }
    
    response = client.put(f"/users/{test_user.id}/objects/{test_object.id}", json=update_data)
    assert response.status_code == 200
    
    updated_obj = response.json()
    assert updated_obj["name"] == "Chaudière Mise à Jour"
    assert updated_obj["brand"] == "NewBrand"
    assert updated_obj["notes"] == "Notes mises à jour"


def test_update_user_object_not_found(test_user):
    """Test: mettre à jour un objet inexistant"""
    update_data = {
        "name": "Test",
        "category": "heating"
    }
    
    response = client.put(f"/users/{test_user.id}/objects/99999", json=update_data)
    assert response.status_code == 404


def test_update_user_object_wrong_owner(test_user, other_user):
    """Test: mettre à jour un objet qui appartient à un autre utilisateur"""
    db = TestingSessionLocal()
    obj = Object(
        name="Other User Object",
        category=ObjectCategory.HEATING,
        owner_id=other_user.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    obj_id = obj.id
    db.close()
    
    update_data = {
        "name": "Updated Name",
        "category": "heating"
    }
    
    response = client.put(f"/users/{test_user.id}/objects/{obj_id}", json=update_data)
    assert response.status_code == 404
    assert "n'appartient pas" in response.json()["detail"]


# ========== TESTS DELETE /users/{user_id}/objects/{object_id} ==========

def test_delete_user_object_success(test_user, test_object):
    """Test: supprimer un objet"""
    response = client.delete(f"/users/{test_user.id}/objects/{test_object.id}")
    assert response.status_code == 204
    
    # Vérifier que l'objet n'existe plus
    get_response = client.get(f"/users/{test_user.id}/objects/{test_object.id}")
    assert get_response.status_code == 404


def test_delete_user_object_not_found(test_user):
    """Test: supprimer un objet inexistant"""
    response = client.delete(f"/users/{test_user.id}/objects/99999")
    assert response.status_code == 404


def test_delete_user_object_wrong_owner(test_user, other_user):
    """Test: supprimer un objet qui appartient à un autre utilisateur"""
    db = TestingSessionLocal()
    obj = Object(
        name="Other User Object",
        category=ObjectCategory.HEATING,
        owner_id=other_user.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    obj_id = obj.id
    db.close()
    
    response = client.delete(f"/users/{test_user.id}/objects/{obj_id}")
    assert response.status_code == 404
    assert "n'appartient pas" in response.json()["detail"]


# ========== TESTS DE SÉCURITÉ ==========

def test_user_isolation(test_user, other_user):
    """Test: vérifier l'isolation complète entre utilisateurs"""
    db = TestingSessionLocal()
    
    # Créer 3 objets pour test_user
    for i in range(3):
        obj = Object(
            name=f"User1 Object {i}",
            category=ObjectCategory.HEATING,
            owner_id=test_user.id
        )
        db.add(obj)
    
    # Créer 2 objets pour other_user
    for i in range(2):
        obj = Object(
            name=f"User2 Object {i}",
            category=ObjectCategory.KITCHEN,
            owner_id=other_user.id
        )
        db.add(obj)
    
    db.commit()
    db.close()
    
    # Vérifier que chaque utilisateur ne voit que ses objets
    response1 = client.get(f"/users/{test_user.id}/objects")
    assert response1.status_code == 200
    assert len(response1.json()) == 3
    
    response2 = client.get(f"/users/{other_user.id}/objects")
    assert response2.status_code == 200
    assert len(response2.json()) == 2
