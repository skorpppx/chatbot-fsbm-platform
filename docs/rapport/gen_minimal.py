# -*- coding: utf-8 -*-
"""PFE_FSBM_Version_Minimale.pdf — Rapport PFE condense (<= 50 pages), Licence Dev Informatique."""
import os, json
from report_engine import *
from report_engine import _hr, _scaled
from front import cc
import fsbm_real as R
from reportlab.platypus import NextPageTemplate, PageBreak, Spacer, Paragraph

MI = [f for f in R.FILIERES if f[0] == "MI"]


def _test_stats():
    """Lit test_results_90.json (s'il existe) pour la section validation."""
    p = os.path.join(os.path.dirname(__file__), "test_results_90.json")
    try:
        data = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    n = len(data)
    groq = sum(1 for r in data if r.get("ia_provider") == "groq")
    by = {}
    for r in data:
        by.setdefault(r["lang"], {"n": 0, "conf": 0.0, "hi": 0, "groq": 0})
        b = by[r["lang"]]; b["n"] += 1; b["conf"] += r.get("conf", 0)
        if r.get("conf", 0) >= 0.5: b["hi"] += 1
        if r.get("ia_provider") == "groq": b["groq"] += 1
    for b in by.values():
        b["avg"] = b["conf"] / max(b["n"], 1)
    return {"n": n, "groq": groq, "by": by}


def cov(s):
    s += [NextPageTemplate("cover"), Spacer(1, 1.0*cm)]
    s.append(cc("Royaume du Maroc", 10, True, MUTED, sa=1))
    s.append(cc("Universite Hassan II de Casablanca", 13, True, NAVY, sa=1))
    s.append(cc("Faculte des Sciences Ben M'Sick", 12, True, NAVY, sa=1))
    s.append(cc("Departement de Mathematiques et Informatique", 10, False, MUTED, sa=8))
    try:
        lf = _scaled(LOGO_FSBM, max_w=7*cm, max_h=3*cm); lf.hAlign = "CENTER"; s.append(lf)
    except Exception: pass
    s += [Spacer(1, 0.4*cm), _hr(NAVY, 1.6), Spacer(1, 0.4*cm)]
    s.append(cc("MEMOIRE DE PROJET DE FIN D'ETUDES", 13, True, ACCENT, sa=2))
    s.append(cc("Presente en vue de l'obtention de la Licence en Developpement Informatique", 10, False, MUTED, sa=12))
    s.append(cc("Plateforme Universitaire Intelligente FSBM", 21, True, NAVY, lead=26, sa=5))
    s.append(cc("Chatbot Conversationnel Multilingue et Architecture Micro-Services", 12.5, False, BLUE, lead=16, sa=8))
    s.append(cc("(Version condensee)", 10, False, MUTED, sa=12))
    s.append(_hr(LINE, 1.0)); s.append(Spacer(1, 0.4*cm))
    s.append(cc("Realise par :", 10.5, True, INK, sa=2))
    s.append(cc("Akram BELMOUSSA · Zakaria BENGHAZALE · Nouhaila BEN SOUMANE", 12, True, NAVY_D, sa=12))
    s.append(cc("Encadre par : Pr. Habib BENLAHMER   —   Co-encadre par : Pr. Salma HANNOUNI", 11, True, NAVY, sa=10))
    s.append(cc("Annee Universitaire 2025 — 2026", 11.5, True, NAVY, sa=2))
    s += [NextPageTemplate("normal"), PageBreak()]


def build_min():
    reset_numbering()
    s = []
    cov(s)
    s += plain_heading("Sommaire"); s.append(make_toc())

    s += front_chapter("Remerciements")
    s.append(para(
        "Nous adressons nos plus vifs remerciements a notre encadrant, <b>Pr. Habib BENLAHMER</b>, "
        "pour sa confiance, sa disponibilite et ses conseils avises tout au long de ce projet, ainsi "
        "qu'a notre co-encadrante, <b>Pr. Salma HANNOUNI</b>, pour son accompagnement attentif et ses "
        "remarques constructives. Nous remercions chaleureusement l'ensemble du corps professoral du "
        "Departement de Mathematiques et Informatique de la FSBM pour la qualite de la formation "
        "dispensee durant notre Licence en Developpement Informatique. Nos remerciements s'adressent "
        "egalement aux membres du jury qui nous font l'honneur d'evaluer ce travail, ainsi qu'a nos "
        "familles et a nos camarades pour leur soutien indefectible."))

    s += front_chapter("Resume")
    s.append(para(
        "Ce projet de fin d'etudes porte sur la conception et la realisation d'une <b>plateforme "
        "universitaire intelligente</b> pour la Faculte des Sciences Ben M'Sick (FSBM), centree sur "
        "un <b>chatbot conversationnel multilingue</b> (francais, anglais, darija marocaine). Le moteur "
        "de reponse combine un classifieur <b>TF-IDF</b> pour la reconnaissance d'intentions et un grand "
        "modele de langage <b>LLaMA 3 (via l'API Groq)</b> encadre par une approche <b>RAG</b> "
        "(Retrieval-Augmented Generation) ancree sur une base de connaissances institutionnelle reelle. "
        "Une cascade de repli (Groq, puis HuggingFace, puis TF-IDF local) garantit une disponibilite de "
        "100 %. La plateforme repose sur une <b>architecture micro-services</b> (Angular 17, FastAPI, "
        "MySQL, MongoDB) et un espace d'administration securise par JWT. L'ensemble est fonde sur des "
        "<b>donnees reelles</b> de la FSBM et a ete valide par une batterie de tests trilingue."))
    s.append(Paragraph("<b>Mots-cles :</b> Chatbot, TALN, TF-IDF, RAG, LLaMA 3, Groq, micro-services, "
                       "Angular, FastAPI, MySQL, MongoDB, darija marocaine, JWT.", ST["body"]))
    s.append(spacer(0.2))
    s.append(Paragraph("<b>Abstract :</b> This work presents an intelligent university platform for FSBM, "
                       "built around a multilingual conversational chatbot (French, English, Moroccan "
                       "darija). It combines a TF-IDF intent classifier with a LLaMA 3 large language "
                       "model (via Groq), grounded by a Retrieval-Augmented Generation pipeline over a "
                       "real institutional knowledge base, within a micro-services architecture.", ST["body"]))

    reset_numbering()
    s += _ch_intro()
    s += _ch_fsbm()
    s += _ch_existant()
    s += _ch_besoin()
    s += _ch_uml()
    s += _ch_archi()
    s += _ch_bdd()
    s += _ch_chatbot()
    s += _ch_demo()
    s += _ch_tests()
    s += _ch_securite()
    s += _ch_gestion()
    s += _ch_limites_persp()
    s += _ch_conclusion()
    s += _ch_sources()
    s += _ch_acronymes()

    build("PFE_FSBM_Version_Minimale.pdf", s,
          title="PFE FSBM - Version Minimale (Licence Developpement Informatique)",
          author="A. BELMOUSSA, Z. BENGHAZALE, N. BEN SOUMANE")


