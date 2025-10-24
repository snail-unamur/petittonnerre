import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { MaintenanceTask, MaintenanceAdvice } from '../../core/models/models';

@Component({
  selector: 'app-maintenance',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="maintenance">
      <h2>🔧 Maintenance</h2>

      <div class="section">
        <h3>📋 Mes Tâches</h3>
        <div class="tasks-list">
          <div class="card task-card" *ngFor="let task of tasks">
            <div class="task-header">
              <span class="task-status" [class]="'status-' + task.status">
                {{ getStatusLabel(task.status) }}
              </span>
              <span class="task-date">{{ task.scheduled_date | date:'shortDate' }}</span>
            </div>
            <p *ngIf="task.notes">{{ task.notes }}</p>
            <button *ngIf="task.status === 'pending'" (click)="completeTask(task)">
              ✅ Marquer comme terminé
            </button>
          </div>

          <div class="card empty" *ngIf="tasks.length === 0">
            <p>Aucune tâche de maintenance planifiée.</p>
          </div>
        </div>
      </div>

      <div class="section">
        <h3>💡 Conseils d'Entretien</h3>
        <div class="advice-list">
          <div class="card" *ngFor="let advice of adviceList">
            <h4>{{ advice.title }}</h4>
            <p>{{ advice.description }}</p>
            <small *ngIf="advice.frequency_days">
              Fréquence : tous les {{ advice.frequency_days }} jours
            </small>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .section {
      margin-bottom: 40px;
    }
    
    .tasks-list, .advice-list {
      display: grid;
      gap: 15px;
    }
    
    .task-card {
      border-left: 4px solid #007bff;
    }
    
    .task-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 10px;
    }
    
    .task-status {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.85rem;
      font-weight: bold;
    }
    
    .status-pending {
      background: #fff3cd;
      color: #856404;
    }
    
    .status-completed {
      background: #d4edda;
      color: #155724;
    }
    
    .status-issue_reported {
      background: #f8d7da;
      color: #721c24;
    }
    
    .empty {
      text-align: center;
      color: #999;
    }
  `]
})
export class MaintenanceComponent implements OnInit {
  tasks: MaintenanceTask[] = [];
  adviceList: MaintenanceAdvice[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.apiService.getMaintenanceTasks().subscribe(data => {
      this.tasks = data;
    });

    this.apiService.getMaintenanceAdvice().subscribe(data => {
      this.adviceList = data;
    });
  }

  getStatusLabel(status: string): string {
    const labels: any = {
      pending: 'En attente',
      completed: 'Terminé',
      skipped: 'Ignoré',
      issue_reported: 'Problème signalé'
    };
    return labels[status] || status;
  }

  completeTask(task: MaintenanceTask) {
    this.apiService.updateMaintenanceTask(task.id, {
      status: 'completed',
      completed_date: new Date()
    }).subscribe(() => {
      this.loadData();
    });
  }
}
