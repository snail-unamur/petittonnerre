"""
Tests pour les fonctionnalités d'objets partagés (many-to-many)
US2.1: En tant qu'utilisateur, je peux lier un objet existant à mon compte
"""
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

@pytest.fixture
def test_db():
    """Créer les tables avant chaque test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_users(test_db):
    """Crée deux utilisateurs de test"""
    db = TestingSessionLocal()
    
    user1 = models.User(
        email="user1@example.com",
        username="user1",
        hashed_password="hashed_password_1",
        location="Paris",
        role=models.UserRole.USER
    )
    user2 = models.User(
        email="user2@example.com",
        username="user2",
        hashed_password="hashed_password_2",
        location="Lyon",
        role=models.UserRole.USER
    )
    
    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    
    users = {
        "user1": {
            "id": user1.id,
            "email": user1.email,
            "username": user1.username
        },
        "user2": {
            "id": user2.id,
            "email": user2.email,
            "username": user2.username
        }
    }
    
    db.close()
    return users


def test_create_object_adds_creator_as_owner(test_users):
    """Test que la création d'un objet ajoute automatiquement le créateur comme propriétaire"""
    user1_id = test_users["user1"]["id"]
    
    object_data = {
        "name": "Chaudière Test",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC"
    }
    
    response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    assert response.status_code == 200
    
    created_object = response.json()
    assert created_object["name"] == object_data["name"]
    assert created_object["created_by"] == user1_id
    
    # Vérifier que l'objet apparaît dans la liste des objets de l'utilisateur
    objects_response = client.get(f"/objects/?user_id={user1_id}")
    assert objects_response.status_code == 200
    user_objects = objects_response.json()
    assert len(user_objects) == 1
    assert user_objects[0]["id"] == created_object["id"]


def test_link_existing_object_to_user(test_users):
    """Test le lien d'un objet existant à un autre utilisateur"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet
    object_data = {
        "name": "Tondeuse à gazon",
        "category": "other",
        "brand": "Honda",
        "model": "HRX537"
    }
    
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    assert create_response.status_code == 200
    created_object = create_response.json()
    object_id = created_object["id"]
    
    # User2 lie l'objet à son compte
    link_data = {"object_id": object_id}
    link_response = client.post(f"/objects/link?user_id={user2_id}", json=link_data)
    assert link_response.status_code == 200
    
    # Vérifier que l'objet apparaît dans les objets de user1 ET user2
    user1_objects = client.get(f"/objects/?user_id={user1_id}").json()
    user2_objects = client.get(f"/objects/?user_id={user2_id}").json()
    
    assert len(user1_objects) == 1
    assert len(user2_objects) == 1
    assert user1_objects[0]["id"] == object_id
    assert user2_objects[0]["id"] == object_id


def test_cannot_link_object_twice(test_users):
    """Test qu'on ne peut pas lier un objet deux fois au même utilisateur"""
    user1_id = test_users["user1"]["id"]
    
    # User1 crée un objet
    object_data = {
        "name": "Four",
        "category": "kitchen",
        "brand": "Bosch"
    }
    
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User1 essaie de lier son propre objet (déjà lié)
    link_data = {"object_id": object_id}
    link_response = client.post(f"/objects/link?user_id={user1_id}", json=link_data)
    
    assert link_response.status_code == 400
    assert "déjà lié" in link_response.json()["detail"]


def test_unlink_object_from_user(test_users):
    """Test le déliaison d'un objet d'un utilisateur"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet
    object_data = {
        "name": "Aspirateur",
        "category": "appliance",
        "brand": "Dyson"
    }
    
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User2 lie l'objet
    link_data = {"object_id": object_id}
    client.post(f"/objects/link?user_id={user2_id}", json=link_data)
    
    # User2 délie l'objet
    unlink_response = client.delete(f"/objects/unlink/{object_id}?user_id={user2_id}")
    assert unlink_response.status_code == 200
    
    # Vérifier que l'objet n'apparaît plus dans les objets de user2
    user2_objects = client.get(f"/objects/?user_id={user2_id}").json()
    assert len(user2_objects) == 0
    
    # Mais toujours dans ceux de user1
    user1_objects = client.get(f"/objects/?user_id={user1_id}").json()
    assert len(user1_objects) == 1


def test_cannot_unlink_as_sole_owner(test_users):
    """Test qu'on ne peut pas délier un objet si on est le seul propriétaire"""
    user1_id = test_users["user1"]["id"]
    
    # User1 crée un objet
    object_data = {
        "name": "Lave-vaisselle",
        "category": "appliance",
        "brand": "Bosch"
    }
    
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User1 essaie de délier son propre objet (seul propriétaire)
    unlink_response = client.delete(f"/objects/unlink/{object_id}?user_id={user1_id}")
    
    assert unlink_response.status_code == 400
    assert "seul propriétaire" in unlink_response.json()["detail"]


