import { Component, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router, NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService, UserResponse } from './core/services/auth.service';
import { filter } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'Petit Tonnerre';
  isMenuOpen = false;
  isUserMenuOpen = false;
  currentUser$: Observable<UserResponse | null>;
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {
    this.currentUser$ = this.authService.currentUser$;
  }
  
  ngOnInit() {
    // Fermer les menus lors de la navigation
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.closeMenus();
    });
  }
  
  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
    if (this.isMenuOpen) {
      this.isUserMenuOpen = false;
    }
  }
  
  closeMenu() {
    this.isMenuOpen = false;
  }
  
  toggleUserMenu() {
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }
  
  closeMenus() {
    this.isMenuOpen = false;
    this.isUserMenuOpen = false;
  }
  
  logout() {
    this.authService.logout().subscribe({
      next: () => {
        this.closeMenus();
        this.router.navigate(['/auth/login']);
      },
      error: () => {
        // Même en cas d'erreur, déconnecter localement
        this.closeMenus();
        this.router.navigate(['/auth/login']);
      }
    });
  }
}
