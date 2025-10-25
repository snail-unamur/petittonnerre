# Scripts de création de données

## Créer un administrateur et des données de test

### Méthode 1: Via Docker (RECOMMANDÉ) ✅

```bash
# Depuis la racine du projet
sudo docker exec petit_tonnerre_backend python create_admin_test_data.py
```

**Crée:**
- 1 utilisateur admin (email: `admin@petittonnerre.com`, password: `Admin1234!`)
- 3 utilisateurs normaux
- 5 demandes d'objets en attente

### Méthode 2: Via API REST (si problème bcrypt)

```bash
# 1. Créer les utilisateurs et demandes via l'API
python create_admin_via_api.py

# 2. Promouvoir en admin via PgAdmin
# Voir docs/ADMIN_SETUP.md pour les instructions SQL
```

### Méthode 3: Données générales (sans admin)

```bash
sudo docker exec petit_tonnerre_backend python create_test_data.py
```

## Problèmes courants

### `ModuleNotFoundError: No module named 'sqlalchemy'`

Vous essayez d'exécuter le script localement sans dépendances. Utilisez Docker:

```bash
sudo docker exec petit_tonnerre_backend python create_admin_test_data.py
```

### `Error: password cannot be longer than 72 bytes`

Problème de version bcrypt. Solutions:

1. **Rebuild Docker avec les nouvelles dépendances:**
   ```bash
   ./start.sh --build
   ```

2. **OU utiliser le script via API:**
   ```bash
   python create_admin_via_api.py
   ```

### Comment vérifier que l'admin est créé ?

**Via PgAdmin:**
```sql
SELECT id, email, username, role FROM users WHERE role = 'admin';
```

**Via API:**
```bash
curl http://localhost:8000/users/
```

## Accéder au dashboard admin

1. URL: http://localhost:4200/admin/auth
2. Sélectionner "Oui"
3. Code: `admin123`
4. Dashboard: http://localhost:4200/admin/dashboard

## Documentation complète

- **Setup admin**: `docs/ADMIN_SETUP.md`
- **Feature admin**: `docs/FEATURE_ADMIN.md`
- **Commandes**: `COMMANDS.md`
