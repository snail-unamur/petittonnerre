import { ComponentFixture, TestBed } from "@angular/core/testing";
import { MaintenanceComponent } from "./maintenance.component";
import { ApiService } from "../../core/services/api.service";
import { MaintenanceTask } from "../../core/models/models";
import { of, throwError } from "rxjs";

describe("MaintenanceComponent", () => {
  let component: MaintenanceComponent;
  let fixture: ComponentFixture<MaintenanceComponent>;
  let apiService: jasmine.SpyObj<ApiService>;

  const mockTasks: MaintenanceTask[] = [
    {
      id: 1,
      name: "Nettoyer le filtre",
      scheduled_date: new Date("2025-10-25"),
      status: "pending",
      object_id: 1,
      user_id: 1,
      advice_id: 1,
      object: {
        id: 1,
        name: "Chaudière",
        category: "heating",
        owner_id: 1,
        created_at: new Date("2025-01-01"),
      },
    },
    {
      id: 2,
      name: "Vérifier la pression",
      scheduled_date: new Date("2025-10-26"),
      status: "completed",
      completed_date: new Date("2025-10-26"),
      object_id: 1,
      user_id: 1,
      advice_id: 2,
      object: {
        id: 1,
        name: "Chaudière",
        category: "heating",
        owner_id: 1,
        created_at: new Date("2025-01-01"),
      },
    },
  ];

  beforeEach(async () => {
    const apiServiceSpy = jasmine.createSpyObj("ApiService", [
      "getMaintenanceTasks",
      "updateMaintenanceTask",
      "getObjects",
      "createMaintenanceTask",
    ]);

    await TestBed.configureTestingModule({
      imports: [MaintenanceComponent],
      providers: [{ provide: ApiService, useValue: apiServiceSpy }],
    }).compileComponents();

    fixture = TestBed.createComponent(MaintenanceComponent);
    component = fixture.componentInstance;
    apiService = TestBed.inject(ApiService) as jasmine.SpyObj<ApiService>;
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  describe("ngOnInit", () => {
    it("should load tasks on init", () => {
      apiService.getMaintenanceTasks.and.returnValue(of(mockTasks));

      component.ngOnInit();

      expect(apiService.getMaintenanceTasks).toHaveBeenCalled();
      expect(component.tasks).toEqual(mockTasks);
    });
  });

  describe("startTask", () => {
    it("should update task status to pending and add note", () => {
      const task = mockTasks[0];
      const updatedTask = {
        ...task,
        notes: "Tâche démarrée.",
      };
      apiService.updateMaintenanceTask.and.returnValue(of(updatedTask));
      component.tasks = [...mockTasks];

      component.startTask(task);

      expect(apiService.updateMaintenanceTask).toHaveBeenCalledWith(task.id, {
        status: "pending",
        notes: "Tâche démarrée.",
      });
    });

    it("should append note to existing notes", () => {
      const task = { ...mockTasks[0], notes: "Note existante" };
      const updatedTask = {
        ...task,
        notes: "Note existante\n[Tâche démarrée]",
      };
      apiService.updateMaintenanceTask.and.returnValue(of(updatedTask));
      component.tasks = [task];

      component.startTask(task);

      expect(apiService.updateMaintenanceTask).toHaveBeenCalledWith(task.id, {
        status: "pending",
        notes: "Note existante\n[Tâche démarrée]",
      });
    });
  });

  describe("completeTask", () => {
    it("should update task status to completed with completion date", () => {
      const task = mockTasks[0];
      const now = new Date();
      const updatedTask = {
        ...task,
        status: "completed" as const,
        completed_date: now,
        notes: "Tâche terminée.",
      };
      apiService.updateMaintenanceTask.and.returnValue(of(updatedTask));
      component.tasks = [...mockTasks];

      component.completeTask(task);

      const callArgs = apiService.updateMaintenanceTask.calls.argsFor(0);
      expect(callArgs[0]).toBe(task.id);
      expect(callArgs[1].status).toBe("completed");
      expect(callArgs[1].completed_date).toBeInstanceOf(Date);
      expect(callArgs[1].notes).toBe("Tâche terminée.");
    });

    it("should append completion note to existing notes", () => {
      const task = { ...mockTasks[0], notes: "Notes importantes" };
      const updatedTask = {
        ...task,
        status: "completed" as const,
        notes: "Notes importantes\n[Tâche terminée]",
      };
      apiService.updateMaintenanceTask.and.returnValue(of(updatedTask));
      component.tasks = [task];

      component.completeTask(task);

      const callArgs = apiService.updateMaintenanceTask.calls.argsFor(0);
      expect(callArgs[1].notes).toBe("Notes importantes\n[Tâche terminée]");
    });

    it("should update task in the list after completion", () => {
      const task = mockTasks[0];
      const updatedTask = {
        ...task,
        status: "completed" as const,
        completed_date: new Date(),
      };
      apiService.updateMaintenanceTask.and.returnValue(of(updatedTask));
      component.tasks = [...mockTasks];

      component.completeTask(task);

      expect(component.tasks[0].status).toBe("completed");
    });
  });

  describe("editTask", () => {
    it("should update task notes when user confirms", () => {
      const task = mockTasks[0];
      const newNotes = "Nouvelles notes";
      const updatedTask = { ...task, notes: newNotes };
      apiService.updateMaintenanceTask.and.returnValue(of(updatedTask));
      component.tasks = [...mockTasks];
      spyOn(window, "prompt").and.returnValue(newNotes);

      component.editTask(task);

      expect(window.prompt).toHaveBeenCalledWith(
        "Modifier les notes de la tâche :",
        task.notes || ""
      );
      expect(apiService.updateMaintenanceTask).toHaveBeenCalledWith(task.id, {
        notes: newNotes,
      });
    });

    it("should not update when user cancels", () => {
      const task = mockTasks[0];
      component.tasks = [...mockTasks];
      spyOn(window, "prompt").and.returnValue(null);

      component.editTask(task);

      expect(apiService.updateMaintenanceTask).not.toHaveBeenCalled();
    });
  });

  describe("updateTask error handling", () => {
    it("should handle update errors gracefully", () => {
      const task = mockTasks[0];
      const error = { message: "Network error" };
      apiService.updateMaintenanceTask.and.returnValue(throwError(() => error));
      component.tasks = [...mockTasks];
      spyOn(console, "error");
      spyOn(window, "alert");

      component.completeTask(task);

      expect(console.error).toHaveBeenCalledWith(
        "Erreur lors de la mise à jour de la tâche:",
        error
      );
      expect(window.alert).toHaveBeenCalledWith(
        "Une erreur est survenue lors de la mise à jour de la tâche."
      );
    });
  });

  describe("filteredTasks", () => {
    beforeEach(() => {
      component.tasks = mockTasks;
    });

    it('should return all tasks when filter is "all"', () => {
      component.activeFilter = "all";
      expect(component.filteredTasks.length).toBe(2);
    });

    it("should filter pending tasks", () => {
      component.activeFilter = "pending";
      const filtered = component.filteredTasks;
      expect(filtered.length).toBe(1);
      expect(filtered[0].status).toBe("pending");
    });

    it("should filter completed tasks", () => {
      component.activeFilter = "completed";
      const filtered = component.filteredTasks;
      expect(filtered.length).toBe(1);
      expect(filtered[0].status).toBe("completed");
    });
  });

  describe("countByStatus", () => {
    beforeEach(() => {
      component.tasks = mockTasks;
    });

    it("should count pending tasks correctly", () => {
      expect(component.countByStatus("pending")).toBe(1);
    });

    it("should count completed tasks correctly", () => {
      expect(component.countByStatus("completed")).toBe(1);
    });

    it("should return 0 for status with no tasks", () => {
      expect(component.countByStatus("skipped")).toBe(0);
    });
  });

  describe("helper methods", () => {
    it("should return correct status label", () => {
      expect(component.getStatusLabel("pending")).toBe("En attente");
      expect(component.getStatusLabel("completed")).toBe("Terminée");
      expect(component.getStatusLabel("skipped")).toBe("Ignorée");
      expect(component.getStatusLabel("issue_reported")).toBe(
        "Problème signalé"
      );
    });

    it("should return correct status icon", () => {
      expect(component.getStatusIcon("pending")).toBe("⏳");
      expect(component.getStatusIcon("completed")).toBe("✅");
      expect(component.getStatusIcon("skipped")).toBe("⏭️");
      expect(component.getStatusIcon("issue_reported")).toBe("⚠️");
    });

    it("should return correct badge type", () => {
      expect(component.getStatusBadgeType("pending")).toBe("warning");
      expect(component.getStatusBadgeType("completed")).toBe("success");
      expect(component.getStatusBadgeType("skipped")).toBe("info");
      expect(component.getStatusBadgeType("issue_reported")).toBe("error");
    });

    it("should format dates correctly", () => {
      const date = new Date("2025-10-25");
      const formatted = component.formatDate(date);
      expect(formatted).toBe("25/10/2025");
    });

    it("should format string dates correctly", () => {
      const formatted = component.formatDate("2025-10-25");
      expect(formatted).toBe("25/10/2025");
    });
  });

  describe("Create Task Form", () => {
    const mockObjects = [
      {
        id: 1,
        name: "Chaudière",
        category: "heating" as const,
        owner_id: 1,
        created_at: new Date("2025-01-01"),
      },
      {
        id: 2,
        name: "Lave-vaisselle",
        category: "appliance" as const,
        owner_id: 1,
        created_at: new Date("2025-01-01"),
      },
    ];

    beforeEach(() => {
      apiService.getMaintenanceTasks.and.returnValue(of(mockTasks));
      apiService.getObjects.and.returnValue(of(mockObjects));
    });

    it("should load objects on init", () => {
      component.ngOnInit();

      expect(apiService.getObjects).toHaveBeenCalled();
      expect(component.objects).toEqual(mockObjects);
    });

    it("should open create form when openCreateForm is called", () => {
      expect(component.showCreateForm).toBe(false);

      component.openCreateForm();

      expect(component.showCreateForm).toBe(true);
      expect(component.newTask.scheduled_date).toBeTruthy();
    });

    it("should close create form and reset when closeCreateForm is called", () => {
      component.showCreateForm = true;
      component.newTask.name = "Test task";
      component.newTask.object_id = 1;
      component.newTask.notes = "Test notes";

      component.closeCreateForm();

      expect(component.showCreateForm).toBe(false);
      expect(component.newTask.name).toBe("");
      expect(component.newTask.object_id).toBe(0);
      expect(component.newTask.notes).toBe("");
    });

    it("should create a new task successfully", () => {
      const newTaskData = {
        name: "Nouvelle tâche",
        object_id: 1,
        advice_id: 1,
        scheduled_date: "2025-11-01T10:00",
        notes: "Notes de test",
      };
      component.newTask = { ...newTaskData };

      const createdTask: MaintenanceTask = {
        id: 3,
        name: newTaskData.name,
        scheduled_date: new Date(newTaskData.scheduled_date),
        status: "pending",
        object_id: newTaskData.object_id,
        user_id: 1,
        advice_id: newTaskData.advice_id,
        notes: newTaskData.notes,
      };

      apiService.createMaintenanceTask.and.returnValue(of(createdTask));
      component.tasks = [...mockTasks];
      component.showCreateForm = true;

      component.createTask();

      expect(apiService.createMaintenanceTask).toHaveBeenCalled();
      expect(component.tasks.length).toBe(3);
      expect(component.showCreateForm).toBe(false);
    });

    it("should show alert if name is missing", () => {
      spyOn(window, "alert");
      component.newTask.name = "";

      component.createTask();

      expect(window.alert).toHaveBeenCalledWith(
        "Le nom de la tâche est obligatoire"
      );
      expect(apiService.createMaintenanceTask).not.toHaveBeenCalled();
    });

    it("should show alert if object_id is missing", () => {
      spyOn(window, "alert");
      component.newTask.name = "Test";
      component.newTask.object_id = 0;

      component.createTask();

      expect(window.alert).toHaveBeenCalledWith("Veuillez sélectionner un objet");
      expect(apiService.createMaintenanceTask).not.toHaveBeenCalled();
    });

    it("should show alert if scheduled_date is missing", () => {
      spyOn(window, "alert");
      component.newTask.name = "Test";
      component.newTask.object_id = 1;
      component.newTask.scheduled_date = "";

      component.createTask();

      expect(window.alert).toHaveBeenCalledWith("La date planifiée est obligatoire");
      expect(apiService.createMaintenanceTask).not.toHaveBeenCalled();
    });
  });
});
