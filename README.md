# 🎓 FSBM Platform — Chatbot Intelligent & Référentiel Académique

> **Projet de Fin d'Études 2025/2026**
> Faculté des Sciences Ben M'Sick — Université Hassan II de Casablanca
> Filière Développement Informatique

---

## 👥 Équipe

| Membre | Rôle |
|--------|------|
| **AKRAM BELMOUSSA** | Architecte Backend & Intégration NLP |
| **ZAKARIA** | Frontend Angular & UX/UI |
| **NOUHAILA** | Base de Données & Contenu FAQ |

---

## 🏛️ Vue d'ensemble

Plateforme universitaire intelligente complète bâtie sur **architecture micro-services** :

```
┌────────────────────────────────────────────────────────────────┐
│                  Frontend Angular 17 (Port 4200)               │
└─────────────────────────┬──────────────────────────────────────┘
                          │ HTTP/JSON (via proxy.conf.json)
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
┌─────────────────┐                ┌──────────────────┐
│ chatbot-service │                │ academic-service │
│   FastAPI :5001 │ ◀────HTTP────▶ │  FastAPI :5002   │
│  NLP TF-IDF v2  │                │ Référentiel univ │
└────────┬────────┘                └─────────┬────────┘
         │                                   │
         └─────────────┬─────────────────────┘
                       ▼
                  MySQL 8.0
                  fsbm_db
```

**Phase 1 implémentée** (cette livraison) :
- ✅ Architecture micro-services
- ✅ 2 micro-services FastAPI complets (chatbot + academic)
- ✅ MySQL : 16 tables, ~3000 étudiants, ~107 profs, 100+ modules
- ✅ MongoDB : 6 collections (reviews, feedbacks, sentiments…)
- ✅ NLP amélioré : TF-IDF n-grammes, mémoire conversationnelle, suggestions
- ✅ Dataset FAQ enrichi : 60+ intents (vs 24 initial)
- ✅ Frontend Angular 17 préservé + service academic.service.ts ajouté
- ✅ Logos FSBM + Département intégrés

**Phase 2 prévue** (prochaine itération) :
- ⏳ student-service (JWT, rôles, profils)
- ⏳ review-service (MongoDB CRUD)
- ⏳ notification-service (SSE)
- ⏳ analytics-service (dashboards admin)
- ⏳ Modernisation UI Angular : dashboard, mode sombre, nouvelles pages

> 📖 Documentation complète d'architecture : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📦 Stack technique

| Couche | Techno | Version |
|---|---|---|
| Frontend | Angular | 17.3 (standalone) |
| Backend | Python + FastAPI | 3.10+, FastAPI 0.110+ |
| ORM | SQLAlchemy async | 2.0+ |
| BDD relationnelle | MySQL | 8.0 |
| BDD documentaire | MongoDB | 7.0 |
| NLP | scikit-learn + NLTK | 1.4+ |
| Docs API | OpenAPI/Swagger | auto-générée |

---

## 🚀 Lancement complet (Windows)

