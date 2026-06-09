# FSBM Platform - Contexte de session (a copier/coller dans la prochaine session)

> Ce fichier resume tout le travail effectue sur la plateforme FSBM Chatbot.
> A coller en debut d'une nouvelle session Claude Code pour continuer sans perdre le contexte.

---

## 1. Vue d'ensemble du projet

**Nom :** FSBM Platform
**Cible :** Faculte des Sciences Ben M'Sick (FSBM), Universite Hassan II Casablanca
**Type :** PFE - Plateforme web modulaire avec chatbot intelligent multilingue
**Etudiant :** belmo (Windows, C:\Users\belmo\studies\PFE\chatbot-fsbm-platform)

**Objectif :** chatbot intelligent qui repond aux questions des etudiants FSBM en
francais, anglais, et **darija marocaine** (script latin + arabe), 24/7, avec
detection de genre/nom pour personnalisation (khoya/khti/lalla).

---

## 2. Architecture technique

### Stack
- **Frontend :** Angular 17 (standalone components, signals, lazy loading)
- **Backend :** FastAPI Python 3.11+ (async, Pydantic v2)
- **Base relationnelle :** MySQL 8.0 (16 tables, 3NF, FULLTEXT indexes)
- **Base NoSQL :** MongoDB 7 (6 collections avec JSON Schema validation)
- **NLP :** TF-IDF + Cosine Similarity (3 modeles paralleles FR/EN/Darija)
- **LLM :** LLaMA 3.3-70B via Groq API + fallback HuggingFace + fallback TF-IDF
- **RAG :** TF-IDF reutilise comme retriever
- **Conteneurisation :** Docker (Compose pour dev)

### Microservices
| Service | Port | Role |
|---------|------|------|
| frontend | 4200 | Angular avec proxy.conf.json |
| chatbot-service | 8001 | NLP + LLM + conversations |
| academic-service | 8002 | Donnees scolaires (filieres, profs, etudiants) |
| MySQL | 3306 | Donnees structurees |
| MongoDB | 27017 | Sessions + logs |

### Structure des dossiers
```
chatbot-fsbm-platform/
  frontend/                       # Angular 17
    src/app/
      pages/                      # 9 pages lazy-loaded
      components/chat-window/     # composant chatbot
      services/chat.service.ts    # avec sendMessageLLM
  services/
    chatbot-service/              # port 8001
      app/
        nlp/                      # classifier, language_detector
        llm/                      # groq_client, rag, llm_service
        core/persona.py           # detection genre/nom
        routers/                  # chat, llm
      data/faq_dataset.json       # v3.2.0 trilingue
    academic-service/             # port 8002
  docs/pdf/
    detailed/                     # 10 PDFs pedagogiques
      pdf_utils.py                # infrastructure partagee
      gen_01..10_*.py             # scripts generateurs
      01_Architecture_Globale_FSBM.pdf
      02_Frontend_Angular_Complet.pdf
      ...
      10_Guide_Soutenance.pdf
  notebooks/fsbm_groq_demo.ipynb  # Colab/Kaggle
  SETUP.ps1                       # one-click setup
  clean-zombies.ps1               # nettoyage ports
  fix-windows-ports.ps1           # exclude port range
```

---

## 3. Travail accompli (tout est livre)

### Phases completees

1. **Phase 1** - Recherche initiale + Google Form pour scolarite
2. **Phase 2** - Refactor microservices FastAPI + MySQL + MongoDB
3. **Phase 3** - Frontend Angular modernise (9 pages, sidebar, topbar, dark mode)
4. **Phase 4** - Setup BDD (MySQL Workbench + scripts)
5. **Phase 5** - Documentation PDF (rapport projet, guide tech, zombies guide)
6. **Phase 6** - Trilingue FR/EN/Darija + web search fsbm.ma
7. **Phase 7** - Detection genre/nom + personnalisation (khoya/khti/lalla)
8. **Phase 8** - Zombies de ports Windows (WSL leak) -> solution permanente
9. **Phase 9** - LLaMA 3 via Groq + RAG + cascade fallback
10. **Phase 10** - **10 PDFs ultra-detailles** (1 par domaine)
11. **PARTIE 2** - Espace admin (login JWT) + zone reviews etudiants (voir section 11)

