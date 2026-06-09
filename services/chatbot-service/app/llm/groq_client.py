"""
============================================================================
 Client Groq API — Heberge LLaMA 3.x (gratuit, ultra-rapide)
============================================================================

POURQUOI GROQ ET PAS GROK ?
  - Grok (avec un 'k') = LLM de xAI/Elon Musk, payant, necessite abonnement X
  - Groq (avec un 'q') = plateforme d'inference LPU (Language Processing Unit),
    heberge des modeles open source comme LLaMA 3 GRATUITEMENT, tres rapide
  - C'est ce que ton encadrant veut probablement dire en parlant de "LLaMA + API"

GROQ EN BREF :
  - URL : https://groq.com
  - Inscription gratuite : https://console.groq.com
  - Free tier : ~30 requetes/minute, generous quotas
  - Modeles dispo : llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b
  - Latence : 50-200ms (vs 500-2000ms pour OpenAI)

COMMENT OBTENIR LA CLE API :
  1. Aller sur https://console.groq.com/keys
  2. Sign up (gratuit, email)
  3. Cliquer "Create API Key"
  4. Copier la cle qui commence par gsk_...
  5. La mettre dans .env : GROQ_API_KEY=gsk_...
============================================================================
"""

from __future__ import annotations
import os
from typing import Optional, Iterator
from dataclasses import dataclass

# La lib `groq` est optionnelle — on l'importe avec un try
try:
    from groq import Groq, APIError, RateLimitError
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None  # type: ignore


# ─── Modeles disponibles sur Groq (Mai 2026) ────────────────────────────────
GROQ_MODELS = {
    "llama-large":  "llama-3.3-70b-versatile",    # Meilleure qualite
    "llama-fast":   "llama-3.1-8b-instant",       # Tres rapide
    "mixtral":      "mixtral-8x7b-32768",          # Bon contexte long
    "default":      "llama-3.3-70b-versatile",
}


@dataclass
class LLMResponse:
    """Reponse d'un modele LLM."""
    content: str
    model: str
    provider: str = "groq"
    tokens_used: int = 0
    latency_ms: int = 0
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None


class GroqClient:
    """
    Client minimaliste pour l'API Groq.

    Usage simple :
        client = GroqClient(api_key="gsk_...")
        result = client.chat(
            system="Tu es un assistant FSBM.",
            user="Quelles sont les filieres ?",
        )
        print(result.content)
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "default"):
        """
        Args:
            api_key: cle API Groq. Si None, lue depuis GROQ_API_KEY env var.
            model: alias dans GROQ_MODELS ou nom complet (ex: "llama-3.3-70b-versatile")
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "").strip()
        self.model = GROQ_MODELS.get(model, model)
        self.available = bool(self.api_key) and GROQ_AVAILABLE

        if self.available:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"[Groq] Erreur init : {e}")
                self.available = False
        else:
            self.client = None
            if not GROQ_AVAILABLE:
                print("[Groq] Lib 'groq' non installee. Lancer: pip install groq")
            elif not self.api_key:
                print("[Groq] GROQ_API_KEY non defini dans .env")

    # ─── Generation simple (non-streaming) ──────────────────────────────────
    def chat(
        self,
        system: str,
        user: str,
        history: Optional[list[dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """
        Envoie une requete chat au modele et retourne la reponse complete.

        Args:
            system: prompt systeme (role, instructions, contexte)
            user: message de l'utilisateur
            history: liste optionnelle de tours precedents au format
                     [{"role": "user", "content": "..."},
                      {"role": "assistant", "content": "..."}]
            temperature: 0 = deterministe, 1 = creatif (defaut 0.7)
            max_tokens: longueur max de la reponse en tokens

        Returns:
            LLMResponse(content, model, tokens_used, latency_ms, error)
        """
        import time

        if not self.available:
            return LLMResponse(
                content="",
                model=self.model,
                error="Groq non configure (cle API manquante ou lib absente)",
            )

        # Construction des messages
        messages = [{"role": "system", "content": system}]
        if history:
            # On ne garde que les 10 derniers tours pour eviter de saturer le contexte
            messages.extend(history[-10:])
        messages.append({"role": "user", "content": user})

        start = time.perf_counter()
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95,
            )
            latency_ms = int((time.perf_counter() - start) * 1000)

            content = completion.choices[0].message.content or ""
            tokens = completion.usage.total_tokens if completion.usage else 0

            return LLMResponse(
                content=content.strip(),
                model=self.model,
                tokens_used=tokens,
                latency_ms=latency_ms,
            )
        except RateLimitError as e:
            return LLMResponse(content="", model=self.model,
                              error=f"Rate limit Groq atteint : {e}")
        except APIError as e:
            return LLMResponse(content="", model=self.model,
                              error=f"Erreur API Groq : {e}")
        except Exception as e:
            return LLMResponse(content="", model=self.model,
                              error=f"Erreur inattendue : {e}")

    # ─── Generation en streaming (pour effet "typing") ──────────────────────
    def chat_stream(
        self,
        system: str,
        user: str,
        history: Optional[list[dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Iterator[str]:
        """
        Version streaming : yield les chunks de texte au fur et a mesure.
        Utile pour afficher la reponse mot par mot dans le frontend.

        Yields:
            str : chunks de texte successifs
        """
        if not self.available:
            yield "[Groq non configure]"
            return

        messages = [{"role": "system", "content": system}]
        if history:
            messages.extend(history[-10:])
        messages.append({"role": "user", "content": user})

        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    yield delta
        except Exception as e:
            yield f"\n[Erreur streaming : {e}]"

    def __repr__(self):
        status = "OK" if self.available else "INDISPONIBLE"
        return f"<GroqClient model={self.model} status={status}>"


# ─── Test rapide ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    """Test direct : python -m app.llm.groq_client"""
    client = GroqClient()
    print(client)
    if client.available:
        r = client.chat(
            system="Tu es un assistant universitaire de la FSBM. Reponds en francais en 2 phrases.",
            user="Quelle est la difference entre licence et master ?",
        )
        print(f"\nReponse ({r.latency_ms}ms, {r.tokens_used} tokens):")
        print(r.content)
