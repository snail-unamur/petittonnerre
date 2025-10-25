# Plan de Développement - Petit Tonnerre (Phase 2)

## Epic 1: Authentification et Droits d'Accès 🔐

### US1.1: En tant qu'utilisateur connecté, je ne peux pas accéder aux pages login/register
**Dépendances:** Aucune  
**Priorité:** Haute
**Statut:** ✅ Done

- [x] 1.1.1 Créer un guard pour rediriger les utilisateurs connectés depuis login/register
- [x] 1.1.2 Modifier les routes pour appliquer le guard
- [x] 1.1.3 Rediriger vers le dashboard après connexion réussie
- [x] 1.1.4 Tester le comportement de redirection

### US1.2: En tant qu'utilisateur non connecté, je ne vois que login/register dans le menu
**Dépendances:** Aucune  
**Priorité:** Haute

- [ ] 1.2.1 Modifier le composant de navigation pour vérifier l'état de connexion
- [ ] 1.2.2 Cacher les éléments de menu pour utilisateurs non connectés
- [ ] 1.2.3 Afficher uniquement Login et Register si non connecté
- [ ] 1.2.4 Tester l'affichage du menu selon l'état de connexion

### US1.3: En tant qu'administrateur connecté, je vois un lien "Admin" dans le menu
**Dépendances:** US1.2  
**Priorité:** Haute

- [ ] 1.3.1 Ajouter la vérification du rôle admin dans AuthService
- [ ] 1.3.2 Afficher le lien Admin dans le menu si role === admin
- [ ] 1.3.3 Créer/améliorer le guard admin pour protéger les routes
- [ ] 1.3.4 Tester l'accès admin selon les rôles

## Epic 2: Gestion des Objets Partagés 📦

### US2.1: En tant qu'utilisateur, je peux lier un objet existant à mon compte
**Dépendances:** Aucune  
**Priorité:** Haute  
**Statut:** ✅ Done

- [x] 2.1.1 Modifier le modèle Object pour supporter plusieurs propriétaires (many-to-many)
- [x] 2.1.2 Créer une table d'association user_objects dans la DB
- [x] 2.1.3 Mettre à jour les endpoints API pour gérer les associations
- [x] 2.1.4 Créer un endpoint pour rechercher les objets existants
- [x] 2.1.5 Écrire les migrations de base de données
- [x] 2.1.6 Tester les associations multiples

### US2.2: En tant qu'utilisateur, je vois d'abord les objets existants avant de créer
**Dépendances:** US2.1  
**Priorité:** Haute

- [ ] 2.2.1 Créer un composant de recherche d'objets existants
- [ ] 2.2.2 Implémenter la recherche par nom/catégorie/marque/modèle
- [ ] 2.2.3 Afficher les résultats avec possibilité de sélection
- [ ] 2.2.4 Ajouter un bouton "Créer un nouvel objet" si aucun résultat
- [ ] 2.2.5 Lier l'objet sélectionné au compte utilisateur
- [ ] 2.2.6 Tester le workflow complet

### US2.3: En tant qu'utilisateur, ma création d'objet nécessite une approbation admin
**Dépendances:** US2.2  
**Priorité:** Haute

- [ ] 2.3.1 Modifier l'endpoint de création d'objet pour créer un ObjectRequest
- [ ] 2.3.2 Définir le status par défaut à "pending"
- [ ] 2.3.3 Afficher un message de confirmation à l'utilisateur
- [ ] 2.3.4 Mettre à jour l'interface admin pour gérer ces demandes
- [ ] 2.3.5 Notifier l'utilisateur lors de l'approbation (future US notifications)
- [ ] 2.3.6 Tester le workflow d'approbation

### US2.4: En tant qu'utilisateur, je ne vois que mes objets dans ma liste
**Dépendances:** US2.1  
**Priorité:** Haute

