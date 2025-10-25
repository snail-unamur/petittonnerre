import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { authenticatedGuard } from './authenticated.guard';
import { AuthService } from '../services/auth.service';

describe('authenticatedGuard', () => {
  let authService: jasmine.SpyObj<AuthService>;
  let router: jasmine.SpyObj<Router>;

  beforeEach(() => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['isAuthenticated']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    });

    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
  });

  it('devrait permettre l\'accès si l\'utilisateur n\'est pas authentifié', () => {
    authService.isAuthenticated.and.returnValue(false);
    
    const result = TestBed.runInInjectionContext(() => authenticatedGuard());
    
    expect(result).toBe(true);
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('devrait rediriger vers /dashboard si l\'utilisateur est authentifié', () => {
    authService.isAuthenticated.and.returnValue(true);
    
    const result = TestBed.runInInjectionContext(() => authenticatedGuard());
    
    expect(result).toBe(false);
    expect(router.navigate).toHaveBeenCalledWith(['/dashboard']);
  });
});
