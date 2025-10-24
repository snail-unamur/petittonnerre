import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { 
    path: 'dashboard', 
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  { 
    path: 'objects', 
    loadComponent: () => import('./features/objects/objects.component').then(m => m.ObjectsComponent)
  },
  { 
    path: 'maintenance', 
    loadComponent: () => import('./features/maintenance/maintenance.component').then(m => m.MaintenanceComponent)
  },
  { 
    path: 'community', 
    loadComponent: () => import('./features/community/community.component').then(m => m.CommunityComponent)
  }
];
