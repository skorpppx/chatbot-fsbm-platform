# 🏛️ Architecture — Plateforme Intelligente FSBM

> **Projet de Fin d'Études 2025/2026**
> Faculté des Sciences Ben M'Sick — Université Hassan II de Casablanca
> Équipe : AKRAM BELMOUSSA · ZAKARIA · NOUHAILA

---

## 1. Vue d'ensemble

La plateforme FSBM est une application universitaire intelligente bâtie autour d'une **architecture micro-services** :

```
                        ┌──────────────────────────────┐
                        │   Frontend Angular 17 (SPA)  │
                        │   Port 4200                  │
                        └───────────────┬──────────────┘
                                        │ HTTP/JSON
                  ┌─────────────────────┼─────────────────────┐
                  │                     │                     │
       ┌──────────▼─────────┐ ┌─────────▼────────┐ ┌──────────▼──────────┐
       │  chatbot-service   │ │ academic-service │ │   student-service   │
       │      :5001         │ │      :5002       │ │       :5003         │
       │  FastAPI + NLP     │ │  FastAPI + SQLA  │ │  FastAPI + JWT      │
       └──────────┬─────────┘ └────────┬─────────┘ └──────────┬──────────┘
                  │                    │                      │
                  └─────────┬──────────┴──────────┬───────────┘
                            │                     │
                  ┌─────────▼─────────┐ ┌─────────▼─────────┐
                  │      MySQL 8      │ │   MongoDB 7       │
                  │  Données métier   │ │  Reviews & logs   │
                  └───────────────────┘ └───────────────────┘
                            ▲                     ▲
                            │                     │
       ┌──────────▼─────────┐ ┌─────────▼────────┐ ┌──────────▼──────────┐
       │  review-service    │ │ notification-svc │ │  analytics-service  │
       │      :5004         │ │      :5005       │ │       :5006         │
       │  FastAPI + Mongo   │ │  FastAPI + SSE   │ │  FastAPI + stats    │
       └────────────────────┘ └──────────────────┘ └─────────────────────┘
```

---

## 2. Stack technique

| Couche | Technologie | Raison |
|---|---|---|
| Frontend | Angular 17 (standalone, signals) | Existant, moderne, performant |
| Backend | FastAPI 0.110+ | Async, OpenAPI auto, Pydantic v2, plus moderne que Flask |
| ORM | SQLAlchemy 2.0 (async) | Standard Python, mature, syntaxe moderne |
| BDD relationnelle | MySQL 8.0 | Demandé par cahier des charges PFE |
| BDD documentaire | MongoDB 7 | Reviews, logs, sentiment, flexible |
| NLP | scikit-learn (TF-IDF + Cosine) + spaCy (FR) | Existant amélioré + embeddings sémantiques |
| Auth | JWT (python-jose) | Léger, standard, sans dépendance externe |
| Validation | Pydantic v2 | Native FastAPI |
| Docs API | OpenAPI / Swagger UI | Généré automatiquement par FastAPI |
| Hot-reload | uvicorn --reload | Confort développeur |

> ⚠️ **Pas de Docker** (contrainte du PFE) — exécution locale Windows.

---

## 3. Description des 6 micro-services

### 3.1 `chatbot-service` — Port 5001
**Responsabilités**
- Gestion des conversations
- NLP : TF-IDF + Cosine Similarity (existant) + embeddings sémantiques
- Mémoire conversationnelle par session (Redis-lite en mémoire pour PFE)
- Suggestions automatiques et boutons interactifs
- Apprentissage continu via feedback

**Endpoints principaux**
- `POST /api/chat` — envoyer un message
- `GET /api/chat/history/{session_id}` — historique conversation
- `GET /api/chat/suggestions` — suggestions contextuelles
- `GET /api/intents` — liste des intents
- `POST /api/feedback` — notation des réponses

### 3.2 `academic-service` — Port 5002
**Responsabilités**
- Référentiel académique : départements, filières, modules, professeurs, étudiants
- Gestion des emplois du temps et examens
- Notes et résultats

**Endpoints principaux**
- `GET /api/departments`, `GET /api/departments/{id}`
- `GET /api/filieres`, `GET /api/filieres/{code}`
- `GET /api/modules`, `GET /api/modules/{code}`
- `GET /api/professors`, `GET /api/professors/{id}`
- `GET /api/students` (avec pagination, filtre, recherche)
- `GET /api/schedule/{filiere}/{semestre}`
- `GET /api/exams/{filiere}/{session}`

### 3.3 `student-service` — Port 5003
**Responsabilités**
- Authentification JWT
- Profils étudiants et professeurs
- Rôles (étudiant, prof, admin, scolarité)
- Préférences

**Endpoints principaux**
- `POST /api/auth/login`, `POST /api/auth/register`
- `GET /api/me` — profil courant
- `PUT /api/me/preferences`
- `GET /api/users` (admin only)

### 3.4 `review-service` — Port 5004 (MongoDB)
**Responsabilités**
- Feedbacks chatbot (👍/👎/étoiles)
- Reviews textuelles
- Sentiment analysis (positif/neutre/négatif)
- Suggestions d'amélioration

**Collections**
- `reviews`, `feedbacks`, `sentiments`

### 3.5 `notification-service` — Port 5005
**Responsabilités**
- Annonces universitaires
- Rappels d'examens
- Événements (conférences, clubs)
- Server-Sent Events (SSE) pour push temps réel

**Endpoints**
- `GET /api/notifications` — liste
- `GET /api/notifications/stream` — SSE
- `POST /api/announcements` (admin)

