import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';
import { AuthService } from '../../core/services/auth.service';
import { ObjectTreeSelectComponent } from '../../shared/components/object-tree-select/object-tree-select.component';
import { ObjectItem } from '../../core/models/models';

interface Problem {
  id: number;
  title: string;
  description: string;
  category: string;
  severity: string;
  status: string;
  symptoms?: string;
  possible_causes?: string;
  object_id: number;
  reported_by: number;
  created_at: string;
  updated_at: string;
  deleted_at?: string | null;
}

interface ProblemResolution {
  id: number;
  solution: string;
  steps?: string;
  cost_estimate?: string;
  time_estimate?: string;
  was_successful?: boolean;
  feedback?: string;
  helpfulness_score: number;
  images?: string;
  problem_id: number;
  resolved_by: number;
  created_at: string;
  updated_at: string;
  deleted_at?: string | null;
}

@Component({
  selector: 'app-problems',
  standalone: true,
  imports: [CommonModule, FormsModule, ObjectTreeSelectComponent],
  templateUrl: './problems.component.html',
  styleUrls: ['./problems.component.scss']
})
export class ProblemsComponent implements OnInit {
  problems: Problem[] = [];
  selectedProblem: Problem | null = null;
  resolutions: ProblemResolution[] = [];
  userObjects: ObjectItem[] = [];
  currentUserId: number | null = null;
  isAdmin: boolean = false;
  
  // Vue admin des problèmes supprimés
  showDeletedProblems: boolean = false;
  deletedProblems: Problem[] = [];
  
  // Vue admin des résolutions supprimées
  showDeletedResolutions: boolean = false;
  deletedResolutions: ProblemResolution[] = [];
  
  // Filtres
  filterStatus: string = 'all';
  filterSeverity: string = 'all';
  filterCategory: string = 'all';
  filterMyProblems: boolean = false;
  
  // État du formulaire
  showCreateForm: boolean = false;
  showResolutionForm: boolean = false;
  
  newProblem = {
    title: '',
    description: '',
    category: 'mechanical',
    severity: 'medium',
    symptoms: '',
    possible_causes: '',
    object_id: null as number | null
  };
  
  newResolution = {
    solution: '',
    steps: '',
    cost_estimate: '',
    time_estimate: '',
    feedback: '',
    images: ''
  };
  
  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {}
  
  ngOnInit() {
    this.currentUserId = this.authService.getUserId();
    this.isAdmin = this.authService.isAdmin();
    this.loadProblems();
    this.loadAllObjects();
  }
  
  loadAllObjects() {
    // Charge TOUS les objets disponibles (pas de filtre utilisateur)
    this.apiService.getObjects().subscribe({
      next: (data: ObjectItem[]) => {
        this.userObjects = data;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des objets:', error);
      }
    });
  }
  
  loadProblems() {
    const filters: any = {};
    
    if (this.filterMyProblems && this.currentUserId) {
      filters.my_problems = true;
      filters.user_id = this.currentUserId;
    }
    
    this.apiService.getProblems(filters).subscribe({
      next: (data: Problem[]) => {
        this.problems = data;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des problèmes:', error);
      }
    });
  }
  
  get filteredProblems(): Problem[] {
    return this.problems.filter(problem => {
      if (this.filterStatus !== 'all' && problem.status !== this.filterStatus) {
        return false;
      }
      if (this.filterSeverity !== 'all' && problem.severity !== this.filterSeverity) {
        return false;
      }
      if (this.filterCategory !== 'all' && problem.category !== this.filterCategory) {
        return false;
      }
      return true;
    });
  }
  
  toggleMyProblems() {
    this.filterMyProblems = !this.filterMyProblems;
    this.loadProblems();
  }
  
  selectProblem(problem: Problem) {
    this.selectedProblem = problem;
    this.loadResolutions(problem.id);
    this.showCreateForm = false;
    this.showResolutionForm = false;
  }
  
