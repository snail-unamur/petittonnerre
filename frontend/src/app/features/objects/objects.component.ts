import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ApiService } from "../../core/services/api.service";
import { ObjectItem } from "../../core/models/models";

@Component({
  selector: "app-objects",
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container">
      <div class="page-header">
        <div>
          <h1>📦 Mes Objets</h1>
          <p class="page-subtitle">
            Gérez tous vos équipements et objets à entretenir
          </p>
        </div>
        <button class="btn btn-primary" (click)="toggleAddForm()">
          <span>{{ showAddForm ? "✖️" : "➕" }}</span>
          {{ showAddForm ? "Annuler" : "Ajouter un objet" }}
        </button>
      </div>

      <!-- Add/Edit Form avec Recherche -->
      <div class="card mb-xl" *ngIf="showAddForm">
        <h3 class="mb-md">
          {{ editingObject ? "✏️ Modifier" : "➕ Ajouter un objet" }}
        </h3>

        <!-- Section de recherche d'objets existants (seulement en mode création) -->
        <div *ngIf="!editingObject" class="search-section mb-lg">
          <div class="alert alert-info mb-md">
            <strong>💡 Conseil :</strong> Avant de créer un nouvel objet,
            vérifiez s'il existe déjà dans la base de données. Cela permet de
            partager les informations et les maintenances avec d'autres
            utilisateurs.
          </div>

          <h4 class="mb-md">🔍 Rechercher un objet existant</h4>

          <div class="form-grid mb-md">
            <div class="form-group">
              <label for="search-name">Nom</label>
              <input
                type="text"
                id="search-name"
                [(ngModel)]="searchQuery.name"
                name="search-name"
                class="form-control"
                placeholder="Ex: Chaudière"
              />
            </div>

            <div class="form-group">
              <label for="search-category">Catégorie</label>
              <select
                id="search-category"
                [(ngModel)]="searchQuery.category"
                name="search-category"
                class="form-control"
              >
                <option value="">Toutes les catégories</option>
                <option value="heating">🔥 Chauffage</option>
                <option value="appliance">🏠 Électroménager</option>
                <option value="kitchen">🍳 Cuisine</option>
                <option value="bathroom">🚿 Salle de bain</option>
                <option value="flooring">🪨 Revêtement sol</option>
                <option value="other">📦 Autre</option>
              </select>
            </div>

            <div class="form-group">
              <label for="search-brand">Marque</label>
              <input
                type="text"
                id="search-brand"
                [(ngModel)]="searchQuery.brand"
                name="search-brand"
                class="form-control"
                placeholder="Ex: Vaillant"
              />
            </div>

            <div class="form-group">
              <label for="search-model">Modèle</label>
              <input
                type="text"
                id="search-model"
                [(ngModel)]="searchQuery.model"
                name="search-model"
                class="form-control"
                placeholder="Ex: ecoTEC"
              />
            </div>
          </div>

          <div class="flex gap-md">
            <button
              type="button"
              class="btn btn-primary"
              (click)="searchExistingObjects()"
              [disabled]="loading"
            >
              🔍 Rechercher
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              (click)="resetSearch()"
              *ngIf="showSearchResults"
            >
              ↺ Réinitialiser
            </button>
          </div>

          <!-- Résultats de recherche -->
          <div *ngIf="showSearchResults" class="search-results mt-lg">
            <!-- Message pour recherche sans résultats -->
            <div class="alert alert-info mb-md" *ngIf="searchMessage">
              {{ searchMessage }}
            </div>

            <h5 class="mb-md">
              {{ searchResults.length }} résultat(s) trouvé(s)
            </h5>

            <div class="grid grid-2 gap-md" *ngIf="searchResults.length > 0">
              <div class="card card-hover" *ngFor="let result of searchResults">
                <div class="flex flex-between items-start mb-sm">
                  <span class="badge badge-primary"
                    >{{ getCategoryIcon(result.category) }}
                    {{ getCategoryLabel(result.category) }}</span
                  >
                  <span
                    class="badge badge-success"
                    *ngIf="isObjectAlreadyLinked(result.id!)"
                    >✓ Déjà lié</span
                  >
                </div>

                <h4 class="mb-sm">{{ result.name }}</h4>

                <div class="text-sm text-secondary mb-md">
                  <div *ngIf="result.brand">🏷️ {{ result.brand }}</div>
                  <div *ngIf="result.model">📋 {{ result.model }}</div>
                </div>

                <button
                  class="btn btn-sm btn-primary full-width"
                  (click)="linkExistingObject(result.id!)"
                  [disabled]="loading || isObjectAlreadyLinked(result.id!)"
                >
                  {{
                    isObjectAlreadyLinked(result.id!)
                      ? "✓ Déjà dans mes objets"
                      : "➕ Ajouter à mes objets"
                  }}
                </button>
              </div>
            </div>

            <div class="divider my-lg"></div>

            <div class="text-center">
              <p class="text-secondary mb-md">
                Vous n'avez pas trouvé votre objet ?
              </p>
              <button
                type="button"
                class="btn btn-primary"
                (click)="showCreateFormSection()"
                *ngIf="!showCreateForm"
              >
                ✨ Créer un nouvel objet
              </button>
            </div>
          </div>
        </div>

        <!-- Formulaire de création/modification -->
        <form
          (ngSubmit)="saveObject()"
          class="form"
          *ngIf="editingObject || showCreateForm"
        >
          <h4 class="mb-md" *ngIf="!editingObject">✨ Créer un nouvel objet</h4>
          <div class="form-grid">
            <div class="form-group">
              <label for="name" class="required">Nom de l'objet</label>
              <input
                type="text"
                id="name"
                [(ngModel)]="formData.name"
                name="name"
                class="form-control"
                placeholder="Ex: Chaudière Vaillant"
                required
              />
            </div>

            <div class="form-group">
              <label for="category" class="required">Catégorie</label>
              <select
                id="category"
                [(ngModel)]="formData.category"
                name="category"
                class="form-control"
                required
              >
                <option [value]="undefined">Sélectionner une catégorie</option>
                <option value="heating">🔥 Chauffage</option>
                <option value="appliance">🏠 Électroménager</option>
                <option value="kitchen">🍳 Cuisine</option>
                <option value="bathroom">🚿 Salle de bain</option>
                <option value="flooring">🪨 Revêtement sol</option>
                <option value="other">📦 Autre</option>
              </select>
            </div>

            <div class="form-group">
              <label for="brand">Marque</label>
              <input
                type="text"
                id="brand"
                [(ngModel)]="formData.brand"
                name="brand"
                class="form-control"
                placeholder="Ex: Vaillant"
              />
            </div>

            <div class="form-group">
              <label for="model">Modèle</label>
              <input
                type="text"
                id="model"
                [(ngModel)]="formData.model"
                name="model"
                class="form-control"
                placeholder="Ex: ecoTEC plus"
              />
            </div>

            <div class="form-group full-width">
              <label for="notes">Notes</label>
              <textarea
                id="notes"
                [(ngModel)]="formData.notes"
                name="notes"
                class="form-control"
                rows="3"
                placeholder="Ajoutez des informations complémentaires..."
              ></textarea>
            </div>
          </div>

          <div class="form-actions">
            <button
              type="button"
              class="btn btn-secondary"
              (click)="cancelEdit()"
            >
              Annuler
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              [disabled]="!formData.name || !formData.category"
            >
              {{ editingObject ? "💾 Enregistrer" : "➕ Ajouter" }}
            </button>
          </div>

          <!-- Success Message after form submission -->
          <div class="alert alert-success mt-lg" *ngIf="successMessage">
            ✅ {{ successMessage }}
          </div>
        </form>
      </div>

      <!-- Loading -->
      <div class="text-center py-xl" *ngIf="loading">
        <div class="spinner"></div>
        <p class="text-secondary mt-md">Chargement...</p>
      </div>

      <!-- Error Message -->
      <div class="alert alert-error mb-lg" *ngIf="error">⚠️ {{ error }}</div>

      <!-- Search Bar for My Objects (US2.5) -->
      <div class="search-bar mb-lg" *ngIf="!loading && objects.length > 0">
        <div class="search-bar-content">
          <span class="search-icon">🔍</span>
          <input
            type="text"
            [(ngModel)]="myObjectsSearchTerm"
            (ngModelChange)="filterMyObjects()"
            placeholder="Rechercher dans mes objets (nom, marque, modèle, catégorie)..."
            class="search-input"
          />
          <button
            *ngIf="myObjectsSearchTerm"
            class="clear-search-btn"
            (click)="clearMyObjectsSearch()"
            title="Effacer la recherche"
          >
            ✖️
          </button>
        </div>
        <p class="search-results-count" *ngIf="myObjectsSearchTerm">
          {{ filteredObjects.length }} résultat(s) trouvé(s)
        </p>
      </div>

      <!-- Sort Options -->
      <div class="sort-bar mb-lg" *ngIf="!loading && objects.length > 0">
        <div class="sort-bar-content">
          <span class="sort-label">Trier par :</span>

          <div class="sort-buttons">
            <button
              *ngFor="let option of sortOptions"
              class="sort-btn"
              [class.active]="sortBy === option.value"
              (click)="changeSortBy(option.value)"
            >
              {{ option.label }}
            </button>
          </div>

          <button
            class="sort-order-toggle"
            (click)="toggleSortOrder()"
            [title]="sortOrder === 'asc' ? 'Tri croissant' : 'Tri décroissant'"
          >
            {{ sortOrder === "asc" ? "↑" : "↓" }}
          </button>
        </div>
      </div>

      <!-- Expand/Collapse All Categories Button -->
      <div class="category-controls mb-lg" *ngIf="!loading && objects.length > 0 && getCategories().length > 1">
        <button class="btn btn-sm btn-ghost" (click)="expandAllCategories()">
          📂 Tout ouvrir
        </button>
        <button class="btn btn-sm btn-ghost" (click)="collapseAllCategories()">
          📁 Tout fermer
        </button>
      </div>

      <!-- Objects Grouped by Category with Accordions (US2.6) -->
      <div class="objects-by-category" *ngIf="!loading && objects.length > 0">
        <div *ngFor="let category of getCategories()" class="category-section mb-lg">
          <div 
            class="category-header" 
            (click)="toggleCategory(category)"
            [class.expanded]="expandedCategories[category]"
          >
            <div class="category-title">
              <span class="category-icon">{{ categoryIcons[category] }}</span>
              <h3>{{ categoryLabels[category] }}</h3>
              <span class="category-count">({{ getCategoryCount(category) }})</span>
            </div>
            <span class="category-toggle">
              {{ expandedCategories[category] ? '▼' : '▶' }}
            </span>
          </div>

          <div class="category-content" *ngIf="expandedCategories[category]">
            <div class="grid grid-3">
              <div class="card" *ngFor="let obj of objectsByCategory[category]">
                <div class="flex flex-between items-start mb-md">
                  <span class="badge badge-primary"
                    >{{ getCategoryIcon(obj.category) }}
                    {{ getCategoryLabel(obj.category) }}</span
                  >
                  <div class="flex gap-xs">
                    <button
                      class="btn btn-sm btn-ghost"
                      (click)="editObject(obj)"
                      title="Modifier"
                    >
                      ✏️
                    </button>
                    <button
                      class="btn btn-sm btn-ghost text-error"
                      (click)="confirmDelete(obj)"
                      title="Supprimer"
                    >
                      🗑️
                    </button>
                  </div>
                </div>

                <h3 class="mb-sm">{{ obj.name }}</h3>

                <div class="divider"></div>

                <div class="flex flex-column gap-xs text-sm">
                  <div *ngIf="obj.brand" class="flex gap-sm items-center">
                    <span class="text-tertiary">🏷️ Marque:</span>
                    <span class="font-medium">{{ obj.brand }}</span>
                  </div>
                  <div *ngIf="obj.model" class="flex gap-sm items-center">
                    <span class="text-tertiary">📋 Modèle:</span>
                    <span class="font-medium">{{ obj.model }}</span>
                  </div>
                  <div *ngIf="obj.purchase_date" class="flex gap-sm items-center">
                    <span class="text-tertiary">📅 Achat:</span>
                    <span class="font-medium">{{
                      formatDate(obj.purchase_date)
                    }}</span>
                  </div>
                </div>

                <p
                  *ngIf="obj.notes"
                  class="text-sm text-secondary mt-md p-sm rounded-md"
                  style="background: var(--bg-tertiary);"
                >
                  💬 {{ obj.notes }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Load More Button (US2.6) -->
      <div class="text-center mb-xl" *ngIf="!loading && hasMoreObjects && objects.length > 0">
        <button 
          class="btn btn-secondary"
          (click)="loadMoreObjects()"
          [disabled]="loadingMore"
        >
          <span *ngIf="!loadingMore">📥 Charger plus d'objets</span>
          <span *ngIf="loadingMore">
            <span class="spinner-sm"></span> Chargement...
          </span>
        </button>
      </div>

      <!-- Empty State -->
      <div
        class="empty-state"
        *ngIf="!loading && objects.length === 0 && !showAddForm"
      >
        <div class="empty-icon">📦</div>
        <h3 class="empty-title">Aucun objet enregistré</h3>
        <p class="empty-description">
          Commencez par ajouter vos équipements et objets à entretenir pour
          suivre leur maintenance facilement.
        </p>
        <button class="btn btn-primary" (click)="toggleAddForm()">
          ➕ Ajouter mon premier objet
        </button>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-4 mt-xl" *ngIf="!loading && objects.length > 0">
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🔥</div>
            <div class="text-sm text-tertiary">Chauffage</div>
            <div class="text-xl font-bold">
              {{ countByCategory("heating") }}
            </div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🏠</div>
            <div class="text-sm text-tertiary">Électroménager</div>
            <div class="text-xl font-bold">
              {{ countByCategory("appliance") }}
            </div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">🍳</div>
            <div class="text-sm text-tertiary">Cuisine</div>
            <div class="text-xl font-bold">
              {{ countByCategory("kitchen") }}
            </div>
          </div>
        </div>
        <div class="card card-flat">
          <div class="text-center">
            <div class="text-2xl mb-sm">�</div>
            <div class="text-sm text-tertiary">Autres</div>
            <div class="text-xl font-bold">{{ countByCategory("other") }}</div>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div class="modal" *ngIf="objectToDelete" (click)="cancelDelete()">
        <div class="modal-content" (click)="$event.stopPropagation()">
          <h3 class="mb-md">� Retirer cet objet</h3>
          <p class="mb-lg">
            Êtes-vous sûr de vouloir retirer
            <strong>{{ objectToDelete.name }}</strong> de votre liste ?
          </p>
          <p class="text-sm text-secondary mb-lg">
            ℹ️ L'objet sera retiré de votre compte mais restera disponible dans
            la base de données pour les autres utilisateurs qui l'utilisent.
          </p>
          <div class="flex gap-md justify-end">
            <button class="btn btn-secondary" (click)="cancelDelete()">
              Annuler
            </button>
            <button class="btn btn-warning" (click)="deleteObject()">
              � Retirer de ma liste
            </button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        padding: var(--spacing-xl) 0;
      }

      .page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-xl);
      }

      .page-header .btn-primary {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        font-weight: 600;
      }

      .page-header .btn-primary:hover {
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
      }

      [data-theme="dark"] .page-header .btn-primary {
        box-shadow: 0 4px 12px rgba(139, 159, 248, 0.3);
      }

      [data-theme="dark"] .page-header .btn-primary:hover {
        box-shadow: 0 6px 16px rgba(139, 159, 248, 0.4);
      }

      .form-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: var(--spacing-md);
      }

      .form-group.full-width {
        grid-column: 1 / -1;
      }

      .form-actions {
        display: flex;
        gap: var(--spacing-md);
        justify-content: flex-end;
        margin-top: var(--spacing-lg);
        padding-top: var(--spacing-lg);
        border-top: 1px solid var(--border-color);
      }

      .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--border-color);
        border-top-color: var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto;
      }

      @keyframes spin {
        to {
          transform: rotate(360deg);
        }
      }

      .modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: var(--spacing-lg);
      }

      .modal-content {
        background: var(--bg-primary);
        padding: var(--spacing-xl);
        border-radius: var(--border-radius-lg);
        max-width: 500px;
        width: 100%;
        box-shadow: var(--shadow-lg);
      }

      .text-error {
        color: var(--error-color);
      }

      .btn-error {
        background: var(--error-color);
        color: white;
      }

      .btn-error:hover {
        opacity: 0.9;
      }

      .btn-warning {
        background: #ff9800;
        color: white;
      }

      .btn-warning:hover {
        background: #f57c00;
      }

      /* Nouveaux styles pour US2.1 */
      .search-section {
        background: var(--bg-secondary);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        border: 2px dashed var(--border-color);
      }

      .alert-info {
        background: #e3f2fd;
        color: #0d47a1;
        padding: var(--spacing-md);
        border-radius: var(--border-radius-md);
        border-left: 4px solid #2196f3;
      }

      .alert-success {
        background: #e8f5e9;
        color: #2e7d32;
        padding: var(--spacing-md);
        border-radius: var(--border-radius-md);
        border-left: 4px solid #4caf50;
      }

      .search-results {
        padding-top: var(--spacing-lg);
        border-top: 1px solid var(--border-color);
      }

      .card-hover {
        transition: transform 0.2s, box-shadow 0.2s;
      }

      .card-hover:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
      }

      .badge-success {
        background: #4caf50;
        color: white;
      }

      .full-width {
        width: 100%;
      }

      /* Styles pour la barre de recherche (US2.5) */
      .search-bar {
        background: var(--bg-secondary);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-md);
        border: 1px solid var(--border-color);
      }

      .search-bar-content {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
      }

      .search-icon {
        font-size: 1.25rem;
        color: var(--text-secondary);
      }

      .search-input {
        flex: 1;
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-md);
        font-size: 0.95rem;
        transition: border-color 0.2s;
      }

      .search-input:focus {
        outline: none;
        border-color: var(--primary-color);
      }

      .clear-search-btn {
        background: transparent;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        color: var(--text-secondary);
        padding: var(--spacing-xs);
        transition: color 0.2s;
      }

      .clear-search-btn:hover {
        color: var(--error-color);
      }

      .search-results-count {
        margin-top: var(--spacing-sm);
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
      }

      /* Styles pour la barre de tri */
      .sort-bar {
        background: var(--bg-secondary);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-md);
        border: 1px solid var(--border-color);
      }

      .sort-bar-content {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        flex-wrap: wrap;
      }

      .sort-label {
        font-weight: 500;
        color: var(--text-secondary);
        font-size: 0.875rem;
      }

      .sort-buttons {
        display: flex;
        gap: var(--spacing-xs);
        flex-wrap: wrap;
        flex: 1;
      }

      .sort-btn {
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--border-color);
        background: var(--bg-primary);
        border-radius: var(--border-radius-md);
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.875rem;
        color: var(--text-primary);
      }

      .sort-btn:hover {
        background: var(--bg-tertiary);
        border-color: var(--primary-color);
      }

      .sort-btn.active {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
        font-weight: 500;
      }

      .sort-order-toggle {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border: 1px solid var(--border-color);
        background: var(--bg-primary);
        border-radius: var(--border-radius-md);
        cursor: pointer;
        transition: all 0.2s;
        font-size: 1.25rem;
        font-weight: bold;
        color: var(--text-primary);
      }

      .sort-order-toggle:hover {
        background: var(--bg-tertiary);
        border-color: var(--primary-color);
      }

      @media (max-width: 767px) {
        .page-header {
          flex-direction: column;
          align-items: stretch;
        }

        .page-header button {
          width: 100%;
        }

        .form-grid {
          grid-template-columns: 1fr;
        }

        .grid-2 {
          grid-template-columns: 1fr !important;
        }

        .sort-bar-content {
          flex-direction: column;
          align-items: stretch;
          gap: var(--spacing-md);
        }

        .sort-buttons {
          justify-content: center;
        }

        .sort-btn {
          flex: 1;
          min-width: 80px;
          justify-content: center;
        }

        .sort-order-toggle {
          width: 100%;
        }
      }

      /* Styles pour les contrôles d'accordéons */
      .category-controls {
        display: flex;
        gap: var(--spacing-sm);
        justify-content: flex-end;
        align-items: center;
      }

      .category-controls .btn {
        font-size: 0.875rem;
      }

      /* Styles pour les accordéons de catégories (US2.6) */
      .objects-by-category {
        margin-top: var(--spacing-xl);
      }

      .category-section {
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-lg);
        overflow: hidden;
        background: var(--bg-secondary);
      }

      .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-lg);
        background: var(--bg-primary);
        cursor: pointer;
        transition: all 0.2s;
        border-bottom: 1px solid var(--border-color);
      }

      .category-header:hover {
        background: var(--bg-tertiary);
      }

      .category-header.expanded {
        background: var(--bg-tertiary);
        border-bottom-color: var(--primary-color);
      }

      .category-title {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
      }

      .category-icon {
        font-size: 1.5rem;
      }

      .category-title h3 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
      }

      .category-count {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
      }

      .category-toggle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        transition: transform 0.2s;
      }

      .category-content {
        padding: var(--spacing-lg);
        animation: slideDown 0.3s ease-out;
      }

      @keyframes slideDown {
        from {
          opacity: 0;
          transform: translateY(-10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      /* Spinner petit pour le bouton "Charger plus" */
      .spinner-sm {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid var(--border-color);
        border-top-color: currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        vertical-align: middle;
        margin-right: var(--spacing-xs);
      }
    `,
  ],
})
export class ObjectsComponent implements OnInit {
  objects: ObjectItem[] = [];
  sortedObjects: ObjectItem[] = [];
  filteredObjects: ObjectItem[] = []; // Pour US2.5 : objets après filtrage
  showAddForm = false;
  showSearchResults = false;
  showCreateForm = false; // Nouvelle variable pour US2.2
  searchResults: ObjectItem[] = [];
  searchQuery = {
    name: "",
    category: "",
    brand: "",
    model: "",
  };
  myObjectsSearchTerm = ""; // Pour US2.5 : terme de recherche dans mes objets
  loading = false;
  loadingMore = false; // Pour le lazy loading
  error = "";
  successMessage = "";
  searchMessage = ""; // Message spécifique pour les résultats de recherche

  // Pagination et lazy loading (US2.6)
  currentPage = 0;
  pageSize = 30;
  hasMoreObjects = true;
  objectsByCategory: { [key: string]: ObjectItem[] } = {};
  expandedCategories: { [key: string]: boolean } = {};
  categoryIcons: { [key: string]: string } = {
    heating: "🔥",
    appliance: "🏠",
    kitchen: "🍳",
    bathroom: "🚿",
    flooring: "🪨",
    other: "📦"
  };
  categoryLabels: { [key: string]: string } = {
    heating: "Chauffage",
    appliance: "Électroménager",
    kitchen: "Cuisine",
    bathroom: "Salle de bain",
    flooring: "Revêtement sol",
    other: "Autre"
  };

  // Tri
  sortBy: "name" | "added_at" | "purchase_date" | "brand" | "model" = "name";
  sortOrder: "asc" | "desc" = "asc";
  sortOptions = [
    { value: "name" as const, label: "Nom" },
    { value: "added_at" as const, label: "Ajout" },
    { value: "purchase_date" as const, label: "Achat" },
    { value: "brand" as const, label: "Marque" },
    { value: "model" as const, label: "Modèle" },
  ];

  // Pour le moment, userId est hardcodé à 1 (en attendant l'authentification)
  currentUserId = 1;

  // Formulaire
  formData: Partial<ObjectItem> = {
    name: "",
    category: undefined,
    brand: "",
    model: "",
    notes: "",
  };

  editingObject: ObjectItem | null = null;
  objectToDelete: ObjectItem | null = null;

  constructor(private readonly apiService: ApiService) {}

  ngOnInit() {
    this.loadObjects();
    // Initialiser toutes les catégories comme fermées
    for (const cat of Object.keys(this.categoryLabels)) {
      this.expandedCategories[cat] = false;
    }
  }

  loadObjects(append = false) {
    if (append) {
      this.loadingMore = true;
    } else {
      this.loading = true;
      this.currentPage = 0;
      this.objects = [];
      this.objectsByCategory = {};
    }
    
    this.error = "";
    const skip = this.currentPage * this.pageSize;

    this.apiService.getObjects(this.currentUserId, skip, this.pageSize).subscribe({
      next: (data) => {
        if (append) {
          this.objects = [...this.objects, ...data];
        } else {
          this.objects = data;
        }
        
        // Vérifier s'il y a plus d'objets à charger
        this.hasMoreObjects = data.length === this.pageSize;
        
        this.currentPage++;
        this.sortObjects();
        this.filterMyObjects(); // Appliquer le filtre après le chargement
        this.groupObjectsByCategory();
        this.loading = false;
        this.loadingMore = false;
      },
      error: (err: any) => {
        console.error("Erreur lors du chargement des objets:", err);
        this.error = "Impossible de charger les objets. Veuillez réessayer.";
        this.loading = false;
        this.loadingMore = false;
      },
    });
  }

  loadMoreObjects() {
    if (!this.loadingMore && this.hasMoreObjects) {
      this.loadObjects(true);
    }
  }

  groupObjectsByCategory() {
    this.objectsByCategory = {};
    
    for (const obj of this.filteredObjects) {
      const category = obj.category || 'other';
      if (!this.objectsByCategory[category]) {
        this.objectsByCategory[category] = [];
      }
      this.objectsByCategory[category].push(obj);
    }
  }

  toggleCategory(category: string) {
    this.expandedCategories[category] = !this.expandedCategories[category];
  }

  expandAllCategories() {
    for (const category of this.getCategories()) {
      this.expandedCategories[category] = true;
    }
  }

  collapseAllCategories() {
    for (const category of this.getCategories()) {
      this.expandedCategories[category] = false;
    }
  }

  getCategoryCount(category: string): number {
    return this.objectsByCategory[category]?.length || 0;
  }

  getCategories(): string[] {
    return Object.keys(this.objectsByCategory).sort((a, b) => a.localeCompare(b));
  }

  toggleAddForm() {
    this.showAddForm = !this.showAddForm;
    if (!this.showAddForm) {
      this.cancelEdit();
      this.showCreateForm = false; // Réinitialiser aussi showCreateForm
    }
  }

  editObject(obj: ObjectItem) {
    this.editingObject = obj;
    this.formData = {
      name: obj.name,
      category: obj.category,
      brand: obj.brand || "",
      model: obj.model || "",
      notes: obj.notes || "",
    };
    this.showAddForm = true;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  cancelEdit() {
    this.showAddForm = false;
    this.editingObject = null;
    this.showCreateForm = false; // Réinitialiser showCreateForm
    this.formData = {
      name: "",
      category: undefined,
      brand: "",
      model: "",
      notes: "",
    };
  }

  saveObject() {
    if (!this.formData.name || !this.formData.category) {
      return;
    }

    this.loading = true;
    this.error = "";

    if (this.editingObject) {
      this.apiService
        .updateObject(this.editingObject.id, this.formData)
        .subscribe({
          next: (updated) => {
            const index = this.objects.findIndex((o) => o.id === updated.id);
            if (index !== -1) {
              this.objects[index] = updated;
            }
            this.sortObjects();
            this.cancelEdit();
            this.loading = false;
          },
          error: (err: any) => {
            console.error("Erreur lors de la mise à jour:", err);
            this.error = "Impossible de mettre à jour l'objet.";
            this.loading = false;
          },
        });
    } else {
      // US2.3: Créer une demande d'objet au lieu de créer directement
      this.apiService
        .createObjectRequest(this.formData, this.currentUserId)
        .subscribe({
          next: (request) => {
            this.successMessage =
              "Votre demande de création d'objet a été envoyée avec succès ! Elle sera examinée par un administrateur.";
            this.loading = false;

            // Masquer le message et fermer le formulaire après 8 secondes
            setTimeout(() => {
              this.successMessage = "";
              this.cancelEdit();
            }, 8000);
          },
          error: (err: any) => {
            console.error("Erreur lors de la création de la demande:", err);
            this.error =
              "Impossible d'envoyer votre demande. Veuillez réessayer.";
            this.loading = false;
          },
        });
    }
  }

  confirmDelete(obj: ObjectItem) {
    this.objectToDelete = obj;
  }

  cancelDelete() {
    this.objectToDelete = null;
  }

  deleteObject() {
    if (!this.objectToDelete) return;

    this.loading = true;
    this.error = "";

    this.apiService
      .deleteObject(this.objectToDelete.id, this.currentUserId)
      .subscribe({
        next: () => {
          this.objects = this.objects.filter(
            (o) => o.id !== this.objectToDelete!.id
          );
          this.sortObjects(); // Mettre à jour aussi sortedObjects
          this.cancelDelete();
          this.loading = false;
        },
        error: (err: any) => {
          console.error("Erreur lors de la suppression:", err);
          this.error = "Impossible de supprimer l'objet.";
          this.cancelDelete();
          this.loading = false;
        },
      });
  }

  getCategoryLabel(category: string): string {
    const labels: Record<string, string> = {
      heating: "Chauffage",
      appliance: "Électroménager",
      kitchen: "Cuisine",
      bathroom: "Salle de bain",
      flooring: "Revêtement sol",
      other: "Autre",
    };
    return labels[category] || category;
  }

  getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
      heating: "🔥",
      appliance: "🏠",
      kitchen: "🍳",
      bathroom: "�",
      flooring: "🪨",
      other: "📦",
    };
    return icons[category] || "📦";
  }

  formatDate(date: Date | string | undefined): string {
    if (!date) return "N/A";
    const dateObj = typeof date === "string" ? new Date(date) : date;
    return dateObj.toLocaleDateString("fr-FR");
  }

  countByCategory(category: string): number {
    return this.objects.filter((obj) => obj.category === category).length;
  }

  // ===== NOUVELLES MÉTHODES POUR US2.1 =====

  searchExistingObjects() {
    if (
      !this.searchQuery.name &&
      !this.searchQuery.category &&
      !this.searchQuery.brand &&
      !this.searchQuery.model
    ) {
      this.error = "Veuillez remplir au moins un critère de recherche";
      return;
    }

    this.loading = true;
    this.error = "";
    this.successMessage = "";
    this.searchMessage = ""; // Réinitialiser le message de recherche

    this.apiService
      .searchObjects(
        this.searchQuery.name || undefined,
        this.searchQuery.category || undefined,
        this.searchQuery.brand || undefined,
        this.searchQuery.model || undefined
      )
      .subscribe({
        next: (results) => {
          this.searchResults = results;
          this.showSearchResults = true;
          this.showCreateForm = false; // Cacher le formulaire de création jusqu'à ce que l'utilisateur clique
          this.loading = false;

          if (results.length === 0) {
            this.searchMessage =
              "Aucun objet trouvé correspondant à vos critères. Vous pouvez créer un nouvel objet en cliquant sur le bouton ci-dessous.";
          } else {
            this.searchMessage = ""; // Réinitialiser le message s'il y a des résultats
          }
        },
        error: (err) => {
          console.error("Erreur lors de la recherche:", err);
          this.error =
            "Impossible d'effectuer la recherche. Veuillez réessayer.";
          this.loading = false;
        },
      });
  }

  linkExistingObject(objectId: number) {
    this.loading = true;
    this.error = "";
    this.successMessage = "";

    this.apiService.linkObjectToUser(objectId, this.currentUserId).subscribe({
      next: (linkedObject) => {
        this.objects.push(linkedObject);
        this.sortObjects();
        this.successMessage = `L'objet "${linkedObject.name}" a été ajouté à votre compte avec succès !`;
        this.resetSearch();
        this.showAddForm = false;
        this.showCreateForm = false; // Réinitialiser aussi le formulaire de création

        // Faire défiler vers le haut pour voir le message de succès
        window.scrollTo({ top: 0, behavior: "smooth" });
        this.loading = false;

        // Cacher le message après 5 secondes
        setTimeout(() => {
          this.successMessage = "";
        }, 5000);
      },
      error: (err) => {
        console.error("Erreur lors du lien de l'objet:", err);
        this.error =
          err.error?.detail ||
          "Impossible de lier l'objet à votre compte. Veuillez réessayer.";
        this.loading = false;
      },
    });
  }

  resetSearch() {
    this.searchQuery = {
      name: "",
      category: "",
      brand: "",
      model: "",
    };
    this.searchResults = [];
    this.showSearchResults = false;
    this.showCreateForm = false; // Masquer le formulaire de création aussi
    this.searchMessage = ""; // Réinitialiser le message de recherche
  }

  showCreateFormSection() {
    this.showCreateForm = true;
    this.searchMessage = ""; // Cacher le message de recherche quand on montre le formulaire
    // Faire défiler vers le formulaire de création
    setTimeout(() => {
      const formElement = document.querySelector("form.form");
      if (formElement) {
        formElement.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 100);
  }

  isObjectAlreadyLinked(objectId: number): boolean {
    return this.objects.some((obj) => obj.id === objectId);
  }

  // ===== MÉTHODES DE TRI =====

  sortObjects() {
    this.sortedObjects = [...this.objects].sort((a, b) => {
      let compareValue = 0;

      switch (this.sortBy) {
        case "name":
          compareValue = (a.name || "").localeCompare(b.name || "");
          break;
        case "brand":
          compareValue = (a.brand || "").localeCompare(b.brand || "");
          break;
        case "model":
          compareValue = (a.model || "").localeCompare(b.model || "");
          break;
        case "added_at": {
          const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
          const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
          compareValue = dateB - dateA; // Plus récent en premier par défaut
          break;
        }
        case "purchase_date": {
          const purchaseA = a.purchase_date
            ? new Date(a.purchase_date).getTime()
            : 0;
          const purchaseB = b.purchase_date
            ? new Date(b.purchase_date).getTime()
            : 0;
          compareValue = purchaseB - purchaseA; // Plus récent en premier par défaut
          break;
        }
      }

      return this.sortOrder === "asc" ? compareValue : -compareValue;
    });

    // Appliquer le filtre après le tri
    this.filterMyObjects();
  }

  toggleSortOrder() {
    this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
    this.sortObjects();
  }

  changeSortBy(
    sortBy: "name" | "added_at" | "purchase_date" | "brand" | "model"
  ) {
    this.sortBy = sortBy;
    this.sortObjects();
  }

  // ===== MÉTHODES DE RECHERCHE DANS MES OBJETS (US2.5) =====

  filterMyObjects() {
    if (this.myObjectsSearchTerm.trim()) {
      const searchLower = this.myObjectsSearchTerm.toLowerCase().trim();
      this.filteredObjects = this.sortedObjects.filter((obj) => {
        const nameMatch = obj.name?.toLowerCase().includes(searchLower);
        const brandMatch = obj.brand?.toLowerCase().includes(searchLower);
        const modelMatch = obj.model?.toLowerCase().includes(searchLower);
        const categoryMatch = this.getCategoryLabel(obj.category)
          .toLowerCase()
          .includes(searchLower);

        return nameMatch || brandMatch || modelMatch || categoryMatch;
      });
    } else {
      // Si pas de recherche, afficher tous les objets triés
      this.filteredObjects = [...this.sortedObjects];
    }
    
    // Regrouper les objets filtrés par catégorie (US2.6)
    this.groupObjectsByCategory();
  }

  clearMyObjectsSearch() {
    this.myObjectsSearchTerm = "";
    this.filterMyObjects();
  }
}
