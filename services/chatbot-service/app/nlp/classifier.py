"""
Classifieur d'intentions MULTILINGUE pour le chatbot FSBM (v3.0).

Améliorations vs v2 :
  * Dataset structuré par langue {fr, en, darija}
  * Entraîne UN modèle TF-IDF par langue (3 classifieurs)
  * Détection automatique de la langue de l'utilisateur
  * Réponse choisie dans la langue détectée (fallback FR si manquant)
  * Support du flag `trigger_web_fetch` pour activer la recherche live
"""

from __future__ import annotations
import json
import os
import pickle
import random
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .preprocessor import TextPreprocessor
from .language_detector import detect_with_confidence, Language


SUPPORTED_LANGS: list[Language] = ["fr", "en", "darija"]


class MultilingualClassifier:
    """Classifieur trilingue TF-IDF + Cosine Similarity."""

    def __init__(self, dataset_path: Optional[str] = None,
                 confidence_threshold: float = 0.15):
        self.preprocessor = TextPreprocessor()
        self.confidence_threshold = confidence_threshold

        # Un vectorizer + une matrice par langue
        self.vectorizers: dict[Language, TfidfVectorizer] = {}
        self.tfidf_matrices: dict[Language, np.ndarray] = {}
        self.pattern_to_intent: dict[Language, list[str]] = {}
        self.patterns_processed: dict[Language, list[str]] = {}

        self.intents: list[dict] = []
        self.dataset_version: str = ""
        self.is_trained = False

        here = Path(__file__).parent.parent.parent
        self.dataset_path = Path(dataset_path) if dataset_path else here / "data" / "faq_dataset.json"
        self.model_path = here / "data" / "model.pkl"

    # ─── ENTRAINEMENT ─────────────────────────────────────────────────────────

    def load_dataset(self) -> dict:
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def train(self, save: bool = True) -> dict:
        print(f"[NLP] Chargement de {self.dataset_path.name}...")
        dataset = self.load_dataset()
        self.intents = dataset["intents"]
        self.dataset_version = dataset.get("version", "unknown")

        stats = {"languages": {}, "total_intents": len(self.intents)}

        for lang in SUPPORTED_LANGS:
            patterns = []
            tags = []
            for intent in self.intents:
                tag = intent["tag"]
                # Le dataset peut être au nouveau format (dict par langue) ou ancien (liste)
                pats_raw = intent.get("patterns", {})
                if isinstance(pats_raw, dict):
                    pats = pats_raw.get(lang, [])
                else:
                    # Ancien format : liste uniquement en FR
                    pats = pats_raw if lang == "fr" else []
                for p in pats:
                    processed = self.preprocessor.preprocess(p)
                    if processed.strip():
                        patterns.append(processed)
                        tags.append(tag)

            if not patterns:
                stats["languages"][lang] = {"patterns": 0, "intents": 0}
                continue

            vec = TfidfVectorizer(ngram_range=(1, 3), min_df=1, sublinear_tf=True)
            matrix = vec.fit_transform(patterns)
            self.vectorizers[lang] = vec
            self.tfidf_matrices[lang] = matrix
            self.pattern_to_intent[lang] = tags
            self.patterns_processed[lang] = patterns

            stats["languages"][lang] = {
                "patterns": len(patterns),
                "features": len(vec.get_feature_names_out()),
                "intents": len(set(tags)),
            }

        self.is_trained = True
        print(f"[NLP] Modèle multilingue entraîné : {stats}")
        if save:
            self._save_model()
        return stats

    def _save_model(self):
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump({
                "version": self.dataset_version,
                "vectorizers": self.vectorizers,
                "tfidf_matrices": self.tfidf_matrices,
                "pattern_to_intent": self.pattern_to_intent,
                "patterns_processed": self.patterns_processed,
                "intents": self.intents,
                "threshold": self.confidence_threshold,
            }, f)
        print(f"[NLP] Modèle sauvegardé → {self.model_path}")

    def load_model(self) -> bool:
        if not self.model_path.exists():
            return False
        try:
            with open(self.model_path, "rb") as f:
                data = pickle.load(f)
            # Vérifier que le cache est compatible (v3 multilingue)
            if not isinstance(data.get("vectorizers"), dict):
                print("[NLP] Cache ancienne version — réentraînement nécessaire.")
                return False
            self.vectorizers       = data["vectorizers"]
            self.tfidf_matrices    = data["tfidf_matrices"]
            self.pattern_to_intent = data["pattern_to_intent"]
            self.patterns_processed= data["patterns_processed"]
            self.intents           = data["intents"]
            self.dataset_version   = data.get("version", "unknown")
            self.confidence_threshold = data.get("threshold", self.confidence_threshold)
            self.is_trained = True
            print(f"[NLP] Modèle multilingue chargé depuis le cache (v{self.dataset_version}).")
            return True
        except Exception as exc:
            print(f"[NLP] ⚠️ Échec chargement modèle : {exc}")
            return False

    # ─── PREDICTION ──────────────────────────────────────────────────────────

    def predict(self, user_message: str, top_k: int = 3,
                forced_language: Optional[Language] = None) -> dict:
        """
        Prédit l'intent du message.

        Args:
            user_message: le message brut.
            top_k: nombre de candidats à retourner.
            forced_language: si fourni, force la langue (sinon auto-détection).

        Returns:
            {
                'intent': str,
                'confidence': float,
                'response': str,
                'matched_pattern': str | None,
                'language': str,  # langue détectée
                'language_confidence': float,
                'top_candidates': [...],
                'trigger_web_fetch': bool
            }
        """
        if not self.is_trained:
            if not self.load_model():
                self.train()

        # 1. Détecter la langue
        if forced_language and forced_language in SUPPORTED_LANGS:
            lang = forced_language
            lang_conf = 1.0
        else:
            lang_info = detect_with_confidence(user_message, default="fr")
            lang = lang_info["language"]
            lang_conf = lang_info["confidence"]

        # 2. Si pas de modèle pour cette langue → fallback sur fr
        if lang not in self.vectorizers or len(self.pattern_to_intent.get(lang, [])) == 0:
            print(f"[NLP] Pas de modèle pour '{lang}', fallback fr")
            lang = "fr"

        # 3. Prétraitement du message
        processed = self.preprocessor.preprocess(user_message)
        if not processed.strip():
            return self._default_response(lang=lang, lang_conf=lang_conf)

        # 4. Vectorisation + similarité
        message_vec = self.vectorizers[lang].transform([processed])
        sims = cosine_similarity(message_vec, self.tfidf_matrices[lang])[0]

        top_indices = np.argsort(sims)[::-1][:max(top_k, 1)]
        candidates = []
        for idx in top_indices:
            score = float(sims[idx])
            if score <= 0:
                continue
            candidates.append({
                "intent": self.pattern_to_intent[lang][idx],
                "confidence": round(score, 4),
                "matched_pattern": self.patterns_processed[lang][idx],
            })

        if not candidates:
            return self._default_response(lang=lang, lang_conf=lang_conf)

        best = candidates[0]
        if best["confidence"] < self.confidence_threshold:
            return self._default_response(
                lang=lang, lang_conf=lang_conf,
                confidence=best["confidence"], top=candidates
            )

        intent_obj = self._find_intent(best["intent"])
        response = self._pick_response(intent_obj, lang)
        trigger_fetch = bool(intent_obj.get("trigger_web_fetch", False)) if intent_obj else False

        return {
            "intent": best["intent"],
            "confidence": best["confidence"],
            "response": response,
            "matched_pattern": best["matched_pattern"],
            "language": lang,
            "language_confidence": lang_conf,
            "top_candidates": candidates,
            "trigger_web_fetch": trigger_fetch,
        }

    def get_suggestions(self, user_message: str, k: int = 4,
                       forced_language: Optional[Language] = None) -> list[dict]:
        """Suggestions de questions proches dans la langue détectée."""
        result = self.predict(user_message, top_k=k * 2, forced_language=forced_language)
        lang = result.get("language", "fr")
        seen = set()
        suggestions = []
        for cand in result.get("top_candidates", []):
            tag = cand["intent"]
            if tag in seen or tag == "default":
                continue
            seen.add(tag)
            intent_data = self._find_intent(tag)
            if intent_data:
                pats = intent_data.get("patterns", {})
                if isinstance(pats, dict):
                    examples = pats.get(lang) or pats.get("fr") or []
                else:
                    examples = pats
                if examples:
                    suggestions.append({
                        "intent": tag,
                        "example_question": examples[0],
                        "confidence": cand["confidence"],
                        "language": lang,
                    })
                    if len(suggestions) >= k:
                        break
        return suggestions

    # ─── UTILS ────────────────────────────────────────────────────────────────

    def _find_intent(self, tag: str) -> Optional[dict]:
        for it in self.intents:
            if it["tag"] == tag:
                return it
        return None

    def _pick_response(self, intent: Optional[dict], lang: Language) -> str:
        if not intent:
            return self._default_response_text(lang)
        responses = intent.get("responses", {})
        if isinstance(responses, dict):
            options = responses.get(lang) or responses.get("fr") or []
        else:
            options = responses
        if not options:
            return self._default_response_text(lang)
        return random.choice(options)

    def _default_response(self, lang: Language = "fr", lang_conf: float = 0.0,
                          confidence: float = 0.0, top: Optional[list] = None) -> dict:
        return {
            "intent": "default",
            "confidence": round(float(confidence), 4),
            "response": self._default_response_text(lang),
            "matched_pattern": None,
            "language": lang,
            "language_confidence": lang_conf,
            "top_candidates": top or [],
            "trigger_web_fetch": False,
        }

    def _default_response_text(self, lang: Language = "fr") -> str:
        default_intent = self._find_intent("default")
        if default_intent:
            resp = default_intent.get("responses", {})
            if isinstance(resp, dict):
                options = resp.get(lang) or resp.get("fr") or []
                if options:
                    return random.choice(options)
        fallback = {
            "fr": "Désolé, je n'ai pas compris. Pouvez-vous reformuler ?",
            "en": "Sorry, I didn't understand. Could you rephrase?",
            "darija": "Sma7li, ma fhmtch. 3awed swali ?",
        }
        return fallback.get(lang, fallback["fr"])

    def get_all_intents(self, lang: Language = "fr") -> list[dict]:
        if not self.intents:
            self.intents = self.load_dataset()["intents"]
        out = []
        for it in self.intents:
            if it["tag"] == "default":
                continue
            pats = it.get("patterns", {})
            if isinstance(pats, dict):
                pats_lang = pats.get(lang) or pats.get("fr") or []
            else:
                pats_lang = pats
            resps = it.get("responses", {})
            if isinstance(resps, dict):
                resps_lang = resps.get(lang) or resps.get("fr") or []
            else:
                resps_lang = resps
            out.append({
                "tag": it["tag"],
                "category": it.get("category", "autre"),
                "icon": it.get("icon"),
                "nb_patterns": len(pats_lang),
                "nb_responses": len(resps_lang),
                "example": pats_lang[0] if pats_lang else None,
                "trigger_web_fetch": it.get("trigger_web_fetch", False),
            })
        return out


# Alias pour rétrocompatibilité avec le code existant qui importe IntentClassifier
IntentClassifier = MultilingualClassifier
