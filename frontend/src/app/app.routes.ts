import { Routes } from "@angular/router";
import { adminGuard } from "./core/guards/admin.guard";
import { authGuard } from "./core/guards/auth.guard";
import { authenticatedGuard } from "./core/guards/authenticated.guard";

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
        canActivate: [authenticatedGuard],
      },
      {
        path: "login",
        loadComponent: () =>
          import("./features/auth/login.component").then(
            (m) => m.LoginComponent
          ),
        canActivate: [authenticatedGuard],
      },
    ],
  },
  {
    path: "dashboard",
    loadComponent: () =>
      import("./features/dashboard/dashboard.component").then(
        (m) => m.DashboardComponent
      ),
    canActivate: [authGuard],
  },
  {
    path: "objects",
    loadComponent: () =>
      import("./features/objects/objects.component").then(
        (m) => m.ObjectsComponent
      ),
    canActivate: [authGuard],
  },
  {
    path: "maintenance",
    loadComponent: () =>
      import("./features/maintenance/maintenance.component").then(
        (m) => m.MaintenanceComponent
      ),
    canActivate: [authGuard],
  },
  {
    path: "community",
    loadComponent: () =>
      import("./features/community/community.component").then(
        (m) => m.CommunityComponent
      ),
    canActivate: [authGuard],
  },
  {
    path: "problems",
    loadComponent: () =>
      import("./features/problems/problems.component").then(
        (m) => m.ProblemsComponent
      ),
    canActivate: [authGuard],
  },
  {
    path: "admin",
    redirectTo: "/admin/dashboard",
    pathMatch: "full",
  },
  {
    path: "admin/dashboard",
    loadComponent: () =>
      import("./features/admin/admin-dashboard.component").then(
        (m) => m.AdminDashboardComponent
      ),
    canActivate: [adminGuard],
  },
];