### 10 PDFs pedagogiques (TOUS GENERES) dans `docs/pdf/detailed/`
| # | Titre | Taille |
|---|-------|--------|
| 01 | Architecture Globale FSBM | 166 KB |
| 02 | Frontend Angular Complet | 160 KB |
| 03 | Backend FastAPI Complet | 155 KB |
| 04 | MySQL + SQLAlchemy Complet | 144 KB |
| 05 | MongoDB + NoSQL Complet | 140 KB |
| 06 | NLP + IA Chatbot Complet | 156 KB |
| 07 | APIs + Communication | 156 KB |
| 08 | Securite Complete | 149 KB |
| 09 | Workflow Complet | 150 KB |
| 10 | Guide Soutenance | 147 KB |

**Total : ~1.5 MB documentation pedagogique**

---

## 4. Fichiers cles

### Backend chatbot-service
- `app/llm/groq_client.py` - client Groq avec chat() / chat_stream()
- `app/llm/rag.py` - RAGRetriever + build_rag_prompt() + SYSTEM_PROMPTS FR/EN/darija
- `app/llm/llm_service.py` - orchestration cascade fallback
- `app/routers/llm.py` - POST /api/llm/chat, GET /api/llm/status, /models
- `app/routers/chat.py` - POST /api/chat (TF-IDF classique)
- `app/core/persona.py` - GENDER_HINTS_F/M, detect_name(), personalize_response()
- `app/nlp/classifier.py` - MultilingualClassifier (3 vectorizers)
- `app/nlp/language_detector.py` - hybride (arabe + numerique 3/7/9 + lex)
- `data/faq_dataset.json` - v3.2.0, 28 intents, 188 FR + 186 EN + 461 Darija

### Infrastructure PDF
- `docs/pdf/detailed/pdf_utils.py` - palette FSBM, styles ST_*, helpers code/diagram/std_table/alert_box/analogy/toc_entry/cover_page/build_doc
- **BUG FIX :** _escape_html() dans code() et diagram() (sinon ReportLab crash sur les `<a>`, etc.)

### Frontend
- `src/app/services/chat.service.ts` - sendMessage + sendMessageLLM + getLLMStatus
- `src/app/components/chat-window/chat-window.component.ts` - toggle TF-IDF/LLM

---

## 5. Bugs resolus

| Probleme | Solution |
|----------|----------|
| MySQL pas dans PATH | Detect C:\Program Files\MySQL\... + Workbench alternative |
| Duplicate email prof | email_used set + suffix loop dans generate_professors() |
| ONLY_FULL_GROUP_BY error | SET SESSION sql_mode = REPLACE(..., 'ONLY_FULL_GROUP_BY', '') |
| Safe Update Mode Workbench | WHERE id > 0 + SET SQL_SAFE_UPDATES = 0 |
| WinError 10013 (port) | clean-zombies.ps1 + fix-windows-ports.ps1 + migration vers 8001/8002 |
| PowerShell SETUP.bat | Cree SETUP.ps1 natif |
| MySQL warning = error | cmd /c wrapper pour isoler stderr |
| Pydantic extra inputs | extra="ignore" dans SettingsConfigDict |
| BOM dans .env | UTF8Encoding($false) pour BOM-less |
| UnicodeEncodeError Windows | sys.stdout.reconfigure(encoding="utf-8") |
| ReportLab HTML parsing | _escape_html() dans pdf_utils.py code()/diagram() |
| fsbm.ma SPA (1981 bytes) | Fallback sur academic-service comme source d'annonces |

---

## 6. Commandes utiles

### Generer un PDF
```powershell
cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\docs\pdf\detailed
$env:PYTHONIOENCODING="utf-8"
py gen_07_apis.py
```

