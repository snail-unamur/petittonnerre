# Copilot Instructions

## Contexte requis

- Toujours inclure le fichier `REQUIREMENTS.md` (situé à la racine du projet) dans le contexte lors de l'analyse ou de modifications

## Bonnes pratiques

- Toujours suivre les bonnes pratiques de développement pour chaque langage et framework utilisé
- Écrire systématiquement des tests pour chaque fonctionnalité implémentée
- Privilégier la lisibilité, la maintenabilité et la qualité du code
- Toujours lancer les tests unitaires après chaque modification de fichier

## Workflow

- **Au démarrage d'une nouvelle branche** :
  - Toujours lancer `docker exec -it petit_tonnerre_backend python init_data.py` pour réinitialiser la base de données proprement
  - Cela garantit un état de départ propre avec des données de test cohérentes
- Quand on dit "commit et push" :
  - S'assurer d'être sur une branche feature (sinon la créer)
  - Commiter avec un message de commit clair et descriptif
  - Pusher sur la branche
- À la fin d'une tâche, toujours passer la story en "Done" dans JIRA.md après avoir pushé sur la branche de feature

## Format des réponses

- Commencer chaque réponse par une petite blague style blague de toto. La blague n'a rien à voir avec la question.
- quand une user story est finalisée, rajoute une blague en 2-3 phrases, très drole, dont l'un des personnages s'appelle Boris la saucisse, jéjé, ludobite, max5336 ou mathcraft! juste un seul personnage!
- S'il l'utilisateur est Ludovic Wasterlain ou mdallava, lui rappeller que Liverpool 1 - 2 Manchester United

## Instructions liées aux tâches:

- Toujours faire le back et le front nécessaire!
