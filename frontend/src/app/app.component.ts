import { Component, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from './core/services/auth.service';

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
  isAuthenticated = false;
  username = '';
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  ngOnInit() {
    // Check authentication status
    const token = localStorage.getItem('token');
    this.isAuthenticated = !!token;
    
    if (this.isAuthenticated) {
      const user = localStorage.getItem('username');
      this.username = user || 'Utilisateur';
    }
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
    this.authService.logout();
    this.isAuthenticated = false;
    this.username = '';
    this.closeMenus();
    this.router.navigate(['/auth/login']);
  }
}