### Lancer la plateforme
```powershell
# Tout en un (depuis racine)
.\SETUP.ps1

# Ou manuellement :
# Terminal 1 - chatbot-service
cd services\chatbot-service
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - academic-service
cd services\academic-service
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 3 - frontend
cd frontend
npm start  # -> http://localhost:4200
```

### Nettoyer les zombies de ports
```powershell
.\clean-zombies.ps1
```

---

## 7. Etat actuel - Tout livre

**TOUT EST FINI.** Le projet est pret pour la soutenance.

Eventuelles suites possibles (Phase 2/3) :
- JWT auth + bcrypt + RBAC 4 roles (STUDENT/PROF/SCOLARITE/ADMIN)
- Rate limiting SlowAPI
- HTTPS + certificat Let's Encrypt
- App mobile Flutter
- Integration WhatsApp Business API + Messenger
- Interface admin pour scolarite (CRUD dataset NLP)
- Tests automatises pytest
- CI/CD GitHub Actions
- Production deploy (VPS + nginx reverse proxy)

---

## 8. Conventions importantes

- **Pas d'emojis** dans le code/PDFs sauf si user demande explicite
- **No NOT** create .md files non demandes
- Preferer Edit a Write pour fichiers existants
- Toujours UTF-8 pour fichiers
- PowerShell 5.1 sur Windows (pas de `&&`, utiliser `; if ($?) {...}`)
- Python via `py` (Windows launcher), pas `python3`

---

## 9. Comment continuer dans une nouvelle session

1. Ouvrir la nouvelle session Claude Code dans `C:\Users\belmo\studies\PFE\chatbot-fsbm-platform`
2. Coller ce fichier au debut : "Voici le contexte de ma session precedente : [paste]"
3. Indiquer ce que tu veux faire :
   - "Ajouter Phase 2 : authentification JWT"
   - "Corriger le bug X"
   - "Ajouter une nouvelle page Angular"
   - "Generer un PDF supplementaire sur Y"

Claude lira le contexte et reprendra exactement ou j'ai laisse.

---

## 10. Files a connaitre absolument

```
SETUP.ps1                                      # one-click launch
clean-zombies.ps1                              # cleanup ports
fix-windows-ports.ps1                          # exclude WSL ports
SESSION_CONTEXT.md                             # ce fichier
docs/pdf/detailed/pdf_utils.py                 # infra PDF
docs/pdf/detailed/gen_*.py                     # 10 generateurs PDF
docs/pdf/detailed/*.pdf                        # 10 PDFs livres
services/chatbot-service/app/main.py           # entry point chatbot
services/chatbot-service/app/llm/llm_service.py # cascade fallback
services/chatbot-service/data/faq_dataset.json # dataset trilingue
services/academic-service/app/main.py          # entry point academic
frontend/src/app/app.routes.ts                 # 9 routes lazy
frontend/src/app/components/chat-window/       # chatbot UI
frontend/proxy.conf.json                       # CORS bypass dev
```

---

---

## 11. PARTIE 2 — Espace Admin + Reviews (livre 2026-05-31)

### Ce qui a ete ajoute
- **Login admin JWT + bcrypt** (la table `users` existait deja, maintenant exploitee)
- **Lien admin MASQUE** aux utilisateurs normaux (visible seulement si admin connecte ;
  acces direct via /admin/login)
- **Espace admin** (plein ecran, hors sidebar) avec 6 onglets CRUD :
  Annonces, Evenements, Academique (departements/filieres/modules/profs),
  Vie etudiante (clubs), Moderation des avis, FAQ
- **Upload de fichiers** (POST /api/admin/upload + statique /uploads) :
  photos profs, logos filieres/departements/clubs, image + PDF pour annonces/evenements
- **CRUD complet verifie** sur TOUTES les entites (profs/departements/clubs etaient manquants)
- **FAQ pre-remplies** : 24 FAQ importees du dataset chatbot dans faq_items (seed_faq.py),
  editables/supprimables depuis l'admin
