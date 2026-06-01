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
La première étape de l'analyse a consisté à explorer le projet dans son ensemble : vérification du fonctionnement de l'application, présence de tests, structure générale du code.
Nous avions initialement envisagé de mettre en parallèle les prompts utilisés avec les commits et pull requests afin d'en faire une donnée d'analyse supplémentaire. Cette piste a cependant dû être abandonnée par manque d'informations : les métadonnées des modèles d'IA utilisés étaient incomplètes, les timestamps absents, et aucun lien fiable ne pouvait être établi avec les commits.
Le dépôt étant hébergé sur un GitLab privé, la sélection des outils d'analyse statique a été contrainte par la nécessité de trouver des solutions compatibles avec ce contexte et gratuites. Après exploration de plusieurs outils — SonarQube, CodeScene, Trivy, Hercules, ainsi que des alternatives comme PMD ou Semgrep — les analyses de SonarQube et CodeScene se sont révélées les plus pertinentes. Un script de repomining basé sur PyDriller a d'abord été utilisé pour extraire les identifiants des pull requests. Sur cette base, une analyse SonarQube automatisée a été exécutée à chaque pull request afin de disposer d'une évolution temporelle des métriques de qualité.
Afin de rendre les données exploitables et partageables, il a été décidé d'anonymiser le projet et de le publier sur un dépôt public.

En parallèle des analyses SonarQube et CodeScene, d'autres outils d'analyse statique ont été intégrés à notre processus d'analyse. L'outil Radon a été utilisé pour évaluer la complexité cyclomatique et le volume (SLOC) du code Python. Le compilateur TypeScript, quant à lui, nous a permis d'extraire les erreurs de typage ainsi que les vulnérabilités du frontend. L'outil JSCPD a été employé pour mesurer le pourcentage de duplication de code à travers le projet. Nous avons également extrait des métriques de Git à l'aide de l'outil GitDelver.

Une fois l'ensemble de ces métriques récupérées, nous avons procédé au croisement de ces données et à leur structuration au sein d'un jeu de données (dataset). Lors de cette phase de structuration, un travail de nettoyage des données a été réalisé. Nous nous sommes ensuite consacrés à une tâche de résolution d'identité : les développeurs ayant utilisé de nombreux alias au cours du projet, il était nécessaire de les fusionner. Une fois cette unification réalisée, une anonymisation des auteurs a été appliquée à l'aide de l'outil git-filter-repo.

Pour terminer, la migration du dépôt initial GitLab vers un dépôt GitHub public a constitué un défi méthodologique. Le transfert entre ces deux gestionnaires de versions a entraîné la perte des Merge Requests ainsi qu'une altération de l'historique Git, cela étant dû au fonctionnement différent des deux systèmes. De nombreuses requêtes de fusion ayant été réalisées à l'aide de l'option squash de GitLab, certains identifiants de commit originaux ont soit été modifiés, soit détruits. Pour conserver l'intégrité de notre dataset, une vérification a dû être effectuée et une réaffectation manuelle des identifiants de commits (Commit IDs) a été opérée sur le fichier data.csv, ainsi que sur le fichier resultats_mr.json. Dans le cas de ce deuxième fichier, le squash ayant fusionné des commits, une perte de données a dû être recensée et documentée au sein dudit fichier afin d'assurer la transparence de nos données.

L'analyse des tests présents a également été effectuée, mais la plupart des tests ne fonctionnant tout simplement pas, les résultats, tel que le coverage, n'ont pas été conservés car ils s'avéraient non pertinents.
### Analyse qualitative
L'analyse qualitative repose sur un examen ciblé d'un sous-ensemble de fichiers analysés via CodeScene. L'objectif n'est pas d'être exhaustif, mais d'illustrer une limite importante de ce type d'outil : un score de code health élevé n'est pas nécessairement le signe d'un code exempt de problèmes d'implémentation, et inversement, un score faible ne signifie pas que le code est inutilisable. CodeScene étant conçu pour analyser du code produit par des développeurs humains, ses résultats ne sont pas nécessairement représentatifs de la qualité réelle d'un code généré par un agent LLM. Le détail de cette analyse est disponible en annexe.
## Résultats

