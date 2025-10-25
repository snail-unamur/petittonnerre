#!/bin/bash

# Script pour démarrer uniquement ce qui est nécessaire en développement
# Utilise les conteneurs existants sans rebuild

echo "🚀 Démarrage rapide en mode développement..."
echo ""

# Démarrer sans rebuild
docker compose up -d

echo ""
echo "⏳ Vérification des services..."
sleep 3

# Vérifier que les services sont up
if docker ps | grep -q "petit_tonnerre"; then
  echo ""
  echo "✅ Services démarrés avec succès !"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📊 PostgreSQL    : localhost:5432"
  echo "🗄️  PgAdmin       : http://localhost:5050"
  echo "🔧 Backend API   : http://localhost:8000/docs"
  echo "🎨 Frontend      : http://localhost:4200"
  echo "🛠️  Admin Dashboard: http://localhost:4200/admin/auth"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "💡 Commandes utiles :"
  echo "   docker compose logs -f backend   # Logs du backend"
  echo "   docker compose restart backend   # Redémarrer le backend"
  echo "   ./start.sh --build              # Rebuild complet si nécessaire"
  echo ""
else
  echo ""
  echo "⚠️  Les services ne semblent pas démarrés correctement."
  echo "💡 Essayez: ./start.sh --build"
  echo ""
fi
