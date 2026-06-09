# -*- coding: utf-8 -*-
"""
Resolveur hybride haute-precision (regles) — complement du classifieur TF-IDF.

POURQUOI : le classifieur TF-IDF mé-route certaines questions (surtout en darija) et
ne couvre pas les questions FACTUELLES (doyen, nombre de professeurs, responsable d'une
filiere, domaines de recherche d'un professeur, chef de departement, adresse, site...),
faute d'intention dediee. Ce module applique des regles multilingues (FR / EN / darija)
ancrees sur la base de connaissances reelle (fsbm_knowledge.json). Il s'execute AVANT
le TF-IDF dans le routeur de chat et fournit une reponse fiable et deterministe.

Concu pour fonctionner aussi bien en mode classique (TF-IDF) qu'en mode IA.
"""
from __future__ import annotations
import json
import os
import re
import unicodedata
from typing import Optional

_KB: Optional[dict] = None


def _kb() -> dict:
    global _KB
    if _KB is None:
        p = os.path.join(os.path.dirname(__file__), "..", "..", "data", "fsbm_knowledge.json")
        try:
            _KB = json.load(open(p, encoding="utf-8"))
        except Exception:
            _KB = {}
    return _KB


def _norm(t: str) -> str:
    """Minuscule + suppression des accents, encadre d'espaces pour matcher des mots."""
    t = (t or "").lower().strip()
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    return " " + re.sub(r"\s+", " ", t) + " "


def _has(t: str, *kws: str) -> bool:
    return any(k in t for k in kws)


# ─── Groupes de mots-cles multilingues ───────────────────────────────────────
COMBIEN = ("combien", "ch7al", "chhal", "ch-hal", "kam ", " kam", "kemmiya", "3dad",
           "how many", "how much", "number of", "nombre de", "nombre d", "nbre")
QUI = ("qui ", "qui est", "c'est qui", "chkoun", "ckoun", "achkoun", "who ", "who's",
       "who is", "mn houwa", "mn hia", "mn howa", "skoun")
WHERE = ("ou se", "ou est", "ou trouve", "ou se trouve", "ou sont", "où", " ou ", "fin ",
         "win ", "where", "located", "location", "kayna", "kayen", "kayn ", "se situe", "situe")
RESP = ("responsable", "mas'oul", "mas2oul", "masoul", "mas'ola", "chef de", "chef du",
        "chef d'", "chef d ", "le chef", " chef ", "qui dirige", "qui gere", "qui gère",
        "qui s'occupe", "qui soccupe", "in charge", "head of", " heads ", " head ", "who heads",
        "coordonnateur", "coordinateur", "coordonateur", "coordinate", "coordinates",
        "coordinator", "manages", "kaydir", "kayssayer", "kaysayer", "directeur", "diriger",
        "gere par", "leads", "kaydiro", "responsible")
RECH = ("recherche", "research", "majal", "domaine", "domaines", "specialite", "specialites",
        "travaux", "publication", "publications", "interet", "interets", "works on", "thematique",
        "khddam 3la", "khdam 3la", "kaykhdem 3la", "kaykhdem f", "axe de recherche", "publie")
PROF_NAMES = {
    "benlahm": "benlahmer", "talea": "talea", "filali": "filali",
    "zahour": "zahour", "guemmat": "guemmat", "gemmat": "guemmat",
}


def _faculty(): return _kb().get("faculte", {})


def _tri(lang, fr, en, dar):
    return {"fr": fr, "en": en, "darija": dar}.get(lang if lang in ("fr", "en", "darija") else "fr", fr)


