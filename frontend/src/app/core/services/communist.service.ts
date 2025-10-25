import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommunistService {
  private readonly STORAGE_KEY = 'communist-mode';
  private communistModeSubject = new BehaviorSubject<boolean>(this.getStoredMode());
  private audio: HTMLAudioElement | null = null;
  
  public communistMode$ = this.communistModeSubject.asObservable();

  constructor() {
    this.initAudio();
    const currentMode = this.communistModeSubject.value;
    this.applyCommunistMode(currentMode);
    
    // Si le mode communiste était déjà activé, jouer l'hymne
    if (currentMode) {
      this.handleAudio(true);
    }
  }

  /**
   * Initialize the audio element
   */
  private initAudio(): void {
    this.audio = new Audio('assets/audio/hymne-URSS.mp3');
    this.audio.loop = true;
    this.audio.volume = 1.0; // VOLUME MAXIMUM POUR LA RÉVOLUTION ! 🚩🔊
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
    this.handleAudio(enabled);
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
   * Handle audio playback based on communist mode
   */
  private handleAudio(enabled: boolean): void {
    if (!this.audio) return;

    if (enabled) {
      // Jouer l'hymne de l'URSS
      this.audio.play().catch(error => {
        console.warn('Impossible de jouer l\'hymne de l\'URSS:', error);
      });
    } else {
      // Arrêter l'hymne
      this.audio.pause();
      this.audio.currentTime = 0; // Remettre au début
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
