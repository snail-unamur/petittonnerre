import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterModule } from "@angular/router";
import { FormsModule } from "@angular/forms";
import { ApiService } from "../../core/services/api.service";
import { AuthService } from "../../core/services/auth.service";

@Component({
  selector: "app-login",
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  template: `
    <div
      class="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8"
    >
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <div class="text-center">
          <h2 class="mt-6 text-4xl font-bold tracking-tight text-white">
            Bienvenue
          </h2>
          <p class="mt-2 text-center text-lg text-blue-100">
            Ou
            <a
              routerLink="/auth/register"
              class="font-medium text-white hover:text-blue-200 underline transition-all duration-200"
            >
              créez un compte
            </a>
          </p>
        </div>

        <div class="mt-8">
          <div
            class="bg-white/90 backdrop-blur-sm py-8 px-4 shadow-2xl rounded-2xl sm:px-10 transition-all duration-300 hover:shadow-blue-400/20"
          >
            <form class="space-y-6" (ngSubmit)="onSubmit()" #loginForm="ngForm">
              <!-- Email -->
              <div class="space-y-2">
                <label
                  for="email"
                  class="block text-sm font-semibold text-gray-700"
                >
                  Email
                </label>
                <div class="mt-1 relative rounded-md shadow-sm">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    [(ngModel)]="loginData.email"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 transition-all duration-200"
                    placeholder="vous@exemple.com"
                  />
                </div>
              </div>

              <!-- Password -->
              <div class="space-y-2">
                <label
                  for="password"
                  class="block text-sm font-semibold text-gray-700"
                >
                  Mot de passe
                </label>
                <div class="mt-1 relative rounded-md shadow-sm">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    [(ngModel)]="loginData.password"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 transition-all duration-200"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <!-- Error Message -->
              <div
                *ngIf="errorMessage"
                class="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm"
              >
                {{ errorMessage }}
              </div>

              <!-- Submit Button -->
              <div class="pt-2">
                <button
                  type="submit"
                  [disabled]="!loginForm.form.valid"
                  class="w-full flex justify-center py-3 px-4 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/20 hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5"
                >
                  Se connecter
                </button>
              </div>

              <div class="mt-6 text-center">
                <a
                  href="#"
                  class="text-sm text-gray-600 hover:text-blue-600 transition-colors duration-200"
                >
                  Mot de passe oublié ?
                </a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  `,
})
export class LoginComponent {
  loginData = {
    email: "",
    password: "",
  };
  errorMessage = "";

  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {}

  onSubmit() {
    // Pour l'instant, juste un placeholder jusqu'à ce qu'on implémente la connexion
    console.log("Login submitted:", this.loginData);
  }
}