# ─── Resolution factuelle (depuis la base de connaissances) ──────────────────
def _factual(t: str, lang: str) -> Optional[dict]:
    kb = _kb()
    fac = _faculty()
    if not fac:
        return None

    # 1) DOYEN
    if _has(t, " doyen", " l3amid", " 3amid", " amid ", " dean", " l'amid", "lamid"):
        d = fac.get("doyen", "")
        return _mk("doyen", _tri(lang,
            f"Le doyen de la FSBM est {d}.",
            f"The dean of FSBM is {d}.",
            f"L3amid dyal FSBM houwa {d}."))

    # 2) RESPONSABLE d'une filiere
    if _has(t, *RESP) and _has(t, "filiere", "filière", "filiya", " di ", "developpement",
                               "développement", "full stack", "cyber", "licence", "master",
                               "stat", "analyse", "program", "programme", "software",
                               "development", "engineering"):
        fil = _match_filiere(t)
        if fil:
            return _mk("responsable_filiere", _tri(lang,
                f"Le/la responsable de la filiere « {fil['nom']} » ({fil['cycle']}) est {fil['responsable']}.",
                f"The coordinator of the « {fil['nom']} » program ({fil['cycle']}) is {fil['responsable']}.",
                f"Lmas'oul 3la filiere « {fil['nom']} » houwa {fil['responsable']}."))

    # 3) CHEF de departement
    if _has(t, *RESP) and _has(t, "departement", "département", "department", "dept", "9ism", "qism"):
        dep = _match_departement(t)
        if dep:
            return _mk("chef_departement", _tri(lang,
                f"Le departement « {dep['nom']} » est dirige par {dep['chef']}.",
                f"The « {dep['nom']} » department is headed by {dep['chef']}.",
                f"Departement « {dep['nom']} » kaydirou {dep['chef']}."))

    # 4) RECHERCHE / domaines / metriques d'un professeur
    prof = _match_prof(t)
    if prof and (_has(t, *RECH) or _has(t, "professeur", "prof ", "ustad", "enseignant", "pr.", "pr ",
                                         "citation", "citations", "h-index", "h index", "scholar",
                                         "indice", "combien", "ch7al", "how many")):
        if _has(t, "citation", "citations", "h-index", "h index", "scholar", "indice"):
            return _mk("prof_metrics", _tri(lang,
                f"{prof['nom']} totalise {prof['citations']} citations sur Google Scholar (h-index {prof['h_index']}).",
                f"{prof['nom']} has {prof['citations']} citations on Google Scholar (h-index {prof['h_index']}).",
                f"{prof['nom']} 3andou {prof['citations']} citation f Google Scholar (h-index {prof['h_index']})."))
        return _mk("recherche_prof", _tri(lang,
            f"{prof['nom']} ({prof['grade']}) travaille sur : {prof['interets']}. "
            f"Sur Google Scholar : {prof['citations']} citations, h-index {prof['h_index']}.",
            f"{prof['nom']} ({prof['grade']}) works on: {prof['interets']}. "
            f"Google Scholar: {prof['citations']} citations, h-index {prof['h_index']}.",
            f"{prof['nom']} ({prof['grade']}) kaykhdem 3la : {prof['interets']}. "
            f"F Google Scholar : {prof['citations']} citation, h-index {prof['h_index']}."))

    # 5) Quel(s) professeur(s) sur un THEME (chatbots, IA, TALN...)
    if _has(t, "prof", "profs", "ustad", "asatida", "enseignant", "enseignants", "chercheur",
            "chercheurs", "researcher", "researchers", "professor", "professors", "teacher",
            "scientist") and not _match_prof(t):
        theme = _match_theme(t)
        if theme:
            return _mk("prof_par_theme", _tri(lang,
                f"Parmi les enseignants-chercheurs : {theme}.",
                f"Among the faculty researchers: {theme}.",
                f"Mn lasatida bahitin : {theme}."))

    # 6) Comptages institutionnels
    if _has(t, *COMBIEN):
        if _has(t, "prof", "ustad", "ostad", "enseignant", "professor", "teacher", "asatida"):
            return _mk("nb_professeurs", _tri(lang,
                f"La FSBM compte {fac.get('nb_professeurs')} enseignants-chercheurs.",
                f"FSBM has {fac.get('nb_professeurs')} faculty members.",
                f"FSBM 3andha {fac.get('nb_professeurs')} ustad (enseignants-chercheurs)."))
        if _has(t, "etudiant", "student", "talib", "3dad dyal nas"):
            return _mk("nb_etudiants", _tri(lang,
                f"La FSBM accueille environ {fac.get('nb_etudiants')} etudiants.",
                f"FSBM hosts about {fac.get('nb_etudiants')} students.",
                f"FSBM fiha t9ribann {fac.get('nb_etudiants')} talib."))
        if _has(t, "departement", "département", "department", "dept", "9ism"):
            deps = ", ".join(d["nom"] for d in kb.get("departements", []))
            return _mk("nb_departements", _tri(lang,
                f"La FSBM compte {fac.get('nb_departements')} departements : {deps}.",
                f"FSBM has {fac.get('nb_departements')} departments: {deps}.",
                f"FSBM 3andha {fac.get('nb_departements')} departements : {deps}."))
        if _has(t, "filiere", "filière", "filiya", "formation", "program"):
            return _mk("nb_filieres", _tri(lang,
                f"La FSBM propose une trentaine de filieres ({fac.get('nb_filieres')}), licences et masters.",
                f"FSBM offers about {fac.get('nb_filieres')} programs (bachelor's and master's).",
                f"FSBM 3andha ta9ribann {fac.get('nb_filieres')} filiere (licence o master)."))
        if _has(t, "labo", "laboratoire", "laboratory", "research lab"):
            return _mk("nb_labos", _tri(lang,
                f"La FSBM compte {fac.get('nb_laboratoires')} laboratoires de recherche.",
                f"FSBM has {fac.get('nb_laboratoires')} research laboratories.",
                f"FSBM 3andha {fac.get('nb_laboratoires')} laboratoire dyal recherche."))
        if _has(t, "partenaire", "entreprise", "partner", "company", "sharika"):
            return _mk("nb_partenaires", _tri(lang,
                f"La FSBM collabore avec environ {fac.get('nb_entreprises_partenaires')} entreprises partenaires.",
                f"FSBM partners with about {fac.get('nb_entreprises_partenaires')} companies.",
                f"FSBM khddama m3a ta9ribann {fac.get('nb_entreprises_partenaires')} sharika."))

    # 7) ADRESSE / localisation (pas l'emploi du temps)
    if _has(t, *WHERE) and _has(t, "fsbm", "faculte", "faculté", "faculty", "kouliya", "kuliya",
                                "ben m", "la fac") and not _has(t, "emploi", "temps", "timetable",
                                "edt", "cours", "salle", "prof", "exam", "module"):
        return _mk("adresse", _tri(lang,
            f"La FSBM est situee : {fac.get('adresse')}.",
            f"FSBM is located at: {fac.get('adresse')}.",
            f"FSBM kayna f : {fac.get('adresse')}."))

    # 8) SITE WEB
    if _has(t, "site", "website", "web ", "url", "lien", "page officielle", "site rasmi") and \
       _has(t, "fsbm", "faculte", "faculté", "faculty", "kouliya", "fac"):
        return _mk("site_web", _tri(lang,
            f"Le site officiel de la FSBM est {fac.get('site')}.",
            f"The official website of FSBM is {fac.get('site')}.",
            f"Site rasmi dyal FSBM houwa {fac.get('site')}."))

    # 9) CONTACT de la faculte
    if _has(t, "contact", "email", "e-mail", "mail", "telephone", "téléphone", "tel ", "numero",
            "numéro", "joindre") and _has(t, "fsbm", "faculte", "faculté", "faculty", "kouliya") \
            and not _has(t, "scolarite", "scolarité"):
        return _mk("contact_faculte", _tri(lang,
            f"Contact FSBM : {fac.get('contact_email')}, tel {fac.get('contact_tel')}.",
            f"FSBM contact: {fac.get('contact_email')}, phone {fac.get('contact_tel')}.",
            f"Contact FSBM : {fac.get('contact_email')}, tel {fac.get('contact_tel')}."))

    # 10) PRESENTATION de la faculte
    if _has(t, "presente", "présente", "presentation", "9ddem", "qddem", "9addem", "tell me about",
            "c'est quoi", "parle", "3lach", "3rrefni", "3arrefni", "kabout") and \
       _has(t, "fsbm", "faculte", "faculté", "faculty", "kouliya", "fac"):
        st = fac
        return _mk("presentation_fsbm", _tri(lang,
            f"La FSBM (Faculte des Sciences Ben M'Sick, Universite Hassan II de Casablanca) est dirigee "
            f"par {st.get('doyen')}. Elle accueille ~{st.get('nb_etudiants')} etudiants, compte "
            f"{st.get('nb_professeurs')} enseignants-chercheurs et {st.get('nb_departements')} departements, "
            f"et propose une trentaine de filieres. Contact : {st.get('contact_email')}.",
            f"FSBM (Faculty of Sciences Ben M'Sick, Hassan II University of Casablanca) is headed by "
            f"{st.get('doyen')}. It hosts ~{st.get('nb_etudiants')} students, {st.get('nb_professeurs')} "
            f"faculty members and {st.get('nb_departements')} departments, with about 30 programs. "
            f"Contact: {st.get('contact_email')}.",
            f"FSBM (Faculte des Sciences Ben M'Sick, Jami3a Hassan II Casablanca) kaydirha {st.get('doyen')}. "
            f"Fiha ~{st.get('nb_etudiants')} talib, {st.get('nb_professeurs')} ustad o {st.get('nb_departements')} "
            f"departements, o 3andha ta9ribann 30 filiere. Contact : {st.get('contact_email')}."))

    return None


