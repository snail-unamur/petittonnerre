# Frontend - Petit Tonnerre

Application Angular pour la gestion d'entretien domestique.

## Installation

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm start
```

L'application sera accessible à : http://localhost:4200

## Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── models/
│   │   │   │   └── models.ts           # Interfaces TypeScript
│   │   │   └── services/
│   │   │       └── api.service.ts      # Service API HTTP
│   │   ├── features/
│   │   │   ├── dashboard/              # Dashboard principal
│   │   │   ├── objects/                # Gestion des objets
│   │   │   ├── maintenance/            # Tâches de maintenance
│   │   │   └── community/              # Contributions communautaires
│   │   ├── shared/
│   │   │   └── components/             # Composants réutilisables
│   │   ├── app.component.ts            # Composant principal
│   │   └── app.routes.ts               # Configuration routing
│   ├── environments/
│   │   ├── environment.ts              # Config développement
│   │   └── environment.prod.ts         # Config production
│   ├── index.html
│   ├── main.ts
│   └── styles.scss
├── angular.json
├── package.json
└── tsconfig.json
```

## Composants

### Dashboard
- Vue d'ensemble des objets
- Statistiques des tâches
- Tâches récentes

### Objets
- Liste des objets domestiques
- Filtrage par catégorie
- Cartes détaillées

### Maintenance
- Liste des tâches
- Conseils d'entretien
- Marquage des tâches terminées

### Communauté
- Feed des contributions
- Système de votes
- Partage d'astuces

## Configuration API

L'URL de l'API backend est définie dans `src/environments/environment.ts` :

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

## Prochaines Étapes

- [ ] Ajouter formulaires de création/édition
- [ ] Implémenter l'authentification
- [ ] Ajouter la pagination
- [ ] Améliorer le design
- [ ] Tests unitaires
