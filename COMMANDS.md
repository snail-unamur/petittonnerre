# Commandes Rapides - Petit Tonnerre

## 🚀 Démarrage

```bash
# Setup initial (une fois)
./setup.sh

# DÉVELOPPEMENT RAPIDE (RECOMMANDÉ)
# Démarrage rapide sans rebuild (utilise les images existantes)
./dev-start.sh

# OU Démarrage complet (rebuild si nécessaire)
./start.sh

# OU Forcer un rebuild complet (après modifications de requirements.txt)
./start.sh --build

# Démarrer uniquement PostgreSQL + PgAdmin (sans backend/frontend)
./start-docker.sh

# Lancer le backend manuellement (mode dev local)
cd backend && source .venv/bin/activate
uvicorn main:app --reload

# Données de test
python create_test_data.py

# Créer admin et demandes d'objets (VIA DOCKER - RECOMMANDÉ)
sudo docker exec petit_tonnerre_backend python create_admin_test_data.py

# OU via API REST (alternative si problème bcrypt)
python create_admin_via_api.py
# Puis promouvoir en admin via PgAdmin (voir docs/ADMIN_SETUP.md)
```

**URLs** :
- API : http://localhost:8000/docs
- PgAdmin : http://localhost:5050 (admin@petittonnerre.com / admin)
- Frontend : http://localhost:4200
- Admin Dashboard : http://localhost:4200/admin/auth (code: admin123)

💡 **Astuces:**
- Utilise `./dev-start.sh` pour démarrer rapidement sans rebuild
- Utilise `./start.sh --build` seulement quand tu modifies `requirements.txt`
- Le serveur "Petit Tonnerre DB" est déjà configuré dans PgAdmin !

---

## 🔧 Backend

```bash
# Activer l'environnement
cd backend && source .venv/bin/activate

# Lancer le serveur (mode dev)
uvicorn main:app --reload

# Lancer sur réseau local
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Désactiver l'environnement
deactivate
```

---

## 🐳 Docker (PostgreSQL + PgAdmin)

```bash
# Démarrer tous les services
./start.sh

# OU uniquement PostgreSQL + PgAdmin (sans backend/frontend)
./start-docker.sh
# OU : docker compose up -d postgres pgadmin

# Voir les conteneurs en cours
docker ps

# Voir les logs PostgreSQL
docker logs petit_tonnerre_db

# Voir les logs PgAdmin
docker logs petit_tonnerre_pgadmin

# Voir les logs Backend
docker compose logs -f backend

# Voir les logs Frontend
docker compose logs -f frontend

# Suivre les logs en temps réel
docker logs -f petit_tonnerre_db

# Se connecter à PostgreSQL en ligne de commande
docker exec -it petit_tonnerre_db psql -U petittonnerre -d petittonnerre_db

# Arrêter tous les services
docker compose down

# Arrêter et supprimer les données (⚠️ DESTRUCTIF)
docker compose down -v

# Redémarrer un service spécifique
docker compose restart backend
docker compose restart frontend
docker compose restart postgres
```

### 🔍 PgAdmin Web

**URL** : http://localhost:5050  
**Login** : admin@petittonnerre.com / admin

**Connexion à la DB** :
- Host : `postgres`
- Port : `5432`
- Database : `petittonnerre_db`
- Username : `petittonnerre`
- Password : `petittonnerre`

### Requêtes SQL Utiles

```sql
-- Lister les tables
\dt

-- Voir structure d'une table
\d users

-- Compter les utilisateurs
SELECT COUNT(*) FROM users;

-- Voir objets avec propriétaires
SELECT o.name, o.category, u.username 
FROM objects o 
JOIN users u ON o.owner_id = u.id;

-- Tâches en attente
SELECT * FROM maintenance_tasks WHERE status = 'pending';

-- Quitter
\q
```

---

## 🧪 Tests

```bash
# Script de test complet
./test_api.sh

# Créer des données de test
cd backend
python create_test_data.py

# Tester un endpoint
curl http://localhost:8000/
curl http://localhost:8000/users/
curl http://localhost:8000/objects/
```

---

## 📦 Dépendances

```bash
# Installer une nouvelle dépendance
cd backend && source .venv/bin/activate
pip install nom_du_package
pip freeze > requirements.txt

# Réinstaller toutes les dépendances
pip install -r requirements.txt
```

---

## 🔍 Debugging

