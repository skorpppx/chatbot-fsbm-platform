"""
============================================================================
 Systeme RAG (Retrieval-Augmented Generation)
============================================================================

C'EST QUOI LE RAG ?
  - Un LLM "pur" peut HALLUCINER (inventer des infos)
  - Le RAG ancre les reponses dans des donnees REELLES :
        1. RETRIEVAL : on cherche les passages pertinents dans la doc FSBM
        2. AUGMENTED : on injecte ces passages dans le prompt
        3. GENERATION : le LLM repond en utilisant ces passages comme source

ANALOGIE :
  Sans RAG = etudiant qui repond de tete (parfois faux)
  Avec RAG = etudiant qui ouvre son cours et cite les passages exacts

ARCHITECTURE :
  Question utilisateur
        |
        v
  [1] Detection langue
        |
        v
  [2] Retrieval : TF-IDF cherche top-3 intents les plus pertinents
        dans notre dataset multilingue
        |
        v
  [3] Build context : on concatene patterns + reponses des top-3
        |
        v
  [4] Build prompt : System (role) + Context (faits) + History (memoire) + User
        |
        v
  [5] Generation : LLM (Groq LLaMA 3.3) repond en se basant sur le contexte
        |
        v
  Reponse intelligente, contextuelle, sans hallucination
============================================================================
"""

from __future__ import annotations
import json
import os
from typing import Optional

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# ─── Base de connaissances institutionnelle REELLE (fsbm_knowledge.json) ──────
_KNOWLEDGE: Optional[dict] = None


def _load_knowledge() -> dict:
    """Charge (une seule fois) la base de connaissances institutionnelle reelle."""
    global _KNOWLEDGE
    if _KNOWLEDGE is None:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "fsbm_knowledge.json")
        try:
            with open(path, encoding="utf-8") as f:
                _KNOWLEDGE = json.load(f)
        except Exception:
            _KNOWLEDGE = {}
    return _KNOWLEDGE


def institutional_context(query: str, lang: str = "fr") -> str:
    """
    Construit un bloc de FAITS INSTITUTIONNELS REELS a injecter dans le contexte RAG.

    POURQUOI : le retriever TF-IDF ne couvre que les intents de la FAQ. Des questions
    factuelles (doyen, nombre de professeurs, chefs de departement, domaines de recherche)
    n'ont pas d'intent dedie -> le LLM repondait "je n'ai pas l'info". On ancre donc
    systematiquement ces faits reels (issus de fsbm.ma et Google Scholar) dans le prompt.

    Les faits de base (doyen, effectifs, departements, contact) sont TOUJOURS inclus
    (volume faible, forte demande). Les filieres et les profils de recherche ne sont
    ajoutes que si la question s'y rapporte (pour limiter la taille du prompt).
    """
    kb = _load_knowledge()
    if not kb:
        return ""
    q = (query or "").lower()
    fac = kb.get("faculte", {})
    blocks: list[str] = []

    # 1) Faits de base — toujours inclus
    core = [
        f"Nom : {fac.get('nom')} — {fac.get('universite')}.",
        f"Doyen : {fac.get('doyen')}.",
        f"Effectifs : {fac.get('nb_etudiants')} etudiants, {fac.get('nb_professeurs')} "
        f"enseignants-chercheurs, {fac.get('nb_departements')} departements, "
        f"{fac.get('nb_filieres')} filieres, {fac.get('nb_laboratoires')} laboratoires, "
        f"{fac.get('nb_entreprises_partenaires')} entreprises partenaires.",
        f"Contact : {fac.get('contact_email')}, tel {fac.get('contact_tel')}.",
        f"Adresse : {fac.get('adresse')} — site {fac.get('site')}.",
    ]
    blocks.append("FAITS INSTITUTIONNELS FSBM (donnees reelles fsbm.ma) :\n- " + "\n- ".join(core))

    # 2) Departements + chefs — toujours inclus (6 lignes)
    deps = kb.get("departements", [])
    if deps:
        dep_lines = [f"{d['nom']} (chef : {d['chef']})" for d in deps]
        blocks.append("LES 6 DEPARTEMENTS ET LEURS CHEFS :\n- " + "\n- ".join(dep_lines))

    # 3) Filieres — uniquement si la question porte sur les filieres/formations
    if any(k in q for k in ("filiere", "filière", "licence", "master", "formation",
                            "responsable", "programme", "program", "etudes", "cycle")):
        fils = kb.get("filieres", [])
        if fils:
            fil_lines = [f"{f['nom']} ({f['cycle']}, dep. {f['departement']}, resp. {f['responsable']})"
                         for f in fils]
            blocks.append("FILIERES (extrait reel) :\n- " + "\n- ".join(fil_lines))

    # 4) Profils de recherche — si question recherche/publication ou nom de prof connu
    profs = kb.get("professeurs_recherche", [])
    rech_kw = ("recherche", "publication", "publish", "domaine", "scholar", "citation",
               "h-index", "h index", "specialite", "spécialité", "travaux", "research",
               "laboratoire", "these", "thèse", "encadrant")
    name_kw = ("benlahm", "talea", "filali", "zahour", "guemmat")
    if profs and (any(k in q for k in rech_kw) or any(n in q for n in name_kw)):
        pr_lines = []
        for p in profs:
            role = f" — {p['role']}" if p.get("role") else ""
            pr_lines.append(
                f"{p['nom']} ({p['grade']}, dep. {p['departement']}) : {p['interets']}. "
                f"Google Scholar : {p['citations']} citations, h-index {p['h_index']}{role}."
            )
        blocks.append("PROFESSEURS-CHERCHEURS (donnees Google Scholar verifiees) :\n- "
                      + "\n- ".join(pr_lines))

    return "\n\n".join(blocks)