# ─── Helpers de matching ─────────────────────────────────────────────────────
_FIL_ALIASES = [
    (("developpement informatique", "dev info", " di ", "filiere di", "developpement info",
      "software development", "software engineering", "computer development"), "Developpement Informatique"),
    (("full stack", "fullstack"), "Developpement Full Stack"),
    (("cyber", "cybersecurite", "securite", "cybersecurity"), "Cybersecurite"),
    (("administration reseaux", "reseaux et systemes", "admin reseau", "network admin"), "Administration Reseaux"),
    (("statistique", "stat ", "statistics"), "Statistiques"),
    (("analyse mathematique", "analyse math", "mathematical analysis"), "Analyse Mathematique"),
]


def _match_filiere(t: str) -> Optional[dict]:
    for aliases, key in _FIL_ALIASES:
        if _has(t, *aliases):
            for f in _kb().get("filieres", []):
                if key.lower() in _norm(f["nom"]):
                    return f
    # match direct par nom
    for f in _kb().get("filieres", []):
        toks = [w for w in _norm(f["nom"]).split() if len(w) >= 5]
        if toks and all(w in t for w in toks[:2]):
            return f
    return None


_DEP_ALIASES = [
    (("math", "informatique", "info "), "Mathematiques et Informatique"),
    (("biolog", "bio "), "Biologie"),
    (("chimie", "chemical"), "Chimie"),
    (("geolog", "geo "), "Geologie"),
    (("physique", "physic"), "Physiques"),
    (("communication", "humanit"), "Sciences de la Communication"),
]


