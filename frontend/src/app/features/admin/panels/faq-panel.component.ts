import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, FaqItem } from '../../../services/admin.service';

@Component({
  selector: 'app-faq-panel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="panel">
      <div class="panel-head">
        <h2>FAQ du chatbot</h2>
        <button class="add" (click)="openNew()">+ Nouvelle FAQ</button>
      </div>

      <div class="muted" *ngIf="loading()">Chargement…</div>
      <div class="muted" *ngIf="!loading() && items().length === 0">Aucune FAQ. Ajoute la première !</div>

      <table class="tbl" *ngIf="items().length">
        <thead><tr><th>Tag</th><th>Question</th><th>Active</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let f of items()">
            <td><code>{{ f.intent_tag }}</code></td>
            <td class="q">{{ f.question }}</td>
            <td><span class="dot" [class.on]="f.is_active"></span></td>
            <td class="actions">
              <button (click)="edit(f)">✏️</button>
              <button (click)="remove(f)">🗑</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Form modal -->
      <div class="overlay" *ngIf="editing()" (click)="close($event)">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>{{ form.id ? 'Modifier' : 'Nouvelle' }} FAQ</h3>
          <label>Tag (intent)</label>
          <input class="inp" [(ngModel)]="form.intent_tag" placeholder="ex: inscription, bourse" />
          <label>Question</label>
          <input class="inp" [(ngModel)]="form.question" placeholder="Comment s'inscrire ?" />
          <label>Réponse</label>
          <textarea class="inp" [(ngModel)]="form.answer" rows="4" placeholder="La réponse officielle…"></textarea>
          <label>Mots-clés (séparés par des virgules)</label>
          <input class="inp" [(ngModel)]="form.keywords" placeholder="inscription, dossier, candidature" />
          <label>Lien associé (optionnel)</label>
          <input class="inp" [(ngModel)]="form.related_url" placeholder="https://fsbm.ma/…" />
          <label class="chk"><input type="checkbox" [(ngModel)]="form.is_active" /> Active</label>

          <div class="err" *ngIf="error()">{{ error() }}</div>
          <div class="modal-actions">
            <button class="save" [disabled]="!valid() || saving()" (click)="save()">{{ saving() ? 'Enregistrement…' : 'Enregistrer' }}</button>
            <button class="cancel" (click)="editing.set(false)">Annuler</button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .panel-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    h2 { margin: 0; font-size: 1.2rem; color: var(--text, #1a2233); }
    .add { background: #1C3F6E; color: #fff; border: none; border-radius: 8px; padding: 8px 14px; cursor: pointer; font-size: .85rem; }
    .muted { padding: 30px; text-align: center; color: #9aa3b2; }
    .tbl { width: 100%; border-collapse: collapse; font-size: .86rem; }
    .tbl th { text-align: left; padding: 9px; color: #7a8499; border-bottom: 2px solid var(--border, #e6e9ef); font-weight: 600; }
    .tbl td { padding: 9px; border-bottom: 1px solid var(--border, #eef1f5); color: var(--text, #1a2233); }
    .tbl code { background: #eef2f7; color: #1C3F6E; padding: 2px 6px; border-radius: 5px; font-size: .8rem; }
    .q { max-width: 420px; }
    .dot { width: 9px; height: 9px; border-radius: 50%; background: #cfd6e0; display: inline-block; }
    .dot.on { background: #1a7a3d; }
    .actions button { border: none; background: none; cursor: pointer; font-size: 1rem; padding: 2px 5px; }
    .overlay { position: fixed; inset: 0; background: rgba(0,0,0,.45); display: flex; align-items: center; justify-content: center; z-index: 100; padding: 16px; }
    .modal { background: var(--surface, #fff); border-radius: 16px; padding: 24px; width: 100%; max-width: 520px; max-height: 90vh; overflow-y: auto; }
    .modal h3 { margin: 0 0 14px; color: #1C3F6E; }
    .modal label { display: block; font-size: .8rem; font-weight: 600; color: #5b6577; margin: 11px 0 5px; }
    .inp { width: 100%; box-sizing: border-box; border: 1px solid #dde1e8; border-radius: 9px; padding: 9px 11px; font-family: inherit; font-size: .88rem; }
    .chk { display: flex; align-items: center; gap: 8px; }
    .chk input { width: auto; }
    .err { color: #c0392b; font-size: .82rem; margin-top: 10px; }
    .modal-actions { display: flex; gap: 8px; margin-top: 18px; }
    .save { background: #1C3F6E; color: #fff; border: none; border-radius: 8px; padding: 9px 18px; cursor: pointer; }
    .save:disabled { opacity: .5; }
    .cancel { background: #eef2f7; border: none; border-radius: 8px; padding: 9px 18px; cursor: pointer; }
  `],
})
export class FaqPanelComponent implements OnInit {
  private svc = inject(AdminService);

  readonly items = signal<FaqItem[]>([]);
  readonly loading = signal(true);
  readonly editing = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);

  form: Partial<FaqItem> = this.blank();

  ngOnInit() { this.load(); }

  blank(): Partial<FaqItem> {
    return { intent_tag: '', question: '', answer: '', keywords: '', related_url: '', is_active: true };
  }

  load() {
    this.loading.set(true);
    this.svc.listFaq().subscribe({
      next: (d) => { this.items.set(d); this.loading.set(false); },
      error: () => this.loading.set(false),
    });
  }

  openNew() { this.form = this.blank(); this.error.set(null); this.editing.set(true); }
  edit(f: FaqItem) { this.form = { ...f }; this.error.set(null); this.editing.set(true); }
  close(_: Event) { this.editing.set(false); }

  valid(): boolean {
    return !!(this.form.intent_tag?.trim() && this.form.question?.trim() && this.form.answer?.trim());
  }

  save() {
    if (!this.valid()) return;
    this.saving.set(true);
    this.error.set(null);
    const body = { ...this.form };
    const obs = this.form.id ? this.svc.updateFaq(this.form.id, body) : this.svc.createFaq(body);
    obs.subscribe({
      next: () => { this.saving.set(false); this.editing.set(false); this.load(); },
      error: (e) => { this.saving.set(false); this.error.set(e?.error?.detail || 'Erreur pendant la sauvegarde.'); },
    });
  }

  remove(f: FaqItem) {
    if (!confirm(`Supprimer la FAQ "${f.intent_tag}" ?`)) return;
    this.svc.deleteFaq(f.id).subscribe(() => this.load());
  }
}
