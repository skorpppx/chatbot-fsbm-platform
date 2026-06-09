"""PDF 3 - Backend FastAPI Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 03/10", "Backend FastAPI Complet",
           "Python + FastAPI + Async + Pydantic + SQLAlchemy",
           accent_color=HexColor('#009688'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - C'est quoi un backend ?", "3"),
    ("Chapitre 2 - C'est quoi FastAPI ?", "6"),
    ("Chapitre 3 - Async/await en Python", "10"),
    ("Chapitre 4 - Anatomie d'une route", "14"),
    ("Chapitre 5 - Pydantic et validation", "18"),
    ("Chapitre 6 - Dependency Injection", "22"),
    ("Chapitre 7 - Routers et organisation", "25"),
    ("Chapitre 8 - Lifespan et configuration", "29"),
    ("Chapitre 9 - chatbot-service decortique", "32"),
    ("Chapitre 10 - academic-service decortique", "38"),
    ("Chapitre 11 - Gestion des erreurs", "43"),
    ("Chapitre 12 - Swagger UI automatique", "46"),
    ("Chapitre 13 - Conclusion", "49"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CHAPITRE 1
story.append(Paragraph("Chapitre 1 - C'est quoi un backend ?", ST_CHAPTER))
story.append(Paragraph(
    "Le <b>backend</b> est la partie serveur d'une application : ce qui tourne dans le cloud "
    "(ou sur ton PC en mode dev) et que l'utilisateur ne voit jamais directement.",
    ST_BODY))

story.append(analogy(
    "Le backend, c'est <b>le cerveau cache du systeme</b>. Tu vois la bouche (frontend) parler, "
    "mais c'est le cerveau qui pense. Si tu coupes le backend, le frontend reste affiche mais "
    "ne peut plus rien faire d'utile."))

story.append(Paragraph("1.1 Roles du backend", ST_H1))
for x in [
    "<b>Recevoir</b> les requetes HTTP du frontend",
    "<b>Authentifier</b> l'utilisateur (qui es-tu ?)",
    "<b>Autoriser</b> (as-tu le droit ?)",
    "<b>Valider</b> les donnees recues (sont-elles correctes ?)",
    "<b>Calculer</b> la reponse (logique metier)",
    "<b>Interroger</b> les bases de donnees",
    "<b>Serializer</b> la reponse en JSON",
    "<b>Logger</b> ce qui s'est passe (debug, monitoring)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("1.2 Backend monolithe vs micro-services", ST_H1))
story.append(std_table([
    ['Critere', 'Monolithe', 'Micro-services'],
    ['Architecture', '1 grosse app', 'N petites apps'],
    ['Deploiement', 'Tout d\'un coup', 'Service par service'],
    ['Resilience', 'Si crash = tout down', 'Crash isole'],
    ['Complexite', 'Plus simple', 'Plus dur (reseau)'],
    ['Performance', 'Bon (pas de reseau)', 'Latence inter-services'],
    ['Equipes', '1 grosse equipe', 'N petites equipes'],
    ['FSBM', 'Non choisi', '6 services planifies'],
], col_widths=[3.5*cm, 5*cm, 7.5*cm]))

story.append(Paragraph("1.3 Choix du langage", ST_H1))
story.append(Paragraph(
    "Pour le backend, on aurait pu choisir :",
    ST_BODY))
for x in [
    "<b>Python</b> : choisi - syntaxe simple, ecosysteme ML/IA riche (sklearn, NLTK)",
    "Node.js : tres rapide, mais asynchronisme verbeux pour debutant",
    "Go : performant, mais courbe d'apprentissage",
    "Java : robuste, mais lourd pour un PFE",
    "PHP : datĂ©, peu adapte aux micro-services modernes",
    "Rust : ultra-rapide, mais experts seulement",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(alert_box(
    "Python a ete choisi pour 3 raisons : (1) syntaxe accessible aux debutants, "
    "(2) librairies NLP/ML deja en place (sklearn, NLTK, transformers), "
    "(3) FastAPI moderne et performant.",
    kind="tip"))
story.append(PageBreak())

# CHAPITRE 2 - FastAPI
story.append(Paragraph("Chapitre 2 - C'est quoi FastAPI ?", ST_CHAPTER))

story.append(Paragraph("2.1 Naissance et popularite", ST_H1))
story.append(Paragraph(
    "<b>FastAPI</b> est un framework Python cree en 2018 par Sebastian Ramirez (alias @tiangolo). "
    "Il a explose en popularite grace a ses 3 atouts uniques : performance + validation auto + "
    "documentation auto.",
    ST_BODY))

story.append(Paragraph("2.2 Hello World FastAPI", ST_H1))
story.append(code(
    "from fastapi import FastAPI\n"
    "\n"
    "app = FastAPI()\n"
    "\n"
    "@app.get('/')\n"
    "async def hello():\n"
    "    return {'message': 'Hello World !'}\n"
    "\n"
    "# Lancer :\n"
    "# py -m uvicorn main:app --reload\n"
    "# -> http://localhost:8000\n"
    "# -> http://localhost:8000/docs  (Swagger UI auto !)"
))

story.append(Paragraph("2.3 Trois forces uniques", ST_H1))

story.append(Paragraph("Force 1 : Performance", ST_H2))
story.append(Paragraph(
    "FastAPI est base sur Starlette (ASGI async) et Pydantic. Il est aussi rapide que "
    "Node.js et Go pour la plupart des cas. C'est l'un des frameworks Python les plus "
    "rapides au monde.",
    ST_BODY))

story.append(Paragraph("Force 2 : Validation automatique avec Pydantic", ST_H2))
story.append(code(
    "from pydantic import BaseModel, Field\n"
    "\n"
    "class ChatRequest(BaseModel):\n"
    "    message: str = Field(..., min_length=1, max_length=500)\n"
    "    session_id: str | None = None\n"
    "\n"
    "@app.post('/chat')\n"
    "async def chat(req: ChatRequest):\n"
    "    # Si l'utilisateur envoie un message vide ou > 500 chars,\n"
    "    # FastAPI rejette automatiquement avec 422\n"
    "    return {'received': req.message}"
))

story.append(Paragraph("Force 3 : Documentation Swagger automatique", ST_H2))
story.append(Paragraph(
    "FastAPI genere automatiquement une interface interactive Swagger UI sur /docs et "
    "ReDoc sur /redoc. Le jury peut tester les endpoints en direct !",
    ST_BODY))

story.append(alert_box(
    "L'URL <b>http://localhost:8001/docs</b> est l'un des grands atouts a montrer en "
    "soutenance. Le jury voit instantanement TOUS les endpoints, leurs parametres, leurs "
    "types de retour, et peut les tester en cliquant.",
    kind="key"))

story.append(Paragraph("2.4 FastAPI vs Flask vs Django", ST_H1))
story.append(std_table([
    ['Critere', 'FastAPI', 'Flask', 'Django'],
    ['Annee', '2018', '2010', '2005'],
    ['Async natif', 'OUI', 'NON', 'Partiel'],
    ['Validation', 'Pydantic native', 'Manuel', 'Forms'],
    ['Doc auto', 'OUI', 'Manuel', 'Manuel'],
    ['Use case', 'APIs modernes', 'Apps simples', 'Apps complets'],
    ['Performance', 'Tres haute', 'Moyenne', 'Moyenne'],
    ['Communaute', 'Croissante', 'Enorme', 'Enorme'],
], col_widths=[3*cm, 3.5*cm, 3*cm, 3*cm, 3.5*cm]))
story.append(PageBreak())

# CHAPITRE 3 - Async
story.append(Paragraph("Chapitre 3 - Async/await en Python", ST_CHAPTER))

story.append(Paragraph("3.1 Le probleme du I/O bloquant", ST_H1))
story.append(Paragraph(
    "Quand ton serveur fait un appel a une base de donnees ou a une API externe, l'attente "
    "peut prendre 100ms a 2 secondes. Pendant ce temps, en synchrone, le serveur ne peut "
    "rien faire d'autre.",
    ST_BODY))

story.append(code(
    "# Synchrone (bloquant)\n"
    "def get_data():\n"
    "    response = requests.get('https://api.example.com')  # attend 1 seconde\n"
    "    return response.json()  # 1 seconde de blocage total\n"
    "\n"
    "# Pendant cette seconde, le serveur ne fait RIEN d'autre.\n"
    "# Si 100 utilisateurs arrivent en meme temps, ils attendent en file."
))

story.append(Paragraph("3.2 La solution async", ST_H1))
story.append(code(
    "# Asynchrone (non-bloquant)\n"
    "async def get_data():\n"
    "    response = await httpx.get('https://api.example.com')\n"
    "    return response.json()\n"
    "\n"
    "# Pendant qu'on attend la reponse externe (await),\n"
    "# Python execute D'AUTRES taches concurrentes."
))

story.append(analogy(
    "Imagine un serveur de restaurant. <b>Synchrone</b> : il prend la commande du table 1, va "
    "en cuisine, attend, ramene, puis seulement apres s'occupe de la table 2. <b>Async</b> : "
    "il prend la commande de la table 1, donne au cuisinier, va prendre la commande de la "
    "table 2, etc. Il revient quand un plat est pret."))

story.append(Paragraph("3.3 Les 3 mots-cles", ST_H1))
story.append(std_table([
    ['Mot-cle', 'Role'],
    ['async', 'Declare une fonction comme asynchrone'],
    ['await', 'Attend le resultat sans bloquer'],
    ['asyncio', 'Bibliotheque standard pour gerer l\'event loop'],
], col_widths=[3*cm, 13*cm]))

story.append(Paragraph("3.4 Exemple dans notre projet", ST_H1))
story.append(code(
    "@router.get('/api/professors')\n"
    "async def list_professors(\n"
    "    department_id: int | None = None,\n"
    "    page: int = 1,\n"
    "    page_size: int = 20,\n"
    "    db: AsyncSession = Depends(get_db),\n"
    "):\n"
    "    # Construction de la requete\n"
    "    stmt = select(Professor)\n"
    "    if department_id:\n"
    "        stmt = stmt.where(Professor.department_id == department_id)\n"
    "    \n"
    "    # await : attend le resultat sans bloquer\n"
    "    total = await db.scalar(select(func.count(Professor.id)))\n"
    "    \n"
    "    # await : execute la requete asynchrone\n"
    "    result = await db.execute(stmt.limit(page_size))\n"
    "    profs = result.scalars().all()\n"
    "    \n"
    "    return PaginatedResponse(items=profs, total=total)"
))

story.append(Paragraph("3.5 ASGI vs WSGI", ST_H1))
story.append(Paragraph(
    "WSGI (1999) est l'ancien protocole synchrone Python pour servir HTTP (Flask, Django). "
    "ASGI (2018) est l'evolution asynchrone (FastAPI, Starlette, Django 3+).",
    ST_BODY))
story.append(Paragraph(
    "On utilise <b>uvicorn</b> comme serveur ASGI pour heberger FastAPI :",
    ST_BODY))
story.append(code("py -m uvicorn app.main:app --reload --port 8001"))
story.append(PageBreak())

# CHAPITRE 4 - Anatomie route
story.append(Paragraph("Chapitre 4 - Anatomie d'une route", ST_CHAPTER))

story.append(Paragraph("4.1 Le decorateur", ST_H1))
story.append(code(
    "@app.get('/api/health')             # methode HTTP + URL\n"
    "@app.post('/api/chat')\n"
    "@app.put('/api/users/{id}')         # parametre d'URL\n"
    "@app.delete('/api/items/{id}')\n"
    "@app.patch('/api/users/{id}')"
))

story.append(Paragraph("4.2 Parametres de chemin (path)", ST_H1))
story.append(code(
    "@app.get('/api/filieres/{code}')\n"
    "async def get_filiere(code: str):\n"
    "    # code est extrait de l'URL : /api/filieres/SMI -> code = 'SMI'\n"
    "    return await find_by_code(code)\n"
    "\n"
    "@app.get('/api/students/{id}')\n"
    "async def get_student(id: int):  # type int -> conversion auto\n"
    "    return await find_by_id(id)\n"
    "    # GET /api/students/abc -> 422 (pas un int)"
))

story.append(Paragraph("4.3 Parametres de query string", ST_H1))
story.append(code(
    "@app.get('/api/filieres')\n"
    "async def list_filieres(\n"
    "    type: str | None = None,         # ?type=MASTER\n"
    "    department_id: int | None = None, # ?department_id=1\n"
    "    search: str | None = None,        # ?search=info\n"
    "    is_active: bool = True,           # ?is_active=true\n"
    "):\n"
    "    # Tous ces params viennent de l'URL :\n"
    "    # GET /api/filieres?type=MASTER&search=info&is_active=true\n"
    "    ..."
))

story.append(Paragraph("4.4 Body JSON (POST/PUT)", ST_H1))
story.append(code(
    "class ChatRequest(BaseModel):\n"
    "    message: str = Field(..., min_length=1, max_length=500)\n"
    "    session_id: str | None = None\n"
    "    temperature: float = 0.7\n"
    "\n"
    "@app.post('/api/chat')\n"
    "async def chat(req: ChatRequest):\n"
    "    # FastAPI desinitialise auto le body JSON en ChatRequest\n"
    "    # Validation auto : si message > 500 chars, 422\n"
    "    return await process_chat(req.message)"
))

story.append(Paragraph("4.5 Headers", ST_H1))
story.append(code(
    "from fastapi import Header\n"
    "\n"
    "@app.get('/api/me')\n"
    "async def get_me(\n"
    "    authorization: str | None = Header(None),  # X-Authorization header\n"
    "    accept_language: str = Header('fr'),\n"
    "):\n"
    "    if not authorization:\n"
    "        raise HTTPException(401, 'Non authentifie')\n"
    "    user = decode_jwt(authorization.replace('Bearer ', ''))\n"
    "    return user"
))

story.append(Paragraph("4.6 Reponse typee", ST_H1))
story.append(code(
    "class FiliereOut(BaseModel):\n"
    "    id: int\n"
    "    code: str\n"
    "    name: str\n"
    "    type: str\n"
    "\n"
    "@app.get('/api/filieres/{code}', response_model=FiliereOut)\n"
    "async def get_filiere(code: str):\n"
    "    f = await db.find_by_code(code)\n"
    "    if not f:\n"
    "        raise HTTPException(404, 'Filiere introuvable')\n"
    "    return f  # serialise automatiquement en JSON"
))
story.append(PageBreak())

# CHAPITRE 5 - Pydantic
story.append(Paragraph("Chapitre 5 - Pydantic et validation", ST_CHAPTER))

story.append(Paragraph("5.1 Le probleme de la validation", ST_H1))
story.append(Paragraph(
    "Sans validation, ton serveur peut recevoir n'importe quoi (string au lieu d'int, "
    "champs manquants, chaines trop longues...). Tu dois ecrire des kilometres de checks.",
    ST_BODY))

story.append(Paragraph("5.2 Pydantic en 1 minute", ST_H1))
story.append(code(
    "from pydantic import BaseModel, Field, EmailStr\n"
    "\n"
    "class StudentCreate(BaseModel):\n"
    "    cne: str = Field(..., min_length=10, max_length=10)\n"
    "    first_name: str = Field(..., min_length=2, max_length=80)\n"
    "    last_name: str = Field(..., min_length=2, max_length=80)\n"
    "    email: EmailStr                        # validation email auto\n"
    "    age: int = Field(..., ge=17, le=80)    # entre 17 et 80\n"
    "    gender: str = Field(..., pattern='^(M|F)$')  # regex"
))

story.append(Paragraph("5.3 Validation automatique", ST_H1))
story.append(Paragraph(
    "Quand FastAPI recoit cette requete :",
    ST_BODY))
story.append(code(
    "POST /api/students\n"
    "{\n"
    "  \"cne\": \"123\",            # trop court !\n"
    "  \"first_name\": \"K\",       # trop court !\n"
    "  \"email\": \"pas-un-email\", # invalide !\n"
    "  \"age\": 200,              # hors range !\n"
    "  \"gender\": \"X\"            # mauvais pattern !\n"
    "}"
))
story.append(Paragraph(
    "FastAPI repond automatiquement avec 422 et un detail des erreurs :",
    ST_BODY))
story.append(code(
    "{\n"
    "  \"detail\": [\n"
    "    {\n"
    "      \"loc\": [\"body\", \"cne\"],\n"
    "      \"msg\": \"String should have at least 10 characters\",\n"
    "      \"type\": \"string_too_short\"\n"
    "    },\n"
    "    {\n"
    "      \"loc\": [\"body\", \"email\"],\n"
    "      \"msg\": \"value is not a valid email address\",\n"
    "      \"type\": \"value_error.email\"\n"
    "    }\n"
    "  ]\n"
    "}"
))
story.append(Paragraph(
    "Zero ligne de code de validation dans notre route ! Tout est dans le schema Pydantic.",
    ST_BODY))

story.append(Paragraph("5.4 Validateurs custom", ST_H1))
story.append(code(
    "from pydantic import field_validator\n"
    "\n"
    "class ChatRequest(BaseModel):\n"
    "    message: str\n"
    "    \n"
    "    @field_validator('message')\n"
    "    @classmethod\n"
    "    def no_spam(cls, v: str) -> str:\n"
    "        if 'spam' in v.lower():\n"
    "            raise ValueError('Le mot spam est interdit')\n"
    "        return v.strip()  # transforme et retourne"
))

story.append(Paragraph("5.5 Settings (Pydantic Settings)", ST_H1))
story.append(Paragraph(
    "Pour la configuration depuis le fichier .env, on utilise pydantic-settings :",
    ST_BODY))
story.append(code(
    "from pydantic_settings import BaseSettings, SettingsConfigDict\n"
    "\n"
    "class Settings(BaseSettings):\n"
    "    service_name: str = 'chatbot-service'\n"
    "    service_port: int = 8001\n"
    "    db_host: str = 'localhost'\n"
    "    db_password: str = ''\n"
    "    groq_api_key: str = ''\n"
    "    \n"
    "    model_config = SettingsConfigDict(\n"
    "        env_file='.env',\n"
    "        env_file_encoding='utf-8',\n"
    "        case_sensitive=False,\n"
    "        extra='ignore',\n"
    "    )\n"
    "\n"
    "settings = Settings()  # charge .env automatiquement\n"
    "print(settings.db_password)  # 'monpassword' lu depuis .env"
))
story.append(PageBreak())

# CHAPITRE 6 - DI
story.append(Paragraph("Chapitre 6 - Dependency Injection", ST_CHAPTER))

story.append(Paragraph("6.1 Le concept", ST_H1))
story.append(Paragraph(
    "<b>DI = Dependency Injection</b>. Au lieu que chaque route cree ses propres dependances "
    "(connexion DB, auth, etc.), FastAPI les <b>injecte</b> automatiquement.",
    ST_BODY))

story.append(analogy(
    "Au lieu que chaque cuisinier fabrique sa propre poele (chronophage et duplique), il y a "
    "un magasinier qui distribue les poeles. Le cuisinier dit 'j'ai besoin d'une poele' et "
    "la recoit automatiquement."))

story.append(Paragraph("6.2 Depends() en action", ST_H1))
story.append(code(
    "from fastapi import Depends\n"
    "from sqlalchemy.ext.asyncio import AsyncSession\n"
    "\n"
    "# Definition de la dependance\n"
    "async def get_db() -> AsyncSession:\n"
    "    async with SessionLocal() as session:\n"
    "        yield session\n"
    "        # apres le yield : cleanup automatique a la fin de la requete\n"
    "\n"
    "# Utilisation dans une route\n"
    "@router.get('/api/filieres')\n"
    "async def list_filieres(db: AsyncSession = Depends(get_db)):\n"
    "    # FastAPI appelle get_db(), recupere la session, la passe en parametre\n"
    "    result = await db.execute(select(Filiere))\n"
    "    return result.scalars().all()\n"
    "    # Apres la requete : get_db() reprend la main pour fermer la session"
))

story.append(Paragraph("6.3 Avantages", ST_H1))
for x in [
    "<b>Reusabilite</b> : la meme dependance dans 50 routes",
    "<b>Testabilite</b> : on peut remplacer get_db par un mock",
    "<b>Composition</b> : une dependance peut utiliser une autre",
    "<b>Lifecycle automatique</b> : creation/destruction geres pour toi",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("6.4 Dependance avec dependances", ST_H1))
story.append(code(
    "async def get_token(authorization: str = Header(None)):\n"
    "    if not authorization:\n"
    "        raise HTTPException(401, 'Token manquant')\n"
    "    return authorization.replace('Bearer ', '')\n"
    "\n"
    "async def get_current_user(\n"
    "    token: str = Depends(get_token),\n"
    "    db: AsyncSession = Depends(get_db),\n"
    "):\n"
    "    user_id = decode_jwt(token)\n"
    "    user = await db.get(User, user_id)\n"
    "    if not user:\n"
    "        raise HTTPException(401, 'User introuvable')\n"
    "    return user\n"
    "\n"
    "@router.get('/api/me')\n"
    "async def me(user: User = Depends(get_current_user)):\n"
    "    return user"
))
story.append(PageBreak())

# CHAPITRE 7 - Routers
story.append(Paragraph("Chapitre 7 - Routers et organisation", ST_CHAPTER))

story.append(Paragraph("7.1 Pourquoi des routers ?", ST_H1))
story.append(Paragraph(
    "Quand on a 30+ routes, on les regroupe par thematique dans des <b>routers</b>. "
    "C'est plus organise et modulaire.",
    ST_BODY))

story.append(Paragraph("7.2 Structure de notre chatbot-service", ST_H1))
story.append(code(
    "app/\n"
    "  main.py             # Bootstrap, include les routers\n"
    "  routers/\n"
    "    chat.py           # POST /api/chat, /api/chat/feedback\n"
    "    llm.py            # POST /api/llm/chat, GET /api/llm/status\n"
    "    intents.py        # GET /api/intents\n"
    "    system.py         # GET /api/health, /api/stats"
))

story.append(Paragraph("7.3 Definition d'un router", ST_H1))
story.append(code(
    "# routers/chat.py\n"
    "from fastapi import APIRouter, Depends\n"
    "\n"
    "router = APIRouter(\n"
    "    prefix='/api/chat',    # toutes les routes commencent par /api/chat\n"
    "    tags=['chat'],          # groupe dans Swagger UI\n"
    ")\n"
    "\n"
    "@router.post('', response_model=ChatResponse)\n"
    "async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):\n"
    "    ...\n"
    "\n"
    "@router.post('/feedback')\n"
    "async def feedback(req: FeedbackRequest):\n"
    "    ...\n"
    "\n"
    "@router.get('/history/{session_id}')\n"
    "async def history(session_id: str):\n"
    "    ..."
))

story.append(Paragraph("7.4 Inclure les routers dans main.py", ST_H1))
story.append(code(
    "# main.py\n"
    "from app.routers.chat import router as chat_router\n"
    "from app.routers.llm import router as llm_router\n"
    "from app.routers.system import router as system_router\n"
    "\n"
    "app = FastAPI(title='FSBM Chatbot Service')\n"
    "\n"
    "app.include_router(chat_router)\n"
    "app.include_router(llm_router)\n"
    "app.include_router(system_router)"
))

story.append(Paragraph("7.5 Tags = groupes dans Swagger", ST_H1))
story.append(Paragraph(
    "Les tags affichent un regroupement visuel sur /docs. Si tu as 30 endpoints, c'est "
    "essentiel pour la lisibilite.",
    ST_BODY))
story.append(PageBreak())

# CHAPITRE 8 - Lifespan
story.append(Paragraph("Chapitre 8 - Lifespan et configuration", ST_CHAPTER))

story.append(Paragraph("8.1 Le concept de lifespan", ST_H1))
story.append(Paragraph(
    "Le <b>lifespan</b> est une fonction qui s'execute au demarrage ET a l'arret de "
    "l'application. C'est la qu'on initialise les ressources couteuses (NLP, DB pool, "
    "configuration).",
    ST_BODY))

story.append(Paragraph("8.2 Code du lifespan FSBM", ST_H1))
story.append(code(
    "from contextlib import asynccontextmanager\n"
    "\n"
    "@asynccontextmanager\n"
    "async def lifespan(app: FastAPI):\n"
    "    # ─── DEMARRAGE ───\n"
    "    print('Demarrage du chatbot-service')\n"
    "    \n"
    "    # Charger le classifier NLP\n"
    "    classifier = IntentClassifier()\n"
    "    if not classifier.load_model():\n"
    "        classifier.train()\n"
    "    set_classifier(classifier)\n"
    "    \n"
    "    # Configurer le LLM Service\n"
    "    llm_svc = LLMService(classifier=classifier, ...)\n"
    "    set_llm_service(llm_svc)\n"
    "    \n"
    "    print('Service pret')\n"
    "    yield  # APP TOURNE ICI\n"
    "    \n"
    "    # ─── ARRET ───\n"
    "    print('Arret du chatbot-service')\n"
    "    # Cleanup (fermeture connexions, etc.)\n"
    "\n"
    "app = FastAPI(lifespan=lifespan)"
))

story.append(Paragraph("8.3 Configuration via Settings", ST_H1))
story.append(Paragraph(
    "Le fichier .env contient les vraies valeurs (mot de passe, cle API). Pydantic Settings "
    "les charge au demarrage :",
    ST_BODY))
story.append(code(
    ".env :\n"
    "GROQ_API_KEY=gsk_xxx\n"
    "DB_PASSWORD=monpassword\n"
    "DB_NAME=fsbm_db\n"
    "\n"
    "config.py :\n"
    "class Settings(BaseSettings):\n"
    "    groq_api_key: str = ''\n"
    "    db_password: str = ''\n"
    "    db_name: str = 'fsbm_db'\n"
    "    \n"
    "    model_config = SettingsConfigDict(env_file='.env')\n"
    "\n"
    "# Au demarrage :\n"
    "settings = Settings()\n"
    "# settings.groq_api_key = 'gsk_xxx' (lu depuis .env)"
))

story.append(Paragraph("8.4 CORS Middleware", ST_H1))
story.append(Paragraph(
    "<b>CORS = Cross-Origin Resource Sharing</b>. Par defaut, le navigateur bloque les requetes "
    "entre domaines differents (security). Le backend doit autoriser explicitement le frontend.",
    ST_BODY))
story.append(code(
    "from fastapi.middleware.cors import CORSMiddleware\n"
    "\n"
    "app.add_middleware(\n"
    "    CORSMiddleware,\n"
    "    allow_origins=['http://localhost:4200'],  # frontend Angular\n"
    "    allow_credentials=True,\n"
    "    allow_methods=['*'],   # GET, POST, PUT, DELETE...\n"
    "    allow_headers=['*'],\n"
    ")"
))
story.append(PageBreak())

# CHAPITRE 9 - chatbot-service
story.append(Paragraph("Chapitre 9 - chatbot-service decortique", ST_CHAPTER))

story.append(Paragraph("9.1 Vue d'ensemble", ST_H1))
story.append(code(
    "chatbot-service/\n"
    "  app/\n"
    "    main.py                    # bootstrap FastAPI + lifespan\n"
    "    core/\n"
    "      config.py                # Pydantic Settings\n"
    "      database.py              # session SQLAlchemy MySQL\n"
    "      memory.py                # memoire conversationnelle RAM\n"
    "      persona.py               # detection genre/nom\n"
    "      web_fetcher.py           # scraping fsbm.ma + Facebook\n"
    "    nlp/\n"
    "      preprocessor.py          # tokenisation + stopwords\n"
    "      language_detector.py     # FR/EN/Darija\n"
    "      classifier.py            # TF-IDF + Cosine multi-langue\n"
    "    llm/\n"
    "      groq_client.py           # client Groq (LLaMA 3.3)\n"
    "      hf_client.py             # client HuggingFace (fallback)\n"
    "      rag.py                   # retrieval + prompt building\n"
    "      llm_service.py           # orchestrateur avec fallback\n"
    "    models/\n"
    "      schemas.py               # Pydantic v2 schemas\n"
    "    routers/\n"
    "      chat.py                  # /api/chat, /feedback, /history\n"
    "      llm.py                   # /api/llm/chat, /status\n"
    "      intents.py               # /api/intents\n"
    "      system.py                # /api/health, /api/stats\n"
    "  data/\n"
    "    faq_dataset.json           # 28 intents trilingues\n"
    "    model.pkl                  # modele TF-IDF entraine"
))

story.append(Paragraph("9.2 Endpoint /api/chat detaille", ST_H1))
story.append(code(
    "@router.post('', response_model=ChatResponse)\n"
    "async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):\n"
    "    # 1. Validation deja faite par Pydantic\n"
    "    classifier = get_classifier()\n"
    "    session_id = req.session_id or f'sess_{uuid.uuid4().hex}'\n"
    "    \n"
    "    # 2. Memoire conversationnelle\n"
    "    ctx = memory.get_or_create(session_id, req.user_id)\n"
    "    \n"
    "    # 3. Detection genre/nom\n"
    "    g = detect_gender(req.message)\n"
    "    n = detect_name(req.message)\n"
    "    if g: ctx.user_context['gender'] = g\n"
    "    if n: ctx.user_context['name'] = n\n"
    "    \n"
    "    # 4. Prediction NLP\n"
    "    result = classifier.predict(\n"
    "        req.message, top_k=5,\n"
    "        forced_language=req.language\n"
    "    )\n"
    "    \n"
    "    # 5. Personnalisation\n"
    "    response_text = personalize_response(\n"
    "        result['response'],\n"
    "        gender=ctx.user_context.get('gender'),\n"
    "        name=ctx.user_context.get('name'),\n"
    "        lang=result['language'],\n"
    "    )\n"
    "    \n"
    "    # 6. Persistance MySQL\n"
    "    conv_id = await save_conversation(db, ...)\n"
    "    \n"
    "    # 7. Memory enrichie\n"
    "    memory.add_turn(session_id, req.message, response_text, ...)\n"
    "    \n"
    "    # 8. Reponse JSON\n"
    "    return ChatResponse(\n"
    "        response=response_text,\n"
    "        intent=result['intent'],\n"
    "        confidence=result['confidence'],\n"
    "        conversation_id=conv_id,\n"
    "        ...\n"
    "    )"
))
story.append(PageBreak())

# CHAPITRE 10 - academic-service
story.append(Paragraph("Chapitre 10 - academic-service decortique", ST_CHAPTER))

story.append(Paragraph("10.1 Vue d'ensemble", ST_H1))
story.append(code(
    "academic-service/\n"
    "  app/\n"
    "    main.py                # bootstrap FastAPI\n"
    "    core/\n"
    "      config.py            # settings .env\n"
    "    db/\n"
    "      session.py           # engine + sessionmaker SQLAlchemy async\n"
    "    models/\n"
    "      entities.py          # 15 modeles ORM mappes MySQL\n"
    "    schemas/\n"
    "      academic.py          # 30+ schemas Pydantic\n"
    "    routers/\n"
    "      departments.py       # /api/departments\n"
    "      filieres.py          # /api/filieres + filtres + /code/SMI\n"
    "      modules.py           # /api/modules\n"
    "      professors.py        # /api/professors (paginé)\n"
    "      students.py          # /api/students (paginé)\n"
    "      schedule.py          # /api/schedule\n"
    "      exams.py             # /api/exams\n"
    "      announcements.py     # /api/announcements + events + clubs\n"
    "      system.py            # /health, /overview"
))

story.append(Paragraph("10.2 Endpoint /api/filieres avec filtres", ST_H1))
story.append(code(
    "@router.get('', response_model=list[FiliereOut])\n"
    "async def list_filieres(\n"
    "    type: str | None = Query(None),\n"
    "    department_id: int | None = Query(None),\n"
    "    is_active: bool = Query(True),\n"
    "    search: str | None = Query(None),\n"
    "    db: AsyncSession = Depends(get_db),\n"
    "):\n"
    "    # Construction dynamique de la query\n"
    "    stmt = select(Filiere)\n"
    "    if type:\n"
    "        stmt = stmt.where(Filiere.type == type)\n"
    "    if department_id:\n"
    "        stmt = stmt.where(Filiere.department_id == department_id)\n"
    "    if is_active is not None:\n"
    "        stmt = stmt.where(Filiere.is_active == is_active)\n"
    "    if search:\n"
    "        like = f'%{search}%'\n"
    "        stmt = stmt.where(or_(\n"
    "            Filiere.name.like(like),\n"
    "            Filiere.code.like(like)\n"
    "        ))\n"
    "    stmt = stmt.order_by(Filiere.type, Filiere.name)\n"
    "    \n"
    "    result = await db.execute(stmt)\n"
    "    return result.scalars().all()"
))

story.append(Paragraph("10.3 Endpoint /api/overview (dashboard)", ST_H1))
story.append(code(
    "@router.get('/overview')\n"
    "async def overview(db: AsyncSession = Depends(get_db)):\n"
    "    # 8 requetes count() en parallele (async)\n"
    "    dept_count    = await db.scalar(select(func.count(Department.id))) or 0\n"
    "    filiere_count = await db.scalar(select(func.count(Filiere.id))) or 0\n"
    "    module_count  = await db.scalar(select(func.count(Module.id))) or 0\n"
    "    prof_count    = await db.scalar(select(func.count(Professor.id))) or 0\n"
    "    student_count = await db.scalar(select(func.count(Student.id))) or 0\n"
    "    event_count   = await db.scalar(select(func.count(Event.id))) or 0\n"
    "    ann_count     = await db.scalar(select(func.count(Announcement.id))) or 0\n"
    "    club_count    = await db.scalar(select(func.count(Club.id))) or 0\n"
    "    \n"
    "    # Repartition par type\n"
    "    type_counts = (await db.execute(\n"
    "        select(Filiere.type, func.count(Filiere.id))\n"
    "        .group_by(Filiere.type)\n"
    "    )).all()\n"
    "    \n"
    "    return {\n"
    "        'departments':    dept_count,\n"
    "        'filieres':       filiere_count,\n"
    "        'modules':        module_count,\n"
    "        'professors':     prof_count,\n"
    "        'students':       student_count,\n"
    "        'events':         event_count,\n"
    "        'announcements':  ann_count,\n"
    "        'clubs':          club_count,\n"
    "        'filieres_by_type': {t: c for t, c in type_counts},\n"
    "    }"
))
story.append(PageBreak())

# CHAPITRE 11 - Erreurs
story.append(Paragraph("Chapitre 11 - Gestion des erreurs", ST_CHAPTER))

story.append(Paragraph("11.1 HTTPException", ST_H1))
story.append(code(
    "from fastapi import HTTPException\n"
    "\n"
    "@router.get('/api/filieres/{id}')\n"
    "async def get_filiere(id: int, db: AsyncSession = Depends(get_db)):\n"
    "    f = await db.get(Filiere, id)\n"
    "    if not f:\n"
    "        raise HTTPException(\n"
    "            status_code=404,\n"
    "            detail=f'Filiere {id} non trouvee'\n"
    "        )\n"
    "    return f"
))

story.append(Paragraph("11.2 Codes HTTP a utiliser", ST_H1))
story.append(std_table([
    ['Code', 'Quand l\'utiliser'],
    ['400', 'Bad Request (mauvais format, params invalides)'],
    ['401', 'Unauthorized (pas de token, token expire)'],
    ['403', 'Forbidden (token OK mais pas les droits)'],
    ['404', 'Not Found (ressource introuvable)'],
    ['409', 'Conflict (ex: email deja utilise)'],
    ['422', 'Unprocessable Entity (validation echouee - auto par FastAPI)'],
    ['429', 'Too Many Requests (rate limit)'],
    ['500', 'Internal Server Error (bug serveur, log et returne)'],
], col_widths=[1.5*cm, 14.5*cm]))

story.append(Paragraph("11.3 Exception handler global", ST_H1))
story.append(code(
    "from fastapi import Request\n"
    "from fastapi.responses import JSONResponse\n"
    "\n"
    "@app.exception_handler(ValueError)\n"
    "async def value_error_handler(request: Request, exc: ValueError):\n"
    "    return JSONResponse(\n"
    "        status_code=400,\n"
    "        content={'detail': str(exc)}\n"
    "    )\n"
    "\n"
    "# Toutes les ValueError du code seront converties en 400 automatiquement"
))

story.append(Paragraph("11.4 Try/except dans les routes", ST_H1))
story.append(code(
    "@router.post('/api/chat')\n"
    "async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):\n"
    "    try:\n"
    "        result = classifier.predict(req.message)\n"
    "    except Exception as exc:\n"
    "        # Log + remontee\n"
    "        logger.error(f'NLP error: {exc}')\n"
    "        raise HTTPException(500, f'Erreur NLP: {exc}')\n"
    "    \n"
    "    # Persistance tolerante : si MySQL down, on continue\n"
    "    try:\n"
    "        conv_id = await save_conversation(db, ...)\n"
    "    except Exception:\n"
    "        conv_id = 0  # mode degrade\n"
    "    \n"
    "    return ChatResponse(..., conversation_id=conv_id)"
))
story.append(PageBreak())

# CHAPITRE 12 - Swagger
story.append(Paragraph("Chapitre 12 - Swagger UI automatique", ST_CHAPTER))

story.append(Paragraph("12.1 C'est quoi Swagger ?", ST_H1))
story.append(Paragraph(
    "<b>Swagger UI</b> (aussi appele OpenAPI) est une <b>interface web interactive</b> qui "
    "documente automatiquement ton API. Tu peux tester chaque endpoint en cliquant.",
    ST_BODY))

story.append(Paragraph("12.2 Comment y acceder", ST_H1))
story.append(Paragraph(
    "Une fois ton service FastAPI lance :",
    ST_BODY))
for x in [
    "<b>http://localhost:8001/docs</b> - Swagger UI (interface interactive)",
    "<b>http://localhost:8001/redoc</b> - ReDoc (documentation plus belle, non-interactive)",
    "<b>http://localhost:8001/openapi.json</b> - le schema OpenAPI en JSON",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("12.3 Ce qu'on voit sur /docs", ST_H1))
for x in [
    "La liste de TOUS les endpoints groupes par <b>tag</b>",
    "Pour chaque endpoint : methode, URL, description",
    "Schemas Pydantic des bodies (request + response)",
    "Bouton <b>Try it out</b> pour tester en direct",
    "Generation automatique de la commande curl",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("12.4 Ameliorer la doc", ST_H1))
story.append(code(
    "@router.post(\n"
    "    '/chat',\n"
    "    response_model=ChatResponse,\n"
    "    summary='Envoyer un message au chatbot',\n"
    "    description='''\n"
    "    Le chatbot detecte la langue (FR/EN/Darija), classifie l'intent,\n"
    "    genere une reponse personnalisee. Memoire 10 tours.\n"
    "    ''',\n"
    "    tags=['chat'],\n"
    ")\n"
    "async def chat(req: ChatRequest):\n"
    "    ..."
))

story.append(Paragraph("12.5 Exemples dans le schema", ST_H1))
story.append(code(
    "class ChatRequest(BaseModel):\n"
    "    model_config = ConfigDict(json_schema_extra={\n"
    "        'example': {\n"
    "            'message': 'Comment m_inscrire en master IADS ?',\n"
    "            'session_id': 'sess_abc123',\n"
    "        }\n"
    "    })\n"
    "    \n"
    "    message: str = Field(..., min_length=1, max_length=500)\n"
    "    session_id: str | None = None"
))

story.append(alert_box(
    "L'exemple apparait dans Swagger UI. L'utilisateur peut cliquer 'Use example' pour "
    "pre-remplir le body de test. Tres pratique pour la demo soutenance.",
    kind="tip"))
story.append(PageBreak())

# CHAPITRE 13 - Conclusion
story.append(Paragraph("Chapitre 13 - Conclusion", ST_CHAPTER))

story.append(Paragraph("13.1 Recap des concepts", ST_H1))
for x in [
    "FastAPI = framework Python async pour APIs REST",
    "Routes = endpoints avec decorateurs @router.get/post/...",
    "Pydantic = validation automatique des inputs",
    "Async/await = non-bloquant pour de meilleures perfs",
    "Depends() = injection de dependances",
    "Routers = organisation modulaire des endpoints",
    "Lifespan = init/cleanup au demarrage/arret",
    "Swagger UI = documentation automatique interactive",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("13.2 Pour aller plus loin", ST_H1))
for x in [
    "PDF 04 - pour comprendre comment FastAPI parle a MySQL via SQLAlchemy",
    "PDF 05 - pour MongoDB avec Motor (driver async)",
    "PDF 06 - pour le pipeline NLP/IA derriere le chatbot",
    "PDF 07 - pour la communication detaillee front/back et inter-services",
    "PDF 08 - pour la securite (JWT, bcrypt, etc.)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Spacer(1, 1*cm))
story.append(alert_box(
    "Maitriser FastAPI te donne acces aux meilleures pratiques Python modernes. C'est un "
    "skill tres valorise sur le marche (Microsoft, Netflix, Uber l'utilisent).",
    kind="tip"))

build_doc("03_Backend_FastAPI_Complet.pdf", story,
          "PDF 03 - Backend FastAPI",
          "FSBM Platform - Backend FastAPI Complet")
