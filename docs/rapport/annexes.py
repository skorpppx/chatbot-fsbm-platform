# -*- coding: utf-8 -*-
"""Annexes et bibliographie du rapport PFE."""
from report_engine import *
import fsbm_real as R
import os as _os

_FSBM_SHOTS_DIR = _os.path.join(PROJECT, "screen-shot-FSBM")
def _fsbm_shot(idx):
    files = sorted(f for f in _os.listdir(_FSBM_SHOTS_DIR) if f.lower().endswith(".png"))
    return _os.path.join(_FSBM_SHOTS_DIR, files[idx-1])


def build():
    el = []
    el += _intro()
    # ─── Donnees REELLES FSBM ─────────────────────────────────────────────────
    el += _annexe_reel_departements()
    el += _annexe_reel_filieres()
    el += _annexe_reel_professeurs()
    el += _annexe_reel_sources()
    el += _annexe_reel_captures()
    # ─── Annexes techniques ───────────────────────────────────────────────────
    el += _annexe_A()
    el += _annexe_B()
    el += _annexe_C()
    el += _annexe_D()
    el += _annexe_E()
    el += _annexe_F()
    el += _annexe_G()
    el += _annexe_H()
    el += _biblio()
    return el


# ══════════════════════════════════════════════════════════════════════════════
#  ANNEXES — DONNEES REELLES DE LA FSBM (sources verifiables)
# ══════════════════════════════════════════════════════════════════════════════
def _annexe_reel_departements():
    el = [pagebreak(), Paragraph("Annexe R-B — Liste reelle des departements de la FSBM", ST["h1n"]),
          hr(NAVY, 1.2), spacer(0.2)]
    el.append(para(
        f"La Faculte des Sciences Ben M'Sick, dirigee par {R.DOYEN}, est organisee en "
        f"{len(R.DEPARTEMENTS)} departements pedagogiques. Donnees relevees sur le site officiel "
        "fsbm.ma (juin 2026)."))
    rows = [["#", "Departement", "Chef de departement"]]
    for i, d in enumerate(R.DEPARTEMENTS, 1):
        rows.append([str(i), d["nom"], d["chef"]])
    el += table(rows, "Liste reelle des departements de la FSBM et de leurs chefs",
                col_widths=[0.8, 5.2, 4.0])
    return el


def _annexe_reel_filieres():
    el = [pagebreak(), Paragraph("Annexe R-C — Liste reelle des filieres de la FSBM", ST["h1n"]),
          hr(NAVY, 1.2), spacer(0.2)]
    el.append(para(
        "Filieres reelles recensees par departement, avec leur cycle et leur responsable "
        "pedagogique (source : fsbm.ma, pages Formation et Departements)."))
    dep_name = {d["code"]: d["nom"] for d in R.DEPARTEMENTS}
    rows = [["Departement", "Filiere", "Cycle", "Responsable"]]
    for code in [d["code"] for d in R.DEPARTEMENTS]:
        for dept, nom, typ, resp in R.FILIERES:
            if dept == code:
                rows.append([dep_name[code].split(" et ")[0], nom, typ.capitalize(), resp])
    el += table(rows, "Liste reelle des filieres de la FSBM par departement",
                col_widths=[2.0, 4.4, 1.3, 2.3], font=7.8)
    return el


def _annexe_reel_professeurs():
    el = [pagebreak(), Paragraph("Annexe R-A — Corps professoral reel de la FSBM", ST["h1n"]),
          hr(NAVY, 1.2), spacer(0.2)]
    el.append(para(
        f"Le corps professoral de la FSBM compte <b>{R.NB_PROFS_REEL} enseignants-chercheurs</b> "
        "(source : fsbm.ma/faculty, 20 pages). Conformement au principe de ne presenter que des "
        "donnees verifiables, nous reproduisons ci-dessous un echantillon representatif des noms "
        "reels releves, sans leur attribuer de metriques non verifiees."))
    sample = R.PROFS_REELS
    half = (len(sample) + 1) // 2
    rows = [["Enseignant", "Grade / Fonction", "Enseignant", "Grade / Fonction"]]
    for i in range(half):
        l = sample[i]; r = sample[i + half] if i + half < len(sample) else ("", "")
        rows.append([f"Pr. {l[0]}", l[1], (f"Pr. {r[0]}" if r[0] else ""), r[1]])
    el += table(rows, "Echantillon du corps professoral reel de la FSBM (source : fsbm.ma)",
                col_widths=[3.0, 2.0, 3.0, 2.0], font=7.6)
    el.append(Paragraph("Profils Google Scholar verifies (reseau de l'encadrant)", ST["h2n"]))
    el.append(para(
        "En exploitant le reseau de co-auteurs de l'encadrant, cinq profils de chercheurs de la FSBM "
        "et de l'Universite Hassan II ont pu etre identifies et verifies. Les metriques ci-dessous "
        "proviennent toutes de Google Scholar (profils publics) ; aucune n'est estimee."))
    sr = [["Chercheur", "Affiliation", "Themes", "Cit.", "h", "i10"]]
    for sp in R.SCHOLAR_PROFS:
        sr.append([sp["nom"], sp["affiliation"], sp["interets"][:42],
                   str(sp["citations"]), str(sp["h_index"]), str(sp["i10_index"])])
    el += table(sr, "Profils Google Scholar verifies de chercheurs FSBM / UH2C",
                col_widths=[2.6, 1.9, 2.8, 0.9, 0.6, 0.7], font=7.6)
    el.append(para(
        "Le Pr. Omar ZAHOUR, en particulier, a publie sur les chatbots d'orientation educative, "
        "thematique directement liee a notre projet. Pour les autres enseignants reels de la faculte, "
        "seuls les noms sont reproduits, sans metriques non verifiees, conformement a la rigueur "
        "scientifique."))
    return el


