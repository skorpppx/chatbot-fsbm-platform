import { Component, Output, EventEmitter } from '@angular/core';
  import { CommonModule } from '@angular/common';
  @Component({ selector: 'app-home-page', standalone: true, imports: [CommonModule], templateUrl: './home-page.component.html' })
  export class HomePageComponent {
    @Output() startChat = new EventEmitter<void>();
    features = [
      { icon: '📋', title: 'Inscription & Scolarité', desc: "Procédures d'inscription, réinscription, retrait de diplôme" },
      { icon: '📚', title: 'Filières & Formations', desc: 'SMI, DI, SV, STU, SMA... toutes les infos sur les filières' },
      { icon: '📅', title: 'Emplois du temps & Examens', desc: 'Horaires, calendrier des examens, résultats' },
      { icon: '🎓', title: 'Stage & PFE', desc: 'Conventions, recherche de stage, conseils' },
      { icon: '📍', title: 'Contacts & Localisation', desc: 'Scolarité, bibliothèque, adresse, transport' },
      { icon: '💡', title: 'Vie Étudiante', desc: 'Clubs, bourses, hébergement, restauration' },
    ];
  }