  loadResolutions(problemId: number) {
    // TODO: Implémenter l'appel API
    this.apiService.getProblemResolutions(problemId).subscribe({
      next: (data: ProblemResolution[]) => {
        this.resolutions = data;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des résolutions:', error);
      }
    });
  }
  
  createProblem() {
    // Validation
    if (!this.newProblem.object_id) {
      alert('Veuillez sélectionner un objet');
      return;
    }
    
    if (!this.newProblem.title || !this.newProblem.description) {
      alert('Veuillez remplir tous les champs obligatoires');
      return;
    }
    
    const userId = this.authService.getUserId();
    if (!userId) {
      alert('Vous devez être connecté pour signaler un problème');
      return;
    }
    
    this.apiService.createProblem(this.newProblem, userId).subscribe({
      next: (problem: Problem) => {
        this.problems.unshift(problem);
        this.showCreateForm = false;
        this.resetNewProblem();
      },
      error: (error) => {
        console.error('Erreur lors de la création du problème:', error);
        alert('Erreur lors de la création du problème. Vérifiez la console.');
      }
    });
  }
  
  createResolution() {
    if (!this.selectedProblem) return;
    
    const userId = this.authService.getUserId();
    if (!userId) {
      alert('Vous devez être connecté pour proposer une résolution');
      return;
    }
    
    this.apiService.createProblemResolution(
      this.selectedProblem.id,
      this.newResolution,
      userId
    ).subscribe({
      next: (resolution: ProblemResolution) => {
        this.resolutions.push(resolution);
        this.showResolutionForm = false;
        this.resetNewResolution();
      },
      error: (error) => {
        console.error('Erreur lors de la création de la résolution:', error);
        alert('Erreur lors de la création de la résolution. Vérifiez la console.');
      }
    });
  }
  
  upvoteResolution(resolution: ProblemResolution) {
    this.apiService.upvoteProblemResolution(resolution.id).subscribe({
      next: (data: any) => {
        resolution.helpfulness_score = data.helpfulness_score;
      },
      error: (error) => {
        console.error('Erreur lors du vote:', error);
      }
    });
  }

  markAsResolved(resolution: ProblemResolution) {
    const userId = this.authService.getUserId();
    if (!userId) {
      alert('Vous devez être connecté pour marquer comme résolu');
      return;
    }

    if (confirm('Confirmer que cette solution a résolu votre problème ?')) {
      this.apiService.markResolutionSuccessful(resolution.id, userId).subscribe({
        next: (data: any) => {
          resolution.was_successful = true;
          // Mettre à jour le statut du problème si c'est le problème sélectionné
          if (this.selectedProblem && this.selectedProblem.id === data.problem_id) {
            this.selectedProblem.status = data.problem_status;
          }
          alert('✅ Problème marqué comme résolu !');
        },
        error: (error) => {
          console.error('Erreur lors du marquage:', error);
          alert('Erreur lors du marquage comme résolu.');
        }
      });
    }
  }

  closeProblem() {
    if (!this.selectedProblem) return;
    
    const userId = this.authService.getUserId();
    if (!userId) {
      alert('Vous devez être connecté pour fermer le problème');
      return;
    }

    if (confirm('Fermer définitivement ce problème ? Aucune nouvelle solution ne pourra être ajoutée.')) {
      this.apiService.closeProblem(this.selectedProblem.id, userId).subscribe({
        next: (data: any) => {
          if (this.selectedProblem) {
            this.selectedProblem.status = data.problem_status;
          }
          alert('🔒 Problème fermé avec succès !');
        },
        error: (error) => {
          console.error('Erreur lors de la fermeture:', error);
          if (error.status === 403) {
            alert('❌ Seul le créateur du problème peut le fermer');
          } else {
            alert('Erreur lors de la fermeture du problème.');
          }
        }
      });
    }
  }

