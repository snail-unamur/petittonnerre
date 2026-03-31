# Analyse de la qualité d'une application vibe codée

## Contexte

Auteurs : Justin Frémy, Olan Heinen, Guillaume Sougne, Gianni Wetzels

DOI : ...

Objectif : Le vibe coding permet de produire des applications rapidement, mais leur qualité est incertaine. Des analyses ont été réalisées afin de mettre en évidence différents aspects de qualité de code.

## Système étudié

Domaine d'application : Système de gestion de maintenance d'appareils ménagers.

Caractéristiques techniques : 
- backend en Python
- frontend en TypeScript
- ~6000 LOC
- réalisé en un weekend en octobre 2025
- 4 développeurs

Le code source du projet analysé est privé.

## Méthodologie

### Outils utilisés :
- SonaQube
- Radon
- typeScript Compiler
- GitDelver
- JSCPD

## Dictionnaire des données

Le nom des développeurs ont été anonymisés.

| Nom de colonne    | Description | Valeur | Source |
| ------- | ------- | ------- | ------- |
| CommitId  | Identifiant unique d'un commit du dépôt Github du projet | texte | GitDelver
| Message | Message lié à un commit, décrivant celui-ci | texte | GitDelver
| BugFix    | Décris si le commit a résolu un bug | booléen | GitDelver
| NbModifiedFiles | Nombre de fichier modifiés dans un commit | entier | GitDelver
| NbInsertions | Nombre d'insertions effectuées dans un commit | entier | GitDelver
| NbDeletions | Nombre de suppression effectuée dans un commit | entier | GitDelver
| dataset_securite.Total_Vulnérabilités | Nombre de vulnérabilités trouvées | entier | typeScript Compiler
| dataset_radon.Complexite_Moyenne | Complexité cyclomatique moyenne | entier | Radon
| dataset_radon.Total_SLOC | Nombre total de lignes de code | entier | Radon
| dataset_radon.Commentaires | Nombre de commentaires présents | entier | Radon
| dataset_typescript.Erreurs_TypeScript |  | entier | Radon
| dataset_duplication.Duplication_Pourcentage | | pourcentage | JSCPD
| dataset_sonarqube_V2.Sonar_Dette_Technique_Min | | entier | Sonarqube
| dataset_sonarqube_V2.Sonar_Duplication_Pct | Densité de lignes dupliquées | pourcentage | Sonarqube
| dataset_sonarqube_V2.Sonar_Code_Smells | | entier | Sonarqube
| dataset_sonarqube_V2.Sonar_Bugs | | entier | SonarQube

## Licence et Utilisation
...