"""
Tests pour les endpoints de chat des problèmes
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app
import models
from datetime import datetime, UTC

# Base de données de test en mémoire
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
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


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Créer les tables pour les tests"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_users():
    """Créer des utilisateurs de test"""
    from auth import get_password_hash
    
    db = TestingSessionLocal()
    
    user1 = models.User(
        email="user1@test.com",
        username="user1",
        hashed_password=get_password_hash("password123"),
        role=models.UserRole.USER
    )
    user2 = models.User(
        email="user2@test.com",
        username="user2",
        hashed_password=get_password_hash("password123"),
        role=models.UserRole.USER
    )
    user3 = models.User(
        email="user3@test.com",
        username="user3",
        hashed_password=get_password_hash("password123"),
        role=models.UserRole.USER
    )
    
    db.add_all([user1, user2, user3])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    db.refresh(user3)
    
    result = {"user1": user1, "user2": user2, "user3": user3}
    
    yield result
    
    db.close()


@pytest.fixture
def test_object_and_problem(test_users):
    """Créer un objet et un problème partagés entre user1 et user2"""
    db = TestingSessionLocal()
    
    # Créer un objet
    obj = models.Object(
        name="Chaudière Test",
        category=models.ObjectCategory.HEATING,
        brand="TestBrand",
        created_by=test_users["user1"].id,
        status="active"
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    
    # Associer l'objet à user1 et user2
    db.execute(
        models.user_objects.insert().values(
            user_id=test_users["user1"].id,
            object_id=obj.id,
            added_at=datetime.now(UTC)
        )
    )
    db.execute(
        models.user_objects.insert().values(
            user_id=test_users["user2"].id,
            object_id=obj.id,
            added_at=datetime.now(UTC)
        )
    )
    db.commit()
    
    # Créer un problème sur cet objet
    problem = models.Problem(
        title="Problème de chauffe",
        description="La chaudière ne chauffe plus",
        category=models.ProblemCategory.HEATING_COOLING,
        severity=models.ProblemSeverity.HIGH,
        object_id=obj.id,
        reported_by=test_users["user1"].id
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)
    
    result = {"object": obj, "problem": problem}
    
    yield result
    
    db.close()


def test_get_chat_messages_success(test_users, test_object_and_problem):
    """Test: Récupérer les messages de chat d'un problème avec succès"""
    db = TestingSessionLocal()
    problem = test_object_and_problem["problem"]
    user1 = test_users["user1"]
    user2 = test_users["user2"]
    
    # Créer quelques messages de chat
    chat1 = models.ProblemChat(
        problem_id=problem.id,
        user_id=user1.id,
        message="Premier message de user1"
    )
    chat2 = models.ProblemChat(
        problem_id=problem.id,
        user_id=user2.id,
        message="Réponse de user2"
    )
    db.add_all([chat1, chat2])
    db.commit()
    
    # User1 récupère les messages
    response = client.get(f"/problems/{problem.id}/chat?user_id={user1.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["message"] == "Premier message de user1"
    assert data[0]["username"] == "user1"
    assert data[1]["message"] == "Réponse de user2"
    assert data[1]["username"] == "user2"
    
    db.close()


def test_get_chat_messages_no_access(test_users, test_object_and_problem):
    """Test: Récupérer les messages sans avoir accès à l'objet"""
    problem = test_object_and_problem["problem"]
    user3 = test_users["user3"]  # user3 n'a pas accès à l'objet
    
    response = client.get(f"/problems/{problem.id}/chat?user_id={user3.id}")
    
    assert response.status_code == 403
    assert "Vous n'avez pas accès à ce problème" in response.json()["detail"]


def test_get_chat_messages_problem_not_found(test_users):
    """Test: Récupérer les messages d'un problème inexistant"""
    user1 = test_users["user1"]
    
    response = client.get(f"/problems/99999/chat?user_id={user1.id}")
    
    assert response.status_code == 404
    assert "Problème non trouvé" in response.json()["detail"]


def test_send_chat_message_success(test_users, test_object_and_problem):
    """Test: Envoyer un message de chat avec succès"""
    db = TestingSessionLocal()
    problem = test_object_and_problem["problem"]
    user1 = test_users["user1"]
    
    message_data = {
        "message": "Nouveau message de test"
    }
    
    response = client.post(
        f"/problems/{problem.id}/chat?user_id={user1.id}",
        json=message_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Nouveau message de test"
    assert data["username"] == "user1"
    assert data["user_id"] == user1.id
    assert data["problem_id"] == problem.id
    
    # Vérifier que le message est bien dans la DB
    chat = db.query(models.ProblemChat).filter(
        models.ProblemChat.problem_id == problem.id,
        models.ProblemChat.user_id == user1.id
    ).first()
    assert chat is not None
    assert chat.message == "Nouveau message de test"
    
    db.close()


def test_send_chat_message_no_access(test_users, test_object_and_problem):
    """Test: Envoyer un message sans avoir accès à l'objet"""
    problem = test_object_and_problem["problem"]
    user3 = test_users["user3"]
    
    message_data = {
        "message": "Message interdit"
    }
    
    response = client.post(
        f"/problems/{problem.id}/chat?user_id={user3.id}",
        json=message_data
    )
    
    assert response.status_code == 403
    assert "Vous n'avez pas accès à ce problème" in response.json()["detail"]


def test_send_chat_message_problem_not_found(test_users):
    """Test: Envoyer un message sur un problème inexistant"""
    user1 = test_users["user1"]
    
    message_data = {
        "message": "Message sur problème inexistant"
    }
    
    response = client.post(
        f"/problems/99999/chat?user_id={user1.id}",
        json=message_data
    )
    
    assert response.status_code == 404
    assert "Problème non trouvé" in response.json()["detail"]


def test_chat_messages_exclude_deleted(test_users, test_object_and_problem):
    """Test: Les messages supprimés ne sont pas retournés"""
    db = TestingSessionLocal()
    problem = test_object_and_problem["problem"]
    user1 = test_users["user1"]
    
    # Créer un message normal et un message supprimé
    chat1 = models.ProblemChat(
        problem_id=problem.id,
        user_id=user1.id,
        message="Message visible"
    )
    chat2 = models.ProblemChat(
        problem_id=problem.id,
        user_id=user1.id,
        message="Message supprimé",
        deleted_at=datetime.now(UTC)
    )
    db.add_all([chat1, chat2])
    db.commit()
    
    response = client.get(f"/problems/{problem.id}/chat?user_id={user1.id}")
    
    assert response.status_code == 200
    data = response.json()
    # Ne devrait retourner que le message non supprimé
    assert len(data) == 1
    assert data[0]["message"] == "Message visible"
    
    db.close()


def test_chat_on_deleted_problem(test_users, test_object_and_problem):
    """Test: Impossible de chatter sur un problème supprimé"""
    db = TestingSessionLocal()
    problem = test_object_and_problem["problem"]
    user1 = test_users["user1"]
    
    # Récupérer le problème de la DB et le supprimer (soft delete)
    db_problem = db.query(models.Problem).filter(models.Problem.id == problem.id).first()
    db_problem.deleted_at = datetime.now(UTC)
    db.commit()
    
    # Essayer de récupérer les messages
    response = client.get(f"/problems/{problem.id}/chat?user_id={user1.id}")
    assert response.status_code == 404
    
    # Essayer d'envoyer un message
    message_data = {"message": "Test message"}
    response = client.post(
        f"/problems/{problem.id}/chat?user_id={user1.id}",
        json=message_data
    )
    assert response.status_code == 404
    
    db.close()


def test_multiple_users_chat(test_users, test_object_and_problem):
    """Test: Plusieurs utilisateurs peuvent chatter sur le même problème"""
    problem = test_object_and_problem["problem"]
    user1 = test_users["user1"]
    user2 = test_users["user2"]
    
    # User1 envoie un message
    response1 = client.post(
        f"/problems/{problem.id}/chat?user_id={user1.id}",
        json={"message": "Message de user1"}
    )
    assert response1.status_code == 201
    
    # User2 envoie un message
    response2 = client.post(
        f"/problems/{problem.id}/chat?user_id={user2.id}",
        json={"message": "Message de user2"}
    )
    assert response2.status_code == 201
    
    # Récupérer tous les messages
    response = client.get(f"/problems/{problem.id}/chat?user_id={user1.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user1"
    assert data[1]["username"] == "user2"
