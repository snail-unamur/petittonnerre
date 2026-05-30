[Consulter le README initial du projet](ORIGINAL_README.md)

# Rapport de projet de recherche exploratoire

## Objectif
L'objectif de ce projet de recherche est d'analyser sur base de critères objectifs et subjectifs la qualité d'un projet de développement logiciel entièrement réalisé à l'aide d'un agent basé sur un large modèle de langage (LLM).

## Contexte
Ce dépôt contient le code source d'une application de gestion intelligente et collaborative de l'entretien d'objets et appareils domestiques, appelée _Petit Tonnerre_.

La spécificité de cette application est qu'elle est le fruit d'un défi lancé entre quatre développeurs, qui se sont donnés pour objectif de générer une application complète en un peu plus de 24 heures à l'aide de larges modèles de langage (LLM). Les développeurs n'ont donc théoriquement pas écrit une seule ligne de code manuellement, mais ont simplement supervisé l'outil de génération de code.

### Outils et technologies utilisés

#### Outils d'intelligence artificielle
L'agent choisi pour ce projet est _GitHub Copilot_, configuré en mode "agent", il n'y a donc pas de distinction entre la phase de planification et la phase d'action, comme on peut trouver dans de nombreux agents plus modernes. L'agent effectue directement les modifications demandées depuis la fenêtre de _chat_, sans validation humaine entre la phase de conception et la phase d'action. Le modèle utilisé est _Claude Sonnet 4.5_.

#### Approche et méthodologie de développement
L'approche adoptée pour le développement de l'application comprend plusieurs étapes :
1. Concept général ? + Structure du projet
2. Explication du concept de l'application à l'agent et génération des spécifications fonctionnelles détaillées de l'application, divisées en _user stories_, elles-mêmes regroupées en plusieurs _epics_. (voir [REQUIREMENTS.md](REQUIREMENTS.md) et [JIRA.md](JIRA.md))
3. Sructure du projet ?
4. Implémentation des fonctionnalités de l'application en suivant une sorte de méthodologie _big bang_. Chaque développeur sélectionne une _epic_, tout le monde développe en même temps les fonctionnalités de sa propre _epic_ sur sa propre branche et sans se soucier de la coordination entre les développeurs. À chaque fonctionnalité terminée, le développeur crée une _pull request_ selon le processus décrit dans le point **Gestion de versions** ci-dessous. Une fois l'_epic_ achevée, le développeur sélectionne une nouvelle _epic_ et recommence le processus.

#### Gestion de versions
La gestion de versions (_commit_ et _push_) a été également entièrement confiée à l'agent. La seule action manuelle des développeurs a été de gérer le processus de création et de validation de _pull requests_, bien que la revue de code en elle-même était également automatisée via le processus suivant :
1. Le développeur teste manuellement la fonctionnalité développée par l'agent et estime qu'elle est prête a être intégrée à la branche principale.
2. Le développeur crée une _pull request_.
3. Un autre développeur visite la branche et demande à l'agent (toujours le même, dans la fenêtre de _chat_ de l'IDE) d'effectuer une revue de code.
4. Une fois la revue de code effectuée, le développeur copie le commentaire généré par l'agent et crée un commentaire sur la _pull request_.
5. Le développeur initial de la branche fournit le commentaire de l'agent à son propre agent, toujours dans la fenêtre de _chat_ de l'IDE, et lui demande de corriger les problèmes soulevés par l'agent relecteur.
6. Ce cycle continue jusqu'à ce que l'agent relecteur estime que les problèmes ont été corrigés, auquel cas le développeur peut fusionner la branche.

## Méthodologie
L'analyse de la qualité du projet sera effectuée via 2 axes distincts : une analyse statique via des outils d'analyse de code, et une analyse qualitative subjective 

### Analyse statique

### Analyse qualitative

## Résultats

### Analyse statique

### Analyse qualitative

## Discussion

## Conclusion