def _annexe_reel_sources():
    el = [pagebreak(), Paragraph("Annexe R-D — Sources academiques et institutionnelles", ST["h1n"]),
          hr(NAVY, 1.2), spacer(0.2)]
    el.append(para(
        "Toutes les donnees presentees comme reelles dans ce memoire proviennent exclusivement des "
        "sources verifiables suivantes. Aucune donnee reelle n'a ete inventee."))
    el += [Paragraph(f"<b>[S{i+1}]</b> {s}", ST["num"]) for i, s in enumerate(R.SOURCES)]
    el.append(spacer(0.2))
    el.append(alert(
        "Contact officiel de la faculte : " + R.CONTACT["email"] + " — " + R.CONTACT["tel"] +
        " — " + R.CONTACT["adresse"] + ".", "info"))
    return el


def _annexe_reel_captures():
    el = [pagebreak(), Paragraph("Annexe R-E — Captures officielles du site FSBM", ST["h1n"]),
          hr(NAVY, 1.2), spacer(0.2)]
    el.append(para(
        "Les captures suivantes, relevees sur le site institutionnel fsbm.ma, attestent de "
        "l'authenticite des donnees integrees a la plateforme (departements, filieres, corps "
        "professoral, mot du doyen)."))
    caps = [
        (3, "Departement de Mathematiques et Informatique et ses filieres reelles"),
        (5, "Departement de Chimie et ses filieres reelles"),
        (6, "Departement de Biologie et ses filieres reelles"),
        (7, "Mot du Doyen, Pr. Abdeslam EL BOUARI"),
        (8, "Corps professoral de la FSBM (239 enseignants recenses)"),
    ]
    for idx, cap in caps:
        try:
            el += figure_img(_fsbm_shot(idx), cap, max_h=10*cm)
        except Exception:
            pass
    return el


def _intro():
    el = front_chapter("Annexes")
    el.append(para(
        "Cette partie regroupe les elements de reference complementaires au corps du memoire : "
        "methodologie et planification du projet, catalogue exhaustif des interfaces de programmation, "
        "dictionnaire de donnees complet, schemas des collections NoSQL, liste des intentions du "
        "chatbot, diagrammes UML complementaires, extraits de code significatifs et guide "
        "d'installation. Ces annexes attestent de la profondeur et de la rigueur de la realisation."))
    el.append(Paragraph("Donnees reelles de la FSBM (sources verifiables)", ST["h2n"]))
    el += bullets([
        "Annexe R-A — Corps professoral reel de la FSBM (+ profil Scholar de l'encadrant)",
        "Annexe R-B — Liste reelle des departements",
        "Annexe R-C — Liste reelle des filieres",
        "Annexe R-D — Sources academiques et institutionnelles",
        "Annexe R-E — Captures officielles du site FSBM",
    ])
    el.append(Paragraph("Annexes techniques", ST["h2n"]))
    el += bullets([
        "Annexe A — Methodologie et gestion de projet",
        "Annexe B — Catalogue complet des API REST",
        "Annexe C — Dictionnaire de donnees complet (MySQL)",
        "Annexe D — Schemas des collections MongoDB",
        "Annexe E — Liste des intentions du chatbot",
        "Annexe F — Diagrammes UML complementaires",
        "Annexe G — Extraits de code significatifs",
        "Annexe H — Guide d'installation et d'utilisation",
    ])
    return el