- [ ] 2.4.1 Modifier l'endpoint GET /objects pour filtrer par user_id
- [ ] 2.4.2 Utiliser la table d'association pour récupérer les objets de l'utilisateur
- [ ] 2.4.3 Mettre à jour le frontend pour passer le user_id
- [ ] 2.4.4 Tester que chaque utilisateur voit uniquement ses objets

### US2.5: En tant qu'utilisateur, je peux rechercher dans tous mes objets
**Dépendances:** US2.4  
**Priorité:** Moyenne

- [ ] 2.5.1 Ajouter une barre de recherche en haut de la page "Mes objets"
- [ ] 2.5.2 Implémenter la recherche côté frontend (filtre en temps réel)
- [ ] 2.5.3 Rechercher dans nom, marque, modèle, catégorie
- [ ] 2.5.4 Ajouter un indicateur de résultats trouvés
- [ ] 2.5.5 Tester la recherche avec divers critères

### US2.6: En tant qu'utilisateur, mes objets sont triés par catégorie avec lazy loading
**Dépendances:** US2.4  
**Priorité:** Moyenne

- [ ] 2.6.1 Organiser l'affichage des objets par catégorie (accordéons)
- [ ] 2.6.2 Implémenter le lazy loading (30 objets par page)
- [ ] 2.6.3 Ajouter un endpoint API avec pagination
- [ ] 2.6.4 Créer un composant de chargement (spinner)
- [ ] 2.6.5 Détecter le scroll pour charger plus d'objets
- [ ] 2.6.6 Tester le lazy loading avec de nombreux objets

## Epic 3: Gestion des Problèmes Partagés 🔧

### US3.1: En tant qu'utilisateur, je vois les problèmes des autres pour mes objets
**Dépendances:** US2.4  
**Priorité:** Haute

- [ ] 3.1.1 Modifier l'endpoint GET /problems pour inclure les problèmes des objets partagés
- [ ] 3.1.2 Filtrer les problèmes par objets de l'utilisateur
- [ ] 3.1.3 Ajouter une indication visuelle "Problème d'un autre utilisateur"
- [ ] 3.1.4 Tester l'affichage des problèmes partagés

### US3.2: En tant qu'utilisateur, je peux répondre aux problèmes des autres
**Dépendances:** US3.1  
**Priorité:** Haute

- [ ] 3.2.1 Vérifier les droits d'accès (objet partagé) avant de permettre la réponse
- [ ] 3.2.2 Permettre la création de résolutions pour problèmes partagés
- [ ] 3.2.3 Afficher l'auteur de chaque résolution
- [ ] 3.2.4 Tester la création de résolutions sur problèmes partagés

### US3.3: En tant qu'utilisateur, je vois "Mes problèmes" et "Problèmes des autres" séparément
**Dépendances:** US3.1  
**Priorité:** Moyenne

- [ ] 3.3.1 Créer deux onglets dans la page Problèmes
- [ ] 3.3.2 Filtrer "Mes problèmes" = problèmes créés par l'utilisateur
- [ ] 3.3.3 Filtrer "Problèmes des autres" = problèmes sur objets partagés non créés par l'utilisateur
- [ ] 3.3.4 Ajouter des compteurs sur les onglets
- [ ] 3.3.5 Tester l'affichage et le filtrage des onglets

### US3.4: En tant qu'utilisateur, je peux chatter sur la page d'un problème
**Dépendances:** US3.1  
**Priorité:** Moyenne

- [ ] 3.4.1 Créer le modèle ProblemChat dans la DB
- [ ] 3.4.2 Implémenter les endpoints CRUD pour les messages de chat
- [ ] 3.4.3 Vérifier les droits d'accès (utilisateurs avec l'objet)
- [ ] 3.4.4 Créer le composant de chat dans la page problème
- [ ] 3.4.5 Afficher les messages en temps réel (polling ou websocket simple)
- [ ] 3.4.6 Ajouter l'indication de l'auteur et timestamp
- [ ] 3.4.7 Tester l'envoi et réception de messages