# ══════════════════════════════════════════════════════════════════════════════
def _ch_intro():
    el = chapter("Introduction Generale")
    el.append(section("Contexte"))
    el.append(para(
        "La transformation numerique des etablissements d'enseignement superieur est devenue une "
        "necessite. Les etudiants attendent un acces immediat, permanent et personnalise a "
        "l'information academique : filieres, modules, emplois du temps, procedures administratives, "
        "bourses. A la Faculte des Sciences Ben M'Sick (FSBM), qui accueille pres de <b>12 000 "
        "etudiants</b>, cette information reste dispersee entre le site institutionnel, les panneaux "
        "d'affichage et le service de la scolarite, souvent sature par des demandes repetitives."))
    el.append(section("Problematique"))
    el.append(quote(
        "Comment offrir aux etudiants de la FSBM un acces simple, immediat, multilingue et fiable a "
        "l'information academique, tout en allegeant la charge du personnel administratif ?"))
    el.append(para(
        "Trois difficultes se conjuguent : la <b>diversite linguistique</b> (francais, anglais, et "
        "surtout la darija marocaine reellement parlee), l'exigence de <b>fiabilite</b> "
        "(une information administrative erronee a des consequences concretes) et la contrainte de "
        "<b>disponibilite permanente</b>."))
    el.append(section("Objectifs"))
    el += numbered([
        "Concevoir un chatbot conversationnel comprenant le langage naturel en trois langues.",
        "Garantir la fiabilite des reponses par une approche RAG ancree sur des donnees reelles.",
        "Adopter une architecture micro-services moderne, modulaire et evolutive.",
        "Offrir un espace d'administration securise pour la mise a jour des contenus.",
        "Fonder l'ensemble de la plateforme sur des donnees authentiques de la FSBM.",
    ])
    el.append(section("Methodologie et organisation"))
    el.append(para(
        "Le projet a suivi une demarche iterative et incrementale : etude du besoin, conception UML, "
        "realisation par increments testables, puis validation. Ce rapport, dans sa version condensee, "
        "presente successivement le contexte institutionnel, l'etude de l'existant, l'analyse des "
        "besoins, la conception (UML, architecture, bases de donnees), le fonctionnement du moteur "
        "conversationnel, la realisation, la validation par les tests, la securite, la gestion de "
        "projet, puis les limites et les perspectives."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_fsbm():
    el = chapter("Presentation de l'Organisme d'Accueil")
    el.append(para(
        "La Faculte des Sciences Ben M'Sick (FSBM) est un etablissement public de l'<b>Universite "
        f"Hassan II de Casablanca</b>, dirige par le doyen <b>{R.DOYEN}</b>. Etablissement scientifique "
        "de reference dans la region, elle assure des formations en sciences fondamentales et "
        "appliquees, de la licence au doctorat, et developpe une activite de recherche soutenue."))
    el.append(section("Chiffres cles (donnees reelles fsbm.ma)"))
    st = R.STATS_OFFICIELLES
    el += table([
        ["Indicateur", "Valeur reelle", "Indicateur", "Valeur reelle"],
        ["Etudiants", f"+{st['etudiants']}", "Professeurs", str(st['professeurs'])],
        ["Departements", str(st['departements']), "Laboratoires", str(st['laboratoires'])],
        ["Licences", str(st['licences']), "Masters", str(st['masters'])],
        ["Doctorats", str(st['doctorats']), "Filieres", str(st['filieres'])],
        ["Entreprises partenaires", str(st['entreprises_partenaires']), "Universite", "UH2C"],
    ], "Chiffres officiels de la FSBM (source : fsbm.ma)", col_widths=[3.0, 2.0, 3.0, 2.0], font=8.6)
    el.append(section("Les six departements"))
    dr = [["Code", "Departement", "Chef de departement"]]
    for d in R.DEPARTEMENTS:
        dr.append([d["code"], d["nom"], d["chef"]])
    el += table(dr, "Les 6 departements reels de la FSBM et leurs chefs", col_widths=[1.3, 5.0, 3.7], font=8.6)
    el.append(section("Le departement de Mathematiques et Informatique"))
    el.append(para(
        "Notre projet s'inscrit dans le departement de <b>Mathematiques et Informatique</b> "
        f"(chef : Pr. ADNAOUI Khalid), qui porte notamment la Licence en <b>Developpement "
        "Informatique</b> (responsable : Pr. SAEL Nihal), cadre de ce travail. Ses filieres :"))
    fr = [["Filiere", "Cycle", "Responsable"]]
    for f in MI:
        fr.append([f[1], f[2], f[3]])
    el += table(fr, "Filieres du departement de Mathematiques et Informatique", col_widths=[5.4, 1.8, 2.8], font=8.4)
    el.append(section("Activite de recherche"))
    el.append(para(
        "Le departement compte des enseignants-chercheurs actifs, dont plusieurs travaillent sur des "
        "themes directement lies a ce projet (traitement du langage, chatbots, apprentissage "
        "automatique). Le tableau suivant presente cinq profils verifies sur Google Scholar :"))
    pr = [["Enseignant-chercheur", "Domaines", "Citations", "h-index"]]
    for p in R.SCHOLAR_PROFS:
        last = p["last"].replace("BENLAHMAR", "BENLAHMER")  # graphie alignee sur le rapport
        pr.append([f"{p['first']} {last}", p["interets"][:42], str(p["citations"]), str(p["h_index"])])
    el += table(pr, "Profils de recherche verifies (Google Scholar)", col_widths=[3.0, 4.0, 1.5, 1.5], font=8.0)
    el.append(alert(
        "L'encadrant de ce projet, le <b>Pr. El Habib Benlahmer</b> (PES), totalise 2785 citations et "
        "un h-index de 24, avec une expertise en TALN et web semantique directement mobilisee ici.", "info"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_existant():
    el = chapter("Etude de l'Existant")
    el.append(para(
        "Avant de concevoir notre solution, nous avons analyse les approches existantes en matiere "
        "d'assistants conversationnels universitaires."))
    el.append(section("Solutions generalistes"))
    el.append(para(
        "Les grands assistants (ChatGPT, Copilot, Gemini) offrent une comprehension remarquable du "
        "langage naturel. Cependant, appliques au contexte universitaire marocain, ils presentent des "
        "limites majeures : absence de connaissance du contexte FSBM, maitrise faible de la darija, "
        "risque d'hallucination sur des informations administratives precises, cout et absence de "
        "souverainete des donnees."))
    el.append(section("Chatbots universitaires a base de regles"))
    el.append(para(
        "Les chatbots universitaires classiques reposent souvent sur des arbres de decision ou des FAQ "
        "statiques : fiables mais rigides, monolingues, et incapables de comprendre une reformulation."))
    el.append(section("Positionnement de notre solution"))
    el += table([
        ["Critere", "Generalistes (LLM)", "FAQ statiques", "Notre solution"],
        ["Contexte FSBM", "Non", "Partiel", "Natif (donnees reelles)"],
        ["Darija marocaine", "Faible", "Non", "Oui (461 patterns)"],
        ["Comprehension naturelle", "Excellente", "Nulle", "Bonne (TF-IDF + LLM)"],
        ["Fiabilite institutionnelle", "Variable", "Elevee", "Elevee (RAG + base reelle)"],
        ["Disponibilite hors ligne", "Non", "Oui", "Oui (repli TF-IDF)"],
        ["Souverainete des donnees", "Non", "Oui", "Oui"],
        ["Cout", "Eleve", "Faible", "Quasi nul"],
    ], "Positionnement face aux approches existantes", col_widths=[3.0, 2.6, 2.0, 2.4], font=7.9)
    el.append(para(
        "Notre solution adopte une approche <b>hybride</b> qui combine le meilleur des deux mondes : la "
        "fiabilite d'une base structuree et la souplesse d'un grand modele de langage, le tout "
        "specialise pour la FSBM et multilingue."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_besoin():
    el = chapter("Analyse et Specification des Besoins")
    el.append(section("Acteurs du systeme"))
    el += table([
        ["Acteur", "Description", "Principales actions"],
        ["Etudiant (visiteur)", "Utilisateur principal, non authentifie", "Dialoguer, consulter, deposer un avis"],
        ["Administrateur", "Personnel autorise", "Gerer les contenus, moderer les avis"],
        ["Systeme externe", "API Groq / HuggingFace", "Generer des reponses (LLM)"],
    ], "Acteurs et roles", col_widths=[2.6, 3.4, 4.0], font=8.4)
    el.append(section("Besoins fonctionnels"))
    el += bullets([
        "<b>BF1</b> — Dialoguer avec le chatbot en langage naturel (FR / EN / darija).",
        "<b>BF2</b> — Detecter automatiquement la langue et reconnaitre l'intention.",
        "<b>BF3</b> — Basculer entre mode classique (TF-IDF) et mode avance (LLaMA 3 + RAG).",
        "<b>BF4</b> — Repondre a partir de donnees institutionnelles reelles (doyen, filieres, profs).",
        "<b>BF5</b> — Consulter le referentiel academique : departements, filieres, modules, professeurs.",
        "<b>BF6</b> — Consulter les annonces, evenements et la vie etudiante.",
        "<b>BF7</b> — Deposer un avis et noter l'assistant.",
        "<b>BF8</b> — Administrer les contenus (CRUD) et moderer les avis via un espace securise.",
    ])
    el.append(section("Besoins non fonctionnels"))
    el += table([
        ["Categorie", "Exigence"],
        ["Performance", "Reponse < 200 ms (mode classique), < 1 s (mode IA)"],
        ["Disponibilite", "Service 24h/24 avec repli automatique (100 %)"],
        ["Securite", "JWT, bcrypt, controle d'acces par roles, validation des entrees"],
        ["Multilinguisme", "Francais, anglais, darija marocaine"],
        ["Fiabilite", "Ancrage RAG, absence d'invention de donnees"],
        ["Utilisabilite", "Interface responsive, mode sombre, accessibilite"],
        ["Maintenabilite", "Code modulaire, separation des responsabilites"],
    ], "Besoins non fonctionnels", col_widths=[2.6, 7.4], font=8.6)
    el.append(section("Diagramme de cas d'utilisation"))
    el += figure_mermaid(r'''flowchart LR
  E(("Etudiant"))
  A(("Administrateur"))
  subgraph SYS["Plateforme FSBM"]
    U1["Dialoguer avec le chatbot"]
    U2["Consulter le referentiel"]
    U3["Consulter annonces et vie etudiante"]
    U4["Deposer un avis"]
    U5["S'authentifier"]
    U6["Gerer les contenus (CRUD)"]
    U7["Moderer les avis"]
  end
  E --> U1
  E --> U2
  E --> U3
  E --> U4
  A --> U5
  A --> U6
  A --> U7
  U6 -.inclut.-> U5
''', "Diagramme de cas d'utilisation general", max_h=10*cm)
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_uml():
    el = chapter("Conception UML")
    el.append(para(
        "La conception s'appuie sur le langage UML pour modeliser la structure et le comportement du "
        "systeme avant l'implementation."))
    el.append(section("Diagramme de classes"))
    el += figure_mermaid(r'''classDiagram
  class Departement { +id +code +nom +chef }
  class Filiere { +id +code +nom +type +responsable }
  class Module { +id +code +nom +semestre +credits }
  class Professeur { +id +nom +grade +specialite +bio }
  class Utilisateur { +id +email +role +mot_de_passe }
  class Conversation { +id +message +reponse +intention +langue }
  class Avis { +id +note +commentaire +statut +date }
  Departement "1" --> "*" Filiere
  Departement "1" --> "*" Professeur
  Filiere "1" --> "*" Module
  Utilisateur "1" --> "*" Avis : modere
''', "Diagramme de classes simplifie", max_h=10.5*cm)
    el.append(section("Diagramme de sequence — mode classique (FAQ / TF-IDF)"))
    el += figure_mermaid(r'''sequenceDiagram
  actor U as Etudiant
  participant A as Angular
  participant C as Chatbot-Service
  participant N as TF-IDF
  U->>A: Message
  A->>C: POST /api/chat
  C->>N: Detecter langue + classifier intention
  N-->>C: (intention, confiance, reponse)
  C-->>A: Reponse predefinie fiable
  A-->>U: Affichage (< 200 ms)
''', "Sequence du mode classique", max_h=8.5*cm)
    el.append(section("Diagramme de sequence — mode avance (RAG + LLaMA 3)"))
    el += figure_mermaid(r'''sequenceDiagram
  actor U as Etudiant
  participant A as Angular
  participant C as Chatbot-Service
  participant R as RAG (retriever + base reelle)
  participant G as Groq (LLaMA 3.3)
  U->>A: Message (mode IA)
  A->>C: POST /api/chat/llm
  C->>R: Recuperer contextes (TF-IDF + faits institutionnels)
  R-->>C: Passages + faits reels (doyen, profs...)
  C->>G: Prompt = role + contexte + question
  G-->>C: Reponse generative encadree
  C-->>A: Reponse + metadonnees
  A-->>U: Affichage
''', "Sequence du mode avance (RAG)", max_h=10.5*cm)
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_archi():
    el = chapter("Architecture du Systeme")
    el.append(para(
        "La plateforme adopte une architecture <b>micro-services</b> : un frontend Angular, deux "
        "services FastAPI independants, et une persistance polyglotte MySQL + MongoDB. Ce decoupage "
        "favorise l'evolutivite, l'isolation des pannes et la specialisation des services."))
    el += figure_mermaid(r'''flowchart TB
  NG["Angular 17 (SPA)"] -->|REST/JSON| CB["Chatbot-Service :8001"]
  NG -->|REST/JSON| AC["Academic-Service :8002"]
  CB --> NLP["NLP TF-IDF (3 langues)"]
  CB --> RAG["RAG + base de connaissances reelle"]
  RAG --> GROQ["Groq LLaMA 3.3 / HuggingFace"]
  CB --> MGO[("MongoDB")]
  AC --> SQL[("MySQL")]
  CB -->|HTTP| AC
''', "Architecture micro-services de la plateforme", max_h=10.5*cm)
    el.append(section("Les couches applicatives"))
    el += table([
        ["Couche", "Technologie", "Role"],
        ["Presentation", "Angular 17 (signals)", "Interface SPA responsive, mode sombre"],
        ["Service conversationnel", "FastAPI :8001", "Chat, NLP, RAG, LLM, conversations"],
        ["Service academique", "FastAPI :8002", "Referentiel, annonces, avis, admin"],
        ["Intelligence", "scikit-learn, Groq, RAG", "Classification + generation encadree"],
        ["Donnees relationnelles", "MySQL 8", "Referentiel academique (3NF)"],
        ["Donnees documentaires", "MongoDB", "Conversations, analytics, feedback"],
        ["Securite", "JWT, bcrypt, RBAC", "Authentification et autorisation"],
    ], "Couches et technologies", col_widths=[3.0, 3.0, 4.0], font=8.2)
    el.append(section("Justification des choix"))
    el += bullets([
        "<b>Angular</b> : framework complet et structurant, TypeScript type, signals performants.",
        "<b>FastAPI</b> : asynchrone, validation Pydantic automatique, documentation Swagger generee.",
        "<b>Micro-services</b> : separation des responsabilites, deploiement et montee en charge cibles.",
        "<b>Persistance polyglotte</b> : MySQL pour le relationnel fortement structure, MongoDB pour "
        "les conversations semi-structurees et volumineuses.",
        "<b>Groq</b> : inference LLaMA 3 a tres faible latence, gratuite, sans infrastructure a gerer.",
    ])
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_bdd():
    el = chapter("Conception des Bases de Donnees")
    el.append(para(
        "La persistance est <b>polyglotte</b> : MySQL pour les donnees academiques relationnelles "
        "(normalisees en 3NF) et MongoDB pour les conversations et les analyses."))
    el.append(section("Modele relationnel (MySQL)"))
    el += figure_mermaid(r'''erDiagram
  DEPARTEMENT ||--o{ FILIERE : contient
  DEPARTEMENT ||--o{ PROFESSEUR : emploie
  FILIERE ||--o{ MODULE : compose
  FILIERE ||--o{ ETUDIANT : inscrit
  UTILISATEUR ||--o{ AVIS : modere
  ANNONCE }o--|| UTILISATEUR : publie
''', "Modele entite-association simplifie (MySQL)", max_h=8.5*cm)
    el.append(para("La base MySQL comprend une dizaine de tables principales :"))
    el += table([
        ["Domaine", "Tables principales"],
        ["Academique", "departements, filieres, modules, professeurs, etudiants"],
        ["Contenu", "annonces, evenements, clubs, faq_items"],
        ["Communaute", "avis (reviews), recommandations"],
        ["Securite", "utilisateurs (roles), sessions admin"],
    ], "Organisation des tables MySQL", col_widths=[2.4, 7.6], font=8.6)
    el.append(section("Modele documentaire (MongoDB)"))
    el += table([
        ["Collection", "Contenu"],
        ["conversations", "Historique des echanges (message, reponse, intention, langue, provider)"],
        ["analytics", "Statistiques d'usage, intentions frequentes, langues"],
        ["feedback", "Retours utilisateurs (pouce haut/bas) sur les reponses"],
    ], "Collections MongoDB", col_widths=[2.4, 7.6], font=8.6)
    el.append(alert(
        "Les fiches etudiants sont <b>modelisees</b> (donnees de simulation) pour respecter la "
        "confidentialite ; toutes les donnees institutionnelles (departements, filieres, professeurs, "
        "doyen) sont <b>reelles</b> et issues de fsbm.ma.", "info"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_chatbot():
    el = chapter("Le Moteur Conversationnel")
    el.append(para(
        "Le coeur du projet est un moteur conversationnel hybride combinant traitement automatique du "
        "langage (TALN), recherche d'information et generation encadree."))
    el.append(section("Pipeline de traitement"))
    el += figure_mermaid(r'''flowchart TD
  S([Message]) --> L["1. Detecter la langue"]
  L --> P["2. Pretraitement (normalisation)"]
  P --> I["3. Classifier l'intention (TF-IDF + cosinus)"]
  I --> D{"Confiance >= seuil ?"}
  D -- Oui --> F["Reponse FAQ fiable + base FSBM"]
  D -- Non / mode IA --> G{"Groq disponible ?"}
  G -- Oui --> RAG["RAG : contextes + faits reels -> LLaMA 3"]
  G -- Non --> H{"HuggingFace ?"}
  H -- Oui --> HF["LLaMA 3 8B"]
  H -- Non --> F
  F --> Rep([Reponse])
  RAG --> Rep
  HF --> Rep
''', "Pipeline complet du moteur conversationnel", max_h=12.5*cm)
    el.append(section("Detection de la langue et reconnaissance d'intention"))
    el.append(para(
        "Un detecteur hybride identifie la langue (script arabe, chiffres darija 3/7/9, mots-cles "
        "lexicaux). Le message est ensuite vectorise par <b>TF-IDF</b> (un modele par langue) et "
        "compare aux patterns d'entrainement par <b>similarite cosinus</b>. L'intention la plus proche "
        "est retenue si sa confiance depasse un seuil ; sinon, le systeme demande une reformulation ou "
        "bascule vers le mode generatif."))
    el += table([
        ["Caracteristique", "Valeur"],
        ["Intentions reconnues", "28"],
        ["Patterns d'entrainement", "~835 (188 FR, 186 EN, 461 darija)"],
        ["Vectorisation", "TF-IDF, n-grammes 1-3, un modele par langue"],
        ["Mesure de similarite", "Cosinus"],
        ["Seuil de confiance", "0,15 (configurable)"],
    ], "Parametres du classifieur TF-IDF", col_widths=[3.4, 6.6], font=8.6)
    el.append(section("Le RAG et la base de connaissances reelle"))
    el.append(para(
        "Pour eviter les hallucinations, le mode avance utilise le <b>RAG</b> : avant d'interroger "
        "LLaMA 3, le systeme recupere des contextes pertinents (passages de la FAQ via TF-IDF) et, "
        "surtout, injecte des <b>faits institutionnels reels</b> issus d'une base de connaissances "
        "(doyen, effectifs, chefs de departement, responsables de filieres, profils de recherche). Le "
        "modele genere alors une reponse <b>encadree</b> par ces faits, sans rien inventer."))
    el.append(alert(
        "<b>Apport technique cle :</b> le branchement de la base de connaissances institutionnelle "
        "dans le contexte RAG. Sans ce branchement, le modele repondait \"Je n'ai pas cette "
        "information\" a des questions pourtant connues (doyen, nombre de professeurs, domaines de "
        "recherche). Avec, il repond desormais correctement et de maniere fondee.", "key"))
    el.append(section("Resolveur hybride (mode classique)"))
    el.append(para(
        "Le classifieur TF-IDF seul mé-routait certaines formulations, surtout en darija (une "
        "question sur le doyen tombait en « salutation », une question sur le nombre de professeurs "
        "en « filieres »). Nous avons ajoute un <b>resolveur hybride a base de regles</b>, "
        "multilingue, ancre sur la base de connaissances : les questions factuelles (doyen, "
        "effectifs, responsable d'une filiere, domaines de recherche, chef de departement, adresse) "
        "sont resolues de maniere deterministe, et les questions procedurales sont routees vers la "
        "bonne reponse meme en cas d'hesitation du TF-IDF. En mode classique, le chatbot atteint "
        "ainsi <b>100 % de bonnes reponses</b> sur la batterie de 90 questions, sans connexion et "
        "en ~10 ms."))
    el.append(section("Multilinguisme et darija"))
    el.append(para(
        "La prise en charge de la <b>darija marocaine</b> (461 patterns, soit plus de la moitie du "
        "corpus) constitue un differenciateur fort. Le systeme adapte meme ses formules selon le genre "
        "detecte (khoya, khti), apportant une dimension humaine rarement presente dans les chatbots "
        "generalistes."))
    el.append(section("La cascade de repli"))
    el.append(para(
        "Trois niveaux assurent une disponibilite de 100 % : <b>Groq</b> (LLaMA 3.3-70B, rapide et "
        "gratuit), puis <b>HuggingFace</b> (LLaMA 3 8B) en repli, puis le <b>TF-IDF local</b> "
        "(reponses predefinies) toujours operationnel, meme hors ligne."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_demo():
    el = chapter("Realisation et Interfaces")
    el.append(para(
        "Cette section presente des captures reelles de la plateforme realisee, illustrant les "
        "principales fonctionnalites cote etudiant et cote administration."))
    el += figure_img(shot(5), "Tableau de bord : assistant et statistiques en temps reel", max_h=8*cm)
    el += figure_img(shot(7), "Assistant conversationnel multilingue (mode IA LLaMA 3 + RAG)", max_h=8.5*cm)
    el += figure_img(shot(8), "Page des departements (donnees reelles fsbm.ma)", max_h=7.5*cm)
    el += figure_img(shot(9), "Page des filieres avec filtres", max_h=7.5*cm)
    el += figure_img(shot(11), "Page des professeurs", max_h=7.5*cm)
    el += figure_img(shot(22), "Espace d'administration : moderation des avis", max_h=7.5*cm)
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_tests():
    el = chapter("Tests et Validation")
    el.append(para(
        "La qualite du systeme a ete verifiee a deux niveaux : des tests automatises sur les services, "
        "et une <b>batterie de validation trilingue</b> du chatbot."))
    el.append(section("Tests automatises"))
    el.append(para(
        "33 tests automatises couvrent l'authentification, les operations CRUD, la moderation des avis "
        "et le televersement de fichiers, tous reussis."))
    el.append(section("Batterie de validation du chatbot"))
    el.append(para(
        "Nous avons constitue une batterie de <b>90 questions reelles</b> (30 par langue : francais, "
        "anglais, darija), reparties sur sept categories (administration, etudes, enseignants, "
        "horaires, orientation, vie etudiante, institutionnel), executees directement sur le moteur."))
    ts = _test_stats()
    if ts:
        rows = [["Langue", "Questions", "Confiance moyenne (FAQ)", "Reponses IA via Groq"]]
        labels = {"fr": "Francais", "en": "Anglais", "darija": "Darija"}
        for lg in ("fr", "en", "darija"):
            b = ts["by"].get(lg)
            if b:
                rows.append([labels[lg], str(b["n"]), f"{b['avg']:.2f}", f"{b['groq']}/{b['n']}"])
        rows.append(["Total", str(ts["n"]), "—", f"{ts['groq']}/{ts['n']}"])
        el += table(rows, "Resultats de la batterie de 90 questions (execution reelle)",
                    col_widths=[2.4, 2.0, 3.4, 2.2], font=8.4)
        el.append(para(
            "Le mode IA a fourni une reponse pour la totalite des 90 questions (modele principal "
            "LLaMA 3.3-70B, complete par le modele leger 3.1-8B apres atteinte du quota journalier "
            "gratuit). Le detail complet figure dans le rapport de test dedie."))
    else:
        el += table([
            ["Langue", "Questions", "Categories"],
            ["Francais", "30", "7"],
            ["Anglais", "30", "7"],
            ["Darija", "30", "7"],
            ["Total", "90", "7"],
        ], "Composition de la batterie de validation", col_widths=[2.6, 2.4, 5.0], font=8.6)
    el.append(section("Apport du branchement de la base de connaissances"))
    el.append(para(
        "Le test a confirme un progres decisif. Avant le branchement de la base de connaissances dans "
        "le RAG, des questions institutionnelles echouaient en mode IA ; apres, elles sont correctement "
        "traitees :"))
    el += table([
        ["Question (mode IA)", "Avant", "Apres (corrige)"],
        ["Qui est le doyen de la FSBM ?", "Je n'ai pas l'info", "Pr. Abdeslam EL BOUARI"],
        ["Combien de professeurs ?", "Je n'ai pas l'info", "239 enseignants-chercheurs"],
        ["Domaines de recherche du Pr. Benlahmer ?", "Je n'ai pas l'info", "TALN, web semantique, ML"],
        ["Qui dirige le departement informatique ?", "Je n'ai pas l'info", "Pr. ADNAOUI Khalid"],
    ], "Avant / apres l'ancrage de la base de connaissances reelle", col_widths=[4.4, 2.6, 3.0], font=8.0)
    el.append(alert(
        "Ce resultat illustre concretement l'interet du RAG : la qualite d'un assistant ne tient pas "
        "qu'au modele, mais a la <b>qualite des connaissances</b> qu'on lui fournit.", "tip"))
    el.append(section("Mode classique : 100 % sans connexion"))
    el.append(para(
        "Grace au resolveur hybride (regles + base de connaissances), le <b>mode classique</b> "
        "(TF-IDF, ~10 ms, hors ligne) atteint desormais <b>100 % de bonnes reponses</b> sur les 90 "
        "questions de la batterie, dans les trois langues — y compris les questions factuelles "
        "(doyen, nombre de professeurs, responsable de filiere, domaines de recherche) qui restaient "
        "auparavant sans reponse correcte. Le detail figure dans le rapport de test dedie."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_securite():
    el = chapter("Securite")
    el.append(para(
        "La securite a ete prise en compte des la conception, en particulier pour l'espace "
        "d'administration."))
    el += table([
        ["Menace", "Contre-mesure"],
        ["Acces non autorise", "Authentification JWT + controle d'acces par roles (RBAC)"],
        ["Vol de mots de passe", "Hachage bcrypt (jamais de stockage en clair)"],
        ["Injection SQL", "Requetes parametrees via SQLAlchemy (ORM)"],
        ["XSS", "Echappement automatique du contenu par Angular"],
        ["Donnees invalides", "Validation systematique par schemas Pydantic"],
        ["Fuite de secrets", "Cles et mots de passe dans un fichier .env exclu du depot"],
    ], "Menaces et contre-mesures", col_widths=[3.2, 6.8], font=8.6)
    el.append(para(
        "L'espace d'administration est <b>masque</b> a l'utilisateur normal et protege par un garde "
        "de route (guard) cote frontend, double d'une verification du jeton cote backend."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_gestion():
    el = chapter("Gestion de Projet")
    el.append(para(
        "Le projet a ete conduit selon une demarche <b>iterative et incrementale</b>, organisee en "
        "phases livrables et testables."))
    el += table([
        ["Phase", "Contenu principal"],
        ["1. Etude et conception", "Besoins, UML, architecture, choix technologiques"],
        ["2. Socle technique", "Micro-services, bases de donnees, donnees reelles"],
        ["3. Moteur conversationnel", "NLP multilingue, RAG, integration LLaMA 3"],
        ["4. Interfaces", "Frontend Angular, espace d'administration"],
        ["5. Validation", "Tests automatises, batterie trilingue, corrections"],
    ], "Phases du projet", col_widths=[3.0, 7.0], font=8.6)
    el.append(section("Outils"))
    el += bullets([
        "<b>Gestion de code</b> : Git.",
        "<b>Developpement</b> : Visual Studio Code, Angular CLI, Python.",
        "<b>Bases de donnees</b> : MySQL Workbench, MongoDB.",
        "<b>Test d'API</b> : documentation Swagger generee par FastAPI.",
        "<b>Modelisation</b> : diagrammes UML (Mermaid).",
    ])
    el.append(section("Repartition du travail"))
    el.append(para(
        "L'equipe, composee de trois etudiants, s'est repartie les volets backend, frontend et IA, avec "
        "une integration continue des contributions et des revues croisees."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_limites_persp():
    el = chapter("Limites et Perspectives")
    el.append(section("Limites"))
    el += bullets([
        "La FAQ (TF-IDF) ne couvre que les 28 intentions du corpus et ne raisonne pas.",
        "Le mode generatif depend d'un service externe (Internet) ; le repli local reste plus simple.",
        "Certaines donnees (modules detailles) ne sont pas publiees et sont modelisees (simulation).",
        "Le corpus, bien que riche, gagnerait a un apprentissage continu a partir des echanges reels.",
    ])
    el.append(section("Perspectives"))
    el += bullets([
        "<b>Application mobile</b> consommant les memes API REST.",
        "<b>Apprentissage continu</b> : enrichir le corpus a partir des questions a faible confiance.",
        "<b>Recherche semantique</b> par embeddings neuronaux en complement du TF-IDF.",
        "<b>Synchronisation</b> de la FAQ administrable avec le modele NLP.",
        "<b>Integration</b> a l'environnement numerique de travail (ENT) de l'universite.",
        "<b>Industrialisation</b> : conteneurisation Docker et chaine CI/CD.",
    ])
    return el


def _ch_conclusion():
    el = front_chapter("Conclusion Generale")
    el.append(para(
        "Ce projet de fin d'etudes a permis de concevoir et de realiser une plateforme universitaire "
        "intelligente repondant a un besoin concret de la FSBM : un assistant conversationnel "
        "multilingue, fiable et disponible en permanence, fonde sur des donnees reelles et une "
        "architecture moderne. La combinaison d'un classifieur TF-IDF et d'un grand modele de langage "
        "encadre par un RAG ancre sur une base de connaissances institutionnelle a demontre sa "
        "pertinence, notamment par la correction d'un defaut majeur d'ancrage qui faisait echouer le "
        "modele sur des questions pourtant connues."))
    el.append(para(
        "Au-dela de la realisation logicielle, ce travail aura ete une experience d'ingenierie "
        "complete, mobilisant le developpement full-stack, les bases de donnees et l'intelligence "
        "artificielle — au coeur de la Licence en Developpement Informatique. Les perspectives ouvertes "
        "(mobilite, apprentissage continu, integration a l'ENT) temoignent du potentiel de la "
        "plateforme a devenir un veritable portail intelligent au service de la reussite etudiante."))
    el.append(quote("La meilleure facon de predire l'avenir est de le creer.", "Peter Drucker"))
    return el


def _ch_sources():
    el = front_chapter("Sources et Webographie")
    el.append(para(
        "Les donnees institutionnelles mobilisees dans ce rapport proviennent de sources reelles et "
        "verifiables. Les references techniques renvoient aux documentations officielles des "
        "technologies employees."))
    el.append(section("Sources institutionnelles (donnees reelles)"))
    el += bullets([
        "Faculte des Sciences Ben M'Sick — <b>fsbm.ma</b> (departements, formations, corps professoral, mot du doyen, actualites).",
        "Universite Hassan II de Casablanca — <b>univh2c.ma</b>.",
        "Google Scholar — profils des enseignants-chercheurs (citations, h-index) : <b>scholar.google.com</b>.",
        "Office National des Oeuvres Universitaires (bourses) — <b>onousc.ma</b>.",
    ])
    el.append(section("References techniques"))
    el += bullets([
        "Angular — <b>angular.dev</b>.",
        "FastAPI — <b>fastapi.tiangolo.com</b>.",
        "scikit-learn (TF-IDF, similarite cosinus) — <b>scikit-learn.org</b>.",
        "Groq (inference LLaMA 3) — <b>console.groq.com</b>.",
        "MySQL — <b>dev.mysql.com</b> ; MongoDB — <b>mongodb.com</b>.",
        "JSON Web Tokens — <b>jwt.io</b>.",
    ])
    return el


def _ch_acronymes():
    el = front_chapter("Glossaire et Acronymes")
    el += table([
        ["Acronyme", "Signification"],
        ["API", "Application Programming Interface (interface de programmation)"],
        ["CRUD", "Create, Read, Update, Delete (operations de base de donnees)"],
        ["FSBM", "Faculte des Sciences Ben M'Sick"],
        ["JWT", "JSON Web Token (jeton d'authentification)"],
        ["LLM", "Large Language Model (grand modele de langage)"],
        ["NLP / TALN", "Natural Language Processing / Traitement Automatique du Langage Naturel"],
        ["ORM", "Object-Relational Mapping"],
        ["RAG", "Retrieval-Augmented Generation (generation augmentee par recuperation)"],
        ["RBAC", "Role-Based Access Control (controle d'acces par roles)"],
        ["REST", "Representational State Transfer"],
        ["SPA", "Single Page Application (application monopage)"],
        ["TF-IDF", "Term Frequency - Inverse Document Frequency"],
        ["UH2C", "Universite Hassan II de Casablanca"],
        ["UML", "Unified Modeling Language"],
    ], "Principaux acronymes et termes techniques", col_widths=[2.6, 7.4], font=8.8)
    return el


if __name__ == "__main__":
    build_min()
