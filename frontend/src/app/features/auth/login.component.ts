import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterModule, Router, ActivatedRoute } from "@angular/router";
import { FormsModule } from "@angular/forms";
import { AuthService } from "../../core/services/auth.service";
import { ThemeService } from "../../core/services/theme.service";

@Component({
  selector: "app-login",
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginData = {
    email: '',
    password: ''
  };
  
  errorMessage = '';
  successMessage = '';
  isLoading = false;
  private returnUrl: string = '/dashboard';
  
  constructor(
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    public themeService: ThemeService
  ) {}

  ngOnInit() {
    // Récupérer l'URL de retour depuis les query params
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
  }
  
  onSubmit() {
    if (!this.loginData.email || !this.loginData.password) {
      this.errorMessage = 'Veuillez remplir tous les champs';
      return;
    }
    
    this.errorMessage = '';
    this.successMessage = '';
    this.isLoading = true;

    this.authService.login({
      email: this.loginData.email,
      password: this.loginData.password
    }).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.successMessage = 'Connexion réussie! Redirection...';
        setTimeout(() => {
          this.router.navigateByUrl(this.returnUrl);
        }, 1000);
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.detail || 'Identifiants incorrects. Veuillez réessayer.';
      }
    });
  }

  toggleTheme() {
    this.themeService.toggleTheme();
  }
}
