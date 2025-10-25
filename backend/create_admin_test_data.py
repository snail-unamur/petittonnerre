"""
Script pour créer des données de test pour le dashboard admin
"""
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import User, UserRole, ObjectRequest, ObjectRequestStatus, ObjectCategory
import bcrypt
from datetime import datetime, UTC

def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt directement"""
    # Bcrypt a une limite de 72 bytes
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def create_test_data():
    """Créer des demandes d'objets pour tester le dashboard admin"""
    db = SessionLocal()
    
    try:
        # Récupérer l'admin existant
        admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if not admin:
            print("❌ Aucun admin trouvé dans la base. Créez d'abord un admin.")
            return
        
        print(f"ℹ️  Admin trouvé: {admin.username} ({admin.email})")
        
        # Récupérer les utilisateurs normaux
        users = db.query(User).filter(User.role == UserRole.USER).limit(3).all()
        if not users:
            # Créer quelques utilisateurs normaux
            for i in range(3):
                email = f"testuser{i+1}@example.com"
                user_exists = db.query(User).filter(User.email == email).first()
                if not user_exists:
                    user = User(
                        email=email,
                        username=f"testuser{i+1}",
                        hashed_password=hash_password("User1234!"),
                        role=UserRole.USER,
                        is_active=True,
                        location="Bruxelles" if i % 2 == 0 else "Liège"
                    )
                    db.add(user)
                    users.append(user)
            db.commit()
            print(f"✅ {len(users)} utilisateurs test créés")
        else:
            print(f"ℹ️  {len(users)} utilisateurs existants utilisés")
        
        # Créer des demandes d'objets en attente
        requests_data = [
            {
                "name": "Chaudière Vaillant ecoTEC",
                "category": ObjectCategory.HEATING,
                "brand": "Vaillant",
                "model": "ecoTEC plus VCW 346/5-5",
                "notes": "Installation récente, garantie 2 ans. Besoin de conseils pour l'entretien annuel.",
                "requester_id": users[0].id if users else 1
            },
            {
                "name": "Lave-vaisselle Bosch",
                "category": ObjectCategory.APPLIANCE,
                "brand": "Bosch",
                "model": "SMS46GI01E",
                "notes": "Acheté en 2020, fonctionne bien mais fait du bruit parfois.",
                "requester_id": users[1].id if len(users) > 1 else 1
            },
            {
                "name": "Four encastrable Siemens",
                "category": ObjectCategory.KITCHEN,
                "brand": "Siemens",
                "model": "HB634GBS1",
                "purchase_date": datetime(2021, 6, 15),
                "manual_url": "https://example.com/manual-siemens.pdf",
                "notes": "Fonction pyrolyse, besoin de conseils pour le nettoyage.",
                "requester_id": users[2].id if len(users) > 2 else 1
            },
            {
                "name": "Pierre bleue escalier",
                "category": ObjectCategory.FLOORING,
                "notes": "Pierre bleue belge, escalier intérieur. Comment l'entretenir sans l'abîmer ?",
                "requester_id": users[0].id if users else 1
            },
            {
                "name": "Pompe de relevage",
                "category": ObjectCategory.BATHROOM,
                "brand": "Grundfos",
                "model": "Sololift2 WC-3",
                "notes": "Installée dans la cave, pour WC suspendu.",
                "requester_id": users[1].id if len(users) > 1 else 1
            }
        ]
        
        requests_created = 0
        for req_data in requests_data:
            # Vérifier si une demande similaire existe déjà
            existing = db.query(ObjectRequest).filter(
                ObjectRequest.name == req_data["name"],
                ObjectRequest.requester_id == req_data["requester_id"]
            ).first()
            
            if not existing:
                request = ObjectRequest(**req_data)
                db.add(request)
                requests_created += 1
        
        db.commit()
        print(f"✅ {requests_created} demandes d'objets créées")
        
        # Afficher les statistiques
        total_requests = db.query(ObjectRequest).count()
        pending_requests = db.query(ObjectRequest).filter(
            ObjectRequest.status == ObjectRequestStatus.PENDING
        ).count()
        
        print(f"\n📊 Statistiques:")
        print(f"   - Total demandes: {total_requests}")
        print(f"   - En attente: {pending_requests}")
        print(f"\n🔐 Pour tester le dashboard admin:")
        print(f"   URL: http://localhost:4200/admin/auth")
        print(f"   Code temporaire: admin123")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
