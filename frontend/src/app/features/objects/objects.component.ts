import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { ObjectItem } from '../../core/models/models';

@Component({
  selector: 'app-objects',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="objects">
      <div class="header">
        <h2>📦 Mes Objets</h2>
        <button (click)="showAddForm = !showAddForm">+ Ajouter un objet</button>
      </div>

      <div class="objects-grid">
        <div class="card" *ngFor="let obj of objects">
          <div class="category-badge">{{ getCategoryLabel(obj.category) }}</div>
          <h3>{{ obj.name }}</h3>
          <p *ngIf="obj.brand"><strong>Marque:</strong> {{ obj.brand }}</p>
          <p *ngIf="obj.model"><strong>Modèle:</strong> {{ obj.model }}</p>
          <p *ngIf="obj.notes" class="notes">{{ obj.notes }}</p>
        </div>

        <div class="card empty" *ngIf="objects.length === 0">
          <p>Aucun objet enregistré. Ajoutez votre premier objet !</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
    }
    
    .objects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    
    .category-badge {
      display: inline-block;
      padding: 4px 12px;
      background: #007bff;
      color: white;
      border-radius: 12px;
      font-size: 0.85rem;
      margin-bottom: 10px;
    }
    
    .notes {
      color: #666;
      font-size: 0.9rem;
      margin-top: 10px;
    }
    
    .empty {
      text-align: center;
      color: #999;
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
    const labels: any = {
      heating: '🔥 Chauffage',
      appliance: '⚡ Électroménager',
      kitchen: '🍳 Cuisine',
      bathroom: '🚿 Salle de bain',
      flooring: '🪨 Sol',
      other: '📦 Autre'
    };
    return labels[category] || category;
  }
}
