import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AcademicService, Department } from '../../services/academic.service';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-departments',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="page-header fade-in-up">
      <div class="page-header-left">
        <div class="page-icon-wrap">🏢</div>
        <div>
          <h1 class="page-title">Départements</h1>
          <p class="page-subtitle">Les 5 départements académiques de la FSBM</p>
        </div>
      </div>
    </div>

    <div *ngIf="loading()" class="grid grid-2">
      <div *ngFor="let i of [1,2,3,4,5]" class="card">
        <div class="skeleton" style="height: 140px;"></div>
      </div>
    </div>

    <div *ngIf="!loading() && departments().length > 0" class="grid grid-2 fade-in-up">
      <div *ngFor="let d of departments(); let i = index"
           class="dept-card"
           [style.animation-delay.ms]="i * 60"
           [style.--dept-color]="d.color_hex || '#1C3F6E'">
        <div class="dept-header">
          <div class="dept-icon">
            <img *ngIf="d.logo_url" [src]="d.logo_url" [alt]="d.name" />
            <span *ngIf="!d.logo_url">🏛️</span>
          </div>
          <div>
            <div class="dept-code-badge">{{ d.code }}</div>
            <h3 class="dept-name">{{ d.name }}</h3>
          </div>
        </div>
        <p class="dept-desc">{{ d.description }}</p>
        <div class="dept-meta">
          <div class="meta-item">
            <span class="meta-label">👔 Chef du département</span>
            <span class="meta-value">{{ d.head_name || '—' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">📧 Email</span>
            <span class="meta-value">{{ d.head_email || '—' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">📞 Téléphone</span>
            <span class="meta-value">{{ d.head_phone || '—' }}</span>
          </div>
        </div>
        <div class="dept-actions">
          <a [routerLink]="['/filieres']" [queryParams]="{ dept: d.id }" class="btn btn-primary">
            Voir les filières →
          </a>
        </div>
      </div>
    </div>

    <div *ngIf="!loading() && departments().length === 0" class="empty-state">
      <div class="empty-state-icon">😕</div>
      <div class="empty-state-title">Aucun département trouvé</div>
      <p>Vérifie que l'academic-service tourne sur le port 5002.</p>
    </div>
  `,
  styles: [`
    .dept-card {
      position: relative;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 24px;
      box-shadow: var(--shadow-sm);
      transition: all 0.3s ease;
      animation: fadeInUp 0.4s ease both;
      overflow: hidden;
    }
    .dept-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 4px;
      background: var(--dept-color, var(--primary));
    }
    .dept-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
    }
    .dept-header { display: flex; gap: 14px; margin-bottom: 14px; }
    .dept-icon {
      width: 56px; height: 56px;
      background: color-mix(in srgb, var(--dept-color) 14%, transparent);
      border-radius: var(--radius-md);
      display: flex; align-items: center; justify-content: center;
      font-size: 1.7rem;
      flex-shrink: 0;
    }
    .dept-icon img { width: 100%; height: 100%; object-fit: contain; padding: 6px; }
    .dept-code-badge {
      display: inline-block;
      background: var(--dept-color, var(--primary));
      color: #fff;
      font-size: 0.7rem; font-weight: 800;
      padding: 3px 10px;
      border-radius: var(--radius-full);
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .dept-name {
      font-size: 1.05rem; font-weight: 700;
      color: var(--text-dark);
      line-height: 1.25;
    }
    .dept-desc {
      font-size: 0.88rem;
      color: var(--text-mid);
      margin-bottom: 14px;
      line-height: 1.55;
    }
    .dept-meta {
      display: flex; flex-direction: column; gap: 6px;
      padding: 12px 14px;
      background: var(--bg);
      border-radius: var(--radius-sm);
      margin-bottom: 14px;
    }
    .meta-item { display: flex; justify-content: space-between; gap: 10px; font-size: 0.78rem; }
    .meta-label { color: var(--text-light); font-weight: 500; }
    .meta-value { color: var(--text-dark); font-weight: 600; text-align: right; word-break: break-word; }
    .dept-actions { display: flex; gap: 10px; }
  `]
})
export class DepartmentsComponent implements OnInit {
  private academic = inject(AcademicService);
  readonly departments = signal<Department[]>([]);
  readonly loading = signal(true);

  ngOnInit() {
    this.academic.getDepartments().pipe(catchError(() => of([])))
      .subscribe(d => { this.departments.set(d); this.loading.set(false); });
  }
}