  reopenProblem() {
    if (!this.selectedProblem) return;
    
    const userId = this.authService.getUserId();
    if (!userId) {
      alert('Vous devez être connecté pour rouvrir le problème');
      return;
    }

    if (confirm('Rouvrir ce problème ? Il repassera en statut "Ouvert" et d\'autres solutions pourront être ajoutées.')) {
      this.apiService.reopenProblem(this.selectedProblem.id, userId).subscribe({
        next: (data: any) => {
          if (this.selectedProblem) {
            this.selectedProblem.status = data.problem_status;
          }
          alert('🔓 Problème rouvert avec succès !');
        },
        error: (error) => {
          console.error('Erreur lors de la réouverture:', error);
          if (error.status === 403) {
            alert('❌ Seul le créateur du problème peut le rouvrir');
          } else {
            alert('Erreur lors de la réouverture du problème.');
          }
        }
      });
    }
  }

  isOwner(): boolean {
    return this.selectedProblem?.reported_by === this.currentUserId;
  }

  // ===== ADMIN OPERATIONS =====
  adminSoftDeleteProblem(problem: Problem) {
    if (!this.isAdmin || !this.currentUserId) {
      alert('❌ Vous devez être administrateur pour effectuer cette action');
      return;
    }

    if (confirm(`⚠️ Êtes-vous sûr de vouloir supprimer le problème "${problem.title}" ?\n\nCette action peut être annulée depuis la vue "Problèmes supprimés".`)) {
      this.apiService.adminSoftDeleteProblem(problem.id, this.currentUserId).subscribe({
        next: (response) => {
          // Retirer le problème de la liste active
          this.problems = this.problems.filter(p => p.id !== problem.id);
          
          // Si c'est le problème sélectionné, revenir à la liste
          if (this.selectedProblem?.id === problem.id) {
            this.backToList();
          }
          
          alert(`✅ Problème "${problem.title}" supprimé avec succès`);
        },
        error: (error) => {
          console.error('Erreur lors de la suppression:', error);
          if (error.status === 403) {
            alert('❌ Accès refusé. Action réservée aux administrateurs.');
          } else if (error.status === 404) {
            alert('❌ Problème non trouvé ou déjà supprimé.');
          } else {
            alert('❌ Erreur lors de la suppression du problème.');
          }
        }
      });
    }
  }

  loadDeletedProblems() {
    if (!this.isAdmin || !this.currentUserId) {
      return;
    }

    this.apiService.adminGetDeletedProblems(this.currentUserId).subscribe({
      next: (data: Problem[]) => {
        this.deletedProblems = data;
        this.showDeletedProblems = true;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des problèmes supprimés:', error);
        alert('❌ Erreur lors du chargement des problèmes supprimés.');
      }
    });
  }

  adminRestoreProblem(problem: Problem) {
    if (!this.isAdmin || !this.currentUserId) {
      alert('❌ Vous devez être administrateur pour effectuer cette action');
      return;
    }

    if (confirm(`Restaurer le problème "${problem.title}" ?`)) {
      this.apiService.adminRestoreProblem(problem.id, this.currentUserId).subscribe({
        next: (response) => {
          // Retirer de la liste des supprimés
          this.deletedProblems = this.deletedProblems.filter(p => p.id !== problem.id);
          
          // Recharger la liste active pour y inclure le problème restauré
          this.loadProblems();
          
          alert(`✅ Problème "${problem.title}" restauré avec succès`);
          
          // Si plus aucun problème supprimé, retourner à la vue normale
          if (this.deletedProblems.length === 0) {
            this.showDeletedProblems = false;
          }
        },
        error: (error) => {
          console.error('Erreur lors de la restauration:', error);
          if (error.status === 403) {
            alert('❌ Accès refusé. Action réservée aux administrateurs.');
          } else if (error.status === 404) {
            alert('❌ Problème non trouvé.');
          } else if (error.status === 400) {
            alert('❌ Ce problème n\'est pas supprimé.');
          } else {
            alert('❌ Erreur lors de la restauration du problème.');
          }
        }
      });
    }
  }

  toggleDeletedView() {
    if (this.showDeletedProblems) {
      this.showDeletedProblems = false;
      this.deletedProblems = [];
    } else {
      this.loadDeletedProblems();
    }
  }

