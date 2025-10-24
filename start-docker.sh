#!/bin/bash

# Script pour lancer uniquement PostgreSQL + PgAdmin (sans backend ni frontend)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🐳 Démarrage de PostgreSQL + PgAdmin uniquement..."
docker compose up -d postgres pgadmin

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
echo "Pour arrêter : docker compose down"
