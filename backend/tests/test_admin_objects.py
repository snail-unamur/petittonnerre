import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

from database import Base, get_db
from main import app
import models

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def setup_users(client):
    """Créer des utilisateurs de test (admin et utilisateur normal)"""
    # Créer un utilisateur normal
    user_data = {
        "email": "user@example.com",
        "username": "testuser",
        "password": "Test1234!",
        "password_confirm": "Test1234!"
    }
    user_response = client.post("/users/", json=user_data)
    user = user_response.json()
    
    # Créer un admin
    admin_data = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "Admin1234!",
        "password_confirm": "Admin1234!"
    }
    admin_response = client.post("/users/", json=admin_data)
    admin = admin_response.json()
    
    # Promouvoir l'utilisateur en admin dans la base
    db = TestingSessionLocal()
    db_admin = db.query(models.User).filter(models.User.id == admin["id"]).first()
    db_admin.role = models.UserRole.ADMIN
    db.commit()
    db.close()
    
    return {"user": user, "admin": admin}


class TestObjectRequests:
    """Tests pour les demandes d'objets"""
    
    def test_create_object_request(self, client, setup_users):
        """Test de création d'une demande d'objet"""
        user = setup_users["user"]
        request_data = {
            "name": "Chaudière Vaillant",
            "category": "heating",
            "brand": "Vaillant",
            "model": "ecoTEC plus",
            "notes": "Installation récente, garantie 2 ans"
        }
        
        response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == request_data["name"]
        assert data["category"] == request_data["category"]
        assert data["status"] == "pending"
        assert data["requester_id"] == user["id"]
    
    def test_get_object_requests(self, client, setup_users):
        """Test de récupération de toutes les demandes"""
        user = setup_users["user"]
        
        # Créer plusieurs demandes
        for i in range(3):
            request_data = {
                "name": f"Objet {i}",
                "category": "appliance",
            }
            client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        
        response = client.get("/objects/requests")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 3
    
    def test_get_pending_requests(self, client, setup_users):
        """Test de récupération des demandes en attente (admin)"""
        user = setup_users["user"]
        admin = setup_users["admin"]
        
        # Créer des demandes
        request_data = {
            "name": "Lave-vaisselle",
            "category": "appliance",
        }
        client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        
        response = client.get(f"/objects/admin/pending-requests?admin_id={admin['id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"
    
    def test_get_pending_requests_non_admin(self, client, setup_users):
        """Test qu'un utilisateur non-admin ne peut pas accéder aux demandes"""
        user = setup_users["user"]
        
        response = client.get(f"/objects/admin/pending-requests?admin_id={user['id']}")
        assert response.status_code == 403
        assert "administrateurs" in response.json()["detail"].lower()


class TestAdminDecisions:
    """Tests pour les décisions admin sur les demandes"""
    
    def test_admin_approve_request(self, client, setup_users):
        """Test d'approbation d'une demande par un admin"""
        user = setup_users["user"]
        admin = setup_users["admin"]
        
        # Créer une demande
        request_data = {
            "name": "Four Bosch",
            "category": "kitchen",
            "brand": "Bosch"
        }
        req_response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        request_id = req_response.json()["id"]
        
        # Approuver la demande
        decision = {
            "status": "approved",
            "admin_notes": "Demande validée - informations complètes"
        }
        response = client.put(
            f"/objects/requests/{request_id}/decide?admin_id={admin['id']}", 
            json=decision
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "approved"
        assert data["admin_notes"] == decision["admin_notes"]
        assert data["reviewed_by"] == admin["id"]
        
        # Vérifier que l'objet a été créé
        objects_response = client.get(f"/objects/?user_id={user['id']}")
        objects = objects_response.json()
        assert len(objects) == 1
        assert objects[0]["name"] == request_data["name"]
    
    def test_admin_reject_request(self, client, setup_users):
        """Test de rejet d'une demande par un admin"""
        user = setup_users["user"]
        admin = setup_users["admin"]
        
        # Créer une demande
        request_data = {
            "name": "Appareil inconnu",
            "category": "other"
        }
        req_response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        request_id = req_response.json()["id"]
        
        # Rejeter la demande
        decision = {
            "status": "rejected",
            "admin_notes": "Informations insuffisantes"
        }
        response = client.put(
            f"/objects/requests/{request_id}/decide?admin_id={admin['id']}", 
            json=decision
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "rejected"
        
        # Vérifier qu'aucun objet n'a été créé
        objects_response = client.get(f"/objects/?user_id={user['id']}")
        objects = objects_response.json()
        assert len(objects) == 0
    
    def test_non_admin_cannot_decide(self, client, setup_users):
        """Test qu'un utilisateur non-admin ne peut pas décider"""
        user = setup_users["user"]
        
        # Créer une demande
        request_data = {
            "name": "Test",
            "category": "other"
        }
        req_response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        request_id = req_response.json()["id"]
        
        # Tenter de décider avec un utilisateur non-admin
        decision = {
            "status": "approved"
        }
        response = client.put(
            f"/objects/requests/{request_id}/decide?admin_id={user['id']}", 
            json=decision
        )
        assert response.status_code == 403
    
    def test_cannot_decide_already_processed_request(self, client, setup_users):
        """Test qu'on ne peut pas décider deux fois sur la même demande"""
        user = setup_users["user"]
        admin = setup_users["admin"]
        
        # Créer une demande
        request_data = {
            "name": "Test",
            "category": "other"
        }
        req_response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        request_id = req_response.json()["id"]
        
        # Première décision
        decision = {
            "status": "approved"
        }
        client.put(
            f"/objects/requests/{request_id}/decide?admin_id={admin['id']}", 
            json=decision
        )
        
        # Tenter une deuxième décision
        decision2 = {
            "status": "rejected"
        }
        response = client.put(
            f"/objects/requests/{request_id}/decide?admin_id={admin['id']}", 
            json=decision2
        )
        assert response.status_code == 400
        assert "déjà été traitée" in response.json()["detail"]


class TestAdminDeleteRequest:
    """Tests pour la suppression de demandes par admin"""
    
    def test_admin_delete_request(self, client, setup_users):
        """Test de suppression d'une demande par un admin"""
        user = setup_users["user"]
        admin = setup_users["admin"]
        
        # Créer une demande
        request_data = {
            "name": "Test à supprimer",
            "category": "other"
        }
        req_response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        request_id = req_response.json()["id"]
        
        # Supprimer la demande
        response = client.delete(f"/objects/admin/requests/{request_id}?admin_id={admin['id']}")
        assert response.status_code == 200
        
        # Vérifier que la demande n'existe plus
        get_response = client.get(f"/objects/requests/{request_id}")
        assert get_response.status_code == 404
    
    def test_non_admin_cannot_delete(self, client, setup_users):
        """Test qu'un utilisateur non-admin ne peut pas supprimer"""
        user = setup_users["user"]
        
        # Créer une demande
        request_data = {
            "name": "Test",
            "category": "other"
        }
        req_response = client.post(f"/objects/requests?user_id={user['id']}", json=request_data)
        request_id = req_response.json()["id"]
        
        # Tenter de supprimer avec un utilisateur non-admin
        response = client.delete(f"/objects/admin/requests/{request_id}?admin_id={user['id']}")
        assert response.status_code == 403