- **Zone Reviews publique** : notation etoiles (1-5) de l'assistant IA + avis libres
  sur tout (faculte, filieres, modules, profs) + mur d'avis + stats (note moyenne IA)
- **Moderation** : l'admin approuve / masque / epingle / repond / supprime les avis

### Nouveaux fichiers media/clubs/FAQ
- database/mysql/06_phase2_uploads.sql            (logo_url filieres + attachment_url)
- services/academic-service/app/routers/admin_upload.py  (upload images/PDF)
- services/academic-service/app/routers/admin_misc.py    (CRUD departements + clubs)
- services/academic-service/seed_faq.py                  (pre-remplit faq_items)
- services/academic-service/test_phase2b.py              (17 checks : upload/depts/clubs/FAQ/prof)
- frontend/.../admin/shared/file-upload.component.ts     (widget upload reutilisable)
- frontend/.../admin/panels/clubs-panel.component.ts     (vie etudiante)
- Tests : test_phase2.py (16/16) + test_phase2b.py (17/17)

### Identifiants admin par defaut
- **Email :** admin@fsbm.ac.ma
- **Mot de passe :** Admin@FSBM2026
- (hash bcrypt cost 12 dans 05_phase2_reviews_auth.sql — A CHANGER en prod)

### Comment activer la Partie 2
```powershell
# 1. Appliquer la migration SQL (table reviews + compte admin)
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -proot fsbm_db `
  -e "source C:/Users/belmo/studies/PFE/chatbot-fsbm-platform/database/mysql/05_phase2_reviews_auth.sql"

# 2. Installer les nouvelles deps backend dans le PYTHON GLOBAL
#    (IMPORTANT : start.ps1 lance "py -m uvicorn" = Python global, PAS le venv !)
py -m pip install bcrypt "python-jose[cryptography]" email-validator

