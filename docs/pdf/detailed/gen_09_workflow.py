"""PDF 9 - Workflow Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 09/10", "Workflow Complet",
           "Du clic utilisateur au rendu final - Pas a pas",
           accent_color=HexColor('#10B981'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - Vue d'ensemble du workflow", "3"),
    ("Chapitre 2 - Etape 1 : L'utilisateur tape", "6"),
    ("Chapitre 3 - Etape 2 : Angular capture", "9"),
    ("Chapitre 4 - Etape 3 : HTTP request part", "13"),
    ("Chapitre 5 - Etape 4 : Proxy redirige", "16"),
    ("Chapitre 6 - Etape 5 : FastAPI recoit", "19"),
    ("Chapitre 7 - Etape 6 : Pydantic valide", "23"),
    ("Chapitre 8 - Etape 7 : Service traite", "26"),
    ("Chapitre 9 - Etape 8 : NLP analyse", "30"),
    ("Chapitre 10 - Etape 9 : SQL/Mongo persiste", "34"),
    ("Chapitre 11 - Etape 10 : Reponse JSON", "37"),
    ("Chapitre 12 - Etape 11 : Angular recoit", "40"),
    ("Chapitre 13 - Etape 12 : DOM se met a jour", "43"),
    ("Chapitre 14 - Cas particulier : LLM/RAG", "46"),
    ("Chapitre 15 - Conclusion", "50"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1
story.append(Paragraph("Chapitre 1 - Vue d'ensemble du workflow", ST_CHAPTER))

story.append(Paragraph("1.1 Le scenario", ST_H1))
story.append(Paragraph(
    "On va suivre une requete <b>de bout en bout</b>. Scenario : un etudiant tape "
    "'Quelles sont les filieres ?' dans le chatbot et voit la reponse.",
    ST_BODY))

story.append(Paragraph("1.2 Les 12 etapes", ST_H1))
story.append(diagram(
    "  [1]  User tape dans textarea\n"
    "        |\n"
    "        v\n"
    "  [2]  Angular event handler (sendMessage)\n"
    "        |\n"
    "        v\n"
    "  [3]  HttpClient envoie POST /api/chat\n"
    "        |\n"
    "        v\n"
    "  [4]  proxy.conf.json redirige vers :8001\n"
    "        |\n"
    "        v\n"
    "  [5]  FastAPI route match POST /api/chat\n"
    "        |\n"
    "        v\n"
    "  [6]  Pydantic valide ChatRequest\n"
    "        |\n"
    "        v\n"
    "  [7]  Service ChatbotService.process()\n"
    "        |\n"
    "        v\n"
    "  [8]  NLP : langue, intent, confidence\n"
    "        |\n"
    "        v\n"
    "  [9]  MySQL log conversation, MongoDB session\n"
    "        |\n"
    "        v\n"
    "  [10] FastAPI serialise ChatResponse JSON\n"
    "        |\n"
    "        v\n"
    "  [11] Angular HttpClient resout l'observable\n"
    "        |\n"
    "        v\n"
    "  [12] Change detection -> DOM update -> User voit"
))

story.append(Paragraph("1.3 Latence totale", ST_H1))
story.append(std_table([
    ['Etape', 'Temps approx', 'Pct'],
    ['1-3 (Angular -> reseau)', '~10 ms', '5%'],
    ['4 (proxy)', '~2 ms', '1%'],
    ['5-6 (FastAPI + Pydantic)', '~5 ms', '2%'],
    ['7-8 (NLP TF-IDF)', '~30 ms', '15%'],
    ['9 (MySQL insert)', '~15 ms', '7%'],
    ['9 (MongoDB upsert)', '~10 ms', '5%'],
    ['10 (serialise JSON)', '~3 ms', '1%'],
    ['11-12 (parse + DOM)', '~5 ms', '2%'],
    ['Reseau aller-retour', '~120 ms', '60%'],
    ['<b>Total moyen</b>', '<b>~200 ms</b>', '100%'],
], col_widths=[6*cm, 4*cm, 3*cm]))
story.append(PageBreak())

# CH 2
story.append(Paragraph("Chapitre 2 - Etape 1 : L'utilisateur tape", ST_CHAPTER))

story.append(Paragraph("2.1 Element HTML", ST_H1))
story.append(code(
    "<!-- chat-window.component.html -->\n"
    "<textarea\n"
    "  [(ngModel)]=\"currentMessage\"\n"
    "  (keydown)=\"onKeyDown($event)\"\n"
    "  placeholder=\"Pose ta question...\"\n"
    "  [disabled]=\"isTyping()\"\n"
    "  rows=\"1\"\n"
    "></textarea>\n"
    "\n"
    "<button\n"
    "  (click)=\"sendMessage()\"\n"
    "  [disabled]=\"!currentMessage.trim() || isTyping()\"\n"
    ">\n"
    "  Envoyer\n"
    "</button>"
))

story.append(Paragraph("2.2 Ce qui se passe quand l'user tape une lettre", ST_H1))
for n, d in [
    ("Browser detect keydown",
     "Le navigateur capte l'evenement clavier."),
    ("Angular zone.js intercepte",
     "Zone.js patche les APIs natives. Detecte le changement."),
    ("ngModel two-way binding",
     "currentMessage est mis a jour."),
    ("Bouton se reactive",
     "[disabled]='!currentMessage.trim()' devient false. Bouton activable."),
    ("Change detection",
     "Angular re-evalue les bindings et met a jour le DOM si besoin."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("2.3 Capture de la touche Entree", ST_H1))
story.append(code(
    "// chat-window.component.ts\n"
    "onKeyDown(event: KeyboardEvent) {\n"
    "  if (event.key === 'Enter' && !event.shiftKey) {\n"
    "    event.preventDefault();  // empeche le retour ligne\n"
    "    this.sendMessage();\n"
    "  }\n"
    "  // Shift+Enter = newline (laisse passer)\n"
    "}"
))
story.append(PageBreak())

# CH 3
story.append(Paragraph("Chapitre 3 - Etape 2 : Angular capture", ST_CHAPTER))

story.append(Paragraph("3.1 Methode sendMessage()", ST_H1))
story.append(code(
    "// chat-window.component.ts\n"
    "sendMessage(): void {\n"
    "  const text = this.currentMessage.trim();\n"
    "  if (!text || this.isTyping()) return;\n"
    "  \n"
    "  // 1. Ajouter message user dans le state local\n"
    "  this.messages.update(msgs => [...msgs, {\n"
    "    sender: 'user',\n"
    "    text,\n"
    "    timestamp: new Date()\n"
    "  }]);\n"
    "  \n"
    "  // 2. Vider la textarea\n"
    "  this.currentMessage = '';\n"
    "  \n"
    "  // 3. Afficher l'indicateur 'is typing'\n"
    "  this.isTyping.set(true);\n"
    "  \n"
    "  // 4. Choisir entre TF-IDF et LLM\n"
    "  const useLLM = this.llmMode();\n"
    "  const call$ = useLLM\n"
    "    ? this.chat.sendMessageLLM(text, this.sessionId)\n"
    "    : this.chat.sendMessage(text, this.sessionId);\n"
    "  \n"
    "  // 5. Souscrire\n"
    "  call$.subscribe({\n"
    "    next: (res) => this.handleResponse(res),\n"
    "    error: (err) => this.handleError(err),\n"
    "    complete: () => this.isTyping.set(false)\n"
    "  });\n"
    "}"
))

story.append(Paragraph("3.2 Service ChatService", ST_H1))
story.append(code(
    "// services/chat.service.ts\n"
    "@Injectable({ providedIn: 'root' })\n"
    "export class ChatService {\n"
    "  constructor(private http: HttpClient) {}\n"
    "  \n"
    "  sendMessage(message: string, sessionId: string): Observable<ChatResponse> {\n"
    "    return this.http.post<ChatResponse>('/api/chat', {\n"
    "      message,\n"
    "      session_id: sessionId\n"
    "    });\n"
    "  }\n"
    "  \n"
    "  sendMessageLLM(message: string, sessionId: string): Observable<LLMResponse> {\n"
    "    return this.http.post<LLMResponse>('/api/llm/chat', {\n"
    "      message,\n"
    "      session_id: sessionId,\n"
    "      temperature: 0.6\n"
    "    });\n"
    "  }\n"
    "}"
))
story.append(PageBreak())

# CH 4
story.append(Paragraph("Chapitre 4 - Etape 3 : HTTP request part", ST_CHAPTER))

story.append(Paragraph("4.1 Sous le capot d'HttpClient", ST_H1))
story.append(Paragraph(
    "<b>HttpClient</b> retourne un Observable RxJS. Il ne fait <b>RIEN</b> tant qu'on ne "
    "souscrit pas. Au subscribe :",
    ST_BODY))
for n, d in [
    ("Construction de la requete",
     "Methode, URL, headers, body JSON serialise."),
    ("Interceptors",
     "Si configures (ex: ajouter Authorization). Pas en Phase 1."),
    ("Appel a fetch() ou XMLHttpRequest",
     "Bas niveau. Le navigateur envoie sur le reseau."),
    ("DNS resolution",
     "localhost = 127.0.0.1 (resolu instantanement)."),
    ("TCP handshake",
     "3-way handshake avec le serveur. Quelques ms."),
    ("Envoi HTTP request",
     "Le navigateur envoie les bytes."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("4.2 La requete bytes finale", ST_H1))
story.append(code(
    "POST /api/chat HTTP/1.1\n"
    "Host: localhost:4200\n"
    "Connection: keep-alive\n"
    "Content-Type: application/json\n"
    "Content-Length: 71\n"
    "Accept: application/json, text/plain, */*\n"
    "User-Agent: Mozilla/5.0...\n"
    "Origin: http://localhost:4200\n"
    "Referer: http://localhost:4200/chatbot\n"
    "\n"
    "{\"message\":\"Quelles sont les filieres ?\",\"session_id\":\"sess_abc123\"}"
))
story.append(PageBreak())

# CH 5
story.append(Paragraph("Chapitre 5 - Etape 4 : Proxy redirige", ST_CHAPTER))

story.append(Paragraph("5.1 Le serveur dev Angular intercepte", ST_H1))
story.append(Paragraph(
    "Le serveur Angular tourne sur :4200. Il a charge proxy.conf.json. Il inspecte l'URL "
    "de chaque requete.",
    ST_BODY))

story.append(Paragraph("5.2 Match du path", ST_H1))
story.append(code(
    "Requete entrante : POST http://localhost:4200/api/chat\n"
    "\n"
    "proxy.conf.json :\n"
    "{\n"
    "  '/api/chat': {\n"
    "    'target': 'http://localhost:8001',\n"
    "    'secure': false,\n"
    "    'changeOrigin': true\n"
    "  }\n"
    "}\n"
    "\n"
    "Match ! /api/chat -> :8001\n"
    "\n"
    "Nouvelle URL : POST http://localhost:8001/api/chat"
))

story.append(Paragraph("5.3 Forwarding", ST_H1))
story.append(diagram(
    "  Browser -> Angular Dev Server (:4200)\n"
    "  Angular Dev Server -> Backend FastAPI (:8001)\n"
    "  Backend repond -> Angular Dev Server (:4200)\n"
    "  Angular Dev Server -> Browser\n"
    "\n"
    "  Le browser pense qu'il parle a :4200\n"
    "  Pas de CORS car proxy = same origin"
))
story.append(PageBreak())

# CH 6
story.append(Paragraph("Chapitre 6 - Etape 5 : FastAPI recoit", ST_CHAPTER))

story.append(Paragraph("6.1 Uvicorn ecoute :8001", ST_H1))
story.append(Paragraph(
    "<b>Uvicorn</b> = serveur ASGI qui execute FastAPI. Il ecoute sur le port 8001 et passe "
    "chaque requete a l'app FastAPI.",
    ST_BODY))

story.append(Paragraph("6.2 Routing FastAPI", ST_H1))
story.append(code(
    "# main.py\n"
    "app = FastAPI(title='Chatbot Service')\n"
    "app.include_router(chat_router, prefix='/api', tags=['chat'])\n"
    "\n"
    "# routers/chat.py\n"
    "@router.post('/chat', response_model=ChatResponse)\n"
    "async def chat(\n"
    "    req: ChatRequest,\n"
    "    db: AsyncSession = Depends(get_db),\n"
    "    mongo = Depends(get_mongo)\n"
    "):\n"
    "    ..."
))

story.append(Paragraph("6.3 Le routeur fait", ST_H1))
for n, d in [
    ("Resolution du chemin",
     "POST /api/chat -> trouve la fonction `chat`."),
    ("Resolution des dependances",
     "Depends(get_db) instancie une session SQLAlchemy. Depends(get_mongo) injecte le client Mongo."),
    ("Parse du body",
     "FastAPI lit le body, le convertit en dict Python."),
    ("Validation Pydantic",
     "Cree un ChatRequest a partir du dict. Si invalide -> 422."),
    ("Appel async de la fonction",
     "await chat(req, db, mongo)."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))
story.append(PageBreak())

# CH 7
story.append(Paragraph("Chapitre 7 - Etape 6 : Pydantic valide", ST_CHAPTER))

story.append(Paragraph("7.1 Le modele ChatRequest", ST_H1))
story.append(code(
    "from pydantic import BaseModel, Field\n"
    "\n"
    "class ChatRequest(BaseModel):\n"
    "    message: str = Field(..., min_length=1, max_length=2000)\n"
    "    session_id: str | None = None\n"
    "    user_id: int | None = None\n"
    "    language: str | None = None"
))

story.append(Paragraph("7.2 Que verifie Pydantic", ST_H1))
for x in [
    "<b>Types</b> : message doit etre une string",
    "<b>Required</b> : message obligatoire (Field(...))",
    "<b>Lengths</b> : 1 <= len(message) <= 2000",
    "<b>Optionnels</b> : session_id, user_id, language peuvent etre null",
    "<b>Extra</b> : par defaut, ignore les champs non definis",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("7.3 Si validation echoue", ST_H1))
story.append(code(
    "Input invalide : { \"message\": \"\" }  (vide)\n"
    "\n"
    "Reponse automatique :\n"
    "HTTP 422 Unprocessable Entity\n"
    "Content-Type: application/json\n"
    "\n"
    "{\n"
    "  \"detail\": [\n"
    "    {\n"
    "      \"type\": \"string_too_short\",\n"
    "      \"loc\": [\"body\", \"message\"],\n"
    "      \"msg\": \"String should have at least 1 character\",\n"
    "      \"input\": \"\",\n"
    "      \"ctx\": { \"min_length\": 1 }\n"
    "    }\n"
    "  ]\n"
    "}"
))

story.append(alert_box(
    "<b>Sans Pydantic</b>, on devrait coder a la main : verifier que message existe, que c'est "
    "une string, que length > 0, etc. Pour chaque endpoint. Pydantic fait tout en 1 ligne.",
    kind="tip"))
story.append(PageBreak())

# CH 8
story.append(Paragraph("Chapitre 8 - Etape 7 : Service traite", ST_CHAPTER))

story.append(Paragraph("8.1 Architecture en couches", ST_H1))
story.append(diagram(
    "  Router (HTTP)\n"
    "      |\n"
    "      v\n"
    "  Service metier (logique)\n"
    "      |\n"
    "      v\n"
    "  NLP / Repository (donnees)"
))

story.append(Paragraph("8.2 Le service ChatbotService", ST_H1))
story.append(code(
    "# services/chatbot.py\n"
    "class ChatbotService:\n"
    "    def __init__(self, classifier, web_fetcher, persona):\n"
    "        self.classifier = classifier\n"
    "        self.web_fetcher = web_fetcher\n"
    "        self.persona = persona\n"
    "    \n"
    "    async def process(\n"
    "        self,\n"
    "        message: str,\n"
    "        session_id: str,\n"
    "        db: AsyncSession,\n"
    "        mongo,\n"
    "        forced_language: str | None = None\n"
    "    ) -> ChatResponse:\n"
    "        # 1. Detecter ou recuperer la session\n"
    "        if not session_id:\n"
    "            session_id = generate_session_id()\n"
    "        \n"
    "        # 2. NLP : langue + intent\n"
    "        result = self.classifier.classify(message, forced_language)\n"
    "        \n"
    "        # 3. Detecter genre / nom\n"
    "        gender = self.persona.detect_gender(message)\n"
    "        name = self.persona.detect_name(message)\n"
    "        \n"
    "        # 4. Personnaliser la reponse\n"
    "        response_text = self.persona.personalize(\n"
    "            result.response, gender, name, result.language\n"
    "        )\n"
    "        \n"
    "        # 5. Enrichir avec news si demande\n"
    "        news_items = []\n"
    "        if result.intent in ['actualites', 'evenements']:\n"
    "            news_items = await self.web_fetcher.fetch_news(\n"
    "                lang=result.language\n"
    "            )\n"
    "        \n"
    "        # 6. Persister en BDD\n"
    "        conversation_id = await self._save_conversation(\n"
    "            db, session_id, message, response_text, result\n"
    "        )\n"
    "        await self._save_session(mongo, session_id, ...)\n"
    "        \n"
    "        # 7. Retourner reponse\n"
    "        return ChatResponse(\n"
    "            response=response_text,\n"
    "            intent=result.intent,\n"
    "            confidence=result.confidence,\n"
    "            session_id=session_id,\n"
    "            language=result.language,\n"
    "            conversation_id=conversation_id,\n"
    "            news_items=news_items,\n"
    "            suggestions=result.suggestions\n"
    "        )"
))
story.append(PageBreak())

# CH 9
story.append(Paragraph("Chapitre 9 - Etape 8 : NLP analyse", ST_CHAPTER))

story.append(Paragraph("9.1 Detection de langue", ST_H1))
story.append(code(
    "# language_detector.py\n"
    "def detect(self, text: str) -> tuple[str, float]:\n"
    "    # 1. Hint script arabe -> darija\n"
    "    if re.search(r'[\\u0600-\\u06FF]', text):\n"
    "        return ('darija', 1.0)\n"
    "    \n"
    "    # 2. Hint numerique darija (3, 7, 9)\n"
    "    if re.search(r'\\b\\w*[379]\\w*\\b', text):\n"
    "        return ('darija', 0.9)\n"
    "    \n"
    "    # 3. Compte mots-cles FR vs EN vs Darija\n"
    "    text_lower = text.lower()\n"
    "    scores = {\n"
    "        'fr': sum(1 for k in FR_KEYWORDS if k in text_lower),\n"
    "        'en': sum(1 for k in EN_KEYWORDS if k in text_lower),\n"
    "        'darija': sum(1 for k in DARIJA_KEYWORDS if k in text_lower),\n"
    "    }\n"
    "    \n"
    "    # 4. Le max gagne\n"
    "    best = max(scores, key=scores.get)\n"
    "    total = sum(scores.values()) or 1\n"
    "    confidence = scores[best] / total\n"
    "    return (best, confidence)"
))

story.append(Paragraph("9.2 Classification d'intent", ST_H1))
story.append(code(
    "# classifier.py\n"
    "def classify(self, text: str, forced_lang=None) -> ClassResult:\n"
    "    # 1. Detecter langue\n"
    "    lang, lang_conf = self.detect(text)\n"
    "    if forced_lang:\n"
    "        lang = forced_lang\n"
    "    \n"
    "    # 2. Choisir vectorizer + matrix pour cette langue\n"
    "    vectorizer = self.vectorizers[lang]\n"
    "    pattern_matrix = self.matrices[lang]\n"
    "    intents = self.intents[lang]\n"
    "    \n"
    "    # 3. Vectoriser la question user\n"
    "    user_vec = vectorizer.transform([text.lower()])\n"
    "    \n"
    "    # 4. Cosine similarity vs TOUS les patterns\n"
    "    similarities = cosine_similarity(user_vec, pattern_matrix)[0]\n"
    "    \n"
    "    # 5. Top 3 candidats\n"
    "    top_idx = similarities.argsort()[::-1][:3]\n"
    "    \n"
    "    # 6. Best intent + sa confidence\n"
    "    best_intent = intents[top_idx[0]]\n"
    "    confidence = similarities[top_idx[0]]\n"
    "    \n"
    "    # 7. Choisir reponse aleatoire de cet intent\n"
    "    response = random.choice(best_intent.responses[lang])\n"
    "    \n"
    "    return ClassResult(\n"
    "        intent=best_intent.tag,\n"
    "        response=response,\n"
    "        confidence=confidence,\n"
    "        language=lang,\n"
    "        top_candidates=[\n"
    "            (intents[i].tag, similarities[i]) for i in top_idx\n"
    "        ]\n"
    "    )"
))
story.append(PageBreak())

# CH 10
story.append(Paragraph("Chapitre 10 - Etape 9 : SQL/Mongo persiste", ST_CHAPTER))

story.append(Paragraph("10.1 Insert dans MySQL conversations", ST_H1))
story.append(code(
    "async def _save_conversation(\n"
    "    self, db, session_id, message, response, result\n"
    ") -> int:\n"
    "    conv = Conversation(\n"
    "        session_id=session_id,\n"
    "        user_message=message,\n"
    "        bot_response=response,\n"
    "        intent_detected=result.intent,\n"
    "        confidence_score=result.confidence,\n"
    "        language=result.language,\n"
    "        response_time_ms=result.response_time_ms\n"
    "    )\n"
    "    db.add(conv)\n"
    "    await db.commit()\n"
    "    await db.refresh(conv)\n"
    "    return conv.id"
))

story.append(Paragraph("10.2 Upsert dans MongoDB sessions", ST_H1))
story.append(code(
    "async def _save_session(\n"
    "    self, mongo, session_id, message, response, result\n"
    "):\n"
    "    sessions = mongo.get_collection('sessions')\n"
    "    \n"
    "    # Append au tableau messages\n"
    "    await sessions.update_one(\n"
    "        {'session_id': session_id},\n"
    "        {\n"
    "            '$setOnInsert': {\n"
    "                'session_id': session_id,\n"
    "                'created_at': datetime.utcnow(),\n"
    "                'language': result.language\n"
    "            },\n"
    "            '$set': {\n"
    "                'updated_at': datetime.utcnow(),\n"
    "                'last_intent': result.intent\n"
    "            },\n"
    "            '$push': {\n"
    "                'messages': {\n"
    "                    'sender': 'user',\n"
    "                    'text': message,\n"
    "                    'timestamp': datetime.utcnow()\n"
    "                }\n"
    "            },\n"
    "            '$inc': { 'message_count': 1 }\n"
    "        },\n"
    "        upsert=True   # cree si pas existe\n"
    "    )"
))

story.append(Paragraph("10.3 Sous le capot SQL", ST_H1))
story.append(code(
    "INSERT INTO conversations (\n"
    "  session_id, user_message, bot_response,\n"
    "  intent_detected, confidence_score, language,\n"
    "  response_time_ms, created_at\n"
    ") VALUES (\n"
    "  ?, ?, ?, ?, ?, ?, ?, NOW()\n"
    ");\n"
    "\n"
    "-- Parametres (echappes par SQLAlchemy)\n"
    "-- ?1 = 'sess_abc123'\n"
    "-- ?2 = 'Quelles sont les filieres ?'\n"
    "-- ?3 = 'La FSBM propose 7 licences...'\n"
    "-- ?4 = 'filieres'\n"
    "-- ?5 = 1.0\n"
    "-- ?6 = 'fr'\n"
    "-- ?7 = 152"
))
story.append(PageBreak())

# CH 11
story.append(Paragraph("Chapitre 11 - Etape 10 : Reponse JSON", ST_CHAPTER))

story.append(Paragraph("11.1 ChatResponse Pydantic", ST_H1))
story.append(code(
    "class ChatResponse(BaseModel):\n"
    "    response: str\n"
    "    intent: str\n"
    "    confidence: float\n"
    "    conversation_id: int\n"
    "    session_id: str\n"
    "    language: str\n"
    "    language_confidence: float\n"
    "    top_candidates: list[dict]\n"
    "    suggestions: list[str]\n"
    "    news_items: list[dict] = []\n"
    "    response_time_ms: int"
))

story.append(Paragraph("11.2 Serialisation auto FastAPI", ST_H1))
story.append(code(
    "# Le router retourne un ChatResponse\n"
    "return ChatResponse(\n"
    "    response='La FSBM propose 7 licences...',\n"
    "    intent='filieres',\n"
    "    confidence=1.0,\n"
    "    session_id='sess_abc123',\n"
    "    ...\n"
    ")\n"
    "\n"
    "# FastAPI fait automatiquement :\n"
    "# 1. response.model_dump() -> dict\n"
    "# 2. json.dumps(dict) -> string JSON\n"
    "# 3. HTTP 200 + Content-Type: application/json\n"
    "# 4. Envoie au client"
))

story.append(Paragraph("11.3 Le JSON final envoye", ST_H1))
story.append(code(
    "HTTP/1.1 200 OK\n"
    "Content-Type: application/json\n"
    "Content-Length: 487\n"
    "Date: Wed, 28 May 2026 13:24:35 GMT\n"
    "Server: uvicorn\n"
    "\n"
    "{\n"
    "  \"response\": \"La FSBM propose 7 licences et 18 masters...\",\n"
    "  \"intent\": \"filieres\",\n"
    "  \"confidence\": 1.0,\n"
    "  \"conversation_id\": 42,\n"
    "  \"session_id\": \"sess_abc123\",\n"
    "  \"language\": \"fr\",\n"
    "  \"language_confidence\": 1.0,\n"
    "  \"top_candidates\": [\n"
    "    {\"intent\": \"filieres\", \"score\": 1.0},\n"
    "    {\"intent\": \"masters\", \"score\": 0.65},\n"
    "    {\"intent\": \"licences\", \"score\": 0.45}\n"
    "  ],\n"
    "  \"suggestions\": [\"Master IADS\", \"Licence SMI\"],\n"
    "  \"news_items\": [],\n"
    "  \"response_time_ms\": 152\n"
    "}"
))
story.append(PageBreak())

# CH 12
story.append(Paragraph("Chapitre 12 - Etape 11 : Angular recoit", ST_CHAPTER))

story.append(Paragraph("12.1 Le browser recoit les bytes", ST_H1))
for n, d in [
    ("TCP recoit les bytes",
     "Reassemble les paquets en ordre."),
    ("HTTP parse headers + body",
     "Sapare headers et body."),
    ("Decodage UTF-8",
     "Les bytes deviennent une string."),
    ("JSON.parse",
     "La string devient un objet JavaScript."),
    ("Observable resout",
     "RxJS emet le 'next' avec la reponse."),
    ("Subscribe handler appele",
     "Notre subscribe({ next: ... }) est invoque."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("12.2 handleResponse", ST_H1))
story.append(code(
    "handleResponse(res: ChatResponse): void {\n"
    "  // 1. Ajouter message bot dans le state\n"
    "  this.messages.update(msgs => [...msgs, {\n"
    "    sender: 'bot',\n"
    "    text: res.response,\n"
    "    timestamp: new Date(),\n"
    "    intent: res.intent,\n"
    "    confidence: res.confidence,\n"
    "    newsItems: res.news_items\n"
    "  }]);\n"
    "  \n"
    "  // 2. Mettre a jour suggestions\n"
    "  this.suggestions.set(res.suggestions);\n"
    "  \n"
    "  // 3. Memoriser conv_id pour feedback\n"
    "  this.lastConversationId = res.conversation_id;\n"
    "  \n"
    "  // 4. Cacher l'indicateur 'typing'\n"
    "  this.isTyping.set(false);\n"
    "  \n"
    "  // 5. Scroller vers le bas\n"
    "  setTimeout(() => this.scrollToBottom(), 50);\n"
    "}"
))
story.append(PageBreak())

# CH 13
story.append(Paragraph("Chapitre 13 - Etape 12 : DOM se met a jour", ST_CHAPTER))

story.append(Paragraph("13.1 Change Detection", ST_H1))
story.append(Paragraph(
    "Angular utilise <b>OnPush + Signals</b> dans notre projet. Quand on appelle "
    "<code>this.messages.update(...)</code>, le signal notifie tous les abonnes.",
    ST_BODY))

story.append(Paragraph("13.2 Le template re-render", ST_H1))
story.append(code(
    "<!-- chat-window.component.html -->\n"
    "<div class=\"messages\">\n"
    "  @for (msg of messages(); track $index) {\n"
    "    <div [class]=\"'message ' + msg.sender\">\n"
    "      <div class=\"avatar\">\n"
    "        @if (msg.sender === 'bot') { Bot } @else { User }\n"
    "      </div>\n"
    "      <div class=\"text\">{{ msg.text }}</div>\n"
    "      \n"
    "      @if (msg.newsItems?.length) {\n"
    "        <div class=\"news-items\">\n"
    "          @for (n of msg.newsItems; track n.url) {\n"
    "            <a [href]=\"n.url\" target=\"_blank\">{{ n.title }}</a>\n"
    "          }\n"
    "        </div>\n"
    "      }\n"
    "    </div>\n"
    "  }\n"
    "</div>"
))

story.append(Paragraph("13.3 Le rendu visuel", ST_H1))
for n, d in [
    ("Angular detecte signal update",
     "Marque le composant comme 'dirty'."),
    ("Angular re-execute le template",
     "Genere une nouvelle representation virtuelle (VDOM-like)."),
    ("Diff avec DOM actuel",
     "Trouve les differences."),
    ("Patch le DOM",
     "Applique seulement les diffs. Ajoute le nouveau message."),
    ("Browser repaint",
     "Le navigateur re-dessine la zone modifiee."),
    ("L'user voit le nouveau message",
     "Tout cela en <16 ms (60 FPS)."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))
story.append(PageBreak())

# CH 14 - LLM/RAG
story.append(Paragraph("Chapitre 14 - Cas particulier : LLM/RAG", ST_CHAPTER))

story.append(Paragraph("14.1 Quand l'user active LLM mode", ST_H1))
story.append(Paragraph(
    "Le workflow change a partir de l'etape 7. Au lieu du ChatbotService, on appelle "
    "LLMService.",
    ST_BODY))

story.append(Paragraph("14.2 Nouveau workflow LLM", ST_H1))
story.append(diagram(
    "  Service LLMService.chat()\n"
    "      |\n"
    "      v\n"
    "  1. Detecter langue (comme avant)\n"
    "      |\n"
    "      v\n"
    "  2. RAG retrieval :\n"
    "     classifier.get_top_k(message, k=3)\n"
    "     -> Top 3 intents + leurs reponses\n"
    "      |\n"
    "      v\n"
    "  3. Build prompt :\n"
    "     SYSTEM + history + CONTEXTES + question\n"
    "      |\n"
    "      v\n"
    "  4. Try Groq (LLaMA 3.3-70B)\n"
    "     - Send messages array\n"
    "     - Wait 100-300 ms\n"
    "     - Recoit completion\n"
    "      |\n"
    "      v\n"
    "  5. Fallback si Groq down :\n"
    "     - Try HuggingFace\n"
    "     - Si HF down : retour TF-IDF\n"
    "      |\n"
    "      v\n"
    "  6. Personnaliser (genre/nom)\n"
    "      |\n"
    "      v\n"
    "  7. Persister + retourner LLMResponse"
))

story.append(Paragraph("14.3 Le prompt envoye a Groq", ST_H1))
story.append(code(
    "messages = [\n"
    "  {\n"
    "    'role': 'system',\n"
    "    'content': \"\"\"Tu es l'assistant officiel de la Faculte des Sciences\n"
    "Ben M'Sick (FSBM), Universite Hassan II Casablanca.\n"
    "Tu reponds en francais de maniere claire et bienveillante.\n"
    "Tu utilises EXCLUSIVEMENT les informations du contexte ci-dessous.\n"
    "Si tu ne sais pas, dis-le.\"\"\"\n"
    "  },\n"
    "  {\n"
    "    'role': 'system',\n"
    "    'content': \"\"\"## CONTEXTES PERTINENTS\n"
    "    \n"
    "[CONTEXTE 1] (intent: master_iads, score: 0.91)\n"
    "Le Master IADS - IA et Data Science - dure 2 ans, capacite 25 places.\n"
    "Public vise : titulaires de licence informatique ou maths.\n"
    "Modules : Machine Learning, Deep Learning, NLP, Computer Vision...\n"
    "Coordinateur : Pr. Mehdi FILALI (m.filali@fsbm.ac.ma).\n"
    "\n"
    "[CONTEXTE 2] (intent: masters, score: 0.45)\n"
    "La FSBM propose 18 masters repartis en 4 departements...\"\"\"\n"
    "  },\n"
    "  # Historique conversation\n"
    "  {'role': 'user', 'content': 'Salut'},\n"
    "  {'role': 'assistant', 'content': 'Bonjour ! Comment puis-je aider ?'},\n"
    "  # Question actuelle\n"
    "  {'role': 'user', 'content': 'Conditions pour le master IADS ?'}\n"
    "]\n"
    "\n"
    "Total : ~800 tokens (input)\n"
    "Reponse attendue : ~200 tokens"
))

story.append(Paragraph("14.4 Reponse Groq", ST_H1))
story.append(code(
    "POST https://api.groq.com/openai/v1/chat/completions\n"
    "Authorization: Bearer gsk_xxx\n"
    "Content-Type: application/json\n"
    "\n"
    "{\n"
    "  \"model\": \"llama-3.3-70b-versatile\",\n"
    "  \"messages\": [...]  // comme ci-dessus,\n"
    "  \"temperature\": 0.6,\n"
    "  \"max_tokens\": 800\n"
    "}\n"
    "\n"
    "Reponse :\n"
    "{\n"
    "  \"choices\": [{\n"
    "    \"message\": {\n"
    "      \"role\": \"assistant\",\n"
    "      \"content\": \"Pour le master IADS, vous devez avoir une licence...\"\n"
    "    }\n"
    "  }],\n"
    "  \"usage\": {\n"
    "    \"prompt_tokens\": 812,\n"
    "    \"completion_tokens\": 187,\n"
    "    \"total_tokens\": 999\n"
    "  }\n"
    "}"
))

story.append(alert_box(
    "LLaMA 3.3-70B genere sa reponse en se basant SUR LES CONTEXTES (RAG). Sans RAG, le "
    "modele invente. Avec RAG, il reformule de maniere naturelle des infos fiables.",
    kind="success"))
story.append(PageBreak())

# CH 15 - Conclusion
story.append(Paragraph("Chapitre 15 - Conclusion", ST_CHAPTER))

story.append(Paragraph("15.1 Le voyage complet", ST_H1))
story.append(Paragraph(
    "On a suivi une requete de bout en bout. Sur ~200 ms :",
    ST_BODY))
for x in [
    "60% en transit reseau (TCP + HTTP)",
    "15% en NLP TF-IDF (vectorisation + cosine)",
    "12% en persistence MySQL + MongoDB",
    "5% en frontend (Angular + DOM)",
    "8% en autres (proxy, FastAPI, Pydantic)",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("15.2 Couches traversees", ST_H1))
story.append(std_table([
    ['Couche', 'Role'],
    ['Browser DOM', 'Capture input + render output'],
    ['Angular', 'Etat, binding, composants'],
    ['HttpClient + RxJS', 'Requete reseau, observable'],
    ['Proxy Dev', 'CORS bypass, routing'],
    ['Uvicorn', 'Serveur ASGI'],
    ['FastAPI', 'Router, dependency injection'],
    ['Pydantic', 'Validation des inputs'],
    ['Service metier', 'Orchestration'],
    ['NLP TF-IDF', 'Classification d\'intent'],
    ['LLM optionnel', 'Generation naturelle'],
    ['SQLAlchemy', 'ORM async MySQL'],
    ['Motor', 'Client async MongoDB'],
], col_widths=[5*cm, 11*cm]))

story.append(Paragraph("15.3 Cle de comprehension", ST_H1))
story.append(Paragraph(
    "<b>Chaque couche a une responsabilite claire.</b> Angular ne sait rien de MySQL. "
    "FastAPI ne sait rien d'Angular. NLP ne sait rien du reseau. Ce decouplage permet de "
    "modifier une couche sans impacter les autres.",
    ST_BODY))

story.append(Paragraph("15.4 Pour aller plus loin", ST_H1))
for x in [
    "PDF 02 - frontend Angular en detail",
    "PDF 03 - backend FastAPI",
    "PDF 06 - NLP et IA",
    "PDF 07 - APIs et endpoints",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("09_Workflow_Complet.pdf", story,
          "PDF 09 - Workflow Complet",
          "FSBM Platform - Workflow Complet")