# ─── ANNEXE A : METHODOLOGIE & GANTT ──────────────────────────────────────────
def _annexe_A():
    el = [pagebreak(), Paragraph("Annexe A — Methodologie et Gestion de Projet", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para(
        "Le projet a ete conduit selon une approche <b>iterative et incrementale</b> inspiree des "
        "methodes agiles. Le travail a ete organise en iterations courtes, chacune produisant un "
        "increment fonctionnel demontrable, ce qui a permis d'integrer regulierement les retours et "
        "d'ajuster les priorites. Les grandes phases du projet sont resumees ci-dessous."))
    el += table([
        ["Phase", "Contenu principal", "Livrables"],
        ["1. Cadrage", "Etude du besoin, etat de l'existant", "Problematique, objectifs"],
        ["2. Analyse & conception", "Besoins, UML, modele de donnees", "Diagrammes, schemas"],
        ["3. Socle technique", "Architecture, services, bases de donnees", "Squelette fonctionnel"],
        ["4. IA conversationnelle", "NLP, multilingue, RAG, LLaMA", "Chatbot operationnel"],
        ["5. Espace public", "Pages de consultation, avis", "Frontend public"],
        ["6. Administration & securite", "Auth JWT, CRUD, moderation, upload", "Espace admin securise"],
        ["7. Tests & finalisation", "Tests, corrections, documentation", "Plateforme validee, memoire"],
    ], "Phases de realisation du projet", col_widths=[2.2, 4.2, 3.6], font=8.4)

    def gantt(fig):
        ax = fig.add_subplot(111)
        phases = ["Cadrage", "Analyse & conception", "Socle technique", "IA conversationnelle",
                  "Espace public", "Admin & securite", "Tests & finalisation"]
        starts = [0, 2, 4, 6, 9, 11, 14]
        durs   = [2, 2, 3, 3, 2, 3, 3]
        cols = ["#1C3F6E", "#2d5a9e", "#13A89E", "#FF6B35", "#2d5a9e", "#1C3F6E", "#13A89E"]
        y = range(len(phases))
        ax.barh(list(y), durs, left=starts, color=cols, edgecolor="white")
        ax.set_yticks(list(y)); ax.set_yticklabels(phases, fontsize=8)
        ax.invert_yaxis(); ax.set_xlabel("Semaines"); ax.set_xlim(0, 17)
        ax.set_title("Diagramme de Gantt previsionnel du projet", fontsize=10)
        ax.grid(axis="x", linestyle=":", alpha=0.5)
    el += chart(gantt, "Diagramme de Gantt du deroulement du projet", h_cm=7.5)

    el.append(Paragraph("Repartition des taches", ST["h2n"]))
    el += table([
        ["Membre", "Contributions principales"],
        ["Akram BELMOUSSA", "Architecture, services backend, IA conversationnelle, securite"],
        ["Zakaria BENGHAZALE", "Frontend Angular, interfaces, espace d'administration, tests"],
        ["Nouhaila BEN SOUMANE", "Modelisation des donnees, dataset multilingue, documentation, validation"],
    ], "Repartition indicative des taches au sein de l'equipe", col_widths=[2.6, 7.4])
    el.append(alert("La repartition ci-dessus est indicative : le projet a fait l'objet d'une forte "
                    "collaboration, chaque membre ayant contribue de maniere transverse.", "info"))
    return el


# ─── ANNEXE B : API ───────────────────────────────────────────────────────────
def _annexe_B():
    el = [pagebreak(), Paragraph("Annexe B — Catalogue Complet des API REST", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para("Chatbot-Service (port 8001) :"))
    el += table([
        ["Methode", "Endpoint", "Description"],
        ["POST", "/api/chat", "Message au chatbot (mode TF-IDF)"],
        ["POST", "/api/chat/feedback", "Retour utilisateur sur une reponse"],
        ["GET", "/api/chat/history/{session}", "Historique d'une session"],
        ["GET", "/api/chat/suggestions", "Suggestions de questions"],
        ["GET", "/api/chat/news", "Actualites agregees"],
        ["GET", "/api/intents", "Liste des intentions"],
        ["POST", "/api/llm/chat", "Message au chatbot (mode LLaMA + RAG)"],
        ["GET", "/api/llm/status", "Etat des fournisseurs IA"],
        ["GET", "/api/llm/models", "Modeles disponibles"],
        ["GET", "/api/health", "Etat de sante du service"],
    ], "Endpoints du Chatbot-Service", col_widths=[1.2, 4.0, 4.8], font=8.2)
    el.append(para("Academic-Service (port 8002) — espace public :"))
    el += table([
        ["Methode", "Endpoint", "Description"],
        ["GET", "/api/overview", "Compteurs du tableau de bord"],
        ["GET", "/api/departments", "Liste des departements"],
        ["GET", "/api/filieres", "Liste des filieres (filtres)"],
        ["GET", "/api/filieres/{id}/modules", "Modules d'une filiere"],
        ["GET", "/api/modules", "Liste des modules"],
        ["GET", "/api/professors", "Annuaire (pagine)"],
        ["GET", "/api/students", "Etudiants (pagine)"],
        ["GET", "/api/schedule", "Emploi du temps"],
        ["GET", "/api/exams", "Calendrier des examens"],
        ["GET", "/api/announcements", "Annonces"],
        ["GET", "/api/events", "Evenements"],
        ["GET", "/api/clubs", "Clubs etudiants"],
        ["POST", "/api/reviews", "Deposer un avis"],
        ["GET", "/api/reviews", "Avis approuves"],
        ["GET", "/api/reviews/stats", "Statistiques des avis"],
    ], "Endpoints publics de l'Academic-Service", col_widths=[1.2, 4.0, 4.8], font=8.2)
    el.append(para("Academic-Service — espace d'administration (protege par JWT) :"))
    el += table([
        ["Methode", "Endpoint", "Description"],
        ["POST", "/api/auth/login", "Authentification"],
        ["GET", "/api/auth/me", "Profil courant"],
        ["GET/POST/PUT/DELETE", "/api/admin/announcements", "CRUD annonces"],
        ["GET/POST/PUT/DELETE", "/api/admin/events", "CRUD evenements"],
        ["POST/PUT/DELETE", "/api/admin/filieres", "CRUD filieres"],
        ["POST/PUT/DELETE", "/api/admin/modules", "CRUD modules"],
        ["POST/PUT/DELETE", "/api/admin/professors", "CRUD professeurs"],
        ["POST/PUT/DELETE", "/api/admin/departments", "CRUD departements"],
        ["GET/POST/PUT/DELETE", "/api/admin/clubs", "CRUD clubs"],
        ["GET/POST/PUT/DELETE", "/api/admin/faq", "CRUD FAQ"],
        ["GET/PATCH/DELETE", "/api/admin/reviews", "Moderation des avis"],
        ["POST", "/api/admin/upload", "Televersement de fichiers"],
    ], "Endpoints d'administration de l'Academic-Service", col_widths=[2.4, 3.4, 4.2], font=8.0)
    return el


# ─── ANNEXE C : DICTIONNAIRE DE DONNEES ───────────────────────────────────────
def _annexe_C():
    el = [pagebreak(), Paragraph("Annexe C — Dictionnaire de Donnees Complet (MySQL)", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para("Les dictionnaires suivants detaillent les colonnes des principales tables du schema relationnel."))

    def dd(title, rows, cap):
        out = [Paragraph(title, ST["h2n"])]
        out += table([["Colonne", "Type", "Contrainte", "Description"]] + rows, cap,
                     col_widths=[2.2, 1.8, 2.2, 3.8], font=8.2)
        return out

    el += dd("Table departments", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["code", "VARCHAR(20)", "UNIQUE", "Code (MI, PH, CH...)"],
        ["name", "VARCHAR(150)", "NOT NULL", "Intitule"],
        ["head_name", "VARCHAR(150)", "NULL", "Chef de departement"],
        ["head_email", "VARCHAR(150)", "NULL", "Courriel du chef"],
        ["color_hex", "VARCHAR(7)", "NULL", "Couleur d'affichage"],
        ["logo_url", "VARCHAR(255)", "NULL", "Logo (Phase 2)"],
    ], "Dictionnaire de la table departments")

    el += dd("Table modules", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["code", "VARCHAR(30)", "UNIQUE", "Code du module"],
        ["name", "VARCHAR(200)", "NOT NULL", "Intitule"],
        ["filiere_id", "BIGINT", "FK", "Filiere de rattachement"],
        ["semester", "TINYINT", "NOT NULL", "Semestre (1-6)"],
        ["credits", "TINYINT", "DEFAULT 4", "Credits ECTS"],
        ["coefficient", "DECIMAL(3,1)", "DEFAULT 1.0", "Coefficient"],
        ["is_eliminatory", "BOOLEAN", "DEFAULT FALSE", "Note eliminatoire"],
    ], "Dictionnaire de la table modules")

    el += dd("Table professors", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["matricule", "VARCHAR(30)", "UNIQUE", "Matricule"],
        ["last_name", "VARCHAR(80)", "NOT NULL", "Nom"],
        ["email", "VARCHAR(150)", "UNIQUE", "Courriel"],
        ["grade", "ENUM", "DEFAULT PA", "PA, PH, PES, VACATAIRE"],
        ["department_id", "BIGINT", "FK", "Departement"],
        ["specialty", "VARCHAR(200)", "NULL", "Specialite"],
        ["photo_url", "VARCHAR(255)", "NULL", "Photo (Phase 2)"],
    ], "Dictionnaire de la table professors")

    el += dd("Table students", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["cne", "VARCHAR(20)", "UNIQUE", "Code National Etudiant"],
        ["last_name", "VARCHAR(80)", "NOT NULL", "Nom"],
        ["gender", "ENUM(M,F)", "NOT NULL", "Genre"],
        ["filiere_id", "BIGINT", "FK", "Filiere"],
        ["annee_etude", "TINYINT", "DEFAULT 1", "Annee d'etude"],
        ["statut", "ENUM", "DEFAULT ACTIF", "Statut administratif"],
        ["is_boursier", "BOOLEAN", "DEFAULT FALSE", "Boursier"],
    ], "Dictionnaire de la table students")

    el += dd("Table users", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["email", "VARCHAR(150)", "UNIQUE", "Courriel de connexion"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "Hash bcrypt"],
        ["role", "ENUM", "DEFAULT STUDENT", "STUDENT, PROF, SCOLARITE, ADMIN"],
        ["is_active", "BOOLEAN", "DEFAULT TRUE", "Compte actif"],
        ["last_login", "TIMESTAMP", "NULL", "Derniere connexion"],
    ], "Dictionnaire de la table users")

    el += dd("Table reviews", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["target_type", "ENUM", "NOT NULL", "AI_ASSISTANT, FACULTE, MODULE..."],
        ["target_id", "BIGINT", "NULL", "Cible eventuelle"],
        ["rating", "TINYINT", "1-5", "Note (assistant IA)"],
        ["comment", "TEXT", "NOT NULL", "Commentaire"],
        ["status", "ENUM", "DEFAULT APPROVED", "PENDING, APPROVED, HIDDEN"],
        ["admin_response", "TEXT", "NULL", "Reponse de l'administration"],
    ], "Dictionnaire de la table reviews")

    el += dd("Table conversations", [
        ["id", "BIGINT", "PK", "Identifiant"],
        ["session_id", "VARCHAR(100)", "INDEX", "Session conversationnelle"],
        ["user_message", "TEXT", "NOT NULL", "Message utilisateur"],
        ["bot_response", "TEXT", "NOT NULL", "Reponse du bot"],
        ["intent_detected", "VARCHAR(80)", "INDEX", "Intention reconnue"],
        ["confidence", "DECIMAL(5,4)", "NULL", "Score de confiance"],
        ["response_time_ms", "INT", "NULL", "Temps de reponse"],
    ], "Dictionnaire de la table conversations")

    el.append(Paragraph("Extraits du schema physique (DDL)", ST["h2n"]))
    el.append(para("Les instructions de creation effectivement appliquees sous MySQL 8 (moteur InnoDB, "
                   "jeu de caracteres utf8mb4) sont reproduites ci-dessous pour les tables centrales."))
    el += code(
        "CREATE TABLE departments (\n"
        "  id          BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "  code        VARCHAR(20)  NOT NULL UNIQUE,\n"
        "  name        VARCHAR(150) NOT NULL,\n"
        "  head_name   VARCHAR(150),\n"
        "  head_email  VARCHAR(150),\n"
        "  color_hex   VARCHAR(7) DEFAULT '#1C3F6E',\n"
        "  logo_url    VARCHAR(255),\n"
        "  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
    el += code(
        "CREATE TABLE filieres (\n"
        "  id            BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "  code          VARCHAR(20) NOT NULL UNIQUE,\n"
        "  name          VARCHAR(200) NOT NULL,\n"
        "  type          ENUM('LICENCE','LICENCE_PRO','MASTER',\n"
        "                     'MASTER_RECHERCHE','DOCTORAT') NOT NULL,\n"
        "  department_id BIGINT NOT NULL,\n"
        "  capacity      INT DEFAULT 100,\n"
        "  logo_url      VARCHAR(255),\n"
        "  is_active     BOOLEAN DEFAULT TRUE,\n"
        "  CONSTRAINT fk_filiere_dept FOREIGN KEY (department_id)\n"
        "      REFERENCES departments(id) ON DELETE RESTRICT,\n"
        "  INDEX idx_filiere_type (type)\n"
        ") ENGINE=InnoDB;")
    el += code(
        "CREATE TABLE users (\n"
        "  id            BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "  email         VARCHAR(150) NOT NULL UNIQUE,\n"
        "  password_hash VARCHAR(255) NOT NULL,\n"
        "  role          ENUM('STUDENT','PROFESSOR','SCOLARITE','ADMIN')\n"
        "                  NOT NULL DEFAULT 'STUDENT',\n"
        "  is_active     BOOLEAN DEFAULT TRUE,\n"
        "  last_login    TIMESTAMP NULL,\n"
        "  INDEX idx_user_role (role)\n"
        ") ENGINE=InnoDB;")
    el += code(
        "CREATE TABLE reviews (\n"
        "  id            BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "  target_type   ENUM('AI_ASSISTANT','MODULE','PROFESSOR',\n"
        "                     'FILIERE','FACULTE','GENERAL') NOT NULL,\n"
        "  target_id     BIGINT NULL,\n"
        "  rating        TINYINT NULL,\n"
        "  comment       TEXT NOT NULL,\n"
        "  status        ENUM('PENDING','APPROVED','HIDDEN') DEFAULT 'APPROVED',\n"
        "  admin_response TEXT NULL,\n"
        "  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  CONSTRAINT chk_rating CHECK (rating IS NULL OR rating BETWEEN 1 AND 5)\n"
        ") ENGINE=InnoDB;")
    return el


# ─── ANNEXE D : MONGODB ───────────────────────────────────────────────────────
def _annexe_D():
    el = [pagebreak(), Paragraph("Annexe D — Schemas des Collections MongoDB", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para("Document type de la collection conversation_logs :"))
    el += code(
        "{\n"
        "  \"_id\": ObjectId,\n"
        "  \"session_id\": \"sess_abc123\",\n"
        "  \"timestamp\": ISODate,\n"
        "  \"language\": \"fr | en | darija\",\n"
        "  \"user_message\": \"...\",\n"
        "  \"bot_response\": \"...\",\n"
        "  \"intent\": \"filieres\",\n"
        "  \"confidence\": 0.87,\n"
        "  \"provider\": \"groq | tfidf | huggingface\",\n"
        "  \"response_time_ms\": 152\n"
        "}")
    el.append(para("Document type de la collection nlp_analytics (agregat journalier) :"))
    el += code(
        "{\n"
        "  \"date\": \"2026-05-28\",\n"
        "  \"total_messages\": 342,\n"
        "  \"by_language\": { \"fr\": 180, \"en\": 40, \"darija\": 122 },\n"
        "  \"top_intents\": [ { \"intent\": \"inscription\", \"count\": 58 }, ... ],\n"
        "  \"avg_confidence\": 0.81,\n"
        "  \"avg_response_time_ms\": 168\n"
        "}")
    el.append(para("Document type de la collection feedback :"))
    el += code(
        "{\n"
        "  \"conversation_id\": 42,\n"
        "  \"note\": 5,\n"
        "  \"is_helpful\": true,\n"
        "  \"commentaire\": \"Tres clair, merci !\",\n"
        "  \"created_at\": ISODate\n"
        "}")
    return el


# ─── ANNEXE E : INTENTIONS ────────────────────────────────────────────────────
def _annexe_E():
    el = [pagebreak(), Paragraph("Annexe E — Liste des Intentions du Chatbot", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para("Le dataset reconnait 28 intentions reparties en categories informationnelles et conversationnelles."))
    intents = [
        ("salutation", "Accueil et salutations"), ("filieres", "Filieres proposees"),
        ("inscription", "Procedure d'inscription"), ("bourses", "Bourses et aides"),
        ("emploi_du_temps", "Emplois du temps"), ("examens", "Calendrier des examens"),
        ("resultats", "Consultation des resultats"), ("diplome", "Retrait de diplome"),
        ("contact_scolarite", "Contact de la scolarite"), ("masters", "Offre de masters"),
        ("master_iads", "Master IA & Data Science"), ("filiere_smi", "Filiere SMI"),
        ("filiere_di", "Filiere DI"), ("modules", "Modules et matieres"),
        ("professeurs", "Corps professoral"), ("departements", "Departements"),
        ("actualites", "Actualites de la faculte"), ("evenements", "Evenements"),
        ("clubs", "Vie etudiante et clubs"), ("stage_pfe", "Stages et PFE"),
        ("bibliotheque", "Bibliotheque"), ("au_revoir", "Prise de conge"),
        ("remerciement", "Remerciements"), ("comment_vas_tu", "Echange social"),
        ("stress_examens", "Soutien (stress)"), ("motivation_etudes", "Motivation"),
        ("demande_aide_psychologique", "Aide et ecoute"), ("identite_genre", "Personnalisation genre/nom"),
    ]
    rows = [["Intention", "Description", "Intention", "Description"]]
    half = (len(intents)+1)//2
    for i in range(half):
        l = intents[i]; r = intents[i+half] if i+half < len(intents) else ("", "")
        rows.append([l[0], l[1], r[0], r[1]])
    el += table(rows, "Les 28 intentions reconnues par le chatbot", col_widths=[2.0, 3.0, 2.0, 3.0], font=7.8)
    return el


# ─── ANNEXE F : UML COMPLEMENTAIRE ────────────────────────────────────────────
def _annexe_F():
    el = [pagebreak(), Paragraph("Annexe F — Diagrammes UML Complementaires", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para("Diagramme de sequence : televersement d'un fichier par l'administrateur."))
    el += figure_mermaid(r'''sequenceDiagram
  actor AD as Administrateur
  participant F as Frontend
  participant S as Academic-Service
  participant FS as Stockage statique
  AD->>F: selectionne un fichier
  F->>S: POST /api/admin/upload (multipart + JWT)
  S->>S: verifier role + type + taille
  S->>FS: enregistrer le fichier (UUID)
  FS-->>S: chemin
  S-->>F: { url }
  F->>F: renseigne le champ image/logo
''', "Diagramme de sequence du televersement de fichier", max_h=10*cm)

    el.append(para("Diagramme d'activites : moderation d'un avis."))
    el += figure_mermaid(r'''flowchart TD
  A([Avis depose]) --> B{Auto-approbation ?}
  B -- Oui --> C[Approuve]
  B -- Non --> D[En attente]
  D --> E{Decision admin}
  E -- Approuver --> C
  E -- Masquer --> F[Masque]
  C --> G{Action ?}
  G -- Epingler --> H[Epingle]
  G -- Repondre --> I[Reponse ajoutee]
  G -- Supprimer --> J([Supprime])
  F --> J
''', "Diagramme d'activites de la moderation d'un avis", max_h=12*cm)
    return el


# ─── ANNEXE G : CODE ──────────────────────────────────────────────────────────
def _annexe_F2_placeholder(): pass

def _annexe_G():
    el = [pagebreak(), Paragraph("Annexe G — Extraits de Code Significatifs", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(Paragraph("Detection hybride de la langue", ST["h2n"]))
    el += code(
        "def detect(self, text):\n"
        "    if re.search(r'[\\u0600-\\u06FF]', text):      # caracteres arabes\n"
        "        return ('darija', 1.0)\n"
        "    if re.search(r'\\b\\w*[379]\\w*\\b', text):       # chiffres darija 3/7/9\n"
        "        return ('darija', 0.9)\n"
        "    scores = {l: sum(1 for k in KW[l] if k in text.lower()) for l in LANGS}\n"
        "    best = max(scores, key=scores.get)\n"
        "    return (best, scores[best] / (sum(scores.values()) or 1))")
    el.append(Paragraph("Construction de l'invite RAG", ST["h2n"]))
    el += code(
        "def build_rag_prompt(question, contexts, history, lang):\n"
        "    system = SYSTEM_PROMPTS[lang]\n"
        "    ctx = '\\n\\n'.join(f'[CONTEXTE {i+1}] {c.text}'\n"
        "                       for i, c in enumerate(contexts))\n"
        "    messages = [\n"
        "        {'role': 'system', 'content': system},\n"
        "        {'role': 'system', 'content': f'## CONTEXTES\\n{ctx}'},\n"
        "        *history,\n"
        "        {'role': 'user', 'content': question},\n"
        "    ]\n"
        "    return messages")
    el.append(Paragraph("Cascade de repli du service LLM", ST["h2n"]))
    el += code(
        "async def chat(self, message, ...):\n"
        "    if self.groq.available:\n"
        "        try: return await self.groq.chat(...)\n"
        "        except Exception: pass\n"
        "    if self.hf.available:\n"
        "        try: return await self.hf.chat(...)\n"
        "        except Exception: pass\n"
        "    return self.tfidf_fallback(message)     # toujours disponible")
    el.append(Paragraph("Intercepteur HTTP Angular (injection du jeton)", ST["h2n"]))
    el += code(
        "export const authInterceptor: HttpInterceptorFn = (req, next) => {\n"
        "  const token = inject(AuthService).token();\n"
        "  if (token && req.url.startsWith('/api/academic')) {\n"
        "    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });\n"
        "  }\n"
        "  return next(req);\n"
        "};")
    return el


# ─── ANNEXE H : INSTALLATION ──────────────────────────────────────────────────
def _annexe_H():
    el = [pagebreak(), Paragraph("Annexe H — Guide d'Installation et d'Utilisation", ST["h1n"]), hr(NAVY, 1.2), spacer(0.2)]
    el.append(para("Prerequis : Python 3.11+, Node.js 18+, MySQL 8, MongoDB, navigateur moderne."))
    el.append(Paragraph("Installation automatisee", ST["h2n"]))
    el += code(
        "# 1. Cloner le projet\n"
        "git clone <depot> && cd chatbot-fsbm-platform\n"
        "# 2. Installation complete (deps, base, donnees)\n"
        "powershell -ExecutionPolicy Bypass -File .\\SETUP.ps1\n"
        "# 3. Lancement des trois services\n"
        "powershell -ExecutionPolicy Bypass -File .\\start.ps1")
    el.append(para("Points d'acces apres lancement :"))
    el += table([
        ["Service", "URL"],
        ["Plateforme (frontend)", "http://localhost:4200"],
        ["Espace administration", "http://localhost:4200/admin/login"],
        ["API Chatbot (Swagger)", "http://localhost:8001/docs"],
        ["API Academic (Swagger)", "http://localhost:8002/docs"],
    ], "Points d'acces de la plateforme", col_widths=[3.6, 6.4])
    el.append(alert("Compte administrateur de demonstration : admin@fsbm.ac.ma / Admin@FSBM2026 "
                    "(a modifier imperativement en production).", "warn"))

    el.append(Paragraph("Configuration du routage (proxy de developpement)", ST["h2n"]))
    el += code(
        "{\n"
        "  \"/api/chat\":     { \"target\": \"http://localhost:8001\" },\n"
        "  \"/api/llm\":      { \"target\": \"http://localhost:8001\" },\n"
        "  \"/api/academic\": { \"target\": \"http://localhost:8002\",\n"
        "                    \"pathRewrite\": { \"^/api/academic\": \"/api\" } }\n"
        "}")
    el.append(Paragraph("Variables d'environnement (extrait de .env.example)", ST["h2n"]))
    el += code(
        "SERVICE_PORT=8002\n"
        "DB_HOST=localhost\nDB_NAME=fsbm_db\nDB_USER=root\nDB_PASSWORD=********\n"
        "JWT_SECRET=********  # chaine longue et aleatoire\n"
        "JWT_EXPIRE_MINUTES=720\n"
        "GROQ_API_KEY=********\n"
        "CORS_ORIGINS=http://localhost:4200")
    el.append(Paragraph("Validation de schema MongoDB (exemple)", ST["h2n"]))
    el += code(
        "{\n"
        "  \"$jsonSchema\": {\n"
        "    \"bsonType\": \"object\",\n"
        "    \"required\": [\"session_id\", \"created_at\"],\n"
        "    \"properties\": {\n"
        "      \"session_id\": { \"bsonType\": \"string\" },\n"
        "      \"language\":   { \"enum\": [\"fr\", \"en\", \"darija\"] },\n"
        "      \"message_count\": { \"bsonType\": \"int\", \"minimum\": 0 }\n"
        "    }\n"
        "  }\n"
        "}")
    return el


# ─── BIBLIOGRAPHIE ────────────────────────────────────────────────────────────
def _biblio():
    el = front_chapter("Bibliographie et Webographie")
    el.append(Paragraph("Ouvrages et articles scientifiques", ST["h1n"]))
    refs = [
        "I. Sommerville, <i>Software Engineering</i>, 10e ed., Pearson, 2015.",
        "M. Fowler, <i>Patterns of Enterprise Application Architecture</i>, Addison-Wesley, 2002.",
        "S. Newman, <i>Building Microservices: Designing Fine-Grained Systems</i>, 2e ed., O'Reilly, 2021.",
        "D. Jurafsky et J. H. Martin, <i>Speech and Language Processing</i>, 3e ed. (draft), 2023.",
        "P. Lewis et al., \"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks\", "
        "<i>Advances in Neural Information Processing Systems (NeurIPS)</i>, 2020.",
        "A. Vaswani et al., \"Attention Is All You Need\", <i>NeurIPS</i>, 2017.",
        "H. Touvron et al., \"LLaMA: Open and Efficient Foundation Language Models\", arXiv:2302.13971, 2023.",
        "G. Salton et C. Buckley, \"Term-weighting approaches in automatic text retrieval\", "
        "<i>Information Processing & Management</i>, 1988.",
        "E. Gamma, R. Helm, R. Johnson, J. Vlissides, <i>Design Patterns</i>, Addison-Wesley, 1994.",
        "M. Jones, J. Bradley, N. Sakimura, \"JSON Web Token (JWT)\", <i>RFC 7519</i>, IETF, 2015.",
    ]
    el += [Paragraph(f"[{i+1}] {r}", ST["num"]) for i, r in enumerate(refs)]
    el.append(spacer(0.3))
    el.append(Paragraph("Documentation technique et ressources en ligne", ST["h1n"]))
    web = [
        "Documentation officielle Angular — angular.dev",
        "Documentation officielle FastAPI — fastapi.tiangolo.com",
        "Documentation SQLAlchemy 2.0 — docs.sqlalchemy.org",
        "Documentation MongoDB — www.mongodb.com/docs",
        "Documentation MySQL 8.0 — dev.mysql.com/doc",
        "Documentation scikit-learn — scikit-learn.org",
        "Documentation Pydantic — docs.pydantic.dev",
        "Documentation Groq (inference LLaMA) — console.groq.com/docs",
        "OWASP Top 10 — owasp.org/www-project-top-ten",
        "Specification OpenAPI — spec.openapis.org",
        "Unified Modeling Language (UML), Object Management Group — www.omg.org/spec/UML",
        "Site officiel de la Faculte des Sciences Ben M'Sick — fsbm.ma",
    ]
    el += [Paragraph(f"[W{i+1}] {w}", ST["num"]) for i, w in enumerate(web)]
    el.append(spacer(0.6))
    el.append(_finalbox())
    return el


from reportlab.platypus import Flowable
class _finalbox(Flowable):
    def wrap(self, aw, ah): self._w = aw; return (aw, 2.2*cm)
    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.roundRect(0, 0, self._w, 2.0*cm, 8, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(self._w/2, 1.25*cm, "Plateforme Universitaire Intelligente FSBM")
        c.setFont("Helvetica", 9)
        c.drawCentredString(self._w/2, 0.75*cm, "Projet de Fin d'Etudes 2025-2026")
        c.drawCentredString(self._w/2, 0.42*cm, "A. BELMOUSSA  -  Z. BENGHAZALE  -  N. BEN SOUMANE")
