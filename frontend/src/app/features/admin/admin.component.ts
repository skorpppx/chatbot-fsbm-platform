import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { AnnouncementsPanelComponent } from './panels/announcements-panel.component';
import { EventsPanelComponent } from './panels/events-panel.component';
import { AcademicPanelComponent } from './panels/academic-panel.component';
import { ReviewsPanelComponent } from './panels/reviews-panel.component';
import { FaqPanelComponent } from './panels/faq-panel.component';
import { ClubsPanelComponent } from './panels/clubs-panel.component';

type Tab = 'announcements' | 'events' | 'academic' | 'clubs' | 'reviews' | 'faq';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [
    CommonModule,
    AnnouncementsPanelComponent, EventsPanelComponent, AcademicPanelComponent,
    ClubsPanelComponent, ReviewsPanelComponent, FaqPanelComponent,
  ],
  template: `
    <div class="admin">
      <header class="admin-top">
        <div class="brand">
          <img src="assets/logos/fsbm.png" alt="FSBM" />
          <div>
            <strong>Espace Administration</strong>
            <span>Plateforme FSBM</span>
          </div>
        </div>
        <div class="user">
          <span class="email">{{ auth.currentUser()?.email }}</span>
          <a class="go-site" href="/" title="Voir la plateforme">🌐</a>
          <button class="logout" (click)="logout()">Déconnexion</button>
        </div>
      </header>

      <nav class="tabs">
        <button [class.active]="tab() === 'announcements'" (click)="tab.set('announcements')">📢 Annonces</button>
        <button [class.active]="tab() === 'events'" (click)="tab.set('events')">📅 Événements</button>
        <button [class.active]="tab() === 'academic'" (click)="tab.set('academic')">🎓 Académique</button>
        <button [class.active]="tab() === 'clubs'" (click)="tab.set('clubs')">🌟 Vie étudiante</button>
        <button [class.active]="tab() === 'reviews'" (click)="tab.set('reviews')">💬 Avis</button>
        <button [class.active]="tab() === 'faq'" (click)="tab.set('faq')">❓ FAQ</button>
      </nav>

      <main class="admin-body">
        <app-announcements-panel *ngIf="tab() === 'announcements'" />
        <app-events-panel        *ngIf="tab() === 'events'" />
        <app-academic-panel      *ngIf="tab() === 'academic'" />
        <app-clubs-panel         *ngIf="tab() === 'clubs'" />
        <app-reviews-panel       *ngIf="tab() === 'reviews'" />
        <app-faq-panel           *ngIf="tab() === 'faq'" />
      </main>
    </div>
  `,
  styles: [`
    .admin { min-height: 100vh; background: var(--bg, #f1f4f9); }
    .admin-top { display: flex; justify-content: space-between; align-items: center;
                 background: #1C3F6E; color: #fff; padding: 12px 24px; }
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand img { height: 40px; background: #fff; border-radius: 8px; padding: 3px; }
    .brand strong { display: block; font-size: 1rem; }
    .brand span { font-size: .76rem; opacity: .8; }
    .user { display: flex; align-items: center; gap: 12px; }
    .email { font-size: .82rem; opacity: .9; }
    .go-site { text-decoration: none; font-size: 1.1rem; }
    .logout { background: rgba(255,255,255,.15); color: #fff; border: 1px solid rgba(255,255,255,.3);
              border-radius: 8px; padding: 7px 14px; cursor: pointer; font-size: .82rem; }
    .logout:hover { background: rgba(255,255,255,.25); }
    .tabs { display: flex; gap: 4px; padding: 0 24px; background: var(--surface, #fff);
            border-bottom: 1px solid var(--border, #e6e9ef); overflow-x: auto; }
    .tabs button { background: none; border: none; padding: 14px 18px; font-size: .9rem; cursor: pointer;
                   color: var(--text-muted, #5b6577); border-bottom: 3px solid transparent; white-space: nowrap; }
    .tabs button.active { color: #1C3F6E; border-bottom-color: #1C3F6E; font-weight: 600; }
    .admin-body { padding: 24px; max-width: 1100px; margin: 0 auto; }
  `],
})
export class AdminComponent {
  readonly auth = inject(AuthService);
  private router = inject(Router);
  readonly tab = signal<Tab>('announcements');

  logout() {
    this.auth.logout();
    this.router.navigate(['/admin/login']);
  }
}
