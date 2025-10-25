"""
Tests pour vérifier que les utilisateurs ne voient que leurs propres objets (US2.4)
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

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
def user1(setup_database):
    """Créer le premier utilisateur"""
    db = TestingSessionLocal()
    password = "password1"
    hashed_password = get_password_hash(password)
    
    user = User(
        email="user1@example.com",
        username="user1",
        hashed_password=hashed_password,
        role=UserRole.USER,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()
    return user_id


@pytest.fixture
def user2(setup_database):
    """Créer le second utilisateur"""
    db = TestingSessionLocal()
    password = "password2"
    hashed_password = get_password_hash(password)
    
    user = User(
        email="user2@example.com",
        username="user2",
        hashed_password=hashed_password,
        role=UserRole.USER,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()
    return user_id


@pytest.fixture
def admin_user(setup_database):
    """Créer un utilisateur admin"""
    db = TestingSessionLocal()
    password = "adminpass"
    hashed_password = get_password_hash(password)
    
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()
    return user_id


def test_user_sees_only_own_objects(user1, user2):
    """Test US2.4: Un utilisateur ne voit que ses propres objets"""
    db = TestingSessionLocal()
    
    # Créer 3 objets pour user1
    obj1 = Object(name="Chaudière User1", category=ObjectCategory.HEATING, created_by=user1)
    obj2 = Object(name="Four User1", category=ObjectCategory.KITCHEN, created_by=user1)
    obj3 = Object(name="Baignoire User1", category=ObjectCategory.BATHROOM, created_by=user1)
    
    db.add_all([obj1, obj2, obj3])
    db.flush()
    
    # Associer les objets à user1
    user1_obj = db.query(User).filter(User.id == user1).first()
    user1_obj.objects.extend([obj1, obj2, obj3])
    
    # Créer 2 objets pour user2
    obj4 = Object(name="Chaudière User2", category=ObjectCategory.HEATING, created_by=user2)
    obj5 = Object(name="Four User2", category=ObjectCategory.KITCHEN, created_by=user2)
    
    db.add_all([obj4, obj5])
    db.flush()
    
    # Associer les objets à user2
    user2_obj = db.query(User).filter(User.id == user2).first()
    user2_obj.objects.extend([obj4, obj5])
    
    db.commit()
    db.close()
    
    # Vérifier que user1 ne voit que ses 3 objets
    response1 = client.get(f"/objects/?user_id={user1}")
    assert response1.status_code == 200
    objects1 = response1.json()
    assert len(objects1) == 3
    object_names1 = [obj["name"] for obj in objects1]
    assert "Chaudière User1" in object_names1
    assert "Four User1" in object_names1
    assert "Baignoire User1" in object_names1
    assert "Chaudière User2" not in object_names1
    assert "Four User2" not in object_names1
    
    # Vérifier que user2 ne voit que ses 2 objets
    response2 = client.get(f"/objects/?user_id={user2}")
    assert response2.status_code == 200
    objects2 = response2.json()
    assert len(objects2) == 2
    object_names2 = [obj["name"] for obj in objects2]
    assert "Chaudière User2" in object_names2
    assert "Four User2" in object_names2
    assert "Chaudière User1" not in object_names2
    assert "Four User1" not in object_names2
    assert "Baignoire User1" not in object_names2


def test_user_with_no_objects(user1):
    """Test: Un utilisateur sans objets reçoit une liste vide"""
    response = client.get(f"/objects/?user_id={user1}")
    assert response.status_code == 200
    assert response.json() == []


def test_shared_object_visibility(user1, user2):
    """Test: Un objet partagé est visible par tous ses propriétaires"""
    db = TestingSessionLocal()
    
    # Créer un objet partagé
    shared_obj = Object(
        name="Objet Partagé",
        category=ObjectCategory.HEATING,
        created_by=user1
    )
    db.add(shared_obj)
    db.flush()
    
    # Associer l'objet à user1 et user2
    user1_obj = db.query(User).filter(User.id == user1).first()
    user2_obj = db.query(User).filter(User.id == user2).first()
    
    shared_obj.owners.extend([user1_obj, user2_obj])
    
    db.commit()
    db.close()
    
    # Vérifier que user1 voit l'objet
    response1 = client.get(f"/objects/?user_id={user1}")
    assert response1.status_code == 200
    objects1 = response1.json()
    assert len(objects1) == 1
    assert objects1[0]["name"] == "Objet Partagé"
    
    # Vérifier que user2 voit aussi l'objet
    response2 = client.get(f"/objects/?user_id={user2}")
    assert response2.status_code == 200
    objects2 = response2.json()
    assert len(objects2) == 1
    assert objects2[0]["name"] == "Objet Partagé"


def test_admin_sees_all_objects_without_filter(user1, user2, admin_user):
    """Test: Un admin peut voir tous les objets s'il ne fournit pas de user_id"""
    db = TestingSessionLocal()
    
    # Créer des objets pour user1
    obj1 = Object(name="Objet User1", category=ObjectCategory.HEATING, created_by=user1)
    db.add(obj1)
    db.flush()
    user1_obj = db.query(User).filter(User.id == user1).first()
    obj1.owners.append(user1_obj)
    
    # Créer des objets pour user2
    obj2 = Object(name="Objet User2", category=ObjectCategory.KITCHEN, created_by=user2)
    db.add(obj2)
    db.flush()
    user2_obj = db.query(User).filter(User.id == user2).first()
    obj2.owners.append(user2_obj)
    
    db.commit()
    db.close()
    
    # L'admin récupère tous les objets sans filtre
    response = client.get("/objects/")
    assert response.status_code == 200
    all_objects = response.json()
    assert len(all_objects) >= 2
    object_names = [obj["name"] for obj in all_objects]
    assert "Objet User1" in object_names
    assert "Objet User2" in object_names


def test_nonexistent_user(setup_database):
    """Test: Un utilisateur inexistant retourne une erreur 404"""
    response = client.get("/objects/?user_id=99999")
    assert response.status_code == 404
    assert "Utilisateur non trouvé" in response.json()["detail"]


def test_multiple_objects_isolation(user1, user2):
    """Test d'isolation avec de nombreux objets"""
    db = TestingSessionLocal()
    
    # Créer 10 objets pour user1
    for i in range(10):
        obj = Object(
            name=f"Objet {i} User1",
            category=ObjectCategory.HEATING,
            created_by=user1
        )
        db.add(obj)
        db.flush()
        user1_obj = db.query(User).filter(User.id == user1).first()
        obj.owners.append(user1_obj)
    
    # Créer 5 objets pour user2
    for i in range(5):
        obj = Object(
            name=f"Objet {i} User2",
            category=ObjectCategory.KITCHEN,
            created_by=user2
        )
        db.add(obj)
        db.flush()
        user2_obj = db.query(User).filter(User.id == user2).first()
        obj.owners.append(user2_obj)
    
    db.commit()
    db.close()
    
    # User1 doit voir exactement 10 objets
    response1 = client.get(f"/objects/?user_id={user1}")
    assert response1.status_code == 200
    assert len(response1.json()) == 10
    
    # User2 doit voir exactement 5 objets
    response2 = client.get(f"/objects/?user_id={user2}")
    assert response2.status_code == 200
    assert len(response2.json()) == 5
