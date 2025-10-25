"""
Script d'initialisation de la base de données
- Drop et recrée le schéma complet
- Crée les tables à partir des models SQLAlchemy
- Insère des données de test
"""
import sys
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy import text
from database import SessionLocal, engine
from models import (
    Base, User, UserRole, Object, ObjectCategory,
    Problem, ProblemCategory, ProblemSeverity, ProblemStatus,
    MaintenanceAdvice, MaintenanceTask, MaintenanceStatus
)

# Configuration du hachage de mot de passe
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash un mot de passe"""
    return pwd_context.hash(password)


def reset_database():
    """Drop et recrée le schéma complet"""
    print("=" * 60)
    print("🗑️  NETTOYAGE COMPLET DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    with engine.connect() as conn:
        # Drop le schéma public et le recrée
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO petittonnerre"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        conn.commit()
        print("✅ Schéma nettoyé")
    
    # Créer toutes les tables à partir des models
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées à partir des models")


def create_test_data():
    """Créer des données de test"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 60)
        print("👥 CRÉATION DES UTILISATEURS")
        print("=" * 60)
        
        # Admin
        admin = User(
            email="admin@petittonnerre.com",
            username="admin",
            hashed_password=hash_password("Admin1234!"),
            role=UserRole.ADMIN,
            is_active=True,
            location="Système"
        )
        db.add(admin)
        print(f"✅ Admin: {admin.email} / Admin1234!")
        
        # Utilisateurs normaux
        users_data = [
            ("alice@example.com", "alice", "Bruxelles"),
            ("bob@example.com", "bob", "Liège"),
            ("charlie@example.com", "charlie", "Namur"),
        ]
        
        users = []
        for email, username, location in users_data:
            user = User(
                email=email,
                username=username,
                hashed_password=hash_password("Password123!"),
                role=UserRole.USER,
                is_active=True,
                location=location
            )
            db.add(user)
            users.append(user)
            print(f"✅ User: {email} / Password123!")
        
        db.commit()
        
        # Refresh pour avoir les IDs
        db.refresh(admin)
        for user in users:
            db.refresh(user)
        
        print("\n" + "=" * 60)
        print("🏠 CRÉATION DES OBJETS")
        print("=" * 60)
        
        # Objets pour Admin, Alice et Bob (15 chacun)
        objects_data = [
            # 15 Objets de l'admin
            {"name": "Système de chauffage central", "category": ObjectCategory.HEATING, "brand": "Viessmann", "model": "Vitodens 200", "purchase_date": datetime(2018, 6, 1), "notes": "Installation complète", "owner_id": admin.id},
            {"name": "Carrelage pierre bleue", "category": ObjectCategory.FLOORING, "brand": "Carrières du Hainaut", "model": "Pierre bleue", "purchase_date": datetime(2015, 3, 15), "notes": "Terrasse", "owner_id": admin.id},
            {"name": "Radiateur chambre 1", "category": ObjectCategory.HEATING, "brand": "Radson", "model": "Compact", "purchase_date": datetime(2018, 6, 1), "notes": "Radiateur principal", "owner_id": admin.id},
            {"name": "Radiateur chambre 2", "category": ObjectCategory.HEATING, "brand": "Radson", "model": "Compact", "purchase_date": datetime(2018, 6, 1), "notes": "Radiateur secondaire", "owner_id": admin.id},
            {"name": "Lavabo salle de bain", "category": ObjectCategory.BATHROOM, "brand": "Villeroy & Boch", "model": "Subway", "purchase_date": datetime(2017, 2, 10), "notes": "Lavabo principal", "owner_id": admin.id},
            {"name": "WC suspendu", "category": ObjectCategory.BATHROOM, "brand": "Geberit", "model": "Duofix", "purchase_date": datetime(2017, 2, 10), "notes": "WC principal", "owner_id": admin.id},
            {"name": "Douche italienne", "category": ObjectCategory.BATHROOM, "brand": "Hansgrohe", "model": "Raindance", "purchase_date": datetime(2017, 2, 10), "notes": "Douche principale", "owner_id": admin.id},
            {"name": "Hotte aspirante", "category": ObjectCategory.KITCHEN, "brand": "Siemens", "model": "LC97BHM50", "purchase_date": datetime(2019, 5, 20), "notes": "Hotte murale", "owner_id": admin.id},
            {"name": "Plaque de cuisson", "category": ObjectCategory.KITCHEN, "brand": "Siemens", "model": "iQ700", "purchase_date": datetime(2019, 5, 20), "notes": "Induction 4 feux", "owner_id": admin.id},
            {"name": "Réfrigérateur", "category": ObjectCategory.KITCHEN, "brand": "Liebherr", "model": "CBNPes", "purchase_date": datetime(2020, 1, 15), "notes": "Frigo combiné", "owner_id": admin.id},
            {"name": "Lave-linge", "category": ObjectCategory.APPLIANCE, "brand": "Miele", "model": "WDB 030", "purchase_date": datetime(2019, 8, 10), "notes": "Machine à laver", "owner_id": admin.id},
            {"name": "Sèche-linge", "category": ObjectCategory.APPLIANCE, "brand": "Miele", "model": "TDB 230", "purchase_date": datetime(2019, 8, 10), "notes": "Pompe à chaleur", "owner_id": admin.id},
            {"name": "Parquet salon", "category": ObjectCategory.FLOORING, "brand": "Quick-Step", "model": "Impressive", "purchase_date": datetime(2016, 9, 5), "notes": "Chêne naturel", "owner_id": admin.id},
            {"name": "Parquet chambres", "category": ObjectCategory.FLOORING, "brand": "Quick-Step", "model": "Impressive", "purchase_date": datetime(2016, 9, 5), "notes": "Chêne gris", "owner_id": admin.id},
            {"name": "Porte d'entrée", "category": ObjectCategory.OTHER, "brand": "Hormann", "model": "ThermoSafe", "purchase_date": datetime(2015, 4, 1), "notes": "Porte blindée", "owner_id": admin.id},
            
            # 15 Objets d'Alice
            {"name": "Chaudière Vaillant", "category": ObjectCategory.HEATING, "brand": "Vaillant", "model": "ecoTEC plus", "purchase_date": datetime(2020, 9, 15), "notes": "Entretien annuel OK", "owner_id": users[0].id},
            {"name": "Four Samsung", "category": ObjectCategory.KITCHEN, "brand": "Samsung", "model": "NV75N5671RS", "purchase_date": datetime(2022, 3, 10), "notes": "Sous garantie", "owner_id": users[0].id},
            {"name": "Lave-vaisselle Bosch", "category": ObjectCategory.APPLIANCE, "brand": "Bosch", "model": "SMV46KX00E", "purchase_date": datetime(2023, 1, 5), "notes": "Garantie 2025", "owner_id": users[0].id},
            {"name": "Micro-ondes", "category": ObjectCategory.KITCHEN, "brand": "Whirlpool", "model": "MWP 3391", "purchase_date": datetime(2021, 6, 20), "notes": "900W", "owner_id": users[0].id},
            {"name": "Cafetière", "category": ObjectCategory.KITCHEN, "brand": "De'Longhi", "model": "Magnifica", "purchase_date": datetime(2020, 12, 15), "notes": "Machine à café", "owner_id": users[0].id},
            {"name": "Baignoire", "category": ObjectCategory.BATHROOM, "brand": "Kaldewei", "model": "Saniform Plus", "purchase_date": datetime(2018, 5, 10), "notes": "Baignoire acier", "owner_id": users[0].id},
            {"name": "Mitigeur cuisine", "category": ObjectCategory.BATHROOM, "brand": "Grohe", "model": "Minta", "purchase_date": datetime(2019, 3, 5), "notes": "Robinet évier", "owner_id": users[0].id},
            {"name": "Aspirateur", "category": ObjectCategory.APPLIANCE, "brand": "Dyson", "model": "V11", "purchase_date": datetime(2021, 11, 25), "notes": "Sans fil", "owner_id": users[0].id},
            {"name": "Ventilateur plafond", "category": ObjectCategory.APPLIANCE, "brand": "Hunter", "model": "Builder Plus", "purchase_date": datetime(2020, 7, 15), "notes": "Salon", "owner_id": users[0].id},
            {"name": "Chauffe-eau", "category": ObjectCategory.HEATING, "brand": "Atlantic", "model": "Zénéo", "purchase_date": datetime(2019, 2, 20), "notes": "200L électrique", "owner_id": users[0].id},
            {"name": "VMC", "category": ObjectCategory.APPLIANCE, "brand": "Atlantic", "model": "Hygro B", "purchase_date": datetime(2019, 2, 20), "notes": "Ventilation", "owner_id": users[0].id},
            {"name": "Pompe piscine", "category": ObjectCategory.OTHER, "brand": "Hayward", "model": "Super Pump", "purchase_date": datetime(2018, 4, 10), "notes": "Filtration", "owner_id": users[0].id},
            {"name": "Portail électrique", "category": ObjectCategory.OTHER, "brand": "Came", "model": "BX", "purchase_date": datetime(2017, 6, 5), "notes": "Motorisation", "owner_id": users[0].id},
            {"name": "Climatiseur", "category": ObjectCategory.HEATING, "brand": "Daikin", "model": "Perfera", "purchase_date": datetime(2021, 5, 15), "notes": "Réversible", "owner_id": users[0].id},
            {"name": "Adoucisseur d'eau", "category": ObjectCategory.APPLIANCE, "brand": "Culligan", "model": "Aqua-Cleer", "purchase_date": datetime(2019, 9, 10), "notes": "Traitement eau", "owner_id": users[0].id},
            
            # 15 Objets de Bob
            {"name": "Robinet salle de bain", "category": ObjectCategory.BATHROOM, "brand": "Grohe", "model": "Eurosmart", "purchase_date": datetime(2019, 4, 20), "notes": "Lavabo", "owner_id": users[1].id},
            {"name": "Chaudière Buderus", "category": ObjectCategory.HEATING, "brand": "Buderus", "model": "Logamax", "purchase_date": datetime(2017, 10, 5), "notes": "Chaudière gaz", "owner_id": users[1].id},
            {"name": "Congélateur", "category": ObjectCategory.KITCHEN, "brand": "Electrolux", "model": "LUT5NF20W", "purchase_date": datetime(2020, 2, 15), "notes": "Bahut 200L", "owner_id": users[1].id},
            {"name": "Table cuisson gaz", "category": ObjectCategory.KITCHEN, "brand": "AEG", "model": "HG654550SY", "purchase_date": datetime(2018, 7, 20), "notes": "4 feux gaz", "owner_id": users[1].id},
            {"name": "Hotte décorative", "category": ObjectCategory.KITCHEN, "brand": "Electrolux", "model": "EFF60560OX", "purchase_date": datetime(2018, 7, 20), "notes": "Inox", "owner_id": users[1].id},
            {"name": "Cave à vin", "category": ObjectCategory.KITCHEN, "brand": "Liebherr", "model": "WKb 1812", "purchase_date": datetime(2019, 12, 10), "notes": "48 bouteilles", "owner_id": users[1].id},
            {"name": "Colonne de douche", "category": ObjectCategory.BATHROOM, "brand": "Hansgrohe", "model": "Crometta", "purchase_date": datetime(2018, 3, 15), "notes": "Thermostatique", "owner_id": users[1].id},
            {"name": "Meuble vasque", "category": ObjectCategory.BATHROOM, "brand": "Ikea", "model": "Godmorgon", "purchase_date": datetime(2018, 3, 15), "notes": "Double vasque", "owner_id": users[1].id},
            {"name": "Sèche-serviettes", "category": ObjectCategory.HEATING, "brand": "Acova", "model": "Atoll Spa", "purchase_date": datetime(2018, 3, 15), "notes": "Électrique", "owner_id": users[1].id},
            {"name": "Tondeuse robot", "category": ObjectCategory.OTHER, "brand": "Husqvarna", "model": "Automower", "purchase_date": datetime(2021, 4, 10), "notes": "Robot jardin", "owner_id": users[1].id},
            {"name": "Tronçonneuse", "category": ObjectCategory.OTHER, "brand": "Stihl", "model": "MS 180", "purchase_date": datetime(2019, 11, 5), "notes": "Élagage", "owner_id": users[1].id},
            {"name": "Nettoyeur HP", "category": ObjectCategory.APPLIANCE, "brand": "Kärcher", "model": "K5", "purchase_date": datetime(2020, 5, 20), "notes": "Haute pression", "owner_id": users[1].id},
            {"name": "Barbecue gaz", "category": ObjectCategory.OTHER, "brand": "Weber", "model": "Spirit II", "purchase_date": datetime(2021, 6, 15), "notes": "3 brûleurs", "owner_id": users[1].id},
            {"name": "Pompe à chaleur", "category": ObjectCategory.HEATING, "brand": "Mitsubishi", "model": "Ecodan", "purchase_date": datetime(2020, 9, 10), "notes": "Chauffage", "owner_id": users[1].id},
            {"name": "Sonnette vidéo", "category": ObjectCategory.OTHER, "brand": "Ring", "model": "Video Doorbell", "purchase_date": datetime(2022, 3, 5), "notes": "Connectée", "owner_id": users[1].id},
        ]
        
        objects = []
        for obj_data in objects_data:
            obj = Object(**obj_data)
            db.add(obj)
            objects.append(obj)
            print(f"✅ Objet: {obj_data['name']}")
        
        db.commit()
        
        # Refresh pour avoir les IDs
        for obj in objects:
            db.refresh(obj)
        
        print("\n" + "=" * 60)
        print("🚨 CRÉATION DES PROBLÈMES")
        print("=" * 60)
        
        problems_data = [
            {
                "title": "Chaudière qui fait du bruit",
                "description": "Claquements au démarrage depuis quelques jours",
                "category": ProblemCategory.NOISE,
                "severity": ProblemSeverity.MEDIUM,
                "status": ProblemStatus.OPEN,
                "object_id": objects[0].id,
                "reported_by": users[0].id
            },
            {
                "title": "Four ne chauffe pas uniformément",
                "description": "Le haut brûle alors que le bas reste cru",
                "category": ProblemCategory.HEATING_COOLING,
                "severity": ProblemSeverity.MEDIUM,
                "status": ProblemStatus.OPEN,
                "object_id": objects[1].id,
                "reported_by": users[0].id
            },
            {
                "title": "Lave-vaisselle ne vidange plus",
                "description": "L'eau reste au fond après le cycle",
                "category": ProblemCategory.LEAK,
                "severity": ProblemSeverity.HIGH,
                "status": ProblemStatus.IN_PROGRESS,
                "object_id": objects[2].id,
                "reported_by": users[0].id
            },
        ]
        
        for problem_data in problems_data:
            problem = Problem(**problem_data)
            db.add(problem)
            print(f"✅ Problème: {problem_data['title']}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("📋 CRÉATION DES CONSEILS DE MAINTENANCE")
        print("=" * 60)
        
        # Créer des conseils génériques
        advice_data = [
            {
                "title": "Entretien annuel chaudière",
                "description": "Faire vérifier et nettoyer la chaudière par un professionnel",
                "frequency_days": 365,
                "category": ObjectCategory.HEATING,
                "is_validated": True
            },
            {
                "title": "Nettoyage filtre lave-vaisselle",
                "description": "Nettoyer le filtre du lave-vaisselle pour maintenir les performances",
                "frequency_days": 30,
                "category": ObjectCategory.APPLIANCE,
                "is_validated": True
            },
            {
                "title": "Détartrage cafetière",
                "description": "Détartrer la machine à café pour prolonger sa durée de vie",
                "frequency_days": 90,
                "category": ObjectCategory.KITCHEN,
                "is_validated": True
            },
            {
                "title": "Vérification joints robinetterie",
                "description": "Vérifier l'état des joints pour éviter les fuites",
                "frequency_days": 180,
                "category": ObjectCategory.BATHROOM,
                "is_validated": True
            },
        ]
        
        advices = []
        for advice_item in advice_data:
            advice = MaintenanceAdvice(**advice_item)
            db.add(advice)
            advices.append(advice)
            print(f"✅ Conseil: {advice_item['title']}")
        
        db.commit()
        
        # Refresh pour avoir les IDs
        for advice in advices:
            db.refresh(advice)
        
        print("\n" + "=" * 60)
        print("🔧 CRÉATION DES TÂCHES DE MAINTENANCE")
        print("=" * 60)
        
        # Créer des tâches de maintenance
        tasks_data = [
            # Tâches de l'admin
            {
                "name": "Entretien annuel chaudière Viessmann",
                "scheduled_date": datetime.now() + timedelta(days=30),
                "status": MaintenanceStatus.PENDING,
                "notes": "Contacter le chauffagiste",
                "object_id": objects[0].id,  # Système chauffage central
                "user_id": admin.id,
                "advice_id": advices[0].id
            },
            {
                "name": "Vérification joints douche",
                "scheduled_date": datetime.now() + timedelta(days=15),
                "status": MaintenanceStatus.PENDING,
                "notes": "Vérifier étanchéité",
                "object_id": objects[6].id,  # Douche italienne
                "user_id": admin.id,
                "advice_id": advices[3].id
            },
            # Tâches d'Alice
            {
                "name": "Nettoyage filtre lave-vaisselle",
                "scheduled_date": datetime.now() + timedelta(days=7),
                "status": MaintenanceStatus.PENDING,
                "notes": "Nettoyer le filtre",
                "object_id": objects[17].id,  # Lave-vaisselle Bosch d'Alice
                "user_id": users[0].id,
                "advice_id": advices[1].id
            },
            {
                "name": "Détartrage machine à café",
                "scheduled_date": datetime.now() + timedelta(days=5),
                "status": MaintenanceStatus.PENDING,
                "notes": "Utiliser produit détartrant",
                "object_id": objects[19].id,  # Cafetière De'Longhi
                "user_id": users[0].id,
                "advice_id": advices[2].id
            },
            {
                "name": "Entretien chaudière",
                "scheduled_date": datetime.now() - timedelta(days=10),
                "completed_date": datetime.now() - timedelta(days=10),
                "status": MaintenanceStatus.COMPLETED,
                "notes": "Entretien effectué",
                "was_successful": True,
                "object_id": objects[15].id,  # Chaudière Vaillant d'Alice
                "user_id": users[0].id,
                "advice_id": advices[0].id
            },
            # Tâches de Bob
            {
                "name": "Entretien chaudière Buderus",
                "scheduled_date": datetime.now() + timedelta(days=45),
                "status": MaintenanceStatus.PENDING,
                "notes": "Prévoir rendez-vous",
                "object_id": objects[31].id,  # Chaudière Buderus de Bob
                "user_id": users[1].id,
                "advice_id": advices[0].id
            },
            {
                "name": "Vérification colonne de douche",
                "scheduled_date": datetime.now() - timedelta(days=5),
                "completed_date": datetime.now() - timedelta(days=5),
                "status": MaintenanceStatus.COMPLETED,
                "notes": "Thermostat vérifié",
                "was_successful": True,
                "object_id": objects[36].id,  # Colonne de douche
                "user_id": users[1].id,
                "advice_id": advices[3].id
            },
        ]
        
        for task_data in tasks_data:
            task = MaintenanceTask(**task_data)
            db.add(task)
            print(f"✅ Tâche: {task_data['name']}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("✅ INITIALISATION TERMINÉE")
        print("=" * 60)
        print("\n🔐 Comptes créés:")
        print(f"   Admin: admin@petittonnerre.com / Admin1234!")
        print(f"   Users: alice@example.com / Password123!")
        print(f"          bob@example.com / Password123!")
        print(f"          charlie@example.com / Password123!")
        print("\n🌐 URLs:")
        print(f"   API:  http://localhost:8000/docs")
        print(f"   App:  http://localhost:4200")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Point d'entrée principal"""
    print("\n" + "=" * 60)
    print("�� INITIALISATION DE PETIT TONNERRE")
    print("=" * 60)
    
    # 1. Reset complet de la DB
    reset_database()
    
    # 2. Créer les données de test
    create_test_data()


if __name__ == "__main__":
    main()
