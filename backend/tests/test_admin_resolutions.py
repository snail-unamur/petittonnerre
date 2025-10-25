"""
Tests pour le soft delete des résolutions avec accès admin (US6.2)
"""
import pytest
from datetime import datetime, UTC
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
import models

# Configuration de la base de données de test
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
    """Créer un utilisateur admin"""
    admin = models.User(
        email="admin@test.com",
        username="admin",
        hashed_password="hashed_password",
        role=models.UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def normal_user(db_session):
    """Créer un utilisateur normal"""
    user = models.User(
        email="user@test.com",
        username="user",
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
        name="Test Object",
        category="heating",
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
        title="Test Problem",
        description="Test Description",
        category="mechanical",
        severity="medium",
        status="open",
        object_id=test_object.id,
        reported_by=normal_user.id
    )
    db_session.add(problem)
    db_session.commit()
    db_session.refresh(problem)
    return problem


@pytest.fixture
def test_resolution(db_session, test_problem, normal_user):
    """Créer une résolution de test"""
    resolution = models.ProblemResolution(
        solution="Test Solution",
        problem_id=test_problem.id,
        resolved_by=normal_user.id
    )
    db_session.add(resolution)
    db_session.commit()
    db_session.refresh(resolution)
    return resolution


# Tests US6.2.1 - Champ deleted_at dans le modèle
def test_resolution_has_deleted_at_field(test_resolution):
    """Vérifier que le modèle ProblemResolution a un champ deleted_at"""
    assert hasattr(test_resolution, 'deleted_at')
    assert test_resolution.deleted_at is None


# Tests US6.2.2 et US6.2.3 - Endpoint admin DELETE et soft delete
def test_admin_can_soft_delete_resolution(db_session, admin_user, test_resolution):
    """Un admin peut soft delete une résolution"""
    response = client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Résolution supprimée avec succès"
    assert data["resolution_id"] == test_resolution.id
    assert "deleted_at" in data
    
    # Vérifier dans la DB
    db_session.refresh(test_resolution)
    assert test_resolution.deleted_at is not None


def test_non_admin_cannot_soft_delete_resolution(db_session, normal_user, test_resolution):
    """Un utilisateur non-admin ne peut pas soft delete une résolution"""
    response = client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={normal_user.id}")
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès réservé aux administrateurs"
    
    # Vérifier dans la DB que rien n'a changé
    db_session.refresh(test_resolution)
    assert test_resolution.deleted_at is None


def test_cannot_delete_already_deleted_resolution(db_session, admin_user, test_resolution):
    """Ne peut pas supprimer une résolution déjà supprimée"""
    # Première suppression
    client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    
    # Tentative de deuxième suppression
    response = client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "La résolution est déjà supprimée"


def test_delete_nonexistent_resolution(admin_user):
    """Supprimer une résolution inexistante retourne 404"""
    response = client.delete(f"/problems/admin/resolutions/99999?admin_id={admin_user.id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Résolution non trouvée"


# Tests US6.2.4 - Exclusion des résolutions supprimées
def test_deleted_resolutions_excluded_from_list(db_session, admin_user, test_problem, test_resolution):
    """Les résolutions supprimées ne doivent pas apparaître dans la liste normale"""
    # Vérifier que la résolution apparaît d'abord
    response = client.get(f"/problems/{test_problem.id}/resolutions")
    assert response.status_code == 200
    resolutions = response.json()
    assert len(resolutions) == 1
    assert resolutions[0]["id"] == test_resolution.id
    
    # Supprimer la résolution
    client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    
    # Vérifier qu'elle n'apparaît plus
    response = client.get(f"/problems/{test_problem.id}/resolutions")
    assert response.status_code == 200
    resolutions = response.json()
    assert len(resolutions) == 0


# Tests admin interface
def test_admin_can_list_deleted_resolutions(db_session, admin_user, test_problem, normal_user):
    """Un admin peut lister les résolutions supprimées"""
    # Créer 3 résolutions
    resolution1 = models.ProblemResolution(
        solution="Solution 1",
        problem_id=test_problem.id,
        resolved_by=normal_user.id
    )
    resolution2 = models.ProblemResolution(
        solution="Solution 2",
        problem_id=test_problem.id,
        resolved_by=normal_user.id
    )
    resolution3 = models.ProblemResolution(
        solution="Solution 3",
        problem_id=test_problem.id,
        resolved_by=normal_user.id
    )
    db_session.add_all([resolution1, resolution2, resolution3])
    db_session.commit()
    db_session.refresh(resolution1)
    db_session.refresh(resolution2)
    
    # Supprimer 2 résolutions
    client.delete(f"/problems/admin/resolutions/{resolution1.id}?admin_id={admin_user.id}")
    client.delete(f"/problems/admin/resolutions/{resolution2.id}?admin_id={admin_user.id}")
    
    # Lister les résolutions supprimées
    response = client.get(f"/problems/admin/resolutions/deleted?admin_id={admin_user.id}")
    
    assert response.status_code == 200
    deleted_resolutions = response.json()
    assert len(deleted_resolutions) == 2
    deleted_ids = [r["id"] for r in deleted_resolutions]
    assert resolution1.id in deleted_ids
    assert resolution2.id in deleted_ids


def test_admin_can_restore_resolution(db_session, admin_user, test_resolution):
    """Un admin peut restaurer une résolution supprimée"""
    # Supprimer d'abord
    client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    db_session.refresh(test_resolution)
    assert test_resolution.deleted_at is not None
    
    # Restaurer
    response = client.post(f"/problems/admin/resolutions/{test_resolution.id}/restore?admin_id={admin_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Résolution restaurée avec succès"
    assert data["resolution_id"] == test_resolution.id
    
    # Vérifier dans la DB
    db_session.refresh(test_resolution)
    assert test_resolution.deleted_at is None


def test_cannot_restore_non_deleted_resolution(admin_user, test_resolution):
    """Ne peut pas restaurer une résolution non supprimée"""
    response = client.post(f"/problems/admin/resolutions/{test_resolution.id}/restore?admin_id={admin_user.id}")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "La résolution n'est pas supprimée"


def test_non_admin_cannot_view_deleted_resolutions(normal_user):
    """Un utilisateur non-admin ne peut pas voir les résolutions supprimées"""
    response = client.get(f"/problems/admin/resolutions/deleted?admin_id={normal_user.id}")
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès réservé aux administrateurs"


def test_non_admin_cannot_restore_resolution(db_session, admin_user, normal_user, test_resolution):
    """Un utilisateur non-admin ne peut pas restaurer une résolution"""
    # Supprimer d'abord (en tant qu'admin)
    client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    
    # Tenter de restaurer (en tant que user normal)
    response = client.post(f"/problems/admin/resolutions/{test_resolution.id}/restore?admin_id={normal_user.id}")
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès réservé aux administrateurs"


# Test workflow complet
def test_complete_soft_delete_workflow(db_session, admin_user, test_problem, test_resolution):
    """Test du workflow complet de soft delete et restauration"""
    # 1. La résolution existe et est visible
    response = client.get(f"/problems/{test_problem.id}/resolutions")
    assert len(response.json()) == 1
    
    # 2. Admin supprime la résolution
    response = client.delete(f"/problems/admin/resolutions/{test_resolution.id}?admin_id={admin_user.id}")
    assert response.status_code == 200
    
    # 3. La résolution n'apparaît plus dans la liste normale
    response = client.get(f"/problems/{test_problem.id}/resolutions")
    assert len(response.json()) == 0
    
    # 4. La résolution apparaît dans la liste admin des supprimées
    response = client.get(f"/problems/admin/resolutions/deleted?admin_id={admin_user.id}")
    assert len(response.json()) == 1
    
    # 5. Admin restaure la résolution
    response = client.post(f"/problems/admin/resolutions/{test_resolution.id}/restore?admin_id={admin_user.id}")
    assert response.status_code == 200
    
    # 6. La résolution réapparaît dans la liste normale
    response = client.get(f"/problems/{test_problem.id}/resolutions")
    assert len(response.json()) == 1
    
    # 7. La résolution ne figure plus dans la liste des supprimées
    response = client.get(f"/problems/admin/resolutions/deleted?admin_id={admin_user.id}")
    assert len(response.json()) == 0
