import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const adminGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  
  // Vérification temporaire de l'authentification admin
  const isAdminAuthenticated = localStorage.getItem('tempAdminAuth') === 'true';
  
  if (!isAdminAuthenticated) {
    router.navigate(['/admin/auth']);
    return false;
  }
  
  return true;
};