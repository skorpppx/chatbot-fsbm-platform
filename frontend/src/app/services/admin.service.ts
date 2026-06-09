import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/** Service CRUD admin — toutes les requêtes sont authentifiées via auth.interceptor. */

export interface FaqItem {
  id: number;
  intent_tag: string;
  question: string;
  answer: string;
  category_id?: number | null;
  keywords?: string | null;
  related_url?: string | null;
  consultations?: number;
  is_active: boolean;
}

export interface AdminAnnouncement {
  id: number;
  title: string;
  content: string;
  type: string;
  author?: string | null;
  target_filiere?: number | null;
  target_year?: number | null;
  published_at?: string;
  expires_at?: string | null;
  is_pinned: boolean;
  image_url?: string | null;
  attachment_url?: string | null;
}

export interface AdminEvent {
  id: number;
  title: string;
  description?: string | null;
  event_type: string;
  start_date: string;
  end_date?: string | null;
  location?: string | null;
  organizer?: string | null;
  registration_url?: string | null;
  image_url?: string | null;
  attachment_url?: string | null;
}

export interface AdminClub {
  id: number;
  name: string;
  description?: string | null;
  category: string;
  president?: string | null;
  contact_email?: string | null;
  logo_url?: string | null;
  members_count?: number;
  is_active: boolean;
}

export interface UploadResult {
  url: string;
  filename: string;
  original_name: string;
  kind: 'image' | 'pdf';
  size: number;
}

@Injectable({ providedIn: 'root' })
export class AdminService {
  private http = inject(HttpClient);
  private base = '/api/academic/admin';

  // ─── Annonces ───────────────────────────────────────────────────────────────
  listAnnouncements(): Observable<AdminAnnouncement[]> {
    return this.http.get<AdminAnnouncement[]>(`${this.base}/announcements`);
  }
  createAnnouncement(body: Partial<AdminAnnouncement>): Observable<AdminAnnouncement> {
    return this.http.post<AdminAnnouncement>(`${this.base}/announcements`, body);
  }
  updateAnnouncement(id: number, body: Partial<AdminAnnouncement>): Observable<AdminAnnouncement> {
    return this.http.put<AdminAnnouncement>(`${this.base}/announcements/${id}`, body);
  }
  deleteAnnouncement(id: number): Observable<any> {
    return this.http.delete(`${this.base}/announcements/${id}`);
  }

  // ─── Événements ───────────────────────────────────────────────────────────────
  listEvents(): Observable<AdminEvent[]> {
    return this.http.get<AdminEvent[]>(`${this.base}/events`);
  }
  createEvent(body: Partial<AdminEvent>): Observable<AdminEvent> {
    return this.http.post<AdminEvent>(`${this.base}/events`, body);
  }
  updateEvent(id: number, body: Partial<AdminEvent>): Observable<AdminEvent> {
    return this.http.put<AdminEvent>(`${this.base}/events/${id}`, body);
  }
  deleteEvent(id: number): Observable<any> {
    return this.http.delete(`${this.base}/events/${id}`);
  }

  // ─── Filières ─────────────────────────────────────────────────────────────────
  createFiliere(body: any): Observable<any> { return this.http.post(`${this.base}/filieres`, body); }
  updateFiliere(id: number, body: any): Observable<any> { return this.http.put(`${this.base}/filieres/${id}`, body); }
  deleteFiliere(id: number): Observable<any> { return this.http.delete(`${this.base}/filieres/${id}`); }

  // ─── Modules ──────────────────────────────────────────────────────────────────
  createModule(body: any): Observable<any> { return this.http.post(`${this.base}/modules`, body); }
  updateModule(id: number, body: any): Observable<any> { return this.http.put(`${this.base}/modules/${id}`, body); }
  deleteModule(id: number): Observable<any> { return this.http.delete(`${this.base}/modules/${id}`); }

  // ─── Professeurs ──────────────────────────────────────────────────────────────
  createProfessor(body: any): Observable<any> { return this.http.post(`${this.base}/professors`, body); }
  updateProfessor(id: number, body: any): Observable<any> { return this.http.put(`${this.base}/professors/${id}`, body); }
  deleteProfessor(id: number): Observable<any> { return this.http.delete(`${this.base}/professors/${id}`); }

  // ─── FAQ ──────────────────────────────────────────────────────────────────────
  listFaq(): Observable<FaqItem[]> { return this.http.get<FaqItem[]>(`${this.base}/faq`); }
  createFaq(body: Partial<FaqItem>): Observable<FaqItem> { return this.http.post<FaqItem>(`${this.base}/faq`, body); }
  updateFaq(id: number, body: Partial<FaqItem>): Observable<FaqItem> { return this.http.put<FaqItem>(`${this.base}/faq/${id}`, body); }
  deleteFaq(id: number): Observable<any> { return this.http.delete(`${this.base}/faq/${id}`); }

  // ─── Départements ───────────────────────────────────────────────────────────
  createDepartment(body: any): Observable<any> { return this.http.post(`${this.base}/departments`, body); }
  updateDepartment(id: number, body: any): Observable<any> { return this.http.put(`${this.base}/departments/${id}`, body); }
  deleteDepartment(id: number): Observable<any> { return this.http.delete(`${this.base}/departments/${id}`); }

  // ─── Clubs (vie étudiante) ──────────────────────────────────────────────────
  listClubs(): Observable<AdminClub[]> { return this.http.get<AdminClub[]>(`${this.base}/clubs`); }
  createClub(body: Partial<AdminClub>): Observable<AdminClub> { return this.http.post<AdminClub>(`${this.base}/clubs`, body); }
  updateClub(id: number, body: Partial<AdminClub>): Observable<AdminClub> { return this.http.put<AdminClub>(`${this.base}/clubs/${id}`, body); }
  deleteClub(id: number): Observable<any> { return this.http.delete(`${this.base}/clubs/${id}`); }

  // ─── Upload fichier (image ou PDF) ──────────────────────────────────────────
  upload(file: File): Observable<UploadResult> {
    const fd = new FormData();
    fd.append('file', file);
    return this.http.post<UploadResult>(`${this.base}/upload`, fd);
  }
}
