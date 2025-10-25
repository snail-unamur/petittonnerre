# Script PowerShell pour lancer le mutation testing sur le backend
# Usage: .\run_mutation_testing.ps1 [-Quick] [-Report] [-Clean]

param(
    [switch]$Quick,
    [switch]$Report,
    [switch]$Clean
)

Write-Host "========================================" -ForegroundColor Blue
Write-Host "🧬 MUTATION TESTING - PETIT TONNERRE" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Vérifier si on est dans le bon dossier
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ Erreur: Veuillez exécuter ce script depuis le dossier backend/" -ForegroundColor Red
    exit 1
}

# Nettoyer les résultats précédents si demandé
if ($Clean) {
    Write-Host "🧹 Nettoyage des résultats précédents..." -ForegroundColor Yellow
    if (Test-Path ".mutmut-cache") { Remove-Item -Recurse -Force .mutmut-cache }
    if (Test-Path "mutmut-report.html") { Remove-Item -Force mutmut-report.html }
    if (Test-Path "html") { Remove-Item -Recurse -Force html }
    Write-Host ""
}

# Étape 1: Lancer via Docker
Write-Host "📦 Lancement du mutation testing dans Docker..." -ForegroundColor Blue
Write-Host ""

if ($Quick) {
    Write-Host "Mode rapide activé (échantillon de mutations)" -ForegroundColor Yellow
    docker exec -it petit_tonnerre_backend bash -c "cd /app && python -m pytest tests/ -v && mutmut run --paths-to-mutate=api/problems.py"
} else {
    docker exec -it petit_tonnerre_backend bash -c "cd /app && python -m pytest tests/ -v && mutmut run"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "📊 RÉSULTATS" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

docker exec -it petit_tonnerre_backend bash -c "cd /app && mutmut results"

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "📈 STATISTIQUES" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

docker exec -it petit_tonnerre_backend bash -c "cd /app && mutmut show"

# Générer un rapport HTML si demandé
if ($Report) {
    Write-Host ""
    Write-Host "📄 Génération du rapport HTML..." -ForegroundColor Blue
    docker exec -it petit_tonnerre_backend bash -c "cd /app && mutmut html"
    Write-Host "✅ Rapport généré: backend/html/index.html" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "💡 COMMANDES UTILES" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Voir tous les résultats:        " -NoNewline; Write-Host "docker exec petit_tonnerre_backend mutmut results" -ForegroundColor Yellow
Write-Host "Voir une mutation spécifique:   " -NoNewline; Write-Host "docker exec petit_tonnerre_backend mutmut show <id>" -ForegroundColor Yellow
Write-Host "Générer rapport HTML:           " -NoNewline; Write-Host "docker exec petit_tonnerre_backend mutmut html" -ForegroundColor Yellow
Write-Host "Nettoyer le cache:              " -NoNewline; Write-Host "docker exec petit_tonnerre_backend rm -rf .mutmut-cache" -ForegroundColor Yellow
Write-Host ""
