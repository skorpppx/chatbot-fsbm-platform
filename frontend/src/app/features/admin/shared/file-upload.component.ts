import { Component, EventEmitter, Input, Output, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../../services/admin.service';

/**
 * Widget réutilisable d'upload de fichier (image ou PDF).
 * Usage :  <app-file-upload [(url)]="form.photo_url" kind="image" label="Photo" />
 */
@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="fu">
      <label class="fu-label" *ngIf="label">{{ label }}</label>

      <div class="fu-row">
        <!-- Aperçu -->
        <div class="fu-preview" *ngIf="url">
          <img *ngIf="isImage()" [src]="url" alt="aperçu" />
          <a *ngIf="!isImage()" [href]="url" target="_blank" class="pdf-chip">📄 Voir le PDF</a>
        </div>
        <div class="fu-placeholder" *ngIf="!url">{{ kind === 'pdf' ? '📄' : '🖼️' }}</div>

        <div class="fu-actions">
          <input #fileInput type="file" hidden [accept]="acceptAttr()"
                 (change)="onFile($event)" />
          <button type="button" class="fu-btn" (click)="fileInput.click()" [disabled]="uploading()">
            {{ uploading() ? 'Envoi…' : (url ? 'Remplacer' : 'Choisir un fichier') }}
          </button>
          <button type="button" class="fu-clear" *ngIf="url" (click)="clear()">Retirer</button>
        </div>
      </div>

      <input class="fu-manual" [ngModel]="url" (ngModelChange)="setUrl($event)"
             placeholder="…ou colle une URL d'image/PDF" />
      <div class="fu-err" *ngIf="error()">{{ error() }}</div>
    </div>
  `,
  styles: [`
    .fu { margin: 6px 0 2px; }
    .fu-label { display: block; font-size: .8rem; font-weight: 600; color: #5b6577; margin: 0 0 5px; }
    .fu-row { display: flex; align-items: center; gap: 12px; }
    .fu-preview img { width: 56px; height: 56px; object-fit: cover; border-radius: 8px; border: 1px solid #dde1e8; }
    .pdf-chip { font-size: .8rem; color: #1C3F6E; text-decoration: none; background: #eef2f7; padding: 8px 10px; border-radius: 8px; }
    .fu-placeholder { width: 56px; height: 56px; display: flex; align-items: center; justify-content: center;
                      background: #f6f8fb; border: 1px dashed #cfd6e0; border-radius: 8px; font-size: 1.4rem; }
    .fu-actions { display: flex; gap: 6px; }
    .fu-btn { background: #eef2f7; color: #1C3F6E; border: 1px solid #d6deea; border-radius: 8px;
              padding: 7px 12px; cursor: pointer; font-size: .82rem; font-weight: 600; }
    .fu-btn:hover:not(:disabled) { background: #e2e9f3; }
    .fu-btn:disabled { opacity: .6; cursor: wait; }
    .fu-clear { background: none; border: none; color: #c0392b; cursor: pointer; font-size: .78rem; }
    .fu-manual { width: 100%; box-sizing: border-box; margin-top: 8px; border: 1px solid #dde1e8;
                 border-radius: 8px; padding: 7px 10px; font-size: .8rem; font-family: inherit; }
    .fu-err { color: #c0392b; font-size: .78rem; margin-top: 4px; }
  `],
})
export class FileUploadComponent {
  private admin = inject(AdminService);

  @Input() url: string | null | undefined = '';
  @Output() urlChange = new EventEmitter<string>();
  @Input() kind: 'image' | 'pdf' | 'any' = 'image';
  @Input() label = '';

  readonly uploading = signal(false);
  readonly error = signal<string | null>(null);

  isImage(): boolean {
    const u = (this.url || '').toLowerCase();
    if (this.kind === 'pdf') return false;
    return !u.endsWith('.pdf');
  }

  acceptAttr(): string {
    if (this.kind === 'image') return 'image/*';
    if (this.kind === 'pdf') return 'application/pdf';
    return 'image/*,application/pdf';
  }

  onFile(ev: Event) {
    const input = ev.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    this.uploading.set(true);
    this.error.set(null);
    this.admin.upload(file).subscribe({
      next: (res) => { this.uploading.set(false); this.setUrl(res.url); },
      error: (e) => { this.uploading.set(false); this.error.set(e?.error?.detail || 'Échec de l upload.'); },
    });
    input.value = '';
  }

  setUrl(u: string) { this.url = u; this.urlChange.emit(u); }
  clear() { this.setUrl(''); }
}
