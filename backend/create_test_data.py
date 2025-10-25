import requests
import json
from datetime import datetime, timedelta
import time

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
        },
        {
            "email": "charlie@example.com",
            "username": "charlie",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "location": "Namur"
        }
    ]
    
    created_users = []
    for user_data in users:
        response = requests.post(f"{BASE_URL}/users/register", json=user_data)
        if response.status_code == 201:
            created_users.append(response.json())
            print(f"✅ Utilisateur créé: {user_data['username']} (ID: {response.json()['id']})")
        else:
            print(f"❌ Erreur: {response.text}")
    
    if not created_users:
        print("❌ Aucun utilisateur créé, arrêt du script")
        return
    
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
        },
        {
            "name": "Robinet lavabo salle de bain",
            "category": "bathroom",
            "brand": "Grohe",
            "model": "Eurosmart",
            "notes": "Mitigeur lavabo"
        },
        {
            "name": "Lave-vaisselle Bosch",
            "category": "appliance",
            "brand": "Bosch",
            "model": "SMV46KX00E",
            "notes": "Lave-vaisselle encastrable"
        }
    ]
    
    created_objects = []
    for obj_data in objects:
        response = requests.post(
            f"{BASE_URL}/objects/",
            params={"user_id": created_users[0]["id"]},
            json=obj_data
        )
        if response.status_code in [200, 201]:
            obj = response.json()
            created_objects.append(obj)
            print(f"✅ Objet créé: {obj_data['name']} (ID: {obj['id']})")
        else:
            print(f"❌ Erreur: {response.text}")
    
    # 3. Créer des problèmes
    print("\n🚨 Création de problèmes...")
    problems = [
        {
            "title": "Fuite sous le lavabo",
            "description": "De l'eau s'accumule sous le lavabo de la salle de bain",
            "category": "leak",
            "severity": "high",
            "symptoms": "Eau qui coule en continu, tache d'humidité sur le meuble",
            "possible_causes": "Joint usé, serrage insuffisant, fissure",
            "object_id": created_objects[3]["id"] if len(created_objects) > 3 else created_objects[0]["id"]  # Robinet
        },
        {
            "title": "Chaudière qui fait du bruit",
            "description": "La chaudière émet un bruit de claquement lors du démarrage",
            "category": "noise",
            "severity": "medium",
            "symptoms": "Claquements forts au démarrage, sifflements intermittents",
            "possible_causes": "Tartre dans les canalisations, air dans le circuit",
            "object_id": created_objects[0]["id"] if len(created_objects) > 0 else None  # Chaudière
        },
        {
            "title": "Four ne chauffe plus uniformément",
            "category": "heating_cooling",
            "severity": "medium",
            "description": "Le four cuit mal les aliments, chauffe beaucoup plus en haut qu'en bas",
            "symptoms": "Cuisson inégale, dessus brûlé et dessous cru",
            "possible_causes": "Résistance défectueuse, ventilateur en panne",
            "object_id": created_objects[1]["id"] if len(created_objects) > 1 else None  # Four
        },
        {
            "title": "Lave-vaisselle ne vidange plus",
            "category": "mechanical",
            "severity": "medium",
            "description": "L'eau reste au fond du lave-vaisselle après le cycle",
            "symptoms": "Eau stagnante, cycle qui ne se termine pas",
            "possible_causes": "Filtre bouché, pompe de vidange défectueuse",
            "object_id": created_objects[4]["id"] if len(created_objects) > 4 else None  # Lave-vaisselle
        }
    ]
    
    created_problems = []
    for problem_data in problems:
        response = requests.post(
            f"{BASE_URL}/problems/",
            params={"user_id": created_users[0]["id"]},
            json=problem_data
        )
        if response.status_code in [200, 201]:
            problem = response.json()
            created_problems.append(problem)
            print(f"✅ Problème créé: {problem_data['title']} (ID: {problem['id']})")
        else:
            print(f"❌ Erreur création problème: {response.text}")
    
    # 4. Créer des résolutions avec images
    print("\n💡 Création de résolutions avec images...")
    
    if len(created_problems) > 0:
        # Résolution 1 : Fuite lavabo (avec images et popularité)
        resolution1 = {
            "solution": "Remplacer le joint du siphon",
            "steps": "1. Couper l'arrivée d'eau\n2. Démonter le siphon\n3. Retirer l'ancien joint\n4. Nettoyer les surfaces\n5. Poser le nouveau joint\n6. Remonter le siphon\n7. Vérifier l'étanchéité",
            "cost_estimate": "5-10€",
            "time_estimate": "30 minutes",
            "feedback": "Solution testée avec succès, plus aucune fuite depuis 2 mois",
            "images": "https://picsum.photos/seed/plumbing1/400/300, https://picsum.photos/seed/plumbing2/400/300, https://picsum.photos/seed/plumbing3/400/300"
        }
        
        response = requests.post(
            f"{BASE_URL}/problems/{created_problems[0]['id']}/resolutions",
            params={"user_id": created_users[1]["id"]},
            json=resolution1
        )
        if response.status_code in [200, 201]:
            res1 = response.json()
            print(f"✅ Résolution créée pour '{created_problems[0]['title']}' (ID: {res1['id']})")
            
            # Ajouter 12 votes pour en faire une solution populaire
            for i in range(12):
                requests.post(f"{BASE_URL}/problems/resolutions/{res1['id']}/upvote")
                time.sleep(0.1)
            print(f"   👍 12 votes ajoutés - Solution populaire!")
            
            # Marquer comme réussie
            requests.post(
                f"{BASE_URL}/problems/resolutions/{res1['id']}/mark-successful",
                params={"user_id": created_users[0]["id"]}
            )
            print(f"   ✅ Marquée comme solution validée")
        
        # Résolution 2 : Alternative sans images
        resolution2 = {
            "solution": "Utiliser du ruban téflon sur les filetages",
            "steps": "1. Dévisser les raccords\n2. Enrouler du téflon dans le sens du vissage\n3. Revisser fermement",
            "cost_estimate": "2-3€",
            "time_estimate": "15 minutes",
            "feedback": "Solution rapide mais moins durable"
        }
        
        response = requests.post(
            f"{BASE_URL}/problems/{created_problems[0]['id']}/resolutions",
            params={"user_id": created_users[2]["id"]},
            json=resolution2
        )
        if response.status_code in [200, 201]:
            print(f"✅ Résolution alternative créée (ID: {response.json()['id']})")
    
    if len(created_problems) > 1:
        # Résolution pour chaudière bruyante avec images
        resolution3 = {
            "solution": "Purger les radiateurs et désembouer le circuit",
            "steps": "1. Éteindre la chaudière\n2. Purger tous les radiateurs\n3. Ajouter un produit désembouant\n4. Faire circuler pendant 1 semaine\n5. Rincer le circuit\n6. Remplir avec de l'eau neuve",
            "cost_estimate": "50-100€ (avec désembouant professionnel)",
            "time_estimate": "2-3 heures",
            "feedback": "Très efficace, la chaudière est redevenue silencieuse",
            "images": "https://picsum.photos/seed/heating1/400/300, https://picsum.photos/seed/heating2/400/300"
        }
        
        response = requests.post(
            f"{BASE_URL}/problems/{created_problems[1]['id']}/resolutions",
            params={"user_id": created_users[1]["id"]},
            json=resolution3
        )
        if response.status_code in [200, 201]:
            res3 = response.json()
            print(f"✅ Résolution créée pour '{created_problems[1]['title']}' (ID: {res3['id']})")
            
            # Ajouter 15 votes
            for i in range(15):
                requests.post(f"{BASE_URL}/problems/resolutions/{res3['id']}/upvote")
                time.sleep(0.1)
            print(f"   👍 15 votes ajoutés - Solution très populaire!")
    
    if len(created_problems) > 2:
        # Résolution pour four avec images
        resolution4 = {
            "solution": "Remplacer la résistance de sole",
            "steps": "1. Débrancher le four\n2. Démonter les parois intérieures\n3. Débrancher la résistance défectueuse\n4. Installer la nouvelle résistance\n5. Remonter et tester",
            "cost_estimate": "80-150€",
            "time_estimate": "1-2 heures",
            "feedback": "La cuisson est redevenue homogène, four comme neuf",
            "images": "https://picsum.photos/seed/oven1/400/300, https://picsum.photos/seed/oven2/400/300, https://picsum.photos/seed/oven3/400/300, https://picsum.photos/seed/oven4/400/300"
        }
        
        response = requests.post(
            f"{BASE_URL}/problems/{created_problems[2]['id']}/resolutions",
            params={"user_id": created_users[2]["id"]},
            json=resolution4
        )
        if response.status_code in [200, 201]:
            res4 = response.json()
            print(f"✅ Résolution créée pour '{created_problems[2]['title']}' (ID: {res4['id']})")
            
            # Ajouter 8 votes
            for i in range(8):
                requests.post(f"{BASE_URL}/problems/resolutions/{res4['id']}/upvote")
                time.sleep(0.1)
            print(f"   👍 8 votes ajoutés")
    
    if len(created_problems) > 3:
        # Résolution pour lave-vaisselle
        resolution5 = {
            "solution": "Nettoyer le filtre et vérifier la pompe de vidange",
            "steps": "1. Retirer le panier inférieur\n2. Dévisser et retirer le filtre\n3. Nettoyer sous l'eau chaude\n4. Vérifier la pompe (rotor libre)\n5. Remonter le filtre",
            "cost_estimate": "0€ (nettoyage) ou 80€ (pompe neuve)",
            "time_estimate": "15-30 minutes",
            "feedback": "Le simple nettoyage du filtre a suffi, tout refonctionne"
        }
        
        response = requests.post(
            f"{BASE_URL}/problems/{created_problems[3]['id']}/resolutions",
            params={"user_id": created_users[0]["id"]},
            json=resolution5
        )
        if response.status_code in [200, 201]:
            res5 = response.json()
            print(f"✅ Résolution créée pour '{created_problems[3]['title']}' (ID: {res5['id']})")
            
            # Marquer comme réussie
            requests.post(
                f"{BASE_URL}/problems/resolutions/{res5['id']}/mark-successful",
                params={"user_id": created_users[0]["id"]}
            )
            print(f"   ✅ Marquée comme solution validée")
    
    # 5. Créer des conseils d'entretien
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
        if response.status_code in [200, 201]:
            created_advice.append(response.json())
            print(f"✅ Conseil créé: {advice_data['title']}")
        else:
            print(f"❌ Erreur: {response.text}")
    
    # 6. Créer des tâches de maintenance
    print("\n📅 Création de tâches de maintenance...")
    if created_objects and created_advice:
        for i, obj in enumerate(created_objects[:3]):  # Seulement les 3 premiers
            if i < len(created_advice):
                task_data = {
                    "scheduled_date": (datetime.now() + timedelta(days=7 + i*3)).isoformat(),
                    "notes": f"Tâche planifiée pour {obj['name']}",
                    "object_id": obj["id"],
                    "advice_id": created_advice[i]["id"]
                }
                response = requests.post(
                    f"{BASE_URL}/maintenance/tasks",
                    params={"user_id": created_users[0]["id"]},
                    json=task_data
                )
                if response.status_code in [200, 201]:
                    print(f"✅ Tâche créée pour: {obj['name']}")
                else:
                    print(f"❌ Erreur: {response.text}")
    
    # 7. Créer des contributions communautaires
    print("\n💬 Création de contributions...")
    contributions = [
        {
            "title": "Astuce nettoyage pierre bleue",
            "content": "Utilisez du savon noir dilué dans l'eau pour un nettoyage efficace sans abîmer la pierre. Évitez les produits acides qui attaquent la surface.",
            "category": "flooring"
        },
        {
            "title": "Détartrage chaudière",
            "content": "Pour éviter le tartre dans votre chaudière, faites installer un adoucisseur d'eau. Vérifiez la dureté de l'eau avec des bandelettes tests.",
            "category": "heating"
        },
        {
            "title": "Entretien four",
            "content": "Pour prolonger la vie de votre four, nettoyez les projections immédiatement après refroidissement. Utilisez la pyrolyse maximum 2 fois par an.",
            "category": "kitchen"
        }
    ]
    
    for contrib_data in contributions:
        response = requests.post(
            f"{BASE_URL}/community/contributions",
            params={"author_id": created_users[1]["id"]},
            json=contrib_data
        )
        if response.status_code in [200, 201]:
            print(f"✅ Contribution créée: {contrib_data['title']}")
        else:
            print(f"❌ Erreur: {response.text}")
    
    # Récapitulatif
    print("\n" + "="*60)
    print("✅ Données de test créées avec succès!")
    print("="*60)
    print(f"� {len(created_users)} utilisateurs créés")
    print(f"🏠 {len(created_objects)} objets créés")
    print(f"🚨 {len(created_problems)} problèmes créés")
    print(f"📋 {len(created_advice)} conseils d'entretien créés")
    print(f"💬 {len(contributions)} contributions créées")
    print("="*60)
    print(f"\n📖 Documentation API: {BASE_URL}/docs")
    print(f"🌐 Application: http://localhost:4200")
    print("\n💡 Testez les fonctionnalités:")
    print("   - Connexion avec alice@example.com / Password123!")
    print("   - Consultez les problèmes avec résolutions et images")
    print("   - Votez pour les solutions populaires")
    print("   - Ajoutez vos propres résolutions avec images")

if __name__ == "__main__":
    try:
        create_test_data()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est lancé sur http://localhost:8000")
        print("Commande: docker-compose up ou ./start-docker.sh")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
