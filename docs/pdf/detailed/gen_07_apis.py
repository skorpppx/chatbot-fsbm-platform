"""PDF 7 - APIs + Communication Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 07/10", "APIs et Communication",
           "REST + HTTP + JSON + Endpoints + Inter-services",
           accent_color=HexColor('#FF6B35'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - C'est quoi HTTP ?", "3"),
    ("Chapitre 2 - Les methodes HTTP", "6"),
    ("Chapitre 3 - Les codes de statut", "9"),
    ("Chapitre 4 - Headers HTTP", "12"),
    ("Chapitre 5 - JSON en details", "15"),
    ("Chapitre 6 - REST : principes", "18"),
    ("Chapitre 7 - Endpoints du chatbot-service", "21"),
    ("Chapitre 8 - Endpoints de l'academic-service", "26"),
    ("Chapitre 9 - Endpoints LLM", "31"),
    ("Chapitre 10 - Communication inter-services", "34"),
    ("Chapitre 11 - Proxy Angular (proxy.conf.json)", "37"),
    ("Chapitre 12 - Swagger/OpenAPI", "40"),
    ("Chapitre 13 - Tester les APIs", "43"),
    ("Chapitre 14 - Conclusion", "46"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1 - HTTP
story.append(Paragraph("Chapitre 1 - C'est quoi HTTP ?", ST_CHAPTER))

story.append(Paragraph("1.1 Definition", ST_H1))
story.append(Paragraph(
    "<b>HTTP = HyperText Transfer Protocol</b>. C'est le <b>langage</b> que parlent les "
    "navigateurs et serveurs web depuis 1991. Chaque fois que tu visites un site web, ton "
    "navigateur fait une (ou plusieurs) requete HTTP.",
    ST_BODY))

story.append(analogy(
    "HTTP est comme la <b>langue parlee</b> dans un magasin. Le client (navigateur) parle au "
    "vendeur (serveur) selon une grammaire stricte : 'Bonjour, je voudrais X, voici mon ID...' "
    "Le serveur repond pareil : 'Voici X, ca coute Y, merci'."))

story.append(Paragraph("1.2 Caracteristiques cles", ST_H1))
for x in [
    "<b>Stateless</b> : chaque requete est independante (pas de memoire)",
    "<b>Client-serveur</b> : le client demande, le serveur repond",
    "<b>Request-Response</b> : pas de communication initiee par le serveur",
    "<b>Texte</b> : protocole texte (lisible), mais peut transporter du binaire",
    "<b>Sur TCP</b> : utilise le protocole TCP/IP",
    "<b>HTTPS</b> : version chiffree (TLS/SSL), securise",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("1.3 Anatomie d'une requete HTTP", ST_H1))
story.append(code(
    "POST /api/chat HTTP/1.1\n"
    "Host: localhost:8001\n"
    "Content-Type: application/json\n"
    "Authorization: Bearer eyJ0eXAiOiJKV1Qi...\n"
    "User-Agent: Mozilla/5.0 (Windows NT 10.0) Chrome/120.0\n"
    "\n"
    "{\n"
    "  \"message\": \"Quelles sont les filieres ?\",\n"
    "  \"session_id\": \"sess_abc123\"\n"
    "}"
))
story.append(Paragraph(
    "<b>Structure :</b>",
    ST_BODY))
for x in [
    "<b>Premiere ligne</b> : methode + URL + version protocole",
    "<b>Headers</b> : metadonnees (type contenu, auth, etc.)",
    "<b>Ligne vide</b> : separe headers et body",
    "<b>Body</b> : donnees envoyees (optionnel, surtout pour POST/PUT)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("1.4 Anatomie d'une reponse HTTP", ST_H1))
story.append(code(
    "HTTP/1.1 200 OK\n"
    "Content-Type: application/json\n"
    "Content-Length: 245\n"
    "Date: Wed, 28 May 2026 13:24:35 GMT\n"
    "\n"
    "{\n"
    "  \"response\": \"La FSBM propose 7 licences...\",\n"
    "  \"intent\": \"filieres\",\n"
    "  \"confidence\": 1.0,\n"
    "  \"session_id\": \"sess_abc123\"\n"
    "}"
))
story.append(PageBreak())

# CH 2 - Methodes
story.append(Paragraph("Chapitre 2 - Les methodes HTTP", ST_CHAPTER))

story.append(Paragraph("2.1 Les 5 principales", ST_H1))
story.append(std_table([
    ['Methode', 'But', 'Idempotent', 'Body'],
    ['GET', 'Lire une ressource', 'Oui', 'Non'],
    ['POST', 'Creer une ressource', 'Non', 'Oui'],
    ['PUT', 'Remplacer integralement', 'Oui', 'Oui'],
    ['PATCH', 'Modifier partiellement', 'Non', 'Oui'],
    ['DELETE', 'Supprimer', 'Oui', 'Non'],
], col_widths=[2.5*cm, 6*cm, 3.5*cm, 4*cm]))

story.append(Paragraph(
    "<b>Idempotent</b> : appeler la methode plusieurs fois donne le meme resultat. "
    "GET, PUT, DELETE le sont. POST ne l'est PAS (2 POST = 2 ressources creees).",
    ST_BODY))

story.append(Paragraph("2.2 GET", ST_H1))
story.append(Paragraph(
    "Pour lire des donnees. <b>Pas de body</b>, les parametres sont dans l'URL.",
    ST_BODY))
story.append(code(
    "# Lecture simple\n"
    "GET /api/filieres\n"
    "\n"
    "# Avec filtres en query string\n"
    "GET /api/filieres?type=MASTER&search=info\n"
    "\n"
    "# Avec parametre de chemin\n"
    "GET /api/filieres/SMI\n"
    "\n"
    "# En Angular\n"
    "this.http.get<Filiere[]>('/api/filieres');"
))

story.append(Paragraph("2.3 POST", ST_H1))
story.append(Paragraph(
    "Pour creer ou pour declencher une action complexe. <b>Body JSON</b> contient les donnees.",
    ST_BODY))
story.append(code(
    "POST /api/chat\n"
    "Content-Type: application/json\n"
    "\n"
    "{\n"
    "  \"message\": \"Bonjour\",\n"
    "  \"session_id\": \"sess_abc\"\n"
    "}\n"
    "\n"
    "# En Angular\n"
    "this.http.post('/api/chat', {\n"
    "  message: 'Bonjour',\n"
    "  session_id: 'sess_abc'\n"
    "});"
))

story.append(Paragraph("2.4 PUT vs PATCH", ST_H1))
story.append(code(
    "# PUT - remplace TOUT le profil\n"
    "PUT /api/users/42\n"
    "{ \"name\": \"Karim\", \"email\": \"karim@etu.fsbm.ma\", \"age\": 21 }\n"
    "# Si on omet un champ, il est mis a defaut/null\n"
    "\n"
    "# PATCH - modifie SEULEMENT certains champs\n"
    "PATCH /api/users/42\n"
    "{ \"email\": \"new@etu.fsbm.ma\" }\n"
    "# Seul email change, le reste est intact"
))

story.append(Paragraph("2.5 DELETE", ST_H1))
story.append(code(
    "DELETE /api/messages/123\n"
    "# Pas de body, juste l'URL\n"
    "\n"
    "# En Angular\n"
    "this.http.delete('/api/messages/123');"
))
story.append(PageBreak())

# CH 3 - Codes
story.append(Paragraph("Chapitre 3 - Les codes de statut", ST_CHAPTER))

story.append(Paragraph("3.1 Les 5 categories", ST_H1))
story.append(std_table([
    ['Plage', 'Categorie', 'Signification'],
    ['1xx', 'Informationnel', 'Requete recue, traitement en cours'],
    ['2xx', 'Succes', 'Requete reussie'],
    ['3xx', 'Redirection', 'Action complementaire necessaire'],
    ['4xx', 'Erreur client', 'Le client a fait une erreur'],
    ['5xx', 'Erreur serveur', 'Le serveur a un probleme'],
], col_widths=[2*cm, 4*cm, 10*cm]))

story.append(Paragraph("3.2 Les codes essentiels", ST_H1))
story.append(std_table([
    ['Code', 'Nom', 'Quand le retourner'],
    ['200', 'OK', 'Succes general (GET, PUT, PATCH)'],
    ['201', 'Created', 'POST qui a cree une ressource'],
    ['204', 'No Content', 'Succes sans donnees (DELETE)'],
    ['301', 'Moved Permanently', 'Redirection definitive'],
    ['302', 'Found', 'Redirection temporaire'],
    ['304', 'Not Modified', 'Cache du client encore valide'],
    ['400', 'Bad Request', 'Mauvais format (JSON invalide)'],
    ['401', 'Unauthorized', 'Pas d\'auth ou token expire'],
    ['403', 'Forbidden', 'Auth OK mais pas les droits'],
    ['404', 'Not Found', 'Ressource introuvable'],
    ['409', 'Conflict', 'Ex: email deja utilise'],
    ['422', 'Unprocessable', 'Validation Pydantic echouee'],
    ['429', 'Too Many', 'Rate limit atteint'],
    ['500', 'Internal Server Error', 'Bug serveur'],
    ['502', 'Bad Gateway', 'Service en aval down'],
    ['503', 'Service Unavailable', 'Surcharge'],
], col_widths=[1.5*cm, 4*cm, 10.5*cm]))

story.append(Paragraph("3.3 Exemple en FastAPI", ST_H1))
story.append(code(
    "@router.get('/api/filieres/{code}')\n"
    "async def get_filiere(code: str, db = Depends(get_db)):\n"
    "    f = await db.find_by_code(code)\n"
    "    if not f:\n"
    "        raise HTTPException(\n"
    "            status_code=404,\n"
    "            detail=f'Filiere {code} introuvable'\n"
    "        )\n"
    "    return f  # 200 OK"
))
story.append(PageBreak())

# CH 4 - Headers
story.append(Paragraph("Chapitre 4 - Headers HTTP", ST_CHAPTER))

story.append(Paragraph("4.1 Headers de requete courants", ST_H1))
story.append(std_table([
    ['Header', 'Role', 'Exemple'],
    ['Content-Type', 'Type du body', 'application/json'],
    ['Accept', 'Type attendu en reponse', 'application/json'],
    ['Authorization', 'Token d\'auth', 'Bearer eyJ0eXAi...'],
    ['User-Agent', 'Identifie le client', 'Mozilla/5.0...'],
    ['Accept-Language', 'Langue preferee', 'fr-FR,fr;q=0.9'],
    ['Cookie', 'Cookies', 'session_id=abc...'],
    ['Origin', 'Domaine d\'origine (CORS)', 'http://localhost:4200'],
    ['Referer', 'Page d\'origine', 'http://example.com/page'],
], col_widths=[3*cm, 5*cm, 8*cm]))

story.append(Paragraph("4.2 Headers de reponse courants", ST_H1))
story.append(std_table([
    ['Header', 'Role'],
    ['Content-Type', 'Type du body retourne'],
    ['Content-Length', 'Taille du body en bytes'],
    ['Set-Cookie', 'Definir un cookie'],
    ['Cache-Control', 'Politique de cache'],
    ['Access-Control-Allow-Origin', 'CORS (autorise quel domaine)'],
    ['Location', 'Pour les redirections'],
    ['X-RateLimit-Remaining', 'Requetes restantes'],
], col_widths=[5.5*cm, 10.5*cm]))

story.append(Paragraph("4.3 CORS expliqué", ST_H1))
story.append(Paragraph(
    "<b>CORS = Cross-Origin Resource Sharing</b>. Par defaut, le navigateur empeche un site "
    "(localhost:4200) de faire des requetes vers un autre (localhost:8001). C'est pour la "
    "securite. Le backend doit <b>explicitement autoriser</b> les origines.",
    ST_BODY))
story.append(code(
    "# FastAPI CORS\n"
    "from fastapi.middleware.cors import CORSMiddleware\n"
    "\n"
    "app.add_middleware(\n"
    "    CORSMiddleware,\n"
    "    allow_origins=['http://localhost:4200'],\n"
    "    allow_credentials=True,\n"
    "    allow_methods=['*'],\n"
    "    allow_headers=['*'],\n"
    ")"
))

story.append(alert_box(
    "Si tu vois 'CORS error' dans la console Angular, c'est que ton frontend n'est pas dans "
    "la whitelist du backend.",
    kind="warning"))
story.append(PageBreak())

# CH 5 - JSON
story.append(Paragraph("Chapitre 5 - JSON en details", ST_CHAPTER))

story.append(Paragraph("5.1 Qu'est-ce que JSON ?", ST_H1))
story.append(Paragraph(
    "<b>JSON = JavaScript Object Notation</b>. Format de donnees structurees, lisible par "
    "humain et facile a parser pour les machines. Standard de facto pour les APIs REST.",
    ST_BODY))

story.append(Paragraph("5.2 Syntaxe", ST_H1))
story.append(code(
    "{\n"
    "  \"string\": \"texte entre guillemets doubles\",\n"
    "  \"number\": 42,\n"
    "  \"float\": 3.14,\n"
    "  \"boolean\": true,\n"
    "  \"null_value\": null,\n"
    "  \"array\": [1, 2, 3, \"melange autorise\"],\n"
    "  \"object\": {\n"
    "    \"nested\": \"sous-objet\"\n"
    "  }\n"
    "}"
))

story.append(Paragraph("5.3 Regles strictes", ST_H1))
for x in [
    "Cles TOUJOURS entre <b>guillemets doubles</b>",
    "Pas de guillemets simples (contrairement a Python)",
    "Pas de commentaires // ou /* */",
    "Pas de virgule finale apres le dernier element",
    "Encodage UTF-8 obligatoire",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("5.4 Exemple FSBM : une filiere", ST_H1))
story.append(code(
    "{\n"
    "  \"id\": 10,\n"
    "  \"code\": \"IADS\",\n"
    "  \"name\": \"Master Intelligence Artificielle et Data Science\",\n"
    "  \"type\": \"MASTER\",\n"
    "  \"department_id\": 1,\n"
    "  \"coordinator\": \"Pr. Mehdi FILALI\",\n"
    "  \"coord_email\": \"m.filali@fsbm.ac.ma\",\n"
    "  \"duration_years\": 2,\n"
    "  \"capacity\": 25,\n"
    "  \"description\": \"Machine learning, deep learning, NLP...\",\n"
    "  \"careers\": \"Data scientist, ingenieur ML\",\n"
    "  \"is_active\": true,\n"
    "  \"created_at\": \"2026-01-15T10:30:00Z\"\n"
    "}"
))

story.append(Paragraph("5.5 Parser JSON", ST_H1))
story.append(code(
    "# Python\n"
    "import json\n"
    "data = json.loads('{\"name\": \"Karim\"}')\n"
    "print(data['name'])  # Karim\n"
    "\n"
    "# JavaScript / TypeScript\n"
    "const data = JSON.parse('{\"name\": \"Karim\"}');\n"
    "console.log(data.name);  // Karim\n"
    "\n"
    "// Avec HttpClient Angular, parsing auto\n"
    "this.http.get<Filiere>('/api/filieres/SMI')\n"
    "  .subscribe(f => console.log(f.name));"
))
story.append(PageBreak())

# CH 6 - REST
story.append(Paragraph("Chapitre 6 - REST : principes", ST_CHAPTER))

story.append(Paragraph("6.1 Qu'est-ce que REST ?", ST_H1))
story.append(Paragraph(
    "<b>REST = Representational State Transfer</b>. Style architectural defini par Roy "
    "Fielding (2000). Ce n'est PAS un standard ni un protocole, mais des principes a "
    "respecter pour designer des APIs.",
    ST_BODY))

story.append(Paragraph("6.2 Les 6 principes", ST_H1))
for n, d in [
    ("1. Client-Server",
     "Separation stricte entre client (UI) et serveur (logique + donnees)."),
    ("2. Stateless",
     "Chaque requete contient toute l'info necessaire. Pas de session cote serveur "
     "(le JWT est dans le header)."),
    ("3. Cacheable",
     "Les reponses indiquent si elles peuvent etre mises en cache."),
    ("4. Uniform Interface",
     "URLs identifient les ressources, methodes HTTP indiquent l'action."),
    ("5. Layered System",
     "Plusieurs couches possibles (load balancer, cache, etc.)."),
    ("6. Code on demand (optionnel)",
     "Le serveur peut envoyer du code executable (JavaScript)."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("6.3 Convention de nommage", ST_H1))
story.append(std_table([
    ['Action', 'URL', 'Methode'],
    ['Lister', '/api/filieres', 'GET'],
    ['Detail', '/api/filieres/SMI', 'GET'],
    ['Creer', '/api/filieres', 'POST'],
    ['Modifier (tout)', '/api/filieres/1', 'PUT'],
    ['Modifier (partiel)', '/api/filieres/1', 'PATCH'],
    ['Supprimer', '/api/filieres/1', 'DELETE'],
    ['Sous-ressources', '/api/filieres/1/modules', 'GET'],
], col_widths=[4*cm, 6.5*cm, 5.5*cm]))

story.append(Paragraph("6.4 Bonnes pratiques", ST_H1))
for x in [
    "URLs en <b>kebab-case</b> ou <b>snake_case</b>, pas en CamelCase",
    "Pluriel pour les collections : /filieres pas /filiere",
    "Verbe non recommande dans l'URL (la methode HTTP suffit)",
    "Pagination : ?page=1&page_size=20",
    "Tri : ?sort=name&order=asc",
    "Filtrage : ?type=MASTER&search=info",
    "Versionning : /api/v1/... si breaking changes",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))
story.append(PageBreak())

# CH 7 - chatbot endpoints
story.append(Paragraph("Chapitre 7 - Endpoints du chatbot-service", ST_CHAPTER))

story.append(Paragraph("7.1 POST /api/chat", ST_H1))
story.append(code(
    "Request :\n"
    "  POST /api/chat\n"
    "  Content-Type: application/json\n"
    "  {\n"
    "    \"message\": \"Quelles sont les filieres ?\",\n"
    "    \"session_id\": \"sess_abc123\",\n"
    "    \"user_id\": null,\n"
    "    \"language\": null\n"
    "  }\n"
    "\n"
    "Response :\n"
    "  200 OK\n"
    "  {\n"
    "    \"response\": \"La FSBM propose 7 licences...\",\n"
    "    \"intent\": \"filieres\",\n"
    "    \"confidence\": 1.0,\n"
    "    \"conversation_id\": 42,\n"
    "    \"session_id\": \"sess_abc123\",\n"
    "    \"language\": \"fr\",\n"
    "    \"language_confidence\": 1.0,\n"
    "    \"top_candidates\": [...],\n"
    "    \"suggestions\": [\"Master IADS\", ...],\n"
    "    \"news_items\": [],\n"
    "    \"response_time_ms\": 152\n"
    "  }"
))

story.append(Paragraph("7.2 POST /api/chat/feedback", ST_H1))
story.append(code(
    "Request :\n"
    "  POST /api/chat/feedback\n"
    "  {\n"
    "    \"conversation_id\": 42,\n"
    "    \"note\": 5,\n"
    "    \"is_helpful\": true,\n"
    "    \"commentaire\": \"Tres clair !\"\n"
    "  }\n"
    "\n"
    "Response :\n"
    "  200 OK\n"
    "  {\n"
    "    \"success\": true,\n"
    "    \"feedback_id\": 123\n"
    "  }"
))

story.append(Paragraph("7.3 GET /api/chat/history/{session_id}", ST_H1))
story.append(code(
    "Request :\n"
    "  GET /api/chat/history/sess_abc123\n"
    "\n"
    "Response :\n"
    "  200 OK\n"
    "  {\n"
    "    \"session_id\": \"sess_abc123\",\n"
    "    \"total_messages\": 4,\n"
    "    \"history\": [\n"
    "      { \"sender\": \"user\", \"text\": \"Bonjour\", \"timestamp\": \"...\" },\n"
    "      { \"sender\": \"bot\", \"text\": \"Bonjour !\", \"intent\": \"salutation\" },\n"
    "      ...\n"
    "    ]\n"
    "  }"
))

story.append(Paragraph("7.4 GET /api/chat/suggestions", ST_H1))
story.append(code(
    "Request :\n"
    "  GET /api/chat/suggestions?lang=fr&limit=6\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"language\": \"fr\",\n"
    "    \"total\": 6,\n"
    "    \"suggestions\": [\n"
    "      { \"intent\": \"inscription\", \"icon\": \"📋\",\n"
    "        \"question\": \"Comment s'inscrire a la FSBM ?\" },\n"
    "      ...\n"
    "    ]\n"
    "  }"
))

story.append(Paragraph("7.5 GET /api/chat/news", ST_H1))
story.append(code(
    "Request :\n"
    "  GET /api/chat/news?source=all&limit=8&lang=fr\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"fetched_at\": \"2026-05-28T...\",\n"
    "    \"total\": 6,\n"
    "    \"sources\": {\n"
    "      \"local_db\": { \"ok\": true, \"count\": 5 },\n"
    "      \"fsbm.ma\": { \"ok\": true, \"count\": 0 },\n"
    "      \"facebook\": { \"ok\": true, \"count\": 1 }\n"
    "    },\n"
    "    \"items\": [...]\n"
    "  }"
))

story.append(Paragraph("7.6 GET /api/intents", ST_H1))
story.append(code(
    "Request :\n"
    "  GET /api/intents?lang=fr\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"total\": 27,\n"
    "    \"intents\": [\n"
    "      {\n"
    "        \"tag\": \"inscription\",\n"
    "        \"category\": \"inscription\",\n"
    "        \"icon\": \"📋\",\n"
    "        \"nb_patterns\": 12,\n"
    "        \"nb_responses\": 3,\n"
    "        \"example\": \"Comment s'inscrire ?\"\n"
    "      },\n"
    "      ...\n"
    "    ]\n"
    "  }"
))
story.append(PageBreak())

# CH 8 - academic endpoints
story.append(Paragraph("Chapitre 8 - Endpoints de l'academic-service", ST_CHAPTER))

story.append(Paragraph("8.1 GET /api/overview (dashboard)", ST_H1))
story.append(code(
    "Response :\n"
    "  {\n"
    "    \"departments\": 5,\n"
    "    \"filieres\": 25,\n"
    "    \"modules\": 100,\n"
    "    \"professors\": 107,\n"
    "    \"students\": 2970,\n"
    "    \"events\": 5,\n"
    "    \"announcements\": 5,\n"
    "    \"clubs\": 8,\n"
    "    \"filieres_by_type\": {\n"
    "      \"LICENCE\": 6, \"LICENCE_PRO\": 1,\n"
    "      \"MASTER\": 16, \"MASTER_RECHERCHE\": 2\n"
    "    }\n"
    "  }"
))

story.append(Paragraph("8.2 GET /api/filieres", ST_H1))
story.append(code(
    "Query params :\n"
    "  type           - LICENCE, LICENCE_PRO, MASTER, MASTER_RECHERCHE\n"
    "  department_id  - 1, 2, 3, 4, 5\n"
    "  is_active      - true / false\n"
    "  search         - texte a chercher dans nom ou code\n"
    "\n"
    "Exemple :\n"
    "  GET /api/filieres?type=MASTER&search=info\n"
    "\n"
    "Response :\n"
    "  [\n"
    "    {\n"
    "      \"id\": 8,\n"
    "      \"code\": \"MIAGE\",\n"
    "      \"name\": \"Master Informatique et Gestion d'Entreprise\",\n"
    "      \"type\": \"MASTER\",\n"
    "      \"department_id\": 1,\n"
    "      \"capacity\": 30,\n"
    "      \"is_active\": true\n"
    "    },\n"
    "    ...\n"
    "  ]"
))

story.append(Paragraph("8.3 GET /api/filieres/code/{code}", ST_H1))
story.append(code(
    "GET /api/filieres/code/IADS\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"id\": 10,\n"
    "    \"code\": \"IADS\",\n"
    "    \"name\": \"Master IA et Data Science\",\n"
    "    \"type\": \"MASTER\",\n"
    "    \"department_id\": 1,\n"
    "    \"department_name\": \"Departement de Math-Info\",\n"
    "    \"coordinator\": \"Pr. Mehdi FILALI\",\n"
    "    \"modules_count\": 13,\n"
    "    \"students_count\": 48,\n"
    "    ...\n"
    "  }"
))

story.append(Paragraph("8.4 GET /api/filieres/{id}/modules", ST_H1))
story.append(code(
    "GET /api/filieres/1/modules\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"filiere_id\": 1,\n"
    "    \"total_modules\": 30,\n"
    "    \"by_semester\": [\n"
    "      { \"semester\": 1, \"modules\": [\n"
    "          { \"code\": \"SMI-S1-M1\", \"name\": \"Analyse I\",\n"
    "            \"credits\": 6, \"hours_cours\": 36 },\n"
    "          ...\n"
    "      ]},\n"
    "      { \"semester\": 2, \"modules\": [...]},\n"
    "      ...\n"
    "    ]\n"
    "  }"
))

story.append(Paragraph("8.5 GET /api/professors (paginé)", ST_H1))
story.append(code(
    "GET /api/professors?department_id=1&page=1&page_size=20\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"items\": [\n"
    "      { \"id\": 1, \"matricule\": \"PROF100001\",\n"
    "        \"first_name\": \"Mohammed\", \"last_name\": \"ALAOUI\",\n"
    "        \"email\": \"...@fsbm.ac.ma\", \"grade\": \"PES\",\n"
    "        \"specialty\": \"Intelligence Artificielle\" },\n"
    "      ...\n"
    "    ],\n"
    "    \"total\": 35,\n"
    "    \"page\": 1,\n"
    "    \"page_size\": 20,\n"
    "    \"total_pages\": 2\n"
    "  }"
))

story.append(Paragraph("8.6 Liste complete des endpoints academic", ST_H1))
story.append(std_table([
    ['Methode', 'URL', 'Description'],
    ['GET', '/api/overview', 'Compteurs dashboard'],
    ['GET', '/api/departments', 'Liste des 5 dept'],
    ['GET', '/api/departments/{id}', 'Detail dept'],
    ['GET', '/api/departments/{id}/filieres', 'Filieres du dept'],
    ['GET', '/api/departments/{id}/professors', 'Profs du dept'],
    ['GET', '/api/filieres', 'Liste filieres + filtres'],
    ['GET', '/api/filieres/{id}', 'Detail filiere'],
    ['GET', '/api/filieres/code/{code}', 'Filiere par code'],
    ['GET', '/api/filieres/{id}/modules', 'Modules par semestre'],
    ['GET', '/api/modules', 'Liste modules + filtres'],
    ['GET', '/api/modules/{id}', 'Detail module'],
    ['GET', '/api/professors', 'Profs paginé'],
    ['GET', '/api/professors/{id}', 'Detail prof'],
    ['GET', '/api/students', 'Etudiants paginé'],
    ['GET', '/api/students/{id}', 'Detail etudiant'],
    ['GET', '/api/students/cne/{cne}', 'Etudiant par CNE'],
    ['GET', '/api/students/stats/by-filiere', 'Stats par filiere'],
    ['GET', '/api/schedule', 'Emploi du temps'],
    ['GET', '/api/exams', 'Calendrier examens'],
    ['GET', '/api/announcements', 'Annonces'],
    ['GET', '/api/events', 'Evenements'],
    ['GET', '/api/clubs', 'Clubs etudiants'],
    ['GET', '/api/health', 'Status service'],
], col_widths=[1.5*cm, 6.5*cm, 8*cm]))
story.append(PageBreak())

# CH 9 - LLM endpoints
story.append(Paragraph("Chapitre 9 - Endpoints LLM", ST_CHAPTER))

story.append(Paragraph("9.1 POST /api/llm/chat", ST_H1))
story.append(code(
    "Request :\n"
    "  POST /api/llm/chat\n"
    "  {\n"
    "    \"message\": \"Quelles conditions pour le master IADS ?\",\n"
    "    \"session_id\": \"sess_abc\",\n"
    "    \"language\": null,\n"
    "    \"temperature\": 0.6\n"
    "  }\n"
    "\n"
    "Response :\n"
    "  {\n"
    "    \"response\": \"Pour le master IADS, vous devez avoir...\",\n"
    "    \"provider\": \"groq\",\n"
    "    \"model\": \"llama-3.3-70b-versatile\",\n"
    "    \"intent_detected\": \"master_iads\",\n"
    "    \"confidence\": 0.85,\n"
    "    \"language\": \"fr\",\n"
    "    \"contexts_used\": [\n"
    "      { \"tag\": \"master_iads\", \"score\": 0.91, ... },\n"
    "      { \"tag\": \"masters\", \"score\": 0.45, ... }\n"
    "    ],\n"
    "    \"conversation_id\": 42,\n"
    "    \"session_id\": \"sess_abc\",\n"
    "    \"history_length\": 4,\n"
    "    \"latency_ms\": 187,\n"
    "    \"tokens_used\": 423\n"
    "  }"
))

story.append(Paragraph("9.2 GET /api/llm/status", ST_H1))
story.append(code(
    "Response :\n"
    "  {\n"
    "    \"groq\": {\n"
    "      \"available\": true,\n"
    "      \"model\": \"llama-3.3-70b-versatile\"\n"
    "    },\n"
    "    \"hf\": {\n"
    "      \"available\": false,\n"
    "      \"model\": \"meta-llama/Meta-Llama-3-8B-Instruct\"\n"
    "    },\n"
    "    \"fallback_tfidf\": true,\n"
    "    \"primary\": \"groq\"\n"
    "  }"
))

story.append(Paragraph("9.3 GET /api/llm/models", ST_H1))
story.append(code(
    "Response :\n"
    "  {\n"
    "    \"groq\": {\n"
    "      \"llama-large\": \"llama-3.3-70b-versatile\",\n"
    "      \"llama-fast\": \"llama-3.1-8b-instant\",\n"
    "      \"mixtral\": \"mixtral-8x7b-32768\"\n"
    "    },\n"
    "    \"huggingface\": {\n"
    "      \"llama\": \"meta-llama/Meta-Llama-3-8B-Instruct\",\n"
    "      \"mistral\": \"mistralai/Mistral-7B-Instruct-v0.3\"\n"
    "    }\n"
    "  }"
))
story.append(PageBreak())

# CH 10 - Communication inter
story.append(Paragraph("Chapitre 10 - Communication inter-services", ST_CHAPTER))

story.append(Paragraph("10.1 Pourquoi inter-services ?", ST_H1))
story.append(Paragraph(
    "Dans une architecture micro-services, les services doivent <b>collaborer</b>. Exemple : "
    "le chatbot-service a besoin des annonces stockees dans academic-service pour repondre "
    "a 'Cherche les dernieres news'.",
    ST_BODY))

story.append(Paragraph("10.2 Methodes possibles", ST_H1))
story.append(std_table([
    ['Methode', 'Description', 'Utilisation'],
    ['HTTP REST', 'Service A appelle service B', 'Notre choix (simple)'],
    ['gRPC', 'RPC binaire performant', 'Microservices haute perf'],
    ['Message queue', 'RabbitMQ, Kafka', 'Async + decouplage'],
    ['GraphQL', 'API flexible avec query', 'BFF, agregation'],
], col_widths=[3*cm, 6*cm, 7*cm]))

story.append(Paragraph("10.3 Notre web_fetcher.py", ST_H1))
story.append(Paragraph(
    "Le chatbot-service appelle academic-service via HTTP avec httpx :",
    ST_BODY))
story.append(code(
    "import httpx\n"
    "\n"
    "class WebFetcher:\n"
    "    def __init__(self, academic_service_url='http://localhost:8002'):\n"
    "        self.academic_service_url = academic_service_url\n"
    "    \n"
    "    async def _fetch_from_academic_service(self):\n"
    "        async with httpx.AsyncClient(timeout=5.0) as client:\n"
    "            # 1. Recuperer les annonces\n"
    "            r = await client.get(\n"
    "                f'{self.academic_service_url}/api/announcements',\n"
    "                params={'limit': 5}\n"
    "            )\n"
    "            if r.status_code == 200:\n"
    "                announcements = r.json()\n"
    "            \n"
    "            # 2. Recuperer les evenements\n"
    "            r = await client.get(\n"
    "                f'{self.academic_service_url}/api/events',\n"
    "                params={'upcoming_only': True}\n"
    "            )\n"
    "            if r.status_code == 200:\n"
    "                events = r.json()\n"
    "        \n"
    "        return announcements + events"
))

story.append(Paragraph("10.4 Gestion des erreurs inter-services", ST_H1))
story.append(code(
    "try:\n"
    "    async with httpx.AsyncClient(timeout=5.0) as client:\n"
    "        r = await client.get(url)\n"
    "        r.raise_for_status()  # leve si 4xx ou 5xx\n"
    "        return r.json()\n"
    "except httpx.TimeoutException:\n"
    "    # Service trop lent ou down\n"
    "    return []  # mode degrade\n"
    "except httpx.HTTPStatusError as e:\n"
    "    # 4xx/5xx\n"
    "    logger.error(f'Service {url} retournee {e.response.status_code}')\n"
    "    return []\n"
    "except Exception as e:\n"
    "    logger.error(f'Erreur inattendue : {e}')\n"
    "    return []"
))

story.append(Paragraph("10.5 Cache TTL", ST_H1))
story.append(Paragraph(
    "Pour eviter de marteler academic-service, on cache les resultats 5 minutes :",
    ST_BODY))
story.append(code(
    "class WebFetcher:\n"
    "    CACHE_TTL = 5 * 60   # 5 minutes\n"
    "    \n"
    "    def _get_cached(self, key):\n"
    "        if key in self._cache:\n"
    "            entry = self._cache[key]\n"
    "            if time.time() - entry.fetched_at < self.CACHE_TTL:\n"
    "                return entry.items\n"
    "        return None\n"
    "    \n"
    "    def _set_cached(self, key, items):\n"
    "        self._cache[key] = CachedResult(items, time.time())"
))
story.append(PageBreak())

# CH 11 - Proxy Angular
story.append(Paragraph("Chapitre 11 - Proxy Angular (proxy.conf.json)", ST_CHAPTER))

story.append(Paragraph("11.1 Probleme : CORS", ST_H1))
story.append(Paragraph(
    "Le frontend Angular tourne sur port 4200. Les services backend tournent sur 8001 et "
    "8002. Faire des requetes inter-ports declencherait CORS si pas configure.",
    ST_BODY))

story.append(Paragraph("11.2 Solution : proxy dev server", ST_H1))
story.append(Paragraph(
    "Angular CLI offre un <b>proxy integrate</b> au dev server. Le navigateur croit que tout "
    "vient de localhost:4200, mais en realite le serveur Angular redirige vers le bon backend.",
    ST_BODY))

story.append(Paragraph("11.3 proxy.conf.json", ST_H1))
story.append(code(
    "{\n"
    "  \"/api/chat/feedback\": {\n"
    "    \"target\": \"http://localhost:8001\",\n"
    "    \"secure\": false,\n"
    "    \"changeOrigin\": true\n"
    "  },\n"
    "  \"/api/chat\": {\n"
    "    \"target\": \"http://localhost:8001\",\n"
    "    \"secure\": false,\n"
    "    \"changeOrigin\": true\n"
    "  },\n"
    "  \"/api/llm\": {\n"
    "    \"target\": \"http://localhost:8001\",\n"
    "    \"secure\": false,\n"
    "    \"changeOrigin\": true\n"
    "  },\n"
    "  \"/api/academic\": {\n"
    "    \"target\": \"http://localhost:8002\",\n"
    "    \"secure\": false,\n"
    "    \"changeOrigin\": true,\n"
    "    \"pathRewrite\": { \"^/api/academic\": \"/api\" }\n"
    "  }\n"
    "}"
))

story.append(Paragraph("11.4 Comment ca marche", ST_H1))
story.append(diagram(
    "    Browser fait :\n"
    "    GET http://localhost:4200/api/academic/filieres\n"
    "         |\n"
    "         v\n"
    "    Angular Dev Server intercepte\n"
    "         |\n"
    "         v\n"
    "    Consulte proxy.conf.json\n"
    "    Trouve /api/academic -> 8002 + pathRewrite\n"
    "         |\n"
    "         v\n"
    "    Reecrit URL : http://localhost:8002/api/filieres\n"
    "         |\n"
    "         v\n"
    "    Envoie au backend academic-service\n"
    "         |\n"
    "         v\n"
    "    academic-service repond\n"
    "         |\n"
    "         v\n"
    "    Angular Dev Server relaie au browser"
))

story.append(alert_box(
    "En production, on remplace ce proxy par un <b>reverse proxy nginx</b> qui fait pareil. "
    "Le frontend devient un site statique servi par nginx, qui redirige /api/... vers les "
    "services backend.",
    kind="tip"))
story.append(PageBreak())

# CH 12 - Swagger
story.append(Paragraph("Chapitre 12 - Swagger/OpenAPI", ST_CHAPTER))

story.append(Paragraph("12.1 OpenAPI specification", ST_H1))
story.append(Paragraph(
    "<b>OpenAPI</b> (anciennement Swagger) est une specification standard pour decrire des "
    "APIs REST. Format YAML ou JSON. FastAPI genere cette specification automatiquement.",
    ST_BODY))

story.append(Paragraph("12.2 Acces dans notre projet", ST_H1))
for x in [
    "<b>http://localhost:8001/docs</b> - Swagger UI interactive",
    "<b>http://localhost:8001/redoc</b> - ReDoc (plus belle, non-interactive)",
    "<b>http://localhost:8001/openapi.json</b> - spec OpenAPI JSON",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("12.3 Ce qu'on voit sur /docs", ST_H1))
for x in [
    "Liste de TOUS les endpoints groupes par tag",
    "Pour chaque endpoint : methode, URL, description",
    "Schemas Pydantic des bodies (request + response)",
    "Codes de statut possibles",
    "Bouton <b>Try it out</b> pour tester en direct",
    "Generation automatique de curl",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("12.4 Ameliorer la doc dans le code", ST_H1))
story.append(code(
    "@router.post(\n"
    "    '/chat',\n"
    "    response_model=ChatResponse,\n"
    "    summary='Envoyer un message au chatbot',\n"
    "    description='''\n"
    "    Le chatbot detecte la langue, classifie l'intent et genere une reponse.\n"
    "    \n"
    "    Memoire conversationnelle 10 tours. Personnalisation genre/nom.\n"
    "    ''',\n"
    "    tags=['chat'],\n"
    "    responses={\n"
    "        200: { 'description': 'Reponse OK' },\n"
    "        422: { 'description': 'Validation echouee' },\n"
    "        500: { 'description': 'Erreur serveur' },\n"
    "    }\n"
    ")\n"
    "async def chat(req: ChatRequest):\n"
    "    ..."
))
story.append(PageBreak())

# CH 13 - Tester
story.append(Paragraph("Chapitre 13 - Tester les APIs", ST_CHAPTER))

story.append(Paragraph("13.1 Avec curl (ligne de commande)", ST_H1))
story.append(code(
    "# GET simple\n"
    "curl http://localhost:8001/api/health\n"
    "\n"
    "# POST avec body JSON\n"
    "curl -X POST http://localhost:8001/api/chat \\\n"
    "  -H \"Content-Type: application/json\" \\\n"
    "  -d '{\"message\": \"Bonjour\"}'\n"
    "\n"
    "# Sauver la reponse dans un fichier\n"
    "curl http://localhost:8002/api/filieres -o filieres.json"
))

story.append(Paragraph("13.2 Avec Postman", ST_H1))
story.append(Paragraph(
    "<b>Postman</b> est une app GUI gratuite pour tester les APIs. Tu peux :",
    ST_BODY))
for x in [
    "Sauvegarder une collection de requetes",
    "Definir des variables d'environnement",
    "Ecrire des tests automatises (JavaScript)",
    "Partager avec ton equipe",
    "Generer la doc auto",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("13.3 Avec Swagger UI", ST_H1))
story.append(Paragraph(
    "Le plus simple pour notre demo : http://localhost:8001/docs et http://localhost:8002/docs. "
    "Clique sur un endpoint, 'Try it out', remplis le body, 'Execute'. La reponse s'affiche.",
    ST_BODY))

story.append(Paragraph("13.4 Avec Python (requests / httpx)", ST_H1))
story.append(code(
    "import httpx\n"
    "\n"
    "# Async\n"
    "async with httpx.AsyncClient() as client:\n"
    "    response = await client.post(\n"
    "        'http://localhost:8001/api/chat',\n"
    "        json={'message': 'Bonjour'}\n"
    "    )\n"
    "    print(response.status_code)\n"
    "    print(response.json())\n"
    "\n"
    "# Sync (avec requests)\n"
    "import requests\n"
    "r = requests.post(\n"
    "    'http://localhost:8001/api/chat',\n"
    "    json={'message': 'Bonjour'}\n"
    ")\n"
    "print(r.json())"
))
story.append(PageBreak())

# CH 14 - Conclusion
story.append(Paragraph("Chapitre 14 - Conclusion", ST_CHAPTER))

story.append(Paragraph("14.1 Recap", ST_H1))
for x in [
    "HTTP = protocole client-serveur en text",
    "Requete = methode + URL + headers + body",
    "Reponse = code statut + headers + body",
    "5 methodes principales : GET/POST/PUT/PATCH/DELETE",
    "16 codes de statut essentiels (200, 404, 500...)",
    "Headers pour metadonnees (Content-Type, Authorization, CORS...)",
    "JSON = format standard d'echange",
    "REST = principes de design (stateless, uniform interface)",
    "23 endpoints academic + 8 endpoints chatbot + 3 endpoints LLM",
    "Communication inter-services via HTTP REST avec httpx async",
    "Proxy Angular pour eviter CORS en dev",
    "Swagger UI auto sur /docs",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("14.2 Pour aller plus loin", ST_H1))
for x in [
    "PDF 03 - implementation FastAPI cote serveur",
    "PDF 08 - securite des APIs (JWT, CORS, etc.)",
    "PDF 09 - workflow complet incluant les appels API",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("07_APIs_Communication_Complet.pdf", story,
          "PDF 07 - APIs et Communication",
          "FSBM Platform - APIs et Communication Complet")
