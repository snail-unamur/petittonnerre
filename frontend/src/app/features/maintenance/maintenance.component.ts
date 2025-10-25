import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { MaintenanceTask } from '../../core/models/models';

@Component({
  selector: 'app-maintenance',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container">
      <div class="page-header">
        <div>
          <h1>🔧 Maintenance</h1>
          <p class="page-subtitle">Planifiez et suivez l'entretien de vos équipements</p>
        </div>
        <button class="btn btn-primary">
          ➕ Nouvelle tâche
        </button>
      </div>

      <!-- Filters -->
      <div class="card card-flat mb-xl">
        <div class="flex gap-sm flex-wrap">
          <button class="btn btn-sm" [class.btn-primary]="activeFilter === 'all'" [class.btn-ghost]="activeFilter !== 'all'" (click)="activeFilter = 'all'">
            Toutes ({{ tasks.length }})
          </button>
          <button class="btn btn-sm" [class.btn-primary]="activeFilter === 'pending'" [class.btn-ghost]="activeFilter !== 'pending'" (click)="activeFilter = 'pending'">
            ⏳ En attente ({{ countByStatus('pending') }})
          </button>
          <button class="btn btn-sm" [class.btn-primary]="activeFilter === 'completed'" [class.btn-ghost]="activeFilter !== 'completed'" (click)="activeFilter = 'completed'">
            ✅ Terminées ({{ countByStatus('completed') }})
          </button>
          <button class="btn btn-sm" [class.btn-primary]="activeFilter === 'issue_reported'" [class.btn-ghost]="activeFilter !== 'issue_reported'" (click)="activeFilter = 'issue_reported'">
            ⚠️ Problèmes ({{ countByStatus('issue_reported') }})
          </button>
        </div>
      </div>

      <!-- Tasks List -->
      <div class="grid grid-2" *ngIf="filteredTasks.length > 0">
        <div class="card" *ngFor="let task of filteredTasks">
          <div class="flex flex-between items-start mb-md">
            <span class="badge" [ngClass]="'badge-' + getStatusBadgeType(task.status)">
              {{ getStatusIcon(task.status) }} {{ getStatusLabel(task.status) }}
            </span>
            <button class="btn btn-sm btn-ghost">⋯</button>
          </div>
          
          <h3 class="mb-sm">Tâche #{{ task.id }}</h3>
          
          <div class="flex flex-column gap-sm text-sm mb-md">
            <div class="flex gap-sm items-center">
              <span class="text-tertiary">📅 Programmée:</span>
              <span class="font-medium">{{ formatDate(task.scheduled_date) }}</span>
            </div>
            <div class="flex gap-sm items-center" *ngIf="task.completed_date">
              <span class="text-tertiary">✅ Complétée:</span>
              <span class="font-medium">{{ formatDate(task.completed_date) }}</span>
            </div>
          </div>
          
          <p class="text-sm text-secondary" *ngIf="task.notes">
            💬 {{ task.notes }}
          </p>
          
          <div class="card-footer mt-lg">
            <button class="btn btn-sm btn-outline" *ngIf="task.status === 'pending'">
              ▶️ Démarrer
            </button>
            <button class="btn btn-sm btn-success" *ngIf="task.status === 'pending'">
              ✅ Terminer
            </button>
            <button class="btn btn-sm btn-ghost">📝 Modifier</button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state" *ngIf="filteredTasks.length === 0">
        <div class="empty-icon">🔧</div>
        <h3 class="empty-title">Aucune tâche {{ activeFilter !== 'all' ? 'dans cette catégorie' : '' }}</h3>
        <p class="empty-description">
          {{ activeFilter === 'all' ? 'Créez votre première tâche de maintenance pour commencer.' : 'Essayez de filtrer par une autre catégorie.' }}
        </p>
        <button class="btn btn-primary" *ngIf="activeFilter === 'all'">
          ➕ Créer une tâche
        </button>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      padding: var(--spacing-xl) 0;
    }
    
    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: var(--spacing-md);
    }
    
    @media (max-width: 767px) {
      .page-header {
        flex-direction: column;
        align-items: stretch;
      }
    }
  `]
})
export class MaintenanceComponent implements OnInit {
  tasks: MaintenanceTask[] = [];
  activeFilter: string = 'all';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadTasks();
  }

  loadTasks() {
    this.apiService.getMaintenanceTasks().subscribe(data => {
      this.tasks = data;
    });
  }

  get filteredTasks(): MaintenanceTask[] {
    if (this.activeFilter === 'all') {
      return this.tasks;
    }
    return this.tasks.filter(task => task.status === this.activeFilter);
  }
  
  countByStatus(status: string): number {
    return this.tasks.filter(task => task.status === status).length;
  }
  
  getStatusLabel(status: string): string {
    const labels: Record<string, string> = {
      'pending': 'En attente',
      'completed': 'Terminée',
      'skipped': 'Ignorée',
      'issue_reported': 'Problème signalé'
    };
    return labels[status] || status;
  }
  
  getStatusIcon(status: string): string {
    const icons: Record<string, string> = {
      'pending': '⏳',
      'completed': '✅',
      'skipped': '⏭️',
      'issue_reported': '⚠️'
    };
    return icons[status] || '📝';
  }
  
  getStatusBadgeType(status: string): string {
    const types: Record<string, string> = {
      'pending': 'warning',
      'completed': 'success',
      'skipped': 'info',
      'issue_reported': 'error'
    };
    return types[status] || 'primary';
  }
  
  formatDate(date: Date | string): string {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleDateString('fr-FR');
  }
}
