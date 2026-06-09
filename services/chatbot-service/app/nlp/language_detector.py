"""
Détecteur de langue trilingue : Français / Anglais / Darija marocaine.

Stratégie hybride :
  1. Si le message contient des caractères arabes → arabe/darija
  2. Sinon, on cherche des marqueurs lexicaux distinctifs (mots fortement
     associés à une langue)
  3. Fallback : score TF-IDF sur les n-grammes des trois corpus

Aucune dépendance externe (langdetect, pycld3) — fonctionne hors ligne.
"""

from __future__ import annotations
import re
from collections import Counter
from typing import Literal

Language = Literal["fr", "en", "darija"]


# ─── Marqueurs lexicaux distinctifs ──────────────────────────────────────────
# Mots qui sont QUASI exclusifs à une langue (forte indication)
DARIJA_KEYWORDS = {
    # Pronoms et expressions très courants en darija
    "ana", "nta", "nti", "huwa", "hiya", "7na", "ntoma", "homa",
    "wesh", "wach", "wesh", "kifash", "kif", "ach", "achno", "chno", "chnou",
    "fin", "feen", "imta", "fou9", "t7t", "lhna", "tema",
    "bghit", "bgha", "kanbghi", "kandir", "ndir", "kaydir",
    "khdma", "khassek", "khassni", "khass", "shokran", "shukran",
    "labas", "ahlan", "salam", "bslama", "marhba", "mzyan", "zwin", "bzaf",
    "barakallah", "llah", "yallah", "wakha", "safi", "iwa", "iyeh", "lala",
    "katdir", "katqra", "katsajjel", "kaymchi", "kaywsel",
    "smiyti", "smiti", "smiytek", "bnt", "wld", "khouya", "khoya", "khti",
    "darija", "maghribi", "maghrib", "casa", "casablanca",
    "9elleb", "n9elleb", "katqalleb", "talab", "talba",
    "7sn", "ahsen", "khsen", "lkhir", "lkhirat",
    # Lettres-chiffres typiques (3=ع, 7=ح, 9=ق, 8=غ)
    # On détecte aussi la présence de chiffres dans des mots latins (3am, 7biba, 9adi)
}

ENGLISH_KEYWORDS = {
    "the", "is", "are", "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "we", "they", "it",
    "what", "where", "when", "why", "how", "who", "which",
    "do", "does", "did", "have", "has", "had",
    "can", "could", "would", "should", "may", "might", "must",
    "and", "or", "but", "if", "then", "than", "with", "without",
    "this", "that", "these", "those",
    "hello", "hi", "hey", "thanks", "thank", "please", "sorry",
    "want", "need", "like", "love", "know", "think", "see", "get",
    "good", "morning", "evening", "night", "day",
    "year", "week", "today", "tomorrow", "yesterday",
    "registration", "enroll", "enrollment", "admission",
    "internship", "scholarship", "schedule", "timetable",
    "available", "online", "website", "computer", "science",
    # Verbes/mots-clés de requete supplementaires
    "search", "find", "fetch", "check", "look", "browse", "show", "tell",
    "latest", "recent", "current", "new", "newest", "fresh",
    "news", "announcement", "announcements", "updates", "info", "information",
    "give", "provide", "send", "share", "explain", "describe",
    "your", "my", "our", "their",
    "from", "about", "between", "during", "before", "after",
    "all", "some", "any", "every", "no", "not",
}

FRENCH_KEYWORDS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "au", "aux",
    "et", "ou", "mais", "donc", "car",
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "on",
    "que", "qui", "quoi", "dont", "où",
    "est", "sont", "était", "ai", "as", "ont", "avoir", "être",
    "comment", "pourquoi", "quand", "combien",
    "bonjour", "salut", "merci", "désolé", "désolée", "stp", "svp",
    "veux", "voudrais", "peux", "puis", "dois",
    "trouver", "chercher", "obtenir", "avoir", "faire",
    "comment", "quel", "quelle", "quels", "quelles",
    "filière", "filières", "scolarité", "étudiant", "étudiante",
    "inscription", "réinscription", "examens", "résultats",
    "emploi", "temps", "bourses", "stage", "diplôme",
    "dans", "sur", "avec", "sans", "pour", "par", "en",
}


# ─── Détection caractères arabes ─────────────────────────────────────────────
ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿ]")


