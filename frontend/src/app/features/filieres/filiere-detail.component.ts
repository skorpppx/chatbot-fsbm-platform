import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AcademicService } from '../../services/academic.service';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-filiere-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="back-link">
      <a routerLink="/filieres" class="chip">← Retour aux filières</a>
    </div>

    <div *ngIf="filiere() as f" class="filiere-detail fade-in-up">
      <div class="detail-hero" [class.master]="f.type.startsWith('MASTER')">
        <div class="detail-hero-content">
          <div class="detail-badges">
            <span class="badge badge-accent">{{ f.code }}</span>
            <span class="badge badge-primary">{{ f.type }}</span>
          </div>
          <h1>{{ f.name }}</h1>
          <p class="detail-desc">{{ f.description }}</p>
          <div class="detail-quick">
            <div><span>📅 Durée</span><strong>{{ f.duration_years }} ans</strong></div>
            <div><span>👥 Capacité</span><strong>{{ f.capacity }}</strong></div>
            <div><span>👔 Coordinateur</span><strong>{{ f.coordinator }}</strong></div>
            <div><span>📧</span><strong>{{ f.coord_email }}</strong></div>
          </div>
        </div>
      </div>

      <div class="detail-grid">
        <div class="info-block" *ngIf="f.objectives">
          <h3>🎯 Objectifs pédagogiques</h3>
          <p>{{ f.objectives }}</p>
        </div>
        <div class="info-block" *ngIf="f.careers">
          <h3>💼 Débouchés professionnels</h3>
          <p>{{ f.careers }}</p>
        </div>
        <div class="info-block" *ngIf="f.admission">
          <h3>📝 Conditions d'accès</h3>
          <p>{{ f.admission }}</p>
        </div>
      </div>

      <div class="modules-section" *ngIf="modulesBySemester().length > 0">
        <h2>📖 Modules par semestre</h2>
        <div class="semesters">
          <div *ngFor="let sem of modulesBySemester()" class="semester-block">
            <div class="semester-header">
              <span class="semester-badge">S{{ sem.semester }}</span>
              <span class="semester-count">{{ sem.modules.length }} module{{ sem.modules.length > 1 ? 's' : '' }}</span>
            </div>
            <div class="module-list">
              <div *ngFor="let m of sem.modules" class="module-row">
                <span class="mod-code">{{ m.code }}</span>
                <span class="mod-name">{{ m.name }}</span>
                <span class="mod-credits">{{ m.credits }} ECTS</span>
                <span class="mod-hours">{{ m.hours_cours + m.hours_td + m.hours_tp }}h</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div *ngIf="loading()" class="card"><div class="skeleton" style="height: 300px;"></div></div>
    <div *ngIf="!loading() && !filiere()" class="empty-state">
      <div class="empty-state-icon">😕</div>
      <div class="empty-state-title">Filière introuvable</div>
    </div>
  `,
  styles: [`
    .back-link { margin-bottom: 18px; }
    .detail-hero {
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-mid) 100%);
      color: #fff;
      padding: 36px 32px;
      border-radius: var(--radius-lg);
      margin-bottom: 28px;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
    }
    .detail-hero.master {
      background: linear-gradient(135deg, var(--accent-mid) 0%, var(--accent) 100%);
    }
    .detail-hero h1 {
      font-size: 1.8rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin: 14px 0 12px;
      line-height: 1.15;
    }
    .detail-badges { display: flex; gap: 8px; flex-wrap: wrap; }
    .detail-badges .badge { background: rgba(255,255,255,0.20); color: #fff; }
    .detail-desc { font-size: 0.95rem; opacity: 0.94; line-height: 1.65; max-width: 700px; }
    .detail-quick {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-top: 22px;
      padding-top: 22px;
      border-top: 1px solid rgba(255,255,255,0.20);
    }
    .detail-quick > div {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .detail-quick span {
      font-size: 0.74rem;
      opacity: 0.78;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .detail-quick strong { font-size: 0.95rem; font-weight: 700; }

    .detail-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      margin-bottom: 28px;
    }
    .info-block {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 22px;
      box-shadow: var(--shadow-sm);
    }
    .info-block h3 {
      font-size: 1rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 10px;
    }
    .info-block p { font-size: 0.9rem; color: var(--text-mid); line-height: 1.65; }

    .modules-section h2 {
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--text-dark);
      margin-bottom: 16px;
    }
    .semesters {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 18px;
    }
    .semester-block {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
    }
    .semester-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-soft);
    }
    .semester-badge {
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      color: #fff;
      font-weight: 800;
      font-size: 0.85rem;
      padding: 5px 14px;
      border-radius: var(--radius-full);
    }
    .semester-count { font-size: 0.8rem; color: var(--text-light); font-weight: 500; }
    .module-row {
      display: grid;
      grid-template-columns: 90px 1fr auto auto;
      gap: 10px;
      align-items: center;
      padding: 10px 12px;
      border-radius: var(--radius-sm);
      transition: background 0.15s;
      font-size: 0.85rem;
    }
    .module-row:hover { background: var(--bg); }
    .mod-code { font-weight: 700; color: var(--primary); font-size: 0.76rem; }
    .mod-name { color: var(--text-dark); font-weight: 500; }
    .mod-credits { color: var(--accent); font-weight: 600; font-size: 0.78rem; }
    .mod-hours { color: var(--text-light); font-size: 0.78rem; }
  `]
})
export class FiliereDetailComponent implements OnInit {
  private academic = inject(AcademicService);
  private route = inject(ActivatedRoute);

  readonly filiere = signal<any>(null);
  readonly modulesBySemester = signal<any[]>([]);
  readonly loading = signal(true);

  ngOnInit() {
    this.route.params.subscribe(p => {
      const code = p['code'];
      this.academic.getFiliereByCode(code).pipe(catchError(() => of(null)))
        .subscribe(f => {
          this.filiere.set(f);
          if (f) {
            this.academic.getFiliereModules((f as any).id).pipe(catchError(() => of(null)))
              .subscribe(m => {
                this.modulesBySemester.set(m?.by_semester || []);
                this.loading.set(false);
              });
          } else {
            this.loading.set(false);
          }
        });
    });
  }
}
