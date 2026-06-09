export interface Message {
    id: number; sender: 'bot' | 'user'; text: string; timestamp: Date;
    conversationId?: number | null; intent?: string; confidence?: number;
  }
  export interface ChatResponse {
    response: string; intent: string; confidence: number; conversation_id: number; session_id: string;
  }
  export interface FeedbackPayload { conversation_id: number; note: number; commentaire?: string; }