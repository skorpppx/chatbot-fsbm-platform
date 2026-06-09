"""
Prétraitement du texte français pour le NLP.
- Tokenisation
- Suppression des stopwords français
- Stemming (Snowball français)
- Normalisation accents / casse
"""

import re
import unicodedata
from typing import List


STOPWORDS_FR = {
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "l",
    "et", "ou", "ni", "mais", "donc", "or", "car",
    "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles",
    "me", "te", "se", "moi", "toi", "lui", "leur", "leurs",
    "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses", "notre", "nos", "votre", "vos",
    "ce", "cet", "cette", "ces",
    "qui", "que", "quoi", "dont", "où", "ou",
    "est", "sont", "était", "ai", "as", "a", "avons", "avez", "ont",
    "être", "avoir", "faire", "dire", "voir",
    "pas", "ne", "n", "plus", "moins", "très", "tres", "trop", "si", "non",
    "pour", "par", "avec", "sans", "sous", "sur", "dans", "en", "y", "à", "au", "aux",
    "vers", "chez", "entre", "depuis", "pendant", "avant", "après", "après",
    "comment", "pourquoi", "quand", "combien",
    "c", "j", "m", "s", "t", "qu", "puis", "alors", "ainsi",
}


class TextPreprocessor:
    """Préprocesseur de texte français pour le chatbot."""

    def __init__(self):
        self._init_stemmer()

    def _init_stemmer(self):
        """Initialise le stemmer NLTK Snowball français."""
        try:
            from nltk.stem.snowball import FrenchStemmer
            self.stemmer = FrenchStemmer()
            self._has_stemmer = True
        except Exception:
            self.stemmer = None
            self._has_stemmer = False

    @staticmethod
    def remove_accents(text: str) -> str:
        """Supprime les accents pour la normalisation."""
        return "".join(
            c for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Découpe le texte en tokens alphanumériques."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)        # ponctuation → espace
        text = re.sub(r"\d+", " ", text)             # nombres → espace
        return [t for t in text.split() if t]

    def preprocess(self, text: str) -> str:
        """Pipeline complet : tokenize → stopwords → stemming."""
        if not text or not text.strip():
            return ""
        tokens = self.tokenize(self.remove_accents(text))
        tokens = [t for t in tokens if t not in STOPWORDS_FR and len(t) > 1]
        if self._has_stemmer:
            tokens = [self.stemmer.stem(t) for t in tokens]
        return " ".join(tokens)

    def keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Renvoie les mots-clés (tokens hors stopwords) pour analyse rapide."""
        tokens = self.tokenize(self.remove_accents(text))
        return [t for t in tokens if t not in STOPWORDS_FR and len(t) > 2][:top_n]
