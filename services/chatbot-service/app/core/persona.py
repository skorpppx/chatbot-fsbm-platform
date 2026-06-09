"""
Module de personnalisation : détection du genre + nom de l'utilisateur,
et substitution dynamique des formules de politesse dans les réponses.

Le bot s'adapte automatiquement :
  * Pour un homme → "khoya", "nta", "monsieur", "sahbi"
  * Pour une femme → "khti" / "lalla" (respect), "nti", "mademoiselle/madame"
  * Genre inconnu → formulation neutre ("sahbi", "khoya/khti", "vous")
"""

from __future__ import annotations
import re
from typing import Optional, Literal

Gender = Literal["M", "F"]


# ─── Détection du genre depuis le message ────────────────────────────────────
GENDER_HINTS_F = [
    # Darija
    r"\bana\s+bnt\b", r"\bana\s+fatat?\b", r"\bana\s+mra\b", r"\bana\s+lalla\b",
    r"\bana\s+wahda?\b", r"\bana\s+bnti\b", r"\bana\s+bn\s*adam\s+mra\b",
    r"\btsajjelt\s+ana\s+bnt\b", r"\bbnt\s+ana\b",
    # Français
    r"je\s+suis\s+une?\s+(fille|étudiante|jeune\s+fille|madame|mademoiselle|femme)",
    r"je\s+suis\s+étudiante\b",
    # English
    r"i\s+am\s+a?\s*(girl|female|woman)", r"i'?m\s+a?\s*(girl|female|woman)",
    # Self-references avec accord féminin
    r"\bétudiante\b", r"\bjeune\s+fille\b",
]
GENDER_HINTS_M = [
    # Darija
    r"\bana\s+wld\b", r"\bana\s+rajl\b", r"\bana\s+zamil\b", r"\bana\s+shab\b",
    r"\bana\s+rajel\b", r"\bana\s+wahed\b", r"\bana\s+wldi\b",
    r"\btsajjelt\s+ana\s+wld\b", r"\bwld\s+ana\b",
    # Français
    r"je\s+suis\s+un\s+(garçon|étudiant|jeune\s+homme|monsieur|homme)",
    r"je\s+suis\s+étudiant\b",
    # English
    r"i\s+am\s+a?\s*(boy|male|man)", r"i'?m\s+a?\s*(boy|male|man)",
    # Self-references masculin
    r"\bétudiant\b(?!e)",  # étudiant mais pas étudiante
]


def detect_gender(message: str) -> Optional[Gender]:
    """Détecte le genre depuis un message. Renvoie 'M', 'F' ou None."""
    if not message:
        return None
    lower = message.lower()
    # Tester d'abord féminin (plus restrictif)
    for pattern in GENDER_HINTS_F:
        if re.search(pattern, lower):
            return "F"
    for pattern in GENDER_HINTS_M:
        if re.search(pattern, lower):
            return "M"
    return None


# ─── Détection du prénom ─────────────────────────────────────────────────────
NAME_PATTERNS = [
    # Darija
    re.compile(r"(?:smiti|smiyti|sm?yti|3rrf|mn?\s*nakhdmek|ana)\s+([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})?)", re.IGNORECASE),
    # Français
    re.compile(r"(?:je\s+m'?appelle|mon\s+nom\s+est|c'?est\s+moi|appelez-moi)\s+([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})?)", re.IGNORECASE),
    # English
    re.compile(r"(?:my\s+name\s+is|i'?m|i\s+am|call\s+me)\s+([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})?)", re.IGNORECASE),
]

# Mots à ne PAS prendre pour des noms (faux positifs courants)
NAME_BLACKLIST = {
    "ana", "bnt", "wld", "fata", "mra", "rajl", "shab",
    "un", "une", "le", "la", "the", "a",
    "etudiant", "etudiante", "student", "boy", "girl",
    "moi", "lui", "elle", "him", "her",
}


def detect_name(message: str) -> Optional[str]:
    """Tente de détecter un prénom dans le message."""
    if not message:
        return None
    for regex in NAME_PATTERNS:
        m = regex.search(message)
        if m:
            name = m.group(1).strip()
            # Capitaliser proprement et filtrer les blacklists
            first = name.split()[0]
            if first.lower() not in NAME_BLACKLIST and len(first) >= 2:
                return name.title()
    return None


