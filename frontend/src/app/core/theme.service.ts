import { Injectable, signal } from '@angular/core';

/** Service de thème — gère mode sombre / clair avec persistance localStorage. */
@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly STORAGE_KEY = 'fsbm-theme';
  readonly theme = signal<'light' | 'dark'>('light');

  constructor() {
    const stored = (typeof window !== 'undefined' ? localStorage.getItem(this.STORAGE_KEY) : null) as 'light' | 'dark' | null;
    const initial = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    this.applyTheme(initial);
  }

  toggle() {
    this.applyTheme(this.theme() === 'light' ? 'dark' : 'light');
  }

  private applyTheme(value: 'light' | 'dark') {
    this.theme.set(value);
    document.documentElement.setAttribute('data-theme', value);
    if (typeof window !== 'undefined') localStorage.setItem(this.STORAGE_KEY, value);
  }
}
