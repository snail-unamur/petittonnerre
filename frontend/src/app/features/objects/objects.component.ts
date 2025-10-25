import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { ObjectItem } from '../../core/models/models';

@Component({
  selector: 'app-objects',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container">
      <div class="page-header">
        <div>
          <h1>📦 Mes Objets</h1>
          <p class="page-subtitle">Gérez tous vos équipements et objets à entretenir</p>
        </div>
        <button class="btn btn-primary" (click)="showAddForm = !showAddForm">
          <span>➕</span>
          Ajouter un objet
        </button>
      </div>

      <!-- Objects Grid -->
      <div class="grid grid-3" *ngIf="objects.length > 0">
        <div class="card" *ngFor="let obj of objects">
          <div class="flex flex-between items-start mb-md">
            <span class="badge badge-primary">{{ getCategoryIcon(obj.category) }} {{ getCategoryLabel(obj.category) }}</span>
            <button class="btn btn-sm btn-ghost">⋯</button>
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
              <span class="font-medium">{{ formatDate(obj.purchase_date) }}</span>
            </div>
          </div>
          
          <p *ngIf="obj.notes" class="text-sm text-secondary mt-md p-sm rounded-md" style="background: var(--bg-tertiary);">
            💬 {{ obj.notes }}
          </p>
          
          <div class="card-footer mt-lg">
            <button class="btn btn-sm btn-outline">📝 Modifier</button>
            <button class="btn btn-sm btn-secondary">🔧 Maintenance</button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state" *ngIf="objects.length === 0">
        <div class="empty-icon">📦</div>
        <h3 class="empty-title">Aucun objet enregistré</h3>
        <p class="empty-description">
          Commencez par ajouter vos équipements et objets à entretenir pour suivre leur maintenance facilement.
        </p>
        <button class="btn btn-primary" (click)="showAddForm = true">
          ➕ Ajouter mon premier objet
        </button>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-4 mt-xl" *ngIf="objects.length > 0">
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🏠</div>
            <div class="text-sm text-tertiary">Électroménager</div>
            <div class="text-xl font-bold">{{ countByCategory('appliance') }}</div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🚗</div>
            <div class="text-sm text-tertiary">Véhicules</div>
            <div class="text-xl font-bold">{{ countByCategory('vehicle') }}</div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">💻</div>
            <div class="text-sm text-tertiary">Électronique</div>
            <div class="text-xl font-bold">{{ countByCategory('electronics') }}</div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🔧</div>
            <div class="text-sm text-tertiary">Autres</div>
            <div class="text-xl font-bold">{{ countByCategory('other') }}</div>
          </div>
        </div>
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
      
      .page-header button {
        width: 100%;
      }
    }
  `]
})
export class ObjectsComponent implements OnInit {
  objects: ObjectItem[] = [];
  showAddForm = false;
  loading = false;
  error = '';
  
  // Pour le moment, userId est hardcodé à 1 (en attendant l'authentification)
  currentUserId = 1;

  // Formulaire
  formData: Partial<ObjectItem> = {
    name: '',
    category: '',
    brand: '',
    model: '',
    notes: ''
  };

  editingObject: ObjectItem | null = null;
  objectToDelete: ObjectItem | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadObjects();
  }

  loadObjects() {
    this.loading = true;
    this.error = '';
    
    this.apiService.getUserObjects(this.currentUserId).subscribe({
      next: (data) => {
        this.objects = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur lors du chargement des objets:', err);
        this.error = 'Impossible de charger les objets. Veuillez réessayer.';
        this.loading = false;
      }
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
      brand: obj.brand || '',
      model: obj.model || '',
      notes: obj.notes || ''
    };
    this.showAddForm = true;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  cancelEdit() {
    this.showAddForm = false;
    this.editingObject = null;
    this.formData = {
      name: '',
      category: '',
      brand: '',
      model: '',
      notes: ''
    };
  }

  saveObject() {
    if (!this.formData.name || !this.formData.category) {
      return;
    }

    this.loading = true;
    this.error = '';

    if (this.editingObject) {
      this.apiService.updateUserObject(this.currentUserId, this.editingObject.id!, this.formData).subscribe({
        next: (updated) => {
          const index = this.objects.findIndex(o => o.id === updated.id);
          if (index !== -1) {
            this.objects[index] = updated;
          }
          this.cancelEdit();
          this.loading = false;
        },
        error: (err) => {
          console.error('Erreur lors de la mise à jour:', err);
          this.error = 'Impossible de mettre à jour l\'objet.';
          this.loading = false;
        }
      });
    } else {
      this.apiService.addUserObject(this.currentUserId, this.formData).subscribe({
        next: (created) => {
          this.objects.push(created);
          this.cancelEdit();
          this.loading = false;
        },
        error: (err) => {
          console.error('Erreur lors de la création:', err);
          this.error = 'Impossible de créer l\'objet.';
          this.loading = false;
        }
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
    this.error = '';

    this.apiService.deleteUserObject(this.currentUserId, this.objectToDelete.id!).subscribe({
      next: () => {
        this.objects = this.objects.filter(o => o.id !== this.objectToDelete!.id);
        this.cancelDelete();
        this.loading = false;
      },
      error: (err) => {
        console.error('Erreur lors de la suppression:', err);
        this.error = 'Impossible de supprimer l\'objet.';
        this.cancelDelete();
        this.loading = false;
      }
    });
  }

  getCategoryLabel(category: string): string {
    const labels: Record<string, string> = {
      'heating': 'Chauffage',
      'appliance': 'Électroménager',
      'kitchen': 'Cuisine',
      'bathroom': 'Salle de bain',
      'flooring': 'Revêtement sol',
      'other': 'Autre'
    };
    return labels[category] || category;
  }
  
  getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
      'heating': '🔥',
      'appliance': '🏠',
      'kitchen': '🍳',
      'bathroom': '�',
      'flooring': '🪨',
      'other': '📦'
    };
    return icons[category] || '📦';
  }
  
  formatDate(date: Date | string | undefined): string {
    if (!date) return 'N/A';
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleDateString('fr-FR');
  }
  
  countByCategory(category: string): number {
    return this.objects.filter(obj => obj.category === category).length;
  }
}

