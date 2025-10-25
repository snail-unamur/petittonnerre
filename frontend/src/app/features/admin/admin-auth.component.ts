import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-auth',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="auth-overlay">
      <div class="auth-dialog">
        <h2>🔐 Accès Administrateur</h2>
        <p>Cette zone est réservée aux administrateurs.</p>
        
        <div class="auth-form">
          <div class="question">
            <label>Êtes-vous administrateur ?</label>
            <div class="radio-group">
              <label>
                <input type="radio" name="isAdmin" value="yes" [(ngModel)]="isAdmin">
                Oui
              </label>
              <label>
                <input type="radio" name="isAdmin" value="no" [(ngModel)]="isAdmin">
                Non
              </label>
            </div>
          </div>

          <div *ngIf="isAdmin === 'yes'" class="admin-code">
            <label for="adminCode">Code administrateur temporaire :</label>
            <input 
              type="password" 
              id="adminCode" 
              [(ngModel)]="adminCode" 
              placeholder="Entrez le code admin"
              (keyup.enter)="authenticate()">
            <small>Code temporaire : admin123</small>
          </div>

          <div class="auth-actions">
            <button class="btn btn-primary" (click)="authenticate()" [disabled]="!canAuthenticate()">
              Accéder
            </button>
            <button class="btn btn-secondary" (click)="goBack()">
              Retour
            </button>
          </div>

          <div *ngIf="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .auth-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.7);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }

    .auth-dialog {
      background: white;
      padding: 30px;
      border-radius: 8px;
      max-width: 400px;
      width: 90%;
      text-align: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    h2 {
      color: #333;
      margin-bottom: 10px;
    }

    p {
      color: #666;
      margin-bottom: 20px;
    }

    .auth-form {
      text-align: left;
    }

    .question {
      margin-bottom: 20px;

      label {
        display: block;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
      }
    }

    .radio-group {
      display: flex;
      gap: 15px;

      label {
        display: flex;
        align-items: center;
        font-weight: normal;
        margin-bottom: 0;
        cursor: pointer;

        input {
          margin-right: 5px;
        }
      }
    }

    .admin-code {
      margin-bottom: 20px;

      label {
        display: block;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
      }

      input {
        width: 100%;
        padding: 8px;
        border: 2px solid #e0e0e0;
        border-radius: 4px;
        margin-bottom: 5px;

        &:focus {
          outline: none;
          border-color: #007bff;
        }
      }

      small {
        color: #666;
        font-style: italic;
      }
    }

    .auth-actions {
      display: flex;
      gap: 10px;
      justify-content: center;

      .btn {
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 500;

        &.btn-primary {
          background-color: #007bff;
          color: white;

          &:hover:not(:disabled) {
            background-color: #0056b3;
          }

          &:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
          }
        }

        &.btn-secondary {
          background-color: #6c757d;
          color: white;

          &:hover {
            background-color: #5a6268;
          }
        }
      }
    }

    .error-message {
      margin-top: 15px;
      padding: 10px;
      background-color: #f8d7da;
      color: #721c24;
      border-radius: 4px;
      text-align: center;
    }
  `]
})
export class AdminAuthComponent {
  isAdmin: string = '';
  adminCode: string = '';
  errorMessage: string = '';

  constructor(private router: Router) {}

  canAuthenticate(): boolean {
    if (this.isAdmin === 'no') return true;
    if (this.isAdmin === 'yes') return this.adminCode.length > 0;
    return false;
  }

  authenticate() {
    if (this.isAdmin === 'no') {
      this.router.navigate(['/']);
      return;
    }

    if (this.isAdmin === 'yes') {
      // Vérification temporaire du code admin
      if (this.adminCode === 'admin123') {
        // Stocker temporairement l'état admin (en production, utiliser un JWT)
        localStorage.setItem('tempAdminAuth', 'true');
        this.router.navigate(['/admin/dashboard']);
      } else {
        this.errorMessage = 'Code administrateur incorrect';
      }
    }
  }

  goBack() {
    this.router.navigate(['/']);
  }
}