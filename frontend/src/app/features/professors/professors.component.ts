import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AcademicService, Professor, Department } from '../../services/academic.service';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-professors',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">👨‍🏫</div>
        <div>
          <h1 class="page-title">Annuaire des Professeurs</h1>
          <p class="page-subtitle">{{ total() }} enseignant{{ total() > 1 ? 's' : '' }} — toutes spécialités confondues</p>
        </div>
      </div>
    </div>

    <div class="filters fade-in-up">
      <input class="input" type="search" placeholder="🔎 Rechercher un professeur (nom, spécialité)..."
             [ngModel]="search()" (ngModelChange)="search.set($event); page.set(1)" />
      <select class="select" [ngModel]="selectedDept()" (ngModelChange)="selectedDept.set($event); page.set(1)">
        <option [ngValue]="null">Tous les départements</option>
        <option *ngFor="let d of departments()" [ngValue]="d.id">{{ d.name }}</option>
      </select>
      <select class="select" [ngModel]="selectedGrade()" (ngModelChange)="selectedGrade.set($event); page.set(1)">
        <option [ngValue]="null">Tous les grades</option>
        <option value="PES">PES</option>
        <option value="PH">Professeur Habilité</option>
        <option value="PA">Professeur Assistant</option>
        <option value="VACATAIRE">Vacataire</option>
      </select>
    </div>

    <div *ngIf="loading()" class="grid grid-3">
      <div *ngFor="let i of [1,2,3,4,5,6]" class="card"><div class="skeleton" style="height: 130px;"></div></div>
    </div>

    <div *ngIf="!loading() && professors().length > 0" class="grid grid-3 fade-in-up">
      <div *ngFor="let p of professors(); let i = index" class="prof-card"
           [style.animation-delay.ms]="(i % 12) * 30">
        <div class="prof-avatar">
          <span class="initials">{{ initials(p) }}</span>
        </div>
        <div class="prof-info">
          <h3 class="prof-name">{{ p.first_name }} {{ p.last_name }}</h3>
          <p class="prof-specialty">{{ p.specialty || 'Spécialité non renseignée' }}</p>
          <div class="prof-tags">
            <span class="badge badge-primary">{{ gradeLabel(p.grade) }}</span>
            <span class="badge badge-accent" *ngIf="p.bureau">📍 {{ p.bureau }}</span>
          </div>
          <a [href]="'mailto:' + p.email" class="prof-email">📧 {{ p.email }}</a>
        </div>
      </div>
    </div>

    <div class="pagination" *ngIf="!loading() && totalPages() > 1">
      <button class="chip" [disabled]="page() === 1" (click)="changePage(page() - 1)">← Précédent</button>
      <span class="page-info">Page {{ page() }} / {{ totalPages() }}</span>
      <button class="chip" [disabled]="page() === totalPages()" (click)="changePage(page() + 1)">Suivant →</button>
    </div>

    <div *ngIf="!loading() && professors().length === 0" class="empty-state">
      <div class="empty-state-icon">👨‍🏫</div>
      <div class="empty-state-title">Aucun professeur trouvé</div>
    </div>
  `,
  styles: [`
    .filters {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 12px;
      margin-bottom: 24px;
    }
    .prof-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s;
      animation: fadeInUp 0.35s ease both;
      display: flex;
      gap: 14px;
    }
    .prof-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent);
    }
    .prof-avatar {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 1.05rem;
      flex-shrink: 0;
      box-shadow: var(--shadow-sm);
    }
    .prof-info { flex: 1; min-width: 0; }
    .prof-name {
      font-size: 0.98rem;
      font-weight: 700;
      color: var(--text-dark);
      margin-bottom: 3px;
      line-height: 1.2;
    }
    .prof-specialty {
      font-size: 0.78rem;
      color: var(--text-mid);
      margin-bottom: 8px;
      line-height: 1.4;
    }
    .prof-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 8px; }
    .prof-email {
      font-size: 0.76rem;
      color: var(--primary);
      text-decoration: none;
      display: block;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .prof-email:hover { color: var(--accent); }
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 14px;
      margin-top: 28px;
    }
    .pagination .chip:disabled { opacity: 0.45; cursor: not-allowed; }
    .page-info { font-size: 0.85rem; color: var(--text-mid); font-weight: 600; }
    @media (max-width: 768px) { .filters { grid-template-columns: 1fr; } }
  `]
})
export class ProfessorsComponent implements OnInit {
  private academic = inject(AcademicService);

  readonly allProfs = signal<Professor[]>([]);
  readonly departments = signal<Department[]>([]);
  readonly loading = signal(true);

  readonly page = signal(1);
  pageSize = 12;
  readonly search = signal('');
  readonly selectedDept = signal<number | null>(null);
  readonly selectedGrade = signal<string | null>(null);

  readonly filtered = computed(() => {
    let list = this.allProfs();
    const dep = this.selectedDept();
    const grade = this.selectedGrade();
    const q = this.search().toLowerCase().trim();
    if (dep) list = list.filter(p => p.department_id === dep);
    if (grade) list = list.filter(p => p.grade === grade);
    if (q) list = list.filter(p =>
      (p.first_name + ' ' + p.last_name).toLowerCase().includes(q) ||
      (p.specialty?.toLowerCase().includes(q)) ||
      (p.email?.toLowerCase().includes(q))
    );
    return list;
  });
  readonly total = computed(() => this.filtered().length);
  readonly totalPages = computed(() => Math.max(1, Math.ceil(this.total() / this.pageSize)));
  readonly professors = computed(() => {
    const start = (this.page() - 1) * this.pageSize;
    return this.filtered().slice(start, start + this.pageSize);
  });

  ngOnInit() {
    this.academic.getDepartments().pipe(catchError(() => of([])))
      .subscribe(d => this.departments.set(d));
    // Charge TOUS les professeurs une fois, puis filtrage client-side reactif
    this.academic.getProfessors(undefined, 1, 500)
      .pipe(catchError(() => of({ items: [], total: 0 })))
      .subscribe((res: any) => {
        this.allProfs.set(res.items || []);
        this.loading.set(false);
      });
  }

  changePage(p: number) {
    if (p < 1 || p > this.totalPages()) return;
    this.page.set(p);
  }

  initials(p: Professor): string {
    return (p.first_name?.[0] || '') + (p.last_name?.[0] || '');
  }

  gradeLabel(g: string): string {
    return { PES: 'PES', PH: 'PH', PA: 'PA', VACATAIRE: 'Vacataire', EMERITE: 'Émérite' }[g] || g;
  }
}
