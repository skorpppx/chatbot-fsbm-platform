import { Component, signal, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { ThemeService } from '../core/theme.service';
import { AuthService } from '../core/auth.service';

interface NavItem {
  path: string;
  icon: string;
  label: string;
  description?: string;
  exact?: boolean;
}

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],
  template: `
    <div class="shell" [class.collapsed]="collapsed()">
      <!-- ═══════ SIDEBAR ═══════ -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <img src="assets/logos/fsbm.png" alt="FSBM" class="logo-main"
               [class.hidden]="collapsed()" />
          <img src="assets/logos/fsbm.png" alt="FSBM" class="logo-mini"
               [class.hidden]="!collapsed()" />
          <button class="collapse-btn" (click)="toggleCollapse()" [title]="collapsed() ? 'Étendre' : 'Réduire'">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path [attr.d]="collapsed() ? 'M9 18l6-6-6-6' : 'M15 18l-6-6 6-6'"/>
            </svg>
          </button>
        </div>

        <nav class="sidebar-nav">
          <a *ngFor="let item of navItems"
             [routerLink]="item.path"
             [routerLinkActiveOptions]="{ exact: item.exact || false }"
             routerLinkActive="active"
             class="nav-item"
             [title]="item.label">
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label" [class.hidden]="collapsed()">{{ item.label }}</span>
          </a>
        </nav>

        <div class="sidebar-footer">
          <a *ngIf="auth.isAdmin()" class="nav-item admin-link" routerLink="/admin" routerLinkActive="active" title="Espace administration">
            <span class="nav-icon">🔐</span>
            <span class="nav-label" [class.hidden]="collapsed()">Admin</span>
          </a>
          <button class="theme-toggle" (click)="theme.toggle()" [title]="isDark() ? 'Mode clair' : 'Mode sombre'">
            <span class="theme-icon">{{ isDark() ? '☀️' : '🌙' }}</span>
            <span class="theme-label" [class.hidden]="collapsed()">{{ isDark() ? 'Clair' : 'Sombre' }}</span>
          </button>
          <div class="footer-credits" [class.hidden]="collapsed()">
            <span>PFE 2025/2026</span>
          </div>
        </div>
      </aside>

      <!-- ═══════ TOPBAR + CONTENU ═══════ -->
      <div class="main">
        <header class="topbar">
          <div class="topbar-brand">
            <img src="assets/logos/fsbm-banner.png" alt="FSBM" class="topbar-banner" />
            <div class="topbar-titles">
              <h1>Faculté des Sciences Ben M'Sick</h1>
              <span>Université Hassan II de Casablanca</span>
            </div>
          </div>
          <div class="topbar-actions">
            <span class="status-pill">
              <span class="dot"></span>
              Plateforme en ligne
            </span>
            <a class="quick-chat-btn" routerLink="/chat" routerLinkActive="active">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              Assistant IA
            </a>
          </div>
        </header>

        <main class="content">
          <router-outlet />
        </main>
      </div>
    </div>
  `,
  styleUrl: './app-shell.component.css',
})
export class AppShellComponent {
  readonly theme = inject(ThemeService);
  readonly auth = inject(AuthService);
  readonly collapsed = signal(false);
  readonly isDark = computed(() => this.theme.theme() === 'dark');

  readonly navItems: NavItem[] = [
    { path: '/',              icon: '🏠', label: 'Accueil',          exact: true },
    { path: '/chat',          icon: '🤖', label: 'Assistant IA' },
    { path: '/departements',  icon: '🏢', label: 'Départements' },
    { path: '/filieres',      icon: '📚', label: 'Filières' },
    { path: '/modules',       icon: '📖', label: 'Modules' },
    { path: '/professeurs',   icon: '👨‍🏫', label: 'Professeurs' },
    { path: '/actualites',    icon: '📰', label: 'Actualités' },
    { path: '/vie-etudiante', icon: '🌟', label: 'Vie étudiante' },
    { path: '/avis',          icon: '💬', label: 'Avis' },
  ];

  toggleCollapse() {
    this.collapsed.update(v => !v);
  }
}
