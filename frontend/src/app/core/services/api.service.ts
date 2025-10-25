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
  ObjectRequest,
  ObjectRequestDecision,
} from "../models/models";

@Injectable({
  providedIn: "root",
})
export class ApiService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

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

  createMaintenanceTask(
    task: Partial<MaintenanceTask>,
    userId: number
  ): Observable<MaintenanceTask> {
    return this.http.post<MaintenanceTask>(
      `${this.apiUrl}/maintenance/tasks?user_id=${userId}`,
      task
    );
  }

  updateMaintenanceTask(
    id: number,
    task: Partial<MaintenanceTask>
  ): Observable<MaintenanceTask> {
    return this.http.patch<MaintenanceTask>(
      `${this.apiUrl}/maintenance/tasks/${id}`,
      task
    );
  }

  exportMaintenanceToIcal(userId: number): Observable<Blob> {
    return this.http.get(
      `${this.apiUrl}/maintenance/export/ical?user_id=${userId}`,
      { responseType: 'blob' }
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

  // ===== PROBLEMS =====
  getProblems(filters?: any): Observable<any[]> {
    let url = `${this.apiUrl}/problems/`;
    const params = new URLSearchParams();
    
    if (filters) {
      if (filters.object_id) params.append('object_id', filters.object_id);
      if (filters.category) params.append('category', filters.category);
      if (filters.status) params.append('status', filters.status);
      if (filters.severity) params.append('severity', filters.severity);
    }
    
    const queryString = params.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
    
    return this.http.get<any[]>(url);
  }

  getProblem(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/problems/${id}`);
  }

  createProblem(problem: any, userId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/problems/?user_id=${userId}`, problem);
  }

  updateProblem(id: number, problem: Partial<any>): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}/problems/${id}`, problem);
  }

  deleteProblem(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/problems/${id}`);
  }

  // ===== PROBLEM RESOLUTIONS =====
  getProblemResolutions(problemId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/problems/${problemId}/resolutions`);
  }

  createProblemResolution(problemId: number, resolution: any, userId: number): Observable<any> {
    return this.http.post<any>(
      `${this.apiUrl}/problems/${problemId}/resolutions?user_id=${userId}`,
      resolution
    );
  }

  updateProblemResolution(resolutionId: number, resolution: Partial<any>): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}/problems/resolutions/${resolutionId}`, resolution);
  }

  upvoteProblemResolution(resolutionId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/problems/resolutions/${resolutionId}/upvote`, {});
  }

  markResolutionSuccessful(resolutionId: number, userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/problems/resolutions/${resolutionId}/mark-successful?user_id=${userId}`, {});
  }

  closeProblem(problemId: number, userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/problems/${problemId}/close?user_id=${userId}`, {});
  }

  reopenProblem(problemId: number, userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/problems/${problemId}/reopen?user_id=${userId}`, {});
  }

  // ===== OBJECT REQUESTS =====
  createObjectRequest(request: Partial<ObjectRequest>, userId: number): Observable<ObjectRequest> {
    return this.http.post<ObjectRequest>(`${this.apiUrl}/objects/requests?user_id=${userId}`, request);
  }

  getObjectRequests(status?: string): Observable<ObjectRequest[]> {
    const url = status ? `${this.apiUrl}/objects/requests?status=${status}` : `${this.apiUrl}/objects/requests`;
    return this.http.get<ObjectRequest[]>(url);
  }

  getObjectRequest(id: number): Observable<ObjectRequest> {
    return this.http.get<ObjectRequest>(`${this.apiUrl}/objects/requests/${id}`);
  }

  // ===== ADMIN OPERATIONS =====
  getPendingRequests(adminId: number): Observable<ObjectRequest[]> {
    return this.http.get<ObjectRequest[]>(`${this.apiUrl}/objects/admin/pending-requests?admin_id=${adminId}`);
  }

  adminDecideRequest(requestId: number, decision: ObjectRequestDecision, adminId: number): Observable<ObjectRequest> {
    return this.http.put<ObjectRequest>(`${this.apiUrl}/objects/requests/${requestId}/decide?admin_id=${adminId}`, decision);
  }

  adminDeleteRequest(requestId: number, adminId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/objects/admin/requests/${requestId}?admin_id=${adminId}`);
  }
}
