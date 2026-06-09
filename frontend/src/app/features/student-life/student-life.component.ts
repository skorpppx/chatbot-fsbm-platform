import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AcademicService } from '../../services/academic.service';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-student-life',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">🌟</div>
        <div>
          <h1 class="page-title">Vie étudiante</h1>
          <p class="page-subtitle">Clubs, associations et activités à la FSBM</p>
        </div>
      </div>
    </div>

    <div *ngIf="loading()" class="grid grid-3">
      <div *ngFor="let i of [1,2,3,4]" class="card"><div class="skeleton" style="height: 160px;"></div></div>
    </div>

    <div *ngIf="!loading() && clubs().length > 0" class="grid grid-3 fade-in-up">
      <article *ngFor="let c of clubs(); let i = index" class="club-card"
               [class.scientifique]="c.category === 'SCIENTIFIQUE'"
               [class.technique]="c.category === 'TECHNIQUE'"
               [class.culturel]="c.category === 'CULTUREL'"
               [class.sportif]="c.category === 'SPORTIF'"
               [class.humanitaire]="c.category === 'HUMANITAIRE'"
               [style.animation-delay.ms]="i * 60">
        <div class="club-header">
          <div class="club-icon">{{ categoryIcon(c.category) }}</div>
          <span class="badge badge-primary">{{ c.category }}</span>
        </div>
        <h3 class="club-name">{{ c.name }}</h3>
        <p class="club-desc">{{ c.description }}</p>
        <div class="club-meta">
          <div class="meta-row"><span>👤 Président</span><strong>{{ c.president || '—' }}</strong></div>
          <div class="meta-row"><span>👥 Membres</span><strong>{{ c.members_count }}</strong></div>
          <div class="meta-row" *ngIf="c.contact_email">
            <span>📧 Contact</span><a [href]="'mailto:' + c.contact_email">{{ c.contact_email }}</a>
          </div>
        </div>
        <div class="club-socials" *ngIf="c.social_links">
          <a *ngIf="c.social_links.facebook" [href]="c.social_links.facebook" target="_blank" class="social-pill">Facebook</a>
          <a *ngIf="c.social_links.instagram" [href]="'https://instagram.com/' + (c.social_links.instagram || '').replace('@','')" target="_blank" class="social-pill">Instagram</a>
          <a *ngIf="c.social_links.github" [href]="c.social_links.github" target="_blank" class="social-pill">GitHub</a>
          <a *ngIf="c.social_links.linkedin" [href]="c.social_links.linkedin" target="_blank" class="social-pill">LinkedIn</a>
        </div>
      </article>
    </div>

    <div *ngIf="!loading() && clubs().length === 0" class="empty-state">
      <div class="empty-state-icon">🌟</div>
      <div class="empty-state-title">Aucun club enregistré</div>
    </div>
  `,
  styles: [`
    .club-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 22px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s;
      animation: fadeInUp 0.4s ease both;
      position: relative;
      overflow: hidden;
    }
    .club-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 4px;
      background: var(--primary);
    }
    .club-card.scientifique::before { background: var(--info); }
    .club-card.technique::before    { background: var(--accent); }
    .club-card.culturel::before     { background: #A855F7; }
    .club-card.sportif::before      { background: var(--success); }
    .club-card.humanitaire::before  { background: #EC4899; }

    .club-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent);
    }
    .club-header {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 14px;
    }
    .club-icon {
      width: 50px; height: 50px;
      background: linear-gradient(135deg, var(--primary-pale) 0%, var(--accent-pale) 100%);
      border-radius: var(--radius-md);
      display: flex; align-items: center; justify-content: center;
      font-size: 1.6rem;
    }
    .club-name {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-dark);
      margin-bottom: 8px;
      line-height: 1.3;
    }
    .club-desc {
      font-size: 0.85rem;
      color: var(--text-mid);
      line-height: 1.55;
      margin-bottom: 14px;
    }
    .club-meta {
      background: var(--bg);
      padding: 12px;
      border-radius: var(--radius-sm);
      display: flex; flex-direction: column; gap: 5px;
      margin-bottom: 12px;
    }
    .meta-row {
      display: flex; justify-content: space-between; gap: 10px;
      font-size: 0.78rem;
    }
    .meta-row span { color: var(--text-light); }
    .meta-row strong, .meta-row a { color: var(--text-dark); font-weight: 600; text-decoration: none; }
    .meta-row a { color: var(--primary); font-size: 0.74rem; }
    .club-socials { display: flex; flex-wrap: wrap; gap: 6px; }
    .social-pill {
      background: var(--bg);
      color: var(--text-mid);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border);
      text-decoration: none;
      transition: all 0.2s;
    }
    .social-pill:hover {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }
  `]
})
export class StudentLifeComponent implements OnInit {
  private academic = inject(AcademicService);

  readonly clubs = signal<any[]>([]);
  readonly loading = signal(true);

  ngOnInit() {
    this.academic.getClubs().pipe(catchError(() => of([])))
      .subscribe(c => { this.clubs.set(c); this.loading.set(false); });
  }

  categoryIcon(c: string): string {
    return { SCIENTIFIQUE: '🔬', TECHNIQUE: '💻', CULTUREL: '🎭', SPORTIF: '⚽', HUMANITAIRE: '❤️' }[c] || '🌟';
  }
}
