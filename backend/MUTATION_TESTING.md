# 🧬 Mutation Testing - Petit Tonnerre Backend

## 📖 Qu'est-ce que le Mutation Testing ?

Le **mutation testing** est une technique avancée de test qui permet de mesurer la **qualité de vos tests** plutôt que juste la couverture de code.

### Comment ça marche ?

1. **Mutation** : L'outil modifie automatiquement votre code source (exemple: `+` devient `-`, `==` devient `!=`, etc.)
2. **Test** : Il relance vos tests sur le code muté
3. **Analyse** :
   - ✅ Si un test échoue → **Mutation tuée** (bon signe, vos tests détectent le bug)
   - ❌ Si tous les tests passent → **Mutation survivante** (mauvais signe, vos tests n'ont pas détecté le bug)

### Pourquoi c'est important ?

Avoir 100% de couverture de code ne signifie pas que vos tests sont bons. Le mutation testing révèle si vos assertions testent vraiment le comportement attendu.

## 🚀 Installation

Les dépendances sont déjà dans `requirements.txt` :
```bash
pip install mutmut pytest-cov
```

Ou via Docker :
```bash
docker exec -it petit_tonnerre_backend pip install mutmut pytest-cov
```

## 📋 Utilisation

### Option 1 : Via scripts (Recommandé)

**Linux/Mac/Git Bash :**
```bash
cd backend
chmod +x run_mutation_testing.sh
./run_mutation_testing.sh
```

**Windows PowerShell :**
```powershell
cd backend
.\run_mutation_testing.ps1
```

### Options disponibles :

```bash
# Mode rapide (teste seulement un fichier)
./run_mutation_testing.sh --quick

# Générer un rapport HTML
./run_mutation_testing.sh --report

# Nettoyer les résultats précédents
./run_mutation_testing.sh --clean

# Combiner plusieurs options
./run_mutation_testing.sh --clean --quick --report
```

### Option 2 : Via Docker (Manuel)

```bash
# Installer mutmut dans le container
docker exec -it petit_tonnerre_backend pip install mutmut

# Lancer le mutation testing
docker exec -it petit_tonnerre_backend bash -c "cd /app && mutmut run"

# Voir les résultats
docker exec -it petit_tonnerre_backend bash -c "cd /app && mutmut results"

# Voir les détails
docker exec -it petit_tonnerre_backend bash -c "cd /app && mutmut show"
```

### Option 3 : En local (sans Docker)

```bash
cd backend

# Lancer les tests normaux d'abord
python -m pytest tests/ -v

# Lancer le mutation testing
mutmut run

# Voir les résultats
mutmut results

# Voir les détails d'une mutation spécifique
mutmut show 1
```

## 📊 Comprendre les résultats

Après l'exécution, vous verrez un résumé comme :

```
Survived: 15
Killed: 85
Timeout: 0
Suspicious: 0
```

- **Killed (85)** : ✅ Mutations détectées par vos tests (bon !)
- **Survived (15)** : ❌ Mutations non détectées (améliorez vos tests)
- **Timeout** : Mutations qui ont causé une boucle infinie
- **Suspicious** : Résultats non concluants

### Score de mutation :
```
Mutation Score = Killed / (Killed + Survived) × 100
                = 85 / (85 + 15) × 100
                = 85%
```

**Objectif recommandé : > 80%**

## 🔍 Analyser une mutation survivante

```bash
# Voir les détails d'une mutation
mutmut show 5

# Cela affichera :
# - Le fichier modifié
# - La ligne de code originale
# - La mutation appliquée
```

Exemple de mutation :
```python
# Original
if user.role == UserRole.ADMIN:

# Muté en
if user.role != UserRole.ADMIN:
```

Si cette mutation **survit**, cela signifie que vous n'avez pas de test qui vérifie le comportement quand `user.role != ADMIN`.

## 📈 Rapport HTML

Pour générer un rapport HTML complet :

```bash
./run_mutation_testing.sh --report
# ou
mutmut html
```

Le rapport sera dans `backend/html/index.html`

## ⚙️ Configuration

### Fichiers de configuration

1. **`setup.cfg`** : Configuration principale de mutmut
   - Chemins à tester
   - Fichiers à exclure
   - Commande de test

2. **`.mutmut-config.py`** : Configuration avancée (hooks Python)
   - Filtrage personnalisé des mutations

### Personnaliser les chemins testés

Dans `setup.cfg` :
```ini
[mutmut]
paths_to_mutate=api/,models.py,schemas.py
paths_to_exclude=alembic/,tests/,init_data.py
```

## 🎯 Bonnes pratiques

### 1. Lancer régulièrement
```bash
# Avant chaque commit important
./run_mutation_testing.sh --quick

# Avant chaque release
./run_mutation_testing.sh --report
```

### 2. Cibler les fichiers critiques
```bash
# Tester seulement un fichier spécifique
mutmut run --paths-to-mutate=api/problems.py
```

### 3. Améliorer les tests pour les mutations survivantes

Si une mutation survit :
1. Analysez-la avec `mutmut show <id>`
2. Identifiez le cas de test manquant
3. Ajoutez un test pour ce cas
4. Relancez le mutation testing

### 4. Intégrer dans la CI/CD

Ajoutez dans votre pipeline :
```yaml
# .gitlab-ci.yml (exemple)
mutation-testing:
  stage: test
  script:
    - pip install mutmut
    - mutmut run
    - mutmut results
  allow_failure: true  # Au début
```

## 📚 Commandes utiles

```bash
# Lancer le mutation testing
mutmut run

# Voir tous les résultats
mutmut results

# Voir une mutation spécifique
mutmut show 5

# Appliquer une mutation pour tester manuellement
mutmut apply 5

# Revenir au code original
mutmut apply

# Générer un rapport HTML
mutmut html

# Nettoyer le cache
rm -rf .mutmut-cache
```

## 🐛 Dépannage

### "No mutations found"
- Vérifiez que `paths_to_mutate` dans `setup.cfg` pointe vers les bons fichiers
- Assurez-vous d'avoir du code à tester (pas juste des imports)

### "All tests failed"
- Lancez d'abord `pytest` pour vérifier que vos tests passent normalement
- Vérifiez que la commande `runner` dans `setup.cfg` est correcte

### Le mutation testing est très lent
- Utilisez `--quick` pour tester un seul fichier
- Utilisez `--use-coverage` pour ne tester que le code couvert
- Ciblez des fichiers spécifiques avec `--paths-to-mutate`

## 📖 Ressources

- [Documentation officielle mutmut](https://mutmut.readthedocs.io/)
- [Introduction au mutation testing](https://en.wikipedia.org/wiki/Mutation_testing)
- [Mutation testing best practices](https://pitest.org/)

## 🎯 Objectifs pour Petit Tonnerre

### Court terme
- [x] Configuration du mutation testing
- [ ] Score > 70% sur les endpoints critiques (auth, problems)
- [ ] Rapport HTML généré

### Moyen terme
- [ ] Score > 80% sur tout le backend
- [ ] Intégration dans la CI/CD
- [ ] Alertes sur les régressions de score

### Long terme
- [ ] Score > 90% sur les fonctionnalités business critiques
- [ ] Documentation des mutations courantes à surveiller
- [ ] Formation de l'équipe au mutation testing

---

**Bon mutation testing ! 🧬**
