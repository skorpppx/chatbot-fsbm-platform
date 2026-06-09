import { Routes } from '@angular/router';
import { AppShellComponent } from './layout/app-shell.component';
import { adminGuard } from './core/auth.guard';

export const routes: Routes = [
  // ─── Espace public (avec sidebar + topbar) ──────────────────────────────────
  {
    path: '',
    component: AppShellComponent,
    children: [
      {
        path: '',
        pathMatch: 'full',
        loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
        title: 'Accueil — Chatbot FSBM',
      },
      {
        path: 'chat',
        loadComponent: () => import('./features/chat/chat-page.component').then(m => m.ChatPageComponent),
        title: 'Assistant IA — FSBM',
      },
      {
        path: 'departements',
        loadComponent: () => import('./features/departments/departments.component').then(m => m.DepartmentsComponent),
        title: 'Départements — FSBM',
      },
      {
        path: 'filieres',
        loadComponent: () => import('./features/filieres/filieres.component').then(m => m.FilieresComponent),
        title: 'Filières — FSBM',
      },
      {
        path: 'filieres/:code',
        loadComponent: () => import('./features/filieres/filiere-detail.component').then(m => m.FiliereDetailComponent),
        title: 'Détail filière — FSBM',
      },
      {
        path: 'modules',
        loadComponent: () => import('./features/modules/modules.component').then(m => m.ModulesComponent),
        title: 'Modules — FSBM',
      },
      {
        path: 'professeurs',
        loadComponent: () => import('./features/professors/professors.component').then(m => m.ProfessorsComponent),
        title: 'Professeurs — FSBM',
      },
      {
        path: 'actualites',
        loadComponent: () => import('./features/news/news.component').then(m => m.NewsComponent),
        title: 'Actualités — FSBM',
      },
      {
        path: 'vie-etudiante',
        loadComponent: () => import('./features/student-life/student-life.component').then(m => m.StudentLifeComponent),
        title: 'Vie étudiante — FSBM',
      },
      {
        path: 'avis',
        loadComponent: () => import('./features/reviews/reviews.component').then(m => m.ReviewsComponent),
        title: 'Avis & Recommandations — FSBM',
      },
    ],
  },

  // ─── Espace admin (plein écran, sans sidebar) ────────────────────────────────
  {
    path: 'admin/login',
    loadComponent: () => import('./features/admin/admin-login.component').then(m => m.AdminLoginComponent),
    title: 'Connexion Admin — FSBM',
  },
  {
    path: 'admin',
    canActivate: [adminGuard],
    loadComponent: () => import('./features/admin/admin.component').then(m => m.AdminComponent),
    title: 'Administration — FSBM',
  },

  { path: '**', redirectTo: '' },
];
