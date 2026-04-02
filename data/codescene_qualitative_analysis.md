# Analyse Qualitative CodeScene - Détection des Code Smells

## Partie Analyse Qualitative (file by file)
L'objectif ici n'est pas de faire une analyse exhaustive mais plutot de mettre en avant qu'une analyse code scene qui détermine un haut **code health** ne signifie pas que le code est sans manquements d'implémentation et à l'inverse qu'une analyse ayant un bas **code health** présente plusieurs manquements.

### 1. local_clones/frontend/src/app/core/services/api.service.ts

**Métadonnées:**
- **Code Health**: 9.38/10 (Haut)
- **Lignes de code**: 449
- **Change Frequency**: 17

**Code Smells détectés:**

1. **Complex Method** (Advisory)
   - Une méthode a des if appelés les uns à la suite des autres
   - Une telle méthode ne serait pas passée dans un processus de développement classique

2. **Primitive Obsession** (Advisory)
   - Globalement sur le fichier il y a beaucoup de Any, et beaucoup de méthodes ont plusieurs params: number ce qui peut amener confusion quant à l'utilisation des méthodes (Merci Refactoring guru)

**Notes supplémentaires:**
- Beaucoup de code inutilisé (un peu plus d'une centaine de lignes sur un fichier de 449 lignes)

---

### 2. local_clones/backend/main.py

**Métadonnées:**
- **Code Health**: 9.34/10 (Haut)
- **Lignes de code**: 168
- **Change Frequency**: 13

**Code Smells détectés:**

1. **Bumpy Road** (Critical)
   - Niveaux d'abstraction incohérents dans le code (route api dans le main)
   - Mélange de détails d'implémentation de bas niveau et de logique de haut niveau (création de la connection à la db au début de l'exécution et qui reste ouverte tout au long du runtime)

2. **Large Method** (Advisory)
   - Méthode trop longue nécessitant d'être décomposée

---

### 3. local_clones/frontend/src/app/features/objects/objects.component.ts

**Métadonnées:**
- **Code Health**: 9.08/10 (Haut)
- **Lignes de code**: 1464
- **Change Frequency**: 13

**Code Smells détectés:**

1. **Complex Method** (Advisory)
   - switch complexe qui pourrait extérioriser une partie de la logique

2. **Complex Conditional** (Advisory - 1 occurrence)
   - Severity: Warning
   - condition de if complexe (qui peut arriver en dev)

---

### 4. local_clones/backend/api/users.py

**Métadonnées:**
- **Code Health**: 8.54/10 (Moyen-Haut)
- **Lignes de code**: 188
- **Change Frequency**: 12

**Code Smells détectés:**

1. **Many Conditionals** (Advisory)
   - on a une méthode qui fait 50 lignes avec beaucoup de vérifications qui peuvent être extéiorisés
2. **Complex Method** (Advisory)
   - idem

3. **High Degree of Code Duplication** (Advisory)

---

### 5. local_clones/backend/api/problems.py

**Métadonnées:**
- **Code Health**: 5.25/10 (Bas) ⚠️
- **Lignes de code**: 748
- **Change Frequency**: 6

**Code Smells détectés:**

1. **Low Cohesion** (Critical)
   - Manque de cohésion dans le fichier - responsabilités trop dispersées

2. **Many Conditionals** (Advisory)
   - Trop de conditions dans le code

3. **Complex Method** (Advisory - 5 occurrences)
   - Plusieurs méthodes avec complexité élevée

4. **Code Duplication** (Advisory - 14 occurrences)
   - Duplication de code importante

5. **Excess Number of Function Arguments** (Advisory - 2 occurrences)
   - Trop de paramètres dans les fonctions

**Notes:**
- **Priorité haute**: Ce fichier a le score de santé le plus bas (5.25/10) et présente de multiples problèmes critiques
- Nécessite une refactorisation majeure
