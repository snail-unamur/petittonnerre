import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { Contribution } from '../../core/models/models';

@Component({
  selector: 'app-community',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="community">
      <div class="header">
        <h2>👥 Communauté</h2>
        <button>+ Partager une astuce</button>
      </div>

      <div class="contributions-list">
        <div class="card contribution" *ngFor="let contrib of contributions">
          <div class="contribution-header">
            <h3>{{ contrib.title }}</h3>
            <span class="category-badge">{{ contrib.category }}</span>
          </div>
          <p>{{ contrib.content }}</p>
          <div class="contribution-footer">
            <button (click)="upvote(contrib)" class="upvote-btn">
              👍 {{ contrib.upvotes }}
            </button>
            <span class="status" [class]="'status-' + contrib.status">
              {{ getStatusLabel(contrib.status) }}
            </span>
          </div>
        </div>

        <div class="card empty" *ngIf="contributions.length === 0">
          <p>Aucune contribution pour le moment. Soyez le premier à partager !</p>
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
    
    .contributions-list {
      display: grid;
      gap: 20px;
    }
    
    .contribution-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }
    
    .contribution-header h3 {
      margin: 0;
    }
    
    .category-badge {
      padding: 4px 12px;
      background: #6c757d;
      color: white;
      border-radius: 12px;
      font-size: 0.85rem;
    }
    
    .contribution-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 15px;
      padding-top: 15px;
      border-top: 1px solid #eee;
    }
    
    .upvote-btn {
      background: #f8f9fa;
      color: #333;
      border: 1px solid #ddd;
    }
    
    .upvote-btn:hover {
      background: #e9ecef;
    }
    
    .status-pending { color: #856404; }
    .status-approved { color: #155724; }
    .status-rejected { color: #721c24; }
    
    .empty {
      text-align: center;
      color: #999;
    }
  `]
})
export class CommunityComponent implements OnInit {
  contributions: Contribution[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadContributions();
  }

  loadContributions() {
    this.apiService.getContributions().subscribe(data => {
      this.contributions = data;
    });
  }

  upvote(contribution: Contribution) {
    this.apiService.upvoteContribution(contribution.id).subscribe(() => {
      contribution.upvotes++;
    });
  }

  getStatusLabel(status: string): string {
    const labels: any = {
      pending: 'En attente',
      approved: 'Approuvé',
      rejected: 'Rejeté'
    };
    return labels[status] || status;
  }
}
