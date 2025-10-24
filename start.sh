#!/bin/bash

# Script pour démarrer tous les services Docker

echo "� Démarrage de tous les services Docker..."
echo ""

# Arrêter les anciens conteneurs si ils existent
echo "🧹 Nettoyage des anciens conteneurs..."
docker compose down

echo ""
echo "� Construction et démarrage des services..."
docker compose up --build -d

echo ""
echo "⏳ Attente du démarrage des services..."
sleep 10

echo ""
echo "✅ Services démarrés !"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 PostgreSQL    : localhost:5432"
echo "   Database      : petittonnerre_db"
echo "   User          : petittonnerre"
echo "   Password      : petittonnerre"
echo ""
echo "🗄️  PgAdmin       : http://localhost:5050"
echo "   Email         : admin@petittonnerre.com"
echo "   Password      : admin"
echo ""
echo "🔧 Backend API   : http://localhost:8000"
echo "   Docs          : http://localhost:8000/docs"
echo ""
echo "🎨 Frontend      : http://localhost:4200"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Le serveur PostgreSQL est pré-configuré dans PgAdmin !"
echo ""
echo "� Commandes utiles :"
echo "   docker compose logs -f          # Voir tous les logs"
echo "   docker compose logs -f backend  # Logs du backend"
echo "   docker compose logs -f frontend # Logs du frontend"
echo "   docker compose down             # Arrêter tout"
echo "   docker compose restart          # Redémarrer tout"
echo ""