import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import {
  User,
  ObjectItem,
  MaintenanceAdvice,
  MaintenanceTask,
  Contribution,
} from "../models/models";

@Injectable({
  providedIn: "root",
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // ===== USERS =====
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users/`);
  }

  createUser(user: Partial<User>): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/users/`, user);
  }

  // ===== OBJECTS =====
  getObjects(userId?: number): Observable<ObjectItem[]> {
    const url = userId
      ? `${this.apiUrl}/objects/?user_id=${userId}`
      : `${this.apiUrl}/objects/`;
    return this.http.get<ObjectItem[]>(url);
  }

  createObject(
    object: Partial<ObjectItem>,
    userId: number
  ): Observable<ObjectItem> {
    return this.http.post<ObjectItem>(
      `${this.apiUrl}/objects/?user_id=${userId}`,
      object
    );
  }

  updateObject(
    id: number,
    object: Partial<ObjectItem>
  ): Observable<ObjectItem> {
    return this.http.put<ObjectItem>(`${this.apiUrl}/objects/${id}`, object);
  }

  deleteObject(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/objects/${id}`);
  }

  // ===== USER OBJECTS (New endpoints US 2.2) =====
  getUserObjects(userId: number): Observable<ObjectItem[]> {
    return this.http.get<ObjectItem[]>(
      `${this.apiUrl}/users/${userId}/objects`
    );
  }

  addUserObject(
    userId: number,
    object: Partial<ObjectItem>
  ): Observable<ObjectItem> {
    return this.http.post<ObjectItem>(
      `${this.apiUrl}/users/${userId}/objects`,
      object
    );
  }

  getUserObject(userId: number, objectId: number): Observable<ObjectItem> {
    return this.http.get<ObjectItem>(
      `${this.apiUrl}/users/${userId}/objects/${objectId}`
    );
  }

  updateUserObject(
    userId: number,
    objectId: number,
    object: Partial<ObjectItem>
  ): Observable<ObjectItem> {
    return this.http.put<ObjectItem>(
      `${this.apiUrl}/users/${userId}/objects/${objectId}`,
      object
    );
  }

  deleteUserObject(userId: number, objectId: number): Observable<any> {
    return this.http.delete(
      `${this.apiUrl}/users/${userId}/objects/${objectId}`
    );
  }

  // ===== MAINTENANCE ADVICE =====
  getMaintenanceAdvice(): Observable<MaintenanceAdvice[]> {
    return this.http.get<MaintenanceAdvice[]>(
      `${this.apiUrl}/maintenance/advice`
    );
  }

  // ===== MAINTENANCE TASKS =====
  getMaintenanceTasks(userId?: number): Observable<MaintenanceTask[]> {
    const url = userId
      ? `${this.apiUrl}/maintenance/tasks?user_id=${userId}`
      : `${this.apiUrl}/maintenance/tasks`;
    return this.http.get<MaintenanceTask[]>(url);
  }

  updateMaintenanceTask(
    id: number,
    task: Partial<MaintenanceTask>
  ): Observable<MaintenanceTask> {
    return this.http.put<MaintenanceTask>(
      `${this.apiUrl}/maintenance/tasks/${id}`,
      task
    );
  }

  // ===== CONTRIBUTIONS =====
  getContributions(): Observable<Contribution[]> {
    return this.http.get<Contribution[]>(
      `${this.apiUrl}/community/contributions`
    );
  }

  createContribution(
    contribution: Partial<Contribution>,
    authorId: number
  ): Observable<Contribution> {
    return this.http.post<Contribution>(
      `${this.apiUrl}/community/contributions?author_id=${authorId}`,
      contribution
    );
  }

  upvoteContribution(id: number): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/community/contributions/${id}/upvote`,
      {}
    );
  }
}
