"""
============================================================================
 LLM Service — Orchestrateur principal avec fallback automatique
============================================================================

ROLE : point d'entree unique pour generer une reponse intelligente.
       Combine RAG + LLM + fallback + memoire.

STRATEGIE DE FALLBACK :
  1. Try Groq (LLaMA 3.3 70B) → rapide, gratuit, qualite excellente
  2. Try HuggingFace (LLaMA 3 8B) → si Groq down ou pas de cle
  3. Fallback TF-IDF → reponse pre-ecrite du dataset (toujours dispo)

CHAQUE NIVEAU est independant : si une cle API manque, on passe au suivant.
============================================================================
"""

from __future__ import annotations
import os
from typing import Optional
from dataclasses import dataclass, asdict

from .groq_client import GroqClient, LLMResponse
from .hf_client import HFClient
from .rag import RAGRetriever, build_rag_prompt


@dataclass
class GeneratedResponse:
    """Reponse finale du LLMService apres RAG."""
    content: str
    provider: str         # "groq" | "hf" | "tfidf"
    model: str
    intent_detected: str
    confidence: float
    language: str
    contexts_used: list[dict]
    history_length: int
    latency_ms: int
    tokens_used: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class LLMService:
    """
    Orchestrateur du pipeline RAG + LLM avec fallback.

    Usage :
        service = LLMService(classifier=existing_classifier)
        response = service.generate(
            message="Kifash ntsajjel master IADS ?",
            history=[...],
            gender="F",
            name="Fatima",
        )
        print(response.content)
    """

    def __init__(
        self,
        classifier,
        groq_api_key: Optional[str] = None,
        hf_api_key: Optional[str] = None,
        groq_model: str = "default",
        rag_top_k: int = 3,
    ):
        """
        Args:
            classifier: MultilingualClassifier deja entraine (sert au RAG)
            groq_api_key: cle Groq (sinon lue depuis env GROQ_API_KEY)
            hf_api_key: cle HF (sinon lue depuis env HF_API_KEY)
            groq_model: modele Groq (defaut = llama-3.3-70b-versatile)
            rag_top_k: nombre de passages a recuperer
        """
        self.classifier = classifier
        self.retriever = RAGRetriever(classifier)
        self.groq = GroqClient(api_key=groq_api_key, model=groq_model)
        self.hf = HFClient(api_key=hf_api_key)
        self.rag_top_k = rag_top_k

    def is_llm_available(self) -> bool:
        """True si au moins un fournisseur LLM est utilisable."""
        return self.groq.available or self.hf.available

    def status(self) -> dict:
        """Etat des fournisseurs (pour /api/llm/status)."""
        return {
            "groq": {
                "available": self.groq.available,
                "model": self.groq.model,
            },
            "hf": {
                "available": self.hf.available,
                "model": self.hf.model,
            },
            "fallback_tfidf": True,
            "primary": "groq" if self.groq.available else ("hf" if self.hf.available else "tfidf"),
        }

    # ─── Pipeline complet ────────────────────────────────────────────────────
    def generate(
        self,
        message: str,
        history: Optional[list[dict]] = None,
        forced_language: Optional[str] = None,
        gender: Optional[str] = None,
        name: Optional[str] = None,
        temperature: float = 0.6,
    ) -> GeneratedResponse:
        """
        Genere une reponse en passant par le pipeline :
          1. Detection langue + intent + confidence (classifier existant)
          2. RAG : top-K contextes pertinents
          3. Build prompt avec contexte + persona
          4. Appel LLM (Groq → HF → TF-IDF fallback)
          5. Retour de la reponse + metadonnees

        Args:
            message: question utilisateur
            history: tours precedents [{role, content}]
            forced_language: forcer langue (sinon auto)
            gender: 'M' / 'F' / None
            name: prenom utilisateur si connu
            temperature: creativite (0=deterministe, 1=creatif)

        Returns:
            GeneratedResponse
        """
        # Etape 1 : Classifier existant (detecte intent + langue)
        clf_result = self.classifier.predict(
            message, top_k=self.rag_top_k * 2, forced_language=forced_language
        )
        lang = clf_result["language"]
        intent = clf_result["intent"]
        confidence = clf_result["confidence"]
        fallback_response = clf_result["response"]  # reponse TF-IDF pre-ecrite

        # Etape 2 : RAG retrieval (top-K passages)
        contexts = self.retriever.retrieve(message, lang=lang, top_k=self.rag_top_k)

        # Etape 3 : Build prompt RAG
        system_prompt, user_prompt = build_rag_prompt(
            user_message=message,
            contexts=contexts,
            lang=lang,
            gender=gender,
            name=name,
        )

        # Etape 4 : Tentative Groq d'abord
        if self.groq.available:
            r = self.groq.chat(
                system=system_prompt,
                user=user_prompt,
                history=history,
                temperature=temperature,
                max_tokens=1024,
            )
            if r.success and r.content:
                return GeneratedResponse(
                    content=r.content,
                    provider="groq",
                    model=r.model,
                    intent_detected=intent,
                    confidence=confidence,
                    language=lang,
                    contexts_used=contexts,
                    history_length=len(history or []),
                    latency_ms=r.latency_ms,
                    tokens_used=r.tokens_used,
                )
            print(f"[LLMService] Groq echec ({r.error}), fallback HF...")

        # Etape 5 : Fallback HuggingFace
        if self.hf.available:
            r = self.hf.chat(
                system=system_prompt,
                user=user_prompt,
                history=history,
                temperature=temperature,
                max_tokens=512,
            )
            if r.success and r.content:
                return GeneratedResponse(
                    content=r.content,
                    provider="hf",
                    model=r.model,
                    intent_detected=intent,
                    confidence=confidence,
                    language=lang,
                    contexts_used=contexts,
                    history_length=len(history or []),
                    latency_ms=r.latency_ms,
                )
            print(f"[LLMService] HF echec ({r.error}), fallback TF-IDF...")

        # Etape 6 : Fallback final = TF-IDF pre-ecrit
        return GeneratedResponse(
            content=fallback_response,
            provider="tfidf",
            model="tf-idf-cosine",
            intent_detected=intent,
            confidence=confidence,
            language=lang,
            contexts_used=contexts,
            history_length=len(history or []),
            latency_ms=10,
            error="LLM indisponible, reponse pre-ecrite servie",
        )
