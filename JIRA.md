# Plan de Développement - Petit Tonnerre

## Epic 1: Création de comptes et logins 🔐

### US1.1: En tant qu'utilisateur, je veux pouvoir créer un compte

- [x] 1.1.1 Créer le modèle User dans la base de données (done)
- [x] 1.1.2 Implémenter l'API d'inscription avec validation des données (done)
- [x] 1.1.3 Créer le formulaire d'inscription frontend (done)
- [x] 1.1.4 Ajouter la validation côté frontend (done)
- [ ] 1.1.5 Écrire les tests unitaires backend (todo)
- [ ] 1.1.6 Écrire les tests e2e frontend (todo)

### US1.2: En tant qu'utilisateur, je veux pouvoir me connecter

- [ ] 1.2.1 Implémenter l'authentification JWT backend (in progress)
- [ ] 1.2.2 Créer les endpoints de login/logout (in progress)
- [ ] 1.2.3 Développer le formulaire de login frontend (todo)
- [ ] 1.2.4 Implémenter la gestion du token JWT côté frontend (todo)
- [ ] 1.2.5 Ajouter les guards Angular pour les routes protégées (todo)
- [ ] 1.2.6 Écrire les tests d'authentification backend (todo)

### US1.3: En tant qu'administrateur, je veux pouvoir gérer les utilisateurs

- [ ] 1.3.1 Créer l'interface d'administration des utilisateurs (todo)
- [ ] 1.3.2 Implémenter les endpoints CRUD admin pour les utilisateurs (todo)
- [ ] 1.3.3 Ajouter la gestion des rôles (admin/user) (todo)
- [ ] 1.3.4 Écrire les tests des endpoints admin (todo)

## Epic 2: Gestion des objets 📦

### US2.1: En tant qu'administrateur, je veux pouvoir créer et gérer le catalogue d'objets

- [ ] 2.1.1 Créer le modèle Object avec hiérarchie dans la DB (in progress)
- [ ] 2.1.2 Développer l'interface d'administration des objets (todo)
- [ ] 2.1.3 Implémenter les endpoints CRUD admin pour les objets (in progress)
- [ ] 2.1.4 Ajouter la gestion des caractéristiques des objets (todo)
- [ ] 2.1.5 Écrire les tests des endpoints objets (todo)

### US2.2: En tant qu'utilisateur, je veux pouvoir sélectionner mes objets

- [x] 2.2.1 Créer la table de liaison User-Objects dans la DB (done)
- [x] 2.2.2 Développer l'interface de sélection des objets (done)
- [x] 2.2.3 Implémenter les endpoints de gestion des objets utilisateur (done)
- [x] 2.2.4 Ajouter la validation des permissions (done)
- [x] 2.2.5 Écrire les tests de sécurisation des endpoints (done)

### US2.3: En tant qu'administrateur, je veux pouvoir enrichir les données des objets via un script

- [x] 2.3.1 Créer le script d'enrichissement de données (done)
- [x] 2.3.2 Implémenter la validation des données enrichies (done)
- [x] 2.3.3 Ajouter des logs pour le suivi d'enrichissement (done)
- [x] 2.3.4 Écrire les tests du script d'enrichissement (done)

## Epic 3: Tâches de maintenance 📋

### US3.1: En tant qu'utilisateur, je veux voir ma todo-list de maintenance

- [ ] 3.1.1 Créer le modèle Task dans la DB (in progress)
- [ ] 3.1.2 Développer l'interface de la todo-list (todo)
- [ ] 3.1.3 Implémenter les endpoints de gestion des tâches (in progress)
- [ ] 3.1.4 Ajouter le filtrage et le tri des tâches (todo)
- [ ] 3.1.5 Écrire les tests des endpoints tâches (todo)

### US3.2: En tant que système, je veux générer automatiquement les tâches de maintenance

- [ ] 3.2.1 Créer le service de génération des tâches (todo)
- [ ] 3.2.2 Implémenter la logique de périodicité (todo)
- [ ] 3.2.3 Ajouter les notifications de nouvelles tâches (todo)
- [ ] 3.2.4 Écrire les tests du service de génération (todo)

## Epic 4: Gestion des problèmes 🔧

### US4.1: En tant qu'administrateur, je veux pouvoir définir les problèmes possibles par objet

- [ ] 4.1.1 Créer le modèle Problem dans la DB (todo)
- [ ] 4.1.2 Développer l'interface de gestion des problèmes (todo)
- [ ] 4.1.3 Implémenter les endpoints CRUD des problèmes (todo)
- [ ] 4.1.4 Ajouter la liaison problèmes-objets (todo)
- [ ] 4.1.5 Écrire les tests des endpoints problèmes (todo)

### US4.2: En tant qu'utilisateur, je veux pouvoir consulter et résoudre les problèmes

- [ ] 4.2.1 Créer l'interface de consultation des problèmes (todo)
- [ ] 4.2.2 Implémenter le suivi de résolution (todo)
- [ ] 4.2.3 Ajouter le partage d'expérience (todo)
- [ ] 4.2.4 Écrire les tests de résolution de problèmes (todo)

## Epic 5: Amélioration visuelle 🎨

### US5.1: En tant qu'utilisateur, je veux une interface responsive et moderne

- [ ] 5.1.1 Implémenter un design system cohérent (todo)
- [ ] 5.1.2 Créer des composants réutilisables (todo)
- [ ] 5.1.3 Ajouter des animations fluides (todo)
- [ ] 5.1.4 Optimiser pour mobile (todo)

### US5.2: En tant qu'utilisateur, je veux une expérience utilisateur intuitive

- [ ] 5.2.1 Ajouter des tooltips d'aide (todo)
- [ ] 5.2.2 Implémenter des messages de feedback (todo)
- [ ] 5.2.3 Créer des écrans de chargement (todo)
- [ ] 5.2.4 Optimiser les performances (todo)

## Notes techniques importantes 🔒

### Sécurité

- Implémenter la validation des tokens JWT pour chaque endpoint
- Ajouter des middlewares de vérification des permissions
- Valider toutes les entrées utilisateur
- Mettre en place le rate limiting
- Utiliser HTTPS en production
- Gérer correctement les sessions
- Implémenter la rotation des tokens

### Tests

#### Backend

- Tests unitaires pour chaque service
- Tests d'intégration pour les endpoints
- Tests de sécurité
- Tests de performance
- Tests de validation des données

#### Frontend

- Tests unitaires des composants
- Tests d'intégration
- Tests e2e avec Cypress
- Tests de performance
- Tests d'accessibilité