def _match_departement(t: str) -> Optional[dict]:
    for aliases, key in _DEP_ALIASES:
        if _has(t, *aliases):
            for d in _kb().get("departements", []):
                if key.lower()[:10] in _norm(d["nom"]):
                    return d
    return None


def _match_prof(t: str) -> Optional[dict]:
    for frag in PROF_NAMES:
        if frag in t:
            target = PROF_NAMES[frag]
            for p in _kb().get("professeurs_recherche", []):
                if target in _norm(p["nom"]):
                    return p
    return None


def _match_theme(t: str) -> Optional[str]:
    themes = {
        "chatbot": "chatbot", "taln": "taln", "nlp": "taln", "langage": "taln",
        "machine learning": "apprentissage", "apprentissage": "apprentissage",
        "data": "data", "donnees": "data", "iot": "iot", "objets": "iot",
        "graphe": "graphe", "semantique": "semantique", "web": "web",
    }
    hit = None
    for k, v in themes.items():
        if k in t:
            hit = v; break
    if not hit:
        return None
    matches = []
    for p in _kb().get("professeurs_recherche", []):
        if hit in _norm(p["interets"]):
            matches.append(f"{p['nom']} ({p['interets']})")
    return " ; ".join(matches) if matches else None


def _mk(intent: str, response: str, conf: float = 0.95) -> dict:
    return {"intent": intent, "response": response, "confidence": conf, "source": "resolver"}


