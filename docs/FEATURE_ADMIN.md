# Feature Admin - Gestion des demandes d'objets

## 📋 Description

Cette feature permet aux administrateurs de gérer les demandes de création d'objets soumises par les utilisateurs.

## 🔧 Fonctionnalités implémentées

### Backend (FastAPI)

1. **Nouveau modèle `ObjectRequest`**
   - Stocke les demandes d'objets avec statut (pending, approved, rejected)
   - Garde l'historique des décisions admin

2. **Endpoints API**
   - `POST /objects/requests` - Créer une demande d'objet
   - `GET /objects/requests` - Récupérer toutes les demandes
   - `GET /objects/requests/{id}` - Récupérer une demande spécifique
   - `GET /objects/admin/pending-requests` - Récupérer les demandes en attente (admin)
   - `PUT /objects/requests/{id}/decide` - Approuver/rejeter une demande (admin)
   - `DELETE /objects/admin/requests/{id}` - Supprimer une demande (admin)

3. **Tests**
   - Tests complets dans `backend/tests/test_admin_objects.py`
   - Couverture des cas nominaux et d'erreur

### Frontend (Angular)

1. **Composant AdminDashboard**
   - Interface pour visualiser les demandes en attente
   - Actions : Approuver, Rejeter, Supprimer
   - Champs pour notes admin

2. **Composant AdminAuth**
   - Dialog temporaire de vérification admin
   - Code temporaire : `admin123`

3. **Routes**
   - `/admin/auth` - Page d'authentification admin
   - `/admin/dashboard` - Dashboard admin (protégé par guard)

4. **Guard AdminGuard**
   - Protège les routes admin
   - Utilise localStorage temporairement

## 🚀 Mise en route

### 1. Migration de la base de données

```bash
cd backend
python migrate_object_requests.py
```

### 2. Lancer le backend

```bash
cd backend
uvicorn main:app --reload
```

### 3. Lancer le frontend

```bash
cd frontend
npm start
```

### 4. Accéder au dashboard admin

1. Naviguer vers `http://localhost:4200/admin/auth`
2. Sélectionner "Oui" pour "Êtes-vous administrateur ?"
3. Entrer le code : `admin123`
4. Accéder au dashboard

## 📝 Workflow

### Pour les utilisateurs

1. L'utilisateur crée une demande d'objet via l'API
2. La demande est créée avec le statut `pending`
3. L'utilisateur est notifié quand l'admin prend une décision

### Pour les admins

1. L'admin se connecte via `/admin/auth`
2. Accède au dashboard où toutes les demandes en attente sont affichées
3. Peut pour chaque demande :
   - **Approuver** : L'objet est créé dans la base et associé à l'utilisateur
   - **Rejeter** : La demande est marquée comme rejetée avec notes
   - **Supprimer** : La demande est supprimée de la base

## 🔒 Sécurité (Temporaire)

⚠️ **ATTENTION** : L'authentification actuelle est temporaire !

- Utilise localStorage pour stocker l'état admin
- Code admin en dur : `admin123`
- Pas de vérification JWT

### TODO pour la production

- [ ] Implémenter JWT pour l'authentification
- [ ] Remplacer localStorage par tokens sécurisés
- [ ] Ajouter middleware de vérification du rôle admin
- [ ] Implémenter refresh tokens
- [ ] Ajouter logs d'audit pour les actions admin

## 🧪 Tests

### Lancer les tests backend

```bash
cd backend
pytest tests/test_admin_objects.py -v
```

### Tests couverts

- ✅ Création de demandes d'objets
- ✅ Récupération des demandes
- ✅ Approbation par admin (+ création de l'objet)
- ✅ Rejet par admin
- ✅ Suppression par admin
- ✅ Vérification des permissions (non-admin ne peut pas décider)
- ✅ Pas de double décision sur une même demande

## 📊 Modèle de données

```python
class ObjectRequest:
    id: int
    name: str
    category: ObjectCategory
    brand: Optional[str]
    model: Optional[str]
    purchase_date: Optional[datetime]
    manual_url: Optional[str]
    notes: Optional[str]
    status: ObjectRequestStatus  # pending, approved, rejected
    admin_notes: Optional[str]
    requester_id: int
    reviewed_by: Optional[int]
    created_at: datetime
    reviewed_at: Optional[datetime]
    parent_id: Optional[int]
```

## 🎨 Interface utilisateur

L'interface admin présente :
- **Liste des demandes** à gauche (scrollable)
- **Détails de la demande** à droite
- **Badges colorés** pour les catégories
- **Zone de notes admin** pour documenter les décisions
- **Boutons d'action** clairs (Approuver ✅, Rejeter ❌, Supprimer 🗑️)

## 🔄 Prochaines étapes

1. Intégrer le système d'authentification JWT
2. Ajouter des notifications pour les utilisateurs
3. Créer un historique des décisions admin
4. Ajouter des filtres et recherche dans le dashboard
5. Implémenter la pagination pour les grandes listes
