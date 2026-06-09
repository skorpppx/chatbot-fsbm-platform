import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export type TargetType = 'AI_ASSISTANT' | 'MODULE' | 'PROFESSOR' | 'FILIERE' | 'FACULTE' | 'GENERAL';
export type ReviewStatus = 'PENDING' | 'APPROVED' | 'HIDDEN';

export interface Review {
  id: number;
  target_type: TargetType;
  target_id?: number | null;
  target_label?: string | null;
  rating?: number | null;
  title?: string | null;
  comment: string;
  author_name?: string | null;
  author_filiere?: string | null;
  is_pinned: boolean;
  admin_response?: string | null;
  created_at: string;
}

export interface ReviewAdmin extends Review {
  author_email?: string | null;
  status: ReviewStatus;
  ip_address?: string | null;
  updated_at: string;
}

export interface ReviewCreate {
  target_type: TargetType;
  target_id?: number | null;
  target_label?: string | null;
  rating?: number | null;
  title?: string | null;
  comment: string;
  author_name?: string | null;
  author_filiere?: string | null;
}

export interface ReviewStats {
  ai_average: number;
  ai_count: number;
  total_reviews: number;
  distribution: { stars: number; count: number }[];
}

@Injectable({ providedIn: 'root' })
export class ReviewsService {
  private http = inject(HttpClient);
  private apiUrl = '/api/academic';

  // ─── Public ───────────────────────────────────────────────────────────────
  submit(payload: ReviewCreate): Observable<Review> {
    return this.http.post<Review>(`${this.apiUrl}/reviews`, payload);
  }

  list(targetType?: TargetType, limit = 50): Observable<Review[]> {
    const params: any = { limit };
    if (targetType) params.target_type = targetType;
    return this.http.get<Review[]>(`${this.apiUrl}/reviews`, { params });
  }

  stats(): Observable<ReviewStats> {
    return this.http.get<ReviewStats>(`${this.apiUrl}/reviews/stats`);
  }

  // ─── Admin (modération) ─────────────────────────────────────────────────────
  adminList(status?: ReviewStatus): Observable<ReviewAdmin[]> {
    const params: any = {};
    if (status) params.status = status;
    return this.http.get<ReviewAdmin[]>(`${this.apiUrl}/admin/reviews`, { params });
  }

  moderate(id: number, patch: Partial<{ status: ReviewStatus; is_pinned: boolean; admin_response: string }>): Observable<ReviewAdmin> {
    return this.http.patch<ReviewAdmin>(`${this.apiUrl}/admin/reviews/${id}`, patch);
  }

  remove(id: number): Observable<{ success: boolean; deleted_id: number }> {
    return this.http.delete<{ success: boolean; deleted_id: number }>(`${this.apiUrl}/admin/reviews/${id}`);
  }
}