### 3.6 `analytics-service` — Port 5006
**Responsabilités**
- Statistiques globales chatbot
- Questions fréquentes en temps réel
- Tracking utilisateur anonymisé
- Tableaux de bord administrateur

**Endpoints**
- `GET /api/stats/overview`
- `GET /api/stats/top-intents`
- `GET /api/stats/satisfaction`
- `GET /api/stats/usage-by-hour`

---

## 4. Communication inter-services

Modèle **REST synchrone** simple (suffisant pour un PFE) :
- `chatbot-service` appelle `academic-service` pour enrichir ses réponses avec des données fraîches (ex. liste à jour des filières).
- `analytics-service` lit en read-only les BDD des autres services.
- Pas de bus de messages (pas de Kafka/RabbitMQ) pour rester simple.

Pour une vraie production on ajouterait : API Gateway (Kong/Traefik), service discovery (Consul), bus async (NATS).

---

## 5. Bases de données

### 5.1 MySQL — `fsbm_db` (schéma normalisé)

```
departments ── 1:n ── filieres ── 1:n ── modules
                          │                  │
                          │                  └─ n:m ── professors (teaches)
                          │
                          └─ 1:n ── students
                                       │
                                       └─ 1:n ── grades

schedules (filiere, module, salle, jour, horaire)
exams     (module, date, salle, surveillants, session)
faq_categories ── 1:n ── faq_items
announcements
news, events, clubs
```

Voir [database/mysql/01_schema.sql](../database/mysql/01_schema.sql) pour le DDL complet (16 tables, clés étrangères, index, contraintes).

### 5.2 MongoDB — `fsbm_reviews`

Collections :
- `reviews` : feedback étudiant détaillé
- `chatbot_feedback` : 👍/👎 par message
- `conversations` : log complet des sessions
- `sentiment_analysis` : résultats NLP de sentiment
- `usage_logs` : tracking d'utilisation

Voir [database/mongodb/init.js](../database/mongodb/init.js).

---

## 6. Sécurité

| Couche | Mesure |
|---|---|
| Auth | JWT signé HS256, expiration 24h, refresh token |
| Rôles | `student`, `professor`, `admin`, `scolarite` |
| Mots de passe | bcrypt (12 rounds) |
| Validation | Pydantic v2 sur tous les inputs |
| CORS | Liste blanche `localhost:4200` en dev |
| Rate limiting | slowapi (60 req/min/IP) |
| SQL injection | SQLAlchemy paramétré uniquement |
| Routes Angular | `AuthGuard` + `RoleGuard` |

---

## 7. Frontend — Architecture Angular

```
frontend/src/app/
├── core/                  # Services globaux, intercepteurs, guards
│   ├── auth/
│   ├── http-interceptors/
│   └── services/
├── shared/                # Composants réutilisables, pipes, directives
│   ├── components/
│   ├── pipes/
│   └── theme/             # Mode sombre, palette
├── features/              # Modules fonctionnels (lazy-loaded)
│   ├── home/              # Existant — préservé
│   ├── chat/              # Existant — modernisé
│   ├── dashboard/         # NOUVEAU — vue étudiant
│   ├── academic/          # NOUVEAU — départements, filières, modules
│   ├── schedule/          # NOUVEAU — emploi du temps
│   ├── exams/             # NOUVEAU — examens & résultats
│   ├── news/              # NOUVEAU — actualités
│   └── reviews/           # NOUVEAU — feedbacks étudiants
└── layouts/               # Header, footer, sidebar
```

Routes lazy-loaded pour de meilleures performances.

---

## 8. Roadmap de développement

### ✅ Phase 1 — Fondations (cette session)
- [x] Architecture documentée
- [x] Scaffolding complet
- [x] MySQL schéma + seed data réaliste
- [x] `chatbot-service` v2 FastAPI
- [x] `academic-service` complet
- [x] Dataset FAQ enrichi (60+ intents)
- [x] Frontend Angular copié et préservé
- [x] Logos intégrés

### 🚧 Phase 2 — Authentification & MongoDB (prochaine session)
- [ ] `student-service` complet (JWT, rôles)
- [ ] `review-service` MongoDB
- [ ] Auth Guards Angular

### 🚧 Phase 3 — Vue étudiant & UI moderne
- [ ] Dashboard étudiant
- [ ] Pages académiques modernes
- [ ] Mode sombre, animations
- [ ] Page reviews

### 🚧 Phase 4 — Notifications & Analytics
- [ ] `notification-service` + SSE
- [ ] `analytics-service` + dashboard admin

---

## 9. Choix d'architecture justifiés (pour la soutenance)

| Décision | Justification |
|---|---|
| Micro-services au lieu de monolithe | Démonstration de compétences modernes, scalabilité, séparation des responsabilités |
| FastAPI au lieu de Flask | Performance async, validation native, OpenAPI auto, modernité |
| MySQL + MongoDB combinés | Démontre la maîtrise SQL **et** NoSQL — exactement ce qu'attend un jury PFE |
| Angular 17 standalone | Architecture moderne, pas de NgModule, signals, hydration |
| JWT au lieu de sessions | Stateless, scalable, compatible micro-services |
| Pas de Docker | Contrainte du cahier des charges, déploiement Windows direct |

---

## 10. Identité visuelle

- Logo FSBM : `frontend/src/assets/logos/fsbm.png`
- Logo Département Math-Info : `frontend/src/assets/logos/dept-math-info.png`
- Palette principale (FSBM) : `#1C3F6E` → `#3A7BD5`
- Palette d'accent (Département) : `#16B5A6` (teal du logo)
- Typographie : Inter / Segoe UI

Voir [design-system.md](./design-system.md) (à venir Phase 3).
