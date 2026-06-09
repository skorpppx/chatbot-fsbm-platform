import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, ActivatedRoute } from '@angular/router';
import { AcademicService, Filiere } from '../../services/academic.service';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-filieres',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">📚</div>
        <div>
          <h1 class="page-title">Filières</h1>
          <p class="page-subtitle">{{ filtered().length }} filière{{ filtered().length > 1 ? 's' : '' }} — Licences, Masters, Doctorat</p>
        </div>
      </div>
    </div>

    <!-- ═══════ FILTRES ═══════ -->
    <div class="filters fade-in-up">
      <div class="search-box">
        <span class="search-icon">🔎</span>
        <input class="input" type="search" placeholder="Rechercher une filière (nom, code, débouché)..."
               [(ngModel)]="searchQuery" (ngModelChange)="onSearch()" />
      </div>
      <div class="filter-chips">
        <button *ngFor="let f of typeFilters" class="chip"
                [class.active]="selectedType() === f.value"
                (click)="filterByType(f.value)">
          <span>{{ f.icon }}</span>{{ f.label }}
        </button>
      </div>
    </div>

    <!-- ═══════ GRID ═══════ -->
    <div *ngIf="loading()" class="grid grid-3">
      <div *ngFor="let i of [1,2,3,4,5,6]" class="card">
        <div class="skeleton" style="height: 180px;"></div>
      </div>
    </div>

    <div *ngIf="!loading() && filtered().length > 0" class="grid grid-3 fade-in-up">
      <a *ngFor="let f of filtered(); let i = index"
         [routerLink]="['/filieres', f.code]"
         class="filiere-card"
         [class.master]="f.type.startsWith('MASTER')"
         [class.doctorat]="f.type === 'DOCTORAT'"
         [style.animation-delay.ms]="i * 35">
        <div class="filiere-header">
          <span class="filiere-code">{{ f.code }}</span>
          <span class="badge" [class.badge-primary]="f.type === 'LICENCE' || f.type === 'LICENCE_PRO'"
                              [class.badge-accent]="f.type.startsWith('MASTER')">
            {{ typeLabel(f.type) }}
          </span>
        </div>
        <h3 class="filiere-name">{{ f.name }}</h3>
        <p class="filiere-desc">{{ f.description?.slice(0, 110) }}{{ (f.description?.length || 0) > 110 ? '…' : '' }}</p>
        <div class="filiere-footer">
          <div class="filiere-stat">
            <span class="stat-label">Capacité</span>
            <span class="stat-value">{{ f.capacity }}</span>
          </div>
          <div class="filiere-stat">
            <span class="stat-label">Durée</span>
            <span class="stat-value">{{ f.duration_years }} an{{ f.duration_years > 1 ? 's' : '' }}</span>
          </div>
          <div class="filiere-stat">
            <span class="stat-label">Coordinateur</span>
            <span class="stat-value coord">{{ shortCoord(f.coordinator) }}</span>
          </div>
        </div>
      </a>
    </div>

    <div *ngIf="!loading() && filtered().length === 0" class="empty-state">
      <div class="empty-state-icon">🔍</div>
      <div class="empty-state-title">Aucune filière ne correspond</div>
      <p>Essayez de modifier votre recherche ou changez le filtre.</p>
    </div>
  `,
  styles: [`
    .filters {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 28px;
    }
    .search-box { position: relative; }
    .search-box .input { padding-left: 42px; }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1rem;
      color: var(--text-light);
    }
    .filter-chips { display: flex; flex-wrap: wrap; gap: 8px; }
    .filter-chips .chip span { font-size: 1rem; }

    .filiere-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 22px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s;
      animation: fadeInUp 0.4s ease both;
      text-decoration: none;
      color: inherit;
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      overflow: hidden;
    }
    .filiere-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--primary) 0%, var(--primary-mid) 100%);
    }
    .filiere-card.master::before {
      background: linear-gradient(90deg, var(--accent) 0%, var(--accent-mid) 100%);
    }
    .filiere-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
      border-color: var(--primary-light);
    }
    .filiere-card.master:hover { border-color: var(--accent); }

    .filiere-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
    }
    .filiere-code {
      font-size: 1rem;
      font-weight: 800;
      color: var(--primary);
      letter-spacing: 0.05em;
    }
    .filiere-card.master .filiere-code { color: var(--accent); }

    .filiere-name {
      font-size: 1.02rem;
      font-weight: 700;
      color: var(--text-dark);
      line-height: 1.3;
      min-height: 2.6em;
    }
    .filiere-desc {
      font-size: 0.85rem;
      color: var(--text-mid);
      line-height: 1.55;
      flex: 1;
    }
    .filiere-footer {
      display: flex;
      gap: 8px;
      padding-top: 12px;
      border-top: 1px solid var(--border-soft);
    }
    .filiere-stat {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }
    .filiere-stat .stat-label {
      font-size: 0.68rem;
      color: var(--text-light);
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .filiere-stat .stat-value {
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-dark);
    }
    .filiere-stat .coord { font-size: 0.78rem; font-weight: 600; overflow: hidden; text-overflow: ellipsis; }
  `]
})
export class FilieresComponent implements OnInit {
  private academic = inject(AcademicService);
  private route = inject(ActivatedRoute);

  readonly filieres = signal<Filiere[]>([]);
  readonly loading = signal(true);
  readonly selectedType = signal<string | null>(null);

  readonly searchQuery = signal('');
  debounceHandle: any;

  readonly typeFilters = [
    { label: 'Toutes',           value: null,                 icon: '✨' },
    { label: 'Licences',         value: 'LICENCE',            icon: '📘' },
    { label: 'Licence Pro',      value: 'LICENCE_PRO',        icon: '💼' },
    { label: 'Masters',          value: 'MASTER',             icon: '🎓' },
    { label: 'Master Recherche', value: 'MASTER_RECHERCHE',   icon: '🔬' },
  ];

  readonly filtered = computed(() => {
    let list = this.filieres();
    const t = this.selectedType();
    const q = this.searchQuery().toLowerCase().trim();
    if (t) list = list.filter(f => f.type === t);
    if (q) list = list.filter(f =>
      f.name.toLowerCase().includes(q) ||
      f.code.toLowerCase().includes(q) ||
      (f.careers?.toLowerCase().includes(q))
    );
    return list;
  });

  ngOnInit() {
    this.route.queryParams.subscribe(p => {
      if (p['type']) this.selectedType.set(p['type']);
    });
    this.load();
  }

  load() {
    this.academic.getFilieres().pipe(catchError(() => of([])))
      .subscribe(f => { this.filieres.set(f); this.loading.set(false); });
  }

  filterByType(value: string | null) { this.selectedType.set(value); }

  onSearch() {
    clearTimeout(this.debounceHandle);
    this.debounceHandle = setTimeout(() => { /* signal auto-updates */ }, 250);
  }

  shortCoord(name?: string): string {
    if (!name) return '—';
    return name.split(' ').slice(0, 2).join(' ');
  }

  typeLabel(type: string): string {
    switch (type) {
      case 'LICENCE':         return 'Licence';
      case 'LICENCE_PRO':     return 'Pro';
      case 'MASTER':          return 'Master';
      case 'MASTER_RECHERCHE':return 'M. Recherche';
      case 'DOCTORAT':        return 'Doctorat';
      default: return type;
    }
  }
}
