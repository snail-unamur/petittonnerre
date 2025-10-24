#!/bin/bash

# Script de test de l'API Petit Tonnerre
# Ce script teste les principaux endpoints de l'API

API_URL="http://localhost:8000"

echo "🧪 Tests de l'API Petit Tonnerre"
echo "================================="
echo ""

# Vérifier que l'API est accessible
echo "1️⃣ Test de connexion à l'API..."
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/)
if [ $response -eq 200 ]; then
    echo "✅ API accessible"
else
    echo "❌ API non accessible. Assurez-vous que le serveur est démarré."
    exit 1
fi
echo ""

# Test création d'utilisateur
echo "2️⃣ Test création d'utilisateur..."
user_response=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com",
        "username": "testuser",
        "location": "Bruxelles"
    }')

user_id=$(echo $user_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ ! -z "$user_id" ]; then
    echo "✅ Utilisateur créé avec l'ID: $user_id"
else
    echo "⚠️  L'utilisateur existe peut-être déjà ou erreur"
    # Essayer de récupérer un utilisateur existant
    user_id=1
fi
echo ""

# Test création d'objet
echo "3️⃣ Test création d'objet..."
object_response=$(curl -s -X POST "$API_URL/objects/?user_id=$user_id" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Chaudière Test",
        "category": "heating",
        "brand": "Vaillant",
        "model": "ecoTEC"
    }')

object_id=$(echo $object_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ ! -z "$object_id" ]; then
    echo "✅ Objet créé avec l'ID: $object_id"
else
    echo "❌ Erreur lors de la création de l'objet"
fi
echo ""

# Test liste des objets
echo "4️⃣ Test liste des objets..."
objects_list=$(curl -s "$API_URL/objects/")
objects_count=$(echo $objects_list | grep -o '"id":' | wc -l | tr -d ' ')
echo "✅ Nombre d'objets trouvés: $objects_count"
echo ""

# Test création de conseil d'entretien
echo "5️⃣ Test création de conseil d'entretien..."
advice_response=$(curl -s -X POST "$API_URL/maintenance/advice" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Contrôle annuel",
        "description": "Vérification annuelle de la chaudière",
        "frequency_days": 365,
        "category": "heating"
    }')

advice_id=$(echo $advice_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ ! -z "$advice_id" ]; then
    echo "✅ Conseil créé avec l'ID: $advice_id"
else
    echo "❌ Erreur lors de la création du conseil"
fi
echo ""

# Test création de tâche de maintenance
echo "6️⃣ Test création de tâche de maintenance..."
if [ ! -z "$object_id" ] && [ ! -z "$advice_id" ]; then
    task_response=$(curl -s -X POST "$API_URL/maintenance/tasks?user_id=$user_id" \
        -H "Content-Type: application/json" \
        -d "{
            \"scheduled_date\": \"2025-11-01T10:00:00\",
            \"notes\": \"Tâche de test\",
            \"object_id\": $object_id,
            \"advice_id\": $advice_id
        }")
    
    task_id=$(echo $task_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)
    
    if [ ! -z "$task_id" ]; then
        echo "✅ Tâche créée avec l'ID: $task_id"
    else
        echo "❌ Erreur lors de la création de la tâche"
    fi
else
    echo "⚠️  Impossible de créer la tâche (objet ou conseil manquant)"
fi
echo ""

# Test création de contribution
echo "7️⃣ Test création de contribution communautaire..."
contribution_response=$(curl -s -X POST "$API_URL/community/contributions?author_id=$user_id" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Astuce nettoyage",
        "content": "Utiliser du vinaigre blanc pour détartrer",
        "category": "heating"
    }')

contribution_id=$(echo $contribution_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ ! -z "$contribution_id" ]; then
    echo "✅ Contribution créée avec l'ID: $contribution_id"
    
    # Test vote
    echo "   └─ Test vote pour la contribution..."
    vote_response=$(curl -s -X POST "$API_URL/community/contributions/$contribution_id/upvote")
    echo "   ✅ Vote enregistré"
else
    echo "❌ Erreur lors de la création de la contribution"
fi
echo ""

# Résumé
echo "================================="
echo "✅ Tests terminés !"
echo ""
echo "📊 Résumé :"
echo "  • Utilisateur ID: $user_id"
echo "  • Objet ID: $object_id"
echo "  • Conseil ID: $advice_id"
echo "  • Tâche ID: $task_id"
echo "  • Contribution ID: $contribution_id"
echo ""
echo "🌐 Consultez la documentation : $API_URL/docs"
