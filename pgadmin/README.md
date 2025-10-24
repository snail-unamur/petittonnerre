# Configuration PgAdmin

Ce dossier contient la configuration pour pré-charger la connexion à la base de données dans PgAdmin.

## Fichiers

- **servers.json** : Configuration du serveur PostgreSQL
- **pgpass** : Fichier de mot de passe (format PostgreSQL)

## Fonctionnement

Au démarrage de PgAdmin, ces fichiers sont automatiquement chargés pour :
- Afficher le serveur "Petit Tonnerre DB" dans la liste des serveurs
- Se connecter automatiquement sans demander de mot de passe

## Modification

Si tu changes les identifiants PostgreSQL dans `docker-compose.yml`, mets à jour :

1. **pgpass** : Format `host:port:database:username:password`
2. **servers.json** : Champs `Host`, `Port`, `MaintenanceDB`, `Username`

Ensuite redémarre PgAdmin :
```bash
docker compose restart pgadmin
```
