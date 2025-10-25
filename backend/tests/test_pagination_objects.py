"""
Tests pour la pagination des objets (US2.6)
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
    """Créer un utilisateur pour les tests"""
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


def test_pagination_with_limit(user1):
    """Test: Pagination avec limite de 10 objets"""
    db = TestingSessionLocal()
    
    # Créer 50 objets pour l'utilisateur
    user = db.query(User).filter(User.id == user1).first()
    for i in range(50):
        obj = Object(
            name=f"Objet {i}",
            category=ObjectCategory.HEATING,
            created_by=user1
        )
        db.add(obj)
        db.flush()
        obj.owners.append(user)
    
    db.commit()
    db.close()
    
    # Récupérer les 10 premiers objets
    response = client.get(f"/objects/?user_id={user1}&skip=0&limit=10")
    assert response.status_code == 200
    objects = response.json()
    assert len(objects) == 10


def test_pagination_skip_parameter(user1):
    """Test: Le paramètre skip fonctionne correctement"""
    db = TestingSessionLocal()
    
    # Créer 50 objets
    user = db.query(User).filter(User.id == user1).first()
    for i in range(50):
        obj = Object(
            name=f"Objet {i:02d}",  # Format avec zéros pour tri cohérent
            category=ObjectCategory.HEATING,
            created_by=user1
        )
        db.add(obj)
        db.flush()
        obj.owners.append(user)
    
    db.commit()
    db.close()
    
    # Récupérer page 1 (objets 0-9)
    response1 = client.get(f"/objects/?user_id={user1}&skip=0&limit=10")
    page1 = response1.json()
    
    # Récupérer page 2 (objets 10-19)
    response2 = client.get(f"/objects/?user_id={user1}&skip=10&limit=10")
    page2 = response2.json()
    
    assert len(page1) == 10
    assert len(page2) == 10
    
    # Vérifier qu'il n'y a pas de doublon entre les pages
    page1_ids = {obj["id"] for obj in page1}
    page2_ids = {obj["id"] for obj in page2}
    assert len(page1_ids.intersection(page2_ids)) == 0


def test_pagination_30_per_page(user1):
    """Test US2.6: Pagination avec 30 objets par page (valeur par défaut)"""
    db = TestingSessionLocal()
    
    # Créer 100 objets
    user = db.query(User).filter(User.id == user1).first()
    for i in range(100):
        obj = Object(
            name=f"Objet {i}",
            category=ObjectCategory.HEATING if i < 50 else ObjectCategory.KITCHEN,
            created_by=user1
        )
        db.add(obj)
        db.flush()
        obj.owners.append(user)
    
    db.commit()
    db.close()
    
    # Récupérer la première page (30 objets)
    response1 = client.get(f"/objects/?user_id={user1}&skip=0&limit=30")
    assert response1.status_code == 200
    page1 = response1.json()
    assert len(page1) == 30
    
    # Récupérer la deuxième page
    response2 = client.get(f"/objects/?user_id={user1}&skip=30&limit=30")
    page2 = response2.json()
    assert len(page2) == 30
    
    # Récupérer la troisième page
    response3 = client.get(f"/objects/?user_id={user1}&skip=60&limit=30")
    page3 = response3.json()
    assert len(page3) == 30
    
    # Récupérer la quatrième page (devrait contenir 10 objets seulement)
    response4 = client.get(f"/objects/?user_id={user1}&skip=90&limit=30")
    page4 = response4.json()
    assert len(page4) == 10


def test_pagination_no_more_objects(user1):
    """Test: Quand skip dépasse le nombre d'objets, retourner une liste vide"""
    db = TestingSessionLocal()
    
    # Créer 20 objets
    user = db.query(User).filter(User.id == user1).first()
    for i in range(20):
        obj = Object(
            name=f"Objet {i}",
            category=ObjectCategory.HEATING,
            created_by=user1
        )
        db.add(obj)
        db.flush()
        obj.owners.append(user)
    
    db.commit()
    db.close()
    
    # Tenter de récupérer à partir de l'index 50 (au-delà des objets disponibles)
    response = client.get(f"/objects/?user_id={user1}&skip=50&limit=30")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_pagination_without_limit(user1):
    """Test: Sans limite, tous les objets (à partir de skip) sont retournés"""
    db = TestingSessionLocal()
    
    # Créer 50 objets
    user = db.query(User).filter(User.id == user1).first()
    for i in range(50):
        obj = Object(
            name=f"Objet {i}",
            category=ObjectCategory.HEATING,
            created_by=user1
        )
        db.add(obj)
        db.flush()
        obj.owners.append(user)
    
    db.commit()
    db.close()
    
    # Récupérer à partir de l'index 20 sans limite
    response = client.get(f"/objects/?user_id={user1}&skip=20")
    assert response.status_code == 200
    objects = response.json()
    assert len(objects) == 30  # Les 30 objets restants (50 - 20)


def test_pagination_with_categories(user1):
    """Test: La pagination fonctionne avec différentes catégories"""
    db = TestingSessionLocal()
    
    # Créer 60 objets de différentes catégories
    user = db.query(User).filter(User.id == user1).first()
    categories = [ObjectCategory.HEATING, ObjectCategory.KITCHEN, ObjectCategory.BATHROOM]
    
    for i in range(60):
        obj = Object(
            name=f"Objet {i}",
            category=categories[i % 3],
            created_by=user1
        )
        db.add(obj)
        db.flush()
        obj.owners.append(user)
    
    db.commit()
    db.close()
    
    # Récupérer toutes les pages
    page1 = client.get(f"/objects/?user_id={user1}&skip=0&limit=30").json()
    page2 = client.get(f"/objects/?user_id={user1}&skip=30&limit=30").json()
    
    assert len(page1) == 30
    assert len(page2) == 30
    
    # Vérifier que toutes les catégories sont présentes
    all_objects = page1 + page2
    categories_found = {obj["category"] for obj in all_objects}
    assert "heating" in categories_found
    assert "kitchen" in categories_found
    assert "bathroom" in categories_found
