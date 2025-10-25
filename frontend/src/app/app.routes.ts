import { Routes } from "@angular/router";

export const routes: Routes = [
  { path: "", redirectTo: "/auth/login", pathMatch: "full" },
  {
    path: "auth",
    children: [
      {
        path: "register",
        loadComponent: () =>
          import("./features/auth/register.component").then(
            (m) => m.RegisterComponent
          ),
      },
      {
        path: "login",
        loadComponent: () =>
          import("./features/auth/login.component").then(
            (m) => m.LoginComponent
          ),
      },
    ],
  },
  {
    path: "dashboard",
    loadComponent: () =>
      import("./features/dashboard/dashboard.component").then(
        (m) => m.DashboardComponent
      ),
  },
  {
    path: "objects",
    loadComponent: () =>
      import("./features/objects/objects.component").then(
        (m) => m.ObjectsComponent
      ),
  },
  {
    path: "maintenance",
    loadComponent: () =>
      import("./features/maintenance/maintenance.component").then(
        (m) => m.MaintenanceComponent
      ),
  },
  {
    path: "community",
    loadComponent: () =>
      import("./features/community/community.component").then(
        (m) => m.CommunityComponent
      ),
  },
  {
    path: "problems",
    loadComponent: () =>
      import("./features/problems/problems.component").then(
        (m) => m.ProblemsComponent
      ),
  },
];
