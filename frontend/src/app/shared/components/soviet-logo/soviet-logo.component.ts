import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-soviet-logo',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="soviet-logo">
      <div class="star">⭐</div>
      <div class="hammer-sickle">⚒️</div>
    </div>
  `,
  styles: [`
    .soviet-logo {
      position: relative;
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle, #FFD700 0%, #FFA500 100%);
      border-radius: 50%;
      box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
      animation: glow 2s ease-in-out infinite;
    }

    .star {
      position: absolute;
      font-size: 24px;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      animation: rotate 20s linear infinite;
    }

    .hammer-sickle {
      position: absolute;
      font-size: 14px;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1;
    }

    @keyframes glow {
      0%, 100% {
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
      }
      50% {
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.9), 0 0 30px rgba(255, 165, 0, 0.6);
      }
    }

    @keyframes rotate {
      from {
        transform: translate(-50%, -50%) rotate(0deg);
      }
      to {
        transform: translate(-50%, -50%) rotate(360deg);
      }
    }
  `]
})
export class SovietLogoComponent {}
