from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from api import users, objects, maintenance, community, problems, auth
from enrich_objects import auto_enrich_on_startup
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Créer les tables
models.Base.metadata.create_all(bind=engine)

# Enrichissement automatique au démarrage
try:
    db = SessionLocal()
    auto_enrich_on_startup(db)
except Exception as e:
    logger.error(f"Erreur lors de l'enrichissement automatique: {e}")
finally:
    if 'db' in locals():
        db.close()

app = FastAPI(
    title="Petit Tonnerre API",
    description="API pour la gestion d'entretien d'objets domestiques",
    version="1.0.0"
)

# Configuration CORS pour Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular dev server local
        "http://frontend:4200",   # Service frontend dans Docker
        "http://localhost:80",    # Frontend via Docker
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)

# Inclure les routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(objects.router)
app.include_router(maintenance.router)
app.include_router(community.router)
app.include_router(problems.router)


@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API Petit Tonnerre",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/admin/create-test-requests")
def create_test_requests():
    """Endpoint temporaire pour créer des demandes d'objets de test"""
    from datetime import datetime, UTC
    from auth import get_password_hash
    
    db = SessionLocal()
    try:
        # Récupérer les utilisateurs normaux
        users = db.query(models.User).filter(models.User.role == models.UserRole.user).limit(3).all()
        
        if not users:
            # Créer quelques utilisateurs normaux si nécessaire
            for i in range(3):
                email = f"testuser{i+1}@example.com"
                user_exists = db.query(models.User).filter(models.User.email == email).first()
                if not user_exists:
                    user = models.User(
                        email=email,
                        username=f"testuser{i+1}",
                        hashed_password=get_password_hash("User1234!"),
                        role=models.UserRole.user,
                        is_active=True,
                        location="Bruxelles" if i % 2 == 0 else "Liège"
                    )
                    db.add(user)
                    users.append(user)
            db.commit()
        
        # Créer des demandes d'objets en attente
        requests_data = [
            {
                "name": "Chaudière Vaillant ecoTEC",
                "category": models.ObjectCategory.HEATING,
                "brand": "Vaillant",
                "model": "ecoTEC plus VCW 346/5-5",
                "notes": "Installation récente, garantie 2 ans. Besoin de conseils pour l'entretien annuel.",
                "requester_id": users[0].id if users else 1
            },
            {
                "name": "Lave-vaisselle Bosch",
                "category": models.ObjectCategory.APPLIANCE,
                "brand": "Bosch",
                "model": "SMS46GI01E",
                "notes": "Acheté en 2020, fonctionne bien mais fait du bruit parfois.",
                "requester_id": users[1].id if len(users) > 1 else 1
            },
            {
                "name": "Four encastrable Siemens",
                "category": models.ObjectCategory.KITCHEN,
                "brand": "Siemens",
                "model": "HB634GBS1",
                "purchase_date": datetime(2021, 6, 15),
                "manual_url": "https://example.com/manual-siemens.pdf",
                "notes": "Fonction pyrolyse, besoin de conseils pour le nettoyage.",
                "requester_id": users[2].id if len(users) > 2 else 1
            },
            {
                "name": "Pierre bleue escalier",
                "category": models.ObjectCategory.FLOORING,
                "notes": "Pierre bleue belge, escalier intérieur. Comment l'entretenir sans l'abîmer ?",
                "requester_id": users[0].id if users else 1
            },
            {
                "name": "Pompe de relevage",
                "category": models.ObjectCategory.BATHROOM,
                "brand": "Grundfos",
                "model": "Sololift2 WC-3",
                "notes": "Installée dans la cave, pour WC suspendu.",
                "requester_id": users[1].id if len(users) > 1 else 1
            }
        ]
        
        requests_created = 0
        for req_data in requests_data:
            # Vérifier si une demande similaire existe déjà en attente
            existing = db.query(models.ObjectRequest).filter(
                models.ObjectRequest.name == req_data["name"],
                models.ObjectRequest.status == models.ObjectRequestStatus.PENDING
            ).first()
            
            if not existing:
                request = models.ObjectRequest(**req_data)
                db.add(request)
                requests_created += 1
        
        db.commit()
        
        # Statistiques
        total_requests = db.query(models.ObjectRequest).count()
        pending_requests = db.query(models.ObjectRequest).filter(
            models.ObjectRequest.status == models.ObjectRequestStatus.PENDING
        ).count()
        
        return {
            "status": "success",
            "requests_created": requests_created,
            "total_requests": total_requests,
            "pending_requests": pending_requests
        }
        
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()