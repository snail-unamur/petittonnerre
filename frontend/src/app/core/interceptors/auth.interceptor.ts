import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Accéder directement au token sans injecter AuthService pour éviter la dépendance circulaire
  const token = localStorage.getItem('token');
  
  // Ajouter le token si présent et si la requête va vers notre backend
  // (localhost:8000 ou toute URL contenant /api/ ou /auth/)
  if (token && (req.url.includes('localhost:8000') || req.url.includes('/api/') || req.url.includes('/auth/'))) {
    const clonedRequest = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(clonedRequest);
  }
  
  return next(req);
};

