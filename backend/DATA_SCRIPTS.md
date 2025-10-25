# Scripts de données

Ce dossier contient le script principal pour initialiser les données de l'application.

## Script principal

### init_data.py
Script unique pour initialiser toutes les données nécessaires au fonctionnement de l'application.

**⚠️ ATTENTION : Ce script RÉINITIALISE COMPLÈTEMENT la base de données !**
- Supprime toutes les tables existantes
- Recrée le schéma complet
- Insère les données de base ou de démonstration

**Ce qu'il fait :**
1. **Nettoyage complet** (toujours effectué) :
   - Suppression de toutes les tables
   - Recréation du schéma de la base de données

2. **Utilisateurs de base** (toujours créés) :
   - 1 administrateur : `admin@petittonnerre.com` / `Admin1234!`
   - 3 utilisateurs test : alice, bob, charlie (password: `Password123!`)

3. **Templates d'objets** (toujours créés) :
   - Chaudière Vaillant ecoTEC plus
   - Four Samsung pyrolyse
   - Lave-vaisselle Bosch
   - Robinet Grohe Eurosmart
   - Pierre bleue belge

4. **Données de démonstration** (mode complet seulement) :
   - Demandes d'objets pour l'admin
   - Objets créés depuis templates
   - Problèmes avec résolutions
   - Conseils d'entretien

**Usage:**

Mode complet (recommandé pour développement) :
```bash
python init_data.py --full
# ou simplement
python init_data.py
```

Mode utilisateurs seulement (minimum pour tester l'app) :
```bash
python init_data.py --users-only
```

**Avec Docker:**
```bash
# Mode complet
docker exec -it petit_tonnerre_backend python init_data.py

# Mode utilisateurs seulement
docker exec -it petit_tonnerre_backend python init_data.py --users-only
```

**Prérequis:**
- Pour le mode complet : L'API doit être accessible sur http://localhost:8000
- La base de données doit être initialisée

## Comptes créés

**Administrateur:**
- Email: `admin@petittonnerre.com`
- Password: `Admin1234!`
- Code admin temporaire: `admin123`

**Utilisateurs test:**
- `alice@example.com` / `Password123!` (Bruxelles)
- `bob@example.com` / `Password123!` (Liège)
- `charlie@example.com` / `Password123!` (Namur)

## URLs utiles

- API Documentation: http://localhost:8000/docs
- Application: http://localhost:4200
- Dashboard Admin: http://localhost:4200/admin/auth
