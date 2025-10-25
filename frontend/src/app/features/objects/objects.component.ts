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

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadObjects();
  }

  loadObjects() {
    this.apiService.getObjects().subscribe(data => {
      this.objects = data;
    });
  }

  getCategoryLabel(category: string): string {
    const labels: Record<string, string> = {
      'appliance': 'Électroménager',
      'vehicle': 'Véhicule',
      'electronics': 'Électronique',
      'furniture': 'Mobilier',
      'other': 'Autre'
    };
    return labels[category] || category;
  }
  
  getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
      'appliance': '🏠',
      'vehicle': '🚗',
      'electronics': '💻',
      'furniture': '�',
      'other': '�'
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

