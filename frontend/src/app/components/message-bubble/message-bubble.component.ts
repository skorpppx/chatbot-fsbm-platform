import { Component, Input } from '@angular/core';
  import { CommonModule } from '@angular/common';
  import { ChatService } from '../../services/chat.service';
  import { Message } from '../../models/message.model';
  @Component({ selector: 'app-message-bubble', standalone: true, imports: [CommonModule], templateUrl: './message-bubble.component.html' })
  export class MessageBubbleComponent {
    @Input() message!: Message;
    feedbackGiven: number | null = null;
    constructor(private chatService: ChatService) {}
    formatTime(t: Date): string { return new Date(t).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }); }
    sendFeedback(note: number) {
      this.feedbackGiven = note;
      if (this.message.conversationId) this.chatService.sendFeedback({ conversation_id: this.message.conversationId, note }).subscribe();
    }
  }