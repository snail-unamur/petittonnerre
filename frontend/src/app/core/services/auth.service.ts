import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";

export interface UserRegistration {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  location?: string;
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
}
