import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ApiService } from "../../core/services/api.service";
import { MaintenanceTask, ObjectItem, MaintenanceAdvice } from "../../core/models/models";
import { ObjectTreeSelectComponent } from "../../shared/components/object-tree-select/object-tree-select.component";
import { DateTimePickerComponent } from "../../shared/components/date-time-picker/date-time-picker.component";

@Component({
  selector: "app-maintenance",
  standalone: true,
  imports: [CommonModule, FormsModule, ObjectTreeSelectComponent, DateTimePickerComponent],
  template: `
    <div class="container">
      <div class="page-header">
        <div>
          <h1>🔧 Maintenance</h1>
          <p class="page-subtitle">
            Planifiez et suivez l'entretien de vos équipements
          </p>
        </div>
        <div class="flex gap-sm">
          <button class="btn btn-ghost" (click)="exportToIcal()" title="Exporter au format iCalendar">
            📅 Exporter
          </button>
          <button class="btn btn-primary" (click)="openCreateForm()">➕ Nouvelle tâche</button>
        </div>
      </div>

      <!-- Filters -->
      <div class="card card-flat mb-xl">
        <div class="flex gap-sm flex-wrap">
          <button
            class="btn btn-sm"
            [class.btn-primary]="activeFilter === 'all'"
            [class.btn-ghost]="activeFilter !== 'all'"
            (click)="activeFilter = 'all'"
          >
            Toutes ({{ tasks.length }})
          </button>
          <button
            class="btn btn-sm"
            [class.btn-primary]="activeFilter === 'pending'"
            [class.btn-ghost]="activeFilter !== 'pending'"
            (click)="activeFilter = 'pending'"
          >
            ⏳ En attente ({{ countByStatus("pending") }})
          </button>
          <button
            class="btn btn-sm"
            [class.btn-primary]="activeFilter === 'completed'"
            [class.btn-ghost]="activeFilter !== 'completed'"
            (click)="activeFilter = 'completed'"
          >
            ✅ Terminées ({{ countByStatus("completed") }})
          </button>
          <button
            class="btn btn-sm"
            [class.btn-primary]="activeFilter === 'issue_reported'"
            [class.btn-ghost]="activeFilter !== 'issue_reported'"
            (click)="activeFilter = 'issue_reported'"
          >
            ⚠️ Problèmes ({{ countByStatus("issue_reported") }})
          </button>
        </div>
      </div>

      <!-- Formulaire de création de tâche -->
      <div class="card mb-xl" *ngIf="showCreateForm">
        <div class="flex flex-between items-center mb-md">
          <h3>➕ Nouvelle tâche de maintenance</h3>
          <button class="btn btn-sm btn-ghost" (click)="closeCreateForm()">✕</button>
        </div>

        <form (ngSubmit)="createTask()" class="flex flex-column gap-md">
          <!-- Nom de la tâche -->
          <div>
            <label class="form-label">Nom de la tâche *</label>
            <input
              type="text"
              class="form-control"
              [(ngModel)]="newTask.name"
              name="taskName"
              placeholder="Ex: Vérifier le filtre de la VMC"
              required
            />
          </div>

          <!-- Sélection de l'objet -->
          <div>
            <label class="form-label">Objet concerné *</label>
            <app-object-tree-select
              [objects]="objects"
              [(ngModel)]="newTask.object_id"
              name="objectId"
              placeholder="Sélectionnez un objet"
            ></app-object-tree-select>
          </div>

          <!-- Date planifiée -->
          <div>
            <label class="form-label">Date planifiée *</label>
            <app-date-time-picker
              [(ngModel)]="newTask.scheduled_date"
              name="scheduledDate"
              placeholder="Sélectionnez une date et heure"
            ></app-date-time-picker>
          </div>

          <!-- Notes (optionnel) -->
          <div>
            <label class="form-label">Notes (optionnel)</label>
            <textarea
              class="form-control"
              [(ngModel)]="newTask.notes"
              name="notes"
              rows="3"
              placeholder="Ajoutez des détails sur cette tâche..."
            ></textarea>
          </div>

          <!-- Boutons -->
          <div class="flex gap-sm">
            <button type="submit" class="btn btn-primary">✅ Créer la tâche</button>
            <button type="button" class="btn btn-ghost" (click)="closeCreateForm()">
              ❌ Annuler
            </button>
          </div>
        </form>
      </div>

      <!-- Tasks List -->
      <div class="grid grid-2" *ngIf="filteredTasks.length > 0">
        <div class="card" *ngFor="let task of filteredTasks">
          <div class="flex flex-between items-start mb-md">
            <span
              class="badge"
              [ngClass]="'badge-' + getStatusBadgeType(task.status)"
            >
              {{ getStatusIcon(task.status) }} {{ getStatusLabel(task.status) }}
            </span>
            <button class="btn btn-sm btn-ghost">⋯</button>
          </div>

          <h3 class="mb-sm" *ngIf="!isEditing(task.id, 'name')" (click)="editField(task, 'name')" style="cursor: pointer;" title="Cliquer pour modifier">
            {{ task.name }}
          </h3>

          <!-- Edit mode for task name -->
          <div *ngIf="isEditing(task.id, 'name')" class="mb-md">
            <input
              type="text"
              class="form-control mb-sm"
              [(ngModel)]="editingName"
              placeholder="Nom de la tâche..."
              style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; font-weight: 600;"
            />
            <div class="flex gap-sm">
              <button class="btn btn-sm btn-primary" (click)="saveTaskName(task)">
                ✅ Enregistrer
              </button>
              <button class="btn btn-sm btn-ghost" (click)="cancelEdit()">
                ❌ Annuler
              </button>
            </div>
          </div>

          <div class="object-info text-sm text-secondary mb-sm">
            <span
              >🔧 {{ task.object?.name || "Objet #" + task.object_id }}</span
            >
          </div>

          <div class="flex flex-column gap-sm text-sm mb-md">
            <div class="flex gap-sm items-center" *ngIf="!isEditing(task.id, 'scheduled_date')" (click)="editField(task, 'scheduled_date')" style="cursor: pointer;" title="Cliquer pour modifier">
              <span class="text-tertiary">📅 Programmée:</span>
              <span class="font-medium">{{
                formatDate(task.scheduled_date)
              }}</span>
            </div>
            
            <!-- Edit mode for scheduled date -->
            <div *ngIf="isEditing(task.id, 'scheduled_date')" class="mb-sm">
              <input
                type="datetime-local"
                class="form-control"
                [(ngModel)]="editingScheduledDate"
                style="padding: 6px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"
              />
              <div class="flex gap-sm mt-sm">
                <button class="btn btn-sm btn-primary" (click)="saveTaskScheduledDate(task)">
                  ✅ Enregistrer
                </button>
                <button class="btn btn-sm btn-ghost" (click)="cancelEdit()">
                  ❌ Annuler
                </button>
              </div>
            </div>
            
            <div class="flex gap-sm items-center" *ngIf="task.completed_date">
              <span class="text-tertiary">✅ Complétée:</span>
              <span class="font-medium">{{
                formatDate(task.completed_date)
              }}</span>
            </div>
          </div>

          <p class="text-sm text-secondary" *ngIf="task.notes && !isEditing(task.id, 'notes')" (click)="editField(task, 'notes')" style="cursor: pointer;" title="Cliquer pour modifier">
            💬 {{ task.notes }}
          </p>
          
          <!-- Empty state for notes -->
          <p class="text-sm text-secondary" *ngIf="!task.notes && !isEditing(task.id, 'notes')" (click)="editField(task, 'notes')" style="cursor: pointer; font-style: italic; opacity: 0.6;" title="Cliquer pour ajouter des notes">
            💬 Ajouter des notes...
          </p>
          
          <!-- Edit mode for notes -->
          <div *ngIf="isEditing(task.id, 'notes')" class="mb-md">
            <textarea
              class="form-control mb-sm"
              [(ngModel)]="editingNotes"
              rows="3"
              placeholder="Ajouter des notes..."
              style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"
            ></textarea>
            <div class="flex gap-sm">
              <button class="btn btn-sm btn-primary" (click)="saveTaskNotes(task)">
                ✅ Enregistrer
              </button>
              <button class="btn btn-sm btn-ghost" (click)="cancelEdit()">
                ❌ Annuler
              </button>
            </div>
          </div>

          <div class="card-footer mt-lg" *ngIf="!isEditing(task.id)">
            <button
              class="btn btn-sm btn-success"
              *ngIf="task.status === 'pending'"
              (click)="completeTask(task)"
            >
              ✅ Terminer
            </button>
            <button
              class="btn btn-sm btn-warning"
              *ngIf="task.status === 'completed'"
              (click)="resetToPending(task)"
            >
              ⏳ Remettre en attente
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state" *ngIf="filteredTasks.length === 0">
        <div class="empty-icon">🔧</div>
        <h3 class="empty-title">
          Aucune tâche
          {{ activeFilter !== "all" ? "dans cette catégorie" : "" }}
        </h3>
        <p class="empty-description">
          {{
            activeFilter === "all"
              ? "Créez votre première tâche de maintenance pour commencer."
              : "Essayez de filtrer par une autre catégorie."
          }}
        </p>
        <button class="btn btn-primary" *ngIf="activeFilter === 'all'">
          ➕ Créer une tâche
        </button>
      </div>
    </div>
  `,
  styles: [
    `
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
    `,
  ],
})
export class MaintenanceComponent implements OnInit {
  tasks: MaintenanceTask[] = [];
  objects: ObjectItem[] = [];
  advices: MaintenanceAdvice[] = [];
  activeFilter: string = "all";
  editingTaskId: number | null = null;
  editingField: string | null = null;
  editingName: string = "";
  editingNotes: string = "";
  editingScheduledDate: string = "";
  
