import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ChatResponse, FeedbackPayload } from '../models/message.model';

/**
 * Service Angular pour le chatbot.
 *
 * Deux modes :
 *   - sendMessage()    -> /api/chat       (TF-IDF, instantane)
 *   - sendMessageLLM() -> /api/llm/chat   (LLaMA 3 via Groq + RAG)
 */

export interface LLMChatResponse {
  response: string;
  provider: 'groq' | 'hf' | 'tfidf';
  model: string;
  intent_detected: string;
  confidence: number;
  language: string;
  contexts_used: Array<{
    tag: string;
    score: number;
    category: string;
    icon?: string;
    patterns?: string[];
    reference_response?: string;
  }>;
  conversation_id: number;
  session_id: string;
  history_length: number;
  latency_ms: number;
  tokens_used: number;
  error?: string;
}

export interface LLMStatus {
  groq: { available: boolean; model: string };
  hf:   { available: boolean; model: string };
  fallback_tfidf: boolean;
  primary: 'groq' | 'hf' | 'tfidf';
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private apiUrl = '/api';

  constructor(private http: HttpClient) {}

  /** Chat TF-IDF classique (rapide, deterministe). */
  sendMessage(message: string, sessionId: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(
      `${this.apiUrl}/chat`,
      { message, session_id: sessionId }
    );
  }

  /** Chat LLM (LLaMA 3 + RAG, contextuel et naturel). */
  sendMessageLLM(
    message: string,
    sessionId: string,
    options: { language?: string; temperature?: number } = {}
  ): Observable<LLMChatResponse> {
    return this.http.post<LLMChatResponse>(
      `${this.apiUrl}/llm/chat`,
      {
        message,
        session_id: sessionId,
        language: options.language ?? null,
        temperature: options.temperature ?? 0.6,
      }
    );
  }

  /** Verifier l'etat des fournisseurs LLM. */
  getLLMStatus(): Observable<LLMStatus> {
    return this.http.get<LLMStatus>(`${this.apiUrl}/llm/status`);
  }

  sendFeedback(payload: FeedbackPayload): Observable<{ success: boolean; feedback_id: number }> {
    return this.http.post<{ success: boolean; feedback_id: number }>(
      `${this.apiUrl}/feedback`,
      payload
    );
  }
}
