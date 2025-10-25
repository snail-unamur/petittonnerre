import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';
import { ObjectRequest, ObjectRequestDecision } from '../../core/models/models';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrl: './admin-dashboard.component.scss'
})
export class AdminDashboardComponent implements OnInit {
  pendingRequests: ObjectRequest[] = [];
  selectedRequest: ObjectRequest | null = null;
  adminId = 3; // Temporaire - ID de l'admin en DB (admin@example.com)
  adminNotes = '';
  loading = false;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadPendingRequests();
  }

  loadPendingRequests() {
    this.loading = true;
    this.apiService.getPendingRequests(this.adminId).subscribe({
      next: (requests) => {
        this.pendingRequests = requests;
        this.loading = false;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des demandes:', error);
        this.loading = false;
      }
    });
  }

  selectRequest(request: ObjectRequest) {
    this.selectedRequest = request;
    this.adminNotes = '';
  }

  approveRequest() {
    if (!this.selectedRequest) return;

    const decision: ObjectRequestDecision = {
      status: 'approved',
      admin_notes: this.adminNotes
    };

    this.apiService.adminDecideRequest(this.selectedRequest.id, decision, this.adminId).subscribe({
      next: () => {
        this.loadPendingRequests();
        this.selectedRequest = null;
        this.adminNotes = '';
      },
      error: (error) => {
        console.error('Erreur lors de l\'approbation:', error);
      }
    });
  }

  rejectRequest() {
    if (!this.selectedRequest) return;

    const decision: ObjectRequestDecision = {
      status: 'rejected',
      admin_notes: this.adminNotes
    };

    this.apiService.adminDecideRequest(this.selectedRequest.id, decision, this.adminId).subscribe({
      next: () => {
        this.loadPendingRequests();
        this.selectedRequest = null;
        this.adminNotes = '';
      },
      error: (error) => {
        console.error('Erreur lors du rejet:', error);
      }
    });
  }

  deleteRequest() {
    if (!this.selectedRequest) return;

    if (confirm('Êtes-vous sûr de vouloir supprimer cette demande ?')) {
      this.apiService.adminDeleteRequest(this.selectedRequest.id, this.adminId).subscribe({
        next: () => {
          this.loadPendingRequests();
          this.selectedRequest = null;
        },
        error: (error) => {
          console.error('Erreur lors de la suppression:', error);
        }
      });
    }
  }

  getCategoryLabel(category: string): string {
    const categories: { [key: string]: string } = {
      heating: 'Chauffage',
      appliance: 'Électroménager',
      kitchen: 'Cuisine',
      bathroom: 'Salle de bain',
      flooring: 'Revêtement sol',
      other: 'Autre'
    };
    return categories[category] || category;
  }

  formatDate(date: Date): string {
    return new Date(date).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
}