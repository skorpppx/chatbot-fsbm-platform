"""PDF 1 - Architecture Globale FSBM Platform (60 pages)"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 01/10", "Architecture Globale",
           "Vue d'ensemble du systeme + Micro-services + Communication",
           accent_color=PRIMARY)

# ═══════ TOC ═══════
story.append(Paragraph("Sommaire", ST_CHAPTER))
toc = [
    ("Chapitre 1 - Qu'est-ce que la FSBM Platform ?", "3"),
    ("Chapitre 2 - Le probleme universitaire FSBM", "6"),
    ("Chapitre 3 - Objectifs du projet", "9"),
    ("Chapitre 4 - Concepts de base avant d'aller plus loin", "12"),
    ("Chapitre 5 - Architecture micro-services expliquee", "18"),
    ("Chapitre 6 - Les 6 services en detail", "23"),
    ("Chapitre 7 - Le frontend Angular (vue d'ensemble)", "29"),
    ("Chapitre 8 - Les bases de donnees (MySQL + MongoDB)", "34"),
    ("Chapitre 9 - Communication via HTTP/REST", "40"),
    ("Chapitre 10 - Les ports et leur utilite", "45"),
    ("Chapitre 11 - Workflow global d'une requete", "49"),
    ("Chapitre 12 - Choix techniques justifies", "54"),
    ("Chapitre 13 - Conclusion et lecture des autres PDFs", "59"),
]
for label, page in toc:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# ═══════ CHAPITRE 1 ═══════
story.append(Paragraph("Chapitre 1 - Qu'est-ce que la FSBM Platform ?", ST_CHAPTER))

story.append(Paragraph("1.1 Le projet en une phrase", ST_H1))
story.append(Paragraph(
    "FSBM Platform est une <b>plateforme universitaire intelligente</b> qui combine un "
    "<b>chatbot multilingue</b> (FR / EN / Darija marocaine) avec un <b>referentiel academique "
    "navigable</b> pour les etudiants de la Faculte des Sciences Ben M'Sick a Casablanca.",
    ST_BODY))

story.append(Paragraph("1.2 De quoi se compose le projet ?", ST_H1))
story.append(Paragraph(
    "Concretement, quand un etudiant ouvre la plateforme dans son navigateur, il voit :",
    ST_BODY))
features = [
    ("Un dashboard d'accueil",
     "Avec 8 cartes statistiques en temps reel (nombre d'etudiants, filieres, modules...), "
     "les dernieres annonces et les evenements a venir."),
    ("Une page Assistant IA",
     "Un chatbot capable de repondre en 3 langues, avec memoire conversationnelle, "
     "personnalisation (khoya/khti selon le genre), et option LLaMA 3 pour des reponses "
     "plus naturelles."),
    ("Des pages de navigation academique",
     "5 departements, 25 filieres (7 licences + 18 masters), 100+ modules, "
     "107 professeurs, EDT, examens, annonces, clubs..."),
    ("Un mode sombre",
     "Toggle dans la sidebar, persiste entre sessions."),
    ("Un design responsive",
     "Fonctionne sur mobile, tablette, desktop."),
]
for n, d in features:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("1.3 Qu'est-ce qu'il y a 'derriere' ce que voit l'utilisateur ?", ST_H1))
story.append(Paragraph(
    "L'utilisateur ne voit que la 'partie emergee de l'iceberg'. Derriere son ecran, "
    "il y a un systeme complexe :",
    ST_BODY))

story.append(diagram(
    "                    L'ETUDIANT VOIT CECI :\n"
    "    +--------------------------------------------------+\n"
    "    |  [Dashboard, Chat, Filieres, Modules, ...]       |\n"
    "    |  C'est ce qu'on appelle le FRONTEND              |\n"
    "    +--------------------------------------------------+\n"
    "                          |\n"
    "                          | (le navigateur fait des requetes invisibles)\n"
    "                          v\n"
    "                  MAIS DERRIERE, IL Y A :\n"
    "    +--------------------------------------------------+\n"
    "    |  BACKEND : 6 services Python qui calculent       |\n"
    "    |  - chatbot-service : NLP, IA, langue             |\n"
    "    |  - academic-service : filieres, profs, etudiants |\n"
    "    |  - student-service : auth, profils (Phase 2)     |\n"
    "    |  - review-service : feedbacks (Phase 2)          |\n"
    "    |  - notification-service : push (Phase 2)         |\n"
    "    |  - analytics-service : stats (Phase 2)           |\n"
    "    +--------------------------------------------------+\n"
    "                          |\n"
    "                          v\n"
    "    +--------------------------------------------------+\n"
    "    |  BASES DE DONNEES : ou tout est stocke           |\n"
    "    |  - MySQL : etudiants, filieres, modules          |\n"
    "    |  - MongoDB : reviews, logs, sentiments           |\n"
    "    +--------------------------------------------------+\n"
))

story.append(analogy(
    "Imagine un <b>restaurant</b>. Le client (utilisateur) voit la salle (frontend Angular), "
    "passe commande au serveur (services backend FastAPI), le serveur va en cuisine (bases "
    "de donnees MySQL/MongoDB) chercher les ingredients, le chef cuisine (logique metier), "
    "et le serveur ramene le plat (la reponse). Le client ne voit jamais la cuisine, mais elle "
    "est essentielle au fonctionnement."))

story.append(Paragraph("1.4 Pourquoi ce projet ?", ST_H1))
story.append(Paragraph(
    "Le projet est un <b>Projet de Fin d'Etudes (PFE)</b> de Licence Developpement "
    "Informatique a la FSBM. Il a 3 objectifs principaux :",
    ST_BODY))
purposes = [
    ("Resoudre un vrai probleme universitaire",
     "Les etudiants FSBM sont satures d'informations dispersees (site web, panneaux, scolarite, "
     "Facebook). Le chatbot centralise tout."),
    ("Demontrer la maitrise de technologies modernes",
     "Angular 17, FastAPI, micro-services, NLP, LLM, RAG, MySQL+MongoDB... Le projet utilise les "
     "memes outils que les vraies entreprises tech (Microsoft, Google, startups marocaines)."),
    ("Avoir un produit reellement deployable",
     "Le code n'est pas un jouet : il est conçu pour pouvoir tourner en vrai dans la FSBM, "
     "avec donnees authentiques, scripts d'installation, documentation, etc."),
]
for n, d in purposes:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))
story.append(PageBreak())

# ═══════ CHAPITRE 2 ═══════
story.append(Paragraph("Chapitre 2 - Le probleme universitaire FSBM", ST_CHAPTER))

story.append(Paragraph("2.1 Le constat", ST_H1))
story.append(Paragraph(
    "Aujourd'hui a la FSBM, quand un etudiant veut savoir une information administrative "
    "(quand sont les examens ? comment s'inscrire au master IADS ? comment obtenir une "
    "attestation ?), il doit :",
    ST_BODY))
constat = [
    "Aller sur le site officiel www.fsbm.ma (souvent incomplet ou pas a jour)",
    "Consulter la page Facebook FSBMUH2C (annonces mais pas archivees, difficiles a chercher)",
    "Aller physiquement aux panneaux d'affichage de son departement",
    "Demander a la scolarite (file d'attente de 1-2 heures en periode de pointe)",
    "Demander a un camarade plus ancien (souvent l'info la plus fiable, ironiquement)",
    "Chercher dans des groupes WhatsApp non-officiels",
]
for c in constat:
    story.append(Paragraph(f"• {c}", ST_LIST))

story.append(alert_box(
    "Resultat : <b>fragmentation</b> de l'information, perte de temps, inegalite d'acces "
    "(les etudiants bien connectes savent, les autres galerent), saturation des services "
    "humains, et un sentiment general de 'la fac est mal organisee'.",
    kind="warning", title="Le probleme central"))

story.append(Paragraph("2.2 Les 5 douleurs identifiees", ST_H1))
pains = [
    ("Fragmentation des sources",
     "Pour une question simple comme 'Quels documents pour s'inscrire ?', l'etudiant doit "
     "consulter 3 a 5 sources differentes. Aucune n'a toute l'information."),
    ("Saturation du service scolarite",
     "En periode de pointe (rentree, examens, reinscription), le service scolarite recoit "
     "200+ etudiants/jour avec des questions repetitives. 80% sont des questions de base "
     "qu'un chatbot peut absorber."),
    ("Indisponibilite hors horaires",
     "Les services administratifs ferment a 16h30 et le weekend. Les etudiants qui travaillent "
     "ou habitent loin sont penalises - ils n'ont acces a l'info qu'aux memes horaires que tout "
     "le monde."),
    ("Inegalite d'acces a l'information",
     "Les primo-entrants (1ere annee, premier semestre) n'ont pas de reseau d'anciens. Ils "
     "manquent des astuces que les anciens connaissent (quel prof est gentil, quels modules sont "
     "eliminatoires, comment reussir un concours...)."),
    ("Absence d'outil moderne",
     "La FSBM est en 2026 - une faculte de sciences ! - et ne dispose pas encore d'un point "
     "d'acces unifie a ses ressources academiques. Aucun moteur de recherche interne, aucun "
     "tableau de bord etudiant, aucun assistant intelligent."),
]
for n, d in pains:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("2.3 Qui souffre de ces problemes ?", ST_H1))
story.append(Paragraph(
    "Trois categories d'acteurs sont impactes :",
    ST_BODY))
actors = [
    ("Les etudiants (3000+)",
     "Frustration, perte de temps, sentiment d'etre 'oublies'."),
    ("Le personnel administratif (~30 personnes)",
     "Surcharge de travail repetitif (repeter 100 fois par jour 'voila les documents'), "
     "stress, fatigue."),
    ("Le decanat",
     "Image de marque ecornee, plaintes recurrentes des etudiants, difficulte a moderniser."),
]
for n, d in actors:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("2.4 Pourquoi un chatbot ?", ST_H1))
story.append(Paragraph(
    "Un chatbot resout ces problemes pour 4 raisons :",
    ST_BODY))
why_bot = [
    ("Disponibilite 24h/24",
     "Le chatbot ne dort jamais. Un etudiant qui revise a 23h peut poser sa question "
     "instantanement."),
    ("Reponses instantanees",
     "Pas de file d'attente. La reponse arrive en moins d'1 seconde."),
    ("Multilingue",
     "Notre chatbot comprend francais, anglais ET darija marocaine. Tres rare !"),
    ("Centralisation",
     "Toutes les sources sont agregees : site web, base de donnees academique, "
     "annonces officielles. L'etudiant n'a qu'un seul endroit a consulter."),
]
for n, d in why_bot:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))
story.append(PageBreak())

# ═══════ CHAPITRE 3 ═══════
story.append(Paragraph("Chapitre 3 - Objectifs du projet", ST_CHAPTER))

story.append(Paragraph("3.1 Methode SMART", ST_H1))
story.append(Paragraph(
    "Les objectifs ont ete formules selon la methode SMART :",
    ST_BODY))
story.append(std_table([
    ['Lettre', 'Signification', 'Application dans notre projet'],
    ['S', 'Specifique', 'Objectif clair, pas vague'],
    ['M', 'Mesurable', 'Avec un indicateur chiffrable'],
    ['A', 'Atteignable', 'Realiste avec nos ressources'],
    ['R', 'Realiste', 'Pertinent et utile'],
    ['T', 'Temporel', 'Avec une echeance'],
], col_widths=[1.5*cm, 3.5*cm, 11*cm]))

story.append(Paragraph("3.2 Les 7 objectifs concrets", ST_H1))
objectives = [
    ("Objectif 1 - Couvrir 60+ types de questions",
     "Indicateur : nombre d'intents reconnus dans le dataset.\nCible : 60+ intents.\n"
     "Resultat atteint : 28 intents enrichis (FR + EN + Darija) + RAG pour les variations."),
    ("Objectif 2 - Reponse en moins de 2 secondes",
     "Indicateur : latence moyenne par requete.\nCible : 2000ms.\n"
     "Resultat atteint : TF-IDF en 50-150ms, LLM en 150-300ms via Groq."),
    ("Objectif 3 - 3 langues supportees",
     "Indicateur : langues du dataset et detection.\nCible : FR + EN + Darija.\n"
     "Resultat atteint : 14/14 tests de detection langue passes."),
    ("Objectif 4 - Architecture professionnelle",
     "Indicateur : architecture micro-services + bonnes pratiques.\n"
     "Cible : 6 services planifies.\nResultat atteint : 2 livres, 4 en scaffolding."),
    ("Objectif 5 - Donnees realistes",
     "Indicateur : volume du seed data.\nCible : 3000+ etudiants.\n"
     "Resultat atteint : 107 profs + 2970 etudiants avec noms marocains."),
    ("Objectif 6 - Interface moderne",
     "Indicateur : nombre de pages + features UX.\nCible : 9 pages + mode sombre.\n"
     "Resultat atteint : 9 pages lazy-loaded, animations, responsive, dark mode."),
    ("Objectif 7 - Documentation exhaustive",
     "Indicateur : nombre de PDFs.\nCible : 3-5 PDFs.\n"
     "Resultat atteint : 6+ PDFs (rapport, guide tech, zombies, doc complete, guide IA, ces 10 PDFs)."),
]
for n, d in objectives:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("3.3 Ce qui est HORS scope (Phase 2)", ST_H1))
out_scope = [
    "Authentification reelle (JWT, login, sessions persistantes) - prevu Phase 2",
    "Reviews avec sentiment analysis - prevu Phase 2",
    "Notifications push en temps reel - prevu Phase 2",
    "Dashboard administrateur - prevu Phase 2",
    "Application mobile native - prevu Phase 3",
    "Integration avec Apogee (le SI universite) - hors scope (necessite accord institution)",
]
for o in out_scope:
    story.append(Paragraph(f"• {o}", ST_LIST))
story.append(PageBreak())

# ═══════ CHAPITRE 4 - CONCEPTS DE BASE ═══════
story.append(Paragraph("Chapitre 4 - Concepts de base avant d'aller plus loin", ST_CHAPTER))

story.append(Paragraph(
    "Ce chapitre presente les concepts fondamentaux que tu DOIS comprendre avant de lire la "
    "suite. C'est volontairement tres vulgarise, comme pour un cours de 1ere annee.",
    ST_BODY))

story.append(Paragraph("4.1 C'est quoi un site web ?", ST_H1))
story.append(Paragraph(
    "Un <b>site web</b> est un ensemble de pages accessibles via un navigateur (Chrome, "
    "Firefox, Edge). Il y a 2 types historiques :",
    ST_BODY))

story.append(Paragraph("Sites statiques (annees 90)", ST_H2))
story.append(Paragraph(
    "Pages HTML pre-ecrites. Le serveur envoie un fichier HTML, le navigateur l'affiche. "
    "C'est tout. Exemple : un blog personnel des annees 2000.",
    ST_BODY))

story.append(Paragraph("Sites dynamiques avec rechargement (annees 2000)", ST_H2))
story.append(Paragraph(
    "Quand tu cliques sur un lien, le navigateur recharge toute la page depuis zero. "
    "Le serveur genere du HTML 'a la volee' avec PHP/JSP/ASP. Exemple : Wikipedia des annees 2010.",
    ST_BODY))

story.append(Paragraph("4.2 C'est quoi une SPA ?", ST_H1))
story.append(Paragraph(
    "<b>SPA = Single Page Application = Application a Page Unique</b>. C'est l'evolution "
    "moderne des sites web (annees 2015+). Le navigateur charge UNE SEULE page HTML au depart, "
    "puis utilise du JavaScript pour <b>modifier dynamiquement le contenu</b> sans jamais "
    "recharger la page entiere.",
    ST_BODY))

story.append(analogy(
    "Imagine un <b>livre de coloriage</b>. Un site classique = chaque page est dans un livre "
    "different (rechargement complet). Une SPA = un seul livre, et tu effaces/redessine "
    "directement sur LA page selon ce que tu veux voir. C'est plus fluide et plus rapide."))

story.append(Paragraph(
    "Exemples connus de SPA : Gmail, Facebook, Twitter, Trello, Notion. Notre frontend "
    "Angular est une SPA.",
    ST_BODY))

story.append(Paragraph("Avantages de la SPA", ST_H2))
spa_pros = [
    "Experience utilisateur fluide (pas de 'flash blanc' au changement de page)",
    "Tres rapide une fois charge",
    "Le serveur ne fait pas de generation HTML (moins de charge)",
    "Le frontend et le backend peuvent etre developpes independamment",
]
for p in spa_pros:
    story.append(Paragraph(f"+ {p}", ST_LIST))

story.append(Paragraph("Inconvenients", ST_H2))
spa_cons = [
    "Premier chargement plus long (il faut telecharger tout le JavaScript)",
    "Moins bon pour le SEO (Google a du mal a indexer)",
    "Necessite du JavaScript active",
]
for c in spa_cons:
    story.append(Paragraph(f"- {c}", ST_LIST))

story.append(Paragraph("4.3 C'est quoi Angular ?", ST_H1))
story.append(Paragraph(
    "<b>Angular</b> est un <b>framework JavaScript</b> developpe par Google. Il sert a creer "
    "des SPA de maniere structuree.",
    ST_BODY))
story.append(Paragraph(
    "Un framework, c'est une <b>boite a outils complete</b> qui impose une organisation. "
    "Au lieu de coder tout from scratch, tu utilises les briques Angular (composants, "
    "services, routing, formulaires...) et tu te concentres sur ta logique metier.",
    ST_BODY))

story.append(analogy(
    "Angular est comme un kit LEGO pre-assemble pour faire une voiture. Tu as deja les roues, "
    "le chassis, les portes. Tu construis le design et l'interieur. Sans framework, tu devrais "
    "fabriquer les roues toi-meme."))

story.append(Paragraph(
    "Notre projet utilise <b>Angular 17</b> (version sortie en novembre 2023) qui apporte :",
    ST_BODY))
angular_features = [
    "<b>Standalone components</b> : composants autonomes sans modules",
    "<b>Signals</b> : reactivite native (alternative a RxJS pour les cas simples)",
    "<b>Control flow</b> : nouvelle syntaxe @if @for plus claire",
    "<b>Lazy loading</b> : chargement a la demande des pages",
]
for f in angular_features:
    story.append(Paragraph(f"• {f}", ST_LIST))

story.append(Paragraph("4.4 C'est quoi un backend ?", ST_H1))
story.append(Paragraph(
    "Le <b>backend</b> (ou serveur, ou cote serveur) est la partie du systeme qui "
    "<b>n'est pas visible</b> par l'utilisateur. C'est le 'cerveau' qui :",
    ST_BODY))
backend_role = [
    "Recoit les requetes du frontend",
    "Verifie qui tu es (authentification)",
    "Cherche les donnees dans la base",
    "Calcule, applique la logique metier",
    "Renvoie les resultats au frontend",
]
for r in backend_role:
    story.append(Paragraph(f"• {r}", ST_LIST))

story.append(analogy(
    "Le backend, c'est comme le <b>chef cuisinier</b> d'un restaurant. Le client (frontend) "
    "passe commande, le serveur (HTTP) transmet, le cuisinier (backend) prepare le plat avec "
    "les ingredients (base de donnees), et renvoie au client."))

story.append(Paragraph("4.5 C'est quoi FastAPI ?", ST_H1))
story.append(Paragraph(
    "<b>FastAPI</b> est un framework Python pour creer des API REST. C'est l'equivalent "
    "d'Angular mais cote serveur, et en Python au lieu de TypeScript.",
    ST_BODY))
fastapi_pros = [
    "<b>Rapide</b> : execution asynchrone native (async/await)",
    "<b>Validation automatique</b> : avec Pydantic (les donnees sont verifiees a l'arrivee)",
    "<b>Documentation auto</b> : Swagger UI genere automatiquement sur /docs",
    "<b>Moderne</b> : sortie en 2018, utilise les dernieres pratiques Python",
]
for p in fastapi_pros:
    story.append(Paragraph(f"• {p}", ST_LIST))

story.append(Paragraph("4.6 C'est quoi une API ?", ST_H1))
story.append(Paragraph(
    "<b>API = Application Programming Interface</b>. C'est un <b>contrat</b> entre 2 logiciels. "
    "Quand le frontend veut parler au backend, il doit suivre les regles definies dans l'API.",
    ST_BODY))

story.append(analogy(
    "L'API, c'est comme la <b>carte d'un restaurant</b>. Tu ne peux pas commander n'importe "
    "quoi - tu dois choisir parmi les plats listes, et les ingredients sont decrits. Une fois "
    "que tu commandes 'pizza margherita', tu sais ce que tu vas recevoir."))

story.append(Paragraph(
    "Notre backend expose une API REST avec des <b>endpoints</b> (= entrees, comme les plats "
    "de la carte) :",
    ST_BODY))
story.append(code(
    "POST /api/chat              -> envoyer un message au chatbot\n"
    "GET  /api/academic/filieres -> recuperer la liste des filieres\n"
    "GET  /api/llm/status        -> verifier si LLaMA est dispo"
))

story.append(Paragraph("4.7 C'est quoi REST ?", ST_H1))
story.append(Paragraph(
    "<b>REST = Representational State Transfer</b>. C'est un <b>style architectural</b> "
    "pour concevoir des API. Les regles :",
    ST_BODY))
rest_rules = [
    ("URL = ressource",
     "L'URL identifie une ressource (un objet). Ex: /api/filieres/SMI = la filiere SMI."),
    ("Methode HTTP = action",
     "GET = lire, POST = creer, PUT = remplacer, DELETE = supprimer, PATCH = modifier partiellement."),
    ("Stateless",
     "Chaque requete contient toute l'info necessaire. Le serveur ne se souvient pas des "
     "requetes precedentes."),
    ("Format standard",
     "Generalement JSON. Plus rarement XML, YAML, etc."),
]
for n, d in rest_rules:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("4.8 C'est quoi JSON ?", ST_H1))
story.append(Paragraph(
    "<b>JSON = JavaScript Object Notation</b>. C'est un format de donnees structurees, "
    "lisible par humain et machine. C'est devenu le standard pour les API.",
    ST_BODY))
story.append(code(
    "{\n"
    "  \"id\": 1,\n"
    "  \"code\": \"SMI\",\n"
    "  \"name\": \"Sciences Mathematiques et Informatique\",\n"
    "  \"type\": \"LICENCE\",\n"
    "  \"capacity\": 180,\n"
    "  \"modules\": [\n"
    "    { \"code\": \"M111\", \"name\": \"Analyse I\" },\n"
    "    { \"code\": \"M112\", \"name\": \"Algebre I\" }\n"
    "  ],\n"
    "  \"is_active\": true\n"
    "}"
))

story.append(Paragraph(
    "Structure :",
    ST_BODY))
json_struct = [
    "Objets entre <b>{ }</b>",
    "Tableaux entre <b>[ ]</b>",
    "Cles entre guillemets",
    "Valeurs : string, nombre, booleen (true/false), null, autre objet, autre tableau",
]
for s in json_struct:
    story.append(Paragraph(f"• {s}", ST_LIST))

story.append(Paragraph("4.9 C'est quoi un micro-service ?", ST_H1))
story.append(Paragraph(
    "Un <b>micro-service</b> est une <b>application autonome</b> qui fait UNE chose et la "
    "fait bien. Au lieu d'avoir une grosse application qui fait tout (monolithe), on la "
    "decoupe en plusieurs petites applications qui communiquent entre elles via HTTP.",
    ST_BODY))

story.append(analogy(
    "Le monolithe = un restaurant ou TOUS les employes font TOUT (caissier-serveur-cuisinier-"
    "vaisseliste). Si l'un est absent, tout s'arrete. Les micro-services = un restaurant ou "
    "chacun a son role : caissier, serveur, cuisinier, vaisseliste. Si le vaisseliste est "
    "absent, le restaurant continue (les autres assurent)."))

story.append(Paragraph(
    "Avantages :",
    ST_BODY))
micro_pros = [
    "Independance : chaque service evolue separement",
    "Resilience : si un service tombe, les autres continuent",
    "Stack heterogene : un service en Python, un autre en Go, un autre en Rust...",
    "Scalabilite : on peut multiplier seulement les services tres charges",
]
for p in micro_pros:
    story.append(Paragraph(f"+ {p}", ST_LIST))

story.append(Paragraph(
    "Inconvenients :",
    ST_BODY))
micro_cons = [
    "Complexite : il faut gerer le reseau, la latence, les pannes inter-services",
    "Debugging : plus dur de tracer une requete qui passe par plusieurs services",
    "Operations : il faut deployer N services au lieu d'1",
]
for c in micro_cons:
    story.append(Paragraph(f"- {c}", ST_LIST))
story.append(PageBreak())

# ═══════ CHAPITRE 5 - ARCHITECTURE ═══════
story.append(Paragraph("Chapitre 5 - Architecture micro-services expliquee", ST_CHAPTER))

story.append(Paragraph("5.1 Vue d'ensemble", ST_H1))
story.append(diagram(
    "  +-----------------------------------------------+\n"
    "  |  LE NAVIGATEUR DE L'UTILISATEUR (Chrome)      |\n"
    "  +-----------------------+-----------------------+\n"
    "                          | HTTP via JavaScript\n"
    "  +-----------------------v-----------------------+\n"
    "  |  FRONTEND ANGULAR (port 4200)                 |\n"
    "  |  (telecharge depuis http://localhost:4200)    |\n"
    "  +-----+--------+--------+--------+--------------+\n"
    "        |        |        |        |\n"
    "        | /api/chat                |\n"
    "        |        |        | /api/llm                 (proxy redirige)\n"
    "        v        v        v        v\n"
    "  +------+ +------+ +------+ +------+\n"
    "  |chatbot|         |academic|       (4 autres en Phase 2)\n"
    "  |:8001  | <-----> |:8002   |       student, review,\n"
    "  +------+         +------+       notification, analytics\n"
    "       |              |\n"
    "       +------+-------+\n"
    "              |\n"
    "              v\n"
    "      +---------------+    +---------------+\n"
    "      | MySQL 8       |    | MongoDB 7     |\n"
    "      | fsbm_db       |    | fsbm_reviews  |\n"
    "      | (16 tables)   |    | (6 collections)|\n"
    "      +---------------+    +---------------+\n"
))

story.append(Paragraph("5.2 Pourquoi cette architecture ?", ST_H1))
story.append(Paragraph(
    "Le projet aurait pu etre un <b>monolithe</b> (tout en un seul gros service). On a "
    "choisi les micro-services pour 5 raisons strategiques :",
    ST_BODY))
why_micro = [
    ("Demonstration pedagogique",
     "Un PFE doit demontrer la maitrise des pratiques modernes. Les grandes entreprises "
     "(Netflix, Uber, Amazon) utilisent toutes des micro-services. Le jury reconnaitra que "
     "l'equipe sait construire un systeme moderne."),
    ("Separation des responsabilites",
     "Chaque service a un role clair : chatbot fait du NLP, academic gere les donnees, "
     "student gerera l'auth. C'est plus facile a comprendre et a maintenir."),
    ("Evolutivite independante",
     "On peut ajouter un service (ex: notification) sans toucher aux autres. Phase 2 "
     "n'impacte pas Phase 1."),
    ("Stack heterogene",
     "Le chatbot utilise scikit-learn (ML), l'academic utilise SQLAlchemy (ORM SQL), le "
     "review utiliserait Motor (driver MongoDB async). Chacun choisit ses outils."),
    ("Resilience",
     "Si le service de reviews tombe, le chatbot et la navigation continuent de marcher. "
     "L'utilisateur n'est pas totalement bloque."),
]
for n, d in why_micro:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("5.3 Les 3 couches", ST_H1))
story.append(Paragraph(
    "L'architecture suit le pattern classique a 3 couches :",
    ST_BODY))

story.append(Paragraph("Couche 1 : Presentation (Frontend Angular)", ST_H2))
story.append(Paragraph(
    "Tout ce que l'utilisateur voit et avec quoi il interagit. C'est le HTML, CSS et "
    "TypeScript qui s'execute dans son navigateur. <b>Aucune logique metier ici</b> - "
    "juste de l'affichage et des appels HTTP au backend.",
    ST_BODY))

story.append(Paragraph("Couche 2 : Services (Backend FastAPI)", ST_H2))
story.append(Paragraph(
    "La logique metier. Les services Python recoivent les requetes du frontend, calculent, "
    "interrogent les bases de donnees, et renvoient des reponses. <b>C'est ici qu'est l'intelligence</b>.",
    ST_BODY))

story.append(Paragraph("Couche 3 : Persistance (MySQL + MongoDB)", ST_H2))
story.append(Paragraph(
    "Le stockage permanent des donnees. Quand on coupe le serveur, les donnees restent. "
    "<b>Aucune logique ici</b> - juste du stockage structure et indexe.",
    ST_BODY))

story.append(alert_box(
    "Cette separation stricte permet de remplacer une couche sans toucher aux autres. Par "
    "exemple, on pourrait remplacer Angular par React (couche 1) sans rien changer au backend.",
    kind="tip", title="Couplage faible"))
story.append(PageBreak())

# ═══════ CHAPITRE 6 - LES 6 SERVICES ═══════
story.append(Paragraph("Chapitre 6 - Les 6 services en detail", ST_CHAPTER))

story.append(Paragraph(
    "Le projet a planifie 6 micro-services. Phase 1 : 2 livres. Phase 2 : 4 a venir.",
    ST_BODY))

story.append(Paragraph("6.1 chatbot-service (port 8001) [LIVRE]", ST_H1))
story.append(Paragraph(
    "<b>Mission :</b> recevoir un message utilisateur et generer une reponse intelligente.",
    ST_BODY))
story.append(Paragraph(
    "<b>Sous-modules internes :</b>",
    ST_BODY))
chatbot_modules = [
    ("nlp/", "Pipeline NLP : preprocessor (tokenisation, stopwords, stemming), language_detector (FR/EN/Darija), classifier (TF-IDF + Cosine multi-langue)."),
    ("llm/", "Integration LLaMA 3 via Groq. groq_client.py, hf_client.py, rag.py, llm_service.py."),
    ("core/", "Memory (session, historique), persona (genre/nom), web_fetcher (scraping fsbm.ma)."),
    ("routers/", "Endpoints FastAPI : /api/chat, /api/llm/chat, /api/intents, /api/health."),
    ("models/", "Schemas Pydantic pour validation des inputs et outputs."),
]
for n, d in chatbot_modules:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("6.2 academic-service (port 8002) [LIVRE]", ST_H1))
story.append(Paragraph(
    "<b>Mission :</b> exposer les donnees academiques via API REST.",
    ST_BODY))
story.append(Paragraph(
    "<b>Endpoints :</b>",
    ST_BODY))
academic_eps = [
    "/api/overview - compteurs pour le dashboard",
    "/api/departments - 5 departements",
    "/api/filieres - 25 filieres (7 licences + 18 masters)",
    "/api/modules - 100+ modules",
    "/api/professors - annuaire paginé 107 profs",
    "/api/students - 2970 etudiants (filtres + pagination)",
    "/api/schedule - emploi du temps",
    "/api/exams - calendrier examens",
    "/api/announcements - annonces officielles",
    "/api/events - evenements universitaires",
    "/api/clubs - 8 clubs etudiants",
]
for e in academic_eps:
    story.append(Paragraph(f"• {e}", ST_LIST))

story.append(Paragraph("6.3 student-service (Phase 2)", ST_H1))
story.append(Paragraph(
    "<b>Mission :</b> authentification JWT + gestion des profils + roles.",
    ST_BODY))
story.append(Paragraph(
    "<b>Endpoints prevus :</b> POST /api/auth/login, POST /api/auth/register, GET /api/me, "
    "PUT /api/me/preferences, GET /api/users (admin only).",
    ST_BODY))

story.append(Paragraph("6.4 review-service (Phase 2)", ST_H1))
story.append(Paragraph(
    "<b>Mission :</b> CRUD des reviews MongoDB + sentiment analysis.",
    ST_BODY))
story.append(Paragraph(
    "<b>Endpoints prevus :</b> POST /api/reviews, GET /api/reviews/by-category, "
    "POST /api/feedbacks/quick (pouce haut/bas), GET /api/sentiment/stats.",
    ST_BODY))

story.append(Paragraph("6.5 notification-service (Phase 2)", ST_H1))
story.append(Paragraph(
    "<b>Mission :</b> notifications push en temps reel via Server-Sent Events (SSE).",
    ST_BODY))
story.append(Paragraph(
    "<b>Endpoints prevus :</b> GET /api/notifications/stream (SSE), "
    "POST /api/announcements (admin).",
    ST_BODY))

story.append(Paragraph("6.6 analytics-service (Phase 2)", ST_H1))
story.append(Paragraph(
    "<b>Mission :</b> dashboards administrateurs avec KPIs.",
    ST_BODY))
story.append(Paragraph(
    "<b>Endpoints prevus :</b> GET /api/stats/overview, GET /api/stats/top-intents, "
    "GET /api/stats/satisfaction, GET /api/stats/usage-by-hour.",
    ST_BODY))

story.append(Paragraph("6.7 Pourquoi exactement 6 services ?", ST_H1))
story.append(Paragraph(
    "Le decoupage en 6 services suit le principe <b>Single Responsibility</b> : chaque service "
    "a UNE mission claire. Si on faisait 2 services seulement, on aurait des 'gros' services "
    "qui violeraient ce principe. Si on faisait 20 services, on aurait trop de complexite "
    "reseau. 6 est un bon equilibre pour un PFE.",
    ST_BODY))
story.append(PageBreak())

# ═══════ CHAPITRE 7 - FRONTEND ═══════
story.append(Paragraph("Chapitre 7 - Le frontend Angular (vue d'ensemble)", ST_CHAPTER))

story.append(Paragraph(
    "Ce chapitre est volontairement bref - le PDF 02 detaille Angular en profondeur.",
    ST_BODY))

story.append(Paragraph("7.1 Structure", ST_H1))
story.append(code(
    "frontend/\n"
    "  src/\n"
    "    main.ts                    -> point d'entree, demarre l'app\n"
    "    index.html                 -> page HTML unique (la 'P' de SPA)\n"
    "    styles.css                 -> styles globaux + variables theme\n"
    "    assets/                    -> images, logos, ressources\n"
    "    app/\n"
    "      app.component.ts         -> composant racine\n"
    "      app.routes.ts            -> definition des 9 routes\n"
    "      layout/                  -> sidebar + topbar shared\n"
    "      core/                    -> theme service, etc.\n"
    "      services/                -> chat.service, academic.service\n"
    "      features/                -> 9 pages lazy-loaded\n"
    "      components/              -> chat-window, message-bubble, etc.\n"
    "      models/                  -> interfaces TypeScript"
))

story.append(Paragraph("7.2 Les 9 pages", ST_H1))
pages = [
    ['Route', 'Composant', 'Role'],
    ['/', 'DashboardComponent', 'Accueil avec stats'],
    ['/chat', 'ChatPageComponent', 'Assistant IA'],
    ['/departements', 'DepartmentsComponent', '5 cartes departements'],
    ['/filieres', 'FilieresComponent', '25 cartes filieres'],
    ['/filieres/:code', 'FiliereDetailComponent', 'Programme par semestre'],
    ['/modules', 'ModulesComponent', '100+ modules filtrables'],
    ['/professeurs', 'ProfessorsComponent', 'Annuaire profs paginé'],
    ['/actualites', 'NewsComponent', 'Annonces + events'],
    ['/vie-etudiante', 'StudentLifeComponent', '8 clubs etudiants'],
]
story.append(std_table(pages, col_widths=[3*cm, 5*cm, 8*cm]))

story.append(Paragraph("7.3 Communication avec le backend", ST_H1))
story.append(Paragraph(
    "Le frontend ne 'parle' jamais directement aux services. Il passe par le <b>proxy "
    "Angular dev server</b> qui redirige selon les regles de proxy.conf.json :",
    ST_BODY))
story.append(code(
    "// proxy.conf.json\n"
    "{\n"
    "  \"/api/chat\":     { \"target\": \"http://localhost:8001\" },\n"
    "  \"/api/llm\":      { \"target\": \"http://localhost:8001\" },\n"
    "  \"/api/academic\": { \"target\": \"http://localhost:8002\",\n"
    "                       \"pathRewrite\": {\"^/api/academic\": \"/api\"} }\n"
    "}"
))
story.append(Paragraph(
    "Ainsi, du point de vue Angular, tout passe par '/api/...' (URL relatives). Le proxy "
    "redirige automatiquement vers le bon micro-service.",
    ST_BODY))
story.append(PageBreak())

# ═══════ CHAPITRE 8 - BDD ═══════
story.append(Paragraph("Chapitre 8 - Les bases de donnees", ST_CHAPTER))

story.append(Paragraph("8.1 Pourquoi 2 bases ?", ST_H1))
story.append(Paragraph(
    "Le projet utilise <b>MySQL ET MongoDB</b> simultanement. Ce n'est pas pour faire "
    "compliqué - c'est une pratique appelee <b>polyglot persistence</b> : chaque type de "
    "donnees est stocke dans la BDD qui lui convient le mieux.",
    ST_BODY))
story.append(std_table([
    ['Type de donnees', 'Caracteristique', 'BDD ideale'],
    ['Etudiants, filieres, modules', 'Tres lies entre eux, schema fixe', 'MySQL (relationnel)'],
    ['Reviews textuelles', 'Schema variable, gros volume', 'MongoDB (documentaire)'],
    ['Logs d\'usage', 'Ecritures massives, peu de lectures', 'MongoDB'],
    ['Notes d\'examen', 'Liaisons fortes etudiant-module', 'MySQL'],
    ['Sentiments analyses', 'Structure JSON imbriquee', 'MongoDB'],
    ['Annonces officielles', 'Structure stable, peu d\'evolution', 'MySQL'],
], col_widths=[4*cm, 5*cm, 7*cm]))

story.append(Paragraph("8.2 MySQL - tour d'horizon", ST_H1))
story.append(Paragraph(
    "MySQL est une base de donnees <b>relationnelle</b> (tableaux relies entre eux par des "
    "cles etrangeres). Notre base s'appelle <code>fsbm_db</code> et contient <b>16 tables</b> :",
    ST_BODY))
mysql_tables = [
    "departments (5 rows) - les 5 departements",
    "filieres (25 rows) - 7 licences + 18 masters",
    "modules (100+ rows) - matieres par filiere",
    "professors (107 rows) - enseignants",
    "students (2970 rows) - etudiants inscrits",
    "module_teachers - relation N:N module/prof",
    "schedules - emploi du temps",
    "exams - calendrier examens",
    "grades (9000+ rows) - notes",
    "faq_categories - 16 categories",
    "faq_items - items FAQ",
    "conversations - historique chatbot",
    "feedbacks - notes utilisateurs",
    "announcements - 5+ annonces",
    "events - 5+ evenements",
    "clubs - 8 clubs",
]
for t in mysql_tables:
    story.append(Paragraph(f"• {t}", ST_LIST))

story.append(Paragraph(
    "Pour le detail des relations entre tables, voir le PDF 04 - MySQL + SQLAlchemy.",
    ST_NOTE))

story.append(Paragraph("8.3 MongoDB - tour d'horizon", ST_H1))
story.append(Paragraph(
    "MongoDB est une base de donnees <b>documentaire</b> (chaque entree est un document JSON). "
    "Notre base s'appelle <code>fsbm_reviews</code> et contient <b>6 collections</b> :",
    ST_BODY))
mongo_cols = [
    "reviews - avis textuels detaillés",
    "chatbot_feedback - pouce haut/bas",
    "conversations - log complet sessions",
    "sentiment_analysis - sentiments analyses",
    "usage_logs - tracking anonyme",
    "suggestions - suggestions ameliorations",
]
for c in mongo_cols:
    story.append(Paragraph(f"• {c}", ST_LIST))

story.append(Paragraph(
    "Pour le detail, voir le PDF 05 - MongoDB + NoSQL.",
    ST_NOTE))
story.append(PageBreak())

# ═══════ CHAPITRE 9 - HTTP/REST ═══════
story.append(Paragraph("Chapitre 9 - Communication via HTTP/REST", ST_CHAPTER))

story.append(Paragraph("9.1 C'est quoi HTTP ?", ST_H1))
story.append(Paragraph(
    "<b>HTTP = HyperText Transfer Protocol</b>. C'est le <b>langage</b> que parlent les "
    "navigateurs et les serveurs web depuis 1991. Chaque fois que tu visites un site web, "
    "ton navigateur fait une requete HTTP.",
    ST_BODY))

story.append(Paragraph("9.2 Anatomie d'une requete HTTP", ST_H1))
story.append(code(
    "REQUETE :\n"
    "POST /api/chat HTTP/1.1\n"
    "Host: localhost:8001\n"
    "Content-Type: application/json\n"
    "Authorization: Bearer eyJ0eXAi...\n"
    "\n"
    "{\n"
    "  \"message\": \"Quelles sont les filieres ?\",\n"
    "  \"session_id\": \"sess_abc123\"\n"
    "}\n"
    "\n"
    "REPONSE :\n"
    "HTTP/1.1 200 OK\n"
    "Content-Type: application/json\n"
    "\n"
    "{\n"
    "  \"response\": \"La FSBM propose 7 licences...\",\n"
    "  \"intent\": \"filieres\",\n"
    "  \"confidence\": 1.0,\n"
    "  \"session_id\": \"sess_abc123\"\n"
    "}"
))

story.append(Paragraph("9.3 Les 5 methodes HTTP principales", ST_H1))
story.append(std_table([
    ['Methode', 'Quand l\'utiliser', 'Exemple FSBM'],
    ['GET', 'Lire une ressource', 'GET /api/filieres'],
    ['POST', 'Creer une ressource', 'POST /api/chat'],
    ['PUT', 'Remplacer entierement', 'PUT /api/me/preferences'],
    ['PATCH', 'Modifier partiellement', 'PATCH /api/users/42'],
    ['DELETE', 'Supprimer', 'DELETE /api/reviews/123'],
], col_widths=[2*cm, 7*cm, 7*cm]))

story.append(Paragraph("9.4 Les codes de statut HTTP", ST_H1))
story.append(std_table([
    ['Code', 'Categorie', 'Signification'],
    ['200', 'Succes', 'OK - tout va bien'],
    ['201', 'Succes', 'Created - ressource creee'],
    ['204', 'Succes', 'No Content - succes sans contenu retourne'],
    ['301', 'Redirection', 'Permanent Redirect'],
    ['400', 'Erreur client', 'Bad Request - mauvais format'],
    ['401', 'Erreur client', 'Unauthorized - pas authentifie'],
    ['403', 'Erreur client', 'Forbidden - pas les droits'],
    ['404', 'Erreur client', 'Not Found - ressource introuvable'],
    ['422', 'Erreur client', 'Unprocessable Entity - validation echouee'],
    ['429', 'Erreur client', 'Too Many Requests - rate limit'],
    ['500', 'Erreur serveur', 'Internal Server Error - bug serveur'],
    ['502', 'Erreur serveur', 'Bad Gateway - service en aval down'],
    ['503', 'Erreur serveur', 'Service Unavailable - service down'],
], col_widths=[1.5*cm, 3.5*cm, 11*cm]))

story.append(Paragraph("9.5 Communication frontend -> backend", ST_H1))
story.append(diagram(
    "  [User clique 'Envoyer message']\n"
    "         |\n"
    "         v\n"
    "  [Angular ChatService.sendMessage()]\n"
    "         |\n"
    "         | this.http.post('/api/chat', { message, session_id })\n"
    "         v\n"
    "  [Navigateur fait requete HTTP POST]\n"
    "         |\n"
    "         | URL : http://localhost:4200/api/chat\n"
    "         v\n"
    "  [Angular Dev Proxy redirige]\n"
    "         |\n"
    "         | URL reecrite : http://localhost:8001/api/chat\n"
    "         v\n"
    "  [FastAPI recoit la requete]\n"
    "         |\n"
    "         | Valide avec Pydantic, traite, repond\n"
    "         v\n"
    "  [Reponse JSON]\n"
    "         |\n"
    "         | { response, intent, confidence, ... }\n"
    "         v\n"
    "  [Angular recoit dans subscribe()]\n"
    "         |\n"
    "         v\n"
    "  [Affichage dans MessageBubble]"
))
story.append(PageBreak())

# ═══════ CHAPITRE 10 - PORTS ═══════
story.append(Paragraph("Chapitre 10 - Les ports et leur utilite", ST_CHAPTER))

story.append(Paragraph("10.1 C'est quoi un port ?", ST_H1))
story.append(Paragraph(
    "Un <b>port</b> est un nombre entre 0 et 65535 qui identifie une application sur un "
    "ordinateur. Quand on dit 'localhost:8001', '8001' est le port.",
    ST_BODY))

story.append(analogy(
    "Imagine que ton ordinateur est un <b>immeuble</b> et que ton adresse IP (localhost = "
    "127.0.0.1) est l'<b>adresse postale</b> de l'immeuble. Le port est le <b>numero "
    "d'appartement</b>. Pour livrer un colis (paquet HTTP) au bon destinataire (application), "
    "il faut le bon numero d'appartement."))

story.append(Paragraph("10.2 Les ports utilises dans FSBM Platform", ST_H1))
story.append(std_table([
    ['Port', 'Service', 'Role'],
    ['4200', 'Angular dev server', 'Sert les fichiers HTML/CSS/JS du frontend'],
    ['8001', 'chatbot-service', 'NLP, chatbot, LLM'],
    ['8002', 'academic-service', 'Donnees academiques (filieres, profs...)'],
    ['3306', 'MySQL Server', 'BDD relationnelle (par defaut)'],
    ['27017', 'MongoDB Server', 'BDD documentaire (par defaut)'],
], col_widths=[2*cm, 4*cm, 10*cm]))

story.append(Paragraph("10.3 Pourquoi 8001 et 8002 et pas 5001/5002 ?", ST_H1))
story.append(Paragraph(
    "Initialement, on utilisait 5001 (chatbot) et 5002 (academic). Mais sous Windows + WSL2, "
    "ces ports sont parfois <b>squattes par des processus zombies</b> du subsystem Linux. "
    "On a migre vers 8001/8002 qui sont plus loin de la plage des reservations Hyper-V.",
    ST_BODY))

story.append(Paragraph(
    "Pour les details du probleme des ports zombies et de la solution, voir le PDF "
    "<i>FSBM_Platform_Guide_Zombies.pdf</i>.",
    ST_NOTE))

story.append(Paragraph("10.4 Comment changer un port ?", ST_H1))
story.append(code(
    "# Pour academic-service\n"
    "# Editer services/academic-service/.env :\n"
    "SERVICE_PORT=8002\n"
    "\n"
    "# Ou ligne de commande directe :\n"
    "py -m uvicorn app.main:app --port 8002\n"
    "\n"
    "# Pour Angular\n"
    "# Editer frontend/proxy.conf.json :\n"
    "{\n"
    "  \"/api/chat\": { \"target\": \"http://localhost:8001\" }\n"
    "}"
))
story.append(PageBreak())

# ═══════ CHAPITRE 11 - WORKFLOW ═══════
story.append(Paragraph("Chapitre 11 - Workflow global d'une requete", ST_CHAPTER))

story.append(Paragraph(
    "Voici ce qui se passe quand un etudiant tape un message dans le chatbot. Note les temps "
    "approximatifs - tout cela se passe en moins de 300ms perçus comme instantanes.",
    ST_BODY))

workflow_steps = [
    ("T+0 ms", "L'utilisateur clique 'Envoyer' dans son navigateur."),
    ("T+5 ms", "Angular intercepte le clic, le ChatService.sendMessage() est appele."),
    ("T+10 ms", "Angular construit une requete HTTP POST avec body JSON."),
    ("T+15 ms", "Le navigateur envoie : POST http://localhost:4200/api/chat"),
    ("T+20 ms", "Le dev server Angular consulte proxy.conf.json"),
    ("T+25 ms", "Il reecrit l'URL : http://localhost:8001/api/chat"),
    ("T+30 ms", "Le paquet TCP arrive sur localhost:8001"),
    ("T+35 ms", "uvicorn (serveur ASGI) recoit la requete, la passe a FastAPI"),
    ("T+40 ms", "FastAPI deserialise le JSON via Pydantic ChatRequest"),
    ("T+45 ms", "Validation : message length, session_id format, etc."),
    ("T+50 ms", "Le router chat.py prend la main : chat() est appele"),
    ("T+55 ms", "memory.get_or_create() recupere ou cree la session"),
    ("T+60 ms", "detect_gender(), detect_name() scannent le message"),
    ("T+65 ms", "classifier.predict() lance le pipeline NLP"),
    ("T+70 ms", "preprocessor preprocess() : lowercase, no stopwords, stemming"),
    ("T+75 ms", "language_detector detecte la langue (FR/EN/Darija)"),
    ("T+80 ms", "vectorizer.transform() vectorise le message"),
    ("T+90 ms", "cosine_similarity() calcule contre 461 patterns Darija"),
    ("T+100 ms", "Top intent identifie + reponse pre-ecrite recuperee"),
    ("T+110 ms", "personalize_response() substitue {voc} -> 'khoya' / 'khti'"),
    ("T+120 ms", "save_conversation() persiste en MySQL (asynchrone)"),
    ("T+130 ms", "memory.add_turn() enrichit la session en RAM"),
    ("T+140 ms", "ChatResponse construite avec metadata"),
    ("T+150 ms", "FastAPI serialise en JSON via Pydantic"),
    ("T+155 ms", "uvicorn envoie la reponse HTTP 200"),
    ("T+160 ms", "Le paquet revient sur localhost:4200"),
    ("T+165 ms", "Angular subscribe() est notifie de la reponse"),
    ("T+170 ms", "Le composant push le message dans messages[]"),
    ("T+200 ms", "Angular detecte le changement, met a jour le DOM"),
    ("T+250 ms", "Animation fadeIn du message bubble"),
    ("T+300 ms", "L'utilisateur voit la reponse, perception 'instantanee'"),
]
for t, d in workflow_steps:
    story.append(Paragraph(f"<b>{t}</b> - {d}", ST_LIST))

story.append(alert_box(
    "Tout ce parcours se passe en moins d'<b>1/3 de seconde</b>. La complexite est masquee "
    "par la rapidite du systeme.",
    kind="success"))
story.append(PageBreak())

# ═══════ CHAPITRE 12 - CHOIX TECHNIQUES ═══════
story.append(Paragraph("Chapitre 12 - Choix techniques justifies", ST_CHAPTER))

story.append(Paragraph(
    "Le jury va POSER ces questions. Voici les reponses preparees.",
    ST_BODY))

choices = [
    ("Pourquoi Angular plutot que React ou Vue ?",
     "Angular est plus opinionated (impose une structure), ce qui force de bonnes pratiques. "
     "Il integre nativement le routing, les formulaires, l'HTTP, les animations. Pour un projet "
     "PFE, c'est plus simple a structurer. React est plus flexible mais demande plus de choix."),
    ("Pourquoi FastAPI plutot que Flask/Django ?",
     "FastAPI est async natif (plus performant), valide automatiquement les inputs avec "
     "Pydantic, et genere Swagger UI gratuitement. Flask demande des libs externes pour tout "
     "ca. Django est trop monolithique pour des micro-services."),
    ("Pourquoi MySQL + MongoDB et pas une seule BDD ?",
     "Polyglot persistence : on choisit la BDD la mieux adaptee a chaque type de donnees. "
     "MySQL pour les donnees relationnelles (etudiants, filieres), MongoDB pour les donnees "
     "flexibles (reviews, logs)."),
    ("Pourquoi pas Docker ?",
     "Le cahier des charges PFE impose une compatibilite Windows sans conteneurs. Docker "
     "Desktop est lourd, conflits Hyper-V courants. On utilise des scripts batch/PowerShell "
     "et venv Python a la place."),
    ("Pourquoi TF-IDF et pas un LLM directement ?",
     "TF-IDF est gratuit, deterministe, explicable, ultra-rapide (5ms). Le LLM (LLaMA via "
     "Groq) est en option pour les questions complexes. Le TF-IDF sert aussi de retrieval "
     "pour le RAG du LLM."),
    ("Pourquoi 6 services et pas 1 ?",
     "Separation des responsabilites + demonstration des patterns modernes. Chaque service "
     "fait UNE chose et peut evoluer independamment."),
    ("Comment gerer la securite (Phase 2) ?",
     "JWT signe HS256 + bcrypt 12 rounds + 4 roles (STUDENT/PROF/SCOLARITE/ADMIN) + CORS "
     "strict + validation Pydantic + rate limiting."),
    ("Comment scaler si 10 000 utilisateurs ?",
     "Replication horizontale de chaque service + cache Redis + MySQL master/slave + "
     "MongoDB replica set + load balancer en front."),
]
for q, a in choices:
    story.append(Paragraph(f"<b>Q : {q}</b>", ST_H3))
    story.append(Paragraph(f"R : {a}", ST_BODY))
story.append(PageBreak())

# ═══════ CHAPITRE 13 - CONCLUSION ═══════
story.append(Paragraph("Chapitre 13 - Conclusion et lecture des autres PDFs", ST_CHAPTER))

story.append(Paragraph("13.1 Ce que tu as appris ici", ST_H1))
learnt = [
    "Le contexte FSBM et le probleme resolu",
    "L'architecture micro-services en 3 couches",
    "Les 6 services et leur role",
    "Les 9 pages du frontend Angular",
    "Les 2 bases de donnees (MySQL + MongoDB) et leur complementarite",
    "Le protocole HTTP, REST, JSON",
    "Les ports et leur utilite",
    "Le workflow complet d'une requete (T+0 a T+300 ms)",
    "Les 8 choix techniques justifies",
]
for l in learnt:
    story.append(Paragraph(f"+ {l}", ST_LIST))

story.append(Paragraph("13.2 Ou aller maintenant ?", ST_H1))
story.append(Paragraph(
    "Ce PDF est volontairement <b>generaliste</b>. Pour aller en profondeur sur chaque "
    "aspect, consulte les 9 autres PDFs :",
    ST_BODY))
next_pdfs = [
    ("PDF 02 - Frontend Angular", "Angular 17 ligne par ligne, signals, components, services, etc."),
    ("PDF 03 - Backend FastAPI", "FastAPI complet, async, Pydantic, routers, code expliqué"),
    ("PDF 04 - MySQL + SQLAlchemy", "SQL complet, 16 tables, relations, ORM, normalisation"),
    ("PDF 05 - MongoDB + NoSQL", "NoSQL, 6 collections, Motor async, comparaison SQL/NoSQL"),
    ("PDF 06 - NLP + IA chatbot", "Pipeline NLP complet, TF-IDF, RAG, LLM, embeddings"),
    ("PDF 07 - APIs + Communication", "REST detaillé, tous endpoints, communication inter-services"),
    ("PDF 08 - Securite", "JWT, bcrypt, OWASP, validation, CORS, roles"),
    ("PDF 09 - Workflow complet", "Step-by-step, 4 scenarios, tous les details"),
    ("PDF 10 - Guide soutenance", "30+ Q/R, demo script, vulgarisation, backup plan"),
]
for n, d in next_pdfs:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("13.3 Ordre de lecture recommande", ST_H1))
story.append(std_table([
    ['Ordre', 'PDF', 'Pourquoi maintenant'],
    ['1', 'PDF 01 (ce document)', 'Vue d\'ensemble'],
    ['2', 'PDF 10 - Soutenance', 'Pour savoir ce que le jury veut entendre'],
    ['3', 'PDF 09 - Workflow', 'Pour comprendre le flux global'],
    ['4', 'PDF 02 - Frontend', 'Approfondir Angular'],
    ['5', 'PDF 03 - Backend', 'Approfondir FastAPI'],
    ['6', 'PDF 06 - NLP/IA', 'Comprendre le cerveau du chatbot'],
    ['7', 'PDF 04 - MySQL', 'Approfondir la BDD principale'],
    ['8', 'PDF 05 - MongoDB', 'Approfondir le NoSQL'],
    ['9', 'PDF 07 - APIs', 'Reference des endpoints'],
    ['10', 'PDF 08 - Securite', 'Pour les questions securite'],
], col_widths=[1.5*cm, 5*cm, 9.5*cm]))

story.append(Spacer(1, 1*cm))
story.append(alert_box(
    "Si tu ne dois lire qu'<b>UN SEUL</b> autre PDF apres celui-ci, lis le <b>PDF 10 - Guide "
    "soutenance</b>. C'est celui qui te prepare le mieux a l'examen oral.",
    kind="key", title="Conseil critique"))

build_doc("01_Architecture_Globale_FSBM.pdf", story,
          "PDF 01 - Architecture Globale",
          "FSBM Platform - Architecture Globale")
