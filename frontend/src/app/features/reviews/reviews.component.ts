import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';
import {
  ReviewsService, Review, ReviewStats, TargetType,
} from '../../services/reviews.service';

interface TargetOption {
  type: TargetType;
  icon: string;
  label: string;
  hint: string;
  needsRating?: boolean;
}

@Component({
  selector: 'app-reviews',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="reviews-page">
      <!-- ═══════ EN-TÊTE + STATS ═══════ -->
      <header class="hero">
        <div class="hero-text">
          <h1>💬 Avis & Recommandations</h1>
          <p>Donne ton avis sur l'assistant IA, ta filière, tes modules, ou laisse un message libre. Ta voix compte.</p>
        </div>

        <div class="rating-summary" *ngIf="stats() as s">
          <div class="big-score">
            <span class="score">{{ s.ai_average ? (s.ai_average | number:'1.1-1') : '—' }}</span>
            <div class="stars-row">
              <span *ngFor="let i of [1,2,3,4,5]"
                    class="star"
                    [class.filled]="i <= roundedAi()">★</span>
            </div>
            <span class="score-label">Assistant IA · {{ s.ai_count }} avis</span>
          </div>
          <div class="dist">
            <div class="dist-row" *ngFor="let b of s.distribution">
              <span class="dist-star">{{ b.stars }}★</span>
              <div class="bar"><div class="bar-fill" [style.width.%]="pct(b.count, s.ai_count)"></div></div>
              <span class="dist-count">{{ b.count }}</span>
            </div>
          </div>
        </div>
      </header>

      <div class="grid">
        <!-- ═══════ FORMULAIRE ═══════ -->
        <section class="card form-card">
          <h2>Laisser un avis</h2>

          <label class="field-label">Sur quoi ?</label>
          <div class="target-chips">
            <button *ngFor="let opt of targets"
                    class="chip"
                    [class.active]="form.target_type === opt.type"
                    (click)="setTarget(opt)"
                    [title]="opt.hint">
              <span class="chip-icon">{{ opt.icon }}</span>{{ opt.label }}
            </button>
          </div>

          <!-- Note étoilée (assistant IA surtout) -->
          <div class="rating-input" *ngIf="currentTarget().needsRating || form.rating! > 0">
            <label class="field-label">
              Ta note
              <span class="req" *ngIf="currentTarget().needsRating">*</span>
            </label>
            <div class="stars-pick" (mouseleave)="hoverStar.set(0)">
              <button *ngFor="let i of [1,2,3,4,5]"
                      type="button"
                      class="star-btn"
                      [class.on]="i <= (hoverStar() || form.rating!)"
                      (mouseenter)="hoverStar.set(i)"
                      (click)="form.rating = i">★</button>
              <span class="rating-text">{{ ratingText() }}</span>
            </div>
          </div>

          <label class="field-label" *ngIf="needsTargetLabel()">
            {{ currentTarget().type === 'MODULE' ? 'Quel module ?' :
               currentTarget().type === 'PROFESSOR' ? 'Quel professeur ?' : 'Quelle filière ?' }}
          </label>
          <input *ngIf="needsTargetLabel()" class="input" [(ngModel)]="targetLabel"
                 [placeholder]="labelPlaceholder()" maxlength="200" />

          <label class="field-label">Titre (optionnel)</label>
          <input class="input" [(ngModel)]="form.title" placeholder="Résume ton avis en quelques mots" maxlength="200" />

          <label class="field-label">Ton message <span class="req">*</span></label>
          <textarea class="input textarea" [(ngModel)]="form.comment" rows="4"
                    placeholder="Partage ton expérience, ta recommandation, ta suggestion…"
                    maxlength="2000"></textarea>
          <div class="char-count">{{ form.comment.length }}/2000</div>

          <div class="two-cols">
            <div>
              <label class="field-label">Ton nom (optionnel)</label>
              <input class="input" [(ngModel)]="form.author_name" placeholder="Anonyme" maxlength="120" />
            </div>
            <div>
              <label class="field-label">Ta filière (optionnel)</label>
              <input class="input" [(ngModel)]="form.author_filiere" placeholder="ex: SMI, Master IADS" maxlength="120" />
            </div>
          </div>

          <button class="submit-btn" [disabled]="!canSubmit() || submitting()" (click)="submit()">
            <span *ngIf="!submitting()">Publier mon avis</span>
            <span *ngIf="submitting()">Envoi…</span>
          </button>

          <div class="toast success" *ngIf="submitted()">
            ✅ Merci ! Ton avis a été publié.
          </div>
          <div class="toast error" *ngIf="error()">⚠️ {{ error() }}</div>
        </section>

        <!-- ═══════ MUR D'AVIS ═══════ -->
        <section class="wall">
          <div class="wall-head">
            <h2>Ce que disent les étudiants</h2>
            <div class="filter-tabs">
              <button class="tab" [class.active]="filter() === 'ALL'" (click)="filter.set('ALL')">Tous</button>
              <button class="tab" [class.active]="filter() === 'AI_ASSISTANT'" (click)="filter.set('AI_ASSISTANT')">🤖 Assistant</button>
              <button class="tab" [class.active]="filter() === 'FACULTE'" (click)="filter.set('FACULTE')">🏛️ Faculté</button>
              <button class="tab" [class.active]="filter() === 'GENERAL'" (click)="filter.set('GENERAL')">💭 Libre</button>
            </div>
          </div>

          <div class="loading" *ngIf="loading()">Chargement des avis…</div>

          <div class="empty" *ngIf="!loading() && visibleReviews().length === 0">
            Aucun avis pour l'instant. Sois le premier à t'exprimer !
          </div>

          <article class="review-card" *ngFor="let r of visibleReviews()" [class.pinned]="r.is_pinned">
            <div class="review-top">
              <div class="avatar">{{ initials(r.author_name) }}</div>
              <div class="meta">
                <span class="author">{{ r.author_name || 'Anonyme' }}</span>
                <span class="sub">
                  <span *ngIf="r.author_filiere" class="filiere-tag">{{ r.author_filiere }}</span>
                  {{ formatDate(r.created_at) }}
                </span>
              </div>
              <span class="target-badge" [attr.data-type]="r.target_type">{{ badge(r) }}</span>
            </div>

            <div class="review-stars" *ngIf="r.rating">
              <span *ngFor="let i of [1,2,3,4,5]" class="star" [class.filled]="i <= r.rating!">★</span>
            </div>

            <h3 class="review-title" *ngIf="r.title">{{ r.title }}</h3>
            <p class="review-comment">{{ r.comment }}</p>

            <span class="pin-flag" *ngIf="r.is_pinned">📌 Épinglé</span>

            <div class="admin-response" *ngIf="r.admin_response">
              <strong>Réponse de l'administration :</strong>
              <p>{{ r.admin_response }}</p>
            </div>
          </article>
        </section>
      </div>
    </div>
  `,
  styles: [`
    .reviews-page { max-width: 1180px; margin: 0 auto; padding: 8px 4px 48px; }

    .hero { display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between;
            align-items: center; background: linear-gradient(135deg, #1C3F6E, #2d5a9e);
            color: #fff; border-radius: 18px; padding: 28px 32px; margin-bottom: 24px; }
    .hero-text h1 { margin: 0 0 8px; font-size: 1.7rem; }
    .hero-text p { margin: 0; opacity: .9; max-width: 460px; line-height: 1.5; }

    .rating-summary { display: flex; gap: 24px; align-items: center;
                      background: rgba(255,255,255,.12); padding: 16px 22px; border-radius: 14px; }
    .big-score { text-align: center; }
    .big-score .score { font-size: 2.6rem; font-weight: 800; line-height: 1; }
    .stars-row .star { color: rgba(255,255,255,.35); font-size: 1.1rem; }
    .stars-row .star.filled { color: #FFD166; }
    .score-label { display: block; font-size: .78rem; opacity: .85; margin-top: 4px; }
    .dist { min-width: 180px; }
    .dist-row { display: flex; align-items: center; gap: 8px; margin: 3px 0; font-size: .78rem; }
    .dist-star { width: 26px; opacity: .9; }
    .bar { flex: 1; height: 7px; background: rgba(255,255,255,.22); border-radius: 4px; overflow: hidden; }
    .bar-fill { height: 100%; background: #FFD166; border-radius: 4px; transition: width .4s; }
    .dist-count { width: 18px; text-align: right; opacity: .85; }

    .grid { display: grid; grid-template-columns: 400px 1fr; gap: 24px; align-items: start; }
    @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }

    .card { background: var(--surface, #fff); border: 1px solid var(--border, #e6e9ef);
            border-radius: 16px; padding: 22px; }
    .form-card { position: sticky; top: 12px; }
    .form-card h2, .wall-head h2 { margin: 0 0 14px; font-size: 1.15rem; color: var(--text, #1a2233); }

    .field-label { display: block; font-size: .82rem; font-weight: 600; margin: 12px 0 6px;
                   color: var(--text-muted, #5b6577); }
    .req { color: #e23; }

    .target-chips { display: flex; flex-wrap: wrap; gap: 8px; }
    .chip { border: 1px solid var(--border, #dde1e8); background: var(--surface-2, #f6f8fb);
            border-radius: 999px; padding: 7px 13px; font-size: .82rem; cursor: pointer;
            display: inline-flex; align-items: center; gap: 6px; transition: .15s; color: var(--text, #1a2233); }
    .chip:hover { border-color: #1C3F6E; }
    .chip.active { background: #1C3F6E; color: #fff; border-color: #1C3F6E; }
    .chip-icon { font-size: .95rem; }

    .stars-pick { display: flex; align-items: center; gap: 4px; }
    .star-btn { background: none; border: none; font-size: 1.8rem; cursor: pointer;
                color: #d4d8e0; transition: .12s; line-height: 1; padding: 0 2px; }
    .star-btn.on { color: #FFB02E; transform: scale(1.05); }
    .rating-text { margin-left: 10px; font-size: .82rem; color: var(--text-muted, #5b6577); }

    .input { width: 100%; box-sizing: border-box; border: 1px solid var(--border, #dde1e8);
             border-radius: 10px; padding: 10px 12px; font-size: .9rem; background: var(--surface, #fff);
             color: var(--text, #1a2233); font-family: inherit; }
    .input:focus { outline: none; border-color: #1C3F6E; box-shadow: 0 0 0 3px rgba(28,63,110,.12); }
    .textarea { resize: vertical; }
    .char-count { text-align: right; font-size: .72rem; color: #9aa3b2; margin-top: 3px; }
    .two-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

    .submit-btn { width: 100%; margin-top: 18px; background: #1C3F6E; color: #fff; border: none;
                  border-radius: 10px; padding: 12px; font-size: .95rem; font-weight: 600; cursor: pointer;
                  transition: .15s; }
    .submit-btn:hover:not(:disabled) { background: #16335a; }
    .submit-btn:disabled { opacity: .5; cursor: not-allowed; }

    .toast { margin-top: 12px; padding: 10px 14px; border-radius: 10px; font-size: .85rem; }
    .toast.success { background: #e7f7ec; color: #1a7a3d; }
    .toast.error { background: #fdecec; color: #c0392b; }

    .wall-head { display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: center; }
    .filter-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
    .tab { border: 1px solid var(--border, #dde1e8); background: var(--surface, #fff);
           border-radius: 8px; padding: 6px 11px; font-size: .8rem; cursor: pointer; color: var(--text, #1a2233); }
    .tab.active { background: #1C3F6E; color: #fff; border-color: #1C3F6E; }

    .loading, .empty { padding: 40px; text-align: center; color: #9aa3b2; }

    .review-card { background: var(--surface, #fff); border: 1px solid var(--border, #e6e9ef);
                   border-radius: 14px; padding: 18px; margin-top: 14px; transition: .15s; }
    .review-card:hover { box-shadow: 0 4px 18px rgba(0,0,0,.06); }
    .review-card.pinned { border-color: #FFB02E; background: linear-gradient(0deg, rgba(255,176,46,.04), transparent); }
    .review-top { display: flex; align-items: center; gap: 12px; }
    .avatar { width: 40px; height: 40px; border-radius: 50%; background: #1C3F6E; color: #fff;
              display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .85rem; flex-shrink: 0; }
    .meta { display: flex; flex-direction: column; flex: 1; min-width: 0; }
    .author { font-weight: 600; color: var(--text, #1a2233); }
    .sub { font-size: .76rem; color: #9aa3b2; display: flex; align-items: center; gap: 8px; }
    .filiere-tag { background: var(--surface-2, #eef2f7); color: #1C3F6E; padding: 2px 7px; border-radius: 6px; font-weight: 600; }
    .target-badge { font-size: .7rem; font-weight: 700; padding: 4px 9px; border-radius: 999px;
                    background: #eef2f7; color: #1C3F6E; white-space: nowrap; }
    .target-badge[data-type="AI_ASSISTANT"] { background: #e8f0fe; color: #1a56db; }
    .target-badge[data-type="FACULTE"] { background: #fef3e8; color: #b45309; }
    .target-badge[data-type="GENERAL"] { background: #f0eafe; color: #6d28d9; }

    .review-stars { margin: 10px 0 4px; }
    .review-stars .star { color: #d4d8e0; font-size: 1.05rem; }
    .review-stars .star.filled { color: #FFB02E; }
    .review-title { margin: 6px 0 4px; font-size: 1rem; color: var(--text, #1a2233); }
    .review-comment { margin: 4px 0; color: var(--text, #38415280); line-height: 1.55; color: var(--text-muted, #44505f); }
    .pin-flag { display: inline-block; margin-top: 6px; font-size: .72rem; color: #b45309; }
    .admin-response { margin-top: 12px; padding: 10px 14px; background: var(--surface-2, #f3f6fb);
                      border-left: 3px solid #1C3F6E; border-radius: 8px; font-size: .85rem; }
    .admin-response p { margin: 4px 0 0; color: var(--text-muted, #44505f); }
  `],
})
export class ReviewsComponent implements OnInit {
  private svc = inject(ReviewsService);

  readonly targets: TargetOption[] = [
    { type: 'AI_ASSISTANT', icon: '🤖', label: 'Assistant IA', hint: 'Note le chatbot', needsRating: true },
    { type: 'FACULTE',  icon: '🏛️', label: 'Faculté', hint: 'Avis sur la FSBM' },
    { type: 'FILIERE',  icon: '📚', label: 'Filière', hint: 'Avis sur une filière' },
    { type: 'MODULE',   icon: '📖', label: 'Module', hint: 'Avis sur une matière' },
    { type: 'PROFESSOR',icon: '👨‍🏫', label: 'Professeur', hint: 'Avis sur un enseignant' },
    { type: 'GENERAL',  icon: '💭', label: 'Libre', hint: 'Message libre' },
  ];

  form: {
    target_type: TargetType; rating: number | null; title: string;
    comment: string; author_name: string; author_filiere: string;
  } = { target_type: 'AI_ASSISTANT', rating: 0, title: '', comment: '', author_name: '', author_filiere: '' };

  targetLabel = '';

  readonly reviews = signal<Review[]>([]);
  readonly stats = signal<ReviewStats | null>(null);
  readonly loading = signal(true);
  readonly submitting = signal(false);
  readonly submitted = signal(false);
  readonly error = signal<string | null>(null);
  readonly hoverStar = signal(0);
  readonly filter = signal<TargetType | 'ALL'>('ALL');

  readonly roundedAi = computed(() => Math.round(this.stats()?.ai_average || 0));
  readonly currentTarget = computed(
    () => this.targets.find(t => t.type === this.form.target_type) || this.targets[0]
  );
  readonly visibleReviews = computed(() => {
    const f = this.filter();
    const list = this.reviews();
    return f === 'ALL' ? list : list.filter(r => r.target_type === f);
  });

  ngOnInit() { this.load(); }

  load() {
    this.loading.set(true);
    forkJoin({ list: this.svc.list(undefined, 100), stats: this.svc.stats() }).subscribe({
      next: ({ list, stats }) => {
        this.reviews.set(list);
        this.stats.set(stats);
        this.loading.set(false);
      },
      error: () => { this.loading.set(false); this.error.set('Impossible de charger les avis.'); },
    });
  }

  setTarget(opt: TargetOption) {
    this.form.target_type = opt.type;
    if (!opt.needsRating && this.form.target_type !== 'AI_ASSISTANT') {
      // garde la note si l'utilisateur en a mis une, sinon 0
    }
    this.targetLabel = '';
  }

  needsTargetLabel(): boolean {
    return ['MODULE', 'PROFESSOR', 'FILIERE'].includes(this.form.target_type);
  }

  labelPlaceholder(): string {
    switch (this.form.target_type) {
      case 'MODULE': return 'ex: Analyse I, Programmation C';
      case 'PROFESSOR': return 'ex: Pr. Alaoui';
      case 'FILIERE': return 'ex: SMI, Master IADS';
      default: return '';
    }
  }

  ratingText(): string {
    const n = this.hoverStar() || this.form.rating || 0;
    return ['', 'Décevant', 'Moyen', 'Correct', 'Très bien', 'Excellent'][n] || '';
  }

  canSubmit(): boolean {
    if (this.form.comment.trim().length < 3) return false;
    if (this.currentTarget().needsRating && !this.form.rating) return false;
    return true;
  }

  submit() {
    if (!this.canSubmit()) return;
    this.submitting.set(true);
    this.error.set(null);
    this.submitted.set(false);

    const label = this.needsTargetLabel() && this.targetLabel.trim()
      ? this.targetLabel.trim()
      : this.currentTarget().label;

    this.svc.submit({
      target_type: this.form.target_type,
      target_label: label,
      rating: this.form.rating || null,
      title: this.form.title.trim() || null,
      comment: this.form.comment.trim(),
      author_name: this.form.author_name.trim() || null,
      author_filiere: this.form.author_filiere.trim() || null,
    }).subscribe({
      next: () => {
        this.submitting.set(false);
        this.submitted.set(true);
        this.form = { target_type: 'AI_ASSISTANT', rating: 0, title: '', comment: '', author_name: '', author_filiere: '' };
        this.targetLabel = '';
        this.load();
        setTimeout(() => this.submitted.set(false), 4000);
      },
      error: (e) => {
        this.submitting.set(false);
        this.error.set(e?.error?.detail || 'Envoi impossible. Réessaie.');
      },
    });
  }

  pct(count: number, total: number): number {
    return total > 0 ? Math.round((count / total) * 100) : 0;
  }

  badge(r: Review): string {
    const map: Record<string, string> = {
      AI_ASSISTANT: '🤖 Assistant IA', MODULE: '📖 ' + (r.target_label || 'Module'),
      PROFESSOR: '👨‍🏫 ' + (r.target_label || 'Prof'), FILIERE: '📚 ' + (r.target_label || 'Filière'),
      FACULTE: '🏛️ Faculté', GENERAL: '💭 Libre',
    };
    return map[r.target_type] || r.target_type;
  }

  initials(name?: string | null): string {
    if (!name || name === 'Anonyme') return '?';
    return name.split(' ').map(p => p[0]).join('').slice(0, 2).toUpperCase();
  }

  formatDate(iso: string): string {
    const d = new Date(iso);
    return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
  }
}
