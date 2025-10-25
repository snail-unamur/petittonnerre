import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterModule, Router } from "@angular/router";
import { FormsModule } from "@angular/forms";
import { AuthService } from "../../core/services/auth.service";

@Component({
  selector: "app-register",
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  formData = {
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    location: ''
  };
  
  errorMessage = '';
  successMessage = '';
  isLoading = false;
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  onSubmit() {
    if (this.isLoading) return;
    
    // Check if passwords match
    if (this.formData.password !== this.formData.password_confirm) {
      this.errorMessage = 'Les mots de passe ne correspondent pas';
      return;
    }
    
    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';
    
    // Prepare user data
    const userData = {
      username: this.formData.username,
      email: this.formData.email,
      password: this.formData.password,
      password_confirm: this.formData.password_confirm,
      location: this.formData.location || undefined
    };
    
    this.authService.register(userData).subscribe({
      next: (response) => {
        this.successMessage = 'Inscription réussie ! Redirection vers la page de connexion...';
        setTimeout(() => {
          this.router.navigate(['/auth/login']);
        }, 2000);
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.detail || 'Une erreur est survenue lors de l\'inscription';
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }
}