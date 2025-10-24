# Commandes Rapides - Petit Tonnerre

## 🚀 Démarrage

```bash
# Setup initial (une fois)
./setup.sh

# Démarrer PostgreSQL
docker compose up -d

# Lancer le backend
cd backend && source .venv/bin/activate
uvicorn main:app --reload

# Données de test
python create_test_data.py
```

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

## 🐳 PostgreSQL

```bash
# Démarrer
docker compose up -d

# Voir les logs
docker logs petit_tonnerre_db

# Suivre les logs en temps réel
docker logs -f petit_tonnerre_db

# Se connecter à PostgreSQL
docker exec -it petit_tonnerre_db psql -U petittonnerre -d petittonnerre_db

# Arrêter
docker compose down

# Arrêter et supprimer les données (⚠️ DESTRUCTIF)
docker compose down -v

# Redémarrer
docker compose restart
```

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

---

## 🌐 URLs

- API Backend : http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc
- PostgreSQL : localhost:5432

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