# ─── Substitution des placeholders selon genre/nom ──────────────────────────
def _subs_for_gender(gender: Optional[Gender], lang: str = "darija") -> dict:
    """Renvoie le dictionnaire de substitutions selon le genre et la langue."""
    if gender == "F":
        return {
            # Darija vocatives
            "{voc}": "khti",
            "{khoya_khti}": "khti",
            "{lalla_sahbi}": "lalla",
            "{nta_nti}": "nti",
            "{wld_bnt}": "bnt",
            "{dayer_dayra}": "dayra",
            "{ach_dayer_dayra}": "ach dayra",
            "{farhan_farhana}": "farhana",
            "{hzin_hzina}": "hzina",
            "{khayf_khayfa}": "khayfa",
            "{fati9_fati9a}": "fati9a",
            "{naj7_naj7a}": "naj7a",
            "{m3a3oun_m3a3ouna}": "m3a3ouna",
            # Français
            "{monsieur_madame}": "Madame",
            "{etudiant_etudiante}": "étudiante",
            "{stresse}": "stressée",
            "{perdu}": "perdue",
            "{sur}": "sûre",
            "{fatigue}": "fatiguée",
            "{decu}": "déçue",
            "{heureux}": "heureuse",
            "{content}": "contente",
            # English
            "{he_she}": "she",
            "{him_her}": "her",
            "{his_her}": "her",
        }
    if gender == "M":
        return {
            "{voc}": "khoya",
            "{khoya_khti}": "khoya",
            "{lalla_sahbi}": "sahbi",
            "{nta_nti}": "nta",
            "{wld_bnt}": "wld",
            "{dayer_dayra}": "dayer",
            "{ach_dayer_dayra}": "ach dayer",
            "{farhan_farhana}": "farhan",
            "{hzin_hzina}": "hzin",
            "{khayf_khayfa}": "khayf",
            "{fati9_fati9a}": "fati9",
            "{naj7_naj7a}": "naj7",
            "{m3a3oun_m3a3ouna}": "m3a3oun",
            "{monsieur_madame}": "Monsieur",
            "{etudiant_etudiante}": "étudiant",
            "{stresse}": "stressé",
            "{perdu}": "perdu",
            "{sur}": "sûr",
            "{fatigue}": "fatigué",
            "{decu}": "déçu",
            "{heureux}": "heureux",
            "{content}": "content",
            "{he_she}": "he",
            "{him_her}": "him",
            "{his_her}": "his",
        }
    # Genre inconnu : neutre / inclusif
    return {
        "{voc}": "sahbi",
        "{khoya_khti}": "sahbi",
        "{lalla_sahbi}": "sahbi",
        "{nta_nti}": "nta/nti",
        "{wld_bnt}": "khouya",
        "{dayer_dayra}": "dayer",
        "{ach_dayer_dayra}": "ach dayer",
        "{farhan_farhana}": "farhan/a",
        "{hzin_hzina}": "hzin/a",
        "{khayf_khayfa}": "khayf/a",
        "{fati9_fati9a}": "fati9/a",
        "{naj7_naj7a}": "naj7/a",
        "{m3a3oun_m3a3ouna}": "m3a3oun/a",
        "{monsieur_madame}": "",
        "{etudiant_etudiante}": "étudiant(e)",
        "{stresse}": "stressé(e)",
        "{perdu}": "perdu(e)",
        "{sur}": "sûr(e)",
        "{fatigue}": "fatigué(e)",
        "{decu}": "déçu(e)",
        "{heureux}": "heureux(se)",
        "{content}": "content(e)",
        "{he_she}": "they",
        "{him_her}": "them",
        "{his_her}": "their",
    }


