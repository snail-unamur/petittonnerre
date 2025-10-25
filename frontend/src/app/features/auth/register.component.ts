import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from "@angular/forms";
import { Router } from "@angular/router";
import { AuthService } from "../../core/services/auth.service";

@Component({
  selector: "app-register",
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h2 class="text-center mb-4">Créer un compte</h2>

              <form [formGroup]="registerForm" (ngSubmit)="onSubmit()">
                <div class="form-group mb-3">
                  <label for="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    formControlName="email"
                    class="form-control"
                    [ngClass]="{ 'is-invalid': submitted && f['email'].errors }"
                  />
                  <div
                    *ngIf="submitted && f['email'].errors"
                    class="invalid-feedback"
                  >
                    <div *ngIf="f['email'].errors?.['required']">
                      Email requis
                    </div>
                    <div *ngIf="f['email'].errors?.['email']">
                      Email invalide
                    </div>
                  </div>
                </div>

                <div class="form-group mb-3">
                  <label for="username">Nom d'utilisateur</label>
                  <input
                    type="text"
                    id="username"
                    formControlName="username"
                    class="form-control"
                    [ngClass]="{
                      'is-invalid': submitted && f['username'].errors
                    }"
                  />
                  <div
                    *ngIf="submitted && f['username'].errors"
                    class="invalid-feedback"
                  >
                    <div *ngIf="f['username'].errors?.['required']">
                      Nom d'utilisateur requis
                    </div>
                    <div *ngIf="f['username'].errors?.['minlength']">
                      Le nom d'utilisateur doit avoir au moins 3 caractères
                    </div>
                  </div>
                </div>

                <div class="form-group mb-3">
                  <label for="password">Mot de passe</label>
                  <input
                    type="password"
                    id="password"
                    formControlName="password"
                    class="form-control"
                    [ngClass]="{
                      'is-invalid': submitted && f['password'].errors
                    }"
                  />
                  <div
                    *ngIf="submitted && f['password'].errors"
                    class="invalid-feedback"
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

                <div class="form-group mb-3">
                  <label for="passwordConfirm">Confirmer le mot de passe</label>
                  <input
                    type="password"
                    id="passwordConfirm"
                    formControlName="password_confirm"
                    class="form-control"
                    [ngClass]="{
                      'is-invalid': submitted && f['password_confirm'].errors
                    }"
                  />
                  <div
                    *ngIf="submitted && f['password_confirm'].errors"
                    class="invalid-feedback"
                  >
                    <div *ngIf="f['password_confirm'].errors?.['required']">
                      Confirmation du mot de passe requise
                    </div>
                    <div *ngIf="f['password_confirm'].errors?.['matching']">
                      Les mots de passe ne correspondent pas
                    </div>
                  </div>
                </div>

                <div class="form-group mb-3">
                  <label for="location">Localisation (optionnel)</label>
                  <input
                    type="text"
                    id="location"
                    formControlName="location"
                    class="form-control"
                  />
                </div>

                <div *ngIf="error" class="alert alert-danger">
                  {{ error }}
                </div>

                <div class="text-center">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    [disabled]="loading"
                  >
                    <span
                      *ngIf="loading"
                      class="spinner-border spinner-border-sm me-1"
                    ></span>
                    S'inscrire
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      .card {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }
    `,
  ],
})
export class RegisterComponent {
  registerForm: FormGroup;
  loading = false;
  submitted = false;
  error = "";

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

    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = "";

    this.authService.register(this.registerForm.value).subscribe({
      next: () => {
        this.router.navigate(["/auth/login"], {
          queryParams: { registered: "true" },
        });
      },
      error: (error) => {
        this.error = error.error.detail || "Une erreur est survenue";
        this.loading = false;
      },
    });
  }
}
