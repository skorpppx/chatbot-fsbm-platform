import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatWindowComponent } from '../../components/chat-window/chat-window.component';

@Component({
  selector: 'app-chat-page',
  standalone: true,
  imports: [CommonModule, ChatWindowComponent],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">🤖</div>
        <div>
          <h1 class="page-title">Assistant Intelligent FSBM</h1>
          <p class="page-subtitle">Posez vos questions en français — réponse instantanée 24h/24</p>
        </div>
      </div>
    </div>
    <div class="chat-page-container fade-in-up">
      <app-chat-window (back)="onBack()"></app-chat-window>
    </div>
  `,
  styles: [`
    .chat-page-container {
      max-width: 920px;
      margin: 0 auto;
    }
  `]
})
export class ChatPageComponent {
  onBack() { /* géré par sidebar */ }
}
