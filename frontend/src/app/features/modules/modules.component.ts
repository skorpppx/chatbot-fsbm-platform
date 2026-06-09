import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AcademicService, Module, Filiere } from '../../services/academic.service';
import { catchError, of, forkJoin } from 'rxjs';

@Component({
  selector: 'app-modules',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">📖</div>
        <div>
          <h1 class="page-title">Modules & Matières</h1>
          <p class="page-subtitle">{{ filtered().length }} module{{ filtered().length > 1 ? 's' : '' }} · <em>programmes indicatifs (données de simulation — la liste officielle des modules n'est pas publiée sur fsbm.ma)</em></p>
        </div>
      </div>
    </div>

    <div class="filters fade-in-up">
      <input class="input" type="search" placeholder="🔎 Rechercher un module..."
             [ngModel]="search()" (ngModelChange)="search.set($event)" />
      <select class="select" [ngModel]="selectedFiliere()" (ngModelChange)="selectedFiliere.set($event)">
        <option [ngValue]="null">Toutes les filières</option>
        <option *ngFor="let f of filieres()" [ngValue]="f.id">{{ f.code }} — {{ f.name }}</option>
      </select>
      <select class="select" [ngModel]="selectedSemester()" (ngModelChange)="selectedSemester.set($event)">
        <option [ngValue]="null">Tous les semestres</option>
        <option *ngFor="let s of [1,2,3,4,5,6]" [ngValue]="s">Semestre {{ s }}</option>
      </select>
    </div>

    <div *ngIf="loading()" class="grid grid-3">
      <div *ngFor="let i of [1,2,3,4,5,6]" class="card"><div class="skeleton" style="height: 130px;"></div></div>
    </div>

    <div *ngIf="!loading() && filtered().length > 0" class="modules-grid fade-in-up">
      <div *ngFor="let m of filtered(); let i = index" class="module-card"
           [style.animation-delay.ms]="(i % 12) * 25">
        <div class="mod-top">
          <span class="mod-code-pill">{{ m.code }}</span>
          <span class="mod-semester">S{{ m.semester }}</span>
        </div>
        <h3 class="mod-title">{{ m.name }}</h3>
        <p class="mod-desc">{{ m.description?.slice(0, 90) || 'Aucune description.' }}{{ (m.description?.length || 0) > 90 ? '…' : '' }}</p>
        <div class="mod-meta">
          <div class="meta-pill">
            <span>💯</span> {{ m.credits }} ECTS
          </div>
          <div class="meta-pill">
            <span>⚖️</span> Coef. {{ m.coefficient }}
          </div>
          <div class="meta-pill">
            <span>⏱️</span> {{ m.hours_cours + m.hours_td + m.hours_tp }}h
          </div>
        </div>
        <div class="mod-hours-breakdown" *ngIf="m.hours_cours || m.hours_td || m.hours_tp">
          <span *ngIf="m.hours_cours" class="hours-tag cours">{{ m.hours_cours }}h cours</span>
          <span *ngIf="m.hours_td"    class="hours-tag td">{{ m.hours_td }}h TD</span>
          <span *ngIf="m.hours_tp"    class="hours-tag tp">{{ m.hours_tp }}h TP</span>
        </div>
      </div>
    </div>

    <div *ngIf="!loading() && filtered().length === 0" class="empty-state">
      <div class="empty-state-icon">📚</div>
      <div class="empty-state-title">Aucun module ne correspond aux filtres</div>
    </div>
  `,
  styles: [`
    .filters {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 12px;
      margin-bottom: 24px;
    }
    .modules-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }
    .module-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s;
      animation: fadeInUp 0.35s ease both;
    }
    .module-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent);
    }
    .mod-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .mod-code-pill {
      background: var(--primary-pale);
      color: var(--primary);
      font-weight: 800;
      font-size: 0.72rem;
      padding: 3px 10px;
      border-radius: var(--radius-full);
      letter-spacing: 0.04em;
    }
    .mod-semester {
      background: var(--accent-pale);
      color: var(--accent);
      font-weight: 700;
      font-size: 0.72rem;
      padding: 3px 10px;
      border-radius: var(--radius-full);
    }
    .mod-title {
      font-size: 0.98rem;
      font-weight: 700;
      color: var(--text-dark);
      line-height: 1.3;
      margin-bottom: 8px;
      min-height: 2.6em;
    }
    .mod-desc {
      font-size: 0.82rem;
      color: var(--text-mid);
      line-height: 1.5;
      margin-bottom: 12px;
    }
    .mod-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
    }
    .meta-pill {
      background: var(--bg);
      color: var(--text-mid);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 4px;
      border: 1px solid var(--border-soft);
    }
    .mod-hours-breakdown { display: flex; flex-wrap: wrap; gap: 5px; padding-top: 8px; border-top: 1px dashed var(--border-soft); }
    .hours-tag {
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 6px;
    }
    .hours-tag.cours { background: rgba(58,123,213,0.12); color: var(--primary-mid); }
    .hours-tag.td    { background: rgba(22,181,166,0.12); color: var(--accent); }
    .hours-tag.tp    { background: rgba(245,158,11,0.12); color: #B45309; }

    @media (max-width: 768px) {
      .filters { grid-template-columns: 1fr; }
    }
  `]
})
export class ModulesComponent implements OnInit {
  private academic = inject(AcademicService);

  readonly modules = signal<Module[]>([]);
  readonly filieres = signal<Filiere[]>([]);
  readonly loading = signal(true);

  readonly search = signal('');
  readonly selectedFiliere = signal<number | null>(null);
  readonly selectedSemester = signal<number | null>(null);

  readonly filtered = computed(() => {
    let list = this.modules();
    const fil = this.selectedFiliere();
    const sem = this.selectedSemester();
    if (fil) list = list.filter(m => m.filiere_id === fil);
    if (sem) list = list.filter(m => m.semester === sem);
    const q = this.search().toLowerCase().trim();
    if (q) list = list.filter(m =>
      m.name.toLowerCase().includes(q) || m.code.toLowerCase().includes(q)
    );
    return list;
  });

  ngOnInit() {
    forkJoin({
      modules: this.academic.getModules().pipe(catchError(() => of([]))),
      filieres: this.academic.getFilieres().pipe(catchError(() => of([]))),
    }).subscribe(({ modules, filieres }) => {
      this.modules.set(modules);
      this.filieres.set(filieres);
      this.loading.set(false);
    });
  }
}
