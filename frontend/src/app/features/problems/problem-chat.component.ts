import { Component, Input, OnInit, OnDestroy } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ApiService } from "../../core/services/api.service";
import { AuthService } from "../../core/services/auth.service";
import { ProblemChat, ProblemChatCreate } from "../../core/models/models";
import { interval, Subscription } from "rxjs";

@Component({
  selector: "app-problem-chat",
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: "./problem-chat.component.html",
  styleUrls: ["./problem-chat.component.scss"],
})
export class ProblemChatComponent implements OnInit, OnDestroy {
  @Input() problemId!: number;

  messages: ProblemChat[] = [];
  newMessage: string = "";
  loading: boolean = false;
  error: string | null = null;
  currentUserId: number | null = null;

  private pollingSubscription?: Subscription;

  constructor(
    private readonly apiService: ApiService,
    private readonly authService: AuthService
  ) {}

  ngOnInit() {
    this.currentUserId = this.authService.getUserId();
    this.loadMessages();

    // Polling toutes les 5 secondes pour rafraîchir les messages
    this.pollingSubscription = interval(5000).subscribe(() => {
      this.loadMessages(true);
    });
  }

  ngOnDestroy() {
    if (this.pollingSubscription) {
      this.pollingSubscription.unsubscribe();
    }
  }

  loadMessages(silent: boolean = false) {
    if (!silent) {
      this.loading = true;
    }

    if (!this.currentUserId) {
      return;
    }

    this.apiService
      .getProblemChat(this.problemId, this.currentUserId)
      .subscribe({
        next: (messages: any) => {
          this.messages = messages;
          this.loading = false;
          this.error = null;
        },
        error: (err: any) => {
          console.error("Erreur lors du chargement des messages", err);
          if (!silent) {
            this.error = "Impossible de charger les messages";
            this.loading = false;
          }
        },
      });
  }

  sendMessage() {
    if (!this.newMessage.trim() || !this.currentUserId) {
      return;
    }

    this.apiService
      .sendChatMessage(
        this.problemId,
        this.newMessage.trim(),
        this.currentUserId
      )
      .subscribe({
        next: (message: any) => {
          this.messages.push(message);
          this.newMessage = "";
          this.error = null;
        },
        error: (err: any) => {
          console.error("Erreur lors de l'envoi du message", err);
          this.error = "Impossible d'envoyer le message";
        },
      });
  }

  onEnterKey(event: KeyboardEvent) {
    if (!event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  isOwnMessage(message: ProblemChat): boolean {
    return message.user_id === this.currentUserId;
  }

  formatDate(date: Date | string): string {
    // Convertir la chaîne ISO en Date si nécessaire
    const d = typeof date === "string" ? new Date(date) : date;
    const now = new Date();
    const diffMs = now.getTime() - d.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) {
      return "À l'instant";
    } else if (diffMins < 60) {
      return `Il y a ${diffMins} minute${diffMins > 1 ? "s" : ""}`;
    } else if (diffMins < 1440) {
      const hours = Math.floor(diffMins / 60);
      return `Il y a ${hours} heure${hours > 1 ? "s" : ""}`;
    } else {
      return d.toLocaleDateString("fr-FR", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
      });
    }
  }
}
