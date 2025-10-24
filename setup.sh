#!/bin/bash

# Script de setup initial du projet

echo "🔧 Configuration initiale de Petit Tonnerre..."

# Backend setup
echo "📦 Configuration du backend..."
cd backend

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d ".venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activer l'environnement et installer les dépendances
source .venv/bin/activate
echo "Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Copier le fichier .env s'il n'existe pas
if [ ! -f ".env" ]; then
    echo "Création du fichier .env..."
    cp .env.example .env
    echo "⚠️  N'oubliez pas de modifier .env avec vos paramètres!"
fi

cd ..

# Frontend setup (si nécessaire)
if [ -d "frontend" ]; then
    echo "🎨 Configuration du frontend..."
    cd frontend
    echo "Installation des dépendances Node.js..."
    npm install
    cd ..
fi

echo "✅ Configuration terminée!"
echo ""
echo "Prochaines étapes:"
echo "1. Démarrer PostgreSQL: docker-compose up -d"
echo "2. Modifier backend/.env si nécessaire"
echo "3. Lancer le projet: ./start.sh"
