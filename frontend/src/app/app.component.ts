import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  template: `
    <div class="app">
      <header>
        <nav>
          <h1>🔧 Petit Tonnerre</h1>
          <ul>
            <li><a routerLink="/dashboard" routerLinkActive="active">Dashboard</a></li>
            <li><a routerLink="/objects" routerLinkActive="active">Mes Objets</a></li>
            <li><a routerLink="/maintenance" routerLinkActive="active">Maintenance</a></li>
            <li><a routerLink="/community" routerLinkActive="active">Communauté</a></li>
          </ul>
        </nav>
      </header>
      <main>
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .app {
      min-height: 100vh;
    }
    
    header {
      background: #2c3e50;
      color: white;
      padding: 1rem 2rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    h1 {
      margin: 0;
      font-size: 1.5rem;
    }
    
    ul {
      display: flex;
      list-style: none;
      gap: 2rem;
      margin: 0;
    }
    
    a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      transition: background 0.3s;
    }
    
    a:hover, a.active {
      background: rgba(255,255,255,0.1);
    }
    
    main {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
  `]
})
export class AppComponent {
  title = 'Petit Tonnerre';
}
