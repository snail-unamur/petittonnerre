import pytest
from datetime import datetime, UTC
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app
import models

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
    """Créer les tables avant chaque test et les supprimer après"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Fournir une session de base de données pour les tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def admin_user(db_session):
    """Créer un utilisateur admin pour les tests"""
    admin = models.User(
        email="admin@test.com",
        username="admin",
        hashed_password="hashed_admin_password",
        role=models.UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def normal_user(db_session):
    """Créer un utilisateur normal pour les tests"""
    user = models.User(
        email="user@test.com",
        username="testuser",
        hashed_password="hashed_password",
        role=models.UserRole.USER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_object(db_session, normal_user):
    """Créer un objet de test"""
    obj = models.Object(
        name="Chaudière Test",
        category=models.ObjectCategory.HEATING,
        created_by=normal_user.id
    )
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj


@pytest.fixture
def test_problem(db_session, test_object, normal_user):
    """Créer un problème de test"""
    problem = models.Problem(
        title="Problème de test",
        description="Description du problème",
        category=models.ProblemCategory.NOISE,
        severity=models.ProblemSeverity.MEDIUM,
        object_id=test_object.id,
        reported_by=normal_user.id
    )
    db_session.add(problem)
    db_session.commit()
    db_session.refresh(problem)
    return problem


# Tests US6.1.1 - Champ deleted_at dans le modèle
def test_problem_has_deleted_at_field(db_session, test_problem):
    """Vérifier que le modèle Problem a bien un champ deleted_at"""
    assert hasattr(test_problem, 'deleted_at')
    assert test_problem.deleted_at is None  # Par défaut, None


# Tests US6.1.2 - Endpoint admin DELETE /admin/problems/{id}
def test_admin_can_soft_delete_problem(db_session, admin_user, test_problem):
    """Test qu'un admin peut supprimer un problème (soft delete)"""
    response = client.delete(
        f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Problème supprimé avec succès"
    assert data["problem_id"] == test_problem.id
    assert "deleted_at" in data
    
    # Vérifier en DB que deleted_at est bien défini
    db_session.refresh(test_problem)
    assert test_problem.deleted_at is not None


def test_non_admin_cannot_soft_delete_problem(db_session, normal_user, test_problem):
    """Test qu'un utilisateur normal ne peut pas supprimer un problème"""
    response = client.delete(
        f"/problems/admin/{test_problem.id}?admin_id={normal_user.id}"
    )
    
    assert response.status_code == 403
    assert "administrateurs" in response.json()["detail"].lower()


def test_cannot_delete_already_deleted_problem(db_session, admin_user, test_problem):
    """Test qu'on ne peut pas supprimer un problème déjà supprimé"""
    # Première suppression
    client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    # Deuxième tentative
    response = client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    assert response.status_code == 400
    assert "déjà supprimé" in response.json()["detail"].lower()


def test_delete_nonexistent_problem(db_session, admin_user):
    """Test de suppression d'un problème inexistant"""
    response = client.delete(f"/problems/admin/99999?admin_id={admin_user.id}")
    
    assert response.status_code == 404


# Tests US6.1.3 - Soft delete implementation
def test_soft_deleted_problem_has_timestamp(db_session, admin_user, test_problem):
    """Vérifier que le soft delete ajoute bien un timestamp"""
    before_delete = datetime.now(UTC)
    
    client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    db_session.refresh(test_problem)
    after_delete = datetime.now(UTC)
    
    assert test_problem.deleted_at is not None
    # SQLite stocke les datetimes sans timezone, on doit donc comparer en enlevant le tzinfo
    assert before_delete.replace(tzinfo=None) <= test_problem.deleted_at.replace(tzinfo=None) <= after_delete.replace(tzinfo=None)


# Tests US6.1.4 - Exclusion des problèmes supprimés
def test_deleted_problems_excluded_from_list(db_session, admin_user, test_problem):
    """Les problèmes supprimés ne doivent pas apparaître dans la liste normale"""
    # Vérifier que le problème apparaît d'abord
    response = client.get("/problems/")
    assert response.status_code == 200
    problems = response.json()
    assert len(problems) == 1
    assert problems[0]["id"] == test_problem.id
    
    # Supprimer le problème
    client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    # Vérifier qu'il n'apparaît plus
    response = client.get("/problems/")
    assert response.status_code == 200
    problems = response.json()
    assert len(problems) == 0


def test_deleted_problem_not_found_by_id(db_session, admin_user, test_problem):
    """Un problème supprimé ne peut pas être récupéré par son ID"""
    # Supprimer le problème
    client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    # Tenter de le récupérer
    response = client.get(f"/problems/{test_problem.id}")
    assert response.status_code == 404


# Tests US6.1.5 - Interface admin pour voir/restaurer
def test_admin_can_list_deleted_problems(db_session, admin_user, test_object, normal_user):
    """Admin peut voir la liste des problèmes supprimés"""
    # Créer plusieurs problèmes
    problem1 = models.Problem(
        title="Problème 1", description="Desc 1", category=models.ProblemCategory.NOISE,
        object_id=test_object.id, reported_by=normal_user.id
    )
    problem2 = models.Problem(
        title="Problème 2", description="Desc 2", category=models.ProblemCategory.LEAK,
        object_id=test_object.id, reported_by=normal_user.id
    )
    db_session.add_all([problem1, problem2])
    db_session.commit()
    
    # Supprimer le premier
    client.delete(f"/problems/admin/{problem1.id}?admin_id={admin_user.id}")
    
    # Récupérer la liste des supprimés
    response = client.get(f"/problems/admin/deleted?admin_id={admin_user.id}")
    assert response.status_code == 200
    deleted = response.json()
    assert len(deleted) == 1
    assert deleted[0]["id"] == problem1.id


def test_admin_can_restore_problem(db_session, admin_user, test_problem):
    """Admin peut restaurer un problème supprimé"""
    # Supprimer
    client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    # Vérifier qu'il est supprimé
    db_session.refresh(test_problem)
    assert test_problem.deleted_at is not None
    
    # Restaurer
    response = client.post(f"/problems/admin/{test_problem.id}/restore?admin_id={admin_user.id}")
    assert response.status_code == 200
    assert "restauré" in response.json()["message"].lower()
    
    # Vérifier qu'il est bien restauré
    db_session.refresh(test_problem)
    assert test_problem.deleted_at is None
    
    # Vérifier qu'il réapparaît dans la liste normale
    response = client.get("/problems/")
    problems = response.json()
    assert len(problems) == 1
    assert problems[0]["id"] == test_problem.id


def test_cannot_restore_non_deleted_problem(db_session, admin_user, test_problem):
    """Ne peut pas restaurer un problème qui n'est pas supprimé"""
    response = client.post(f"/problems/admin/{test_problem.id}/restore?admin_id={admin_user.id}")
    
    assert response.status_code == 400
    assert "pas supprimé" in response.json()["detail"].lower()


def test_non_admin_cannot_view_deleted_problems(db_session, normal_user):
    """Utilisateur normal ne peut pas voir les problèmes supprimés"""
    response = client.get(f"/problems/admin/deleted?admin_id={normal_user.id}")
    
    assert response.status_code == 403


def test_non_admin_cannot_restore_problem(db_session, normal_user, admin_user, test_problem):
    """Utilisateur normal ne peut pas restaurer un problème"""
    # Supprimer d'abord (avec admin)
    client.delete(f"/problems/admin/{test_problem.id}?admin_id={admin_user.id}")
    
    # Tenter de restaurer (avec user normal)
    response = client.post(f"/problems/admin/{test_problem.id}/restore?admin_id={normal_user.id}")
    
    assert response.status_code == 403


# Tests US6.1.6 - Tests complets
def test_complete_soft_delete_workflow(db_session, admin_user, test_problem):
    """Test du workflow complet: créer -> supprimer -> restaurer"""
    problem_id = test_problem.id
    
    # 1. Vérifier que le problème existe
    response = client.get(f"/problems/{problem_id}")
    assert response.status_code == 200
    
    # 2. Supprimer
    response = client.delete(f"/problems/admin/{problem_id}?admin_id={admin_user.id}")
    assert response.status_code == 200
    
    # 3. Vérifier qu'il n'est plus accessible
    response = client.get(f"/problems/{problem_id}")
    assert response.status_code == 404
    
    # 4. Vérifier qu'il apparaît dans la liste des supprimés
    response = client.get(f"/problems/admin/deleted?admin_id={admin_user.id}")
    assert response.status_code == 200
    deleted = response.json()
    assert any(p["id"] == problem_id for p in deleted)
    
    # 5. Restaurer
    response = client.post(f"/problems/admin/{problem_id}/restore?admin_id={admin_user.id}")
    assert response.status_code == 200
    
    # 6. Vérifier qu'il est de nouveau accessible
    response = client.get(f"/problems/{problem_id}")
    assert response.status_code == 200
    
    # 7. Vérifier qu'il n'est plus dans la liste des supprimés
    response = client.get(f"/problems/admin/deleted?admin_id={admin_user.id}")
    deleted = response.json()
    assert not any(p["id"] == problem_id for p in deleted)