```bash
# Vérifier PostgreSQL
docker ps | grep postgres

# Vérifier port 8000
lsof -i :8000

# Tester connexion DB
docker exec petit_tonnerre_db pg_isready -U petittonnerre

# Voir variables d'environnement
cat backend/.env
```

### Résoudre les problèmes

```bash
# Port occupé
lsof -i :8000
kill -9 <PID>

# Réinitialiser la DB
docker compose down -v
docker compose up -d

# Réinstaller l'environnement Python
cd backend
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📡 API - Exemples curl

### Users

```bash
# Créer
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "test", "location": "Bruxelles"}'

# Lister
curl http://localhost:8000/users/

# Détails
curl http://localhost:8000/users/1
```

### Objects

```bash
# Créer
curl -X POST "http://localhost:8000/objects/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Chaudière", "category": "heating", "brand": "Vaillant"}'

# Lister
curl http://localhost:8000/objects/

# Lister pour un user
curl "http://localhost:8000/objects/?user_id=1"

# Modifier
curl -X PUT "http://localhost:8000/objects/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Chaudière Modifiée", "category": "heating"}'

# Supprimer
curl -X DELETE http://localhost:8000/objects/1
```

### Maintenance

```bash
# Créer un conseil
curl -X POST "http://localhost:8000/maintenance/advice" \
  -H "Content-Type: application/json" \
  -d '{"title": "Contrôle annuel", "description": "Faire vérifier", "frequency_days": 365, "category": "heating"}'

# Lister conseils
curl "http://localhost:8000/maintenance/advice"

# Filtrer par catégorie
curl "http://localhost:8000/maintenance/advice?category=heating&validated_only=true"

# Créer une tâche
curl -X POST "http://localhost:8000/maintenance/tasks?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"scheduled_date": "2025-11-01T10:00:00", "object_id": 1, "advice_id": 1, "notes": "À faire"}'

# Mettre à jour (feedback)
curl -X PATCH "http://localhost:8000/maintenance/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "completed_date": "2025-10-24T14:30:00", "was_successful": true, "notes": "Fait"}'
```

### Community

```bash
# Créer contribution
curl -X POST "http://localhost:8000/community/contributions?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Astuce", "content": "Utiliser du vinaigre blanc", "category": "heating"}'

# Lister
curl http://localhost:8000/community/contributions

# Voter
curl -X POST http://localhost:8000/community/contributions/1/upvote

# Valider
curl -X PATCH "http://localhost:8000/community/contributions/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

### Admin - Demandes d'objets

```bash
# Créer une demande d'objet
curl -X POST "http://localhost:8000/objects/requests?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Chaudière Vaillant", "category": "heating", "brand": "Vaillant", "model": "ecoTEC", "notes": "Besoin conseils entretien"}'

# Lister toutes les demandes
curl http://localhost:8000/objects/requests

# Lister demandes en attente (admin)
curl "http://localhost:8000/objects/admin/pending-requests?admin_id=1"

# Approuver une demande (admin)
curl -X PUT "http://localhost:8000/objects/requests/1/decide?admin_id=1" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved", "admin_notes": "Demande validée"}'

# Rejeter une demande (admin)
curl -X PUT "http://localhost:8000/objects/requests/1/decide?admin_id=1" \
  -H "Content-Type: application/json" \
  -d '{"status": "rejected", "admin_notes": "Informations incomplètes"}'

# Supprimer une demande (admin)
curl -X DELETE "http://localhost:8000/objects/admin/requests/1?admin_id=1"
```

---

## 🌐 URLs

- API Backend : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc
- PostgreSQL : localhost:5432
- **Admin Dashboard** : http://localhost:4200/admin/auth (code: admin123)

---

## 🎨 Frontend (quand créé)

```bash
# Créer le projet Angular
ng new frontend --routing --style=scss

# Lancer
cd frontend && ng serve

# Générer composant
ng g component components/dashboard

# Générer service
ng g service services/api

# Build production
ng build --configuration production
```

---

## 📊 Monitoring

```bash
# Stats Docker
docker stats

# Espace disque Docker
docker system df

# Nettoyer Docker
docker system prune
```

---

## 🔄 Workflow Type

```bash
# 1. Démarrer les services
docker compose up -d

# 2. Activer environnement et lancer serveur
cd backend && source .venv/bin/activate
uvicorn main:app --reload

# 3. Travailler (le serveur redémarre auto avec --reload)

# 4. Arrêter
# Ctrl+C pour uvicorn
# deactivate pour sortir de l'env
# docker compose down (optionnel)
```

---

Voir [README.md](README.md) pour plus d'informations.
