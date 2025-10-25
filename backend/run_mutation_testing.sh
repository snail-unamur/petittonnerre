#!/bin/bash

# Script pour lancer le mutation testing sur le backend
# Usage: ./run_mutation_testing.sh [options]
#
# Options:
#   --quick    Lance seulement un échantillon de mutations (plus rapide)
#   --report   Génère un rapport HTML
#   --clean    Nettoie les résultats précédents avant de lancer

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🧬 MUTATION TESTING - PETIT TONNERRE${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Vérifier si on est dans le bon dossier
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Erreur: Veuillez exécuter ce script depuis le dossier backend/${NC}"
    exit 1
fi

# Parser les arguments
QUICK_MODE=false
GENERATE_REPORT=false
CLEAN=false

for arg in "$@"
do
    case $arg in
        --quick)
        QUICK_MODE=true
        shift
        ;;
        --report)
        GENERATE_REPORT=true
        shift
        ;;
        --clean)
        CLEAN=true
        shift
        ;;
    esac
done

# Nettoyer les résultats précédents si demandé
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}🧹 Nettoyage des résultats précédents...${NC}"
    rm -rf .mutmut-cache
    rm -f mutmut-report.html
    echo ""
fi

# Étape 1: Installer les dépendances
echo -e "${BLUE}📦 Vérification des dépendances...${NC}"
pip install -q mutmut pytest-cov 2>/dev/null || true
echo -e "${GREEN}✅ Dépendances installées${NC}"
echo ""

# Étape 2: Lancer les tests normaux pour vérifier qu'ils passent
echo -e "${BLUE}🧪 Lancement des tests normaux...${NC}"
if python -m pytest tests/ -v --tb=short; then
    echo -e "${GREEN}✅ Tous les tests passent${NC}"
else
    echo -e "${RED}❌ Certains tests échouent. Veuillez les corriger avant de lancer le mutation testing.${NC}"
    exit 1
fi
echo ""

# Étape 3: Lancer le mutation testing
echo -e "${BLUE}🧬 Lancement du mutation testing...${NC}"
echo -e "${YELLOW}⚠️  Cela peut prendre plusieurs minutes...${NC}"
echo ""

if [ "$QUICK_MODE" = true ]; then
    echo -e "${YELLOW}Mode rapide activé (échantillon de mutations)${NC}"
    mutmut run --paths-to-mutate=api/problems.py --use-coverage || true
else
    mutmut run || true
fi

echo ""

# Étape 4: Afficher les résultats
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📊 RÉSULTATS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

mutmut results

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📈 STATISTIQUES${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

mutmut show

# Générer un rapport HTML si demandé
if [ "$GENERATE_REPORT" = true ]; then
    echo ""
    echo -e "${BLUE}📄 Génération du rapport HTML...${NC}"
    mutmut html
    echo -e "${GREEN}✅ Rapport généré: html/index.html${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}💡 COMMANDES UTILES${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Voir tous les résultats:        ${YELLOW}mutmut results${NC}"
echo -e "Voir une mutation spécifique:   ${YELLOW}mutmut show <id>${NC}"
echo -e "Appliquer une mutation:         ${YELLOW}mutmut apply <id>${NC}"
echo -e "Générer rapport HTML:           ${YELLOW}mutmut html${NC}"
echo -e "Nettoyer le cache:              ${YELLOW}rm -rf .mutmut-cache${NC}"
echo ""
