import { Component, Input, Output, EventEmitter, forwardRef, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';

@Component({
  selector: 'app-date-time-picker',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './date-time-picker.component.html',
  styleUrls: ['./date-time-picker.component.scss'],
  encapsulation: ViewEncapsulation.None,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DateTimePickerComponent),
      multi: true
    }
  ]
})
export class DateTimePickerComponent implements OnInit, ControlValueAccessor {
  @Input() placeholder: string = 'Sélectionnez une date';
  @Input() minDate?: Date;
  @Input() maxDate?: Date;
  @Output() dateChange = new EventEmitter<Date | null>();

  isOpen: boolean = false;
  selectedDate: Date | null = null;
  
  // Calendar state
  currentMonth: Date = new Date();
  selectedDay: number | null = null;
  selectedHour: number = 9;
  selectedMinute: number = 0;

  // Arrays for time selection
  hours: number[] = Array.from({ length: 24 }, (_, i) => i);
  minutes: number[] = Array.from({ length: 60 }, (_, i) => i);

  weekDays: string[] = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
  months: string[] = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ];

  private onChange: any = () => {};
  private onTouched: any = () => {};

  ngOnInit() {
    if (this.selectedDate) {
      this.currentMonth = new Date(this.selectedDate);
      this.selectedDay = this.selectedDate.getDate();
      this.selectedHour = this.selectedDate.getHours();
      this.selectedMinute = this.selectedDate.getMinutes();
    }
  }

  get formattedDate(): string {
    if (!this.selectedDate) return '';
    
    const day = this.selectedDate.getDate().toString().padStart(2, '0');
    const month = (this.selectedDate.getMonth() + 1).toString().padStart(2, '0');
    const year = this.selectedDate.getFullYear();
    const hours = this.selectedDate.getHours().toString().padStart(2, '0');
    const minutes = this.selectedDate.getMinutes().toString().padStart(2, '0');
    
    return `${day}/${month}/${year} à ${hours}:${minutes}`;
  }

  get calendarDays(): (number | null)[] {
    const year = this.currentMonth.getFullYear();
    const month = this.currentMonth.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    // Adjust for Monday start (0 = Sunday, we want 0 = Monday)
    let firstDayOfWeek = firstDay.getDay() - 1;
    if (firstDayOfWeek < 0) firstDayOfWeek = 6;
    
    const days: (number | null)[] = [];
    
    // Add empty cells for days before month starts
    for (let i = 0; i < firstDayOfWeek; i++) {
      days.push(null);
    }
    
    // Add all days of the month
    for (let day = 1; day <= lastDay.getDate(); day++) {
      days.push(day);
    }
    
    return days;
  }

  togglePicker() {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      this.onTouched();
    }
  }

  previousMonth() {
    this.currentMonth = new Date(
      this.currentMonth.getFullYear(),
      this.currentMonth.getMonth() - 1,
      1
    );
  }

  nextMonth() {
    this.currentMonth = new Date(
      this.currentMonth.getFullYear(),
      this.currentMonth.getMonth() + 1,
      1
    );
  }

  selectDay(day: number | null) {
    if (day === null) return;
    
    // Empêcher la sélection de jours passés
    if (this.isPastDay(day)) return;
    
    this.selectedDay = day;
    const newDate = new Date(
      this.currentMonth.getFullYear(),
      this.currentMonth.getMonth(),
      day,
      this.selectedHour,
      this.selectedMinute
    );
    
    this.updateDate(newDate);
  }

  selectHour(hour: number) {
    this.selectedHour = hour;
    if (this.selectedDay) {
      const newDate = new Date(
        this.currentMonth.getFullYear(),
        this.currentMonth.getMonth(),
        this.selectedDay,
        hour,
        this.selectedMinute
      );
      this.updateDate(newDate);
    }
  }

  selectMinute(minute: number) {
    this.selectedMinute = minute;
    if (this.selectedDay) {
      const newDate = new Date(
        this.currentMonth.getFullYear(),
        this.currentMonth.getMonth(),
        this.selectedDay,
        this.selectedHour,
        minute
      );
      this.updateDate(newDate);
    }
  }

  updateDate(date: Date) {
    this.selectedDate = date;
    this.onChange(date);
    this.dateChange.emit(date);
  }

  confirmSelection() {
    if (this.selectedDate) {
      this.isOpen = false;
    }
  }

  clearSelection(event: Event) {
    event.stopPropagation();
    this.selectedDate = null;
    this.selectedDay = null;
    this.onChange(null);
    this.dateChange.emit(null);
  }

  isToday(day: number | null): boolean {
    if (day === null) return false;
    const today = new Date();
    return (
      day === today.getDate() &&
      this.currentMonth.getMonth() === today.getMonth() &&
      this.currentMonth.getFullYear() === today.getFullYear()
    );
  }

  isSelected(day: number | null): boolean {
    if (day === null || !this.selectedDate) return false;
    return (
      day === this.selectedDay &&
      this.currentMonth.getMonth() === this.selectedDate.getMonth() &&
      this.currentMonth.getFullYear() === this.selectedDate.getFullYear()
    );
  }

  isPastDay(day: number | null): boolean {
    if (day === null) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const dayDate = new Date(
      this.currentMonth.getFullYear(),
      this.currentMonth.getMonth(),
      day
    );
    dayDate.setHours(0, 0, 0, 0);
    
    return dayDate < today;
  }

  onManualInput(event: Event) {
    const input = (event.target as HTMLInputElement).value;
    
    // Format attendu: DD/MM/YYYY HH:MM
    const dateTimeRegex = /^(\d{2})\/(\d{2})\/(\d{4})\s+(\d{1,2}):(\d{2})$/;
    const match = input.match(dateTimeRegex);
    
    if (match) {
      const [, day, month, year, hour, minute] = match;
      const date = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day),
        parseInt(hour),
        parseInt(minute)
      );
      
      // Vérifier que la date est valide et pas dans le passé
      if (!isNaN(date.getTime())) {
        const now = new Date();
        if (date >= now) {
          this.selectedDate = date;
          this.currentMonth = new Date(date);
          this.selectedDay = date.getDate();
          this.selectedHour = date.getHours();
          this.selectedMinute = date.getMinutes();
          this.updateDate(date);
        }
      }
    }
  }

  // ControlValueAccessor implementation
  writeValue(value: Date | string | null): void {
    if (value) {
      this.selectedDate = typeof value === 'string' ? new Date(value) : value;
      this.currentMonth = new Date(this.selectedDate);
      this.selectedDay = this.selectedDate.getDate();
      this.selectedHour = this.selectedDate.getHours();
      this.selectedMinute = this.selectedDate.getMinutes();
    } else {
      this.selectedDate = null;
      this.selectedDay = null;
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
