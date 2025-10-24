#!/bin/bash

# Script pour réinitialiser complètement la base de données

echo "⚠️  ATTENTION : Ce script va supprimer TOUTES les données !"
echo ""
read -p "Êtes-vous sûr de vouloir continuer ? (oui/non) : " confirmation

if [ "$confirmation" != "oui" ]; then
    echo "❌ Opération annulée."
    exit 0
fi

echo ""
echo "🗑️  Suppression de toutes les données..."

# Se connecter à PostgreSQL et supprimer toutes les tables
docker exec -it petit_tonnerre_db psql -U petittonnerre -d petittonnerre_db -c "
DROP TABLE IF EXISTS object_tags CASCADE;
DROP TABLE IF EXISTS maintenance_tasks CASCADE;
DROP TABLE IF EXISTS contributions CASCADE;
DROP TABLE IF EXISTS maintenance_advice CASCADE;
DROP TABLE IF EXISTS objects CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS users CASCADE;
"

echo ""
echo "✅ Tables supprimées !"
echo ""
echo "🔄 Recréation des tables..."

cd backend
source .venv/bin/activate
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine); print('✅ Tables créées!')"

echo ""
echo "📊 Création de données de test..."
python create_test_data.py

echo ""
echo "✨ Base de données réinitialisée avec succès !"
echo ""
echo "🔍 Vérification :"
docker exec -it petit_tonnerre_db psql -U petittonnerre -d petittonnerre_db -c "\dt"
