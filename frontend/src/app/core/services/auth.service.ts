import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, tap, BehaviorSubject } from "rxjs";
import { environment } from "../../../environments/environment";

export interface UserRegistration {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  location?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  email: string;
  username: string;
  location?: string;
  role: string;
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private currentUserSubject = new BehaviorSubject<UserResponse | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    // Charger l'utilisateur au démarrage si token existe
    if (this.isAuthenticated()) {
      this.loadCurrentUser();
    }
  }

  register(userData: UserRegistration): Observable<UserResponse> {
    return this.http.post<UserResponse>(
      `${this.apiUrl}/auth/register`,
      userData
    );
  }

  login(credentials: LoginData): Observable<Token> {
    // Le backend attend le format OAuth2 (FormData avec username/password)
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    return this.http.post<Token>(
      `${this.apiUrl}/auth/login`,
      formData
    ).pipe(
      tap(response => {
        localStorage.setItem('token', response.access_token);
        // Charger les infos utilisateur après login
        this.loadCurrentUser();
      })
    );
  }

  logout(): Observable<any> {
    // Nettoyer immédiatement le localStorage et l'état
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
    this.currentUserSubject.next(null);
    
    // Appeler le backend (sans bloquer le logout local si ça échoue)
    return this.http.post(`${this.apiUrl}/auth/logout`, {});
  }

  getCurrentUser(): Observable<UserResponse> {
    return this.http.get<UserResponse>(`${this.apiUrl}/auth/me`).pipe(
      tap(user => {
        this.currentUserSubject.next(user);
        // Garder en localStorage pour compatibilité
        localStorage.setItem('username', user.username);
        localStorage.setItem('userId', user.id.toString());
      })
    );
  }

  private loadCurrentUser(): void {
    this.getCurrentUser().subscribe({
      error: () => {
        // Si erreur (token invalide), nettoyer
        this.logout().subscribe();
      }
    });
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem("token");
  }

  getToken(): string | null {
    return localStorage.getItem("token");
  }

  getUsername(): string | null {
    return localStorage.getItem("username");
  }

  getUserId(): number | null {
    const userId = localStorage.getItem('userId');
    return userId ? parseInt(userId, 10) : null;
  }

  getCurrentUserValue(): UserResponse | null {
    return this.currentUserSubject.value;
  }
}
