import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, AdminEvent } from '../../../services/admin.service';
import { FileUploadComponent } from '../shared/file-upload.component';

@Component({
  selector: 'app-events-panel',
  standalone: true,
  imports: [CommonModule, FormsModule, FileUploadComponent],
  template: `
    <div class="panel">
      <div class="panel-head">
        <h2>Événements</h2>
        <button class="add" (click)="openNew()">+ Nouvel événement</button>
      </div>

      <div class="muted" *ngIf="loading()">Chargement…</div>
      <div class="muted" *ngIf="!loading() && items().length === 0">Aucun événement.</div>

      <table class="tbl" *ngIf="items().length">
        <thead><tr><th>Titre</th><th>Type</th><th>Date</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let e of items()">
            <td>{{ e.title }}</td>
            <td><span class="type">{{ e.event_type }}</span></td>
            <td>{{ fmt(e.start_date) }}</td>
            <td class="actions">
              <button (click)="edit(e)">✏️</button>
              <button (click)="remove(e)">🗑</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="overlay" *ngIf="editing()" (click)="editing.set(false)">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>{{ form.id ? 'Modifier' : 'Nouvel' }} événement</h3>
          <label>Titre</label>
          <input class="inp" [(ngModel)]="form.title" />
          <label>Description</label>
          <textarea class="inp" [(ngModel)]="form.description" rows="3"></textarea>
          <div class="row">
            <div>
              <label>Type</label>
              <select class="inp" [(ngModel)]="form.event_type">
                <option value="CONFERENCE">CONFERENCE</option>
                <option value="HACKATHON">HACKATHON</option>
                <option value="PORTES_OUVERTES">PORTES_OUVERTES</option>
                <option value="GALA">GALA</option>
                <option value="FORUM">FORUM</option>
                <option value="AUTRE">AUTRE</option>
              </select>
            </div>
            <div>
              <label>Lieu</label>
              <input class="inp" [(ngModel)]="form.location" placeholder="Amphi A, FSBM" />
            </div>
          </div>
          <div class="row">
            <div>
              <label>Début</label>
              <input class="inp" type="datetime-local" [(ngModel)]="form.start_date" />
            </div>
            <div>
              <label>Fin (optionnel)</label>
              <input class="inp" type="datetime-local" [(ngModel)]="form.end_date" />
            </div>
          </div>
          <label>Organisateur</label>
          <input class="inp" [(ngModel)]="form.organizer" />
          <label>Lien d'inscription (optionnel)</label>
          <input class="inp" [(ngModel)]="form.registration_url" placeholder="https://…" />
          <app-file-upload [(url)]="form.image_url" kind="image" label="Image / affiche (optionnel)" />
          <app-file-upload [(url)]="form.attachment_url" kind="pdf" label="Programme PDF (optionnel)" />

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
export class EventsPanelComponent implements OnInit {
  private svc = inject(AdminService);

  readonly items = signal<AdminEvent[]>([]);
  readonly loading = signal(true);
  readonly editing = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);

  form: Partial<AdminEvent> = this.blank();

  ngOnInit() { this.load(); }
  blank(): Partial<AdminEvent> {
    return { title: '', description: '', event_type: 'AUTRE', start_date: '', location: '', organizer: '' };
  }
  load() {
    this.loading.set(true);
    this.svc.listEvents().subscribe({
      next: (d) => { this.items.set(d); this.loading.set(false); },
      error: () => this.loading.set(false),
    });
  }
  openNew() { this.form = this.blank(); this.error.set(null); this.editing.set(true); }
  edit(e: AdminEvent) {
    this.form = { ...e, start_date: this.toLocal(e.start_date), end_date: this.toLocal(e.end_date) };
    this.error.set(null); this.editing.set(true);
  }
  valid(): boolean { return !!(this.form.title?.trim() && this.form.start_date); }
  save() {
    if (!this.valid()) return;
    this.saving.set(true); this.error.set(null);
    const body: any = { ...this.form };
    if (!body.end_date) delete body.end_date;
    const obs = this.form.id ? this.svc.updateEvent(this.form.id, body) : this.svc.createEvent(body);
    obs.subscribe({
      next: () => { this.saving.set(false); this.editing.set(false); this.load(); },
      error: (e) => { this.saving.set(false); this.error.set(e?.error?.detail || 'Erreur.'); },
    });
  }
  remove(e: AdminEvent) {
    if (!confirm(`Supprimer l'événement "${e.title}" ?`)) return;
    this.svc.deleteEvent(e.id).subscribe(() => this.load());
  }
  fmt(iso?: string | null): string {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  }
  toLocal(iso?: string | null): string {
    if (!iso) return '';
    const d = new Date(iso);
    const pad = (n: number) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }
}
