"""
Script principal pour initialiser les données de test (utilisateurs normaux + admin + données de démonstration)
Usage: python init_data.py [--users-only | --full]
"""
import sys
from passlib.context import CryptContext
import requests
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, UserRole, ObjectRequest, ObjectCategory

BASE_URL = "http://localhost:8000"

# Configuration du hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash un mot de passe avec passlib/bcrypt"""
    return pwd_context.hash(password)


def create_base_users():
    """Créer les utilisateurs de base (admin + utilisateurs normaux) directement en base"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("👥 CRÉATION DES UTILISATEURS DE BASE")
        print("=" * 60)
        
        # 1. Créer un admin si inexistant
        admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if not admin:
            admin = User(
                email="admin@petittonnerre.com",
                username="admin",
                hashed_password=hash_password("Admin1234!"),
                role=UserRole.ADMIN,
                is_active=True,
                location="Système"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"✅ Admin créé: {admin.email}")
            print(f"   Password: Admin1234!")
        else:
            print(f"ℹ️  Admin existant: {admin.email}")
        
        # 2. Créer des utilisateurs de test
        test_users = [
            ("alice@example.com", "alice", "Password123!", "Bruxelles"),
            ("bob@example.com", "bob", "Password123!", "Liège"),
            ("charlie@example.com", "charlie", "Password123!", "Namur"),
        ]
        
        created_users = [admin]
        for email, username, password, location in test_users:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    username=username,
                    hashed_password=hash_password(password),
                    role=UserRole.USER,
                    is_active=True,
                    location=location
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"✅ Utilisateur créé: {email}")
            else:
                print(f"ℹ️  Utilisateur existant: {email}")
            created_users.append(user)
        
        print(f"\n✅ Total: {len(created_users)} utilisateurs (1 admin + {len(created_users)-1} users)")
        return created_users
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        return []
    finally:
        db.close()


def create_base_templates():
    """Créer des templates d'objets de base directement en base"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 60)
        print("📦 CRÉATION DES TEMPLATES D'OBJETS")
        print("=" * 60)
        
        templates_data = [
            {
                "name": "Chaudière Vaillant ecoTEC plus",
                "category": ObjectCategory.HEATING,
                "brand": "Vaillant",
                "model": "ecoTEC plus",
                "description": "Chaudière gaz à condensation haute performance",
                "is_validated": True
            },
            {
                "name": "Four Samsung pyrolyse",
                "category": ObjectCategory.KITCHEN,
                "brand": "Samsung",
                "model": "NV75N5671RS",
                "description": "Four encastrable avec fonction pyrolyse",
                "is_validated": True
            },
            {
                "name": "Lave-vaisselle Bosch",
                "category": ObjectCategory.APPLIANCE,
                "brand": "Bosch",
                "model": "SMV46KX00E",
                "description": "Lave-vaisselle encastrable silencieux",
                "is_validated": True
            },
            {
                "name": "Robinet Grohe Eurosmart",
                "category": ObjectCategory.BATHROOM,
                "brand": "Grohe",
                "model": "Eurosmart",
                "description": "Mitigeur lavabo chromé",
                "is_validated": True
            },
            {
                "name": "Pierre bleue belge",
                "category": ObjectCategory.OTHER,  # Changé de FLOORING à OTHER
                "description": "Pierre bleue naturelle pour terrasse/escalier",
                "is_validated": True
            },
        ]
        
        created = 0
        for template_data in templates_data:
            existing = db.query(ObjectTemplate).filter(
                ObjectTemplate.name == template_data["name"]
            ).first()
            
            if not existing:
                template = ObjectTemplate(**template_data)
                db.add(template)
                created += 1
        
        db.commit()
        print(f"✅ {created} templates créés")
        return created
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        return 0
    finally:
        db.close()