def test_search_objects_by_name(test_users):
    """Test la recherche d'objets par nom"""
    user1_id = test_users["user1"]["id"]
    
    # Créer plusieurs objets
    objects_data = [
        {"name": "Chaudière Gaz", "category": "heating", "brand": "Vaillant"},
        {"name": "Chaudière Électrique", "category": "heating", "brand": "Atlantic"},
        {"name": "Four", "category": "kitchen", "brand": "Bosch"}
    ]
    
    for obj_data in objects_data:
        client.post(f"/objects/?user_id={user1_id}", json=obj_data)
    
    # Rechercher "chaudière"
    search_response = client.get("/objects/search?name=chaudière")
    assert search_response.status_code == 200
    results = search_response.json()
    
    assert len(results) == 2
    assert all("chaudière" in obj["name"].lower() for obj in results)


def test_search_objects_by_category(test_users):
    """Test la recherche d'objets par catégorie"""
    user1_id = test_users["user1"]["id"]
    
    # Créer plusieurs objets
    objects_data = [
        {"name": "Chaudière", "category": "heating", "brand": "Vaillant"},
        {"name": "Radiateur", "category": "heating", "brand": "Acova"},
        {"name": "Four", "category": "kitchen", "brand": "Bosch"}
    ]
    
    for obj_data in objects_data:
        client.post(f"/objects/?user_id={user1_id}", json=obj_data)
    
    # Rechercher par catégorie "heating"
    search_response = client.get("/objects/search?category=heating")
    assert search_response.status_code == 200
    results = search_response.json()
    
    assert len(results) == 2
    assert all(obj["category"] == "heating" for obj in results)


def test_search_objects_by_brand_and_model(test_users):
    """Test la recherche d'objets par marque et modèle"""
    user1_id = test_users["user1"]["id"]
    
    # Créer plusieurs objets
    objects_data = [
        {"name": "Chaudière 1", "category": "heating", "brand": "Vaillant", "model": "ecoTEC"},
        {"name": "Chaudière 2", "category": "heating", "brand": "Vaillant", "model": "ecoTEC plus"},
        {"name": "Four", "category": "kitchen", "brand": "Bosch", "model": "HBG675BS1"}
    ]
    
    for obj_data in objects_data:
        client.post(f"/objects/?user_id={user1_id}", json=obj_data)
    
    # Rechercher par marque "Vaillant" et modèle contenant "ecoTEC"
    search_response = client.get("/objects/search?brand=Vaillant&model=ecoTEC")
    assert search_response.status_code == 200
    results = search_response.json()
    
    assert len(results) == 2
    assert all(obj["brand"] == "Vaillant" for obj in results)
    assert all("ecoTEC" in obj["model"] for obj in results)


def test_multiple_users_share_same_object(test_users):
    """Test que plusieurs utilisateurs peuvent partager le même objet"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet (chaudière de la copropriété par exemple)
    object_data = {
        "name": "Chaudière Copropriété",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC"
    }
    
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User2 lie l'objet à son compte
    link_data = {"object_id": object_id}
    client.post(f"/objects/link?user_id={user2_id}", json=link_data)
    
    # Les deux utilisateurs voient l'objet
    user1_objects = client.get(f"/objects/?user_id={user1_id}").json()
    user2_objects = client.get(f"/objects/?user_id={user2_id}").json()
    
    assert len(user1_objects) == 1
    assert len(user2_objects) == 1
    assert user1_objects[0]["id"] == object_id
    assert user2_objects[0]["id"] == object_id
    assert user1_objects[0]["name"] == "Chaudière Copropriété"
    assert user2_objects[0]["name"] == "Chaudière Copropriété"


def test_get_user_objects_only(test_users):
    """Test que chaque utilisateur ne voit que ses propres objets"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet
    object1_data = {"name": "Objet User1", "category": "other"}
    client.post(f"/objects/?user_id={user1_id}", json=object1_data)
    
    # User2 crée un objet
    object2_data = {"name": "Objet User2", "category": "other"}
    client.post(f"/objects/?user_id={user2_id}", json=object2_data)
    
    # Vérifier que chaque utilisateur ne voit que son objet
    user1_objects = client.get(f"/objects/?user_id={user1_id}").json()
    user2_objects = client.get(f"/objects/?user_id={user2_id}").json()
    
    assert len(user1_objects) == 1
    assert len(user2_objects) == 1
    assert user1_objects[0]["name"] == "Objet User1"
    assert user2_objects[0]["name"] == "Objet User2"