  // Formulaire de création
  showCreateForm: boolean = false;
  newTask = {
    name: "",
    object_id: 0,
    advice_id: 1, // Valeur par défaut, sera ajustable plus tard
    scheduled_date: "",
    notes: ""
  };

  constructor(private readonly apiService: ApiService) {}

  ngOnInit() {
    this.loadTasks();
    this.loadObjects();
  }

  loadTasks() {
    this.apiService.getMaintenanceTasks().subscribe((data) => {
      this.tasks = data;
    });
  }

  loadObjects() {
    this.apiService.getObjects().subscribe((data) => {
      this.objects = data;
    });
  }

  openCreateForm() {
    this.showCreateForm = true;
    // Initialiser la date à maintenant
    const now = new Date();
    this.newTask.scheduled_date = this.formatDateForInput(now);
  }

  closeCreateForm() {
    this.showCreateForm = false;
    // Réinitialiser le formulaire
    this.newTask = {
      name: "",
      object_id: 0,
      advice_id: 1,
      scheduled_date: "",
      notes: ""
    };
  }

  createTask() {
    // Validation basique
    if (!this.newTask.name.trim()) {
      alert("Le nom de la tâche est obligatoire");
      return;
    }
    if (!this.newTask.object_id || this.newTask.object_id === 0) {
      alert("Veuillez sélectionner un objet");
      return;
    }
    if (!this.newTask.scheduled_date) {
      alert("La date planifiée est obligatoire");
      return;
    }

    // Créer la tâche
    const taskToCreate: any = {
      name: this.newTask.name.trim(),
      object_id: this.newTask.object_id,
      advice_id: this.newTask.advice_id,
      scheduled_date: new Date(this.newTask.scheduled_date).toISOString(),
      notes: this.newTask.notes.trim() || undefined,
      status: "pending"
    };

    // Récupérer le user_id depuis le service d'auth (pour l'instant hardcodé)
    const userId = 1;

    this.apiService.createMaintenanceTask(taskToCreate, userId).subscribe({
      next: (createdTask: MaintenanceTask) => {
        this.tasks.push(createdTask);
        this.closeCreateForm();
      },
      error: (err: any) => {
        console.error("Erreur lors de la création de la tâche:", err);
        alert("Une erreur est survenue lors de la création de la tâche.");
      },
    });
  }

