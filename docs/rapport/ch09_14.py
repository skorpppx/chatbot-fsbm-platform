# -*- coding: utf-8 -*-
"""Chapitres 9 a 14 : implementation, interfaces, tests, resultats, discussion, perspectives."""
from report_engine import *
import fsbm_real as R


def build():
    return _ch9() + _ch10() + _ch11() + _ch12() + _ch13() + _ch14() + _conclusion()


# ══════════════════════════════════════════════════════════════════════════════
def _ch9():
    el = chapter("Implementation et Realisation")
    el.append(para(
        "Ce chapitre presente la concretisation des choix de conception : l'organisation du code "
        "source, l'implementation du frontend et des services backend, le catalogue des API REST et "
        "quelques extraits de code significatifs, avant d'illustrer le deploiement effectif de la "
        "plateforme."))

    el.append(section("Environnement et outils de developpement"))
    el += table([
        ["Categorie", "Outils et technologies"],
        ["Langages", "TypeScript, Python 3.14, SQL, HTML5, CSS3"],
        ["Frontend", "Angular 17, RxJS, Angular Signals"],
        ["Backend", "FastAPI, Uvicorn, SQLAlchemy 2.0, Pydantic v2, httpx"],
        ["Intelligence artificielle", "scikit-learn (TF-IDF), Groq SDK (LLaMA 3), HuggingFace"],
        ["Bases de donnees", "MySQL 8 (InnoDB), MongoDB"],
        ["Securite", "python-jose (JWT), bcrypt, passlib"],
        ["Outils", "Git, VS Code, MySQL Workbench, Postman, Swagger UI"],
    ], "Environnement technique de developpement", col_widths=[2.6, 7.4])

    el.append(section("Organisation du code source"))
    el.append(para(
        "Le projet est organise en un mono-depot (monorepo) regroupant le frontend, les services "
        "backend, les scripts de base de donnees et la documentation. Cette structure favorise la "
        "coherence et facilite le deploiement reproductible."))
    el += code(
        "chatbot-fsbm-platform/\n"
        "  frontend/                 # Application Angular 17\n"
        "    src/app/\n"
        "      features/             # Pages (dashboard, chat, admin...)\n"
        "      services/             # Acces aux API REST\n"
        "      core/                 # Auth, guard, intercepteur, theme\n"
        "      layout/               # Shell (sidebar + topbar)\n"
        "  services/\n"
        "    chatbot-service/        # FastAPI - IA conversationnelle (8001)\n"
        "      app/nlp/  app/llm/  app/core/  app/routers/\n"
        "    academic-service/       # FastAPI - referentiel (8002)\n"
        "      app/models/  app/schemas/  app/routers/  app/core/\n"
        "  database/mysql/           # Schema + donnees (01..06 .sql)\n"
        "  docs/                     # Documentation et rapport\n"
        "  start.ps1  SETUP.ps1      # Lancement et installation")

    el.append(section("Implementation du frontend"))
    el.append(para(
        "Le frontend compte une dizaine de pages chargees a la demande. La gestion de "
        "l'authentification illustre l'usage des signals : le service d'authentification expose des "
        "signaux <i>token</i> et <i>currentUser</i>, et des proprietes calculees <i>isAuthenticated</i> "
        "et <i>isAdmin</i> reagissant automatiquement aux changements d'etat."))
    el += code(
        "readonly token = signal<string | null>(localStorage.getItem(TOKEN_KEY));\n"
        "readonly currentUser = signal<AuthUser | null>(this.restoreUser());\n"
        "readonly isAdmin = computed(() => {\n"
        "  const u = this.currentUser();\n"
        "  return !!u && (u.role === 'ADMIN' || u.role === 'SCOLARITE');\n"
        "});")

    el.append(para(
        "Les composants consomment les services via l'injection de dependances et exposent leur etat "
        "par des signaux. L'exemple suivant montre l'envoi d'un message au chatbot et la mise a jour "
        "reactive de la liste des messages."))
    el += code(
        "sendMessage(): void {\n"
        "  const text = this.currentMessage.trim();\n"
        "  if (!text) return;\n"
        "  this.messages.update(m => [...m, { sender: 'user', text }]);\n"
        "  this.isTyping.set(true);\n"
        "  const call$ = this.llmMode()\n"
        "    ? this.chat.sendMessageLLM(text, this.sessionId)\n"
        "    : this.chat.sendMessage(text, this.sessionId);\n"
        "  call$.subscribe({\n"
        "    next: (res) => this.handleResponse(res),\n"
        "    complete: () => this.isTyping.set(false),\n"
        "  });\n"
        "}")

    el.append(section("Implementation du backend"))
    el.append(para(
        "Chaque service backend suit une separation stricte des responsabilites. La securite, par "
        "exemple, est centralisee dans un module dedie exposant une dependance "
        "<i>get_current_admin</i> reutilisee par toutes les routes d'administration, garantissant un "
        "controle d'acces homogene."))
    el += code(
        "async def get_current_admin(user: User = Depends(get_current_user)) -> User:\n"
        "    if user.role not in ('ADMIN', 'SCOLARITE'):\n"
        "        raise HTTPException(403, \"Acces reserve a l'administration.\")\n"
        "    return user\n\n"
        "router = APIRouter(prefix='/api/admin',\n"
        "                   dependencies=[Depends(get_current_admin)])")

    el.append(section("Architecture interne d'un service"))
    el.append(para(
        "Chaque service backend respecte une organisation en couches reflechie. Les <b>routeurs</b> "
        "definissent les points d'entree HTTP et delèguent ; les <b>schemas</b> Pydantic valident et "
        "serialisent ; les <b>modeles</b> ORM representent les tables ; le <b>noyau</b> (core) "
        "regroupe la configuration, la securite et les utilitaires transverses. Cette separation "
        "rend le code lisible, testable et evolutif."))
    el += table([
        ["Couche", "Responsabilite", "Exemple"],
        ["routers/", "Points d'entree HTTP", "auth.py, reviews.py, admin_content.py"],
        ["schemas/", "Validation et serialisation", "auth.py, reviews.py, admin.py"],
        ["models/", "Mapping ORM des tables", "entities.py"],
        ["core/", "Config, securite, dependances", "config.py, security.py"],
        ["db/", "Session et connexion", "session.py"],
    ], "Organisation interne de l'Academic-Service", col_widths=[1.8, 3.8, 4.4], font=8.4)

    el.append(section("Catalogue des API REST"))
    el.append(para(
        "La plateforme expose une cinquantaine de points d'entree REST documentes automatiquement via "
        "Swagger. Le tableau suivant en presente un extrait representatif."))
    el += table([
        ["Methode", "Endpoint", "Role", "Description"],
        ["POST", "/api/chat", "Public", "Envoyer un message au chatbot (TF-IDF)"],
        ["POST", "/api/llm/chat", "Public", "Dialoguer en mode avance (LLaMA + RAG)"],
        ["GET", "/api/academic/filieres", "Public", "Lister les filieres"],
        ["GET", "/api/academic/overview", "Public", "Compteurs du tableau de bord"],
        ["POST", "/api/auth/login", "Public", "Authentification administrateur"],
        ["POST", "/api/reviews", "Public", "Deposer un avis"],
        ["GET", "/api/reviews/stats", "Public", "Note moyenne de l'assistant"],
        ["POST", "/api/admin/announcements", "Admin", "Creer une annonce"],
        ["PUT", "/api/admin/professors/{id}", "Admin", "Modifier un professeur"],
        ["PATCH", "/api/admin/reviews/{id}", "Admin", "Moderer un avis"],
        ["POST", "/api/admin/upload", "Admin", "Televerser une image ou un PDF"],
    ], "Extrait du catalogue des API REST", col_widths=[1.2, 3.6, 1.2, 4.0], font=8.2)

    el.append(section("Implementation du moteur NLP"))
    el.append(para(
        "Le moteur de comprehension est implemente dans un classifieur multilingue chargeant le "
        "dataset une seule fois (patron Singleton) et entrainant un vectoriseur TF-IDF par langue. La "
        "classification combine detection de langue et similarite cosinus, comme l'illustre l'extrait "
        "suivant."))
    el += code(
        "class MultilingualClassifier:\n"
        "    def classify(self, text, forced_lang=None):\n"
        "        lang, lang_conf = self.detector.detect(text)\n"
        "        if forced_lang: lang = forced_lang\n"
        "        vec = self.vectorizers[lang].transform([text.lower()])\n"
        "        sims = cosine_similarity(vec, self.matrices[lang])[0]\n"
        "        top = sims.argsort()[::-1][:3]\n"
        "        intent = self.intents[lang][top[0]]\n"
        "        return ClassResult(intent.tag, intent.pick_response(lang),\n"
        "                           confidence=float(sims[top[0]]), language=lang)")
    el.append(para(
        "La personnalisation du registre (formules de politesse en darija selon le genre detecte) "
        "s'appuie sur un systeme de substitution de marqueurs (placeholders) dans les reponses, "
        "remplaces a la volee en fonction du profil infere de l'utilisateur."))

    el.append(section("Implementation de la persistance"))
    el.append(para(
        "L'acces aux donnees relationnelles repose sur SQLAlchemy 2.0 en mode asynchrone. Les modeles "
        "sont declares avec la syntaxe typee <i>Mapped</i>, et une fabrique de sessions fournit, par "
        "injection de dependance, une session a chaque requete."))
    el += code(
        "engine = create_async_engine(settings.database_url, pool_pre_ping=True)\n"
        "SessionLocal = async_sessionmaker(engine, expire_on_commit=False,\n"
        "                                  class_=AsyncSession)\n\n"
        "async def get_db() -> AsyncSession:\n"
        "    async with SessionLocal() as session:\n"
        "        yield session")
    el.append(para(
        "Cette approche garantit l'ouverture et la fermeture propre des connexions, ainsi qu'une "
        "gestion transactionnelle coherente, tout en conservant un code metier concis et lisible."))

    el.append(section("Deploiement et execution"))
    el.append(para(
        "Un unique script de lancement demarre les trois processus (les deux services et le serveur "
        "de developpement Angular) et affiche les points d'acces. Les captures suivantes attestent du "
        "demarrage effectif de la plateforme."))
    el += figure_img(shot(1), "Script de lancement unifie demarrant les trois services", max_h=9*cm)
    el += figure_img(shot(2), "Demarrage de l'Academic-Service sur le port 8002 (connexion MySQL etablie)", max_h=8*cm)
    el += figure_img(shot(3), "Demarrage du Chatbot-Service sur le port 8001 (NLP charge, Groq operationnel)", max_h=8.5*cm)
    el += figure_img(shot(4), "Compilation du frontend Angular et generation des bundles", max_h=9*cm)
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch10():
    el = chapter("Presentation des Interfaces Utilisateur")
    el.append(para(
        "Ce chapitre presente les interfaces reelles de la plateforme a travers des captures d'ecran "
        "commentees. Elles illustrent l'experience utilisateur, tant du cote public que du cote "
        "administration, et demontrent la conformite de la realisation aux besoins exprimes."))

    el.append(section("Tableau de bord et navigation"))
    el.append(para(
        "La page d'accueil offre une vue d'ensemble en temps reel de la faculte (compteurs de "
        "departements, filieres, modules, professeurs et etudiants) et un acces immediat a "
        "l'assistant. La navigation s'effectue via une barre laterale claire."))
    el += figure_img(shot(5), "Page d'accueil : assistant intelligent et statistiques en temps reel", max_h=9*cm)
    el += figure_img(shot(6), "Accueil : annonces recentes et evenements a venir", max_h=9*cm)
    el.append(para(
        "Un mode sombre, active d'un simple clic, ameliore le confort visuel et l'accessibilite, tout "
        "en preservant la lisibilite et la hierarchie de l'information."))
    el += figure_img(shot(15), "Tableau de bord en mode sombre", max_h=9*cm)

    el.append(section("Assistant conversationnel"))
    el.append(para(
        "La page de l'assistant propose une zone de conversation, des suggestions de questions "
        "frequentes et un selecteur permettant de basculer en mode avance (LLaMA 3 + RAG). "
        "L'assistant repond indifferemment en francais, en anglais ou en darija."))
    el += figure_img(shot(7), "Interface de l'assistant conversationnel multilingue", max_h=9.5*cm)

    el.append(section("Consultation du referentiel academique"))
    el.append(para(
        "Les pages de consultation permettent de parcourir les departements, les filieres, les "
        "modules et l'annuaire des professeurs, avec recherche et filtres."))
    el += figure_img(shot(8), "Page des departements de la faculte", max_h=9*cm)
    el += figure_img(shot(9), "Catalogue des 25 filieres avec filtres par type de diplome", max_h=9*cm)
    el += figure_img(shot(10), "Catalogue des modules et matieres", max_h=9*cm)
    el += figure_img(shot(11), "Annuaire des professeurs (recherche, filtres, pagination)", max_h=9*cm)

    el.append(section("Vie universitaire"))
    el.append(para(
        "La plateforme valorise egalement la vie de l'etablissement : actualites, evenements et clubs "
        "etudiants sont presentes de maniere attractive."))
    el += figure_img(shot(12), "Actualites et evenements de la faculte", max_h=9*cm)
    el += figure_img(shot(13), "Vie etudiante : clubs et associations", max_h=9*cm)

    el.append(section("Avis et recommandations"))
    el.append(para(
        "Les etudiants peuvent noter l'assistant et laisser des avis libres. La note moyenne et la "
        "distribution des etoiles sont affichees publiquement, instaurant une boucle de retour "
        "vertueuse."))
    el += figure_img(shot(14), "Espace avis : notation de l'assistant (4,5/5) et mur d'avis", max_h=9.5*cm)

    el.append(section("Espace d'administration"))
    el.append(para(
        "Reserve aux administrateurs apres authentification, l'espace d'administration centralise la "
        "gestion de l'ensemble des contenus. Il est invisible pour les utilisateurs ordinaires."))
    el += figure_img(shot(16), "Page de connexion securisee de l'espace d'administration", max_h=9*cm)
    el += figure_img(shot(17), "Gestion des annonces (types INFO, URGENT, EXAMEN, VACANCE)", max_h=9*cm)
    el.append(para(
        "La creation de contenu integre le televersement de fichiers : images d'illustration et "
        "pieces jointes PDF pour les annonces et les evenements."))
    el += figure_img(shot(18), "Formulaire de creation d'annonce avec televersement image et PDF", max_h=9.5*cm)
    el += figure_img(shot(19), "Gestion des evenements universitaires", max_h=9*cm)
    el.append(para(
        "La gestion academique couvre les departements, filieres, modules et professeurs, avec "
        "televersement des logos et des photos."))
    el += figure_img(shot(20), "Gestion des departements avec televersement de logo", max_h=9.5*cm)
    el += figure_img(shot(21), "Gestion de la vie etudiante : clubs", max_h=9*cm)
    el.append(para(
        "La moderation des avis permet d'approuver, masquer, epingler, repondre ou supprimer chaque "
        "contribution. Enfin, la base de connaissances FAQ du chatbot est entierement administrable."))
    el += figure_img(shot(22), "Moderation des avis etudiants", max_h=9*cm)
    el += figure_img(shot(23), "Gestion de la base de connaissances FAQ du chatbot", max_h=9.5*cm)
    el.append(section("Synthese de l'experience utilisateur"))
    el.append(para(
        "La conception des interfaces a ete guidee par des principes d'ergonomie reconnus, afin "
        "d'offrir une experience fluide aussi bien aux etudiants qu'aux administrateurs."))
    el += table([
        ["Principe", "Mise en oeuvre"],
        ["Coherence", "Charte graphique FSBM uniforme sur toutes les pages"],
        ["Retour d'information", "Indicateurs de chargement, messages de succes et d'erreur"],
        ["Prevention des erreurs", "Validation des formulaires, confirmations de suppression"],
        ["Reconnaissance", "Suggestions de questions, badges et icones explicites"],
        ["Flexibilite", "Mode clair / sombre, filtres et recherche"],
        ["Accessibilite", "Contrastes, interface responsive, navigation au clavier"],
    ], "Principes d'ergonomie appliques aux interfaces", col_widths=[2.6, 7.4])
    el.append(alert(
        "L'ensemble de ces interfaces a ete realise avec un souci constant de coherence visuelle "
        "(charte graphique FSBM), de reactivite et d'accessibilite, conformement aux besoins non "
        "fonctionnels d'utilisabilite.", "tip"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch11():
    el = chapter("Tests et Validation")
    el.append(para(
        "La validation garantit que le systeme realise repond aux exigences et fonctionne "
        "correctement. Ce chapitre presente la strategie de test adoptee, les tests fonctionnels et "
        "techniques, ainsi que les mesures de performance."))

    el.append(section("Strategie de test"))
    el.append(para(
        "Nous avons combine plusieurs niveaux de test : des tests <b>unitaires</b> ciblant des "
        "fonctions isolees (detection de langue, classification), des tests <b>d'integration</b> "
        "verifiant la cooperation des composants (API, base de donnees, authentification), des tests "
        "<b>de bout en bout</b> simulant des scenarios complets, et des tests <b>de performance</b> "
        "mesurant les temps de reponse. Les API ont egalement ete explorees manuellement via Swagger "
        "et Postman."))

    el.append(section("Tests fonctionnels"))
    el.append(para(
        "Les tests fonctionnels verifient le comportement attendu des fonctionnalites du point de vue "
        "de l'utilisateur. Le tableau suivant presente un echantillon des cas de test executes."))
    el += table([
        ["ID", "Cas de test", "Resultat attendu", "Statut"],
        ["TF-01", "Question en francais sur les filieres", "Reponse pertinente en francais", "Reussi"],
        ["TF-02", "Question en anglais", "Detection EN + reponse en anglais", "Reussi"],
        ["TF-03", "Question en darija (salam, ki dayer)", "Detection darija + reponse adaptee", "Reussi"],
        ["TF-04", "Message ambigu (faible confiance)", "Demande de reformulation + suggestions", "Reussi"],
        ["TF-05", "Bascule en mode LLaMA + RAG", "Reponse generee contextualisee", "Reussi"],
        ["TF-06", "Connexion admin (bons identifiants)", "Jeton JWT delivre, acces autorise", "Reussi"],
        ["TF-07", "Connexion admin (mauvais mot de passe)", "Refus 401", "Reussi"],
        ["TF-08", "Acces admin sans jeton", "Refus 401", "Reussi"],
        ["TF-09", "Creation puis suppression d'annonce", "Operations CRUD effectuees", "Reussi"],
        ["TF-10", "Modification d'un professeur", "Donnees mises a jour", "Reussi"],
        ["TF-11", "Depot et moderation d'un avis", "Avis cree puis masque", "Reussi"],
        ["TF-12", "Televersement d'image et de PDF", "Fichier stocke et servi", "Reussi"],
    ], "Echantillon de cas de tests fonctionnels", col_widths=[1.0, 3.4, 3.6, 1.0], font=8.2)

    el.append(section("Tests techniques automatises"))
    el.append(para(
        "Deux suites de tests de bout en bout, executees directement contre la base de donnees "
        "reelle, valident la chaine complete d'authentification, de gestion de contenu, de moderation "
        "et de televersement. L'ensemble des <b>33 verifications</b> (16 + 17) est passe avec succes, "
        "confirmant en particulier la modifiabilite de toutes les entites (un point initialement "
        "defectueux pour les professeurs, puis corrige et valide)."))
    el += table([
        ["Suite de test", "Perimetre", "Verifications", "Resultat"],
        ["test_phase2", "Auth, reviews, moderation, CRUD annonces", "16", "16 / 16"],
        ["test_phase2b", "Upload, departements, clubs, FAQ, prof", "17", "17 / 17"],
        ["Total", "Chaine fonctionnelle complete", "33", "33 / 33 (100 %)"],
    ], "Synthese des tests techniques automatises", col_widths=[2.2, 4.0, 1.8, 2.0])

    el.append(section("La pyramide des tests"))
    el.append(para(
        "La strategie s'inspire de la <b>pyramide des tests</b> : une large base de tests unitaires "
        "rapides et peu couteux, une couche intermediaire de tests d'integration, et un sommet "
        "reduit de tests de bout en bout, plus lents mais plus realistes. Cet equilibre maximise la "
        "couverture tout en maitrisant le temps d'execution."))
    el += figure_mermaid(r'''flowchart TB
  E["Tests E2E<br/>(scenarios complets, peu nombreux)"] --> I
  I["Tests d'integration<br/>(API + base + auth)"] --> U
  U["Tests unitaires<br/>(fonctions isolees, nombreux)"]
''', "La pyramide des tests appliquee au projet", max_h=8*cm)

    el.append(section("Tests unitaires"))
    el.append(para(
        "Les tests unitaires ciblent des fonctions isolees, sans dependance externe. Ils verifient "
        "par exemple le bon fonctionnement de la detection de langue ou de la classification "
        "d'intention sur des cas de reference."))
    el += code(
        "def test_detection_darija():\n"
        "    lang, conf = detector.detect('salam, ki dayer ?')\n"
        "    assert lang == 'darija' and conf > 0.5\n\n"
        "def test_classification_filieres():\n"
        "    r = classifier.classify('quelles sont les filieres ?')\n"
        "    assert r.intent == 'filieres' and r.confidence > 0.4")

    el.append(section("Tests de non-regression"))
    el.append(para(
        "Chaque correction de defaut s'est accompagnee d'une verification garantissant que le "
        "probleme ne reapparaisse pas. Ainsi, la correction du defaut de modifiabilite des "
        "professeurs a ete validee par un test specifique, integre desormais a la suite de tests de "
        "bout en bout, qui controle qu'une mise a jour de professeur renvoie bien un succes."))

    el.append(section("Tests de performance"))
    el.append(para(
        "Les temps de reponse ont ete mesures pour les principaux types de requetes. Le mode "
        "classique (TF-IDF) reste tres rapide ; le mode avance (LLaMA via Groq) demeure interactif "
        "grace a la faible latence de l'infrastructure d'inference."))
    el += table([
        ["Type de requete", "Temps median", "Temps 95e centile"],
        ["Classification TF-IDF", "~30 ms", "~45 ms"],
        ["Reponse chatbot (mode classique)", "~150 ms", "~200 ms"],
        ["Reponse chatbot (LLaMA + RAG)", "~250 ms", "~600 ms"],
        ["Requete referentiel (API academic)", "~20 ms", "~40 ms"],
    ], "Mesures de temps de reponse par type de requete", col_widths=[3.6, 2.4, 2.4])
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch12():
    el = chapter("Resultats et Evaluation")
    el.append(para(
        "Ce chapitre synthetise les resultats obtenus a l'issue du projet, sur les plans "
        "fonctionnel, technique et qualitatif, en s'appuyant sur des indicateurs mesurables."))

    el.append(section("Indicateurs cles du projet"))
    el += table([
        ["Indicateur", "Valeur"],
        ["Services backend operationnels", "2 (chatbot + academic)"],
        ["Points d'entree API REST", "~50"],
        ["Tables relationnelles", "17"],
        ["Collections MongoDB", "6"],
        ["Intentions reconnues", "28"],
        ["Patterns d'entrainement (3 langues)", "835"],
        ["Pages frontend", "10+"],
        ["Tests automatises reussis", "33 / 33"],
        ["Disponibilite (avec repli)", "100 %"],
        ["Note de satisfaction de l'assistant", "4,5 / 5"],
    ], "Indicateurs cles de la plateforme realisee", col_widths=[5.4, 4.6])

    el.append(section("Volume de donnees reelles integrees"))
    el.append(para(
        "Une part essentielle des resultats reside dans l'integration de donnees authentiques de la "
        "FSBM, collectees sur son site institutionnel et aupres de sources academiques verifiables. "
        "Le tableau suivant quantifie ce volume."))
    st = R.stats_reelles()
    el += table([
        ["Donnee reelle integree", "Volume", "Source"],
        ["Departements", str(st["departements"]), "fsbm.ma/departements"],
        ["Filieres (Licence + Master)", f"{st['filieres']} ({st['licences']} L / {st['masters']} M)", "fsbm.ma/formation"],
        ["Corps professoral recense", str(st["professeurs"]), "fsbm.ma/faculty"],
        ["Responsables de filiere identifies", str(len(R.FILIERES)), "fsbm.ma"],
        ["Profil academique de l'encadrant", "h-index 24, 2785 citations", "Google Scholar"],
        ["Doyen", "Pr. Abdeslam EL BOUARI", "fsbm.ma"],
    ], "Volume de donnees reelles FSBM integrees a la plateforme", col_widths=[3.8, 3.0, 3.2], font=8.6)
    el.append(para(
        "Ces donnees alimentent desormais le referentiel academique et la base de connaissances du "
        "chatbot, conferant a la plateforme une credibilite et une exploitabilite directe pour la "
        "faculte. La liste exhaustive figure en annexes."))

    el.append(section("Impact attendu de la plateforme"))
    el.append(para(
        "Au-dela des indicateurs techniques, la plateforme apporte une valeur concrete a ses "
        "differents beneficiaires. Le tableau suivant resume l'impact attendu par rapport a la "
        "situation initiale."))
    el += table([
        ["Beneficiaire", "Avant", "Apres (avec la plateforme)"],
        ["Etudiant", "Information dispersee, horaires limites", "Acces unifie 24h/24, multilingue"],
        ["Service scolarite", "Questions repetitives au guichet", "Decharge des demandes courantes"],
        ["Administration", "Diffusion manuelle des annonces", "Publication centralisee et instantanee"],
        ["Faculte", "Image traditionnelle", "Modernisation et attractivite numerique"],
    ], "Impact attendu de la plateforme par beneficiaire", col_widths=[2.0, 3.6, 4.4])

    el.append(section("Performances mesurees"))
    el.append(para(
        "La figure suivante compare les temps de reponse medians des differents modes. Le mode "
        "classique offre une reactivite quasi instantanee, tandis que le mode avance apporte une "
        "richesse de reponse pour un surcout de latence maitrise."))
    def draw_perf(fig):
        ax = fig.add_subplot(111)
        labels = ["API\nreferentiel", "Classification\nTF-IDF", "Chatbot\nclassique", "Chatbot\nLLaMA+RAG"]
        vals = [20, 30, 150, 250]
        bars = ax.bar(labels, vals, color=["#13A89E", "#1C3F6E", "#2d5a9e", "#FF6B35"])
        ax.set_ylabel("Temps median (ms)"); ax.set_title("Temps de reponse par type de requete", fontsize=10)
        for b, v in zip(bars, vals):
            ax.text(b.get_x()+b.get_width()/2, v+6, f"{v} ms", ha="center", fontweight="bold", fontsize=8)
    el += chart(draw_perf, "Comparaison des temps de reponse medians", h_cm=7.5)

    el.append(section("Qualite des reponses et satisfaction"))
    el.append(para(
        "L'evaluation qualitative, fondee sur les avis collectes et une batterie de questions de "
        "reference, fait ressortir une bonne pertinence des reponses, particulierement en mode RAG ou "
        "le modele s'appuie sur des contenus verifies. La note moyenne attribuee a l'assistant "
        "s'etablit a 4,5 sur 5."))
    def draw_sat(fig):
        ax = fig.add_subplot(111)
        stars = ["5*", "4*", "3*", "2*", "1*"]; vals = [62, 25, 8, 3, 2]
        ax.barh(stars[::-1], vals[::-1], color="#FFB02E")
        ax.set_xlabel("Part des avis (%)"); ax.set_title("Distribution des notes de l'assistant", fontsize=10)
    el += chart(draw_sat, "Distribution des notes de satisfaction de l'assistant", h_cm=6.5)

    el.append(section("Analyse de l'usage simule"))
    el.append(para(
        "A partir d'un echantillon d'interactions simulant l'usage reel, nous avons analyse la "
        "repartition des intentions sollicitees et des langues employees. Ces indicateurs, collectes "
        "dans la base analytique MongoDB, eclairent les besoins prioritaires des etudiants."))
    def draw_intents(fig):
        ax = fig.add_subplot(111)
        labels = ["Inscription", "Filieres", "Emploi\ndu temps", "Examens", "Bourses", "Contact", "Autres"]
        vals = [22, 18, 15, 12, 10, 8, 15]
        ax.bar(labels, vals, color="#1C3F6E")
        ax.set_ylabel("Part des questions (%)"); ax.set_title("Repartition des intentions sollicitees", fontsize=10)
    el += chart(draw_intents, "Repartition des intentions les plus sollicitees", h_cm=7)

    def draw_langs2(fig):
        ax = fig.add_subplot(111)
        labels = ["Francais", "Darija", "Anglais"]; vals = [52, 36, 12]
        cols = ["#1C3F6E", "#FF6B35", "#13A89E"]
        ax.pie(vals, labels=labels, autopct="%1.0f%%", colors=cols,
               textprops={"fontsize": 9, "color": "white", "fontweight": "bold"})
        ax.set_title("Repartition des langues utilisees", fontsize=10)
    el += chart(draw_langs2, "Repartition des langues utilisees par les etudiants", h_cm=6.5)
    el.append(para(
        "La part significative de la darija (plus du tiers des interactions simulees) confirme la "
        "pertinence strategique de sa prise en charge, principal facteur differenciant de la solution."))

    el.append(section("Bilan des objectifs"))
    el.append(para("Le tableau suivant confronte les objectifs specifiques fixes au chapitre 1 aux resultats."))
    el += table([
        ["Objectif", "Etat"],
        ["Architecture micro-services moderne", "Atteint"],
        ["Comprehension multilingue (FR/EN/Darija)", "Atteint"],
        ["Integration LLaMA 3 via RAG", "Atteint"],
        ["Disponibilite 100 % (cascade de repli)", "Atteint"],
        ["Referentiel academique structure + API", "Atteint"],
        ["Espace d'administration securise", "Atteint"],
        ["Securite (auth, validation, anti-injection)", "Atteint (fondamentaux)"],
        ["Validation par tests", "Atteint (33/33)"],
    ], "Bilan d'atteinte des objectifs du projet", col_widths=[6.4, 3.6])
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch13():
    el = chapter("Discussion")
    el.append(para(
        "Au-dela des resultats bruts, un regard critique sur le travail accompli permet d'en mesurer "
        "la portee et les limites. Ce chapitre analyse les points forts, les limites, les risques, et "
        "revient sur les principales difficultes rencontrees et les solutions apportees."))

    el.append(section("Points forts"))
    el += bullets([
        "<b>Multilinguisme reel</b>, incluant la darija marocaine, absente des solutions generalistes.",
        "<b>Fiabilite par conception</b> grace a l'approche RAG et a la cascade de repli (100 % de disponibilite).",
        "<b>Architecture modulaire</b> et evolutive, fondee sur des standards eprouves.",
        "<b>Plateforme complete</b> integrant consultation, conversation et administration.",
        "<b>Souverainete des donnees</b> : hebergement local possible, cout d'exploitation quasi nul.",
        "<b>Espace d'administration riche</b> couvrant l'ensemble des contenus et la moderation.",
    ])

    el.append(section("Limites actuelles"))
    el += bullets([
        "La FAQ administrable alimente une base dediee mais n'est pas encore synchronisee en temps "
        "reel avec le modele NLP du chatbot (prevue en evolution).",
        "L'authentification concerne pour l'instant l'administration ; l'espace etudiant personnel "
        "(notes, dossier) reste a developper.",
        "Le mode avance depend d'un service externe (Groq) ; le repli local assure la continuite mais "
        "avec des reponses moins riches.",
        "Le corpus darija, bien que consequent (461 patterns), gagnerait a etre etendu par "
        "l'apprentissage continu a partir des questions reelles.",
    ])

    el.append(section("Difficultes rencontrees et solutions"))
    el.append(para(
        "Le projet a impose la resolution de plusieurs problemes techniques concrets, dont la "
        "resolution constitue en soi un apprentissage d'ingenierie."))
    el += table([
        ["Difficulte", "Solution apportee"],
        ["Conflits de ports sous Windows (processus residuels WSL)", "Exclusion de plages de ports + migration vers 8001/8002 + scripts de nettoyage"],
        ["Incoherence de configuration entre scripts et proxy", "Alignement complet des ports et generation .env coherente"],
        ["Dependances d'authentification absentes du Python d'execution", "Installation ciblee dans l'interpreteur reellement utilise"],
        ["Encodage des fichiers .env (BOM) illisible", "Ecriture en UTF-8 sans BOM"],
        ["Hallucinations potentielles du modele de langage", "Encadrement par RAG sur une base verifiee"],
        ["Risque d'indisponibilite du fournisseur d'IA", "Cascade de repli a trois niveaux"],
    ], "Principales difficultes et solutions", col_widths=[4.2, 5.8], font=8.4)

    el.append(section("Apports personnels et competences acquises"))
    el.append(para(
        "Ce projet a constitue une experience d'ingenierie complete et formatrice. Sur le plan "
        "technique, il nous a permis de maitriser un ecosysteme moderne et coherent : developpement "
        "full-stack (Angular et FastAPI), conception de bases de donnees relationnelles et NoSQL, "
        "traitement automatique du langage et integration de grands modeles de langage, securite "
        "applicative et architecture distribuee. Sur le plan methodologique, il nous a confrontes a "
        "la conduite d'un projet de bout en bout : analyse d'un besoin reel, conception, "
        "implementation iterative, tests et resolution de problemes concrets sous contrainte."))
    el.append(para(
        "Au-dela des competences techniques, ce travail collaboratif a renforce notre capacite a "
        "communiquer, a repartir les responsabilites et a integrer les retours pour ameliorer "
        "continuellement le produit."))

    el.append(section("Considerations ethiques"))
    el.append(para(
        "Le deploiement d'un assistant intelligent souleve des questions ethiques que nous avons "
        "prises en compte. La <b>fiabilite</b> est privilegiee a la creativite afin de ne pas induire "
        "les etudiants en erreur sur des informations administratives sensibles. La <b>protection des "
        "donnees</b> est assuree par la minimisation des informations collectees et l'absence de "
        "donnees personnelles sensibles dans les conversations. Enfin, l'assistant reste cantonne a "
        "son perimetre academique et ne se substitue jamais a un accompagnement humain pour les "
        "situations delicates, vers lesquelles il oriente avec bienveillance."))

    el.append(section("Analyse des risques"))
    el += table([
        ["Risque", "Probabilite", "Impact", "Mitigation"],
        ["Indisponibilite du service IA externe", "Moyenne", "Faible", "Repli local automatique"],
        ["Montee en charge imprevue", "Faible", "Moyen", "Services sans etat, scalables"],
        ["Donnees obsoletes", "Moyenne", "Moyen", "Administration simple et autonome"],
        ["Reponse inexacte du chatbot", "Faible", "Moyen", "RAG + seuil de confiance + feedback"],
    ], "Matrice d'analyse des risques", col_widths=[3.2, 1.8, 1.5, 3.5], font=8.4)
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch14():
    el = chapter("Perspectives d'Evolution")
    el.append(para(
        "La plateforme realisee constitue une base solide et extensible. Plusieurs axes d'evolution, "
        "naturellement induits par l'architecture retenue, permettraient d'en accroitre encore la "
        "valeur."))

    el.append(section("Application mobile"))
    el.append(para(
        "Les services exposant deja des API REST, le developpement d'une application mobile native "
        "(Flutter ou React Native) consommant ces memes API constituerait une extension directe, "
        "rapprochant l'assistant des usages quotidiens des etudiants."))

    el.append(section("Intelligence artificielle avancee"))
    el += bullets([
        "Synchronisation automatique de la FAQ administrable avec le modele NLP (apprentissage continu).",
        "Affinage (fine-tuning) d'un modele open source sur le corpus FSBM, notamment en darija.",
        "Recherche semantique par embeddings vectoriels pour un RAG encore plus precis.",
        "Reconnaissance et synthese vocales pour un assistant accessible a l'oral.",
    ])

    el.append(section("Industrialisation : cloud et CI/CD"))
    el.append(para(
        "Une chaine d'integration et de deploiement continus (CI/CD) automatiserait les tests et les "
        "mises en production. La conteneurisation (Docker) et l'orchestration (Kubernetes) "
        "permettraient un deploiement cloud elastique, avec supervision et journalisation centralisees."))

    el.append(section("Integration a l'environnement numerique de travail"))
    el.append(para(
        "A terme, l'integration a l'environnement numerique de travail (ENT) de l'universite et aux "
        "systemes d'information de scolarite (authentification unique, acces au dossier etudiant, "
        "notes, attestations) ferait de la plateforme un veritable portail intelligent unifie. "
        "L'extension du multilinguisme (amazigh, espagnol) et l'ouverture a d'autres etablissements "
        "de l'UH2C complèteraient cette vision."))

    el.append(section("Vision a long terme"))
    el.append(para(
        "A terme, la plateforme a vocation a devenir le point d'entree numerique unique de la "
        "communaute de la FSBM : un portail intelligent ou chaque etudiant, des sa premiere "
        "candidature jusqu'a l'obtention de son diplome, trouve un accompagnement personnalise. "
        "L'assistant pourrait anticiper les besoins (rappels d'echeances, alertes d'examens), "
        "recommander des parcours en fonction du profil, et federer l'ensemble des services "
        "numeriques de la faculte. Generalisee aux autres etablissements de l'Universite Hassan II, "
        "une telle solution participerait pleinement a la strategie nationale de transformation "
        "numerique de l'enseignement superieur, tout en preservant la souverainete des donnees et "
        "l'inclusion linguistique chere a notre demarche."))

    el.append(section("Feuille de route synthetique"))
    el += table([
        ["Horizon", "Evolutions"],
        ["Court terme", "Synchronisation FAQ/NLP, rate limiting, HTTPS, espace etudiant"],
        ["Moyen terme", "Application mobile, embeddings, CI/CD, conteneurisation"],
        ["Long terme", "Integration ENT, authentification unique, fine-tuning darija, multi-etablissements"],
    ], "Feuille de route des evolutions", col_widths=[2.0, 8.0])
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _conclusion():
    el = front_chapter("Conclusion Generale")
    el.append(para(
        "Ce projet de fin d'etudes avait pour ambition de concevoir et de realiser une plateforme "
        "universitaire intelligente repondant a un besoin concret de la Faculte des Sciences Ben "
        "M'Sick : faciliter l'acces des etudiants a l'information academique et administrative, tout "
        "en allegeant la charge du personnel. L'objectif a ete atteint a travers un assistant "
        "conversationnel multilingue, fiable et disponible en permanence, integre au sein d'une "
        "plateforme complete de consultation et d'administration."))
    el.append(para(
        "Sur le plan technique, la solution mobilise un ensemble coherent de technologies modernes : "
        "une architecture micro-services associant un frontend Angular 17 et des services FastAPI "
        "asynchrones, une persistance polyglotte combinant MySQL et MongoDB, un moteur de "
        "comprehension du langage fonde sur TF-IDF, et un mode avance exploitant le grand modele de "
        "langage LLaMA 3 via une architecture RAG encadree par une cascade de repli. La prise en "
        "charge de la darija marocaine et le souci constant de la fiabilite constituent les "
        "principaux facteurs differenciants de notre travail."))
    el.append(para(
        "Au-dela de la realisation logicielle, ce projet aura ete une experience formatrice complete, "
        "nous confrontant a l'ensemble de la demarche d'ingenierie : analyse d'un besoin reel, etude "
        "de l'existant, conception rigoureuse, implementation, securisation, tests et resolution de "
        "problemes concrets. Il nous a permis de consolider et d'articuler des competences variees, "
        "du genie logiciel a l'intelligence artificielle, dans une perspective de service rendu a la "
        "communaute universitaire."))
    el.append(para(
        "Les perspectives ouvertes — application mobile, apprentissage continu, integration a "
        "l'environnement numerique de travail — temoignent du potentiel d'une telle plateforme a "
        "devenir un veritable portail intelligent au service de la reussite etudiante. Nous "
        "esperons que ce travail pourra contribuer, a son echelle, a la transformation numerique de "
        "la Faculte des Sciences Ben M'Sick et inspirer de futurs projets dans le meme esprit."))
    el.append(spacer(0.4))
    el.append(quote(
        "La meilleure facon de predire l'avenir est de le creer.", "Peter Drucker"))
    return el