def test_link_nonexistent_object(test_users):
    """Test la liaison d'un objet inexistant"""
    user1_id = test_users["user1"]["id"]
    
    link_data = {"object_id": 9999}
    link_response = client.post(f"/objects/link?user_id={user1_id}", json=link_data)
    
    assert link_response.status_code == 404
    assert "Objet non trouvé" in link_response.json()["detail"]


def test_unlink_nonexistent_object(test_users):
    """Test le déliaison d'un objet inexistant"""
    user1_id = test_users["user1"]["id"]
    
    unlink_response = client.delete(f"/objects/unlink/9999?user_id={user1_id}")
    
    assert unlink_response.status_code == 404
    assert "Objet non trouvé" in unlink_response.json()["detail"]


def test_unlink_object_not_linked(test_users):
    """Test le déliaison d'un objet non lié à l'utilisateur"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet
    object_data = {"name": "Objet User1", "category": "other"}
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User2 essaie de délier un objet qui n'est pas le sien
    unlink_response = client.delete(f"/objects/unlink/{object_id}?user_id={user2_id}")
    
    assert unlink_response.status_code == 400
    assert "n'est pas lié" in unlink_response.json()["detail"]


def test_delete_object_removes_user_link_only(test_users):
    """Test que la suppression d'un objet retire uniquement le lien utilisateur, pas l'objet"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet
    object_data = {"name": "Objet partagé", "category": "other"}
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User2 lie cet objet
    link_data = {"object_id": object_id}
    client.post(f"/objects/link?user_id={user2_id}", json=link_data)
    
    # User1 "supprime" l'objet (retire son lien)
    delete_response = client.delete(f"/objects/{object_id}?user_id={user1_id}")
    assert delete_response.status_code == 200
    assert "retiré de votre liste" in delete_response.json()["message"]
    
    # Vérifier que l'objet existe toujours pour User2
    user2_objects = client.get(f"/objects/?user_id={user2_id}")
    assert user2_objects.status_code == 200
    user2_obj_ids = [obj["id"] for obj in user2_objects.json()]
    assert object_id in user2_obj_ids
    
    # Vérifier que User1 ne voit plus l'objet
    user1_objects = client.get(f"/objects/?user_id={user1_id}")
    assert user1_objects.status_code == 200
    user1_obj_ids = [obj["id"] for obj in user1_objects.json()]
    assert object_id not in user1_obj_ids


def test_delete_object_removes_from_db_when_no_owners(test_users):
    """Test que l'objet est supprimé de la BD quand il n'a plus de propriétaires"""
    user1_id = test_users["user1"]["id"]
    
    # User1 crée un objet
    object_data = {"name": "Objet solo", "category": "other"}
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User1 supprime l'objet
    delete_response = client.delete(f"/objects/{object_id}?user_id={user1_id}")
    assert delete_response.status_code == 200
    assert "supprimé de la base" in delete_response.json()["message"]
    
    # Vérifier que l'objet n'existe plus du tout
    get_response = client.get(f"/objects/{object_id}")
    assert get_response.status_code == 404


def test_delete_object_not_owner(test_users):
    """Test qu'un utilisateur ne peut pas supprimer un objet dont il n'est pas propriétaire"""
    user1_id = test_users["user1"]["id"]
    user2_id = test_users["user2"]["id"]
    
    # User1 crée un objet
    object_data = {"name": "Objet User1", "category": "other"}
    create_response = client.post(f"/objects/?user_id={user1_id}", json=object_data)
    object_id = create_response.json()["id"]
    
    # User2 essaie de supprimer l'objet de User1
    delete_response = client.delete(f"/objects/{object_id}?user_id={user2_id}")
    assert delete_response.status_code == 403
    assert "pas propriétaire" in delete_response.json()["detail"]
