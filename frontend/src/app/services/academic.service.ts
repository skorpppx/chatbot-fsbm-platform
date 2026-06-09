import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * Service Angular pour consommer le academic-service (port 5002).
 * Routes proxifiées via /api/academic → http://localhost:5002/api
 */

export interface Department {
  id: number;
  code: string;
  name: string;
  name_short?: string;
  description?: string;
  head_name?: string;
  head_email?: string;
  head_phone?: string;
  color_hex?: string;
  logo_url?: string;
}

export interface Filiere {
  id: number;
  code: string;
  name: string;
  type: string;
  department_id: number;
  coordinator?: string;
  capacity: number;
  duration_years: number;
  description?: string;
  careers?: string;
  logo_url?: string;
  is_active: boolean;
}

export interface Module {
  id: number;
  code: string;
  name: string;
  filiere_id: number;
  semester: number;
  credits: number;
  coefficient: number;
  hours_cours: number;
  hours_td: number;
  hours_tp: number;
  description?: string;
}

export interface Professor {
  id: number;
  matricule: string;
  first_name: string;
  last_name: string;
  email: string;
  grade: string;
  department_id?: number;
  specialty?: string;
  bureau?: string;
  photo_url?: string;
  bio?: string;
}

export interface Overview {
  departments: number;
  filieres: number;
  modules: number;
  professors: number;
  students: number;
  events: number;
  announcements: number;
  clubs: number;
  laboratoires?: number;
  entreprises_partenaires?: number;
  doyen?: string;
  doyen_message?: string;
  filieres_by_type: Record<string, number>;
}

export interface Announcement {
  id: number;
  title: string;
  content: string;
  type: string;
  author?: string;
  published_at: string;
  is_pinned: boolean;
}

@Injectable({ providedIn: 'root' })
export class AcademicService {
  private apiUrl = '/api/academic';

  constructor(private http: HttpClient) {}

  // Overview
  getOverview(): Observable<Overview> {
    return this.http.get<Overview>(`${this.apiUrl}/overview`);
  }

  // Departments
  getDepartments(): Observable<Department[]> {
    return this.http.get<Department[]>(`${this.apiUrl}/departments`);
  }

  getDepartment(id: number): Observable<Department> {
    return this.http.get<Department>(`${this.apiUrl}/departments/${id}`);
  }

  // Filieres
  getFilieres(type?: string, departmentId?: number, search?: string): Observable<Filiere[]> {
    const params: any = {};
    if (type) params.type = type;
    if (departmentId) params.department_id = departmentId;
    if (search) params.search = search;
    return this.http.get<Filiere[]>(`${this.apiUrl}/filieres`, { params });
  }

  getFiliere(id: number): Observable<Filiere> {
    return this.http.get<Filiere>(`${this.apiUrl}/filieres/${id}`);
  }

  getFiliereByCode(code: string): Observable<Filiere> {
    return this.http.get<Filiere>(`${this.apiUrl}/filieres/code/${code}`);
  }

  getFiliereModules(filiereId: number, semester?: number): Observable<any> {
    const params: any = {};
    if (semester) params.semester = semester;
    return this.http.get<any>(`${this.apiUrl}/filieres/${filiereId}/modules`, { params });
  }

  // Modules
  getModules(filiereId?: number, semester?: number, search?: string): Observable<Module[]> {
    const params: any = {};
    if (filiereId) params.filiere_id = filiereId;
    if (semester) params.semester = semester;
    if (search) params.search = search;
    return this.http.get<Module[]>(`${this.apiUrl}/modules`, { params });
  }

  // Professors
  getProfessors(departmentId?: number, page = 1, pageSize = 20): Observable<any> {
    const params: any = { page, page_size: pageSize };
    if (departmentId) params.department_id = departmentId;
    return this.http.get<any>(`${this.apiUrl}/professors`, { params });
  }

  // Announcements & Events
  getAnnouncements(limit = 10): Observable<Announcement[]> {
    return this.http.get<Announcement[]>(`${this.apiUrl}/announcements`, { params: { limit } });
  }

  getEvents(upcomingOnly = true): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/events`, { params: { upcoming_only: upcomingOnly } });
  }

  getClubs(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/clubs`);
  }

  // Schedule & Exams
  getSchedule(filiereId: number, semester: number, group?: string): Observable<any> {
    const params: any = { filiere_id: filiereId, semester };
    if (group) params.group_name = group;
    return this.http.get<any>(`${this.apiUrl}/schedule`, { params });
  }

  getExams(filiereId?: number, session = 'NORMALE_S2'): Observable<any> {
    const params: any = { session };
    if (filiereId) params.filiere_id = filiereId;
    return this.http.get<any>(`${this.apiUrl}/exams`, { params });
  }
}
