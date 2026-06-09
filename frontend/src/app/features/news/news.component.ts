import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AcademicService, Announcement } from '../../services/academic.service';
import { catchError, of, forkJoin } from 'rxjs';

@Component({
  selector: 'app-news',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">📰</div>
        <div>
          <h1 class="page-title">Actualités & Événements</h1>
          <p class="page-subtitle">Restez informé de la vie universitaire FSBM</p>
        </div>
      </div>
    </div>

    <div class="news-grid fade-in-up">
      <!-- ═══════ ANNONCES ═══════ -->
      <section class="news-section">
        <h2 class="news-title">📣 Annonces officielles</h2>
        <div *ngIf="loading()" class="grid">
          <div *ngFor="let i of [1,2,3]" class="card"><div class="skeleton" style="height: 90px;"></div></div>
        </div>
        <div *ngIf="!loading() && announcements().length > 0" class="announcement-list">
          <article *ngFor="let a of announcements(); let i = index"
                   class="announcement"
                   [class.pinned]="a.is_pinned"
                   [style.animation-delay.ms]="i * 60">
            <div class="ann-marker"
                 [class.urgent]="a.type === 'URGENT'"
                 [class.examen]="a.type === 'EXAMEN'"
                 [class.vacance]="a.type === 'VACANCE'"
                 [class.event]="a.type === 'EVENT'">
              {{ icon(a.type) }}
            </div>
            <div class="ann-body">
              <div class="ann-title">
                <span class="badge"
                      [class.badge-danger]="a.type === 'URGENT'"
                      [class.badge-warning]="a.type === 'EXAMEN'"
                      [class.badge-success]="a.type === 'VACANCE'"
                      [class.badge-accent]="a.type === 'EVENT'"
                      [class.badge-primary]="a.type === 'INFO'">{{ a.type }}</span>
                <span *ngIf="a.is_pinned" class="pin-badge">📌 Épinglée</span>
                <h3>{{ a.title }}</h3>
              </div>
              <div class="ann-meta">
                <span>👤 {{ a.author || 'Administration' }}</span>
                <span>·</span>
                <span>📅 {{ formatDate(a.published_at) }}</span>
              </div>
              <p class="ann-content">{{ a.content }}</p>
            </div>
          </article>
        </div>
      </section>

      <!-- ═══════ ÉVÉNEMENTS ═══════ -->
      <aside class="events-aside">
        <h2 class="news-title">🎉 Événements à venir</h2>
        <div *ngIf="loading()" class="grid">
          <div class="card"><div class="skeleton" style="height: 120px;"></div></div>
        </div>
        <div *ngIf="!loading() && events().length > 0" class="event-cards">
          <article *ngFor="let e of events(); let i = index" class="event-aside-card"
                   [style.animation-delay.ms]="i * 70">
            <div class="event-type">{{ e.event_type }}</div>
            <h3 class="event-title">{{ e.title }}</h3>
            <p class="event-desc">{{ e.description?.slice(0, 120) }}{{ (e.description?.length || 0) > 120 ? '…' : '' }}</p>
            <div class="event-info">
              <div>📅 {{ formatDate(e.start_date) }}</div>
              <div *ngIf="e.location">📍 {{ e.location }}</div>
              <div *ngIf="e.organizer">👥 {{ e.organizer }}</div>
            </div>
            <a *ngIf="e.registration_url" [href]="e.registration_url" target="_blank" class="btn btn-accent" style="margin-top: 10px;">
              S'inscrire →
            </a>
          </article>
        </div>
      </aside>
    </div>
  `,
  styles: [`
    .news-grid {
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 24px;
    }
    .news-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-dark);
      margin-bottom: 16px;
    }
    .announcement-list { display: flex; flex-direction: column; gap: 14px; }
    .announcement {
      display: flex;
      gap: 14px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s;
      animation: fadeInUp 0.4s ease both;
    }
    .announcement:hover {
      transform: translateX(3px);
      box-shadow: var(--shadow-md);
    }
    .announcement.pinned {
      border-left: 4px solid var(--accent);
      background: linear-gradient(90deg, var(--accent-pale) 0%, var(--surface) 30%);
    }
    .ann-marker {
      width: 46px; height: 46px;
      background: var(--primary-pale);
      color: var(--primary);
      display: flex; align-items: center; justify-content: center;
      border-radius: var(--radius-sm);
      font-size: 1.3rem;
      flex-shrink: 0;
    }
    .ann-marker.urgent  { background: rgba(239,68,68,0.12); color: #DC2626; }
    .ann-marker.examen  { background: rgba(245,158,11,0.12); color: #D97706; }
    .ann-marker.vacance { background: rgba(34,197,94,0.12); color: #16A34A; }
    .ann-marker.event   { background: var(--accent-pale); color: var(--accent); }

    .ann-body { flex: 1; }
    .ann-title { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 6px; }
    .ann-title h3 {
      font-size: 1rem; font-weight: 700;
      color: var(--text-dark);
      width: 100%;
      margin-top: 4px;
    }
    .pin-badge {
      background: var(--accent-pale);
      color: var(--accent);
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: var(--radius-full);
    }
    .ann-meta {
      font-size: 0.77rem;
      color: var(--text-light);
      margin-bottom: 10px;
      display: flex; gap: 6px; align-items: center;
    }
    .ann-content {
      font-size: 0.88rem;
      color: var(--text-mid);
      line-height: 1.65;
    }

    .event-cards { display: flex; flex-direction: column; gap: 14px; }
    .event-aside-card {
      background: linear-gradient(135deg, var(--accent-pale) 0%, var(--primary-pale) 100%);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s;
      animation: fadeInUp 0.4s ease both;
    }
    .event-aside-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
    .event-type {
      display: inline-block;
      background: var(--accent);
      color: #fff;
      font-size: 0.66rem;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: var(--radius-full);
      letter-spacing: 0.05em;
      margin-bottom: 10px;
    }
    .event-title {
      font-size: 0.98rem;
      font-weight: 700;
      color: var(--text-dark);
      margin-bottom: 6px;
      line-height: 1.3;
    }
    .event-desc {
      font-size: 0.83rem;
      color: var(--text-mid);
      margin-bottom: 10px;
      line-height: 1.55;
    }
    .event-info {
      font-size: 0.78rem;
      color: var(--text-mid);
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    @media (max-width: 1024px) {
      .news-grid { grid-template-columns: 1fr; }
    }
  `]
})
export class NewsComponent implements OnInit {
  private academic = inject(AcademicService);

  readonly announcements = signal<Announcement[]>([]);
  readonly events = signal<any[]>([]);
  readonly loading = signal(true);

  ngOnInit() {
    forkJoin({
      ann: this.academic.getAnnouncements(20).pipe(catchError(() => of([]))),
      evt: this.academic.getEvents(true).pipe(catchError(() => of([]))),
    }).subscribe(({ ann, evt }) => {
      this.announcements.set(ann);
      this.events.set(evt);
      this.loading.set(false);
    });
  }

  formatDate(d: string): string {
    return new Date(d).toLocaleDateString('fr-FR', {
      day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
  }

  icon(type: string): string {
    return { URGENT: '🚨', EXAMEN: '📝', VACANCE: '🏖️', EVENT: '🎉', INFO: 'ℹ️' }[type] || 'ℹ️';
  }
}
