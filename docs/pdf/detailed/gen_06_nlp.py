"""PDF 6 - NLP + IA chatbot Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 06/10", "NLP + IA du Chatbot",
           "TF-IDF + Cosine + RAG + LLaMA + Memoire conversationnelle",
           accent_color=HexColor('#A855F7'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - C'est quoi le NLP ?", "3"),
    ("Chapitre 2 - Pipeline NLP complet", "6"),
    ("Chapitre 3 - Tokenisation", "9"),
    ("Chapitre 4 - Stopwords et stemming", "12"),
    ("Chapitre 5 - TF-IDF en details", "15"),
    ("Chapitre 6 - Cosine similarity", "20"),
    ("Chapitre 7 - n-grammes", "24"),
    ("Chapitre 8 - Detection de langue", "27"),
    ("Chapitre 9 - Multilingue (FR/EN/Darija)", "30"),
    ("Chapitre 10 - Memoire conversationnelle", "33"),
    ("Chapitre 11 - Personnalisation (genre/nom)", "36"),
    ("Chapitre 12 - LLM (LLaMA 3 + Groq)", "39"),
    ("Chapitre 13 - RAG = retrieval + generation", "43"),
    ("Chapitre 14 - Embeddings (vectorielle moderne)", "47"),
    ("Chapitre 15 - Conclusion", "50"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1
story.append(Paragraph("Chapitre 1 - C'est quoi le NLP ?", ST_CHAPTER))

story.append(Paragraph("1.1 Definition", ST_H1))
story.append(Paragraph(
    "<b>NLP = Natural Language Processing = Traitement Automatique du Langage Naturel</b>. "
    "C'est le domaine de l'IA qui permet aux ordinateurs de <b>comprendre, analyser et "
    "generer du langage humain</b>.",
    ST_BODY))

story.append(analogy(
    "Sans NLP, un ordinateur ne fait QUE du calcul mathematique. Avec NLP, il peut "
    "comprendre 'Bonjour, comment vas-tu ?' et repondre intelligemment. C'est ce qui fait "
    "la difference entre une calculatrice et Siri."))

story.append(Paragraph("1.2 Applications du NLP", ST_H1))
for x in [
    "<b>Assistants conversationnels</b> : ChatGPT, Siri, Alexa, notre chatbot FSBM",
    "<b>Traduction automatique</b> : Google Translate, DeepL",
    "<b>Analyse de sentiment</b> : detecter si un texte est positif/negatif",
    "<b>Resume automatique</b> : YouTube auto-resume, ChatGPT",
    "<b>Reconnaissance d'entites</b> : extraire noms, dates, lieux d'un texte",
    "<b>Classification de spam</b> : ton mail le fait deja",
    "<b>Detection de plagiat</b> : Turnitin, Compilatio",
    "<b>Recherche semantique</b> : Google Search comprend le sens, pas juste les mots",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("1.3 Les 2 ecoles", ST_H1))
story.append(std_table([
    ['Approche', 'Methode', 'Exemples'],
    ['Statistique', 'TF-IDF, regex, n-grammes', 'Notre chatbot v1'],
    ['Deep learning', 'Reseaux de neurones, transformers', 'ChatGPT, BERT, LLaMA'],
], col_widths=[3*cm, 5*cm, 8*cm]))

story.append(alert_box(
    "Notre projet combine les deux : <b>TF-IDF (statistique)</b> pour le retrieval rapide, "
    "<b>LLaMA 3 (deep learning)</b> pour la generation contextuelle.",
    kind="tip"))
story.append(PageBreak())

# CH 2 - Pipeline
story.append(Paragraph("Chapitre 2 - Pipeline NLP complet", ST_CHAPTER))

story.append(Paragraph("2.1 Vue d'ensemble", ST_H1))
story.append(diagram(
    "    Message brut\n"
    "    'Salam khoya, kifash ntsajjel f master IADS ?'\n"
    "         |\n"
    "         v\n"
    "    [1] Detection de langue\n"
    "    -> 'darija' (confidence 1.0)\n"
    "         |\n"
    "         v\n"
    "    [2] Pretraitement\n"
    "       a) lowercasing -> 'salam khoya, kifash...'\n"
    "       b) suppression ponctuation -> 'salam khoya kifash...'\n"
    "       c) tokenisation -> ['salam', 'khoya', 'kifash', ...]\n"
    "       d) suppression stopwords -> ['salam', 'khoya', 'kifash', ...]\n"
    "       e) stemming (FR uniquement) -> ['salam', 'khoy', 'kifash', ...]\n"
    "         |\n"
    "         v\n"
    "    [3] Vectorisation TF-IDF\n"
    "    -> vecteur de dimensions ~1500 (Darija)\n"
    "         |\n"
    "         v\n"
    "    [4] Cosine similarity\n"
    "       comparaison contre 461 patterns d'entrainement\n"
    "         |\n"
    "         v\n"
    "    [5] Top-K + selection intent gagnant\n"
    "    -> intent='master_iads' (confidence 0.78)\n"
    "         |\n"
    "         v\n"
    "    [6] Recuperation reponse pre-ecrite\n"
    "    -> 'Master IADS - IA & Data Science...'\n"
    "         |\n"
    "         v\n"
    "    [7] Personnalisation\n"
    "       a) substitution {voc} -> 'khoya'\n"
    "       b) substitution {name} -> ''\n"
    "         |\n"
    "         v\n"
    "    Reponse finale a l'utilisateur"
))

story.append(Paragraph("2.2 Latences typiques", ST_H1))
story.append(std_table([
    ['Etape', 'Temps'],
    ['Detection langue', '< 1 ms'],
    ['Pretraitement', '2-5 ms'],
    ['Vectorisation TF-IDF', '10-15 ms'],
    ['Cosine similarity', '20-30 ms'],
    ['Selection top-K', '< 1 ms'],
    ['Personnalisation', '< 1 ms'],
    ['Total NLP', '35-50 ms'],
], col_widths=[8*cm, 8*cm]))
story.append(PageBreak())

# CH 3 - Tokenisation
story.append(Paragraph("Chapitre 3 - Tokenisation", ST_CHAPTER))

story.append(Paragraph("3.1 C'est quoi un token ?", ST_H1))
story.append(Paragraph(
    "Un <b>token</b> est une <b>unite atomique</b> de texte. Pour notre NLP statistique, un "
    "token = un mot (apres nettoyage). Pour un LLM, c'est un sous-mot.",
    ST_BODY))

story.append(Paragraph("3.2 Exemple concret", ST_H1))
story.append(code(
    "Phrase : 'Bonjour, comment allez-vous ?'\n"
    "\n"
    "Etape 1 : enlever la ponctuation\n"
    "  -> 'Bonjour comment allez vous'\n"
    "\n"
    "Etape 2 : mettre en minuscules\n"
    "  -> 'bonjour comment allez vous'\n"
    "\n"
    "Etape 3 : decouper en tokens (split sur espace)\n"
    "  -> ['bonjour', 'comment', 'allez', 'vous']\n"
    "\n"
    "Total : 4 tokens"
))

story.append(Paragraph("3.3 Notre implementation", ST_H1))
story.append(code(
    "# nlp/preprocessor.py\n"
    "import re\n"
    "import unicodedata\n"
    "\n"
    "def tokenize(text: str) -> list[str]:\n"
    "    text = text.lower()\n"
    "    text = re.sub(r'[^\\w\\s]', ' ', text)   # ponctuation -> espaces\n"
    "    text = re.sub(r'\\d+', ' ', text)         # nombres -> espaces\n"
    "    return [t for t in text.split() if t]   # split + remove vides\n"
    "\n"
    "# Usage\n"
    "tokens = tokenize(\"Bonjour, comment allez-vous ?\")\n"
    "# ['bonjour', 'comment', 'allez', 'vous']"
))

story.append(Paragraph("3.4 Gestion des accents", ST_H1))
story.append(Paragraph(
    "Pour que 'eleve' et 'élève' soient consideres identiques :",
    ST_BODY))
story.append(code(
    "def remove_accents(text: str) -> str:\n"
    "    return ''.join(\n"
    "        c for c in unicodedata.normalize('NFD', text)\n"
    "        if unicodedata.category(c) != 'Mn'\n"
    "    )\n"
    "\n"
    "remove_accents('élève préparé')\n"
    "# 'eleve prepare'"
))
story.append(PageBreak())

# CH 4 - Stopwords
story.append(Paragraph("Chapitre 4 - Stopwords et stemming", ST_CHAPTER))

story.append(Paragraph("4.1 C'est quoi un stopword ?", ST_H1))
story.append(Paragraph(
    "Un <b>stopword</b> est un mot tres frequent mais qui apporte <b>peu d'information "
    "semantique</b> : 'le', 'la', 'de', 'et', 'a', 'pour', etc.",
    ST_BODY))

story.append(Paragraph("4.2 Pourquoi les supprimer ?", ST_H1))
for x in [
    "Reduit la taille du vecteur TF-IDF",
    "Concentre le signal sur les mots importants",
    "Les phrases comparees ont la meme structure (pas biaisé par 'le' vs 'la')",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("4.3 Notre liste de stopwords", ST_H1))
story.append(code(
    "STOPWORDS_FR = {\n"
    "    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de',\n"
    "    'et', 'ou', 'mais', 'donc', 'or', 'car',\n"
    "    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils',\n"
    "    'ce', 'cet', 'cette', 'ces',\n"
    "    'qui', 'que', 'quoi', 'dont', 'ou',\n"
    "    'est', 'sont', 'avoir', 'etre', 'faire',\n"
    "    'pas', 'ne', 'plus', 'moins', 'tres',\n"
    "    'pour', 'par', 'avec', 'sans', 'sous', 'sur', 'dans',\n"
    "    'comment', 'pourquoi', 'quand', 'combien',\n"
    "    # ... ~110 mots\n"
    "}\n"
    "\n"
    "tokens = [t for t in tokens if t not in STOPWORDS_FR and len(t) > 1]"
))

story.append(Paragraph("4.4 C'est quoi le stemming ?", ST_H1))
story.append(Paragraph(
    "Le <b>stemming</b> reduit un mot a sa <b>racine</b>. Exemple : 'mangeait', 'mangions', "
    "'mangerai' -> 'mang'. Ainsi, ces 3 mots sont consideres identiques en NLP.",
    ST_BODY))

story.append(Paragraph("4.5 Snowball stemmer (NLTK)", ST_H1))
story.append(code(
    "from nltk.stem.snowball import FrenchStemmer\n"
    "\n"
    "stemmer = FrenchStemmer()\n"
    "\n"
    "stemmer.stem('mangeait')      # 'mang'\n"
    "stemmer.stem('mangerons')     # 'mang'\n"
    "stemmer.stem('etudiant')      # 'etudi'\n"
    "stemmer.stem('etudiante')     # 'etudi'\n"
    "stemmer.stem('etudier')       # 'etudi'\n"
    "\n"
    "# Tous reduits a 'etudi' = consideres identiques"
))

story.append(alert_box(
    "Le stemming n'est PAS du dictionnaire (les stems ne sont pas des mots reels). C'est "
    "une heuristique qui marche bien en pratique.",
    kind="info"))
story.append(PageBreak())

# CH 5 - TF-IDF
story.append(Paragraph("Chapitre 5 - TF-IDF en details", ST_CHAPTER))

story.append(Paragraph("5.1 Intuition", ST_H1))
story.append(Paragraph(
    "<b>TF-IDF = Term Frequency - Inverse Document Frequency</b>. C'est une formule qui "
    "mesure l'<b>importance d'un mot</b> dans un document, en fonction de :",
    ST_BODY))
for x in [
    "<b>TF</b> : frequence du mot dans CE document (plus il apparait, plus important)",
    "<b>IDF</b> : rarete du mot dans TOUS les documents (plus c'est rare, plus c'est discriminant)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(analogy(
    "Pour identifier un livre : <b>TF</b> = combien de fois 'sorcier' apparait dans Harry "
    "Potter. <b>IDF</b> = combien de livres parlent de 'sorcier' (rare). 'le' a un TF eleve "
    "PARTOUT donc IDF faible -> on l'ignore. 'sorcier' a un TF eleve SEULEMENT dans HP -> "
    "tres discriminant."))

story.append(Paragraph("5.2 Formules mathematiques", ST_H1))
story.append(code(
    "TF(t, d)  = (nombre de fois ou t apparait dans d) / (nb total de mots dans d)\n"
    "\n"
    "IDF(t)    = log(N / df(t))\n"
    "  ou N = nombre total de documents\n"
    "     df(t) = nombre de docs qui contiennent t\n"
    "\n"
    "TF-IDF(t, d) = TF(t, d) * IDF(t)"
))

story.append(Paragraph("5.3 Exemple chiffre", ST_H1))
story.append(code(
    "Documents :\n"
    "  D1 = \"comment inscription master IADS\"\n"
    "  D2 = \"comment inscription master MIAGE\"\n"
    "  D3 = \"bonjour comment allez vous\"\n"
    "\n"
    "Pour t = 'master' :\n"
    "  TF(master, D1) = 1/4 = 0.25\n"
    "  TF(master, D2) = 1/4 = 0.25\n"
    "  TF(master, D3) = 0/4 = 0\n"
    "  \n"
    "  IDF(master) = log(3/2) = 0.176\n"
    "\n"
    "  TF-IDF(master, D1) = 0.25 * 0.176 = 0.044\n"
    "  TF-IDF(master, D2) = 0.25 * 0.176 = 0.044\n"
    "  TF-IDF(master, D3) = 0\n"
    "\n"
    "Pour t = 'iads' :\n"
    "  TF(iads, D1) = 1/4 = 0.25\n"
    "  IDF(iads) = log(3/1) = 0.477\n"
    "  TF-IDF(iads, D1) = 0.25 * 0.477 = 0.119\n"
    "\n"
    "'iads' est plus discriminant que 'master' (TF-IDF plus eleve)"
))

story.append(Paragraph("5.4 Implementation avec scikit-learn", ST_H1))
story.append(code(
    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
    "\n"
    "documents = [\n"
    "    \"comment inscription master IADS\",\n"
    "    \"comment inscription master MIAGE\",\n"
    "    \"bonjour comment allez vous\",\n"
    "]\n"
    "\n"
    "vectorizer = TfidfVectorizer(\n"
    "    ngram_range=(1, 3),  # uni + bi + tri-grammes\n"
    "    min_df=1,             # mot doit apparaitre au moins 1 fois\n"
    "    sublinear_tf=True,    # ln(1+tf) au lieu de tf brut\n"
    ")\n"
    "tfidf_matrix = vectorizer.fit_transform(documents)\n"
    "\n"
    "print(vectorizer.get_feature_names_out())\n"
    "print(tfidf_matrix.shape)   # (3, 12) - 3 docs, 12 features"
))
story.append(PageBreak())

# CH 6 - Cosine
story.append(Paragraph("Chapitre 6 - Cosine similarity", ST_CHAPTER))

story.append(Paragraph("6.1 Intuition", ST_H1))
story.append(Paragraph(
    "Une fois qu'on a vectorise les documents, comment savoir lesquels sont <b>similaires</b> ? "
    "On calcule l'<b>angle</b> entre leurs vecteurs.",
    ST_BODY))

story.append(analogy(
    "Imagine que chaque document est une <b>fleche</b> partant de l'origine. Deux fleches "
    "qui pointent dans <b>la meme direction</b> = documents similaires. Deux fleches "
    "<b>perpendiculaires</b> = documents sans rapport. <b>Opposees</b> = contraires."))

story.append(Paragraph("6.2 Formule", ST_H1))
story.append(code(
    "cosine(A, B) = (A . B) / (|A| * |B|)\n"
    "\n"
    "Ou :\n"
    "  A . B  = produit scalaire des vecteurs\n"
    "  |A|    = norme du vecteur A\n"
    "\n"
    "Resultat :\n"
    "  1   = vecteurs identiques (meme direction)\n"
    "  0   = vecteurs perpendiculaires (aucune similitude)\n"
    "  -1  = vecteurs opposes (rare avec TF-IDF qui est >= 0)"
))

story.append(Paragraph("6.3 Pourquoi cosine et pas distance euclidienne ?", ST_H1))
story.append(Paragraph(
    "La distance euclidienne (|A - B|) est sensible a la <b>longueur</b> des documents. Un "
    "long document n'est PAS forcement different d'un court avec le meme contenu. La cosine "
    "ignore la magnitude et compare juste la <b>direction</b> (= le contenu semantique).",
    ST_BODY))

story.append(Paragraph("6.4 Implementation", ST_H1))
story.append(code(
    "from sklearn.metrics.pairwise import cosine_similarity\n"
    "\n"
    "# Vectoriser la query utilisateur\n"
    "query = \"je veux faire master IADS\"\n"
    "query_vec = vectorizer.transform([query])\n"
    "\n"
    "# Calculer la similarite avec tous les documents d'entrainement\n"
    "sims = cosine_similarity(query_vec, tfidf_matrix)[0]\n"
    "\n"
    "# sims est un array : [sim_avec_D1, sim_avec_D2, sim_avec_D3]\n"
    "print(sims)\n"
    "# [0.85, 0.42, 0.05]  -> D1 est la plus pertinente"
))

story.append(Paragraph("6.5 Top-K candidats", ST_H1))
story.append(code(
    "import numpy as np\n"
    "\n"
    "# Trier les indices par similarite decroissante\n"
    "top_indices = np.argsort(sims)[::-1][:5]\n"
    "\n"
    "# top_indices = [0, 1, 2, ...] (indices de documents)\n"
    "for idx in top_indices:\n"
    "    score = sims[idx]\n"
    "    intent_tag = pattern_to_intent[idx]\n"
    "    print(f'{intent_tag}: {score:.3f}')"
))
story.append(PageBreak())

# CH 7 - n-grammes
story.append(Paragraph("Chapitre 7 - n-grammes", ST_CHAPTER))

story.append(Paragraph("7.1 C'est quoi un n-gramme ?", ST_H1))
story.append(Paragraph(
    "Un <b>n-gramme</b> est une <b>sequence de N tokens consecutifs</b>. Au lieu de "
    "considerer les mots isolement, on considere aussi leurs combinaisons.",
    ST_BODY))

story.append(Paragraph("7.2 Exemple", ST_H1))
story.append(code(
    "Phrase : 'comment m_inscrire en master IADS'\n"
    "\n"
    "Unigrammes (1-grammes) :\n"
    "  ['comment', 'minscrire', 'master', 'IADS']\n"
    "\n"
    "Bigrammes (2-grammes) :\n"
    "  ['comment minscrire', 'minscrire master', 'master IADS']\n"
    "\n"
    "Trigrammes (3-grammes) :\n"
    "  ['comment minscrire master', 'minscrire master IADS']"
))

story.append(Paragraph("7.3 Pourquoi utiles ?", ST_H1))
story.append(Paragraph(
    "Les n-grammes capturent les <b>expressions composees</b> qui ont un sens different "
    "de leurs mots isoles.",
    ST_BODY))
for x in [
    "'pomme de terre' n'est PAS 'pomme' + 'de' + 'terre' separes",
    "'emploi du temps' est une expression specifique",
    "'master IADS' n'est PAS 'master' generique + 'IADS'",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("7.4 Configuration scikit-learn", ST_H1))
story.append(code(
    "vectorizer = TfidfVectorizer(\n"
    "    ngram_range=(1, 3),   # uni + bi + tri-grammes\n"
    ")\n"
    "\n"
    "# Pour 'master IADS' avec ngram_range=(1,3) :\n"
    "# - unigrammes : 'master', 'IADS'\n"
    "# - bigramme  : 'master IADS'\n"
    "# - trigrammes : aucun (trop court)"
))

story.append(alert_box(
    "Notre projet utilise <code>ngram_range=(1, 3)</code> qui capture beaucoup d'expressions "
    "FSBM specifiques : 'emploi du temps', 'master IADS', 'kifash ntsajjel', etc.",
    kind="tip"))
story.append(PageBreak())

# CH 8 - Detection langue
story.append(Paragraph("Chapitre 8 - Detection de langue", ST_CHAPTER))

story.append(Paragraph("8.1 Pourquoi detecter la langue ?", ST_H1))
story.append(Paragraph(
    "Si l'utilisateur ecrit en darija, on veut chercher dans les patterns darija et repondre "
    "en darija. Si en francais, idem. La detection doit se faire <b>avant</b> le matching.",
    ST_BODY))

story.append(Paragraph("8.2 Notre algorithme (hybride)", ST_H1))
story.append(Paragraph(
    "On combine 3 strategies en cascade :",
    ST_BODY))
for n, d in [
    ("1. Caracteres arabes",
     "Si le message contient des caracteres Unicode arabes -> darija/arabe."),
    ("2. Chiffres-lettres",
     "Les chiffres 3, 7, 9, 8 dans des mots latins sont des marqueurs darija forts. "
     "Ex: '3am' (annee), '7biba' (mon amour), '9rib' (proche)."),
    ("3. Score lexical",
     "Comptage des mots-cles distinctifs par langue. ~110 mots FR, 100+ EN, 80+ darija."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("8.3 Mots-cles distinctifs", ST_H1))
story.append(code(
    "DARIJA_KEYWORDS = {\n"
    "    'ana', 'nta', 'nti', 'wesh', 'wach',\n"
    "    'kifash', 'kif', 'ach', 'achno', 'chno',\n"
    "    'fin', 'imta', 'bghit', 'kandir',\n"
    "    'khdma', 'khassek', 'shokran', 'salam',\n"
    "    'labas', 'bslama', 'marhba', 'mzyan',\n"
    "    'kanstress', 'kanhass', 'ma3andich',\n"
    "    # ... ~80 mots\n"
    "}\n"
    "\n"
    "FRENCH_KEYWORDS = {\n"
    "    'le', 'la', 'je', 'tu', 'comment', 'pourquoi',\n"
    "    'inscription', 'master', 'filiere', 'examen',\n"
    "    # ... ~110 mots\n"
    "}\n"
    "\n"
    "ENGLISH_KEYWORDS = {\n"
    "    'the', 'is', 'are', 'how', 'what',\n"
    "    'master', 'enrollment', 'student',\n"
    "    # ... ~100 mots\n"
    "}"
))

story.append(Paragraph("8.4 Algorithme final", ST_H1))
story.append(code(
    "def detect_language(text: str, default='fr') -> str:\n"
    "    # 1. Caracteres arabes ?\n"
    "    if has_arabic_script(text):\n"
    "        return 'darija'\n"
    "    \n"
    "    tokens = tokenize(text.lower())\n"
    "    tokens_set = set(tokens)\n"
    "    \n"
    "    # 2. Chiffres-lettres darija ?\n"
    "    if has_darija_numerals(tokens):\n"
    "        return 'darija'\n"
    "    \n"
    "    # 3. Score lexical\n"
    "    fr  = len(tokens_set & FRENCH_KEYWORDS)\n"
    "    en  = len(tokens_set & ENGLISH_KEYWORDS)\n"
    "    dar = len(tokens_set & DARIJA_KEYWORDS)\n"
    "    \n"
    "    total = fr + en + dar\n"
    "    if total == 0:\n"
    "        return default\n"
    "    \n"
    "    scores = {'fr': fr, 'en': en, 'darija': dar}\n"
    "    return max(scores, key=scores.get)"
))

story.append(alert_box(
    "Taux de detection : <b>14/14 tests reussis</b> (100%). Fonctionne sans aucune "
    "dependance externe (pas langdetect, pas cld3) - tout en Python pur.",
    kind="success"))
story.append(PageBreak())

# CH 9 - Multilingue
story.append(Paragraph("Chapitre 9 - Multilingue (FR/EN/Darija)", ST_CHAPTER))

story.append(Paragraph("9.1 Strategie : 3 modeles paralleles", ST_H1))
story.append(Paragraph(
    "Au lieu d'avoir un seul modele qui melange les 3 langues, on entraine <b>3 modeles "
    "TF-IDF separes</b>, un par langue. Cela donne :",
    ST_BODY))
for x in [
    "Vocabulaire distinct par langue (pas de pollution)",
    "Meilleur matching dans la langue native",
    "Possibilite d'enrichir une langue sans toucher les autres",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("9.2 Structure du dataset", ST_H1))
story.append(code(
    "// faq_dataset.json\n"
    "{\n"
    "  \"version\": \"3.2.0\",\n"
    "  \"languages\": [\"fr\", \"en\", \"darija\"],\n"
    "  \"intents\": [\n"
    "    {\n"
    "      \"tag\": \"inscription\",\n"
    "      \"patterns\": {\n"
    "        \"fr\": [\"Comment m'inscrire\", \"Procedure inscription\", ...],\n"
    "        \"en\": [\"How to enroll\", \"Registration procedure\", ...],\n"
    "        \"darija\": [\"Kifash ntsajjel\", \"Bghit ntsajjel f FSBM\", ...]\n"
    "      },\n"
    "      \"responses\": {\n"
    "        \"fr\": [\"Pour s'inscrire a la FSBM : ...\"],\n"
    "        \"en\": [\"To enroll at FSBM : ...\"],\n"
    "        \"darija\": [\"Bach ttsajjel f FSBM : ...\"]\n"
    "      }\n"
    "    },\n"
    "    // ...\n"
    "  ]\n"
    "}"
))

story.append(Paragraph("9.3 Entrainement multilingue", ST_H1))
story.append(code(
    "class MultilingualClassifier:\n"
    "    def train(self):\n"
    "        # Un vectorizer par langue\n"
    "        self.vectorizers = {}        # {'fr': ..., 'en': ..., 'darija': ...}\n"
    "        self.tfidf_matrices = {}\n"
    "        self.pattern_to_intent = {}\n"
    "        \n"
    "        for lang in ['fr', 'en', 'darija']:\n"
    "            patterns = []\n"
    "            tags = []\n"
    "            \n"
    "            for intent in self.intents:\n"
    "                pats = intent['patterns'].get(lang, [])\n"
    "                for p in pats:\n"
    "                    patterns.append(self.preprocess(p))\n"
    "                    tags.append(intent['tag'])\n"
    "            \n"
    "            if patterns:\n"
    "                vec = TfidfVectorizer(ngram_range=(1, 3), sublinear_tf=True)\n"
    "                matrix = vec.fit_transform(patterns)\n"
    "                self.vectorizers[lang] = vec\n"
    "                self.tfidf_matrices[lang] = matrix\n"
    "                self.pattern_to_intent[lang] = tags"
))

story.append(Paragraph("9.4 Statistiques du modele entraine", ST_H1))
story.append(std_table([
    ['Langue', 'Patterns', 'Features TF-IDF', 'Intents'],
    ['FR', '188', '341', '27'],
    ['EN', '186', '565', '27'],
    ['Darija', '461', '1507', '27'],
    ['TOTAL', '835', '~2400', '28'],
], col_widths=[3*cm, 3*cm, 5*cm, 5*cm]))
story.append(PageBreak())

# CH 10 - Memoire
story.append(Paragraph("Chapitre 10 - Memoire conversationnelle", ST_CHAPTER))

story.append(Paragraph("10.1 Pourquoi une memoire ?", ST_H1))
story.append(Paragraph(
    "Sans memoire, chaque message est traite isolement. Avec memoire, le bot peut :",
    ST_BODY))
for x in [
    "Se souvenir du nom de l'utilisateur",
    "Connaitre son genre (khoya/khti)",
    "Suivre la conversation (resolution de pronoms : 'pour ça' -> 'pour le master IADS')",
    "Adapter le ton selon les tours precedents",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("10.2 Notre architecture", ST_H1))
story.append(code(
    "class SessionContext:\n"
    "    session_id: str\n"
    "    user_id: Optional[int]\n"
    "    started_at: datetime\n"
    "    history: deque[Turn]                # max 20 derniers tours\n"
    "    user_context: dict                  # {'filiere', 'annee', 'gender', 'name'}\n"
    "    total_turns: int\n"
    "\n"
    "class Turn:\n"
    "    user_message: str\n"
    "    bot_response: str\n"
    "    intent: str\n"
    "    confidence: float\n"
    "    timestamp: datetime"
))

story.append(Paragraph("10.3 Singleton ConversationMemory", ST_H1))
story.append(code(
    "class ConversationMemory:\n"
    "    _instance = None\n"
    "    _sessions: dict[str, SessionContext] = {}\n"
    "    \n"
    "    def __new__(cls):\n"
    "        if cls._instance is None:\n"
    "            cls._instance = super().__new__(cls)\n"
    "        return cls._instance\n"
    "    \n"
    "    def get_or_create(self, session_id, user_id=None):\n"
    "        if session_id not in self._sessions:\n"
    "            self._sessions[session_id] = SessionContext(\n"
    "                session_id=session_id,\n"
    "                history=deque(maxlen=20)\n"
    "            )\n"
    "        return self._sessions[session_id]\n"
    "    \n"
    "    def add_turn(self, session_id, user_msg, bot_resp, intent, conf, user_id=None):\n"
    "        ctx = self.get_or_create(session_id, user_id)\n"
    "        ctx.history.append(Turn(user_msg, bot_resp, intent, conf))\n"
    "        self._extract_context(ctx, user_msg, intent)\n"
    "\n"
    "memory = ConversationMemory()  # singleton global"
))

story.append(Paragraph("10.4 Extraction automatique de contexte", ST_H1))
story.append(code(
    "def _extract_context(ctx: SessionContext, message: str, intent: str):\n"
    "    msg = message.lower()\n"
    "    \n"
    "    # Filieres mentionnees\n"
    "    for code, keywords in {\n"
    "        'SMI': ['smi', 'sciences mathematiques et informatique'],\n"
    "        'DI':  ['di', 'developpement informatique'],\n"
    "        # ...\n"
    "    }.items():\n"
    "        if any(k in msg for k in keywords):\n"
    "            ctx.user_context['filiere'] = code\n"
    "            break\n"
    "    \n"
    "    # Annee d'etudes\n"
    "    for n, kw in [(1, ['s1', 's2', 'premiere annee', 'L1']),\n"
    "                  (2, ['s3', 's4', 'deuxieme annee', 'L2']),\n"
    "                  (3, ['s5', 's6', 'troisieme annee', 'L3'])]:\n"
    "        if any(k in msg for k in kw):\n"
    "            ctx.user_context['annee'] = n"
))
story.append(PageBreak())

# CH 11 - Persona
story.append(Paragraph("Chapitre 11 - Personnalisation (genre/nom)", ST_CHAPTER))

story.append(Paragraph("11.1 Detection du genre", ST_H1))
story.append(code(
    "GENDER_HINTS_F = [\n"
    "    r'\\bana\\s+bnt\\b',                  # Darija\n"
    "    r'\\bana\\s+fata\\b',\n"
    "    r'je\\s+suis\\s+une?\\s+fille',       # FR\n"
    "    r'je\\s+suis\\s+etudiante',\n"
    "    r\"i\\s+am\\s+a?\\s*(girl|female)\",    # EN\n"
    "]\n"
    "\n"
    "GENDER_HINTS_M = [\n"
    "    r'\\bana\\s+wld\\b',\n"
    "    r'\\bana\\s+rajl\\b',\n"
    "    r'je\\s+suis\\s+un\\s+garcon',\n"
    "    r\"i\\s+am\\s+a?\\s*(boy|male|man)\",\n"
    "]\n"
    "\n"
    "def detect_gender(message: str) -> Optional[Gender]:\n"
    "    lower = message.lower()\n"
    "    for pat in GENDER_HINTS_F:\n"
    "        if re.search(pat, lower):\n"
    "            return 'F'\n"
    "    for pat in GENDER_HINTS_M:\n"
    "        if re.search(pat, lower):\n"
    "            return 'M'\n"
    "    return None"
))

story.append(Paragraph("11.2 Substitution dans les reponses", ST_H1))
story.append(Paragraph(
    "Les reponses pre-ecrites contiennent des <b>placeholders</b> qui sont remplaces selon "
    "le genre detecte :",
    ST_BODY))
story.append(code(
    "Template : 'Salam {voc}, ach {dayer_dayra} ? Je suis content de te connaitre.'\n"
    "\n"
    "Pour un homme (gender=M) :\n"
    "  -> 'Salam khoya, ach dayer ?'\n"
    "\n"
    "Pour une femme (gender=F) :\n"
    "  -> 'Salam khti, ach dayra ?'\n"
    "\n"
    "Genre inconnu :\n"
    "  -> 'Salam sahbi, ach dayer/dayra ?'"
))

story.append(Paragraph("11.3 Code de substitution", ST_H1))
story.append(code(
    "def personalize_response(text, gender=None, name=None, lang='darija'):\n"
    "    if gender == 'F':\n"
    "        subs = {\n"
    "            '{voc}': 'khti',\n"
    "            '{dayer_dayra}': 'dayra',\n"
    "            '{stresse}': 'stressee',\n"
    "            '{name}': name or '',\n"
    "        }\n"
    "    elif gender == 'M':\n"
    "        subs = {\n"
    "            '{voc}': 'khoya',\n"
    "            '{dayer_dayra}': 'dayer',\n"
    "            '{stresse}': 'stresse',\n"
    "            '{name}': name or '',\n"
    "        }\n"
    "    else:\n"
    "        subs = {\n"
    "            '{voc}': 'sahbi',\n"
    "            '{dayer_dayra}': 'dayer/dayra',\n"
    "            '{stresse}': 'stresse(e)',\n"
    "            '{name}': '',\n"
    "        }\n"
    "    \n"
    "    for placeholder, value in subs.items():\n"
    "        text = text.replace(placeholder, value)\n"
    "    return text"
))
story.append(PageBreak())

# CH 12 - LLM
story.append(Paragraph("Chapitre 12 - LLM (LLaMA 3 + Groq)", ST_CHAPTER))

story.append(Paragraph("12.1 Limites du TF-IDF", ST_H1))
story.append(Paragraph(
    "Le TF-IDF est parfait pour des FAQs structurees, mais limite pour :",
    ST_BODY))
for x in [
    "Questions formulees avec des mots <b>inconnus</b> du dataset",
    "Questions combinant <b>plusieurs sujets</b> ('master IADS + bourse + logement')",
    "Conversations longues avec <b>resolution d'ambiguites</b>",
    "Reponses <b>creatives</b> ou tres personnalisees",
]:
    story.append(Paragraph(f"- {x}", ST_LIST))

story.append(Paragraph("12.2 Solution : LLM (LLaMA 3.3)", ST_H1))
story.append(Paragraph(
    "Un <b>LLM (Large Language Model)</b> comme LLaMA 3 peut comprendre le sens semantique "
    "et generer des reponses uniques. Pour notre PFE on utilise <b>Groq</b> qui heberge "
    "LLaMA 3 gratuitement et tres rapidement (~150ms).",
    ST_BODY))

story.append(Paragraph("12.3 Client Groq", ST_H1))
story.append(code(
    "from groq import Groq\n"
    "\n"
    "client = Groq(api_key='gsk_xxx')\n"
    "\n"
    "completion = client.chat.completions.create(\n"
    "    model='llama-3.3-70b-versatile',\n"
    "    messages=[\n"
    "        {'role': 'system', 'content': 'Tu es un assistant FSBM. Reponds en francais.'},\n"
    "        {'role': 'user', 'content': 'Quelles filieres a la FSBM ?'},\n"
    "    ],\n"
    "    temperature=0.7,\n"
    "    max_tokens=1024,\n"
    ")\n"
    "\n"
    "print(completion.choices[0].message.content)"
))

story.append(Paragraph("12.4 Architecture en cascade (fallback)", ST_H1))
story.append(diagram(
    "    Question utilisateur\n"
    "         |\n"
    "         v\n"
    "    Try Groq (LLaMA 3.3-70B)\n"
    "         |\n"
    "         | OK -> reponse\n"
    "         | echec\n"
    "         v\n"
    "    Try HuggingFace (LLaMA 3-8B)\n"
    "         |\n"
    "         | OK -> reponse\n"
    "         | echec\n"
    "         v\n"
    "    Fallback TF-IDF (toujours dispo)\n"
    "         |\n"
    "         v\n"
    "    Reponse pre-ecrite garantie"
))

story.append(alert_box(
    "Cette cascade garantit <b>100% de disponibilite</b>. Le chatbot ne tombe JAMAIS. Au "
    "pire, il revient au comportement de la v1 (TF-IDF).",
    kind="key"))
story.append(PageBreak())

# CH 13 - RAG
story.append(Paragraph("Chapitre 13 - RAG = retrieval + generation", ST_CHAPTER))

story.append(Paragraph("13.1 Le probleme du LLM 'pur'", ST_H1))
story.append(Paragraph(
    "Un LLM 'pur' peut HALLUCINER : inventer des informations qui ont l'air vraies mais "
    "sont fausses. Dangereux pour une fac (numero de tel imagine, date d'examen fausse).",
    ST_BODY))

story.append(Paragraph("13.2 Solution : RAG", ST_H1))
story.append(Paragraph(
    "<b>RAG = Retrieval-Augmented Generation</b>. On combine 2 systemes :",
    ST_BODY))
for n, d in [
    ("1. RETRIEVAL",
     "On cherche dans notre dataset FSBM les passages les plus pertinents pour la question."),
    ("2. AUGMENTED",
     "On injecte ces passages dans le prompt du LLM."),
    ("3. GENERATION",
     "Le LLM repond en se basant sur ces passages, donc SANS inventer."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(analogy(
    "Sans RAG = etudiant qui repond de tete (parfois faux). Avec RAG = etudiant qui ouvre "
    "son cahier de cours specifique a la FSBM et cite les passages exacts. La qualite est "
    "bien meilleure."))

story.append(Paragraph("13.3 Notre RAG : retrieval avec TF-IDF", ST_H1))
story.append(Paragraph(
    "On REUTILISE notre classifier TF-IDF comme retriever. Pas besoin d'embeddings neuronaux.",
    ST_BODY))
story.append(code(
    "class RAGRetriever:\n"
    "    def __init__(self, classifier):\n"
    "        self.classifier = classifier  # MultilingualClassifier deja entraine\n"
    "    \n"
    "    def retrieve(self, query, lang='fr', top_k=3):\n"
    "        # Pretraitement comme dans predict()\n"
    "        processed = self.classifier.preprocessor.preprocess(query)\n"
    "        \n"
    "        # Vectorisation TF-IDF dans la bonne langue\n"
    "        vec = self.classifier.vectorizers[lang].transform([processed])\n"
    "        \n"
    "        # Similarite cosinus contre tous les patterns\n"
    "        sims = cosine_similarity(vec,\n"
    "            self.classifier.tfidf_matrices[lang])[0]\n"
    "        \n"
    "        # Top-K candidats (dedoublonnes par intent)\n"
    "        # ...\n"
    "        \n"
    "        return [{\n"
    "            'tag': intent_tag,\n"
    "            'score': score,\n"
    "            'patterns': intent.patterns[lang][:5],\n"
    "            'reference_response': intent.responses[lang][0],\n"
    "        }, ...]"
))

story.append(Paragraph("13.4 Construction du prompt RAG", ST_H1))
story.append(code(
    "def build_rag_prompt(user_message, contexts, lang='fr',\n"
    "                    gender=None, name=None):\n"
    "    system = SYSTEM_PROMPTS[lang]  # role officiel FSBM\n"
    "    \n"
    "    if contexts:\n"
    "        system += '\\n\\n=== CONTEXTE FSBM ===\\n'\n"
    "        for i, c in enumerate(contexts, 1):\n"
    "            system += f'Passage #{i} (sujet: {c.tag}, score: {c.score})\\n'\n"
    "            system += f'Exemples : {c.patterns[:3]}\\n'\n"
    "            system += f'Information : {c.reference_response}\\n\\n'\n"
    "        system += '=== FIN CONTEXTE ==='\n"
    "    \n"
    "    # Info personnelle (genre/nom)\n"
    "    if gender or name:\n"
    "        system += f'\\n[INFO : nom={name}, genre={gender}]'\n"
    "    \n"
    "    return system, user_message"
))

story.append(Paragraph("13.5 Exemple de prompt RAG complet", ST_H1))
story.append(code(
    "SYSTEM :\n"
    "Tu es l'assistant officiel de la FSBM.\n"
    "Reponds UNIQUEMENT en utilisant le contexte ci-dessous.\n"
    "Si l'info n'est pas dans le contexte, dis 'Je ne sais pas'.\n"
    "\n"
    "=== CONTEXTE FSBM ===\n"
    "Passage #1 (sujet: master_iads, score: 0.91)\n"
    "Master IADS - IA & Data Science. 2 ans, 25 places.\n"
    "Programme : ML, Deep Learning, NLP, Vision, Big Data...\n"
    "\n"
    "Passage #2 (sujet: bourses, score: 0.65)\n"
    "Bourse ONOUSC : revenus famille + distance. ~3500 DH/an.\n"
    "Demande sur www.onousc.ma en juillet-aout.\n"
    "=== FIN CONTEXTE ===\n"
    "\n"
    "USER :\n"
    "Je veux faire le master IADS, est-ce qu'il y a une bourse ?\n"
    "\n"
    "ASSISTANT (genere par LLaMA) :\n"
    "Oui, vous pouvez postuler a la fois au master IADS et a la bourse ONOUSC.\n"
    "Le master IADS est selectif (25 places). La bourse ONOUSC vous donnerait\n"
    "~3500 DH/an si vous remplissez les criteres (revenus + distance)."
))
story.append(PageBreak())

# CH 14 - Embeddings
story.append(Paragraph("Chapitre 14 - Embeddings (vectorielle moderne)", ST_CHAPTER))

story.append(Paragraph("14.1 Limite du TF-IDF", ST_H1))
story.append(Paragraph(
    "TF-IDF compare les <b>mots EXACTS</b>. Si l'utilisateur dit 'chat' et notre pattern dit "
    "'feline', le score est 0. C'est limitant.",
    ST_BODY))

story.append(Paragraph("14.2 Solution : Embeddings neuronaux", ST_H1))
story.append(Paragraph(
    "Un <b>embedding</b> est un vecteur de nombres qui represente le <b>sens</b> d'un mot ou "
    "d'une phrase. Les mots de sens proche ont des embeddings proches (meme s'ils sont "
    "differents lexicalement).",
    ST_BODY))

story.append(code(
    "embedding('chat')    = [0.23, -0.45, 0.81, ..., 0.34]\n"
    "embedding('feline')  = [0.21, -0.43, 0.79, ..., 0.32]  # tres proche !\n"
    "embedding('meteo')   = [-0.89, 0.12, -0.34, ..., -0.23]  # tres different"
))

story.append(Paragraph("14.3 Modeles d'embedding populaires", ST_H1))
for x in [
    "<b>OpenAI text-embedding-3</b> : commercial, dim 1536-3072",
    "<b>Sentence-BERT</b> : open source, dim 384-768",
    "<b>BGE-M3</b> : open source multilingue, dim 1024",
    "<b>Multilingual-E5</b> : open source, 100 langues",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("14.4 Quand passer du TF-IDF aux embeddings ?", ST_H1))
story.append(std_table([
    ['Critere', 'TF-IDF (notre v1)', 'Embeddings (v2 future)'],
    ['Dimensions', '~1500', '384-3072'],
    ['Semantique', 'Aucune', 'Excellente'],
    ['Vitesse', 'Tres rapide (<10ms)', 'Lent (CPU) ou GPU'],
    ['Cout', 'Gratuit', 'Gratuit en local'],
    ['Adapte a', '28 intents structures', 'Documents longs varies'],
    ['Notre PFE', 'Suffisant', 'Phase 2 si scale'],
], col_widths=[3*cm, 6*cm, 7*cm]))

story.append(alert_box(
    "Pour notre PFE (28 intents), TF-IDF suffit largement et est tres rapide. Si on "
    "passait a 10 000 documents (Phase 2), on basculerait sur BGE-M3 ou Sentence-BERT.",
    kind="tip"))
story.append(PageBreak())

# CH 15 - Conclusion
story.append(Paragraph("Chapitre 15 - Conclusion", ST_CHAPTER))

story.append(Paragraph("15.1 Recap des concepts", ST_H1))
for x in [
    "NLP = traitement automatique du langage",
    "Pipeline : detection langue -> preprocessing -> vectorisation -> matching",
    "Tokenisation = decoupage en mots",
    "Stopwords = mots peu informatifs a enlever",
    "Stemming = reduction a la racine",
    "TF-IDF = importance d'un mot (frequence + rarete)",
    "Cosine similarity = proximite entre vecteurs",
    "n-grammes = capture expressions composees",
    "Detection langue hybride (caracteres + mots-cles)",
    "Multilingue = 3 modeles TF-IDF separes",
    "Memoire = historique + contexte utilisateur",
    "Personnalisation = substitution placeholders selon genre/nom",
    "LLM = LLaMA 3 via Groq pour reponses naturelles",
    "RAG = retrieval + augmentation prompt + generation",
    "Embeddings = vectorisation semantique moderne (Phase 2)",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("15.2 Pour aller plus loin", ST_H1))
for x in [
    "PDF 09 - workflow complet d'un message dans le pipeline",
    "PDF 10 - guide soutenance avec Q/R sur l'IA",
    "Le PDF Guide_IA_Pedagogique existant (192 KB) qui detaille Groq, LLaMA, RAG",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("06_NLP_IA_Chatbot_Complet.pdf", story,
          "PDF 06 - NLP + IA",
          "FSBM Platform - NLP et IA du Chatbot Complet")
