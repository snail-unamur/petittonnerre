"""
Script de migration pour ajouter la table object_requests
"""
from sqlalchemy import create_engine
from database import Base, SQLALCHEMY_DATABASE_URL
import models

def migrate():
    """Créer la nouvelle table object_requests"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Créer uniquement la nouvelle table
    models.ObjectRequest.__table__.create(bind=engine, checkfirst=True)
    
    print("✅ Migration réussie: table 'object_requests' créée")

if __name__ == "__main__":
    migrate()