  startTask(task: MaintenanceTask) {
    const update: Partial<MaintenanceTask> = {
      status: "pending",
    };
    this.updateTask(task.id, update);
  }

  completeTask(task: MaintenanceTask) {
    const update: Partial<MaintenanceTask> = {
      status: "completed",
      completed_date: new Date(),
    };
    this.updateTask(task.id, update);
  }

  resetToPending(task: MaintenanceTask) {
    const update: any = {
      status: "pending",
      completed_date: null,
    };
    this.updateTask(task.id, update);
  }

  editTask(task: MaintenanceTask) {
    this.editingTaskId = task.id;
    this.editingField = 'name';
    this.editingName = task.name || "";
  }

  editField(task: MaintenanceTask, field: string) {
    this.editingTaskId = task.id;
    this.editingField = field;
    
    switch(field) {
      case 'name':
        this.editingName = task.name || "";
        break;
      case 'notes':
        this.editingNotes = task.notes || "";
        break;
      case 'scheduled_date': {
        // Convertir la date en format ISO pour l'input datetime-local
        const date = new Date(task.scheduled_date);
        this.editingScheduledDate = this.formatDateForInput(date);
        break;
      }
    }
  }

  saveTaskName(task: MaintenanceTask) {
    if (this.editingName.trim() && this.editingName.trim() !== task.name) {
      const update: any = { name: this.editingName.trim() };
      this.updateTask(task.id, update);
    }
    this.cancelEdit();
  }

