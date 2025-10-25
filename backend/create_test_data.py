import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"

def create_test_data():
    """Crée des données de test pour l'application"""
    
    print("🔧 Création de données de test...\n")
    
    # 1. Créer des utilisateurs
    print("👥 Création d'utilisateurs...")
    users = [
        {
            "email": "alice@example.com",
            "username": "alice",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "Bruxelles"
        },
        {
            "email": "bob@example.com",
            "username": "bob",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "Liège"
        }
    ]
    
    created_users = []
    for user_data in users:
        response = requests.post(f"{BASE_URL}/users/register", json=user_data)
        if response.status_code == 201:
            created_users.append(response.json())
            print(f"✅ Utilisateur créé: {user_data['username']}")
        else:
            print(f"❌ Erreur: {response.text}")
    
    # 2. Créer des objets
    print("\n🏠 Création d'objets...")
    objects = [
        {
            "name": "Chaudière Vaillant",
            "category": "heating",
            "brand": "Vaillant",
            "model": "ecoTEC plus",
            "notes": "Chaudière gaz condensation"
        },
        {
            "name": "Four Samsung",
            "category": "kitchen",
            "brand": "Samsung",
            "model": "NV75N5671RS",
            "notes": "Four encastrable pyrolyse"
        },
        {
            "name": "Pierre bleue terrasse",
            "category": "flooring",
            "brand": None,
            "model": None,
            "notes": "Terrasse extérieure 20m²"
        }
    ]
    
    # Créer les objets et stocker leurs IDs
    created_objects = []
    for obj_data in objects:
        response = requests.post(
            f"{BASE_URL}/objects/",
            params={"user_id": created_users[0]["id"]},
            json=obj_data
        )
        if response.status_code == 200:
            created_objects.append(response.json())
            print(f"✅ Objet créé: {obj_data['name']}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    # Créer des objets enfants
    if created_objects:
        print("\n🔗 Création d'objets enfants (hiérarchie)...")
        child_objects = [
            {
                "name": "Thermostat connecté",
                "category": "heating",
                "brand": "Nest",
                "model": "T3007ES",
                "notes": "Thermostat lié à la chaudière",
                "parent_id": created_objects[0]["id"]  # Enfant de la chaudière
            },
            {
                "name": "Sonde de température",
                "category": "heating",
                "brand": "Vaillant",
                "model": "VR 920",
                "notes": "Sonde sans fil",
                "parent_id": created_objects[0]["id"]  # Enfant de la chaudière
            }
        ]
        
        for child_data in child_objects:
            response = requests.post(
                f"{BASE_URL}/objects/",
                params={"user_id": created_users[0]["id"]},
                json=child_data
            )
            if response.status_code == 200:
                print(f"✅ Objet enfant créé: {child_data['name']}")
            else:
                print(f"❌ Erreur: {response.text}")
    
    created_objects = []
    for obj_data in objects:
        response = requests.post(
            f"{BASE_URL}/objects/",
            params={"user_id": created_users[0]["id"]},
            json=obj_data
        )
        if response.status_code == 200:
            created_objects.append(response.json())
            print(f"✅ Objet créé: {obj_data['name']}")
        else:
            print(f"❌ Erreur: {response.text}")
    
    # 3. Créer des conseils d'entretien
    print("\n📋 Création de conseils d'entretien...")
    advice_list = [
        {
            "title": "Contrôle annuel chaudière",
            "description": "Faire vérifier la chaudière par un technicien agréé",
            "frequency_days": 365,
            "category": "heating"
        },
        {
            "title": "Nettoyage four pyrolyse",
            "description": "Lancer un cycle de pyrolyse pour nettoyer le four",
            "frequency_days": 90,
            "category": "kitchen"
        },
        {
            "title": "Traitement pierre bleue",
            "description": "Appliquer un produit hydrofuge pour protéger la pierre",
            "frequency_days": 180,
            "category": "flooring"
        }
    ]
    
    created_advice = []
    for advice_data in advice_list:
        response = requests.post(f"{BASE_URL}/maintenance/advice", json=advice_data)
        if response.status_code == 200:
            created_advice.append(response.json())
            print(f"✅ Conseil créé: {advice_data['title']}")
        else:
            print(f"❌ Erreur: {response.text}")
    
    # 4. Créer des tâches de maintenance
    print("\n📅 Création de tâches de maintenance...")
    for i, obj in enumerate(created_objects):
        if i < len(created_advice):
            task_data = {
                "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "notes": "Tâche planifiée",
                "object_id": obj["id"],
                "advice_id": created_advice[i]["id"]
            }
            response = requests.post(
                f"{BASE_URL}/maintenance/tasks",
                params={"user_id": created_users[0]["id"]},
                json=task_data
            )
            if response.status_code == 200:
                print(f"✅ Tâche créée pour: {obj['name']}")
            else:
                print(f"❌ Erreur: {response.text}")
    
    # 5. Créer des contributions communautaires
    print("\n💬 Création de contributions...")
    contributions = [
        {
            "title": "Astuce nettoyage pierre bleue",
            "content": "Utilisez du savon noir dilué dans l'eau pour un nettoyage efficace",
            "category": "flooring"
        },
        {
            "title": "Détartrage chaudière",
            "content": "Pour éviter le tartre, faire installer un adoucisseur d'eau",
            "category": "heating"
        }
    ]
    
    for contrib_data in contributions:
        response = requests.post(
            f"{BASE_URL}/community/contributions",
            params={"author_id": created_users[1]["id"]},
            json=contrib_data
        )
        if response.status_code == 200:
            print(f"✅ Contribution créée: {contrib_data['title']}")
        else:
            print(f"❌ Erreur: {response.text}")
    
    print("\n✅ Données de test créées avec succès!")
    print(f"\n📖 Consultez la documentation API: {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        create_test_data()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est lancé: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Erreur: {e}")
