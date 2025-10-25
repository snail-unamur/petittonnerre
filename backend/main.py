from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from api import users, objects, maintenance, community

# Créer les tables
models.Base.metadata.create_all(bind=engine)

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
app.include_router(users.router)
app.include_router(objects.router)
app.include_router(maintenance.router)
app.include_router(community.router)


@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API Petit Tonnerre",
        "version": "1.0.0",
        "docs": "/docs"
    }