### Analyse statique
Le projet étant fait en un weekend, les métriques ont évolués très rapidement. Le nombre de lignes de code a dépassé 6000, dont certains fichiers à plus de mille lignes de code. La dette technique s'est vite accumulée avec plus d'une centaine de code smells. Les erreurs TypeScript sont également nombreuses et la concentration des modifications sur certains fichiers est très importante, comme _api.service.ts_ et _schemas.py_, montrant un problème la définition de l'architecture et les séparation des responsabilités.

### Analyse qualitative
Comme mentionné dans [codescene_qualitative_analysis](data/codescene_qualitative_analysis.md), les outils d'analyse statique traditionnels montrent leurs limites lorsque l'on souhaite déterminer la qualité d'un projet généré par IA. Un _Code Health_ élevé ne garantit pas une architecture saine. Par exemple, le fichier _api.service.ts_ mentionné au point précédant comme problématique a tout de même obtenu un bon score sur CodeScene alors qu'il possède plus d'une centaine de lignes de code inutilisées. Certains problèmes architecturaux pourraient donc échapper aux outils utilisés.

D'un point de vue utilisateur, la qualité globale de l'application générée s'avère largement insuffisante. Les tests d'utilisation révèlent de nombreuses lacunes tant sur le plan technique qu'ergonomique:
1. Une grande part des fonctionnalités sont soit non fonctionelles, soit instable (présence de nombreux bugs).
2. L'interface utilisateur manque de cohérence. De nombreux boutons sont redondants, dupliqués, mal positionnés, ou d'utilité questionables. Les thèmes visuels ne sont pas appliqués correctement partout.
3. L'application présente des failles de sécurité basiques (IDOR).

## Discussion
Comme cité plus haut, le modèle d'intelligence artificiel était utilisé en mode "agent" et non selon un paradigme de "planification-action". Cette dernière approche est pourtant notoirement connue pour sa capacité à améliorer la qualité d'excécution des modèles. À cela s'ajoute le fait que la méthode d'écriture des prompts était purement chaotique et le prompt système s'est vu pollué par les blagues des développeurs. La structure des réponses, et donc la fenêtre de contexte, s'en est trouvée dégradée qualitativement, ce qui a certainement contribué à un grand nombre d'erreurs dans le code. 

De plus, l'imprécision et la qualité médiocre de ces requêtes ont directement conduit à une gestion désordonnée du dépôt GitLab. Les instructions données à l'agent ont générés des erreurs en cascade: développement direct sur la branche _main_, des revert commits effectués dans l'urgence pour annuler les mauvaises actions de l'IA, et la branche _dev_ qui est devenue la  branche principale.

## Conclusion
Ce projet exploratoire visait à évaluer la qualité d'une application entièrement générée par un agent LLM. 
L'expérience menée autour de Petit Tonnerre confirme qu'il est possible de produire en 24 heures une application 
fonctionnelle, mais que cette faisabilité technique ne garantit en rien sa qualité.
L'analyse statique révèle une dette technique accumulée très rapidement (volume de code élevé, nombreux code smells, erreurs de typage, architecture mal définie), tandis que l'analyse qualitative montre une application largement insuffisante pour l'utilisateur final : fonctionnalités instables, interface incohérente, failles de sécurité élémentaires. Surtout, elle souligne une limite méthodologique : les outils conçus pour du code humain, comme CodeScene, peinent à rendre compte de la qualité réelle d'un code généré par IA, un bon score pouvant masquer des défauts structurels.

Ces résultats s'expliquent toutefois en grande partie par les conditions de l'expérience : un mode « agent » sans phase de planification, des prompts désordonnés et une méthodologie big bang sans réelle coordination. Le problème peut aussi bien venir de la manière de procéder que du modèle lui-même. Comme il s'agit d'un cas unique réalisé dans des conditions très particulières, ces conclusions ne peuvent pas être généralisées.

Évaluer du code généré par IA nécessite de repenser les outils ainsi que les critères d'évaluation. Par ailleurs, l'impossibilité de relier les prompts aux commits et pull requests, faute de métadonnées exploitables, nous a privés d'un axe d'analyse précieux. De futurs travaux sur un sujet similaire gagneraient donc à collecter systématiquement ces données au niveau des prompts, afin de déterminer dans quelle mesure la qualité du code dépend du modèle d'IA lui-même plutôt que de la formulation des requêtes, et à comparer plusieurs configurations d'agents pour cerner les conditions dans lesquelles ces outils performent.