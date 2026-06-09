import { Component, Output, EventEmitter, OnInit, ViewChild, ElementRef, AfterViewChecked, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService, LLMStatus } from '../../services/chat.service';
import { Message } from '../../models/message.model';
import { MessageBubbleComponent } from '../message-bubble/message-bubble.component';
import { InputBarComponent } from '../input-bar/input-bar.component';
import { TypingIndicatorComponent } from '../typing-indicator/typing-indicator.component';
import { QuickActionsComponent } from '../quick-actions/quick-actions.component';
import { catchError, of } from 'rxjs';

/**
 * Chat window avec toggle TF-IDF / LLM (LLaMA 3 + RAG).
 *
 * - Mode TF-IDF : reponses pre-ecrites (instantanees)
 * - Mode LLM    : reponses generees par LLaMA 3 via Groq (contextuelles)
 *
 * Le mode LLM se desactive automatiquement si Groq + HF indisponibles.
 */
@Component({
  selector: 'app-chat-window',
  standalone: true,
  imports: [CommonModule, MessageBubbleComponent, InputBarComponent, TypingIndicatorComponent, QuickActionsComponent],
  templateUrl: './chat-window.component.html',
})
export class ChatWindowComponent implements OnInit, AfterViewChecked {
  private chatService = inject(ChatService);

  @Output() back = new EventEmitter<void>();
  @ViewChild('messagesEnd') messagesEnd!: ElementRef;

  messages: Message[] = [];
  isTyping = false;
  showQuickActions = true;
  sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

  // Mode IA
  readonly useLLM = signal(false);
  readonly llmStatus = signal<LLMStatus | null>(null);
  readonly lastProvider = signal<string | null>(null);
  readonly lastLatency = signal<number | null>(null);

  ngOnInit() {
    this.messages.push({
      id: 0,
      sender: 'bot',
      timestamp: new Date(),
      conversationId: null,
      text: "Bonjour ! 👋 Je suis le chatbot de la FSBM.\n\nJe peux vous aider avec les inscriptions, les filières, les emplois du temps, les examens et bien plus encore !\n\n💡 Activez le mode **IA (LLaMA 3)** en haut pour des réponses encore plus naturelles."
    });
    this.checkLLMStatus();
  }

  ngAfterViewChecked() {
    if (this.messagesEnd) this.messagesEnd.nativeElement.scrollIntoView({ behavior: 'smooth' });
  }

  private checkLLMStatus() {
    this.chatService.getLLMStatus().pipe(
      catchError(() => of(null))
    ).subscribe(status => {
      this.llmStatus.set(status);
      // Activer auto si Groq dispo
      if (status?.groq?.available) {
        this.useLLM.set(true);
      }
    });
  }

  toggleLLM() {
    this.useLLM.update(v => !v);
  }

  sendMessage(text: string) {
    this.messages.push({ id: Date.now(), sender: 'user', text, timestamp: new Date() });
    this.isTyping = true;
    this.showQuickActions = false;

    if (this.useLLM()) {
      this.sendViaLLM(text);
    } else {
      this.sendViaTFIDF(text);
    }
  }

  private sendViaTFIDF(text: string) {
    this.chatService.sendMessage(text, this.sessionId).subscribe({
      next: (data) => {
        setTimeout(() => {
          this.messages.push({
            id: Date.now() + 1,
            sender: 'bot',
            text: data.response,
            timestamp: new Date(),
            conversationId: data.conversation_id,
            intent: data.intent,
            confidence: data.confidence,
          });
          this.lastProvider.set('tfidf');
          this.lastLatency.set(null);
          this.isTyping = false;
        }, 300 + Math.random() * 500);
      },
      error: () => {
        this.pushError("Désolé, une erreur s'est produite. Vérifiez que le serveur backend est lancé (port 8001).");
        this.isTyping = false;
      }
    });
  }

  private sendViaLLM(text: string) {
    this.chatService.sendMessageLLM(text, this.sessionId).subscribe({
      next: (data) => {
        this.messages.push({
          id: Date.now() + 1,
          sender: 'bot',
          text: data.response,
          timestamp: new Date(),
          conversationId: data.conversation_id,
          intent: data.intent_detected,
          confidence: data.confidence,
        });
        this.lastProvider.set(data.provider);
        this.lastLatency.set(data.latency_ms);
        this.isTyping = false;
      },
      error: (err) => {
        // Fallback automatique sur TF-IDF
        console.warn('LLM error, fallback TF-IDF', err);
        this.sendViaTFIDF(text);
      }
    });
  }

  private pushError(msg: string) {
    this.messages.push({
      id: Date.now() + 1,
      sender: 'bot',
      timestamp: new Date(),
      conversationId: null,
      text: msg,
    });
  }

  providerBadge(): { label: string; color: string } {
    const p = this.lastProvider();
    if (p === 'groq')  return { label: '🤖 LLaMA 3.3 via Groq', color: '#A855F7' };
    if (p === 'hf')    return { label: '🤗 LLaMA via HuggingFace', color: '#F59E0B' };
    if (p === 'tfidf') return { label: '⚡ TF-IDF', color: '#3B82F6' };
    return { label: '', color: '#94A3B8' };
  }
}
