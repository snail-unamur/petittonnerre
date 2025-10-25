import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app
from database import get_db, Base, engine
from sqlalchemy.orm import Session
import models

client = TestClient(app)


# Configuration de la base de données de test
@pytest.fixture(scope="function")
def test_db():
    """Crée une nouvelle base de données pour chaque test"""
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(test_db: Session):
    """Crée un utilisateur de test"""
    from auth import get_password_hash
    
    user = models.User(
        email="testmaintenance@example.com",
        username="testmaintenanceuser",
        hashed_password=get_password_hash("password123"),
        role=models.UserRole.USER,
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_object(test_db: Session, test_user):
    """Crée un objet de test"""
    obj = models.Object(
        name="Chaudière Test",
        category=models.ObjectCategory.HEATING,
        brand="TestBrand",
        model="TestModel",
        owner_id=test_user.id,
        status="active"
    )
    test_db.add(obj)
    test_db.commit()
    test_db.refresh(obj)
    return obj


@pytest.fixture
def test_advice(test_db: Session):
    """Crée un conseil d'entretien de test"""
    advice = models.MaintenanceAdvice(
        title="Entretien annuel",
        description="Vérifier et nettoyer la chaudière",
        frequency_days=365,
        category=models.ObjectCategory.HEATING,
        is_validated=True
    )
    test_db.add(advice)
    test_db.commit()
    test_db.refresh(advice)
    return advice


@pytest.fixture
def test_maintenance_task(test_db: Session, test_user, test_object, test_advice):
    """Crée une tâche de maintenance de test"""
    task = models.MaintenanceTask(
        name="Entretien chaudière",
        scheduled_date=datetime.now() + timedelta(days=7),
        status=models.MaintenanceStatus.PENDING,
        object_id=test_object.id,
        user_id=test_user.id,
        advice_id=test_advice.id,
        notes="Test task"
    )
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)
    return task


def test_create_maintenance_advice(test_db: Session):
    """Test de création d'un conseil d'entretien"""
    advice_data = {
        "title": "Nettoyage mensuel",
        "description": "Nettoyer les filtres",
        "frequency_days": 30,
        "category": "heating"
    }
    
    response = client.post("/maintenance/advice", json=advice_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == advice_data["title"]
    assert data["description"] == advice_data["description"]
    assert data["is_validated"] is False


def test_get_maintenance_advice(test_db: Session, test_advice):
    """Test de récupération des conseils d'entretien"""
    response = client.get("/maintenance/advice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(advice["id"] == test_advice.id for advice in data)


def test_get_maintenance_advice_by_category(test_db: Session, test_advice):
    """Test de récupération des conseils par catégorie"""
    response = client.get("/maintenance/advice?category=heating")
    assert response.status_code == 200
    data = response.json()
    assert all(advice["category"] == "heating" for advice in data)


def test_create_maintenance_task(test_db: Session, test_user, test_object, test_advice):
    """Test de création d'une tâche de maintenance"""
    task_data = {
        "name": "Entretien test",
        "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "object_id": test_object.id,
        "advice_id": test_advice.id,
        "notes": "Notes de test"
    }
    
    response = client.post(f"/maintenance/tasks?user_id={test_user.id}", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == task_data["name"]
    assert data["status"] == "pending"
    assert data["object_id"] == test_object.id


def test_get_maintenance_tasks(test_db: Session, test_maintenance_task):
    """Test de récupération des tâches de maintenance"""
    response = client.get("/maintenance/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(task["id"] == test_maintenance_task.id for task in data)


def test_get_maintenance_tasks_by_user(test_db: Session, test_user, test_maintenance_task):
    """Test de récupération des tâches par utilisateur"""
    response = client.get(f"/maintenance/tasks?user_id={test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert all(task["user_id"] == test_user.id for task in data)


def test_get_maintenance_tasks_by_status(test_db: Session, test_maintenance_task):
    """Test de récupération des tâches par statut"""
    response = client.get("/maintenance/tasks?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert all(task["status"] == "pending" for task in data)


def test_update_maintenance_task_to_completed(test_db: Session, test_maintenance_task):
    """Test de mise à jour d'une tâche vers le statut 'completed'"""
    update_data = {
        "status": "completed",
        "completed_date": datetime.now().isoformat(),
        "notes": "Tâche terminée avec succès",
        "was_successful": True
    }
    
    response = client.patch(f"/maintenance/tasks/{test_maintenance_task.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_date"] is not None
    assert data["was_successful"] is True


def test_update_completed_task_to_pending(test_db: Session, test_maintenance_task):
    """Test de modification d'une tâche terminée vers le statut 'pending'"""
    # D'abord, compléter la tâche
    complete_data = {
        "status": "completed",
        "completed_date": datetime.now().isoformat(),
        "was_successful": True
    }
    
    response = client.patch(f"/maintenance/tasks/{test_maintenance_task.id}", json=complete_data)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    
    # Ensuite, remettre la tâche en attente
    reset_data = {
        "status": "pending",
        "completed_date": None,
        "notes": "Tâche remise en attente"
    }
    
    response = client.patch(f"/maintenance/tasks/{test_maintenance_task.id}", json=reset_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    # La completed_date devrait être None ou absente
    assert data.get("completed_date") is None


def test_update_task_with_issue_reported(test_db: Session, test_maintenance_task):
    """Test de mise à jour d'une tâche avec un problème signalé"""
    update_data = {
        "status": "issue_reported",
        "was_successful": False,
        "issues_encountered": "Problème détecté lors de l'entretien"
    }
    
    response = client.patch(f"/maintenance/tasks/{test_maintenance_task.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "issue_reported"
    assert data["was_successful"] is False
    assert data["issues_encountered"] is not None


def test_get_single_task(test_db: Session, test_maintenance_task):
    """Test de récupération d'une tâche spécifique"""
    response = client.get(f"/maintenance/tasks/{test_maintenance_task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_maintenance_task.id
    assert data["name"] == test_maintenance_task.name


def test_get_nonexistent_task(test_db: Session):
    """Test de récupération d'une tâche inexistante"""
    response = client.get("/maintenance/tasks/99999")
    assert response.status_code == 404
    assert "Tâche non trouvée" in response.json()["detail"]


def test_create_task_with_nonexistent_object(test_db: Session, test_user, test_advice):
    """Test de création d'une tâche avec un objet inexistant"""
    task_data = {
        "name": "Entretien test",
        "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "object_id": 99999,
        "advice_id": test_advice.id
    }
    
    response = client.post(f"/maintenance/tasks?user_id={test_user.id}", json=task_data)
    assert response.status_code == 404
    assert "Objet non trouvé" in response.json()["detail"]


def test_create_task_with_nonexistent_advice(test_db: Session, test_user, test_object):
    """Test de création d'une tâche avec un conseil inexistant"""
    task_data = {
        "name": "Entretien test",
        "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "object_id": test_object.id,
        "advice_id": 99999
    }
    
    response = client.post(f"/maintenance/tasks?user_id={test_user.id}", json=task_data)
    assert response.status_code == 404
    assert "Conseil non trouvé" in response.json()["detail"]
