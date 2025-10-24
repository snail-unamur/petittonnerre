# Petit Tonnerre 🔧

Application de gestion intelligente et collaborative de l'entretien d'objets et appareils domestiques.

**Stack** : FastAPI + PostgreSQL + Angular

---

## 🚀 Démarrage Rapide

### Backend

```bash
# 1. Setup initial
./setup.sh

# 2. Démarrer PostgreSQL
docker compose up -d

# 3. Lancer le backend
cd backend && source .venv/bin/activate
uvicorn main:app --reload

# 4. Créer des données de test
python create_test_data.py
```

🌐 **API** : http://localhost:8000/docs

### Frontend

```bash
# 1. Installer les dépendances
cd frontend
npm install

# 2. Configurer l'URL du backend (optionnel)
cp .env.example .env
# Éditer .env pour changer VITE_API_URL si nécessaire

# 3. Lancer le serveur Angular
npm start
```

🌐 **App** : http://localhost:4200  
📖 **Config** : Voir `frontend/ENV.md` pour la configuration

---

## 📋 Fonctionnalités

- 📦 **Gestion des objets** : Inventaire domestique (chaudière, four, sanitaires...)
- 💡 **Conseils d'entretien** : Recommandations personnalisées par catégorie
- ✅ **Tâches & Feedback** : Planification et suivi avec retour d'expérience
- 👥 **Communauté** : Partage d'expériences et système de votes

---

## 🏗️ Structure

```
petit-tonnerre/
├── backend/                 ✅ Backend FastAPI
│   ├── api/                 # Routes API (users, objects, maintenance, community)
│   ├── main.py              # Application FastAPI
│   ├── models.py            # 7 modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   ├── database.py          # Configuration PostgreSQL
│   └── create_test_data.py  # Génération de données
├── frontend/                ✅ Frontend Angular
│   ├── src/app/
│   │   ├── core/            # Services & Models
│   │   ├── features/        # Dashboard, Objects, Maintenance, Community
│   │   └── shared/          # Composants réutilisables
│   └── package.json
├── docker-compose.yml       # PostgreSQL 15
├── setup.sh                 # Installation backend
└── test_api.sh              # Tests API
```

---

## 💻 Installation

### Prérequis
- **Python 3.10+** ✅
- **Docker Desktop** → [Télécharger](https://www.docker.com/products/docker-desktop/)
- Node.js 18+ (pour le frontend, optionnel)

### Étapes

1. **Installer Docker Desktop** et le lancer

2. **Setup du projet**
   ```bash
   ./setup.sh
   ```

3. **Démarrer PostgreSQL**
   ```bash
   docker compose up -d
   ```

4. **Lancer le backend**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn main:app --reload
   ```

5. **Tester**
   ```bash
   # Données de test
   python create_test_data.py
   
   # Ou script de test
   ./test_api.sh
   ```

---

## 🔌 API Endpoints

### 👤 Users (3)
```
POST   /users/           Créer un utilisateur
GET    /users/           Liste
GET    /users/{id}       Détails
```

### �� Objects (5)
```
POST   /objects/         Créer
GET    /objects/         Liste (filtre: ?user_id=1)
GET    /objects/{id}     Détails
PUT    /objects/{id}     Modifier
DELETE /objects/{id}     Supprimer
```

### 🔧 Maintenance (7)
```
# Conseils
POST   /maintenance/advice        Créer
GET    /maintenance/advice        Liste (filtres: category, validated_only)
GET    /maintenance/advice/{id}   Détails

# Tâches
POST   /maintenance/tasks         Créer
GET    /maintenance/tasks         Liste (filtres: user_id, object_id, status)
GET    /maintenance/tasks/{id}    Détails
PATCH  /maintenance/tasks/{id}    Mettre à jour (feedback)
```

### 👥 Community (5)
```
POST   /community/contributions            Créer
GET    /community/contributions            Liste (tri par votes)
GET    /community/contributions/{id}       Détails
PATCH  /community/contributions/{id}       Valider/rejeter
POST   /community/contributions/{id}/upvote Vote
```

📖 **Documentation** : http://localhost:8000/docs

---

## 📊 Modèles de Données

- **User** : Utilisateurs (email, username, location)
- **Object** : Objets domestiques (6 catégories)
- **MaintenanceAdvice** : Conseils d'entretien
- **MaintenanceTask** : Tâches avec feedback
- **Contribution** : Partages communautaires
- **Tag** + **object_tags** : Tags Many-to-Many

**Categories** : `heating`, `appliance`, `kitchen`, `bathroom`, `flooring`, `other`

---

## 📝 Exemples

### Créer un utilisateur et un objet
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "username": "alice", "location": "Bruxelles"}'

curl -X POST "http://localhost:8000/objects/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Chaudière", "category": "heating", "brand": "Vaillant"}'
```

### Planifier une tâche avec feedback
```bash
# Créer un conseil
curl -X POST "http://localhost:8000/maintenance/advice" \
  -H "Content-Type: application/json" \
  -d '{"title": "Contrôle annuel", "description": "Vérification", "frequency_days": 365, "category": "heating"}'

# Planifier
curl -X POST "http://localhost:8000/maintenance/tasks?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"scheduled_date": "2025-11-01T10:00:00", "object_id": 1, "advice_id": 1}'

# Feedback
curl -X PATCH "http://localhost:8000/maintenance/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "was_successful": true, "notes": "OK"}'
```

Plus d'exemples : [COMMANDS.md](COMMANDS.md)

---

## 🛠️ Commandes

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn main:app --reload

# PostgreSQL
docker compose up -d              # Démarrer
docker logs petit_tonnerre_db -f  # Logs
docker compose down               # Arrêter
docker compose down -v            # Réinitialiser (⚠️ supprime données)

# Tests
./test_api.sh
python create_test_data.py
```

Référence complète : [COMMANDS.md](COMMANDS.md)

---

## 🐛 Troubleshooting

**Docker non installé**
```bash
# Télécharger : https://www.docker.com/products/docker-desktop/
```

**Port 8000 occupé**
```bash
lsof -i :8000
kill -9 <PID>
```

**Erreur DB**
```bash
docker compose restart
# ou
docker compose down -v && docker compose up -d
```

---

## 🔄 Prochaines Étapes

### Phase 1 - Frontend Angular 🔴
```bash
ng new frontend --routing --style=scss
```
Composants : Dashboard, Objets, Maintenance, Communauté

### Phase 2 - Sécurité 🟡
- Authentification JWT
- Protection des routes
- Rôles utilisateur

### Phase 3 - Features 🟡
- Notifications
- Upload fichiers (manuels PDF)
- Tests unitaires

### Phase 4 - Production 🔴
- Déploiement (Vercel + Railway)
- CI/CD

---

## 🛠️ Technologies

**Backend** : FastAPI 0.104, SQLAlchemy 2.0, PostgreSQL 15, Pydantic 2.5  
**Frontend** : Angular 17+ (à créer)

---

## 📚 Ressources

- [COMMANDS.md](COMMANDS.md) - Référence des commandes
- http://localhost:8000/docs - Documentation API
- https://fastapi.tiangolo.com/ - FastAPI
- https://angular.io/docs - Angular

---

**Projet créé le 24 octobre 2025**
