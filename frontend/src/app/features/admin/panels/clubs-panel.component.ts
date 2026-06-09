import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, AdminClub } from '../../../services/admin.service';
import { FileUploadComponent } from '../shared/file-upload.component';

@Component({
  selector: 'app-clubs-panel',
  standalone: true,
  imports: [CommonModule, FormsModule, FileUploadComponent],
  template: `
    <div class="panel">
      <div class="panel-head">
        <h2>Vie étudiante — Clubs</h2>
        <button class="add" (click)="openNew()">+ Nouveau club</button>
      </div>

      <div class="muted" *ngIf="loading()">Chargement…</div>
      <div class="muted" *ngIf="!loading() && items().length === 0">Aucun club. Ajoute le premier !</div>

      <table class="tbl" *ngIf="items().length">
        <thead><tr><th>Logo</th><th>Nom</th><th>Catégorie</th><th>Membres</th><th>Actif</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let c of items()">
            <td><img *ngIf="c.logo_url" [src]="c.logo_url" class="thumb" /><span *ngIf="!c.logo_url">—</span></td>
            <td>{{ c.name }}</td><td><span class="type">{{ c.category }}</span></td>
            <td>{{ c.members_count || 0 }}</td><td>{{ c.is_active ? '✓' : '—' }}</td>
            <td class="actions"><button (click)="edit(c)">✏️</button><button (click)="remove(c)">🗑</button></td>
          </tr>
        </tbody>
      </table>

      <div class="overlay" *ngIf="editing()" (click)="editing.set(false)">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>{{ form.id ? 'Modifier' : 'Nouveau' }} club</h3>
          <label>Nom</label><input class="inp" [(ngModel)]="form.name" />
          <label>Description</label><textarea class="inp" [(ngModel)]="form.description" rows="3"></textarea>
          <div class="row">
            <div><label>Catégorie</label>
              <select class="inp" [(ngModel)]="form.category">
                <option value="SCIENTIFIQUE">SCIENTIFIQUE</option>
                <option value="CULTUREL">CULTUREL</option>
                <option value="SPORTIF">SPORTIF</option>
                <option value="HUMANITAIRE">HUMANITAIRE</option>
                <option value="TECHNIQUE">TECHNIQUE</option>
              </select>
            </div>
            <div><label>Membres</label><input class="inp" type="number" [(ngModel)]="form.members_count" /></div>
          </div>
          <div class="row">
            <div><label>Président</label><input class="inp" [(ngModel)]="form.president" /></div>
            <div><label>Email contact</label><input class="inp" [(ngModel)]="form.contact_email" /></div>
          </div>
          <app-file-upload [(url)]="form.logo_url" kind="image" label="Logo du club" />
          <label class="chk"><input type="checkbox" [(ngModel)]="form.is_active" /> Club actif</label>

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
  styles: [`.thumb { width: 34px; height: 34px; object-fit: cover; border-radius: 6px; border: 1px solid #e6e9ef; }`],
})
export class ClubsPanelComponent implements OnInit {
  private svc = inject(AdminService);

  readonly items = signal<AdminClub[]>([]);
  readonly loading = signal(true);
  readonly editing = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);

  form: Partial<AdminClub> = this.blank();

  ngOnInit() { this.load(); }
  blank(): Partial<AdminClub> {
    return { name: '', description: '', category: 'TECHNIQUE', president: '', contact_email: '', logo_url: '', members_count: 0, is_active: true };
  }
  load() {
    this.loading.set(true);
    this.svc.listClubs().subscribe({
      next: (d) => { this.items.set(d); this.loading.set(false); },
      error: () => this.loading.set(false),
    });
  }
  openNew() { this.form = this.blank(); this.error.set(null); this.editing.set(true); }
  edit(c: AdminClub) { this.form = { ...c }; this.error.set(null); this.editing.set(true); }
  valid(): boolean { return !!this.form.name?.trim(); }
  save() {
    if (!this.valid()) return;
    this.saving.set(true); this.error.set(null);
    const body = { ...this.form };
    const obs = this.form.id ? this.svc.updateClub(this.form.id, body) : this.svc.createClub(body);
    obs.subscribe({
      next: () => { this.saving.set(false); this.editing.set(false); this.load(); },
      error: (e) => { this.saving.set(false); this.error.set(e?.error?.detail || 'Erreur pendant la sauvegarde.'); },
    });
  }
  remove(c: AdminClub) {
    if (!confirm(`Supprimer le club "${c.name}" ?`)) return;
    this.svc.deleteClub(c.id).subscribe(() => this.load());
  }
}