def create_object_requests(users):
    """Créer des demandes d'objets pour l'admin"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 60)
        print("📝 CRÉATION DES DEMANDES D'OBJETS")
        print("=" * 60)
        
        if len(users) < 2:
            print("⚠️  Pas assez d'utilisateurs pour créer des demandes")
            return 0
        
        requests_data = [
            {
                "name": "Pompe de relevage Grundfos",
                "category": ObjectCategory.BATHROOM,
                "brand": "Grundfos",
                "model": "Sololift2 WC-3",
                "notes": "Pour WC suspendu dans la cave",
                "requester_id": users[1].id
            },
            {
                "name": "Radiateur acier",
                "category": ObjectCategory.HEATING,
                "brand": "Radson",
                "model": "Compact",
                "notes": "Radiateurs panneau double",
                "requester_id": users[2].id if len(users) > 2 else users[1].id
            },
        ]
        
        created = 0
        for req_data in requests_data:
            existing = db.query(ObjectRequest).filter(
                ObjectRequest.name == req_data["name"],
                ObjectRequest.requester_id == req_data["requester_id"]
            ).first()
            
            if not existing:
                request = ObjectRequest(**req_data)
                db.add(request)
                created += 1
        
        db.commit()
        print(f"✅ {created} demandes créées")
        return created
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        return 0
    finally:
        db.close()


def create_full_demo_data():
    """Créer des données complètes de démonstration via l'API"""
    print("\n" + "=" * 60)
    print("🎬 CRÉATION DES DONNÉES DE DÉMONSTRATION")
    print("=" * 60)
    
    try:
        # Récupérer les utilisateurs créés
        db = SessionLocal()
        users = db.query(User).filter(User.role == UserRole.USER).limit(3).all()
        db.close()
        
        if len(users) < 1:
            print("⚠️  Pas d'utilisateurs disponibles")
            return
        
        user_id = users[0].id
        
        # 1. Créer des objets
        print("\n🏠 Création d'objets...")
        objects_data = [
            {"template_id": 1, "notes": "Installation 2020, entretien annuel OK"},
            {"template_id": 2, "notes": "Achat 2022"},
            {"template_id": 3, "notes": "Sous garantie"},
        ]
        
        created_objects = []
        for obj_data in objects_data:
            try:
                response = requests.post(
                    f"{BASE_URL}/objects/from-template?user_id={user_id}",
                    json=obj_data,
                    timeout=5
                )
                if response.status_code in [200, 201]:
                    created_objects.append(response.json())
                    print(f"✅ Objet créé depuis template {obj_data['template_id']}")
            except:
                pass
        
        # 2. Créer des problèmes
        if created_objects:
            print("\n🚨 Création de problèmes...")
            problems_data = [
                {
                    "title": "Chaudière qui fait du bruit",
                    "description": "Claquements au démarrage",
                    "category": "noise",
                    "severity": "medium",
                    "object_id": created_objects[0]["id"]
                },
                {
                    "title": "Four ne chauffe pas uniformément",
                    "description": "Le haut brûle, le bas reste cru",
                    "category": "heating_cooling",
                    "severity": "medium",
                    "object_id": created_objects[1]["id"] if len(created_objects) > 1 else created_objects[0]["id"]
                },
            ]
            
            for problem_data in problems_data:
                try:
                    response = requests.post(
                        f"{BASE_URL}/problems/?user_id={user_id}",
                        json=problem_data,
                        timeout=5
                    )
                    if response.status_code in [200, 201]:
                        print(f"✅ Problème créé: {problem_data['title']}")
                except:
                    pass
        
        # 3. Créer des conseils d'entretien
        print("\n📋 Création de conseils...")
        advice_data = [
            {
                "title": "Contrôle annuel chaudière",
                "description": "Vérification obligatoire par technicien agréé",
                "frequency_days": 365,
                "category": "heating"
            },
            {
                "title": "Nettoyage four",
                "description": "Cycle pyrolyse tous les 3 mois",
                "frequency_days": 90,
                "category": "kitchen"
            },
        ]
        
        for advice in advice_data:
            try:
                response = requests.post(f"{BASE_URL}/maintenance/advice", json=advice, timeout=5)
                if response.status_code in [200, 201]:
                    print(f"✅ Conseil créé: {advice['title']}")
            except:
                pass
        
        print("\n✅ Données de démonstration créées")
        
    except Exception as e:
        print(f"⚠️  Impossible de créer toutes les données de démo: {e}")


def main():
    """Point d'entrée principal"""
    mode = sys.argv[1] if len(sys.argv) > 1 else "--full"
    
    print("\n" + "=" * 60)
    print("🚀 INITIALISATION DES DONNÉES - PETIT TONNERRE")
    print("=" * 60)
    
    # Toujours créer les utilisateurs et templates de base
    users = create_base_users()
    create_base_templates()
    
    if mode == "--users-only":
        print("\n✅ Mode 'users-only' : Seulement les utilisateurs créés")
    else:
        # Mode complet : ajouter demandes et démo
        create_object_requests(users)
        create_full_demo_data()
    
    print("\n" + "=" * 60)
    print("✅ INITIALISATION TERMINÉE")
    print("=" * 60)
    print("\n🔐 Comptes créés:")
    print("   Admin: admin@petittonnerre.com / Admin1234!")
    print("   User:  alice@example.com / Password123!")
    print("\n🌐 URLs:")
    print(f"   API:  {BASE_URL}/docs")
    print("   App:  http://localhost:4200")
    print("   Admin: http://localhost:4200/admin/auth (code: admin123)")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
