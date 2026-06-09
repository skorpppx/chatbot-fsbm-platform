import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AcademicService, Overview, Announcement } from '../../services/academic.service';
import { catchError, of } from 'rxjs';

interface StatCard {
  label: string;
  value: number | string;
  icon: string;
  color: string;
  route?: string;
  delta?: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {
  private academic = inject(AcademicService);

  readonly overview = signal<Overview | null>(null);
  readonly announcements = signal<Announcement[]>([]);
  readonly events = signal<any[]>([]);
  readonly loading = signal(true);
  readonly backendOnline = signal(true);

  readonly quickActions = [
    { icon: '🤖', label: 'Poser une question', route: '/chat',          color: 'accent' },
    { icon: '🏢', label: 'Voir les départements', route: '/departements',color: 'primary' },
    { icon: '📚', label: 'Explorer les filières', route: '/filieres',    color: 'primary' },
    { icon: '📰', label: 'Dernières actualités',  route: '/actualites',  color: 'primary' },
  ];

  get stats(): StatCard[] {
    const o = this.overview();
    if (!o) {
      return [
        { label: 'Départements', value: '—', icon: '🏢', color: 'primary', route: '/departements' },
        { label: 'Filières',     value: '—', icon: '📚', color: 'accent',  route: '/filieres' },
        { label: 'Modules',      value: '—', icon: '📖', color: 'primary', route: '/modules' },
        { label: 'Professeurs',  value: '—', icon: '👨‍🏫', color: 'accent', route: '/professeurs' },
      ];
    }
    return [
      { label: 'Départements', value: o.departments,           icon: '🏢',  color: 'primary', route: '/departements', delta: 'académiques' },
      { label: 'Filières',     value: o.filieres,              icon: '📚',  color: 'accent',  route: '/filieres',     delta: `${o.filieres_by_type?.['LICENCE'] || 0}L + ${(o.filieres_by_type?.['MASTER'] || 0) + (o.filieres_by_type?.['MASTER_RECHERCHE'] || 0)}M` },
      { label: 'Modules',      value: o.modules,               icon: '📖',  color: 'primary', route: '/modules',      delta: 'matières' },
      { label: 'Professeurs',  value: o.professors,            icon: '👨‍🏫', color: 'accent', route: '/professeurs',  delta: 'enseignants' },
      { label: 'Étudiants',    value: o.students.toLocaleString('fr-FR'), icon: '🎓', color: 'primary', delta: 'étudiantes et étudiants' },
      { label: 'Laboratoires', value: o.laboratoires ?? 12,    icon: '🔬',  color: 'accent',  delta: 'de recherche' },
      { label: 'Partenaires',  value: o.entreprises_partenaires ?? 160, icon: '🤝', color: 'primary', delta: 'entreprises & mécènes' },
      { label: 'Événements',   value: o.events,                icon: '🎉',  color: 'accent',  route: '/actualites',   delta: 'à venir' },
      { label: 'Annonces',     value: o.announcements,         icon: '📣',  color: 'primary', route: '/actualites',   delta: 'publiées' },
      { label: 'Clubs',        value: o.clubs,                 icon: '🌟',  color: 'accent',  route: '/vie-etudiante',delta: 'actifs' },
    ];
  }

  get doyen(): string { return this.overview()?.doyen || ''; }
  get doyenMessage(): string { return this.overview()?.doyen_message || ''; }

  ngOnInit() {
    this.academic.getOverview().pipe(
      catchError(() => { this.backendOnline.set(false); return of(null); })
    ).subscribe(o => {
      this.overview.set(o);
      this.loading.set(false);
    });

    this.academic.getAnnouncements(4).pipe(
      catchError(() => of([]))
    ).subscribe(a => this.announcements.set(a));

    this.academic.getEvents(true).pipe(
      catchError(() => of([]))
    ).subscribe(e => this.events.set(e.slice(0, 3)));
  }

  formatDate(date: string): string {
    return new Date(date).toLocaleDateString('fr-FR', {
      day: '2-digit', month: 'short', year: 'numeric'
    });
  }

  formatDateTime(date: string): string {
    return new Date(date).toLocaleDateString('fr-FR', {
      day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
    });
  }
}
