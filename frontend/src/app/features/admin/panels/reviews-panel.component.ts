import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReviewsService, ReviewAdmin, ReviewStatus } from '../../../services/reviews.service';

@Component({
  selector: 'app-reviews-panel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="panel">
      <div class="panel-head">
        <h2>Modération des avis</h2>
        <div class="filters">
          <button *ngFor="let f of statusFilters" class="fbtn"
                  [class.active]="filter() === f.value" (click)="setFilter(f.value)">
            {{ f.label }}
          </button>
        </div>
      </div>

      <div class="muted" *ngIf="loading()">Chargement…</div>
      <div class="muted" *ngIf="!loading() && rows().length === 0">Aucun avis.</div>

      <article class="rev" *ngFor="let r of rows()" [class.hidden-rev]="r.status === 'HIDDEN'">
        <div class="rev-head">
          <span class="who">{{ r.author_name || 'Anonyme' }}</span>
          <span class="badge" [attr.data-s]="r.status">{{ statusLabel(r.status) }}</span>
          <span class="tgt">{{ r.target_label || r.target_type }}</span>
          <span class="stars" *ngIf="r.rating">{{ '★'.repeat(r.rating) }}</span>
        </div>
        <p class="rev-comment">{{ r.comment }}</p>
        <div class="rev-resp" *ngIf="r.admin_response"><strong>Réponse :</strong> {{ r.admin_response }}</div>

        <div class="rev-actions">
          <button class="a approve" *ngIf="r.status !== 'APPROVED'" (click)="set(r, 'APPROVED')">✓ Approuver</button>
          <button class="a hide" *ngIf="r.status !== 'HIDDEN'" (click)="set(r, 'HIDDEN')">⦸ Masquer</button>
          <button class="a pin" (click)="togglePin(r)">{{ r.is_pinned ? '📌 Désépingler' : '📌 Épingler' }}</button>
          <button class="a reply" (click)="openReply(r)">💬 Répondre</button>
          <button class="a del" (click)="remove(r)">🗑 Supprimer</button>
        </div>

        <div class="reply-box" *ngIf="replyingId() === r.id">
          <textarea [(ngModel)]="replyText" rows="2" placeholder="Réponse officielle de l'administration…"></textarea>
          <div class="reply-actions">
            <button class="save" (click)="sendReply(r)">Envoyer</button>
            <button class="cancel" (click)="replyingId.set(null)">Annuler</button>
          </div>
        </div>
      </article>
    </div>
  `,
  styles: [`
    .panel-head { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    h2 { margin: 0; font-size: 1.2rem; color: var(--text, #1a2233); }
    .filters { display: flex; gap: 6px; }
    .fbtn { border: 1px solid var(--border, #dde1e8); background: var(--surface, #fff); border-radius: 8px;
            padding: 6px 12px; font-size: .8rem; cursor: pointer; color: var(--text, #1a2233); }
    .fbtn.active { background: #1C3F6E; color: #fff; border-color: #1C3F6E; }
    .muted { padding: 30px; text-align: center; color: #9aa3b2; }
    .rev { border: 1px solid var(--border, #e6e9ef); border-radius: 12px; padding: 15px; margin-bottom: 12px; background: var(--surface, #fff); }
    .rev.hidden-rev { opacity: .55; }
    .rev-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
    .who { font-weight: 700; color: var(--text, #1a2233); }
    .badge { font-size: .7rem; font-weight: 700; padding: 3px 8px; border-radius: 999px; }
    .badge[data-s="APPROVED"] { background: #e7f7ec; color: #1a7a3d; }
    .badge[data-s="PENDING"] { background: #fef3e8; color: #b45309; }
    .badge[data-s="HIDDEN"] { background: #fdecec; color: #c0392b; }
    .tgt { font-size: .76rem; background: #eef2f7; color: #1C3F6E; padding: 3px 8px; border-radius: 6px; }
    .stars { color: #FFB02E; }
    .rev-comment { margin: 10px 0; color: var(--text-muted, #44505f); line-height: 1.5; }
    .rev-resp { font-size: .84rem; background: var(--surface-2, #f3f6fb); padding: 8px 12px; border-radius: 8px; border-left: 3px solid #1C3F6E; }
    .rev-actions { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
    .a { border: 1px solid var(--border, #dde1e8); background: var(--surface, #fff); border-radius: 7px;
         padding: 5px 10px; font-size: .78rem; cursor: pointer; color: var(--text, #1a2233); }
    .a:hover { border-color: #1C3F6E; }
    .a.approve:hover { background: #e7f7ec; }
    .a.hide:hover { background: #fef3e8; }
    .a.del:hover { background: #fdecec; color: #c0392b; }
    .reply-box { margin-top: 10px; }
    .reply-box textarea { width: 100%; box-sizing: border-box; border: 1px solid #dde1e8; border-radius: 8px; padding: 8px; font-family: inherit; }
    .reply-actions { display: flex; gap: 6px; margin-top: 6px; }
    .save { background: #1C3F6E; color: #fff; border: none; border-radius: 7px; padding: 6px 14px; cursor: pointer; font-size: .8rem; }
    .cancel { background: #eef2f7; border: none; border-radius: 7px; padding: 6px 14px; cursor: pointer; font-size: .8rem; }
  `],
})
export class ReviewsPanelComponent implements OnInit {
  private svc = inject(ReviewsService);

  readonly statusFilters: { label: string; value: ReviewStatus | 'ALL' }[] = [
    { label: 'Tous', value: 'ALL' },
    { label: 'En attente', value: 'PENDING' },
    { label: 'Approuvés', value: 'APPROVED' },
    { label: 'Masqués', value: 'HIDDEN' },
  ];

  readonly rows = signal<ReviewAdmin[]>([]);
  readonly loading = signal(true);
  readonly filter = signal<ReviewStatus | 'ALL'>('ALL');
  readonly replyingId = signal<number | null>(null);
  replyText = '';

  ngOnInit() { this.load(); }

  setFilter(f: ReviewStatus | 'ALL') { this.filter.set(f); this.load(); }

  load() {
    this.loading.set(true);
    const f = this.filter();
    this.svc.adminList(f === 'ALL' ? undefined : f).subscribe({
      next: (data) => { this.rows.set(data); this.loading.set(false); },
      error: () => this.loading.set(false),
    });
  }

  set(r: ReviewAdmin, status: ReviewStatus) {
    this.svc.moderate(r.id, { status }).subscribe(() => this.load());
  }
  togglePin(r: ReviewAdmin) {
    this.svc.moderate(r.id, { is_pinned: !r.is_pinned }).subscribe(() => this.load());
  }
  openReply(r: ReviewAdmin) { this.replyingId.set(r.id); this.replyText = r.admin_response || ''; }
  sendReply(r: ReviewAdmin) {
    this.svc.moderate(r.id, { admin_response: this.replyText.trim() }).subscribe(() => {
      this.replyingId.set(null); this.load();
    });
  }
  remove(r: ReviewAdmin) {
    if (!confirm('Supprimer définitivement cet avis ?')) return;
    this.svc.remove(r.id).subscribe(() => this.load());
  }

  statusLabel(s: string): string {
    return { APPROVED: 'Approuvé', PENDING: 'En attente', HIDDEN: 'Masqué' }[s] || s;
  }
}
