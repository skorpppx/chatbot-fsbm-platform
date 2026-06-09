# -*- coding: utf-8 -*-
"""Chapitres 5 a 8 : architecture, bases de donnees, intelligence artificielle, securite."""
from report_engine import *


def build():
    return _ch5() + _ch6() + _ch7() + _ch8()


# ══════════════════════════════════════════════════════════════════════════════
def _ch5():
    el = chapter("Architecture du Systeme")
    el.append(para(
        "L'architecture logicielle conditionne la qualite, l'evolutivite et la maintenabilite d'une "
        "application. Ce chapitre justifie le choix d'une architecture micro-services, decrit "
        "l'organisation des couches frontend et backend, et detaille les mecanismes de communication "
        "entre les composants."))

    el.append(section("Choix d'une architecture micro-services"))
    el.append(para(
        "Une architecture <b>monolithique</b> regroupe l'ensemble des fonctionnalites dans une seule "
        "application deployee d'un bloc. Simple au depart, elle devient difficile a maintenir et a "
        "faire evoluer a mesure que le systeme grossit : un changement mineur impose de redeployer "
        "l'ensemble, et une defaillance peut affecter tout le service."))
    el.append(para(
        "Nous avons donc retenu une architecture <b>micro-services</b>, dans laquelle l'application "
        "est decoupee en services autonomes, chacun responsable d'un domaine fonctionnel precis, "
        "deployable et evolutif independamment. Notre plateforme s'organise autour de deux services "
        "metier principaux :"))
    el += bullets([
        "<b>Chatbot-Service (port 8001)</b> : comprehension du langage, classification des "
        "intentions, generation des reponses, integration des grands modeles de langage, memoire "
        "conversationnelle et journalisation des echanges.",
        "<b>Academic-Service (port 8002)</b> : gestion du referentiel academique (departements, "
        "filieres, modules, professeurs, etudiants), des contenus (annonces, evenements, clubs), de "
        "l'authentification, des avis et de la FAQ.",
    ])
    el.append(para(
        "Cette separation reflete deux preoccupations distinctes : l'intelligence conversationnelle "
        "d'une part, la gestion des donnees institutionnelles d'autre part. Elle permet, par exemple, "
        "de faire evoluer le moteur d'IA sans toucher au referentiel, ou de mettre a l'echelle le "
        "seul service le plus sollicite."))
    el += table([
        ["Critere", "Monolithe", "Micro-services (retenu)"],
        ["Couplage", "Fort", "Faible"],
        ["Deploiement", "Global", "Independant par service"],
        ["Mise a l'echelle", "Verticale (tout)", "Horizontale (par service)"],
        ["Resilience", "Panne globale", "Isolation des pannes"],
        ["Evolutivite", "Limitee", "Elevee"],
        ["Complexite operationnelle", "Faible", "Moderee"],
    ], "Comparaison monolithe / micro-services", col_widths=[2.6, 3.4, 4.0])

    el.append(section("Architecture en couches"))
    el.append(para(
        "Au-dela du decoupage en services, la plateforme respecte une architecture en couches "
        "(layered architecture) qui separe les responsabilites : presentation, communication, "
        "logique metier et persistance. La figure suivante presente cette organisation d'ensemble."))
    el += figure_mermaid(r'''flowchart TB
  subgraph P["Couche Presentation"]
    NG["Angular 17 SPA<br/>(navigateur, port 4200)"]
  end
  subgraph API["Couche API / Communication"]
    PX["Proxy de developpement<br/>(routage /api)"]
  end
  subgraph M["Couche Logique Metier"]
    CB["Chatbot-Service<br/>FastAPI :8001"]
    AC["Academic-Service<br/>FastAPI :8002"]
  end
  subgraph IA["Couche Intelligence"]
    NLP["NLP TF-IDF"]
    RAG["RAG + LLaMA 3"]
  end
  subgraph D["Couche Persistance"]
    SQL[("MySQL 8")]
    MGO[("MongoDB")]
  end
  NG --> PX
  PX --> CB
  PX --> AC
  CB --> NLP
  CB --> RAG
  CB --> MGO
  AC --> SQL
  CB -->|HTTP REST| AC
''', "Architecture en couches de la plateforme", max_h=15*cm)

    el.append(section("Le frontend Angular"))
    el.append(para(
        "Le frontend est une application monopage (SPA) developpee avec <b>Angular 17</b>. Il "
        "exploite les fonctionnalites les plus recentes du framework : composants <i>standalone</i> "
        "(sans NgModule), <i>signals</i> pour une gestion de l'etat reactive et performante, et "
        "<i>lazy loading</i> des routes pour ne charger que le code necessaire a chaque page."))
    el.append(para(
        "L'interface est organisee autour d'un <b>shell applicatif</b> (barre laterale de navigation "
        "et barre superieure) qui encapsule les pages publiques, tandis que l'espace d'administration "
        "occupe un gabarit plein ecran distinct. Un intercepteur HTTP injecte automatiquement le "
        "jeton d'authentification, et un garde de route (guard) protege l'acces a l'administration."))
    el += table([
        ["Element", "Technologie / Pattern", "Role"],
        ["Composants", "Standalone Components", "Briques d'interface autonomes et reutilisables"],
        ["Etat", "Signals", "Reactivite fine et detection de changement optimisee"],
        ["Routage", "Lazy loading", "Chargement differe des pages"],
        ["HTTP", "HttpClient + Interceptor", "Appels REST et injection du jeton JWT"],
        ["Securite", "CanActivate Guard", "Protection des routes d'administration"],
        ["Theme", "CSS variables", "Mode clair / sombre"],
    ], "Choix techniques du frontend Angular", col_widths=[2.0, 3.2, 4.8])

    el.append(subsection("Structure de navigation"))
    el.append(para(
        "Le routage Angular distingue deux espaces : un espace public encapsule dans le shell "
        "applicatif (barre laterale et superieure), et un espace d'administration plein ecran, "
        "protege par un garde de route. Le diagramme suivant illustre la navigation entre les "
        "principales vues."))
    el += figure_mermaid(r'''flowchart LR
  H["Accueil"] --> CH["Assistant IA"]
  H --> DEP["Departements"]
  H --> FIL["Filieres"]
  FIL --> FD["Detail filiere"]
  H --> MOD["Modules"]
  H --> PROF["Professeurs"]
  H --> ACT["Actualites"]
  H --> VIE["Vie etudiante"]
  H --> AV["Avis"]
  LOG["/admin/login"] -->|JWT| ADM["Espace admin"]
''', "Structure de navigation de l'application", max_h=8*cm)
    el.append(para(
        "Cette separation est mise en oeuvre par un routage a deux niveaux : une route parente "
        "portant le shell et ses routes enfants pour l'espace public, et des routes de premier niveau "
        "pour la connexion et le tableau de bord d'administration, ce dernier etant garde par une "
        "fonction de controle d'acces (CanActivate)."))

    el.append(section("Le backend FastAPI"))
    el.append(para(
        "Les deux services backend reposent sur <b>FastAPI</b>, framework Python moderne fonde sur la "
        "norme ASGI. FastAPI offre un traitement <b>asynchrone</b> des requetes (async/await), une "
        "<b>validation automatique</b> des donnees via Pydantic, et une <b>documentation interactive</b> "
        "generee automatiquement (Swagger UI et ReDoc). Chaque service suit une organisation claire : "
        "routeurs (points d'entree HTTP), schemas (validation), modeles (ORM) et services (logique)."))
    el.append(para(
        "L'acces a la base relationnelle s'effectue via <b>SQLAlchemy 2.0</b> en mode asynchrone "
        "(pilote aiomysql), ce qui evite de bloquer le serveur pendant les operations d'entree-sortie. "
        "Le code suivant illustre la concision d'un point d'entree FastAPI typique."))
    el += code(
        "@router.get('/api/filieres', response_model=list[FiliereOut])\n"
        "async def list_filieres(\n"
        "    type: str | None = Query(None),\n"
        "    search: str | None = Query(None),\n"
        "    db: AsyncSession = Depends(get_db),\n"
        "):\n"
        "    stmt = select(Filiere)\n"
        "    if type:\n"
        "        stmt = stmt.where(Filiere.type == type)\n"
        "    if search:\n"
        "        stmt = stmt.where(Filiere.name.ilike(f'%{search}%'))\n"
        "    result = await db.execute(stmt)\n"
        "    return result.scalars().all()")

    el.append(section("Communication REST et routage"))
    el.append(para(
        "Les echanges entre le frontend et les services s'effectuent selon le style <b>REST</b>, par "
        "des requetes HTTP transportant des donnees au format JSON. En developpement, un proxy "
        "integre au serveur Angular route les chemins applicatifs vers le bon service, evitant ainsi "
        "les problemes de partage de ressources entre origines (CORS) :"))
    el += table([
        ["Chemin (frontend)", "Service cible", "Port"],
        ["/api/chat, /api/llm", "Chatbot-Service", "8001"],
        ["/api/academic/*", "Academic-Service", "8002"],
        ["/uploads/*", "Fichiers statiques", "8002"],
    ], "Regles de routage du proxy de developpement", col_widths=[3.4, 3.0, 1.2])
    el.append(para(
        "Les services communiquent egalement entre eux : le Chatbot-Service interroge "
        "l'Academic-Service en HTTP (client httpx asynchrone) pour recuperer, par exemple, les "
        "dernieres annonces a presenter dans une reponse conversationnelle. Un cache a duree de vie "
        "limitee evite de surcharger le service appele."))
    el.append(alert(
        "En production, le proxy de developpement est remplace par un <b>reverse proxy nginx</b> qui "
        "sert le frontend statique et redirige les appels d'API vers les services, tout en assurant "
        "la terminaison TLS (HTTPS).", "info"))

    el.append(section("Le modele asynchrone et la norme ASGI"))
    el.append(para(
        "Les serveurs Python traditionnels reposent sur la norme <b>WSGI</b> (Web Server Gateway "
        "Interface), synchrone : chaque requete monopolise un fil d'execution (thread) pendant toute "
        "sa duree, y compris lors des attentes d'entree-sortie (acces a la base, appel reseau). "
        "FastAPI s'appuie au contraire sur la norme <b>ASGI</b> (Asynchronous Server Gateway "
        "Interface), qui exploite la programmation asynchrone (async/await). Pendant qu'une requete "
        "attend une reponse de la base de donnees, le serveur peut traiter d'autres requetes, ce qui "
        "ameliore considerablement le debit sous charge."))
    el.append(para(
        "Concretement, lorsqu'un point d'entree declare <i>async def</i> et utilise <i>await</i> pour "
        "ses operations d'entree-sortie, le serveur Uvicorn n'est jamais bloque inutilement. Cette "
        "propriete est essentielle pour un assistant conversationnel susceptible de recevoir de "
        "nombreuses requetes simultanees, dont certaines impliquent des appels reseau vers un service "
        "d'inference distant."))
    el += table([
        ["Aspect", "WSGI (synchrone)", "ASGI (asynchrone) — retenu"],
        ["Concurrence", "1 thread par requete", "Boucle d'evenements non bloquante"],
        ["Operations I/O", "Bloquantes", "Liberent le thread (await)"],
        ["Debit sous charge", "Limite par les threads", "Eleve"],
        ["Adapte au temps reel", "Peu", "Oui (WebSocket, streaming)"],
    ], "Comparaison des modeles WSGI et ASGI", col_widths=[2.4, 3.4, 4.2])

    el.append(section("Patrons de conception mis en oeuvre"))
    el.append(para(
        "La realisation s'appuie sur plusieurs patrons de conception (design patterns) eprouves qui "
        "structurent le code et favorisent sa maintenabilite."))
    el += table([
        ["Patron", "Application dans le projet"],
        ["Injection de dependances", "FastAPI injecte la session de base et l'utilisateur courant via Depends()"],
        ["Repository / DAO", "Acces aux donnees encapsule par l'ORM SQLAlchemy"],
        ["DTO (Data Transfer Object)", "Schemas Pydantic separant le modele interne de l'API publique"],
        ["Singleton", "Classifieur NLP et memoire conversationnelle charges une seule fois"],
        ["Strategy", "Selection dynamique du fournisseur d'IA (Groq, HuggingFace, TF-IDF)"],
        ["Facade", "Service orchestrateur (LLMService) masquant la complexite de la cascade"],
        ["Observer / reactif", "Signals Angular propageant les changements d'etat a l'interface"],
    ], "Patrons de conception utilises", col_widths=[2.6, 7.4])

    el.append(section("Cycle de vie complet d'une requete"))
    el.append(para(
        "Pour synthetiser l'interaction des couches, suivons le parcours complet d'une requete, du "
        "clic de l'utilisateur a l'affichage de la reponse. Ce cheminement traverse l'ensemble des "
        "composants decrits precedemment."))
    el += numbered([
        "L'utilisateur saisit un message ; le composant Angular capte l'evenement.",
        "Le service Angular emet une requete HTTP POST via HttpClient (un Observable RxJS).",
        "L'intercepteur ajoute eventuellement le jeton d'authentification.",
        "Le proxy (ou nginx en production) route la requete vers le service concerne.",
        "Uvicorn recoit la requete et la transmet a l'application FastAPI.",
        "Le routeur resout le point d'entree et injecte ses dependances (session, utilisateur).",
        "Pydantic valide le corps de la requete ; une entree invalide est rejetee (422).",
        "La logique metier s'execute : NLP, RAG, ou acces au referentiel selon le cas.",
        "Les donnees sont lues ou ecrites via l'ORM (MySQL) ou le pilote (MongoDB).",
        "FastAPI serialise la reponse en JSON et la renvoie avec le code de statut adapte.",
        "Angular resout l'Observable, met a jour l'etat (signal) et reaffiche l'interface.",
    ])
    el += figure_mermaid(r'''flowchart LR
  U["Utilisateur"] --> NG["Angular"]
  NG --> PX["Proxy"]
  PX --> FA["FastAPI"]
  FA --> VAL["Validation Pydantic"]
  VAL --> BIZ["Logique metier"]
  BIZ --> DB[("Base de donnees")]
  DB --> BIZ
  BIZ --> JSON["Reponse JSON"]
  JSON --> NG
  NG --> U
''', "Cycle de vie d'une requete a travers les couches", max_h=6.5*cm)
    el.append(para(
        "Sur l'ensemble de ce parcours, mesure aux alentours de deux cents millisecondes en mode "
        "classique, la majeure partie du temps est consacree au transit reseau, le traitement "
        "applicatif proprement dit restant tres rapide."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch6():
    el = chapter("Conception et Realisation des Bases de Donnees")
    el.append(para(
        "La plateforme adopte une strategie de <b>persistance polyglotte</b> : une base relationnelle "
        "MySQL pour les donnees structurees et fortement relationnelles, et une base NoSQL MongoDB "
        "pour les donnees semi-structurees et volatiles. Ce chapitre presente la modelisation "
        "conceptuelle, logique et physique de la base relationnelle, le dictionnaire de donnees, puis "
        "les collections MongoDB."))

    el.append(section("Justification de la persistance polyglotte"))
    el.append(para(
        "Les donnees academiques (departements, filieres, modules, professeurs, etudiants, notes) "
        "presentent de nombreuses relations et des contraintes d'integrite fortes : elles sont donc "
        "ideales pour un modele relationnel normalise. A l'inverse, les conversations et les sessions "
        "ont une structure variable, un volume croissant et un besoin de souplesse : un stockage "
        "documentaire NoSQL leur convient mieux. Combiner les deux permet de tirer parti des forces "
        "de chaque paradigme."))

    el += figure_mermaid(r'''flowchart LR
  APP["Plateforme FSBM"] --> SQL[("MySQL<br/>donnees structurees<br/>academiques")]
  APP --> MGO[("MongoDB<br/>conversations<br/>et analytics")]
  SQL --> S1["Integrite forte<br/>relations, ACID"]
  MGO --> M1["Flexibilite<br/>volume, evolutivite"]
''', "Persistance polyglotte : repartition des donnees", max_h=6.5*cm)

    el.append(section("Modele conceptuel de donnees (MCD)"))
    el.append(para(
        "Le modele conceptuel decrit les entites du domaine et leurs associations, independamment de "
        "toute implementation. Le diagramme entite-association suivant en presente le coeur."))
    el += figure_mermaid(r'''erDiagram
  DEPARTEMENT ||--o{ FILIERE : "contient"
  DEPARTEMENT ||--o{ PROFESSEUR : "emploie"
  FILIERE ||--o{ MODULE : "compose"
  FILIERE ||--o{ ETUDIANT : "inscrit"
  MODULE }o--o{ PROFESSEUR : "enseigne"
  ETUDIANT ||--o{ NOTE : "obtient"
  MODULE ||--o{ NOTE : "porte sur"
  FILIERE ||--o{ EMPLOI : "planifie"
  MODULE ||--o{ EXAMEN : "evalue"
  UTILISATEUR ||--o{ AVIS : "modere"
  DEPARTEMENT {
    bigint id PK
    string code
    string nom
    string logo_url
  }
  FILIERE {
    bigint id PK
    string code
    string nom
    string type
    int capacite
  }
  MODULE {
    bigint id PK
    string code
    string nom
    int semestre
    int credits
  }
  ETUDIANT {
    bigint id PK
    string cne
    string nom
    string genre
  }
''', "Modele conceptuel de donnees (diagramme entite-association)", max_h=16*cm)

    el.append(section("Modele logique de donnees (MLD)"))
    el.append(para(
        "Le passage au modele logique traduit les entites en relations (tables) et les associations "
        "en cles etrangeres. Les associations de type <i>plusieurs-a-plusieurs</i>, comme "
        "<i>enseigne</i> entre modules et professeurs, donnent lieu a une table d'association "
        "(<i>module_teachers</i>). Le schema relationnel comprend <b>dix-sept tables</b>, dont les "
        "principales sont listees ci-dessous (cles primaires soulignees, cles etrangeres en italique)."))
    el += table([
        ["Table", "Colonnes principales (PK, FK)"],
        ["departments", "id (PK), code, name, head_name, logo_url"],
        ["filieres", "id (PK), code, name, type, department_id (FK), capacity, logo_url"],
        ["modules", "id (PK), code, name, filiere_id (FK), semester, credits"],
        ["professors", "id (PK), matricule, last_name, grade, department_id (FK), photo_url"],
        ["module_teachers", "id (PK), module_id (FK), professor_id (FK), role"],
        ["students", "id (PK), cne, last_name, gender, filiere_id (FK), annee_etude"],
        ["grades", "id (PK), student_id (FK), module_id (FK), note_finale, mention"],
        ["schedules", "id (PK), filiere_id (FK), module_id (FK), professor_id (FK), salle"],
        ["exams", "id (PK), module_id (FK), filiere_id (FK), exam_date, salle"],
        ["announcements", "id (PK), title, type, target_filiere (FK), attachment_url"],
        ["events", "id (PK), title, event_type, start_date, attachment_url"],
        ["clubs", "id (PK), name, category, members_count, logo_url"],
        ["users", "id (PK), email, password_hash, role, student_id (FK), professor_id (FK)"],
        ["conversations", "id (PK), session_id, user_message, bot_response, intent_detected"],
        ["feedbacks", "id (PK), conversation_id (FK), note, is_helpful"],
        ["reviews", "id (PK), target_type, target_id, rating, status, admin_response"],
        ["faq_items", "id (PK), category_id (FK), intent_tag, question, answer"],
    ], "Modele logique : tables du schema relationnel et cles", col_widths=[2.4, 7.6], font=8.2)

    el.append(section("Modele physique et dictionnaire de donnees (MPD)"))
    el.append(para(
        "Le modele physique precise les types SQL, les contraintes et les index reellement "
        "implementes sous MySQL 8 (moteur InnoDB, jeu de caracteres utf8mb4 pour le support de "
        "l'arabe). A titre d'illustration, le dictionnaire de la table <i>filieres</i> est detaille "
        "ci-dessous."))
    el += table([
        ["Colonne", "Type", "Contrainte", "Description"],
        ["id", "BIGINT", "PK, AUTO_INCREMENT", "Identifiant unique"],
        ["code", "VARCHAR(20)", "UNIQUE, NOT NULL", "Code de la filiere (ex. SMI, DI)"],
        ["name", "VARCHAR(200)", "NOT NULL", "Intitule complet"],
        ["type", "ENUM", "NOT NULL", "LICENCE, MASTER, MASTER_RECHERCHE..."],
        ["department_id", "BIGINT", "FK -> departments", "Departement de rattachement"],
        ["capacity", "INT", "DEFAULT 100", "Capacite d'accueil"],
        ["logo_url", "VARCHAR(255)", "NULL", "Logo de la filiere (Phase 2)"],
        ["is_active", "BOOLEAN", "DEFAULT TRUE", "Filiere ouverte ou non"],
        ["created_at", "TIMESTAMP", "DEFAULT NOW()", "Date de creation"],
    ], "Dictionnaire de donnees de la table filieres", col_widths=[2.2, 1.8, 2.4, 3.6], font=8.4)
    el.append(para(
        "Des <b>index</b> ont ete crees sur les colonnes frequemment filtrees (type, department_id) "
        "et un index <b>FULLTEXT</b> a ete pose sur les questions et reponses de la FAQ afin "
        "d'accelerer la recherche textuelle. L'integrite referentielle est garantie par des "
        "contraintes de cle etrangere avec des politiques adaptees (CASCADE, RESTRICT, SET NULL)."))

    el.append(section("Normalisation du schema relationnel"))
    el.append(para(
        "La normalisation est un processus de structuration des tables visant a reduire la redondance "
        "et a prevenir les anomalies de mise a jour. Notre schema respecte la <b>troisieme forme "
        "normale (3NF)</b>, atteinte par application successive des trois premieres formes."))
    el += table([
        ["Forme normale", "Regle", "Application dans le projet"],
        ["1NF", "Valeurs atomiques, pas de groupes repetitifs", "Chaque colonne contient une seule valeur"],
        ["2NF", "1NF + dependance totale a la cle", "Aucun attribut ne depend d'une partie de cle composite"],
        ["3NF", "2NF + pas de dependance transitive", "Le nom du departement n'est pas duplique dans filieres"],
    ], "Formes normales respectees par le schema", col_widths=[2.0, 4.0, 4.0])
    el.append(para(
        "Par exemple, plutot que de repeter le nom du departement dans chaque filiere (source de "
        "redondance et d'incoherence), la table <i>filieres</i> ne stocke qu'une cle etrangere "
        "<i>department_id</i> referencant la table <i>departments</i>. Cette decomposition elimine la "
        "dependance transitive caracteristique d'un schema non normalise."))

    el.append(section("Index, contraintes et integrite referentielle"))
    el.append(para(
        "Les performances de lecture reposent sur une indexation judicieuse. Outre les index "
        "implicites sur les cles primaires et les colonnes uniques, des index secondaires accelerent "
        "les filtres frequents, et un index FULLTEXT optimise la recherche dans la FAQ."))
    el += table([
        ["Type d'index", "Colonnes concernees", "Objectif"],
        ["Primaire", "id (toutes les tables)", "Acces direct par identifiant"],
        ["Unique", "code, email, matricule, cne", "Garantir l'unicite metier"],
        ["Secondaire", "type, department_id, filiere_id", "Accelerer les filtres"],
        ["FULLTEXT", "question, answer (faq_items)", "Recherche textuelle rapide"],
    ], "Strategie d'indexation de la base relationnelle", col_widths=[2.0, 4.2, 3.8])
    el.append(para(
        "L'<b>integrite referentielle</b> est garantie par des contraintes de cle etrangere assorties "
        "de politiques adaptees : <i>ON DELETE CASCADE</i> pour les donnees dependantes (les modules "
        "d'une filiere supprimee), <i>RESTRICT</i> pour empecher la suppression d'une entite encore "
        "referencee (un departement rattache a des filieres), et <i>SET NULL</i> pour conserver une "
        "donnee tout en rompant un lien optionnel."))

    el.append(section("Transactions et coherence"))
    el.append(para(
        "Le moteur InnoDB de MySQL assure les proprietes <b>ACID</b> (Atomicite, Coherence, "
        "Isolation, Durabilite). Les operations d'ecriture composees sont encapsulees dans des "
        "transactions : en cas d'erreur, un retour arriere (rollback) preserve la coherence de la "
        "base. L'ORM SQLAlchemy gere ces transactions de maniere transparente, validant (commit) ou "
        "annulant l'ensemble des modifications d'une session selon le resultat."))

    el.append(section("La base NoSQL MongoDB"))
    el.append(para(
        "MongoDB stocke les donnees conversationnelles et analytiques sous forme de documents JSON "
        "(BSON). Six collections principales structurent ces donnees, avec une validation de schema "
        "(JSON Schema) garantissant un minimum de coherence."))
    el += table([
        ["Collection", "Contenu", "Usage"],
        ["sessions", "Sessions conversationnelles et historique", "Memoire multi-tours du chatbot"],
        ["conversation_logs", "Journal detaille des echanges", "Tracabilite et amelioration"],
        ["nlp_analytics", "Statistiques d'intentions et de langues", "Tableau de bord analytique"],
        ["feedback", "Retours et notes des utilisateurs", "Mesure de satisfaction"],
        ["unanswered", "Questions a faible confiance", "Enrichissement du dataset"],
        ["audit", "Journal des actions d'administration", "Securite et tracabilite"],
    ], "Collections MongoDB de la plateforme", col_widths=[2.2, 4.0, 3.8])
    el.append(para("Exemple de document de la collection <i>sessions</i> :"))
    el += code(
        "{\n"
        "  \"session_id\": \"sess_abc123\",\n"
        "  \"created_at\": \"2026-05-28T13:24:35Z\",\n"
        "  \"language\": \"darija\",\n"
        "  \"message_count\": 4,\n"
        "  \"messages\": [\n"
        "    { \"sender\": \"user\", \"text\": \"shno hia les filieres ?\" },\n"
        "    { \"sender\": \"bot\", \"text\": \"...\", \"intent\": \"filieres\" }\n"
        "  ],\n"
        "  \"last_intent\": \"filieres\"\n"
        "}")
    el.append(section("Comparaison des deux paradigmes"))
    el.append(para(
        "Le tableau suivant resume les caracteristiques complementaires des deux moteurs de stockage "
        "et justifie leur usage respectif dans la plateforme."))
    el += table([
        ["Critere", "MySQL (relationnel)", "MongoDB (documentaire)"],
        ["Structure", "Tables, schema rigide", "Documents, schema flexible"],
        ["Relations", "Cles etrangeres, jointures", "Imbrication / references"],
        ["Integrite", "Forte (contraintes, ACID)", "Souple (validation JSON Schema)"],
        ["Cas d'usage ici", "Referentiel academique", "Conversations, analytics"],
        ["Montee en charge", "Verticale, replication", "Horizontale (sharding)"],
        ["Langage de requete", "SQL", "Requetes documentaires"],
    ], "Comparaison des paradigmes relationnel et documentaire", col_widths=[2.2, 3.9, 3.9])
    el.append(alert(
        "Cette complementarite MySQL / MongoDB illustre un principe d'architecture moderne : choisir "
        "le bon outil de stockage selon la nature de la donnee, plutot que de forcer toutes les "
        "donnees dans un modele unique.", "tip"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch7():
    el = chapter("Intelligence Artificielle et Traitement du Langage")
    el.append(para(
        "Le coeur intelligent de la plateforme repose sur le traitement automatique du langage "
        "naturel (TALN) et sur l'integration de grands modeles de langage. Ce chapitre detaille la "
        "chaine de traitement linguistique, le classifieur TF-IDF, la detection de langue, la "
        "memoire conversationnelle, puis l'architecture RAG et la cascade de repli qui garantissent "
        "fiabilite et disponibilite."))

    el.append(section("Chaine de traitement du langage naturel"))
    el.append(para(
        "Comprendre un message en langage naturel suppose plusieurs etapes successives : "
        "normalisation du texte, decoupage en unites (tokenisation), suppression des mots vides, "
        "puis vectorisation pour rendre le texte exploitable par des algorithmes. La figure suivante "
        "presente cette chaine."))
    el += figure_mermaid(r'''flowchart LR
  A["Message brut"] --> B["Normalisation<br/>(minuscules, accents)"]
  B --> C["Tokenisation"]
  C --> D["Suppression mots vides"]
  D --> E["Vectorisation TF-IDF"]
  E --> F["Similarite cosinus"]
  F --> G["Intention + confiance"]
''', "Chaine de traitement du langage naturel", max_h=7*cm)

    el.append(section("Tokenisation et pretraitement"))
    el.append(para(
        "Avant toute analyse, le texte subit un pretraitement. La <b>normalisation</b> ramene le "
        "texte en minuscules et harmonise les accents, afin que <i>Filiere</i>, <i>filiere</i> et "
        "<i>FILIERE</i> soient traites de maniere identique. La <b>tokenisation</b> decoupe ensuite "
        "la phrase en unites lexicales (tokens). Enfin, les <b>mots vides</b> (stop words) tres "
        "frequents et peu informatifs — articles, prepositions, pronoms — peuvent etre filtres pour "
        "concentrer l'analyse sur les termes porteurs de sens."))
    el.append(para(
        "Le caractere multilingue impose un pretraitement adapte a chaque langue. En darija "
        "translitteree, par exemple, les chiffres 3, 7 et 9 representent des phonemes arabes "
        "specifiques et constituent des indices precieux qu'il convient de preserver plutot que de "
        "supprimer."))

    el.append(section("N-grammes et robustesse aux reformulations"))
    el.append(para(
        "Pour capturer le contexte local et mieux resister aux reformulations, la vectorisation "
        "exploite des <b>n-grammes</b> : des sequences de un a deux mots consecutifs. Ainsi, "
        "l'expression <i>emploi du temps</i> est representee non seulement par ses mots isoles "
        "(unigrammes) mais aussi par les bigrammes <i>emploi du</i> et <i>du temps</i>, ce qui "
        "renforce la discrimination entre intentions proches et accroit la tolerance aux variations "
        "de formulation."))

    el.append(section("Vectorisation TF-IDF"))
    el.append(para(
        "La technique <b>TF-IDF</b> (Term Frequency-Inverse Document Frequency) transforme un texte "
        "en vecteur numerique. Elle accorde un poids eleve aux termes frequents dans un document mais "
        "rares dans l'ensemble du corpus, c'est-a-dire aux termes les plus discriminants. Le poids "
        "d'un terme t dans un document d est defini par :"))
    el.append(quote(
        "tf-idf(t, d) = tf(t, d) x idf(t) , avec idf(t) = log( N / df(t) )"))
    el.append(para(
        "ou tf(t, d) est la frequence du terme t dans d, N le nombre total de documents (patterns) et "
        "df(t) le nombre de documents contenant t. Chaque intention du chatbot est associee a un "
        "ensemble de formulations types (patterns) ; la question de l'utilisateur est vectorisee dans "
        "le meme espace, puis comparee a tous les patterns."))

    el.append(section("Similarite cosinus et reconnaissance d'intention"))
    el.append(para(
        "La proximite entre la question et chaque pattern est mesuree par la <b>similarite cosinus</b>, "
        "qui evalue l'angle entre deux vecteurs independamment de leur norme :"))
    el.append(quote(
        "cos(theta) = (A . B) / ( ||A|| x ||B|| )"))
    el.append(para(
        "Une valeur proche de 1 indique une forte similarite, une valeur proche de 0 une absence de "
        "rapport. L'intention retenue est celle dont un pattern maximise cette similarite. Si le "
        "meilleur score reste inferieur a un seuil de confiance, le systeme demande une reformulation "
        "plutot que de risquer une reponse erronee."))
    el += code(
        "user_vec = vectorizer.transform([question.lower()])\n"
        "similarites = cosine_similarity(user_vec, pattern_matrix)[0]\n"
        "best = similarites.argmax()\n"
        "intention, confiance = intents[best], similarites[best]\n"
        "if confiance < SEUIL:\n"
        "    return reponse_par_defaut_avec_suggestions()")

    el.append(subsection("Illustration numerique"))
    el.append(para(
        "Considerons un mini-corpus de trois formulations et le terme <i>inscription</i>. Supposons "
        "qu'il apparaisse une fois dans un document de dix mots (tf = 0,1) et dans un seul des trois "
        "documents (df = 1, N = 3). Son idf vaut log(3/1) &asymp; 1,10, et son poids tf-idf "
        "&asymp; 0,11. A l'inverse, un mot tres frequent present dans les trois documents a un idf nul "
        "et donc un poids tf-idf nul : il n'apporte aucune capacite de discrimination. Cet exemple "
        "illustre le principe central de la methode : <b>valoriser les termes rares et discriminants</b>."))

    el.append(subsection("TF-IDF face aux embeddings neuronaux"))
    el.append(para(
        "Une alternative au TF-IDF consiste a utiliser des <b>embeddings</b> neuronaux, qui capturent "
        "la similarite semantique au-dela de la correspondance lexicale. Nous avons neanmoins retenu "
        "le TF-IDF pour le coeur du moteur classique, pour des raisons d'efficacite, de transparence "
        "et d'autonomie ; les capacites semantiques sont apportees, lorsque necessaire, par le mode "
        "avance fonde sur le grand modele de langage."))
    el += table([
        ["Critere", "TF-IDF (retenu)", "Embeddings neuronaux"],
        ["Comprehension semantique", "Lexicale", "Semantique profonde"],
        ["Ressources requises", "Tres faibles", "Elevees (modele, GPU)"],
        ["Latence", "~30 ms", "Variable"],
        ["Explicabilite", "Elevee", "Faible (boite noire)"],
        ["Autonomie (hors ligne)", "Totale", "Limitee"],
    ], "Comparaison TF-IDF / embeddings neuronaux", col_widths=[2.6, 3.4, 4.0])

    el.append(section("Detection de langue et approche multilingue"))
    el.append(para(
        "La plateforme prend en charge trois langues : le francais, l'anglais et la darija marocaine. "
        "Un detecteur hybride identifie la langue par trois indices complementaires : la presence de "
        "caracteres arabes, des marqueurs numeriques propres a la darija en graphie latine (les "
        "chiffres 3, 7, 9 substituant des phonemes arabes), et un comptage de mots-cles lexicaux. "
        "Pour chaque langue, un modele TF-IDF distinct est entraine, garantissant une comprehension "
        "fine de chaque registre."))
    el += table([
        ["Langue", "Patterns", "Indices de detection"],
        ["Francais", "188", "Mots-cles lexicaux francais"],
        ["Anglais", "186", "Mots-cles lexicaux anglais"],
        ["Darija (latin + arabe)", "461", "Caracteres arabes, chiffres 3/7/9, lexique darija"],
        ["Total", "835", "28 intentions reconnues"],
    ], "Repartition du jeu de donnees NLP par langue", col_widths=[3.0, 1.6, 5.4])

    def draw_lang(fig):
        ax = fig.add_subplot(111)
        langs = ["Francais", "Anglais", "Darija"]; vals = [188, 186, 461]
        bars = ax.bar(langs, vals, color=["#1C3F6E", "#2d5a9e", "#FF6B35"])
        ax.set_ylabel("Nombre de patterns"); ax.set_title("Patterns d'entrainement par langue", fontsize=10)
        for b, v in zip(bars, vals):
            ax.text(b.get_x()+b.get_width()/2, v+8, str(v), ha="center", fontweight="bold", fontsize=9)
    el += chart(draw_lang, "Volume de donnees d'entrainement par langue", h_cm=7)

    el.append(para(
        "Architecturalement, trois modeles TF-IDF independants sont entraines en parallele, un par "
        "langue, et la detection de langue aiguille la requete vers le modele approprie."))
    el += figure_mermaid(r'''flowchart TB
  Q["Message utilisateur"] --> D{"Detection de langue"}
  D -- fr --> MF["Modele TF-IDF Francais<br/>(188 patterns)"]
  D -- en --> ME["Modele TF-IDF Anglais<br/>(186 patterns)"]
  D -- darija --> MD["Modele TF-IDF Darija<br/>(461 patterns)"]
  MF --> R["Intention + confiance"]
  ME --> R
  MD --> R
''', "Architecture multilingue a trois modeles TF-IDF paralleles", max_h=8.5*cm)

    el.append(section("Memoire conversationnelle et personnalisation"))
    el.append(para(
        "Pour gerer les echanges multi-tours, le systeme conserve une memoire de session (jusqu'a "
        "vingt tours) permettant de tenir compte du contexte des messages precedents. Par ailleurs, "
        "un module de <b>personnalisation</b> detecte le genre et eventuellement le prenom de "
        "l'utilisateur afin d'adapter les formules de politesse, particulierement importantes en "
        "darija (par exemple <i>khoya</i>, <i>khti</i> ou <i>lalla</i> selon le genre). Cette "
        "attention au registre social renforce le caractere naturel et respectueux de l'assistant."))

    el.append(section("Architecture RAG et integration de LLaMA 3"))
    el.append(para(
        "Le mode avance de l'assistant exploite un grand modele de langage, <b>LLaMA 3.3-70B</b>, "
        "accessible via l'API <b>Groq</b> reputee pour sa tres faible latence. Pour eviter les "
        "hallucinations — risque majeur des modeles generatifs — nous employons l'approche <b>RAG "
        "(Retrieval-Augmented Generation)</b> : avant d'interroger le modele, le systeme recupere les "
        "contextes les plus pertinents (reutilisant le classifieur TF-IDF comme moteur de "
        "recuperation) et les injecte dans l'invite. Le modele <i>reformule</i> ainsi des "
        "informations verifiees plutot que d'inventer."))
    el += figure_mermaid(r'''flowchart LR
  Q["Question utilisateur"] --> RET["Recuperation TF-IDF<br/>(top-k contextes)"]
  RET --> PR["Construction de l'invite<br/>(systeme + contextes + historique)"]
  PR --> LLM["LLaMA 3.3-70B<br/>(via Groq)"]
  LLM --> REP["Reponse naturelle<br/>et fiable"]
  KB[("Base de connaissances<br/>FSBM")] --> RET
''', "Architecture RAG : recuperation puis generation encadree", max_h=8*cm)

    el.append(section("Base de connaissances institutionnelle reelle"))
    el.append(para(
        "Conformement a l'exigence d'ancrage dans des donnees authentiques, la base de connaissances "
        "du chatbot a ete alimentee a partir des <b>donnees reelles de la FSBM</b> : les six "
        "departements et leurs chefs, les filieres reelles et leurs responsables, le nom du doyen "
        "(Pr. Abdeslam EL BOUARI), les coordonnees officielles, ainsi que des questions-reponses "
        "fondees sur le site institutionnel fsbm.ma. Ces connaissances, regroupees dans un fichier "
        "structure (<i>fsbm_knowledge.json</i>) et dans la table des FAQ, constituent la couche "
        "documentaire sur laquelle s'appuie la recuperation RAG."))
    el.append(para(
        "Ainsi, lorsqu'un etudiant interroge l'assistant sur sa filiere ou son departement, la "
        "reponse generee se fonde sur des informations verifiees et a jour, et non sur des donnees "
        "fictives. Cette demarche renforce la credibilite de l'assistant et son exploitabilite "
        "reelle par la faculte."))
    el.append(alert(
        "Toutes les donnees presentees comme reelles proviennent de sources verifiables (site "
        "officiel fsbm.ma, Google Scholar pour le profil de l'encadrant). Aucune donnee reelle n'a "
        "ete inventee, conformement a la rigueur scientifique exigee.", "key"))

    el.append(section("Ingenierie de l'invite et limitation des hallucinations"))
    el.append(para(
        "La qualite des reponses d'un grand modele de langage depend etroitement de la qualite de "
        "l'invite (prompt) qui lui est soumise. Notre invite est structuree en trois blocs : un "
        "<b>message systeme</b> qui fixe le role (assistant officiel de la FSBM), la langue et les "
        "regles de conduite (ne pas inventer, rester dans le perimetre academique) ; un bloc de "
        "<b>contextes</b> issus de la recuperation RAG ; et l'<b>historique</b> recent de la "
        "conversation suivi de la question courante."))
    el.append(para(
        "Cette structuration encadre fortement le modele : en lui imposant de s'appuyer "
        "exclusivement sur les contextes fournis et en l'autorisant a declarer son ignorance, on "
        "reduit considerablement le risque d'hallucination. Le parametre de <i>temperature</i>, fixe "
        "a une valeur moderee, limite par ailleurs la creativite excessive au profit de la "
        "fiabilite."))
    el += table([
        ["Bloc de l'invite", "Role"],
        ["Message systeme", "Identite, langue, regles, perimetre"],
        ["Contextes (RAG)", "Connaissances verifiees a reformuler"],
        ["Historique", "Continuite conversationnelle"],
        ["Question", "Besoin courant de l'utilisateur"],
    ], "Structure de l'invite envoyee au modele de langage", col_widths=[2.6, 7.4])

    el.append(section("Cascade de repli et haute disponibilite"))
    el.append(para(
        "La disponibilite du service ne doit jamais dependre d'un fournisseur externe unique. Le "
        "systeme implemente donc une <b>cascade de repli</b> a trois niveaux : il tente d'abord Groq "
        "(LLaMA 3), puis, en cas d'indisponibilite, un modele de secours via HuggingFace, et enfin, "
        "en dernier recours, le moteur TF-IDF local. Ce dernier etant totalement autonome, le service "
        "reste fonctionnel meme sans connexion aux services d'IA externes, garantissant une "
        "disponibilite de 100 %."))
    el += table([
        ["Niveau", "Fournisseur", "Latence typique", "Disponibilite"],
        ["1 (principal)", "Groq — LLaMA 3.3-70B", "~150-250 ms", "Cloud"],
        ["2 (repli)", "HuggingFace — modele 8B", "~1-3 s", "Cloud"],
        ["3 (local)", "TF-IDF + base locale", "~30 ms", "Toujours disponible"],
    ], "Cascade de repli garantissant la continuite de service", col_widths=[1.8, 3.4, 2.4, 2.4])
    el.append(alert(
        "Ce mecanisme illustre un principe d'ingenierie de la fiabilite : <b>degradation gracieuse</b>. "
        "En cas de defaillance, le systeme reduit la richesse de ses reponses mais ne s'interrompt "
        "jamais.", "key"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch8():
    el = chapter("Securite de la Plateforme")
    el.append(para(
        "La securite est une exigence transversale qui conditionne la confiance accordee a la "
        "plateforme. Ce chapitre presente les mecanismes d'authentification et d'autorisation, la "
        "protection des donnees sensibles, la prevention des vulnerabilites web courantes, et "
        "positionne nos mesures par rapport au referentiel OWASP."))

    el.append(section("Authentification et autorisation"))
    el.append(para(
        "Il convient de distinguer l'<b>authentification</b> (verifier l'identite : qui es-tu ?) de "
        "l'<b>autorisation</b> (verifier les droits : as-tu la permission ?). L'espace "
        "d'administration de la plateforme repose sur une authentification par identifiants (email et "
        "mot de passe) et une autorisation fondee sur les roles (RBAC)."))
    el.append(subsection("Hachage des mots de passe avec bcrypt"))
    el.append(para(
        "Les mots de passe ne sont jamais stockes en clair. Ils sont haches avec l'algorithme "
        "<b>bcrypt</b>, concu pour etre volontairement lent (facteur de coût 12) et integrant un sel "
        "aleatoire, ce qui rend les attaques par force brute et par tables precalculees (rainbow "
        "tables) impraticables. La verification compare le hash stocke au hash du mot de passe saisi, "
        "sans jamais pouvoir reconstituer l'original."))
    el += code(
        "def hash_password(plain: str) -> str:\n"
        "    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()\n\n"
        "def verify_password(plain: str, hashed: str) -> bool:\n"
        "    return bcrypt.checkpw(plain.encode(), hashed.encode())")

    el.append(subsection("Jetons JWT"))
    el.append(para(
        "Apres authentification reussie, le serveur emet un <b>jeton JWT</b> (JSON Web Token) signe, "
        "contenant l'identifiant et le role de l'utilisateur ainsi qu'une date d'expiration. Ce jeton, "
        "stocke cote client, est joint a chaque requete protegee via l'en-tete Authorization. Le "
        "serveur verifie sa signature et sa validite sans avoir a conserver d'etat de session, ce qui "
        "rend l'architecture <i>stateless</i> et donc aisement scalable."))
    el += figure_mermaid(r'''sequenceDiagram
  actor U as Administrateur
  participant F as Frontend
  participant S as Academic-Service
  U->>F: email + mot de passe
  F->>S: POST /api/auth/login
  S->>S: verify (bcrypt) + signer JWT
  S-->>F: JWT (exp 12h)
  Note over F: stockage local du jeton
  U->>F: action protegee
  F->>S: requete + "Authorization: Bearer JWT"
  S->>S: verifier signature + role
  S-->>F: 200 OK / 401 / 403
''', "Flux d'authentification par jeton JWT", max_h=11*cm)

    el.append(section("Controle d'acces par roles (RBAC)"))
    el.append(para(
        "Chaque utilisateur possede un role determinant ses permissions. Le modele prevoit quatre "
        "roles ; les operations d'administration sont reservees aux roles ADMIN et SCOLARITE, "
        "verifies par une dependance FastAPI commune a toutes les routes protegees."))
    el += table([
        ["Role", "Permissions"],
        ["ETUDIANT", "Consultation, chatbot, depot d'avis"],
        ["PROFESSEUR", "Consultation, enrichissement futur des donnees pedagogiques"],
        ["SCOLARITE", "Gestion des contenus et des donnees academiques"],
        ["ADMIN", "Toutes permissions, gestion des comptes et moderation"],
    ], "Roles et permissions (RBAC)", col_widths=[2.0, 8.0])

    el.append(section("Prevention des vulnerabilites web"))
    el.append(subsection("Injection SQL"))
    el.append(para(
        "Toutes les requetes vers la base relationnelle passent par l'ORM SQLAlchemy avec des "
        "requetes <b>parametrees</b> : les valeurs fournies par l'utilisateur ne sont jamais "
        "concatenees au texte SQL, ce qui neutralise les tentatives d'injection. Aucune requete "
        "construite par concatenation de chaines n'existe dans le code."))
    el.append(subsection("Cross-Site Scripting (XSS)"))
    el.append(para(
        "Angular echappe automatiquement le contenu interpole dans ses gabarits : une saisie "
        "malveillante contenant du code est affichee comme du texte inerte et non executee. Les "
        "champs libres (avis, messages) sont ainsi neutralises a l'affichage."))
    el.append(subsection("Validation des entrees avec Pydantic"))
    el.append(para(
        "Cote backend, chaque requete est validee par un schema Pydantic qui controle les types, les "
        "longueurs, les formats et les bornes des donnees. Une entree non conforme est rejetee avec "
        "un code 422 avant meme d'atteindre la logique metier, constituant une premiere ligne de "
        "defense robuste."))
    el.append(subsection("CORS et gestion des secrets"))
    el.append(para(
        "Le partage de ressources entre origines (CORS) est restreint a une liste blanche d'origines "
        "autorisees. Les secrets (mot de passe de base de donnees, cle de signature JWT, cle d'API "
        "Groq) ne figurent jamais dans le code : ils sont charges depuis un fichier d'environnement "
        "exclu du depot de code."))

    el.append(section("Positionnement OWASP Top 10"))
    el.append(para(
        "Le referentiel OWASP recense les dix risques de securite applicative les plus critiques. Le "
        "tableau suivant resume notre couverture."))
    el += table([
        ["Risque OWASP", "Mesure mise en oeuvre"],
        ["A01 Controle d'acces defaillant", "RBAC + verification systematique du role"],
        ["A02 Defaillances cryptographiques", "bcrypt, HTTPS en production"],
        ["A03 Injection", "Requetes parametrees (SQLAlchemy)"],
        ["A05 Mauvaise configuration", "Secrets externalises, CORS restreint"],
        ["A07 Defaillances d'authentification", "JWT signe + expiration, anti-bruteforce (perspective)"],
        ["A09 Journalisation insuffisante", "Journalisation des actions et des conversations"],
    ], "Couverture des principaux risques OWASP", col_widths=[3.4, 6.6])
    el.append(section("Defense en profondeur"))
    el.append(para(
        "La securite de la plateforme ne repose pas sur une mesure unique mais sur une superposition "
        "de barrieres complementaires, selon le principe de <b>defense en profondeur</b> : si une "
        "couche est franchie, les suivantes continuent de proteger le systeme. La figure suivante "
        "synthetise cet empilement de controles."))
    el += figure_mermaid(r'''flowchart TB
  A["Requete entrante"] --> B["1. CORS - origines autorisees"]
  B --> C["2. Authentification JWT"]
  C --> D["3. Autorisation RBAC (role)"]
  D --> E["4. Validation Pydantic"]
  E --> F["5. Requetes parametrees (anti-injection)"]
  F --> G["6. Logique metier"]
  G --> H[("Base de donnees")]
''', "Defense en profondeur : empilement des controles de securite", max_h=12*cm)

    el.append(section("Gestion des secrets"))
    el.append(para(
        "Les informations sensibles (mot de passe de la base, cle de signature des jetons, cle d'API "
        "du fournisseur d'IA) ne sont jamais inscrites dans le code source ni versionnees. Elles sont "
        "externalisees dans un fichier d'environnement (.env) exclu du depot par le fichier "
        "<i>.gitignore</i>, et chargees au demarrage par la configuration applicative. Un fichier "
        "d'exemple (.env.example) documente les variables attendues sans en divulguer les valeurs."))
    el += table([
        ["Secret", "Stockage", "Bonne pratique"],
        ["Mot de passe BDD", ".env (hors depot)", "Compte applicatif a privileges limites"],
        ["Cle JWT", ".env (hors depot)", "Chaine longue et aleatoire, rotation"],
        ["Cle API Groq", ".env (hors depot)", "Quota et revocation possibles"],
        ["Mots de passe utilisateurs", "Base (hash bcrypt)", "Jamais en clair"],
    ], "Gestion des secrets de la plateforme", col_widths=[2.6, 3.2, 4.2])

    el.append(section("Journalisation et tracabilite"))
    el.append(para(
        "La tracabilite constitue un pilier de la securite operationnelle. Les actions sensibles "
        "(connexions, operations d'administration) et les conversations sont journalisees, "
        "permettant l'analyse a posteriori, la detection d'anomalies et l'amelioration continue du "
        "service. Cette journalisation respecte le principe de minimisation : aucune donnee "
        "personnelle sensible n'est conservee sans necessite."))

    el.append(alert(
        "L'etat actuel couvre les fondamentaux de securite. Des renforcements sont prevus pour une "
        "mise en production : limitation du debit (rate limiting), HTTPS avec HSTS, et audit de "
        "securite complet (chapitre 14).", "warn"))
    return el
