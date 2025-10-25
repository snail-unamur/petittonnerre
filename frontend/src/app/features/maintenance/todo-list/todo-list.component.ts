import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaintenanceService } from '../../../core/services/maintenance.service';
import { MaintenanceTask } from '../../../core/models/models';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-todo-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container">
      <div class="todo-list">
        <div class="todo-item" *ngFor="let task of tasks">
          <div class="todo-status" [class]="'status-' + task.status">
            {{ getStatusIcon(task.status) }}
          </div>
          <div class="todo-content">
            <div class="todo-header">
              <span class="todo-title">{{ task.object?.name || 'Tâche #' + task.id }}</span>
              <span class="todo-date">{{ formatDate(task.scheduled_date) }}</span>
            </div>
            <p class="todo-notes" *ngIf="task.notes">{{ task.notes }}</p>
            <div class="todo-actions" *ngIf="task.status === 'pending'">
              <button class="btn-action" (click)="startTask(task)">Démarrer</button>
              <button class="btn-success" (click)="completeTask(task)">Terminer</button>
              <button class="btn-warning" (click)="skipTask(task)">Ignorer</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .todo-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .todo-item {
      display: flex;
      gap: 1rem;
      padding: 1rem;
      background-color: var(--color-bg-secondary);
      border-radius: var(--radius-md);
    }

    .todo-status {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 2.5rem;
      height: 2.5rem;
      border-radius: 50%;
      font-size: 1.2rem;
    }

    .status-pending {
      background-color: var(--color-warning-light);
      color: var(--color-warning);
    }

    .status-completed {
      background-color: var(--color-success-light);
      color: var(--color-success);
    }

    .status-skipped {
      background-color: var(--color-info-light);
      color: var(--color-info);
    }

    .status-issue_reported {
      background-color: var(--color-error-light);
      color: var(--color-error);
    }

    .todo-content {
      flex: 1;
    }

    .todo-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }

    .todo-title {
      font-weight: 500;
    }

    .todo-date {
      font-size: 0.9rem;
      color: var(--color-text-tertiary);
    }

    .todo-notes {
      font-size: 0.9rem;
      color: var(--color-text-secondary);
      margin: 0.5rem 0;
    }

    .todo-actions {
      display: flex;
      gap: 0.5rem;
      margin-top: 1rem;
    }

    .btn-action {
      padding: 0.5rem 1rem;
      border-radius: var(--radius-sm);
      border: none;
      cursor: pointer;
      font-size: 0.9rem;
      background-color: var(--color-primary);
      color: white;
    }

    .btn-success {
      background-color: var(--color-success);
    }

    .btn-warning {
      background-color: var(--color-warning);
    }
  `]
})
export class TodoListComponent implements OnInit {
  tasks: MaintenanceTask[] = [];
  currentUserId: number | null = null;

  constructor(
    private readonly maintenanceService: MaintenanceService,
    private readonly authService: AuthService
  ) {}

  ngOnInit() {
    // Récupérer l'ID de l'utilisateur connecté
    this.currentUserId = this.authService.getCurrentUserId();
    if (this.currentUserId) {
      this.loadTasks();
    }
  }

  loadTasks() {
    if (this.currentUserId) {
      this.maintenanceService.getTasks({
        user_id: this.currentUserId,
        status: 'pending'
      }).subscribe((tasks: MaintenanceTask[]) => {
        this.tasks = tasks;
      });
    }
  }

  startTask(task: MaintenanceTask) {
    const update: Partial<MaintenanceTask> = {
      status: 'pending',
      notes: task.notes ? task.notes + '\nTâche démarrée.' : 'Tâche démarrée.'
    };
    this.updateTask(task.id, update);
  }

  completeTask(task: MaintenanceTask) {
    const update: Partial<MaintenanceTask> = {
      status: 'completed',
      completed_date: new Date(),
      notes: task.notes ? task.notes + '\nTâche terminée.' : 'Tâche terminée.'
    };
    this.updateTask(task.id, update);
  }

  skipTask(task: MaintenanceTask) {
    const update: Partial<MaintenanceTask> = {
      status: 'skipped',
      notes: task.notes ? task.notes + '\nTâche ignorée.' : 'Tâche ignorée.'
    };
    this.updateTask(task.id, update);
  }

  private updateTask(taskId: number, update: Partial<MaintenanceTask>) {
    this.maintenanceService.updateTask(taskId, update).subscribe(
      (updatedTask: MaintenanceTask) => {
        this.tasks = this.tasks.map(t => 
          t.id === updatedTask.id ? updatedTask : t
        );
      }
    );
  }

  getStatusIcon(status: string): string {
    const icons: Record<string, string> = {
      'pending': '⏳',
      'completed': '✅',
      'skipped': '⏭️',
      'issue_reported': '⚠️',
      'in_progress': '🔄'
    };
    return icons[status] || '📝';
  }

  formatDate(date: Date | string): string {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleDateString('fr-FR');
  }
}