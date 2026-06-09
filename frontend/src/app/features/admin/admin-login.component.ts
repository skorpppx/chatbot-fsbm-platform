import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="login-wrap">
      <div class="login-card">
        <img src="assets/logos/fsbm.png" alt="FSBM" class="logo" />
        <h1>Espace Administration</h1>
        <p class="subtitle">Connecte-toi pour gérer la plateforme</p>

        <label class="lbl">Email</label>
        <input class="inp" type="email" [(ngModel)]="email" (keyup.enter)="submit()"
               placeholder="admin@fsbm.ac.ma" autocomplete="username" />

        <label class="lbl">Mot de passe</label>
        <input class="inp" type="password" [(ngModel)]="password" (keyup.enter)="submit()"
               placeholder="••••••••" autocomplete="current-password" />

        <div class="error" *ngIf="error()">⚠️ {{ error() }}</div>

        <button class="btn" [disabled]="loading() || !email || !password" (click)="submit()">
          {{ loading() ? 'Connexion…' : 'Se connecter' }}
        </button>

        <div class="hint">
          <strong>Démo :</strong> admin&#64;fsbm.ac.ma / Admin&#64;FSBM2026
        </div>
        <a class="back" href="/">← Retour à la plateforme</a>
      </div>
    </div>
  `,
  styles: [`
    .login-wrap { min-height: 100%; display: flex; align-items: center; justify-content: center;
                  padding: 40px 16px; background: linear-gradient(135deg, #1C3F6E, #2d5a9e); }
    .login-card { width: 100%; max-width: 380px; background: #fff; border-radius: 18px;
                  padding: 34px 30px; box-shadow: 0 20px 60px rgba(0,0,0,.25); text-align: center; }
    .logo { height: 64px; object-fit: contain; margin-bottom: 14px; }
    h1 { margin: 0 0 4px; font-size: 1.35rem; color: #1C3F6E; }
    .subtitle { margin: 0 0 22px; color: #7a8499; font-size: .88rem; }
    .lbl { display: block; text-align: left; font-size: .8rem; font-weight: 600; color: #5b6577;
           margin: 12px 0 6px; }
    .inp { width: 100%; box-sizing: border-box; border: 1px solid #dde1e8; border-radius: 10px;
           padding: 11px 13px; font-size: .92rem; font-family: inherit; }
    .inp:focus { outline: none; border-color: #1C3F6E; box-shadow: 0 0 0 3px rgba(28,63,110,.12); }
    .error { text-align: left; background: #fdecec; color: #c0392b; padding: 9px 12px;
             border-radius: 8px; font-size: .82rem; margin-top: 14px; }
    .btn { width: 100%; margin-top: 20px; background: #1C3F6E; color: #fff; border: none;
           border-radius: 10px; padding: 12px; font-size: .95rem; font-weight: 600; cursor: pointer; }
    .btn:hover:not(:disabled) { background: #16335a; }
    .btn:disabled { opacity: .5; cursor: not-allowed; }
    .hint { margin-top: 18px; font-size: .76rem; color: #9aa3b2; background: #f6f8fb;
            padding: 8px; border-radius: 8px; }
    .back { display: inline-block; margin-top: 16px; font-size: .82rem; color: #1C3F6E; text-decoration: none; }
    .back:hover { text-decoration: underline; }
  `],
})
export class AdminLoginComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  email = '';
  password = '';
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  submit() {
    if (!this.email || !this.password) return;
    this.loading.set(true);
    this.error.set(null);
    this.auth.login(this.email.trim(), this.password).subscribe({
      next: () => { this.loading.set(false); this.router.navigate(['/admin']); },
      error: (e) => {
        this.loading.set(false);
        this.error.set(e?.error?.detail || 'Email ou mot de passe incorrect.');
      },
    });
  }
}