def personalize_response(
    text: str,
    gender: Optional[Gender] = None,
    name: Optional[str] = None,
    lang: str = "darija",
) -> str:
    """
    Applique les substitutions de placeholders et insère le prénom si dispo.

    Placeholders supportés :
      {voc}                — terme d'adresse (khoya/khti/sahbi)
      {khoya_khti}         — variante similaire
      {lalla_sahbi}        — formule plus respectueuse
      {nta_nti}            — pronom (tu)
      {wld_bnt}            — garçon/fille
      {name}               — prénom de l'utilisateur (vide si inconnu)
      {dayer_dayra}        — accord (fait/faite)
      {farhan_farhana}     — heureux/heureuse en darija
      {hzin_hzina}         — triste
      {khayf_khayfa}       — qui a peur
      {fati9_fati9a}       — fatigué(e)
      {monsieur_madame}    — civilité française
      {stresse} {perdu}    — accords en français
    """
    if not text:
        return text
    subs = _subs_for_gender(gender, lang)
    # Nom personnalisé
    subs["{name}"] = name or ""
    subs["{name_comma}"] = f", {name}" if name else ""
    subs["{name_space}"] = f" {name}" if name else ""
    for placeholder, value in subs.items():
        text = text.replace(placeholder, value)
    # Nettoyer les espaces doubles (qui apparaissent quand {name} est vide)
    text = re.sub(r"  +", " ", text)
    text = re.sub(r"  ?,", ",", text)
    return text


# ─── Acknowledgement du genre/nom (réponse personnalisée) ───────────────────
def acknowledge_self_intro(gender: Optional[Gender], name: Optional[str], lang: str) -> str:
    """Renvoie une réponse personnalisée quand l'utilisateur se présente."""
    name_part = f", {name}" if name else ""
    if lang == "darija":
        if gender == "F":
            return (f"Ahlan wa sahlan{name_part} ! 🌸 Marhba bik khti f chatbot dyal FSBM. "
                    f"Ana daba 3raftk nti bnt, 7anatfeker hadshi bach n'addressek b la3ada mzyana. "
                    f"Sawalini 3la ay haja li khasselk t3rfi : tassjil, filiyat, lexams, stage, lminha, walakin ay haja!")
        elif gender == "M":
            return (f"Ahlan wa sahlan{name_part} ! 👋 Marhba bik khoya f chatbot dyal FSBM. "
                    f"Mzyan li 3rrefti rasek, hadshi katsahel li n3awnek a7sn. "
                    f"Sawalini 3la ay haja li khasslek t3raf : tassjil, filiyat, lexams, stage, lminha, ay haja!")
        else:
            return (f"Marhba bik{name_part} f chatbot dyal FSBM ! 😊 "
                    f"Ana hna bach n3awnek f ay haja li khasselk t3raf 3la FSBM. Goul li ach bghiti !")
    if lang == "en":
        if gender == "F":
            return (f"Hello{name_part}! 🌸 Welcome to the FSBM chatbot. "
                    f"Nice to meet you! I'll address you as 'mademoiselle'/'khti' from now on. "
                    f"Feel free to ask me anything about FSBM!")
        elif gender == "M":
            return (f"Hello{name_part}! 👋 Welcome to the FSBM chatbot. "
                    f"Glad to meet you! Feel free to ask me anything about FSBM.")
        else:
            return f"Welcome{name_part} to the FSBM chatbot! 😊 How can I help?"
    # FR
    if gender == "F":
        return (f"Bonjour{name_part} ! 🌸 Bienvenue à la FSBM. "
                f"Ravie de faire votre connaissance. Je vous appellerai « khti » ou « Madame » selon votre préférence. "
                f"Posez-moi vos questions !")
    elif gender == "M":
        return (f"Bonjour{name_part} ! 👋 Bienvenue à la FSBM. "
                f"Ravi de faire votre connaissance. Posez-moi toutes vos questions !")
    return f"Bienvenue{name_part} à la FSBM ! 😊 Que voulez-vous savoir ?"


# ─── Test rapide ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    samples = [
        ("ana bnt", "F"),
        ("ana wld", "M"),
        ("je suis une fille", "F"),
        ("je suis un garçon", "M"),
        ("I am a girl", "F"),
        ("I'm a boy", "M"),
        ("salam khoya", None),
        ("smiti Fatima", None),
        ("je m'appelle Karim", None),
    ]
    for msg, expected in samples:
        g = detect_gender(msg)
        name = detect_name(msg)
        ok = "OK" if g == expected else "??"
        print(f"[{ok}] {msg!r:40s} → gender={g}, name={name}")

    print()
    print("=== Substitution example ===")
    template = "Salam {voc}, ach {dayer_dayra} ? Ana farhan li 3rrefti {wld_bnt}."
    for g in ("M", "F", None):
        print(f"  [{g}] {personalize_response(template, gender=g)}")
