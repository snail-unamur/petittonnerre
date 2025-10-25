import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-community',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container">
      <div class="page-header">
        <div>
          <h1>👥 Communauté</h1>
          <p class="page-subtitle">Partagez vos expériences et découvrez les conseils de la communauté</p>
        </div>
      </div>

      <!-- Community Stats -->
      <div class="grid grid-4 mb-xl">
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-label">Membres</div>
          <div class="stat-value">1,234</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💬</div>
          <div class="stat-label">Discussions</div>
          <div class="stat-value">456</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💡</div>
          <div class="stat-label">Astuces</div>
          <div class="stat-value">789</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-label">Expertises</div>
          <div class="stat-value">234</div>
        </div>
      </div>

      <!-- Trending Topics -->
      <div class="card mb-xl">
        <div class="card-header">
          <h3>🔥 Sujets Tendances</h3>
          <p class="card-subtitle">Les discussions les plus populaires</p>
        </div>
        <div class="card-body">
          <div class="list">
            <div class="list-item" *ngFor="let topic of trendingTopics">
              <div class="list-item-icon">{{ topic.icon }}</div>
              <div class="list-item-content">
                <div class="list-item-title">
                  {{ topic.title }}
                  <span class="badge badge-primary">{{ topic.replies }} réponses</span>
                </div>
                <div class="list-item-subtitle">
                  Par {{ topic.author }} • {{ topic.date }}
                </div>
              </div>
              <button class="btn btn-sm btn-ghost">Voir →</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Categories -->
      <h3 class="mb-lg">📂 Catégories</h3>
      <div class="grid grid-3 mb-xl">
        <div class="card card-flat" *ngFor="let category of categories">
          <div class="flex gap-md items-start">
            <div class="text-3xl">{{ category.icon }}</div>
            <div class="flex-1">
              <h4 class="mb-xs">{{ category.name }}</h4>
              <p class="text-sm text-tertiary mb-sm">{{ category.description }}</p>
              <div class="flex gap-sm text-xs">
                <span class="badge badge-info">{{ category.topics }} sujets</span>
                <span class="badge badge-success">{{ category.posts }} posts</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card">
        <div class="card-header">
          <h3>⚡ Activité Récente</h3>
          <p class="card-subtitle">Dernières contributions de la communauté</p>
        </div>
        <div class="card-body">
          <div class="empty-state">
            <div class="empty-icon">🌟</div>
            <h4 class="empty-title">Fonctionnalité à venir</h4>
            <p class="empty-description">
              La section communauté sera bientôt disponible! Vous pourrez échanger des astuces, poser des questions et partager vos expériences.
            </p>
            <button class="btn btn-primary">
              📧 M'avertir du lancement
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="alert alert-info mt-xl">
        <div class="alert-icon">💡</div>
        <div class="alert-content">
          <div class="alert-title">Envie de contribuer?</div>
          Partagez vos connaissances et aidez la communauté à grandir!
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      padding: var(--spacing-xl) 0;
    }
  `]
})
export class CommunityComponent implements OnInit {
  trendingTopics = [
    {
      icon: '🔧',
      title: 'Comment entretenir sa chaudière?',
      author: 'Jean Dupont',
      date: 'Il y a 2 heures',
      replies: 12
    },
    {
      icon: '🚗',
      title: 'Meilleurs moments pour vidanger sa voiture',
      author: 'Marie Martin',
      date: 'Il y a 5 heures',
      replies: 8
    },
    {
      icon: '💻',
      title: 'Nettoyage d\'ordinateur: les bonnes pratiques',
      author: 'Pierre Bernard',
      date: 'Hier',
      replies: 15
    }
  ];

  categories = [
    {
      icon: '🏠',
      name: 'Maison & Jardin',
      description: 'Entretien de la maison, jardinage, bricolage',
      topics: 123,
      posts: 456
    },
    {
      icon: '🚗',
      name: 'Automobile',
      description: 'Entretien véhicules, mécanique, conseils',
      topics: 89,
      posts: 234
    },
    {
      icon: '💻',
      name: 'Électronique',
      description: 'Informatique, électroménager, gadgets',
      topics: 67,
      posts: 189
    },
    {
      icon: '🛠️',
      name: 'Bricolage & DIY',
      description: 'Projets DIY, réparations, tutoriels',
      topics: 45,
      posts: 123
    },
    {
      icon: '💡',
      name: 'Astuces & Conseils',
      description: 'Trucs et astuces, économies, optimisation',
      topics: 78,
      posts: 267
    },
    {
      icon: '❓',
      name: 'Questions Générales',
      description: 'Questions diverses, aide, support',
      topics: 92,
      posts: 345
    }
  ];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    // Future implementation
  }
}
