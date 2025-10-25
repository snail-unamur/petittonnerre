"""
Script simplifié pour créer un admin via l'API REST
"""
import requests
import json

API_URL = "http://localhost:8000"

def create_admin_user():
    """Créer un utilisateur admin via l'API"""
    
    # 1. Créer l'utilisateur
    user_data = {
        "email": "admin@petittonnerre.com",
        "username": "admin",
        "password": "Admin1234!",
        "password_confirm": "Admin1234!",
        "location": "Bruxelles"
    }
    
    print("🔨 Création de l'utilisateur admin...")
    try:
        response = requests.post(f"{API_URL}/users/", json=user_data)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Utilisateur créé avec ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Username: {user['username']}")
            return user['id']
        elif response.status_code == 400 and "already registered" in response.text.lower():
            print("ℹ️  L'utilisateur existe déjà")
            # Récupérer l'ID de l'utilisateur existant
            users_response = requests.get(f"{API_URL}/users/")
            users = users_response.json()
            for u in users:
                if u['email'] == user_data['email']:
                    print(f"   ID trouvé: {u['id']}")
                    return u['id']
            return None
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("💡 Assurez-vous que le backend est démarré (http://localhost:8000)")
        return None

def create_sample_requests(user_ids):
    """Créer des demandes d'objets de test"""
    requests_data = [
        {
            "name": "Chaudière Vaillant ecoTEC",
            "category": "heating",
            "brand": "Vaillant",
            "model": "ecoTEC plus VCW 346/5-5",
            "notes": "Installation récente, garantie 2 ans. Besoin de conseils pour l'entretien annuel."
        },
        {
            "name": "Lave-vaisselle Bosch",
            "category": "appliance",
            "brand": "Bosch",
            "model": "SMS46GI01E",
            "notes": "Acheté en 2020, fonctionne bien mais fait du bruit parfois."
        },
        {
            "name": "Four encastrable Siemens",
            "category": "kitchen",
            "brand": "Siemens",
            "model": "HB634GBS1",
            "manual_url": "https://example.com/manual-siemens.pdf",
            "notes": "Fonction pyrolyse, besoin de conseils pour le nettoyage."
        },
        {
            "name": "Pierre bleue escalier",
            "category": "flooring",
            "notes": "Pierre bleue belge, escalier intérieur. Comment l'entretenir sans l'abîmer ?"
        },
        {
            "name": "Pompe de relevage",
            "category": "bathroom",
            "brand": "Grundfos",
            "model": "Sololift2 WC-3",
            "notes": "Installée dans la cave, pour WC suspendu."
        }
    ]
    
    print(f"\n🔨 Création de {len(requests_data)} demandes d'objets...")
    created = 0
    for req_data in requests_data:
        try:
            # Alterner entre les utilisateurs
            user_id = user_ids[created % len(user_ids)]
            response = requests.post(
                f"{API_URL}/objects/requests?user_id={user_id}",
                json=req_data
            )
            if response.status_code == 200:
                created += 1
                print(f"  ✅ {req_data['name']}")
            else:
                print(f"  ⚠️  {req_data['name']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    print(f"\n✅ {created}/{len(requests_data)} demandes créées")

def main():
    print("=" * 60)
    print("  Script de création de données admin - Via API REST")
    print("=" * 60)
    print()
    
    # Créer l'admin
    admin_id = create_admin_user()
    
    if not admin_id:
        print("\n⚠️  Impossible de créer/trouver l'admin")
        print("💡 Note: Pour promouvoir en admin, utilisez PgAdmin:")
        print("   UPDATE users SET role = 'admin' WHERE email = 'admin@petittonnerre.com';")
        return
    
    # Créer quelques utilisateurs normaux
    print("\n🔨 Création d'utilisateurs de test...")
    user_ids = [admin_id]
    for i in range(1, 4):
        user_data = {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "User1234!",
            "password_confirm": "User1234!",
            "location": "Bruxelles" if i % 2 == 0 else "Liège"
        }
        try:
            response = requests.post(f"{API_URL}/users/", json=user_data)
            if response.status_code == 200:
                user = response.json()
                user_ids.append(user['id'])
                print(f"  ✅ {user['username']}")
            elif "already registered" in response.text.lower():
                print(f"  ℹ️  {user_data['username']} existe déjà")
        except:
            pass
    
    # Créer des demandes d'objets
    if len(user_ids) > 0:
        create_sample_requests(user_ids)
    
    print("\n" + "=" * 60)
    print("✅ Script terminé !")
    print("=" * 60)
    print()
    print("📋 Informations importantes:")
    print(f"   Email admin: admin@petittonnerre.com")
    print(f"   Password: Admin1234!")
    print(f"   Admin ID: {admin_id}")
    print()
    print("⚠️  Note: L'utilisateur n'est PAS encore admin !")
    print("   Pour le promouvoir admin, connectez-vous à PgAdmin et exécutez:")
    print("   UPDATE users SET role = 'admin' WHERE email = 'admin@petittonnerre.com';")
    print()
    print("🌐 URLs:")
    print("   Dashboard admin: http://localhost:4200/admin/auth")
    print("   Code temporaire: admin123")
    print()

if __name__ == "__main__":
    main()
