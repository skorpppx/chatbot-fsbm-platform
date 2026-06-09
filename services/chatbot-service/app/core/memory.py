"""
Mémoire conversationnelle en mémoire (in-process).
Pour PFE — pas de Redis. Pour la prod : remplacer par Redis ou Memcached.

Stocke :
  * Historique des N derniers messages par session
  * Contexte utilisateur (filière mentionnée, année, etc.)
  * Compteur de tours
"""

from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Optional


@dataclass
class Turn:
    """Un échange utilisateur ↔ bot."""
    user_message: str
    bot_response: str
    intent: str
    confidence: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SessionContext:
    """Contexte d'une session de chat."""
    session_id: str
    user_id: Optional[int] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    history: deque[Turn] = field(default_factory=lambda: deque(maxlen=20))
    user_context: dict = field(default_factory=dict)  # ex: {'filiere': 'SMI', 'annee': 2}
    total_turns: int = 0

    def add_turn(self, turn: Turn):
        self.history.append(turn)
        self.total_turns += 1

    def last_intent(self) -> Optional[str]:
        if self.history:
            return self.history[-1].intent
        return None

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "started_at": self.started_at.isoformat(),
            "total_turns": self.total_turns,
            "user_context": dict(self.user_context),
            "history": [
                {
                    "user_message": t.user_message,
                    "bot_response": t.bot_response,
                    "intent": t.intent,
                    "confidence": t.confidence,
                    "timestamp": t.timestamp.isoformat(),
                }
                for t in self.history
            ],
        }


class ConversationMemory:
    """Singleton de gestion des sessions en mémoire."""

    _instance: Optional["ConversationMemory"] = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._sessions = {}
                cls._instance._sessions_lock = Lock()
        return cls._instance

    def __init__(self, max_history: int = 20):
        self.max_history = max_history

    def get_or_create(self, session_id: str, user_id: Optional[int] = None) -> SessionContext:
        with self._sessions_lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = SessionContext(
                    session_id=session_id,
                    user_id=user_id,
                    history=deque(maxlen=self.max_history),
                )
            return self._sessions[session_id]

    def add_turn(self, session_id: str, user_message: str, bot_response: str,
                 intent: str, confidence: float, user_id: Optional[int] = None):
        ctx = self.get_or_create(session_id, user_id)
        ctx.add_turn(Turn(user_message, bot_response, intent, confidence))
        self._extract_context(ctx, user_message, intent)

    def get_history(self, session_id: str) -> list[Turn]:
        if session_id not in self._sessions:
            return []
        return list(self._sessions[session_id].history)

    def get_session(self, session_id: str) -> Optional[SessionContext]:
        return self._sessions.get(session_id)

    def clear_session(self, session_id: str):
        with self._sessions_lock:
            self._sessions.pop(session_id, None)

    @staticmethod
    def _extract_context(ctx: SessionContext, message: str, intent: str):
        """Détecte des éléments de contexte (genre, prénom, filière, année)."""
        from app.core.persona import detect_gender, detect_name

        msg = message.lower()

        # Genre (NE PAS écraser un genre déjà détecté)
        if "gender" not in ctx.user_context:
            g = detect_gender(message)
            if g:
                ctx.user_context["gender"] = g

        # Prénom (NE PAS écraser)
        if "name" not in ctx.user_context:
            n = detect_name(message)
            if n:
                ctx.user_context["name"] = n

        # Filières
        for code, keywords in {
            "SMI": ["smi", "sciences mathematiques et informatique"],
            "DI":  ["di", "developpement informatique"],
            "SMA": ["sma", "sciences mathematiques et applications"],
            "SMP": ["smp", "physique"],
            "SMC": ["smc", "chimie"],
            "SV":  ["sv", "sciences de la vie", "biologie"],
            "STU": ["stu", "geologie", "sciences de la terre"],
        }.items():
            if any(k in msg for k in keywords):
                ctx.user_context["filiere"] = code
                break
        # Année
        for n, kw in [(1, ["s1", "s2", "premiere annee", "1ere annee", "l1"]),
                      (2, ["s3", "s4", "deuxieme annee", "2eme annee", "l2"]),
                      (3, ["s5", "s6", "troisieme annee", "3eme annee", "l3"])]:
            if any(k in msg for k in kw):
                ctx.user_context["annee"] = n
                break

    def stats(self) -> dict:
        with self._sessions_lock:
            sessions = list(self._sessions.values())
        return {
            "active_sessions": len(sessions),
            "total_turns": sum(s.total_turns for s in sessions),
            "avg_turns_per_session": (
                round(sum(s.total_turns for s in sessions) / len(sessions), 2) if sessions else 0
            ),
        }


memory = ConversationMemory()
