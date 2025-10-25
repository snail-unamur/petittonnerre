# Guide: Promouvoir un utilisateur en administrateur

## Méthode 1: Via PgAdmin (Interface graphique) ✅ RECOMMANDÉ

1. **Ouvrir PgAdmin**
   - URL: http://localhost:5050
   - Email: `admin@petittonnerre.com`
   - Password: `admin`

2. **Se connecter à la base de données**
   - Le serveur "Petit Tonnerre DB" devrait apparaître automatiquement
   - Sinon, créez-le avec:
     - Host: `postgres`
     - Port: `5432`
     - Database: `petittonnerre_db`
     - Username: `petittonnerre`
     - Password: `petittonnerre`

3. **Ouvrir l'éditeur SQL**
   - Clic droit sur `petittonnerre_db` > "Query Tool"

4. **Promouvoir l'utilisateur en admin**
   ```sql
   -- Voir tous les utilisateurs
   SELECT id, email, username, role FROM users;
   
   -- Promouvoir par email
   UPDATE users 
   SET role = 'admin' 
   WHERE email = 'admin@petittonnerre.com';
   
   -- OU promouvoir par ID
   UPDATE users 
   SET role = 'admin' 
   WHERE id = 1;
   
   -- Vérifier
   SELECT id, email, username, role FROM users WHERE role = 'admin';
   ```

5. **Exécuter**
   - Cliquer sur le bouton "Execute/Refresh" (F5)
   - Vérifier que "UPDATE 1" apparaît en bas

## Méthode 2: Via ligne de commande Docker

```bash
# Se connecter au conteneur PostgreSQL
sudo docker exec -it petit_tonnerre_db psql -U petittonnerre -d petittonnerre_db

# Promouvoir l'utilisateur
UPDATE users SET role = 'admin' WHERE email = 'admin@petittonnerre.com';

# Vérifier
SELECT id, email, username, role FROM users WHERE role = 'admin';

# Quitter
\q
```

## Méthode 3: Créer directement un admin avec SQL

```sql
-- Dans PgAdmin ou psql

INSERT INTO users (email, username, hashed_password, role, is_active, location, created_at)
VALUES (
  'admin@petittonnerre.com',
  'admin',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyB3nB5fPuWa',  -- Hash de "Admin1234!"
  'admin',
  true,
  'Bruxelles',
  NOW()
);
```

**Note**: Le hash ci-dessus est celui de "Admin1234!" mais il est recommandé d'utiliser l'API pour créer les utilisateurs.

## Vérification

### Via PgAdmin
```sql
SELECT id, email, username, role, is_active FROM users;
```

### Via API
```bash
curl http://localhost:8000/users/
```

Cherchez l'utilisateur et vérifiez que `"role": "admin"`.

## Tester l'accès admin

1. Allez sur http://localhost:4200/admin/auth
2. Sélectionnez "Oui" pour "Êtes-vous administrateur ?"
3. Entrez le code: `admin123`
4. Vous devriez voir le dashboard admin

## En cas de problème

### L'utilisateur n'apparaît pas
```sql
-- Lister tous les utilisateurs
SELECT * FROM users;

-- Si vide, créer via l'API:
```
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@petittonnerre.com",
    "username": "admin",
    "password": "Admin1234!",
    "password_confirm": "Admin1234!"
  }'
```

### Le rôle ne change pas
```sql
-- Vérifier les valeurs possibles
SELECT DISTINCT role FROM users;

-- Le rôle doit être exactement 'admin' (minuscules)
UPDATE users SET role = 'admin' WHERE email = 'admin@petittonnerre.com';
```

### Réinitialiser un admin
```sql
-- Supprimer l'admin existant
DELETE FROM users WHERE email = 'admin@petittonnerre.com';

-- Puis recréer via l'API ou le script
```