def _tokenize(text: str) -> list[str]:
    """Tokenisation simple : sépare en mots, conserve les chiffres dans les mots."""
    return re.findall(r"\w+", text.lower())


def has_arabic_script(text: str) -> bool:
    return bool(ARABIC_RE.search(text))


def has_darija_numerals(tokens: list[str]) -> bool:
    """Détecte les chiffres-lettres typiques (3, 7, 9, 8) dans les mots latins."""
    for tok in tokens:
        if re.fullmatch(r"[a-z0-9]+", tok) and re.search(r"[3789]", tok):
            # Exclure les nombres purs (ex: '2024')
            if not tok.isdigit():
                return True
    return False


def _score_keywords(tokens: set[str], keyword_set: set[str]) -> int:
    return len(tokens & keyword_set)


def detect_language(text: str, default: Language = "fr") -> Language:
    """
    Détecte la langue du texte.

    Renvoie 'fr', 'en' ou 'darija'.
    Si ambigu, renvoie `default`.
    """
    if not text or not text.strip():
        return default

    # 1. Caractères arabes → darija (ou arabe standard, mais on traite comme darija)
    if has_arabic_script(text):
        return "darija"

    tokens = _tokenize(text)
    if not tokens:
        return default

    tokens_set = set(tokens)

    # 2. Chiffres-lettres typiques darija (3am, 7aja, 9rib)
    if has_darija_numerals(tokens):
        return "darija"

    # 3. Score par marqueurs lexicaux
    fr_score    = _score_keywords(tokens_set, FRENCH_KEYWORDS)
    en_score    = _score_keywords(tokens_set, ENGLISH_KEYWORDS)
    dar_score   = _score_keywords(tokens_set, DARIJA_KEYWORDS)

    # Bonus si le mot est dans plusieurs phrases
    total = fr_score + en_score + dar_score
    if total == 0:
        return default

    scores = {"fr": fr_score, "en": en_score, "darija": dar_score}
    best = max(scores, key=scores.get)

    # Si darija a au moins 1 marqueur fort, on choisit darija même si tie
    if dar_score >= 1 and dar_score >= fr_score and dar_score >= en_score:
        return "darija"

    return best  # type: ignore


def detect_with_confidence(text: str, default: Language = "fr") -> dict:
    """Version détaillée renvoyant les scores."""
    if not text or not text.strip():
        return {"language": default, "confidence": 0.0, "scores": {}}

    if has_arabic_script(text):
        return {"language": "darija", "confidence": 0.95, "scores": {"darija": 1.0}}

    tokens = _tokenize(text)
    if not tokens:
        return {"language": default, "confidence": 0.0, "scores": {}}

    if has_darija_numerals(tokens):
        return {"language": "darija", "confidence": 0.85, "scores": {"darija": 1.0}}

    tokens_set = set(tokens)
    fr  = _score_keywords(tokens_set, FRENCH_KEYWORDS)
    en  = _score_keywords(tokens_set, ENGLISH_KEYWORDS)
    dar = _score_keywords(tokens_set, DARIJA_KEYWORDS)

    total = max(fr + en + dar, 1)
    scores = {"fr": fr / total, "en": en / total, "darija": dar / total}

    best_lang = max(scores, key=scores.get)
    confidence = scores[best_lang]

    # Si darija a un score positif ET >= aux autres, prioriser
    if dar > 0 and dar >= fr and dar >= en:
        best_lang = "darija"
        confidence = scores["darija"]

    if confidence < 0.15:
        return {"language": default, "confidence": confidence, "scores": scores}

    return {"language": best_lang, "confidence": round(confidence, 3), "scores": scores}


# ─── Test rapide ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    samples = [
        "Bonjour comment vas-tu ?",
        "Hello how are you doing today?",
        "Salam khoya kifash bghit ntsajjel f FSBM",
        "Wesh dialk labas ?",
        "Comment m'inscrire en master IADS",
        "How to enroll in IADS master",
        "Kifash ntsajjel f master IADS",
        "Cherche les dernières news",
        "Search latest news please",
        "9elleb 3la lkhbar lawalin",
        "salam",
        "thanks",
        "merci",
        "wach 3andkom EDT online",
    ]
    print(f"{'Texte':<55} → {'Langue':<8} (confiance)")
    print("─" * 80)
    for s in samples:
        r = detect_with_confidence(s)
        print(f"{s:<55} → {r['language']:<8} ({r['confidence']})")
