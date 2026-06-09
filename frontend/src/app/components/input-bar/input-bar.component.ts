import { Component, Output, EventEmitter, Input, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
  import { CommonModule } from '@angular/common';
  import { FormsModule } from '@angular/forms';
  @Component({ selector: 'app-input-bar', standalone: true, imports: [CommonModule, FormsModule],
    template: `<div class="input-bar">
      <input #inputRef type="text" [(ngModel)]="message" (keydown.enter)="handleSend()"
        [disabled]="disabled" placeholder="Tapez votre question ici..." maxlength="500" autocomplete="off" />
      <button class="send-btn" (click)="handleSend()" [disabled]="disabled || !message.trim()" title="Envoyer">➤</button>
    </div>`
  })
  export class InputBarComponent implements AfterViewInit {
    @Input() disabled = false;
    @Output() sendMessage = new EventEmitter<string>();
    @ViewChild('inputRef') inputRef!: ElementRef<HTMLInputElement>;
    message = '';
    ngAfterViewInit() { this.inputRef.nativeElement.focus(); }
    handleSend() {
      const t = this.message.trim();
      if (t && !this.disabled) { this.sendMessage.emit(t); this.message = ''; }
    }
  }