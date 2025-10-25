import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export type Theme = 'light' | 'dark';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private readonly STORAGE_KEY = 'theme';
  private themeSubject = new BehaviorSubject<Theme>(this.getStoredTheme());
  
  public theme$ = this.themeSubject.asObservable();

  constructor() {
    this.applyTheme(this.themeSubject.value);
  }

  /**
   * Get the currently active theme
   */
  getCurrentTheme(): Theme {
    return this.themeSubject.value;
  }

  /**
   * Toggle between light and dark theme
   */
  toggleTheme(): void {
    const newTheme: Theme = this.themeSubject.value === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
  }

  /**
   * Set a specific theme
   */
  setTheme(theme: Theme): void {
    this.themeSubject.next(theme);
    this.applyTheme(theme);
    this.storeTheme(theme);
  }

  /**
   * Apply theme to the document
   */
  private applyTheme(theme: Theme): void {
    const root = document.documentElement;
    
    if (theme === 'dark') {
      root.setAttribute('data-theme', 'dark');
    } else {
      root.removeAttribute('data-theme');
    }
  }

  /**
   * Get theme from localStorage or default to 'light'
   */
  private getStoredTheme(): Theme {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    return (stored === 'dark' || stored === 'light') ? stored : 'light';
  }

  /**
   * Store theme preference in localStorage
   */
  private storeTheme(theme: Theme): void {
    localStorage.setItem(this.STORAGE_KEY, theme);
  }
}
