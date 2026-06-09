import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AcademicService, Filiere, Module, Department } from '../../../services/academic.service';
import { AdminService } from '../../../services/admin.service';
import { FileUploadComponent } from '../shared/file-upload.component';

type Tab = 'filieres' | 'modules' | 'professors' | 'departments';

@Component({
  selector: 'app-academic-panel',
  standalone: true,
  imports: [CommonModule, FormsModule, FileUploadComponent],
  template: `
    <div class="panel">
      <div class="panel-head">
        <div class="sub-tabs">
          <button [class.active]="tab() === 'departments'" (click)="switch('departments')">🏢 Départements</button>
          <button [class.active]="tab() === 'filieres'" (click)="switch('filieres')">📚 Filières</button>
          <button [class.active]="tab() === 'modules'" (click)="switch('modules')">📖 Modules</button>
          <button [class.active]="tab() === 'professors'" (click)="switch('professors')">👨‍🏫 Professeurs</button>
        </div>
        <button class="add" (click)="openNew()">+ Ajouter</button>
      </div>

      <div class="muted" *ngIf="loading()">Chargement…</div>

      <!-- DEPARTEMENTS -->
      <table class="tbl" *ngIf="tab() === 'departments' && !loading()">
        <thead><tr><th>Logo</th><th>Code</th><th>Nom</th><th>Chef</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let d of departments()">
            <td><img *ngIf="d.logo_url" [src]="d.logo_url" class="thumb" /><span *ngIf="!d.logo_url">—</span></td>
            <td><code>{{ d.code }}</code></td><td>{{ d.name }}</td><td>{{ d.head_name || '—' }}</td>
            <td class="actions"><button (click)="edit(d)">✏️</button><button (click)="remove(d)">🗑</button></td>
          </tr>
        </tbody>
      </table>

      <!-- FILIERES -->
      <table class="tbl" *ngIf="tab() === 'filieres' && !loading()">
        <thead><tr><th>Logo</th><th>Code</th><th>Nom</th><th>Type</th><th>Active</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let f of filieres()">
            <td><img *ngIf="f.logo_url" [src]="f.logo_url" class="thumb" /><span *ngIf="!f.logo_url">—</span></td>
            <td><code>{{ f.code }}</code></td><td>{{ f.name }}</td><td>{{ f.type }}</td>
            <td>{{ f.is_active ? '✓' : '—' }}</td>
            <td class="actions"><button (click)="edit(f)">✏️</button><button (click)="remove(f)">🗑</button></td>
          </tr>
        </tbody>
      </table>

      <!-- MODULES -->
      <div *ngIf="tab() === 'modules' && !loading()">
        <select class="filter-sel" [(ngModel)]="moduleFiliereFilter" (ngModelChange)="applyModuleFilter()">
          <option [ngValue]="null">Toutes les filières</option>
          <option *ngFor="let f of filieres()" [ngValue]="f.id">{{ f.code }} — {{ f.name }}</option>
        </select>
        <table class="tbl">
          <thead><tr><th>Code</th><th>Nom</th><th>Sem.</th><th>Crédits</th><th></th></tr></thead>
          <tbody>
            <tr *ngFor="let m of visibleModules()">
              <td><code>{{ m.code }}</code></td><td>{{ m.name }}</td><td>{{ m.semester }}</td><td>{{ m.credits }}</td>
              <td class="actions"><button (click)="edit(m)">✏️</button><button (click)="remove(m)">🗑</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PROFESSORS -->
      <table class="tbl" *ngIf="tab() === 'professors' && !loading()">
        <thead><tr><th>Photo</th><th>Matricule</th><th>Nom</th><th>Grade</th><th>Spécialité</th><th></th></tr></thead>
        <tbody>
          <tr *ngFor="let p of professors()">
            <td><img *ngIf="p.photo_url" [src]="p.photo_url" class="thumb round" /><span *ngIf="!p.photo_url">—</span></td>
            <td><code>{{ p.matricule }}</code></td><td>{{ p.first_name }} {{ p.last_name }}</td>
            <td>{{ p.grade }}</td><td>{{ p.specialty || '—' }}</td>
            <td class="actions"><button (click)="edit(p)">✏️</button><button (click)="remove(p)">🗑</button></td>
          </tr>
        </tbody>
      </table>

      <!-- MODAL -->
      <div class="overlay" *ngIf="editing()" (click)="editing.set(false)">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>{{ form.id ? 'Modifier' : 'Ajouter' }} — {{ tabLabel() }}</h3>

          <!-- DEPARTMENT form -->
          <ng-container *ngIf="tab() === 'departments'">
            <div class="row">
              <div><label>Code</label><input class="inp" [(ngModel)]="form.code" /></div>
              <div><label>Nom court</label><input class="inp" [(ngModel)]="form.name_short" /></div>
            </div>
            <label>Nom</label><input class="inp" [(ngModel)]="form.name" />
            <div class="row">
              <div><label>Chef de département</label><input class="inp" [(ngModel)]="form.head_name" /></div>
              <div><label>Email chef</label><input class="inp" [(ngModel)]="form.head_email" /></div>
            </div>
            <label>Couleur (hex)</label><input class="inp" [(ngModel)]="form.color_hex" placeholder="#1C3F6E" />
            <app-file-upload [(url)]="form.logo_url" kind="image" label="Logo du département" />
          </ng-container>

          <!-- FILIERE form -->
          <ng-container *ngIf="tab() === 'filieres'">
            <div class="row">
              <div><label>Code</label><input class="inp" [(ngModel)]="form.code" /></div>
              <div><label>Type</label>
                <select class="inp" [(ngModel)]="form.type">
                  <option value="LICENCE">LICENCE</option><option value="LICENCE_PRO">LICENCE_PRO</option>
                  <option value="MASTER">MASTER</option><option value="MASTER_RECHERCHE">MASTER_RECHERCHE</option>
                </select>
              </div>
            </div>
            <label>Nom</label><input class="inp" [(ngModel)]="form.name" />
            <div class="row">
              <div><label>Département</label>
                <select class="inp" [(ngModel)]="form.department_id">
                  <option *ngFor="let d of departments()" [ngValue]="d.id">{{ d.name }}</option>
                </select>
              </div>
              <div><label>Capacité</label><input class="inp" type="number" [(ngModel)]="form.capacity" /></div>
            </div>
            <label>Coordinateur</label><input class="inp" [(ngModel)]="form.coordinator" />
            <app-file-upload [(url)]="form.logo_url" kind="image" label="Logo de la filière" />
            <label class="chk"><input type="checkbox" [(ngModel)]="form.is_active" /> Active</label>
          </ng-container>

          <!-- MODULE form -->
          <ng-container *ngIf="tab() === 'modules'">
            <div class="row">
              <div><label>Code</label><input class="inp" [(ngModel)]="form.code" /></div>
              <div><label>Semestre</label><input class="inp" type="number" min="1" max="6" [(ngModel)]="form.semester" /></div>
            </div>
            <label>Nom</label><input class="inp" [(ngModel)]="form.name" />
            <div class="row">
              <div><label>Filière</label>
                <select class="inp" [(ngModel)]="form.filiere_id">
                  <option *ngFor="let f of filieres()" [ngValue]="f.id">{{ f.code }}</option>
                </select>
              </div>
              <div><label>Crédits</label><input class="inp" type="number" [(ngModel)]="form.credits" /></div>
            </div>
          </ng-container>

          <!-- PROFESSOR form -->
          <ng-container *ngIf="tab() === 'professors'">
            <div class="row">
              <div><label>Matricule</label><input class="inp" [(ngModel)]="form.matricule" /></div>
              <div><label>Grade</label>
                <select class="inp" [(ngModel)]="form.grade">
                  <option value="PA">PA</option><option value="PH">PH</option><option value="PES">PES</option>
                  <option value="VACATAIRE">VACATAIRE</option><option value="EMERITE">EMERITE</option>
                </select>
              </div>
            </div>
            <div class="row">
              <div><label>Prénom</label><input class="inp" [(ngModel)]="form.first_name" /></div>
              <div><label>Nom</label><input class="inp" [(ngModel)]="form.last_name" /></div>
            </div>
            <label>Email</label><input class="inp" [(ngModel)]="form.email" />
            <div class="row">
              <div><label>Département</label>
                <select class="inp" [(ngModel)]="form.department_id">
                  <option *ngFor="let d of departments()" [ngValue]="d.id">{{ d.name }}</option>
                </select>
              </div>
              <div><label>Spécialité</label><input class="inp" [(ngModel)]="form.specialty" /></div>
            </div>
            <app-file-upload [(url)]="form.photo_url" kind="image" label="Photo du professeur" />
          </ng-container>

          <div class="err" *ngIf="error()">{{ error() }}</div>
          <div class="modal-actions">
            <button class="save" [disabled]="saving()" (click)="save()">{{ saving() ? '…' : 'Enregistrer' }}</button>
            <button class="cancel" (click)="editing.set(false)">Annuler</button>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./panel-shared.css'],
  styles: [`
    .filter-sel { margin-bottom: 12px; border: 1px solid var(--border,#dde1e8); border-radius: 8px; padding: 7px 10px; font-family: inherit; }
    .thumb { width: 34px; height: 34px; object-fit: cover; border-radius: 6px; border: 1px solid #e6e9ef; }
    .thumb.round { border-radius: 50%; }
  `],
})
export class AcademicPanelComponent implements OnInit {
  private academic = inject(AcademicService);
  private admin = inject(AdminService);

  readonly tab = signal<Tab>('departments');
  readonly filieres = signal<Filiere[]>([]);
  readonly modules = signal<Module[]>([]);
  readonly visibleModules = signal<Module[]>([]);
  readonly professors = signal<any[]>([]);
  readonly departments = signal<Department[]>([]);
  readonly loading = signal(true);
  readonly editing = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);

  moduleFiliereFilter: number | null = null;
  form: any = {};

  ngOnInit() {
    this.academic.getDepartments().subscribe(d => this.departments.set(d));
    this.academic.getFilieres().subscribe(d => this.filieres.set(d));
    this.load();
  }

  switch(t: Tab) { this.tab.set(t); this.load(); }

  load() {
    this.loading.set(true);
    if (this.tab() === 'departments') {
      this.academic.getDepartments().subscribe({ next: d => { this.departments.set(d); this.loading.set(false); }, error: () => this.loading.set(false) });
    } else if (this.tab() === 'filieres') {
      this.academic.getFilieres().subscribe({ next: d => { this.filieres.set(d); this.loading.set(false); }, error: () => this.loading.set(false) });
    } else if (this.tab() === 'modules') {
      if (this.filieres().length === 0) this.academic.getFilieres().subscribe(d => this.filieres.set(d));
      this.academic.getModules().subscribe({ next: d => { this.modules.set(d); this.applyModuleFilter(); this.loading.set(false); }, error: () => this.loading.set(false) });
    } else {
      this.academic.getProfessors(undefined, 1, 300).subscribe({ next: (r: any) => { this.professors.set(r.items || r); this.loading.set(false); }, error: () => this.loading.set(false) });
    }
  }

  applyModuleFilter() {
    const f = this.moduleFiliereFilter;
    this.visibleModules.set(f ? this.modules().filter(m => m.filiere_id === f) : this.modules());
  }

  tabLabel(): string {
    return { departments: 'Département', filieres: 'Filière', modules: 'Module', professors: 'Professeur' }[this.tab()];
  }

  openNew() {
    this.error.set(null);
    const dept = this.departments()[0]?.id ?? 1;
    const fil = this.filieres()[0]?.id ?? 1;
    if (this.tab() === 'departments') this.form = { code: '', name: '', color_hex: '#1C3F6E', logo_url: '' };
    else if (this.tab() === 'filieres') this.form = { type: 'LICENCE', department_id: dept, capacity: 100, duration_years: 3, is_active: true, logo_url: '' };
    else if (this.tab() === 'modules') this.form = { semester: 1, credits: 4, filiere_id: fil };
    else this.form = { grade: 'PA', department_id: dept, photo_url: '' };
    this.editing.set(true);
  }

  edit(item: any) { this.form = { ...item }; this.error.set(null); this.editing.set(true); }

  save() {
    this.saving.set(true); this.error.set(null);
    const id = this.form.id;
    const body = { ...this.form };
    let obs;
    if (this.tab() === 'departments') obs = id ? this.admin.updateDepartment(id, body) : this.admin.createDepartment(body);
    else if (this.tab() === 'filieres') obs = id ? this.admin.updateFiliere(id, body) : this.admin.createFiliere(body);
    else if (this.tab() === 'modules') obs = id ? this.admin.updateModule(id, body) : this.admin.createModule(body);
    else obs = id ? this.admin.updateProfessor(id, body) : this.admin.createProfessor(body);

    obs.subscribe({
      next: () => { this.saving.set(false); this.editing.set(false); this.load(); },
      error: (e) => { this.saving.set(false); this.error.set(e?.error?.detail || 'Erreur pendant la sauvegarde.'); },
    });
  }

  remove(item: any) {
    const label = item.code || item.matricule || item.name;
    if (!confirm(`Supprimer "${label}" ?`)) return;
    let obs;
    if (this.tab() === 'departments') obs = this.admin.deleteDepartment(item.id);
    else if (this.tab() === 'filieres') obs = this.admin.deleteFiliere(item.id);
    else if (this.tab() === 'modules') obs = this.admin.deleteModule(item.id);
    else obs = this.admin.deleteProfessor(item.id);
    obs.subscribe({ next: () => this.load(), error: (e) => alert(e?.error?.detail || 'Suppression impossible.') });
  }
}
