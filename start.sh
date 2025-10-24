#!/bin/bash

# Script de démarrage rapide pour le projet Petit Tonnerre

echo "🚀 Démarrage de Petit Tonnerre..."

# Démarrer PostgreSQL avec Docker
echo "📦 Démarrage de PostgreSQL..."
docker-compose up -d

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente de PostgreSQL..."
sleep 5

# Démarrer le backend
echo "🔧 Démarrage du backend FastAPI..."
cd backend
# Vérifier quel fichier d'activation existe
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Erreur: Environnement virtuel non trouvé!"
    exit 1
fi
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Attendre un peu
sleep 2

# Démarrer le frontend (si disponible)
if [ -d "frontend" ]; then
    echo "🎨 Démarrage du frontend Angular..."
    cd ../frontend
    npm start &
    FRONTEND_PID=$!
fi

echo "✅ Projet démarré!"
echo "📖 API: http://localhost:8000/docs"
echo "🌐 Frontend: http://localhost:4200"
echo ""
echo "Pour arrêter: Ctrl+C"

# Attendre que les processus se terminent
wait
