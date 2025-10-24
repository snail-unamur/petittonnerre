#!/bin/bash

# Script pour lancer Docker Compose depuis n'importe où dans le projet

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/pgadmin"

echo "🐳 Démarrage de PostgreSQL + PgAdmin..."
docker compose up -d

echo ""
echo "✅ Services démarrés !"
echo ""
echo "📊 PostgreSQL : localhost:5432"
echo "   Database: petittonnerre_db"
echo "   User: petittonnerre"
echo "   Password: petittonnerre"
echo ""
echo "🗄️  PgAdmin : http://localhost:5050"
echo "   Email: admin@petittonnerre.com"
echo "   Password: admin"
echo ""
echo "💡 Le serveur 'Petit Tonnerre DB' est déjà configuré dans PgAdmin !"
echo ""
echo "Pour arrêter : cd pgadmin && docker compose down"