  // === Admin methods - Resolutions ===
  adminSoftDeleteResolution(resolution: ProblemResolution) {
    if (!this.isAdmin || !this.currentUserId) {
      alert('Vous devez être administrateur pour supprimer une résolution.');
      return;
    }
    
    if (!confirm(`Êtes-vous sûr de vouloir supprimer cette résolution ? Cette action peut être annulée.`)) {
      return;
    }
    
    this.apiService.adminSoftDeleteResolution(resolution.id, this.currentUserId).subscribe({
      next: () => {
        // Recharger les résolutions du problème courant
        if (this.selectedProblem) {
          this.loadResolutions(this.selectedProblem.id);
        }
        alert('Résolution supprimée avec succès');
      },
      error: (error) => {
        console.error('Erreur lors de la suppression:', error);
        alert('Erreur lors de la suppression de la résolution');
      }
    });
  }

  loadDeletedResolutions() {
    if (!this.isAdmin || !this.currentUserId) return;
    
    this.apiService.adminGetDeletedResolutions(this.currentUserId).subscribe({
      next: (data) => {
        this.deletedResolutions = data;
        this.showDeletedResolutions = true;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des résolutions supprimées:', error);
      }
    });
  }

  adminRestoreResolution(resolution: ProblemResolution) {
    if (!this.isAdmin || !this.currentUserId) {
      alert('Vous devez être administrateur pour restaurer une résolution.');
      return;
    }
    
    this.apiService.adminRestoreResolution(resolution.id, this.currentUserId).subscribe({
      next: () => {
        // Retirer de la liste des supprimés
        this.deletedResolutions = this.deletedResolutions.filter(r => r.id !== resolution.id);
        
        // Recharger les résolutions du problème courant si c'est le même
        if (this.selectedProblem && this.selectedProblem.id === resolution.problem_id) {
          this.loadResolutions(this.selectedProblem.id);
        }
        
        alert('Résolution restaurée avec succès');
        
        // Si plus de résolutions supprimées, fermer la vue
        if (this.deletedResolutions.length === 0) {
          this.showDeletedResolutions = false;
        }
      },
      error: (error) => {
        console.error('Erreur lors de la restauration:', error);
        alert('Erreur lors de la restauration de la résolution');
      }
    });
  }

  toggleDeletedResolutionsView() {
    if (this.showDeletedResolutions) {
      this.showDeletedResolutions = false;
      this.deletedResolutions = [];
    } else {
      this.loadDeletedResolutions();
    }
  }
  
  getSeverityClass(severity: string): string {
    const classes: { [key: string]: string } = {
      'low': 'badge-info',
      'medium': 'badge-warning',
      'high': 'badge-error',
      'critical': 'badge-error'
    };
    return classes[severity] || 'badge-primary';
  }
  
  getStatusClass(status: string): string {
    const classes: { [key: string]: string } = {
      'open': 'badge-warning',
      'in_progress': 'badge-info',
      'resolved': 'badge-success',
      'closed': 'badge-primary'
    };
    return classes[status] || 'badge-primary';
  }
  
  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      'open': 'Ouvert',
      'in_progress': 'En cours',
      'resolved': 'Résolu',
      'closed': 'Fermé'
    };
    return labels[status] || status;
  }
  
  getSeverityLabel(severity: string): string {
    const labels: { [key: string]: string } = {
      'low': 'Faible',
      'medium': 'Moyen',
      'high': 'Élevé',
      'critical': 'Critique'
    };
    return labels[severity] || severity;
  }
  
  resetNewProblem() {
    this.newProblem = {
      title: '',
      description: '',
      category: 'mechanical',
      severity: 'medium',
      symptoms: '',
      possible_causes: '',
      object_id: null
    };
  }
  
  resetNewResolution() {
    this.newResolution = {
      solution: '',
      steps: '',
      cost_estimate: '',
      time_estimate: '',
      feedback: '',
      images: ''
    };
  }
  
  backToList() {
    this.selectedProblem = null;
    this.resolutions = [];
    this.showResolutionForm = false;
  }
}
