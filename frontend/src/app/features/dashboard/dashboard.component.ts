import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { ObjectItem, MaintenanceTask } from '../../core/models/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <h2>📊 Dashboard</h2>
      
      <div class="stats">
        <div class="card">
          <h3>📦 Mes Objets</h3>
          <p class="number">{{ objects.length }}</p>
        </div>
        <div class="card">
          <h3>✅ Tâches en attente</h3>
          <p class="number">{{ pendingTasks.length }}</p>
        </div>
        <div class="card">
          <h3>🎯 Tâches terminées</h3>
          <p class="number">{{ completedTasks.length }}</p>
        </div>
      </div>

      <div class="recent-tasks card">
        <h3>📋 Tâches Récentes</h3>
        <div *ngIf="tasks.length === 0">
          <p>Aucune tâche pour le moment.</p>
        </div>
        <ul *ngIf="tasks.length > 0">
          <li *ngFor="let task of tasks.slice(0, 5)">
            <span [class]="'status-' + task.status">{{ task.status }}</span>
            Tâche #{{ task.id }}
          </li>
        </ul>
      </div>
    </div>
  `,
  styles: [`
    .dashboard {
      padding: 20px;
    }
    
    h2 {
      margin-bottom: 30px;
    }
    
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    
    .number {
      font-size: 3rem;
      font-weight: bold;
      color: #007bff;
      margin: 10px 0;
    }
    
    .recent-tasks ul {
      list-style: none;
    }
    
    .recent-tasks li {
      padding: 10px;
      border-bottom: 1px solid #eee;
    }
    
    .status-pending { color: orange; }
    .status-completed { color: green; }
    .status-issue_reported { color: red; }
  `]
})
export class DashboardComponent implements OnInit {
  objects: ObjectItem[] = [];
  tasks: MaintenanceTask[] = [];
  pendingTasks: MaintenanceTask[] = [];
  completedTasks: MaintenanceTask[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.apiService.getObjects().subscribe(data => {
      this.objects = data;
    });

    this.apiService.getMaintenanceTasks().subscribe(data => {
      this.tasks = data;
      this.pendingTasks = data.filter(t => t.status === 'pending');
      this.completedTasks = data.filter(t => t.status === 'completed');
    });
  }
}
