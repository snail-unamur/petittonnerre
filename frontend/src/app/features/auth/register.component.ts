import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from "@angular/forms";
import { Router, RouterModule } from "@angular/router";
import { AuthService } from "../../core/services/auth.service";

@Component({
  selector: "app-register",
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  template: `
    <div
      class="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8"
    >
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <div class="text-center">
          <h2 class="text-4xl font-bold tracking-tight text-white">
            Créer un compte
          </h2>
          <p class="mt-2 text-lg text-purple-100">
            Ou
            <a
              routerLink="/auth/login"
              class="font-medium text-white hover:text-purple-200 underline transition-all duration-200"
            >
              connectez-vous
            </a>
          </p>
        </div>

        <div class="mt-8">
          <div
            class="bg-white/90 backdrop-blur-sm py-8 px-4 shadow-2xl rounded-2xl sm:px-10 transition-all duration-300 hover:shadow-purple-400/20"
          >
            <form
              [formGroup]="registerForm"
              (ngSubmit)="onSubmit()"
              class="space-y-6"
            >
              <!-- Email -->
              <div class="space-y-2">
                <label
                  for="email"
                  class="block text-sm font-semibold text-gray-700"
                >
                  Email
                </label>
                <div class="mt-1 relative">
                  <input
                    type="email"
                    id="email"
                    formControlName="email"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 transition-all duration-200"
                    [ngClass]="{
                      'ring-red-500 ring-2':
                        submitted && (f['email'].errors || fieldErrors['email'])
                    }"
                    placeholder="vous@exemple.com"
                  />
                  <div
                    *ngIf="
                      submitted && (f['email'].errors || fieldErrors['email'])
                    "
                    class="mt-2 text-sm font-medium text-red-600 animate-fade-in"
                  >
                    <div *ngIf="f['email'].errors?.['required']">
                      Email requis
                    </div>
                    <div *ngIf="f['email'].errors?.['email']">
                      Email invalide
                    </div>
                    <div
                      *ngIf="f['email'].errors?.['emailExists']"
                      class="flex items-center gap-1"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                        />
                      </svg>
                      {{ fieldErrors["email"] }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Username -->
              <div class="space-y-2">
                <label
                  for="username"
                  class="block text-sm font-semibold text-gray-700"
                >
                  Nom d'utilisateur
                </label>
                <div class="mt-1 relative">
                  <input
                    type="text"
                    id="username"
                    formControlName="username"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 transition-all duration-200"
                    [ngClass]="{
                      'ring-red-500 ring-2': submitted && f['username'].errors
                    }"
                    placeholder="votre pseudo"
                  />
                  <div
                    *ngIf="
                      submitted &&
                      (f['username'].errors || fieldErrors['username'])
                    "
                    class="mt-2 text-sm font-medium text-red-600 animate-fade-in"
                  >
                    <div *ngIf="f['username'].errors?.['required']">
                      Nom d'utilisateur requis
                    </div>
                    <div *ngIf="f['username'].errors?.['minlength']">
                      Le nom d'utilisateur doit avoir au moins 3 caractères
                    </div>
                    <div
                      *ngIf="f['username'].errors?.['usernameTaken']"
                      class="flex items-center gap-1"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                        />
                      </svg>
                      {{ fieldErrors["username"] }}
                    </div>
                  </div>
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
                <div class="mt-1 relative">
                  <input
                    type="password"
                    id="password"
                    formControlName="password"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 transition-all duration-200"
                    [ngClass]="{
                      'ring-red-500 ring-2': submitted && f['password'].errors
                    }"
                    placeholder="••••••••"
                  />
                  <div
                    *ngIf="submitted && f['password'].errors"
                    class="mt-2 text-sm text-red-600"
                  >
                    <div *ngIf="f['password'].errors?.['required']">
                      Mot de passe requis
                    </div>
                    <div *ngIf="f['password'].errors?.['pattern']">
                      Le mot de passe doit contenir au moins 8 caractères, une
                      majuscule, une minuscule, un chiffre et un caractère
                      spécial
                    </div>
                  </div>
                </div>
              </div>

              <!-- Confirm Password -->
              <div class="space-y-2">
                <label
                  for="passwordConfirm"
                  class="block text-sm font-semibold text-gray-700"
                >
                  Confirmer le mot de passe
                </label>
                <div class="mt-1 relative">
                  <input
                    type="password"
                    id="passwordConfirm"
                    formControlName="password_confirm"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 transition-all duration-200"
                    [ngClass]="{
                      'ring-red-500 ring-2':
                        submitted &&
                        (f['password_confirm'].errors ||
                          registerForm.hasError('matching'))
                    }"
                    placeholder="••••••••"
                  />
                  <div
                    *ngIf="
                      submitted &&
                      (f['password_confirm'].errors ||
                        registerForm.hasError('matching'))
                    "
                    class="mt-2 text-sm text-red-600"
                  >
                    <div *ngIf="f['password_confirm'].errors?.['required']">
                      Confirmation du mot de passe requise
                    </div>
                    <div *ngIf="registerForm.hasError('matching')">
                      Les mots de passe ne correspondent pas
                    </div>
                  </div>
                </div>
              </div>

              <!-- Location -->
              <div class="space-y-2">
                <label
                  for="location"
                  class="block text-sm font-semibold text-gray-700"
                >
                  Localisation
                </label>
                <div class="mt-1 relative">
                  <input
                    type="text"
                    id="location"
                    formControlName="location"
                    class="block w-full px-4 py-3 rounded-xl border-0 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 transition-all duration-200"
                    placeholder="Votre ville"
                  />
                </div>
              </div>

              <!-- General Error Message -->
              <div
                *ngIf="error"
                class="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm animate-fade-in"
              >
                {{ error }}
              </div>

              <!-- Submit Button -->
              <div class="pt-2">
                <button
                  type="submit"
                  [disabled]="loading"
                  class="w-full flex justify-center items-center py-3 px-4 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-purple-500/20 hover:shadow-xl hover:shadow-purple-500/30 hover:-translate-y-0.5"
                >
                  <span
                    *ngIf="loading"
                    class="inline-block mr-2 h-4 w-4 animate-spin rounded-full border-2 border-solid border-current border-r-transparent motion-reduce:animate-[spin_1.5s_linear_infinite]"
                  ></span>
                  S'inscrire
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  `,
})
export class RegisterComponent {
  registerForm: FormGroup;
  loading = false;
  submitted = false;
  error = "";
  fieldErrors: { [key: string]: string } = {};

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {
    this.registerForm = this.formBuilder.group(
      {
        email: ["", [Validators.required, Validators.email]],
        username: ["", [Validators.required, Validators.minLength(3)]],
        password: [
          "",
          [
            Validators.required,
            Validators.pattern(
              /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/
            ),
          ],
        ],
        password_confirm: ["", Validators.required],
        location: [""],
      },
      {
        validator: this.passwordMatchValidator,
      }
    );
  }

  get f(): { [key: string]: any } {
    const controls = this.registerForm.controls;
    return {
      email: controls["email"],
      username: controls["username"],
      password: controls["password"],
      password_confirm: controls["password_confirm"],
      location: controls["location"],
    };
  }

  passwordMatchValidator(g: FormGroup) {
    return g.get("password")?.value === g.get("password_confirm")?.value
      ? null
      : { matching: true };
  }

  onSubmit() {
    this.submitted = true;
    this.fieldErrors = {};
    this.error = "";

    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;

    this.authService.register(this.registerForm.value).subscribe({
      next: () => {
        this.router.navigate(["/auth/login"], {
          queryParams: { registered: "true" },
        });
      },
      error: (error) => {
        this.loading = false;

        // Gérer les erreurs spécifiques
        if (error.error.detail === "Email already registered") {
          this.fieldErrors["email"] = "Cet email est déjà utilisé";
          this.f["email"].setErrors({ emailExists: true });
        } else if (error.error.detail === "Username already taken") {
          this.fieldErrors["username"] = "Ce nom d'utilisateur est déjà pris";
          this.f["username"].setErrors({ usernameTaken: true });
        } else {
          this.error = error.error.detail || "Une erreur est survenue";
        }
      },
    });
  }
}
