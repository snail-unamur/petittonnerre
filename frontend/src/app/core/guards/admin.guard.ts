import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const adminGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  const currentUser = authService.getCurrentUserValue();
  
  // Vérifier si l'utilisateur est connecté ET est admin
  if (!currentUser) {
    // Pas connecté, redirection vers login
    router.navigate(['/auth/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }
  
  if (!authService.isAdmin()) {
    // Connecté mais pas admin, redirection vers dashboard
    router.navigate(['/dashboard']);
    return false;
  }
  
  return true;
};