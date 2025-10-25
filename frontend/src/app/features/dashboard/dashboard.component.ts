import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Router, RouterModule } from "@angular/router";
import { ApiService } from "../../core/services/api.service";
import { AuthService } from "../../core/services/auth.service";
import { ObjectItem, MaintenanceTask } from "../../core/models/models";

@Component({
  selector: "app-dashboard",
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="container">
      <div class="page-header">
        <h1>📊 Dashboard</h1>
        <p class="page-subtitle">Vue d'ensemble de vos objets et tâches de maintenance</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-3 mb-xl">
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-label">Mes Objets</div>
          <div class="stat-value">{{ stats?.total_objects || 0 }}</div>
          <div class="stat-change positive" *ngIf="(stats?.total_objects || 0) > 0">
            ↗ +{{ stats?.total_objects || 0 }} objets enregistrés
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-label">Tâches en attente</div>
          <div class="stat-value">{{ stats?.pending_tasks || 0 }}</div>
          <div class="stat-change" [class.positive]="(stats?.pending_tasks || 0) === 0" [class.negative]="(stats?.pending_tasks || 0) > 0">
            {{ (stats?.pending_tasks || 0) === 0 ? '✓ Tout est à jour' : '! Nécessite attention' }}
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🔧</div>
          <div class="stat-label">Problèmes ouverts</div>
          <div class="stat-value">{{ stats?.open_problems || 0 }}</div>
          <div class="stat-change" [class.positive]="(stats?.open_problems || 0) === 0" [class.negative]="(stats?.open_problems || 0) > 0">
            {{ (stats?.open_problems || 0) === 0 ? '✓ Aucun problème' : '! À résoudre' }}
          </div>
        </div>
      </div>

      <!-- Recent Tasks -->
      <div class="card">
        <div class="card-header">
          <h3>📋 Tâches Récentes</h3>
          <p class="card-subtitle">Activités de maintenance récentes</p>
        </div>
        
        <div class="card-body">
          <div class="empty-state" *ngIf="tasks.length === 0">
            <div class="empty-icon">📭</div>
            <h4 class="empty-title">Aucune tâche</h4>
            <p class="empty-description">
              Vous n'avez pas encore de tâches de maintenance. Commencez par ajouter des objets!
            </p>
            <button class="btn btn-primary">Ajouter un objet</button>
          </div>
          
          <div class="list" *ngIf="tasks.length > 0">
            <div class="list-item" *ngFor="let task of tasks.slice(0, 5)">
              <div class="list-item-icon">
                {{ getTaskIcon(task.status) }}
              </div>
              <div class="list-item-content">
                <div class="list-item-title">
                  Tâche #{{ task.id }}
                  <span class="badge" [ngClass]="'badge-' + getTaskBadgeType(task.status)">
                    {{ task.status }}
                  </span>
                </div>
                <div class="list-item-subtitle">
                  Maintenance programmée
                </div>
              </div>
              <button class="btn btn-sm btn-ghost">Voir détails</button>
            </div>
          </div>
        </div>
        
        <div class="card-footer" *ngIf="tasks.length > 5">
          <button class="btn btn-secondary">Voir toutes les tâches</button>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-2 mt-xl">
        <div class="card card-flat">
          <div class="card-body">
            <h4>🎯 Actions Rapides</h4>
            <div class="flex flex-column gap-sm mt-md">
              <button class="btn btn-outline w-full" (click)="goToObjects()">➕ Ajouter un objet</button>
              <button class="btn btn-outline w-full" (click)="goToMaintenance()">📝 Voir mes maintenances</button>
              <button class="btn btn-outline w-full" (click)="goToProblems()">🔧 Signaler un problème</button>
              <button class="btn btn-outline w-full" (click)="goToCommunity()">👥 Rejoindre la communauté</button>
            </div>
          </div>
        </div>
        
        <div class="card card-flat">
          <div class="card-body">
            <h4>💡 Astuce du jour</h4>
            <p class="mt-md">
              N'oubliez pas de programmer vos entretiens réguliers pour prolonger la durée de vie de vos équipements!
            </p>
            <div class="alert alert-info mt-md">
              <div class="alert-icon">ℹ️</div>
              <div class="alert-content">
                <div class="alert-title">Rappel</div>
                Vérifiez vos filtres tous les 3 mois
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        padding: var(--spacing-xl) 0;
      }
    `
  ]
})
export class DashboardComponent implements OnInit {
  objects: ObjectItem[] = [];
  tasks: MaintenanceTask[] = [];
  pendingTasks: MaintenanceTask[] = [];
  completedTasks: MaintenanceTask[] = [];
  stats: any = null;

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadData();
    this.loadStats();
  }

  loadData() {
    this.apiService.getObjects().subscribe((data) => {
      this.objects = data;
    });

    this.apiService.getMaintenanceTasks().subscribe((data) => {
      this.tasks = data;
      this.pendingTasks = data.filter((t) => t.status === "pending");
      this.completedTasks = data.filter((t) => t.status === "completed");
    });
  }

  loadStats() {
    const userId = this.authService.getUserId();
    if (userId) {
      this.apiService.getDashboardStats(userId).subscribe({
        next: (data) => {
          this.stats = data;
        },
        error: (err) => {
          console.error('Erreur lors du chargement des stats:', err);
        }
      });
    }
  }
  
  goToObjects() {
    this.router.navigate(['/objects']);
  }

  goToMaintenance() {
    this.router.navigate(['/maintenance']);
  }

  goToProblems() {
    this.router.navigate(['/problems']);
  }

  goToCommunity() {
    this.router.navigate(['/community']);
  }
  
  getTaskIcon(status: string): string {
    const icons: Record<string, string> = {
      'pending': '⏳',
      'completed': '✅',
      'issue_reported': '⚠️',
      'in_progress': '🔄'
    };
    return icons[status] || '📝';
  }
  
  getTaskBadgeType(status: string): string {
    const types: Record<string, string> = {
      'pending': 'warning',
      'completed': 'success',
      'issue_reported': 'error',
      'in_progress': 'info'
    };
    return types[status] || 'primary';
  }
}

