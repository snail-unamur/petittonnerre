import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, tap } from "rxjs";
import { environment } from "../../../environments/environment";

export interface UserRegistration {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  location?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserResponse;
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

  constructor(private http: HttpClient) {}

  register(userData: UserRegistration): Observable<UserResponse> {
    return this.http.post<UserResponse>(
      `${this.apiUrl}/users/register`,
      userData
    );
  }

  login(credentials: UserLogin): Observable<LoginResponse> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    return this.http.post<LoginResponse>(
      `${this.apiUrl}/users/login`,
      formData
    ).pipe(
      tap(response => {
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('username', response.user.username);
        localStorage.setItem('userId', response.user.id.toString());
      })
    );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }

  getUserId(): number | null {
    const userId = localStorage.getItem('userId');
    return userId ? parseInt(userId, 10) : null;
  }
}