## Epic 4: Dashboard et Actions Rapides 📊

### US4.1: En tant qu'utilisateur, je vois des boutons d'actions rapides sur le dashboard
**Dépendances:** Aucune  
**Priorité:** Haute
**Statut:** ✅ Done

- [x] 4.1.1 Créer des cards avec actions rapides (Nouvelle maintenance, Nouveau problème, etc.)
- [x] 4.1.2 Afficher les statistiques (nombre d'objets, maintenances à venir, problèmes en cours)
- [x] 4.1.3 Ajouter des raccourcis vers les pages principales
- [x] 4.1.4 Implémenter les actions directement depuis le dashboard
- [x] 4.1.5 Tester toutes les actions rapides

### US4.2: En tant qu'utilisateur, quand je change de page, la page scroll en haut
**Dépendances:** Aucune  
**Priorité:** Basse

- [ ] 4.2.1 Créer un service ou utiliser un router event listener
- [ ] 4.2.2 Scroll vers le haut lors de la navigation
- [ ] 4.2.3 Tester sur toutes les pages

## Epic 5: Export et Dark Mode 🌙

### US5.1: En tant qu'utilisateur, je peux exporter mes maintenances en iCal
**Dépendances:** Aucune  
**Priorité:** Moyenne

- [x] 5.1.1 Créer un endpoint pour générer un fichier .ics
- [x] 5.1.2 Formater les maintenances au format iCalendar
- [x] 5.1.3 Ajouter un bouton "Exporter" sur la page maintenance
- [x] 5.1.4 Télécharger le fichier .ics côté frontend
- [ ] 5.1.5 Tester l'import dans différents calendriers (Google, Outlook, etc.)

### US5.2: En tant qu'utilisateur, je peux activer le mode sombre
**Dépendances:** Aucune  
**Priorité:** Basse
**Statut:** ✅ Done

- [x] 5.2.1 Créer un thème dark dans les styles SCSS
- [x] 5.2.2 Ajouter un toggle dark/light mode dans le header
- [x] 5.2.3 Sauvegarder la préférence dans localStorage
- [x] 5.2.4 Appliquer le thème au chargement de l'application
- [x] 5.2.5 Adapter tous les composants au dark mode
- [x] 5.2.6 Tester le switch entre les modes

## Epic 6: Administration Avancée 👨‍💼

### US6.1: En tant qu'admin, je peux supprimer des problèmes (soft delete)
**Dépendances:** US1.3  
**Priorité:** Moyenne

- [ ] 6.1.1 Ajouter un champ deleted_at dans le modèle Problem
- [ ] 6.1.2 Créer l'endpoint admin DELETE /admin/problems/{id}
- [ ] 6.1.3 Implémenter le soft delete (mettre deleted_at = now())
- [ ] 6.1.4 Exclure les problèmes supprimés des requêtes normales
- [ ] 6.1.5 Ajouter une interface admin pour voir/restaurer les problèmes supprimés
- [ ] 6.1.6 Tester le soft delete et la restauration

### US6.2: En tant qu'admin, je peux supprimer des commentaires (soft delete)
**Dépendances:** US6.1  
**Priorité:** Moyenne

- [ ] 6.2.1 Ajouter un champ deleted_at dans le modèle ProblemResolution
- [ ] 6.2.2 Créer l'endpoint admin DELETE /admin/resolutions/{id}
- [ ] 6.2.3 Implémenter le soft delete pour les résolutions
- [ ] 6.2.4 Afficher [supprimé] pour les commentaires soft deleted
- [ ] 6.2.5 Tester le soft delete des commentaires

### US6.3: En tant qu'admin, je peux supprimer des messages de chat (soft delete)
**Dépendances:** US3.4, US6.1  
**Priorité:** Basse

- [ ] 6.3.1 Ajouter un champ deleted_at dans le modèle ProblemChat
- [ ] 6.3.2 Créer l'endpoint admin DELETE /admin/chats/{id}
- [ ] 6.3.3 Implémenter le soft delete pour les chats
- [ ] 6.3.4 Afficher [message supprimé] dans le chat
- [ ] 6.3.5 Tester le soft delete des messages

### US6.4: En tant qu'admin, j'ai un dashboard de modération complet
**Dépendances:** US6.1, US6.2, US6.3  
**Priorité:** Basse

- [ ] 6.4.1 Créer une page dashboard admin avec statistiques
- [ ] 6.4.2 Afficher les contenus récents nécessitant modération
- [ ] 6.4.3 Actions rapides de modération (approuver/rejeter/supprimer)
- [ ] 6.4.4 Logs d'activité admin
- [ ] 6.4.5 Tester toutes les fonctionnalités de modération

## Epic 7: Système de Notifications 🔔

### US7.1: En tant qu'utilisateur, je reçois une notif pour un nouveau problème sur mes objets
**Dépendances:** US3.1  
**Priorité:** Moyenne

- [ ] 7.1.1 Créer le modèle Notification dans la DB
- [ ] 7.1.2 Implémenter la création de notification lors d'un nouveau problème
- [ ] 7.1.3 Créer l'endpoint GET /notifications pour récupérer les notifications
- [ ] 7.1.4 Créer un composant de notification dans le header
- [ ] 7.1.5 Afficher un badge avec le nombre de notifications non lues
- [ ] 7.1.6 Marquer les notifications comme lues
- [ ] 7.1.7 Tester la création et affichage des notifications

### US7.2: En tant qu'utilisateur, je reçois une notif pour une réponse à mon problème
**Dépendances:** US7.1  
**Priorité:** Moyenne

- [ ] 7.2.1 Créer une notification lors d'une nouvelle résolution
- [ ] 7.2.2 Vérifier que la notification va au créateur du problème
- [ ] 7.2.3 Inclure un lien vers le problème dans la notification
- [ ] 7.2.4 Tester les notifications de réponse

### US7.3: En tant qu'utilisateur, je reçois une notif pour un nouveau message chat
**Dépendances:** US3.4, US7.1  
**Priorité:** Basse

- [ ] 7.3.1 Créer une notification lors d'un nouveau message de chat
- [ ] 7.3.2 Notifier tous les utilisateurs ayant accès au problème
- [ ] 7.3.3 Éviter de notifier l'auteur du message
- [ ] 7.3.4 Tester les notifications de chat

### US7.4: En tant qu'utilisateur, je reçois une notif quand mon objet est approuvé
**Dépendances:** US2.3, US7.1  
**Priorité:** Moyenne

- [ ] 7.4.1 Créer une notification lors de l'approbation d'un ObjectRequest
- [ ] 7.4.2 Inclure le nom de l'objet approuvé
- [ ] 7.4.3 Ajouter un lien vers la page des objets
- [ ] 7.4.4 Tester les notifications d'approbation

## Epic 8: Navigation et UX 🎯

### US8.1: Supprimer l'onglet Communauté du menu
**Dépendances:** Aucune  
**Priorité:** Haute

- [ ] 8.1.1 Retirer le lien Communauté du composant de navigation
- [ ] 8.1.2 Supprimer ou désactiver la route /community
- [ ] 8.1.3 Supprimer le composant CommunityComponent si non utilisé
- [ ] 8.1.4 Tester que le menu ne contient plus Communauté

## Epic 9: IoT et Raspberry Pi 🤖

### US9.1: En tant qu'utilisateur, je reçois une notif quand je passe devant un capteur
**Dépendances:** US7.1  
**Priorité:** Basse

- [ ] 9.1.1 Configurer Raspberry Pi avec capteur de mouvement
- [ ] 9.1.2 Créer un endpoint API pour recevoir les événements du capteur
- [ ] 9.1.3 Associer une pièce à un capteur
- [ ] 9.1.4 Récupérer les maintenances liées aux objets de cette pièce
- [ ] 9.1.5 Envoyer une notification avec les maintenances à faire
- [ ] 9.1.6 Tester le déclenchement par mouvement

### US9.2: En tant qu'utilisateur, je vois les maintenances de la pièce sur l'écran Raspberry
**Dépendances:** US9.1  
**Priorité:** Basse

- [ ] 9.2.1 Configurer l'écran de la Raspberry Pi
- [ ] 9.2.2 Créer une page web dédiée pour l'affichage pièce
- [ ] 9.2.3 Afficher les maintenances à faire dans cette pièce
- [ ] 9.2.4 Rafraîchir automatiquement l'affichage
- [ ] 9.2.5 Design adapté pour écran petit format
- [ ] 9.2.6 Tester l'affichage sur la Raspberry

### US9.3: En tant qu'utilisateur, je peux encoder une maintenance via pavé tactile
**Dépendances:** US9.2  
**Priorité:** Basse

- [ ] 9.3.1 Configurer le pavé tactile sur la Raspberry Pi
- [ ] 9.3.2 Créer une interface de saisie de numéro d'objet
- [ ] 9.3.3 Associer chaque objet à un code unique
- [ ] 9.3.4 Créer un endpoint pour marquer une maintenance comme complétée
- [ ] 9.3.5 Afficher une confirmation visuelle sur l'écran
- [ ] 9.3.6 Tester l'encodage via pavé tactile

### US9.4: En tant qu'admin, je peux configurer les associations pièce-capteur
**Dépendances:** US9.1  
**Priorité:** Basse

- [ ] 9.4.1 Créer le modèle Room et RaspberryDevice dans la DB
- [ ] 9.4.2 Créer une interface admin pour gérer les pièces
- [ ] 9.4.3 Associer des objets à des pièces
- [ ] 9.4.4 Enregistrer les Raspberry Pi dans le système
- [ ] 9.4.5 Lier une Raspberry à une pièce
- [ ] 9.4.6 Tester la configuration complète

---

## Ordre de Développement Recommandé

### Phase 1: Authentification et Droits (Epic 1)
1. US1.2 → US1.1 → US1.3

### Phase 2: Objets Partagés (Epic 2)
2. US2.1 → US2.2 → US2.3 → US2.4 → US2.5 → US2.6

### Phase 3: Problèmes Partagés (Epic 3)
3. US3.1 → US3.2 → US3.3 → US3.4

### Phase 4: Dashboard et Navigation (Epic 4, 8)
4. US8.1 → US4.1 → US4.2

### Phase 5: Notifications (Epic 7)
5. US7.1 → US7.4 → US7.2 → US7.3

### Phase 6: Administration (Epic 6)
6. US6.1 → US6.2 → US6.3 → US6.4

### Phase 7: Export et Dark Mode (Epic 5)
7. US5.1 → US5.2

### Phase 8: IoT (Epic 9) - Optionnel
8. US9.1 → US9.2 → US9.3 → US9.4

---

## Notes Techniques

### Modifications de Base de Données Majeures
- Table `user_objects` (many-to-many) pour US2.1
- Champs `deleted_at` pour soft delete (US6.x)
- Table `notifications` pour US7.x
- Tables `rooms` et `raspberry_devices` pour US9.x
- Table `problem_chats` pour US3.4

### Dépendances Externes Potentielles
- Bibliothèque iCalendar pour US5.1
- WebSocket ou polling pour chat temps réel (US3.4)
- Raspberry Pi SDK/GPIO pour US9.x

### Tests Prioritaires
- Tests d'intégration pour les objets partagés (Epic 2)
- Tests de permissions pour les problèmes partagés (Epic 3)
- Tests de notifications (Epic 7)
- Tests de soft delete (Epic 6)
