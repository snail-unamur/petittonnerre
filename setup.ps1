# Script de setup initial du projet

Write-Host "🔧 Configuration initiale de Petit Tonnerre..."

# Backend setup
Write-Host "📦 Configuration du backend..."
Set-Location backend

# Créer l'environnement virtuel s'il n'existe pas
if (-not (Test-Path ".venv")) {
    Write-Host "Création de l'environnement virtuel..."
    python -m venv .venv
}

# Activer l'environnement et installer les dépendances
Write-Host "Activation de l'environnement virtuel..."
.\.venv\Scripts\Activate.ps1
Write-Host "Installation des dépendances Python..."
python -m pip install --upgrade pip
python -m pip install --only-binary psycopg2-binary -r requirements.txt

# Copier le fichier .env s'il n'existe pas
if (-not (Test-Path ".env")) {
    Write-Host "Création du fichier .env..."
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  N'oubliez pas de modifier .env avec vos paramètres!"
}

Set-Location ..

# Frontend setup (si nécessaire)
if (Test-Path "frontend") {
    Write-Host "🎨 Configuration du frontend..."
    Set-Location frontend
    Write-Host "Installation des dépendances Node.js..."
    npm install
    Set-Location ..
}

Write-Host "✅ Configuration terminée!"
Write-Host ""
Write-Host "Prochaines étapes:"
Write-Host "1. Démarrer PostgreSQL: docker-compose up -d"
Write-Host "2. Modifier backend/.env si nécessaire"
Write-Host "3. Lancer le projet: ./start.ps1"