# ─── Resolution procedurale (reutilise les reponses pre-ecrites du dataset) ──
# tag du dataset -> groupes de mots-cles (FR / EN / darija)
_PROC = [
    ("contact_scolarite", (("contact", "email", "numero", "numéro", "telephone", "téléphone", "tel "),
                           ("scolarite", "scolarité", "administration"))),
    ("diplome", (("diplome", "diplôme", "diploma", "attestation", "releve", "relevé", "transcript",
                  "nakhod diplome", "wati9a"),)),
    ("bourses", (("bourse", "bourses", "min7a", "mn7a", "minha", "scholarship", "grant", "onousc",
                  "mn7at", "financ"),)),
    ("reinscription", (("reinscription", "réinscription", "re-inscription", "reinscrire",
                        "watai9 khassni", "re inscription"),)),
    ("inscription", (("inscription", "inscrire", "tassjil", "tasjil", "register", "registration",
                      "enroll", "s'inscrire", "ndir l'inscription", "kayfiya tasjil"),)),
    ("examens", (("examen", "examens", "exam", "exams", "lexams", "controle", "contrôle", "partiel",
                  "rattrapage", "evaluation", "évaluation", "notes", "controle continu"),)),
    ("emploi_du_temps", (("emploi du temps", "emploi", "timetable", "edt", "planning",
                          "horaire", "schedule", "edt dyali"),)),
    ("stage_pfe", (("stage", "pfe", "internship", "projet de fin", "fin d'etudes", "fin detudes",
                    "memoire", "mémoire", "soutenance"),)),
    ("master_iads", (("iads", "ia et data", "intelligence artificielle et data"),)),
    ("masters", (("master", "masters", "mastere", "mastère", "magister"),)),
    ("filiere_di", (("developpement informatique", "filiere di", " di ", "dev info"),)),
    ("filieres", (("filiere", "filières", "filieres", "filiyat", "formation", "formations",
                   "program", "programs", "licence", "licences", "debouche", "débouché",
                   "specialite", "spécialité", "orientation", "choisir filiere"),)),
    ("vie_etudiante_darija", (("club", "clubs", "vie etudiante", "vie étudiante", "activite",
                               "activité", "sport", "association"),)),
]


def _procedural(t: str, lang: str, classifier) -> Optional[dict]:
    if classifier is None:
        return None
    # Garde-fou : ne pas detourner les questions de soutien psychologique / stress
    if _has(t, "stress", "stresse", "stressé", "anxie", "angoiss", "peur", "khayef", "khayfa",
            "3yit", "deprim", "déprim", "triste", "mal "):
        return None
    for tag, groups in _PROC:
        if all(_has(t, *g) for g in groups):
            resp = _canned(classifier, tag, lang)
            if resp:
                return {"intent": tag, "response": resp, "confidence": 0.90, "source": "resolver"}
    return None


def _canned(classifier, tag: str, lang: str) -> Optional[str]:
    """Recupere la reponse pre-ecrite d'une intention dans la langue voulue."""
    try:
        intent = classifier._find_intent(tag)
    except Exception:
        intent = None
    if not intent:
        return None
    resps = intent.get("responses", {}) or {}
    pool = resps.get(lang) or resps.get("fr") or resps.get("en") or []
    return pool[0] if pool else None


# ─── Point d'entree ──────────────────────────────────────────────────────────
# Intentions "generiques/faibles" : si le TF-IDF y route une question contenant un mot-cle
# procedural precis (diplome, bourse...), c'est presque surement une mé-classification.
_GENERIC = {"salutation", "identite_chatbot", "identite_genre", "comment_vas_tu", "default",
            "ramadan_horaires", "live_news", "compliment_bot", "aurevoir", "motivation_etudes",
            "actualites", "remerciement"}


def resolve(message: str, lang: str = "fr", classifier=None,
            tfidf_conf: float = 1.0, tfidf_intent: str = "") -> Optional[dict]:
    """
    Tente de resoudre la question par regles. Retourne
    {"intent", "response", "confidence", "source"} ou None si aucune regle ne matche.

    - Les regles FACTUELLES (doyen, nombre de profs, responsable, recherche...) s'appliquent
      TOUJOURS : le TF-IDF peut etre confiant mais faux (il decrit la filiere au lieu de donner
      le responsable, par exemple).
    - Le routage PROCEDURAL (reponses pre-ecrites) s'applique si le TF-IDF n'est pas deja confiant
      (tfidf_conf < 0.90) OU s'il a route vers une intention generique/faible malgre un mot-cle
      procedural precis (ex. "kifash n7sel 3la min7a" classe par erreur en "salutation").
    """
    t = _norm(message)
    fact = _factual(t, lang)
    if fact:
        return fact
    if tfidf_conf < 0.90 or tfidf_intent in _GENERIC:
        return _procedural(t, lang, classifier)
    return None
