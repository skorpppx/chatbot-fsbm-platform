import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, AdminAnnouncement } from '../../../services/admin.service';
import { FileUploadComponent } from '../shared/file-upload.component';

@Component({
  selector: 'app-announcements-panel',
  standalone: true,
  imports: [CommonModule, FormsModule, FileUploadComponent],
  template: `
    <div class="panel">
      <div class="panel-head">
        <h2>Annonces</h2>
        <button class="add" (click)="openNew()">+ Nouvelle annonce</button>
      </div>

      <div class="muted" *ngIf="loading()">Chargement…</div>
      <div class="muted" *ngIf="!loading() && items().length === 0">Aucune annonce.</div>

      <table class="tbl" *ngIf="items().length">
        <thead><tr><th>Titre</th><th>Type</th><th>Épinglée</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let a of items()">
            <td>{{ a.title }}</td>
            <td><span class="type" [attr.data-t]="a.type">{{ a.type }}</span></td>
            <td>{{ a.is_pinned ? '📌' : '—' }}</td>
            <td class="actions">
              <button (click)="edit(a)">✏️</button>
              <button (click)="remove(a)">🗑</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="overlay" *ngIf="editing()" (click)="editing.set(false)">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>{{ form.id ? 'Modifier' : 'Nouvelle' }} annonce</h3>
          <label>Titre</label>
          <input class="inp" [(ngModel)]="form.title" />
          <label>Contenu</label>
          <textarea class="inp" [(ngModel)]="form.content" rows="4"></textarea>
          <div class="row">
            <div>
              <label>Type</label>
              <select class="inp" [(ngModel)]="form.type">
                <option value="INFO">INFO</option>
                <option value="URGENT">URGENT</option>
                <option value="EXAMEN">EXAMEN</option>
                <option value="EVENT">EVENT</option>
                <option value="VACANCE">VACANCE</option>
              </select>
            </div>
            <div>
              <label>Auteur</label>
              <input class="inp" [(ngModel)]="form.author" placeholder="Administration FSBM" />
            </div>
          </div>
          <app-file-upload [(url)]="form.image_url" kind="image" label="Image (optionnel)" />
          <app-file-upload [(url)]="form.attachment_url" kind="pdf" label="Pièce jointe PDF (optionnel)" />
          <label class="chk"><input type="checkbox" [(ngModel)]="form.is_pinned" /> Épingler en haut</label>

          <div class="err" *ngIf="error()">{{ error() }}</div>
          <div class="modal-actions">
            <button class="save" [disabled]="!valid() || saving()" (click)="save()">{{ saving() ? '…' : 'Enregistrer' }}</button>
            <button class="cancel" (click)="editing.set(false)">Annuler</button>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./panel-shared.css'],
})
export class AnnouncementsPanelComponent implements OnInit {
  private svc = inject(AdminService);

  readonly items = signal<AdminAnnouncement[]>([]);
  readonly loading = signal(true);
  readonly editing = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);

  form: Partial<AdminAnnouncement> = this.blank();

  ngOnInit() { this.load(); }
  blank(): Partial<AdminAnnouncement> {
    return { title: '', content: '', type: 'INFO', author: 'Administration FSBM', is_pinned: false, image_url: '', attachment_url: '' };
  }
  load() {
    this.loading.set(true);
    this.svc.listAnnouncements().subscribe({
      next: (d) => { this.items.set(d); this.loading.set(false); },
      error: () => this.loading.set(false),
    });
  }
  openNew() { this.form = this.blank(); this.error.set(null); this.editing.set(true); }
  edit(a: AdminAnnouncement) { this.form = { ...a }; this.error.set(null); this.editing.set(true); }
  valid(): boolean { return !!(this.form.title?.trim() && this.form.content?.trim()); }
  save() {
    if (!this.valid()) return;
    this.saving.set(true); this.error.set(null);
    const body = { ...this.form };
    const obs = this.form.id ? this.svc.updateAnnouncement(this.form.id, body) : this.svc.createAnnouncement(body);
    obs.subscribe({
      next: () => { this.saving.set(false); this.editing.set(false); this.load(); },
      error: (e) => { this.saving.set(false); this.error.set(e?.error?.detail || 'Erreur.'); },
    });
  }
  remove(a: AdminAnnouncement) {
    if (!confirm(`Supprimer l'annonce "${a.title}" ?`)) return;
    this.svc.deleteAnnouncement(a.id).subscribe(() => this.load());
  }
}
