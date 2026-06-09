# 📓 Notebooks Colab / Kaggle — FSBM Platform IA

Ce dossier contient des notebooks Jupyter pour expérimenter avec l'IA en dehors du projet principal.

## Notebooks disponibles

### `fsbm_groq_demo.ipynb`
Démo complète Groq + LLaMA 3.3 + RAG.

**Contenu :**
- Connexion à Groq en 5 lignes
- Implémentation RAG (TF-IDF + LLM)
- Comparaison LLaMA 3-8B vs 3.3-70B
- Conversation multi-tour avec mémoire

**Utilisation Google Colab :**
1. Aller sur https://colab.research.google.com/
2. **File → Upload notebook** → choisir `fsbm_groq_demo.ipynb`
3. **Runtime → Change runtime type → GPU T4** (recommandé)
4. **Secrets (clé en bas à gauche)** → Add new secret `GROQ_API_KEY`
5. Exécuter cellule par cellule

**Utilisation Kaggle :**
1. Aller sur https://www.kaggle.com/code
2. **+ New Notebook**
3. **File → Import Notebook** → uploader `fsbm_groq_demo.ipynb`
4. **Add-ons → Secrets** → ajouter `GROQ_API_KEY`
5. **Settings → Accelerator → GPU T4 x2**
6. Run All

## Pré-requis : obtenir une clé Groq gratuite

1. Aller sur https://console.groq.com
2. Sign up gratuit (Google ou email)
3. https://console.groq.com/keys → Create API Key
4. Copier la clé qui commence par `gsk_...`

## Pourquoi Colab / Kaggle ?

- **Gratuit** : pas besoin d'un PC puissant
- **GPU** : T4 (Colab) ou T4 x2 (Kaggle) pour tests poussés
- **Partage facile** : envoyer un lien au jury
- **Reproducible** : tout le monde a le même environnement

## Pour aller plus loin

Le code production-grade est dans `services/chatbot-service/app/llm/` :
- `groq_client.py` — client Groq robuste
- `rag.py` — RAG avec multi-langue
- `llm_service.py` — orchestrateur avec fallback
