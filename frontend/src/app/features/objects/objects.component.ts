import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ApiService } from "../../core/services/api.service";
import { ObjectItem } from "../../core/models/models";

@Component({
  selector: "app-objects",
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container">
      <div class="page-header">
        <div>
          <h1>📦 Mes Objets</h1>
          <p class="page-subtitle">
            Gérez tous vos équipements et objets à entretenir
          </p>
        </div>
        <button class="btn btn-primary" (click)="toggleAddForm()">
          <span>{{ showAddForm ? '✖️' : '➕' }}</span>
          {{ showAddForm ? 'Annuler' : 'Ajouter un objet' }}
        </button>
      </div>

      <!-- Add/Edit Form -->
      <div class="card mb-xl" *ngIf="showAddForm">
        <h3 class="mb-md">{{ editingObject ? '✏️ Modifier' : '➕ Nouvel objet' }}</h3>
        <form (ngSubmit)="saveObject()" class="form">
          <div class="form-grid">
            <div class="form-group">
              <label for="name" class="required">Nom de l'objet</label>
              <input
                type="text"
                id="name"
                [(ngModel)]="formData.name"
                name="name"
                class="form-control"
                placeholder="Ex: Chaudière Vaillant"
                required
              />
            </div>

            <div class="form-group">
              <label for="category" class="required">Catégorie</label>
              <select
                id="category"
                [(ngModel)]="formData.category"
                name="category"
                class="form-control"
                required
              >
                <option [value]="undefined">Sélectionner une catégorie</option>
                <option value="heating">🔥 Chauffage</option>
                <option value="appliance">🏠 Électroménager</option>
                <option value="kitchen">🍳 Cuisine</option>
                <option value="bathroom">🚿 Salle de bain</option>
                <option value="flooring">🪨 Revêtement sol</option>
                <option value="other">📦 Autre</option>
              </select>
            </div>

            <div class="form-group">
              <label for="brand">Marque</label>
              <input
                type="text"
                id="brand"
                [(ngModel)]="formData.brand"
                name="brand"
                class="form-control"
                placeholder="Ex: Vaillant"
              />
            </div>

            <div class="form-group">
              <label for="model">Modèle</label>
              <input
                type="text"
                id="model"
                [(ngModel)]="formData.model"
                name="model"
                class="form-control"
                placeholder="Ex: ecoTEC plus"
              />
            </div>

            <div class="form-group full-width">
              <label for="notes">Notes</label>
              <textarea
                id="notes"
                [(ngModel)]="formData.notes"
                name="notes"
                class="form-control"
                rows="3"
                placeholder="Ajoutez des informations complémentaires..."
              ></textarea>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" (click)="cancelEdit()">
              Annuler
            </button>
            <button type="submit" class="btn btn-primary" [disabled]="!formData.name || !formData.category">
              {{ editingObject ? '💾 Enregistrer' : '➕ Ajouter' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Loading -->
      <div class="text-center py-xl" *ngIf="loading">
        <div class="spinner"></div>
        <p class="text-secondary mt-md">Chargement...</p>
      </div>

      <!-- Error Message -->
      <div class="alert alert-error mb-lg" *ngIf="error">
        ⚠️ {{ error }}
      </div>

      <!-- Objects Grid -->
      <div class="grid grid-3" *ngIf="!loading && objects.length > 0">
        <div class="card" *ngFor="let obj of objects">
          <div class="flex flex-between items-start mb-md">
            <span class="badge badge-primary"
              >{{ getCategoryIcon(obj.category) }}
              {{ getCategoryLabel(obj.category) }}</span
            >
            <div class="flex gap-xs">
              <button class="btn btn-sm btn-ghost" (click)="editObject(obj)" title="Modifier">
                ✏️
              </button>
              <button class="btn btn-sm btn-ghost text-error" (click)="confirmDelete(obj)" title="Supprimer">
                🗑️
              </button>
            </div>
          </div>

          <h3 class="mb-sm">{{ obj.name }}</h3>

          <div class="divider"></div>

          <div class="flex flex-column gap-xs text-sm">
            <div *ngIf="obj.brand" class="flex gap-sm items-center">
              <span class="text-tertiary">🏷️ Marque:</span>
              <span class="font-medium">{{ obj.brand }}</span>
            </div>
            <div *ngIf="obj.model" class="flex gap-sm items-center">
              <span class="text-tertiary">📋 Modèle:</span>
              <span class="font-medium">{{ obj.model }}</span>
            </div>
            <div *ngIf="obj.purchase_date" class="flex gap-sm items-center">
              <span class="text-tertiary">📅 Achat:</span>
              <span class="font-medium">{{
                formatDate(obj.purchase_date)
              }}</span>
            </div>
          </div>

          <p
            *ngIf="obj.notes"
            class="text-sm text-secondary mt-md p-sm rounded-md"
            style="background: var(--bg-tertiary);"
          >
            💬 {{ obj.notes }}
          </p>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state" *ngIf="!loading && objects.length === 0 && !showAddForm">
        <div class="empty-icon">📦</div>
        <h3 class="empty-title">Aucun objet enregistré</h3>
        <p class="empty-description">
          Commencez par ajouter vos équipements et objets à entretenir pour
          suivre leur maintenance facilement.
        </p>
        <button class="btn btn-primary" (click)="toggleAddForm()">
          ➕ Ajouter mon premier objet
        </button>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-4 mt-xl" *ngIf="!loading && objects.length > 0">
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🔥</div>
            <div class="text-sm text-tertiary">Chauffage</div>
            <div class="text-xl font-bold">
              {{ countByCategory("heating") }}
            </div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🏠</div>
            <div class="text-sm text-tertiary">Électroménager</div>
            <div class="text-xl font-bold">
              {{ countByCategory("appliance") }}
            </div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🍳</div>
            <div class="text-sm text-tertiary">Cuisine</div>
            <div class="text-xl font-bold">
              {{ countByCategory("kitchen") }}
            </div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">�</div>
            <div class="text-sm text-tertiary">Autres</div>
            <div class="text-xl font-bold">{{ countByCategory("other") }}</div>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div class="modal" *ngIf="objectToDelete" (click)="cancelDelete()">
        <div class="modal-content" (click)="$event.stopPropagation()">
          <h3 class="mb-md">🗑️ Confirmer la suppression</h3>
          <p class="mb-lg">
            Êtes-vous sûr de vouloir supprimer <strong>{{ objectToDelete.name }}</strong> ?
            Cette action est irréversible.
          </p>
          <div class="flex gap-md justify-end">
            <button class="btn btn-secondary" (click)="cancelDelete()">
              Annuler
            </button>
            <button class="btn btn-error" (click)="deleteObject()">
              🗑️ Supprimer
            </button>
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

      .page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-xl);
      }

      .form-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: var(--spacing-md);
      }

      .form-group.full-width {
        grid-column: 1 / -1;
      }

      .form-actions {
        display: flex;
        gap: var(--spacing-md);
        justify-content: flex-end;
        margin-top: var(--spacing-lg);
        padding-top: var(--spacing-lg);
        border-top: 1px solid var(--border-color);
      }

      .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--border-color);
        border-top-color: var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto;
      }

      @keyframes spin {
        to { transform: rotate(360deg); }
      }

      .modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: var(--spacing-lg);
      }

      .modal-content {
        background: var(--bg-primary);
        padding: var(--spacing-xl);
        border-radius: var(--border-radius-lg);
        max-width: 500px;
        width: 100%;
        box-shadow: var(--shadow-lg);
      }

      .text-error {
        color: var(--error-color);
      }

      .btn-error {
        background: var(--error-color);
        color: white;
      }

      .btn-error:hover {
        opacity: 0.9;
      }

      @media (max-width: 767px) {
        .page-header {
          flex-direction: column;
          align-items: stretch;
        }

        .page-header button {
          width: 100%;
        }

        .form-grid {
          grid-template-columns: 1fr;
        }
      }
    `,
  ],
})
export class ObjectsComponent implements OnInit {
  objects: ObjectItem[] = [];
  showAddForm = false;
  loading = false;
  error = "";

  // Pour le moment, userId est hardcodé à 1 (en attendant l'authentification)
  currentUserId = 1;

  // Formulaire
  formData: Partial<ObjectItem> = {
    name: "",
    category: undefined,
    brand: "",
    model: "",
    notes: "",
  };

  editingObject: ObjectItem | null = null;
  objectToDelete: ObjectItem | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadObjects();
  }

  loadObjects() {
    this.loading = true;
    this.error = "";

    this.apiService.getUserObjects(this.currentUserId).subscribe({
      next: (data) => {
        this.objects = data;
        this.loading = false;
      },
      error: (err) => {
        console.error("Erreur lors du chargement des objets:", err);
        this.error = "Impossible de charger les objets. Veuillez réessayer.";
        this.loading = false;
      },
    });
  }

  toggleAddForm() {
    this.showAddForm = !this.showAddForm;
    if (!this.showAddForm) {
      this.cancelEdit();
    }
  }

  editObject(obj: ObjectItem) {
    this.editingObject = obj;
    this.formData = {
      name: obj.name,
      category: obj.category,
      brand: obj.brand || "",
      model: obj.model || "",
      notes: obj.notes || "",
    };
    this.showAddForm = true;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  cancelEdit() {
    this.showAddForm = false;
    this.editingObject = null;
    this.formData = {
      name: "",
      category: undefined,
      brand: "",
      model: "",
      notes: "",
    };
  }

  saveObject() {
    if (!this.formData.name || !this.formData.category) {
      return;
    }

    this.loading = true;
    this.error = "";

    if (this.editingObject) {
      this.apiService
        .updateUserObject(
          this.currentUserId,
          this.editingObject.id!,
          this.formData
        )
        .subscribe({
          next: (updated) => {
            const index = this.objects.findIndex((o) => o.id === updated.id);
            if (index !== -1) {
              this.objects[index] = updated;
            }
            this.cancelEdit();
            this.loading = false;
          },
          error: (err) => {
            console.error("Erreur lors de la mise à jour:", err);
            this.error = "Impossible de mettre à jour l'objet.";
            this.loading = false;
          },
        });
    } else {
      this.apiService
        .addUserObject(this.currentUserId, this.formData)
        .subscribe({
          next: (created) => {
            this.objects.push(created);
            this.cancelEdit();
            this.loading = false;
          },
          error: (err) => {
            console.error("Erreur lors de la création:", err);
            this.error = "Impossible de créer l'objet.";
            this.loading = false;
          },
        });
    }
  }

  confirmDelete(obj: ObjectItem) {
    this.objectToDelete = obj;
  }

  cancelDelete() {
    this.objectToDelete = null;
  }

  deleteObject() {
    if (!this.objectToDelete) return;

    this.loading = true;
    this.error = "";

    this.apiService
      .deleteUserObject(this.currentUserId, this.objectToDelete.id!)
      .subscribe({
        next: () => {
          this.objects = this.objects.filter(
            (o) => o.id !== this.objectToDelete!.id
          );
          this.cancelDelete();
          this.loading = false;
        },
        error: (err) => {
          console.error("Erreur lors de la suppression:", err);
          this.error = "Impossible de supprimer l'objet.";
          this.cancelDelete();
          this.loading = false;
        },
      });
  }

  getCategoryLabel(category: string): string {
    const labels: Record<string, string> = {
      heating: "Chauffage",
      appliance: "Électroménager",
      kitchen: "Cuisine",
      bathroom: "Salle de bain",
      flooring: "Revêtement sol",
      other: "Autre",
    };
    return labels[category] || category;
  }

  getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
      heating: "🔥",
      appliance: "🏠",
      kitchen: "🍳",
      bathroom: "�",
      flooring: "🪨",
      other: "📦",
    };
    return icons[category] || "📦";
  }

  formatDate(date: Date | string | undefined): string {
    if (!date) return "N/A";
    const dateObj = typeof date === "string" ? new Date(date) : date;
    return dateObj.toLocaleDateString("fr-FR");
  }

  countByCategory(category: string): number {
    return this.objects.filter((obj) => obj.category === category).length;
  }
}
