import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

/**
 * Guard qui empêche les utilisateurs déjà connectés d'accéder aux pages login/register
 * Redirige vers le dashboard si l'utilisateur est connecté
 */
export const authenticatedGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // Si l'utilisateur est déjà connecté, rediriger vers le dashboard
  if (authService.isAuthenticated()) {
    router.navigate(['/dashboard']);
    return false;
  }

  // Sinon, autoriser l'accès à la page login/register
  return true;
};