# 3. (Re)lancer academic-service (port 8002) + frontend (4200)
#    Test e2e : .\venv\Scripts\python.exe test_phase2.py  (16 OK / 0 FAIL)
```
- **Page Avis (public)** : http://localhost:4200/avis (lien "💬 Avis" dans la sidebar)
- **Login admin** : http://localhost:4200/admin/login (lien "🔐 Admin" en bas de sidebar)
- **Dashboard admin** : http://localhost:4200/admin (protege par adminGuard)

### Nouveaux fichiers Partie 2
```
database/mysql/05_phase2_reviews_auth.sql            # table reviews + seed admin
services/academic-service/app/core/security.py        # bcrypt + JWT + get_current_admin
services/academic-service/app/routers/auth.py         # /api/auth/login + /me
services/academic-service/app/routers/reviews.py      # public + /api/admin/reviews
services/academic-service/app/routers/admin_content.py # CRUD annonces/events/faq
services/academic-service/app/routers/admin_academic.py# CRUD filieres/modules/profs
services/academic-service/app/schemas/{auth,reviews,admin}.py
services/academic-service/test_phase2.py              # smoke test e2e (16 checks)
frontend/src/app/core/{auth.service,auth.guard,auth.interceptor}.ts
frontend/src/app/services/{reviews.service,admin.service}.ts
frontend/src/app/features/reviews/reviews.component.ts
frontend/src/app/features/admin/admin-login.component.ts
frontend/src/app/features/admin/admin.component.ts
frontend/src/app/features/admin/panels/*.component.ts (5 panneaux + panel-shared.css)
```

### API Partie 2 (toutes via proxy /api/academic -> :8002/api)
| Methode | Endpoint | Auth | Role |
|---------|----------|------|------|
| POST | /api/auth/login | non | — |
| GET  | /api/auth/me | Bearer | tout user |
| GET/POST | /api/reviews | non | public |
| GET | /api/reviews/stats | non | public |
| GET/PATCH/DELETE | /api/admin/reviews | Bearer | ADMIN |
| CRUD | /api/admin/announcements\|events\|faq | Bearer | ADMIN |
| CRUD | /api/admin/filieres\|modules\|professors | Bearer | ADMIN |

### Verifie
- Backend : import OK (58 routes), test e2e 16/16 OK contre MySQL reel
- Frontend : `npm run build` complet (chunks admin/reviews/login generes)

---

---

## 12. PHASE 3 — Donnees REELLES FSBM + Rapport PFE (juin 2026)

### Rapport PFE professionnel
- `docs/rapport/Rapport_PFE_FSBM.pdf` — **136 pages**, jury-ready.
- Genere par `docs/rapport/build_rapport.py` (moteur `report_engine.py`, modules
  `front.py`, `ch01_04.py`, `ch05_08.py`, `ch09_14.py`, `annexes.py`).
- Diagrammes UML via Mermaid (mermaid.ink, cache `assets/`), graphiques matplotlib,
  23 captures app + captures officielles FSBM, TOC/listes auto.

### Corrections appliquees (exigence encadrant)
- Salma CHENANI -> **Salma HANNOUNI** (co-encadrante, partout).
- "Master en Informatique" -> **"Licence en Developpement Informatique"** (couverture,
  jury, coherence) — confirme comme filiere reelle de la FSBM (Resp. Pr. SAEL Nihal).
- Encadrant conserve : Pr. Habib BENLAHMER.

### Donnees REELLES integrees (sources verifiables, rien d'invente)
- Source de verite : `docs/rapport/fsbm_real.py` (depuis fsbm.ma + Google Scholar).
- **6 departements reels** + chefs ; **~25 filieres reelles** + responsables ;
  **239 professeurs** (effectif reel, ~40 noms releves) ; Doyen **Pr. Abdeslam EL BOUARI**.
- Profil Scholar verifie de l'encadrant (Benlahmar : 2785 citations, h-index 24, i10 61).
- **Base de donnees** : `database/mysql/07_real_fsbm_data.sql` (UPSERT, FAQ reelles) PUIS
  `database/mysql/08_real_fsbm_clean.sql` (genere par `gen_real_clean.py`) qui REMPLACE
  les donnees synthetiques par les reelles : 6 dep, 25 filieres, 64 profs (emails
  **@univh2c.ma**), 5 profs avec metriques Scholar verifiees, 4 vraies actualites, 300
  etudiants. Les deux charges par SETUP.ps1.
- **Endpoint /api/overview** (academic-service `routers/system.py`) renvoie desormais les
  CHIFFRES OFFICIELS REELS : 11994 etudiants, 239 profs, 6 dep, 30 filieres, 12 labos,
  160 partenaires (source fsbm.ma). -> Le tableau de bord affiche les vrais nombres.
  IMPORTANT : relancer academic-service pour prendre en compte ce changement de code.
- **Reseau Scholar** (5 profs reels via co-auteurs de Benlahmar) : Benlahmar (2785 cit/h24),
  El Filali (1164/h13), Zahour (182/h5, chatbots educatifs), El Guemmat (395/h13),
  Talea (6755/h39). Dans le rapport (Ch2 + Annexe R-A) et la base (bio des profs).
- **Chatbot** : `services/chatbot-service/data/fsbm_knowledge.json` — couche de
  connaissance institutionnelle reelle pour le RAG + FAQ reelles en base.
- **Rapport** : Ch1 (chiffres reels), Ch2 (etude detaillee FSBM + profil Scholar
  encadrant), Ch7 (base de connaissance reelle), Ch12 (volume de donnees reelles),
  Annexes R-A..R-E (profs, departements, filieres, sources, captures FSBM officielles).

### Contrainte respectee
Aucune donnee presentee comme reelle n'a ete inventee. Scholar bloque l'extraction
massive : seules les metriques de l'encadrant sont affichees ; les autres professeurs
figurent par leurs noms reels sans metriques fabriquees.

---

_Fichier genere le 2026-05-31, mis a jour Partie 2 puis Phase 3 (donnees reelles + rapport)._
_Projet : FSBM Platform - PFE chatbot intelligent multilingue._