### Pré-requis
- **Python 3.10+** ([python.org](https://www.python.org/downloads/) — cocher « Add to PATH »)
- **Node.js 18+** ([nodejs.org](https://nodejs.org))
- **MySQL 8.0+** ([dev.mysql.com](https://dev.mysql.com/downloads/installer/))
- **MongoDB 7+** ([mongodb.com](https://www.mongodb.com/try/download/community)) — *optionnel pour la Phase 1*
- **Git** ([git-scm.com](https://git-scm.com/))

### Étape 1 — Préparer la base MySQL

```cmd
:: Ouvrir un terminal MySQL
mysql -u root -p

:: Dans MySQL, exécuter dans l'ordre :
SOURCE C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\database\mysql\01_schema.sql;
SOURCE C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\database\mysql\02_seed_static.sql;
SOURCE C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\database\mysql\03_seed_modules.sql;
SOURCE C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\database\mysql\04_seed_data.sql;
exit;
```

✅ Tu obtiens : `fsbm_db` avec 5 départements, 25 filières (7L + 18M), 100+ modules, 107 profs, 2970 étudiants, 5 annonces, 5 événements, 8 clubs, 60+ intents FAQ.

> 💡 Si `04_seed_data.sql` n'existe pas, lance le générateur :
> ```cmd
> cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\database\seed
> py generate_data.py
> ```

### Étape 2 — Initialiser MongoDB (optionnel Phase 1)

```cmd
:: Démarrer le service mongod, puis :
mongosh < C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\database\mongodb\init.js
```

✅ Tu obtiens : base `fsbm_reviews` avec 6 collections + 5 reviews + 4 suggestions seed.

### Étape 3 — Démarrer le chatbot-service (Port 5001)

Ouvrir un **premier** terminal :

```cmd
cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\services\chatbot-service

:: Créer l'environnement virtuel
py -m venv venv
venv\Scripts\activate

:: Installer les dépendances
pip install -r requirements.txt

:: Configurer (copier .env.example en .env et adapter)
copy .env.example .env
:: → éditer .env et mettre votre mot de passe MySQL

:: Lancer le service
py -m uvicorn app.main:app --reload --port 5001
```

🌐 Vérifier :
- API : http://localhost:5001
- **Documentation Swagger** : http://localhost:5001/docs
- Health : http://localhost:5001/api/health

### Étape 4 — Démarrer le academic-service (Port 5002)

Ouvrir un **deuxième** terminal :

```cmd
cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\services\academic-service

py -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env
:: → éditer .env

py -m uvicorn app.main:app --reload --port 5002
```

🌐 Vérifier :
- API : http://localhost:5002
- **Swagger** : http://localhost:5002/docs
- Overview : http://localhost:5002/api/overview

### Étape 5 — Démarrer le frontend Angular (Port 4200)

Ouvrir un **troisième** terminal :

```cmd
cd C:\Users\belmo\studies\PFE\chatbot-fsbm-platform\frontend

npm install
npm start
```

🌐 Ouvrir : **http://localhost:4200**

> 🎉 Le chatbot répond, et le proxy redirige `/api/chat` vers le chatbot-service et `/api/academic/*` vers l'academic-service.

---

## 📂 Structure du projet

```
chatbot-fsbm-platform/
├── README.md                         (ce fichier)
├── docs/
│   └── ARCHITECTURE.md               (architecture détaillée)
├── database/
│   ├── mysql/
│   │   ├── 01_schema.sql             (16 tables, contraintes, index)
│   │   ├── 02_seed_static.sql        (départements, filières, masters)
│   │   ├── 03_seed_modules.sql       (modules par filière)
│   │   └── 04_seed_data.sql          (auto-généré, ~720 KB)
│   ├── mongodb/
│   │   └── init.js                   (collections + seed reviews)
│   └── seed/
│       └── generate_data.py          (générateur Python)
├── services/
│   ├── chatbot-service/              ✅ FastAPI port 5001
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/                 (config, memory, database)
│   │   │   ├── nlp/                  (classifier, preprocessor)
│   │   │   ├── models/               (Pydantic schemas)
│   │   │   └── routers/              (chat, intents, system)
│   │   ├── data/faq_dataset.json    (60+ intents)
│   │   └── requirements.txt
│   ├── academic-service/             ✅ FastAPI port 5002
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/
│   │   │   ├── db/                   (SQLAlchemy session)
│   │   │   ├── models/entities.py    (ORM)
│   │   │   ├── schemas/              (Pydantic)
│   │   │   └── routers/              (8 routers complets)
│   │   └── requirements.txt
│   ├── student-service/              ⏳ Phase 2
│   ├── review-service/               ⏳ Phase 2
│   ├── notification-service/         ⏳ Phase 2
│   └── analytics-service/            ⏳ Phase 2
├── frontend/                         ✅ Angular 17 (préservé)
│   ├── src/app/
│   │   ├── components/               (chat-window, home-page, etc.)
│   │   ├── services/
│   │   │   ├── chat.service.ts       (existant)
│   │   │   └── academic.service.ts   ⭐ NOUVEAU
│   │   └── models/message.model.ts
│   ├── src/assets/logos/
│   │   ├── fsbm.png                  (logo officiel)
│   │   ├── fsbm-banner.png           (variante bannière)
│   │   └── dept-math-info.png        (logo département)
│   ├── proxy.conf.json               (mis à jour)
│   ├── angular.json
│   └── package.json
└── shared/python/                    (utilitaires partagés Phase 2)
```

---

## 🌐 Endpoints principaux

### chatbot-service (`:5001`)

| Méthode | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Envoyer un message au chatbot |
| `POST` | `/api/chat/feedback` | Noter une réponse |
| `GET` | `/api/chat/history/{session_id}` | Historique d'une session |
| `GET` | `/api/chat/suggestions` | Questions suggérées |
| `GET` | `/api/intents` | Liste des 60+ intents |
| `GET` | `/api/health` | Statut |
| `GET` | `/api/stats` | Statistiques globales |

### academic-service (`:5002`)

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/overview` | Compteurs globaux (dashboard) |
| `GET` | `/api/departments` | Liste des 5 départements |
| `GET` | `/api/departments/{id}` | Détail département |
| `GET` | `/api/filieres` | Filières (filtres : type, dept, recherche) |
| `GET` | `/api/filieres/code/{code}` | Filière par code (SMI, DI, IADS…) |
| `GET` | `/api/filieres/{id}/modules` | Modules par semestre |
| `GET` | `/api/modules` | Liste des modules |
| `GET` | `/api/professors` | Liste paginée des profs |
| `GET` | `/api/students` | Liste paginée des étudiants |
| `GET` | `/api/schedule` | Emploi du temps |
| `GET` | `/api/exams` | Calendrier des examens |
| `GET` | `/api/announcements` | Annonces officielles |
| `GET` | `/api/events` | Événements universitaires |
| `GET` | `/api/clubs` | Clubs étudiants |

---

## 🧪 Tester rapidement

### Test 1 — Envoyer un message au chatbot

```cmd
curl -X POST http://localhost:5001/api/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Comment m'inscrire en master IADS ?\"}"
```

Réponse attendue :
```json
{
  "response": "🤖 Master IADS — Intelligence Artificielle...",
  "intent": "master_iads",
  "confidence": 0.78,
  "conversation_id": 1,
  "suggestions": ["Quels masters", "Master sécurité", ...],
  ...
}
```

### Test 2 — Lister les filières via academic-service

```cmd
curl http://localhost:5002/api/filieres?type=MASTER
```

### Test 3 — Overview pour dashboard

```cmd
curl http://localhost:5002/api/overview
```

Réponse :
```json
{
  "departments": 5,
  "filieres": 25,
  "modules": 100,
  "professors": 107,
  "students": 2970,
  ...
}
```

---

## 🎨 Identité visuelle

| Élément | Valeur |
|---|---|
| Couleur primaire FSBM | `#1C3F6E` (bleu marine) |
| Couleur secondaire | `#265DAB` / `#3A7BD5` |
| Accent département Math-Info | `#16B5A6` (teal du logo) |
| Typographie | Inter / Segoe UI |
| Logo principal | `assets/logos/fsbm.png` |
| Logo département | `assets/logos/dept-math-info.png` |

---

## 🛡️ Sécurité & qualité

| Mesure | Statut |
|---|---|
| Validation Pydantic v2 sur tous les inputs | ✅ |
| CORS configuré | ✅ |
| SQLAlchemy paramétré (anti-injection) | ✅ |
| Documentation OpenAPI auto | ✅ |
| Pagination des listes longues | ✅ |
| Gestion d'erreurs HTTP propres | ✅ |
| JWT + rôles | ⏳ Phase 2 |
| Rate limiting | ⏳ Phase 2 |
| Tests pytest | ⏳ Phase 2 |

---

## 📊 Données réalistes générées

- **107 professeurs** (Math-Info: 35, Physique: 18, Chimie: 17, Biologie: 22, Géologie: 15) avec grades PA/PH/PES/Vacataire, spécialités cohérentes
- **2970 étudiants** avec noms marocains authentiques (Alaoui, Bennani, Tazi, Chaoui…), CNE valides, emails universitaires, groupes
- **100+ modules** détaillés (SMI, DI, autres filières + Master IADS 13 modules)
- **Examens** sessions hiver/été/rattrapage
- **Notes & résultats** avec compensation et mentions

---

## 🐛 Dépannage

### Le chatbot ne répond pas (ECONNREFUSED)
→ Vérifier que `chatbot-service` tourne sur le port 5001 : `curl http://localhost:5001/api/health`

### Erreur MySQL "Access denied"
→ Vérifier les credentials dans `services/chatbot-service/.env` et `services/academic-service/.env`

### Erreur d'encodage Python sur Windows
→ Avant de lancer : `set PYTHONIOENCODING=utf-8`

### Le proxy Angular ne fonctionne pas
→ Redémarrer `npm start` après modification de `proxy.conf.json`

### NLTK Snowball indisponible
→ Le préprocesseur fonctionne sans (juste pas de stemming). Pour l'activer :
```python
import nltk
nltk.download('stopwords')
```

---

## 📄 Licence

Projet académique — Faculté des Sciences Ben M'Sick — 2025/2026.
Code libre d'utilisation à des fins pédagogiques.
