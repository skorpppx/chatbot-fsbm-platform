import { Component, Output, EventEmitter } from '@angular/core';
  import { CommonModule } from '@angular/common';
  @Component({ selector: 'app-quick-actions', standalone: true, imports: [CommonModule],
    template: `<div class="quick-actions"><button class="quick-action-btn" *ngFor="let a of actions" (click)="quickAction.emit(a.message)">{{ a.label }}</button></div>`
  })
  export class QuickActionsComponent {
    @Output() quickAction = new EventEmitter<string>();
    actions = [
      { label: "📋 Inscription",     message: "Comment s'inscrire à la FSBM ?" },
      { label: "📚 Filières",        message: "Quelles sont les filières disponibles ?" },
      { label: "📅 Emploi du temps", message: "Où trouver l'emploi du temps ?" },
      { label: "📊 Résultats",       message: "Comment consulter mes résultats ?" },
      { label: "📍 Contact",         message: "Comment contacter la scolarité ?" },
      { label: "🎓 Stage PFE",       message: "Comment trouver un stage ?" },
    ];
  }