import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommunistService {
  private readonly STORAGE_KEY = 'communist-mode';
  private communistModeSubject = new BehaviorSubject<boolean>(this.getStoredMode());
  
  public communistMode$ = this.communistModeSubject.asObservable();

  constructor() {
    this.applyCommunistMode(this.communistModeSubject.value);
  }

  /**
   * Get the current communist mode state
   */
  isCommunistMode(): boolean {
    return this.communistModeSubject.value;
  }

  /**
   * Toggle communist mode on/off
   */
  toggleCommunistMode(): void {
    const newMode = !this.communistModeSubject.value;
    this.setCommunistMode(newMode);
  }

  /**
   * Set communist mode to a specific state
   */
  setCommunistMode(enabled: boolean): void {
    this.communistModeSubject.next(enabled);
    this.applyCommunistMode(enabled);
    this.storeMode(enabled);
  }

  /**
   * Apply communist mode to the document
   */
  private applyCommunistMode(enabled: boolean): void {
    const root = document.documentElement;
    
    if (enabled) {
      root.setAttribute('data-communist', 'true');
    } else {
      root.removeAttribute('data-communist');
    }
  }

  /**
   * Get mode from localStorage or default to 'false'
   */
  private getStoredMode(): boolean {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    return stored === 'true';
  }

  /**
   * Store mode preference in localStorage
   */
  private storeMode(enabled: boolean): void {
    localStorage.setItem(this.STORAGE_KEY, enabled.toString());
  }
}
