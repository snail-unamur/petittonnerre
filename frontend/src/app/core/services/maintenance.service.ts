import { Injectable } from "@angular/core";
import { ApiService } from "./api.service";
import { Observable } from "rxjs";
import { MaintenanceTask } from "../models/models";

@Injectable({
  providedIn: "root",
})
export class MaintenanceService {
  constructor(private readonly api: ApiService) {}

  getTasks(filters?: {
    user_id?: number;
    object_id?: number;
    status?: "pending" | "completed" | "skipped" | "issue_reported";
    skip?: number;
    limit?: number;
  }): Observable<MaintenanceTask[]> {
    return this.api.getMaintenanceTasks(filters?.user_id);
  }

  getTask(taskId: number): Observable<MaintenanceTask> {
    return this.api.getMaintenanceTask(taskId);
  }

  updateTask(
    taskId: number,
    update: Partial<MaintenanceTask>
  ): Observable<MaintenanceTask> {
    return this.api.updateMaintenanceTask(taskId, update);
  }
}