  saveTaskNotes(task: MaintenanceTask) {
    if (this.editingNotes.trim() !== task.notes) {
      const update: any = { notes: this.editingNotes.trim() || null };
      this.updateTask(task.id, update);
    }
    this.cancelEdit();
  }

  saveTaskScheduledDate(task: MaintenanceTask) {
    if (this.editingScheduledDate) {
      const update: any = { scheduled_date: new Date(this.editingScheduledDate).toISOString() };
      this.updateTask(task.id, update);
    }
    this.cancelEdit();
  }

  cancelEdit() {
    this.editingTaskId = null;
    this.editingField = null;
    this.editingName = "";
    this.editingNotes = "";
    this.editingScheduledDate = "";
  }

  isEditing(taskId: number, field?: string): boolean {
    if (field) {
      return this.editingTaskId === taskId && this.editingField === field;
    }
    return this.editingTaskId === taskId;
  }

  formatDateForInput(date: Date): string {
    // Format: YYYY-MM-DDTHH:mm
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }

  private updateTask(taskId: number, update: Partial<MaintenanceTask>) {
    this.apiService.updateMaintenanceTask(taskId, update).subscribe({
      next: (updatedTask: MaintenanceTask) => {
        this.tasks = this.tasks.map((t) =>
          t.id === updatedTask.id ? updatedTask : t
        );
      },
      error: (err) => {
        console.error("Erreur lors de la mise à jour de la tâche:", err);
        alert("Une erreur est survenue lors de la mise à jour de la tâche.");
      },
    });
  }

  get filteredTasks(): MaintenanceTask[] {
    if (this.activeFilter === "all") {
      return this.tasks;
    }
    return this.tasks.filter((task) => task.status === this.activeFilter);
  }

  countByStatus(status: string): number {
    return this.tasks.filter((task) => task.status === status).length;
  }

  getStatusLabel(status: string): string {
    const labels: Record<string, string> = {
      pending: "En attente",
      completed: "Terminée",
      skipped: "Ignorée",
      issue_reported: "Problème signalé",
    };
    return labels[status] || status;
  }

  getStatusIcon(status: string): string {
    const icons: Record<string, string> = {
      pending: "⏳",
      completed: "✅",
      skipped: "⏭️",
      issue_reported: "⚠️",
    };
    return icons[status] || "📝";
  }

  getStatusBadgeType(status: string): string {
    const types: Record<string, string> = {
      pending: "warning",
      completed: "success",
      skipped: "info",
      issue_reported: "error",
    };
    return types[status] || "primary";
  }

  formatDate(date: Date | string): string {
    const dateObj = typeof date === "string" ? new Date(date) : date;
    return dateObj.toLocaleDateString("fr-FR");
  }

  exportToIcal() {
    // Récupérer le user_id depuis le service d'auth (pour l'instant hardcodé)
    const userId = 1;

    this.apiService.exportMaintenanceToIcal(userId).subscribe({
      next: (blob: Blob) => {
        // Créer un lien de téléchargement
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `maintenances-petit-tonnerre-${userId}.ics`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error("Erreur lors de l'export iCalendar:", err);
        alert("Une erreur est survenue lors de l'export. Assurez-vous d'avoir des maintenances à exporter.");
      },
    });
  }
}
