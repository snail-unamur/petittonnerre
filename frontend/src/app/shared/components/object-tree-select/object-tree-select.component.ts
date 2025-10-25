import { Component, Input, Output, EventEmitter, OnInit, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';
import { ObjectItem } from '../../../core/models/models';

interface CategoryGroup {
  label: string;
  key: string;
  icon: string;
  objects: ObjectItem[];
  expanded: boolean;
}

@Component({
  selector: 'app-object-tree-select',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './object-tree-select.component.html',
  styleUrls: ['./object-tree-select.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => ObjectTreeSelectComponent),
      multi: true
    }
  ]
})
export class ObjectTreeSelectComponent implements OnInit, ControlValueAccessor {
  @Input() objects: ObjectItem[] = [];
  @Input() placeholder: string = 'Sélectionnez un objet';
  @Output() selectionChange = new EventEmitter<number | null>();

  searchText: string = '';
  isOpen: boolean = false;
  selectedObjectId: number | null = null;
  selectedObjectName: string = '';

  categoryGroups: CategoryGroup[] = [];

  // Labels pour les catégories
  categoryLabels: { [key: string]: { label: string; icon: string } } = {
    'heating': { label: 'Chauffage', icon: '🔥' },
    'appliance': { label: 'Électroménager', icon: '⚡' },
    'kitchen': { label: 'Cuisine', icon: '🍳' },
    'bathroom': { label: 'Salle de bain', icon: '🚿' },
    'flooring': { label: 'Revêtement de sol', icon: '🪵' },
    'other': { label: 'Autre', icon: '📦' }
  };

  private onChange: any = () => {};
  private onTouched: any = () => {};

  ngOnInit() {
    this.organizeObjectsByCategory();
  }

  ngOnChanges() {
    this.organizeObjectsByCategory();
  }

  organizeObjectsByCategory() {
    const categories = ['heating', 'appliance', 'kitchen', 'bathroom', 'flooring', 'other'];
    this.categoryGroups = categories.map(cat => ({
      label: this.categoryLabels[cat]?.label || cat,
      key: cat,
      icon: this.categoryLabels[cat]?.icon || '📦',
      objects: this.objects.filter(obj => obj.category === cat),
      expanded: false
    })).filter(group => group.objects.length > 0);
  }

  get filteredGroups(): CategoryGroup[] {
    if (!this.searchText.trim()) {
      return this.categoryGroups;
    }

    const search = this.searchText.toLowerCase();
    return this.categoryGroups
      .map(group => ({
        ...group,
        objects: group.objects.filter(obj =>
          obj.name.toLowerCase().includes(search) ||
          (obj.brand && obj.brand.toLowerCase().includes(search)) ||
          (obj.model && obj.model.toLowerCase().includes(search))
        ),
        expanded: true // Auto-expand lors de la recherche
      }))
      .filter(group => group.objects.length > 0);
  }

  toggleDropdown() {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      this.onTouched();
    }
  }

  toggleCategory(group: CategoryGroup) {
    group.expanded = !group.expanded;
  }

  selectObject(obj: ObjectItem) {
    this.selectedObjectId = obj.id;
    this.selectedObjectName = obj.name;
    this.isOpen = false;
    this.searchText = '';
    this.onChange(obj.id);
    this.selectionChange.emit(obj.id);
  }

  clearSelection(event: Event) {
    event.stopPropagation();
    this.selectedObjectId = null;
    this.selectedObjectName = '';
    this.onChange(null);
    this.selectionChange.emit(null);
  }

  // ControlValueAccessor implementation
  writeValue(value: number | null): void {
    this.selectedObjectId = value;
    if (value) {
      const obj = this.objects.find(o => o.id === value);
      if (obj) {
        this.selectedObjectName = obj.name;
      }
    } else {
      this.selectedObjectName = '';
    }
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    // Implement if needed
  }
}
