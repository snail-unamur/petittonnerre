# Structure Frontend - Petit Tonnerre

## 📁 Arborescence

```
frontend/
├── 📦 Configuration
│   ├── package.json              → Dépendances npm
│   ├── angular.json              → Config Angular
│   ├── tsconfig.json             → Config TypeScript
│   └── tsconfig.app.json         → Config TS application
│
├── 📄 src/
│   ├── index.html                → Page HTML principale
│   ├── main.ts                   → Bootstrap Angular
│   ├── styles.scss               → Styles globaux
│   │
│   ├── 🌍 environments/
│   │   ├── environment.ts        → Dev (API: localhost:8000)
│   │   └── environment.prod.ts   → Production
│   │
│   └── 🎨 app/
│       ├── app.component.ts      → Shell + Navigation
│       ├── app.routes.ts         → Routing (lazy loading)
│       │
│       ├── 🔧 core/
│       │   ├── models/
│       │   │   └── models.ts     → Interfaces TypeScript
│       │   │       • User
│       │   │       • ObjectItem
│       │   │       • MaintenanceAdvice
│       │   │       • MaintenanceTask
│       │   │       • Contribution
│       │   │
│       │   └── services/
│       │       └── api.service.ts → Service HTTP
│       │           • getUsers()
│       │           • getObjects()
│       │           • getMaintenanceTasks()
│       │           • getContributions()
│       │           • updateMaintenanceTask()
│       │           • upvoteContribution()
│       │
│       ├── 📱 features/
│       │   ├── dashboard/
│       │   │   └── dashboard.component.ts
│       │   │       • Stats des objets
│       │   │       • Tâches en attente
│       │   │       • Tâches terminées
│       │   │
│       │   ├── objects/
│       │   │   └── objects.component.ts
│       │   │       • Liste des objets
│       │   │       • Grid responsive
│       │   │       • Badges catégories
│       │   │
│       │   ├── maintenance/
│       │   │   └── maintenance.component.ts
│       │   │       • Liste des tâches
│       │   │       • Conseils d'entretien
│       │   │       • Marquage terminé
│       │   │
│       │   └── community/
│       │       └── community.component.ts
│       │           • Feed contributions
│       │           • Système de votes
│       │           • Badges statut
│       │
│       └── 🔄 shared/
           └── components/         → (Futurs composants réutilisables)
```

## 🎯 Composants Créés

### 1. AppComponent (Shell)
```typescript
Navigation principale avec 4 sections :
• Dashboard
• Mes Objets
• Maintenance
• Communauté
```

### 2. DashboardComponent
```typescript
Vue d'ensemble :
• Nombre d'objets
• Tâches en attente
• Tâches terminées
• Liste des tâches récentes
```

### 3. ObjectsComponent
```typescript
Gestion des objets :
• Grid responsive
• 6 catégories (heating, appliance, kitchen, bathroom, flooring, other)
• Badges de catégorie avec emojis
• Affichage marque/modèle/notes
```

### 4. MaintenanceComponent
```typescript
Maintenance :
• Liste des tâches avec statuts
• Conseils d'entretien
• Bouton "Marquer comme terminé"
• Fréquence d'entretien
```

### 5. CommunityComponent
```typescript
Communauté :
• Feed des contributions
• Système de votes (upvote)
• Badges de statut (pending, approved, rejected)
• Filtrage par catégorie
```

## 🔌 Service API

Le `ApiService` centralise tous les appels HTTP vers le backend :

```typescript
// Configuration
apiUrl = 'http://localhost:8000'

// Méthodes disponibles
getUsers(): Observable<User[]>
createUser(user): Observable<User>
getObjects(userId?): Observable<ObjectItem[]>
createObject(obj, userId): Observable<ObjectItem>
updateObject(id, obj): Observable<ObjectItem>
deleteObject(id): Observable<any>
getMaintenanceAdvice(): Observable<MaintenanceAdvice[]>
getMaintenanceTasks(userId?): Observable<MaintenanceTask[]>
updateMaintenanceTask(id, task): Observable<MaintenanceTask>
getContributions(): Observable<Contribution[]>
createContribution(contrib, authorId): Observable<Contribution>
upvoteContribution(id): Observable<any>
```

## 🎨 Design

### Styles Globaux (styles.scss)
- Reset CSS
- Police système
- Background gris clair
- Cards avec ombres
- Boutons bleus
- Inputs stylisés

### Composants Standalone
Tous les composants utilisent l'approche standalone d'Angular 17+ :
```typescript
@Component({
  selector: 'app-xxx',
  standalone: true,
  imports: [CommonModule],
  template: `...`,
  styles: [`...`]
})
```

### Lazy Loading
Routes chargées dynamiquement pour optimiser les performances :
```typescript
loadComponent: () => import('./features/xxx/xxx.component')
  .then(m => m.XxxComponent)
```

## 📊 Interfaces TypeScript

```typescript
User {
  id, email, username, location, created_at
}

ObjectItem {
  id, name, category, brand, model, 
  purchase_date, manual_url, notes, 
  owner_id, created_at
}

MaintenanceAdvice {
  id, title, description, frequency_days,
  category, is_validated, created_at
}

MaintenanceTask {
  id, scheduled_date, completed_date, status,
  notes, was_successful, issues_encountered,
  object_id, user_id, advice_id
}

Contribution {
  id, title, content, category, status,
  upvotes, author_id, created_at
}
```

## 🚀 Pour Démarrer

```bash
# Installer
npm install

# Lancer
npm start

# Accéder
http://localhost:4200
```

## ✨ Fonctionnalités Implémentées

✅ Navigation principale responsive
✅ Dashboard avec statistiques
✅ Liste des objets avec badges
✅ Gestion des tâches de maintenance
✅ Feed communautaire avec votes
✅ Service HTTP centralisé
✅ Interfaces TypeScript complètes
✅ Lazy loading des routes
✅ Styles CSS cohérents

## 🔄 Prochaines Améliorations

- [ ] Formulaires de création/édition
- [ ] Authentification & Guards
- [ ] Pagination & filtres
- [ ] Loading states
- [ ] Error handling
- [ ] Tests unitaires
- [ ] Design UI/UX avancé
- [ ] Notifications temps réel