# ─── Prompts systeme par langue ──────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "fr": """Tu es l'assistant officiel de la Faculte des Sciences Ben M'Sick (FSBM), \
Universite Hassan II de Casablanca.

ROLE : Repondre aux questions des etudiants avec precision et chaleur.

REGLES STRICTES :
1. Reponds UNIQUEMENT en francais (sauf si l'etudiant ecrit dans une autre langue).
2. Utilise EXCLUSIVEMENT les informations du CONTEXTE ci-dessous.
3. Si l'info n'est pas dans le contexte, dis-le franchement : \
"Je n'ai pas cette information precise, contacte le service de la scolarite au 05 22 70 46 71."
4. JAMAIS inventer de numero, date, montant ou nom de professeur non present dans le contexte.
5. Reponse claire, structuree (puces si liste), longueur 100-300 mots.
6. Ton bienveillant, comme un grand frere/sœur etudiant(e) qui aide.""",

    "en": """You are the official assistant of Faculty of Sciences Ben M'Sick (FSBM), \
Hassan II University of Casablanca.

ROLE: Answer student questions with precision and warmth.

STRICT RULES:
1. Answer ONLY in English (unless the student writes in another language).
2. Use EXCLUSIVELY information from the CONTEXT below.
3. If info is missing, say so frankly: \
"I don't have that specific info, contact admissions at +212 5 22 70 46 71."
4. NEVER invent numbers, dates, amounts or professor names not in the context.
5. Clear, structured answer (bullet points if list), 100-300 words.
6. Friendly tone, like a helpful senior student.""",

    "darija": """Nta l'assistant rasmi dyal Faculte des Sciences Ben M'Sick (FSBM), \
Jami3a Hassan II Casablanca.

DOR : Jaweb 3la as'ila dyal lstudent b dakhi o b 7anan, b darija marocaine.

L9a3ida :
1. Jaweb GHA b darija marocaine (sauf ila katab b chi loga okhra).
2. Khdem GHIR b lma3louma li f CONTEXTE t7t.
3. Ila ma kanatch lma3louma f contexte, goul b sara7a : \
"Hadshi ma3rftch b dabt, ittasel m3a scolarite : 05 22 70 46 71."
4. JAMAIS taat-akhri3 chi raqm wla tarikh wla isim dyal prof li ma kayench f contexte.
5. Reponse waddi7a, b puces ila kant lista, 100-300 kalma.
6. B tari9a saheb saheba dyal student, machi rasmiya jaffa.""",
}


# ─── Couche RAG ──────────────────────────────────────────────────────────────
class RAGRetriever:
    """
    Recuperation des passages pertinents en utilisant le classifier TF-IDF
    existant comme moteur de recherche vectoriel.

    INNOVATION CLE : on REUTILISE notre classifier TF-IDF (qui sert deja a
    detecter l'intent) comme retriever RAG. Pas besoin d'embeddings dedies.
    """

    def __init__(self, classifier):
        """
        Args:
            classifier: instance de MultilingualClassifier (deja entraine)
        """
        self.classifier = classifier

    def retrieve(self, query: str, lang: str = "fr", top_k: int = 3) -> list[dict]:
        """
        Retourne les top-K intents les plus pertinents pour la requete.

        Args:
            query: question de l'utilisateur
            lang: langue (fr/en/darija)
            top_k: nombre de contextes a retourner

        Returns:
            list[dict] : [{tag, score, patterns: [...], response: "..."}]
        """
        if lang not in self.classifier.vectorizers:
            lang = "fr"

        # Pretraitement comme dans predict()
        processed = self.classifier.preprocessor.preprocess(query)
        if not processed.strip():
            return []

        # Vectorisation
        vec = self.classifier.vectorizers[lang].transform([processed])
        sims = cosine_similarity(vec, self.classifier.tfidf_matrices[lang])[0]

        # Top-K indices
        top_indices = np.argsort(sims)[::-1][:top_k * 3]  # prendre plus pour dedoublonner

        # Regrouper par intent (un intent peut avoir plusieurs patterns matchants)
        seen_intents = {}
        for idx in top_indices:
            score = float(sims[idx])
            if score <= 0:
                continue
            tag = self.classifier.pattern_to_intent[lang][idx]
            if tag == "default":
                continue
            if tag not in seen_intents or score > seen_intents[tag]["score"]:
                seen_intents[tag] = {
                    "tag": tag,
                    "score": round(score, 4),
                    "matched_pattern": self.classifier.patterns_processed[lang][idx],
                }
            if len(seen_intents) >= top_k:
                break

        # Enrichir avec patterns + reponse de reference
        contexts = []
        for tag, info in list(seen_intents.items())[:top_k]:
            intent = self.classifier._find_intent(tag)
            if not intent:
                continue
            pats = intent.get("patterns", {})
            patterns_lang = pats.get(lang) or pats.get("fr") or []
            resps = intent.get("responses", {})
            response_lang = (resps.get(lang) or resps.get("fr") or [""])[0]
            contexts.append({
                "tag": tag,
                "score": info["score"],
                "category": intent.get("category", "autre"),
                "icon": intent.get("icon", ""),
                "patterns": patterns_lang[:5],
                "reference_response": response_lang,
            })
        return contexts


def build_rag_prompt(
    user_message: str,
    contexts: list[dict],
    lang: str = "fr",
    gender: Optional[str] = None,
    name: Optional[str] = None,
) -> tuple[str, str]:
    """
    Construit le couple (system_prompt, user_prompt) pour le LLM.

    Le system contient :
        - Le role officiel FSBM
        - Les regles (ne pas inventer, repondre en {lang}, etc.)
        - Le contexte FSBM extrait (top-K passages)
        - Info perso si dispo (genre, nom)

    Le user contient simplement la question.

    Returns:
        (system_prompt, user_prompt)
    """
    system = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["fr"])

    # Assemblage du contexte : faits institutionnels reels + passages FAQ recuperes
    sections: list[str] = []

    # (a) Faits institutionnels reels (doyen, effectifs, departements, recherche...)
    inst = institutional_context(user_message, lang)
    if inst:
        sections.append(inst)

    # (b) Passages FAQ recuperes par le retriever TF-IDF
    if contexts:
        ctx_lines = []
        for i, c in enumerate(contexts, 1):
            ctx_lines.append(
                f"--- Passage #{i} (sujet: {c['tag']}, pertinence: {c['score']:.2f}) ---\n"
                f"Exemples de questions similaires : {', '.join(c['patterns'][:3])}\n"
                f"Information de reference :\n{c['reference_response']}\n"
            )
        sections.append("PASSAGES FAQ PERTINENTS :\n" + "\n".join(ctx_lines))

    if sections:
        system += "\n\n=== CONTEXTE FSBM (utilise UNIQUEMENT ces informations) ===\n"
        system += "\n\n".join(sections)
        system += "\n=== FIN DU CONTEXTE ==="
    else:
        system += "\n\n[Aucun contexte FSBM trouve pour cette question. " \
                  "Reponds en disant que tu n'as pas l'info specifique.]"

    # Info personnelle (genre, nom)
    if gender or name:
        if lang == "darija":
            persona_hint = "\n\n[INFO PERSO :"
            if name: persona_hint += f" nom = {name},"
            if gender == "F": persona_hint += " genre = feminin (appelle-la 'khti'),"
            elif gender == "M": persona_hint += " genre = masculin (appelle-le 'khoya'),"
            persona_hint += "]"
            system += persona_hint
        elif lang == "fr":
            if name: system += f"\n\n[INFO : l'etudiant s'appelle {name}.]"

    return system, user_message
