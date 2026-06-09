"""PDF 10 - Guide Soutenance"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 10/10", "Guide Soutenance",
           "Q/R + Demo script + Vulgarisation + Backup plan",
           accent_color=HexColor('#8B5CF6'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - Avant la soutenance", "3"),
    ("Chapitre 2 - Structure de la presentation", "6"),
    ("Chapitre 3 - Pitch 30 secondes", "10"),
    ("Chapitre 4 - Demo script (10 min)", "12"),
    ("Chapitre 5 - Vulgarisation des concepts", "17"),
    ("Chapitre 6 - Q/R techniques", "22"),
    ("Chapitre 7 - Q/R fonctionnelles", "29"),
    ("Chapitre 8 - Q/R pieges", "34"),
    ("Chapitre 9 - Backup plan", "39"),
    ("Chapitre 10 - Erreurs a eviter", "42"),
    ("Chapitre 11 - Conclusion", "45"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1
story.append(Paragraph("Chapitre 1 - Avant la soutenance", ST_CHAPTER))

story.append(Paragraph("1.1 Checklist materiel", ST_H1))
for x in [
    "PC portable charge + chargeur",
    "Cle USB avec presentation + backup PDFs",
    "Adaptateur HDMI/VGA selon la salle",
    "Cable RJ45 (si WiFi salle mauvaise)",
    "Hotspot 4G de secours sur telephone",
    "Bouteille d'eau, mouchoirs",
    "Tenue professionnelle (cravate, chemise...)",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("1.2 Checklist technique", ST_H1))
for x in [
    "MySQL demarre + base remplie verifiee",
    "MongoDB demarre + collections OK",
    "Chatbot-service tourne sur :8001",
    "Academic-service tourne sur :8002",
    "Frontend Angular tourne sur :4200",
    "GROQ_API_KEY valide (test rapide)",
    "Tester /api/health pour les 2 services",
    "Browser favori avec onglets pre-ouverts",
    "Screenshots/captures en backup",
    "Video de demo enregistree si tout casse",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("1.3 La veille", ST_H1))
for x in [
    "Repeter la demo 3 fois (chronometre)",
    "Faire un git pull final et tester",
    "Mettre l'ordinateur en veille prolongee",
    "Imprimer 2 copies des PDFs + slides",
    "Dormir tot (vraiment, ca fait la difference)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("1.4 Le jour J : 1h avant", ST_H1))
for x in [
    "Arriver 30 min en avance",
    "Verifier que le retroprojecteur marche",
    "Demarrer tous les services + valider /health",
    "Faire une question test au chatbot",
    "Ouvrir Swagger UI dans un onglet de secours",
    "Respirer profondement, sourire",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 2
story.append(Paragraph("Chapitre 2 - Structure de la presentation", ST_CHAPTER))

story.append(Paragraph("2.1 Plan classique 20 minutes", ST_H1))
story.append(std_table([
    ['Section', 'Temps', 'Slides'],
    ['1. Introduction + contexte', '2 min', '2'],
    ['2. Problematique + objectifs', '2 min', '2'],
    ['3. Etat de l\'art', '1 min', '1'],
    ['4. Architecture choisie', '3 min', '3'],
    ['5. Technologies', '2 min', '2'],
    ['6. DEMO en LIVE', '5 min', '0'],
    ['7. Difficultes rencontrees', '1 min', '1'],
    ['8. Resultats + chiffres', '2 min', '2'],
    ['9. Perspectives (Phase 2)', '1 min', '1'],
    ['10. Conclusion', '1 min', '1'],
    ['<b>TOTAL</b>', '<b>20 min</b>', '<b>15</b>'],
], col_widths=[7*cm, 4*cm, 3*cm]))

story.append(Paragraph("2.2 Distribution des roles (si en binome)", ST_H1))
story.append(std_table([
    ['Personne', 'Parties'],
    ['Etudiant 1', 'Intro, contexte, problematique, demo, conclusion'],
    ['Etudiant 2', 'Architecture, technos, difficultes, perspectives, Q/R'],
], col_widths=[4*cm, 12*cm]))

story.append(Paragraph("2.3 Slide 1 : Page de garde", ST_H1))
story.append(Paragraph(
    "Doit contenir : titre du projet, nom etudiant(s), encadrant, jury, date, logo FSBM, "
    "logo UH2C. Sobre, propre, professionnel.",
    ST_BODY))

story.append(Paragraph("2.4 Slides cle : tu DOIS avoir", ST_H1))
for x in [
    "Schema d'<b>architecture globale</b>",
    "Schema du <b>workflow chatbot</b> (NLP -> reponse)",
    "Diagramme du <b>schema BDD</b> (MySQL + MongoDB)",
    "Comparaison <b>TF-IDF vs LLM</b>",
    "Captures d'ecran <b>du frontend</b>",
    "Chiffres : <b>nb d'intents, patterns, endpoints</b>",
    "Captures Swagger UI",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(alert_box(
    "<b>REGLE D'OR :</b> max 6 lignes par slide. Pas de phrases entieres. Des mots-cles, "
    "des images, des chiffres. Tu PARLES, le slide ILLUSTRE.",
    kind="tip"))
story.append(PageBreak())

# CH 3
story.append(Paragraph("Chapitre 3 - Pitch 30 secondes", ST_CHAPTER))

story.append(Paragraph("3.1 La version courte (pour debuter)", ST_H1))
story.append(Paragraph(
    "<i>'Bonjour, nous avons developpe FSBM Platform, un assistant intelligent pour la "
    "Faculte des Sciences Ben M'Sick. Concretement, c'est un chatbot multilingue francais, "
    "anglais et darija qui repond aux questions des etudiants 24h/24 sur les inscriptions, "
    "les filieres, les emplois du temps. L'architecture est en microservices : "
    "frontend Angular, backends FastAPI, MySQL pour les donnees structurees, MongoDB "
    "pour les conversations, et LLaMA 3 pour les reponses naturelles. Aujourd'hui on va "
    "vous montrer le systeme en action.'</i>",
    ST_BODY))

story.append(Paragraph("3.2 La version technique (pour jury exigeant)", ST_H1))
story.append(Paragraph(
    "<i>'Nous avons concu une plateforme web modulaire repondant a 4 enjeux : disponibilite "
    "24/7 du service scolarite, support multilingue FR/EN/Darija, comprehension du langage "
    "naturel, et scalabilite. L'architecture en microservices decouple frontend Angular 17 "
    "et 2 backends FastAPI - un pour le chatbot et un pour les donnees academiques. "
    "Le moteur NLP combine TF-IDF + cosine similarity pour la classification d'intent, "
    "avec une cascade fallback vers LLaMA 3.3-70B via Groq API enrichi par RAG. "
    "MySQL stocke les 16 tables structurees, MongoDB gere les sessions et logs. "
    "Le tout est documente via Swagger.'</i>",
    ST_BODY))

story.append(Paragraph("3.3 Conseils delivery", ST_H1))
for x in [
    "<b>Lent</b>, articule, regarde le jury",
    "Pas de 'euh', 'genre', 'tu vois'",
    "Mains visibles, pas dans les poches",
    "Sourire au debut + a la fin",
    "Si tu blanchis, prend une respiration, reprend",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 4 - Demo script
story.append(Paragraph("Chapitre 4 - Demo script (10 min)", ST_CHAPTER))

story.append(Paragraph("4.1 Sequence recommandee", ST_H1))

story.append(Paragraph("<b>SCENE 1 : Accueil (1 min)</b>", ST_H1))
story.append(Paragraph(
    "1. Ouvrir <b>http://localhost:4200</b><br/>"
    "2. Montrer le dashboard avec les compteurs (25 filieres, 107 profs, 2970 etudiants)<br/>"
    "3. Naviguer dans le sidebar : Filieres, Departements, Annonces, Evenements<br/>"
    "<i>Phrase : 'Le frontend Angular sert de hub central : un etudiant a une vue globale "
    "de la faculte.'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 2 : Filieres (1 min)</b>", ST_H1))
story.append(Paragraph(
    "1. Cliquer sur 'Filieres' dans sidebar<br/>"
    "2. Filtrer par 'MASTER'<br/>"
    "3. Cliquer sur 'Master IADS' -> page detail<br/>"
    "4. Montrer les modules par semestre, coordinateur, capacite<br/>"
    "<i>Phrase : 'Les donnees viennent directement de l'academic-service via REST API. "
    "Aucune donnee codee en dur.'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 3 : Chatbot FR (2 min)</b>", ST_H1))
story.append(Paragraph(
    "1. Aller sur la page Chatbot<br/>"
    "2. Question 1 : 'Quelles sont les filieres ?' -> reponse en FR<br/>"
    "3. Montrer le badge 'intent: filieres, confidence: 1.0'<br/>"
    "4. Question 2 : 'Conditions inscription Master IADS ?' -> reponse detaillee<br/>"
    "5. Question 3 : 'Comment t'appelles-tu ?' -> presentation perso<br/>"
    "<i>Phrase : 'Le bot detecte la langue, classifie l'intent en 30ms, repond.'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 4 : Chatbot EN (1 min)</b>", ST_H1))
story.append(Paragraph(
    "1. 'What are the masters in computer science ?'<br/>"
    "2. Reponse en anglais natif<br/>"
    "3. Montrer le badge 'language: en'<br/>"
    "<i>Phrase : 'La detection de langue est hybride : script, mots-cles, et bascule auto'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 5 : Chatbot Darija (2 min)</b>", ST_H1))
story.append(Paragraph(
    "1. 'salam, ki dayer ?' -> salutation darija<br/>"
    "2. 'shno hia les filieres ?' -> filieres en darija<br/>"
    "3. 'ana 7ass b stress f les examens' -> reponse motivante darija<br/>"
    "4. Montrer comment le mot 'ana' detecte un user feminin si nom de fille suit<br/>"
    "<i>Phrase : 'Darija est rare dans les chatbots. On a fait un dataset de 461 patterns "
    "et un algo de detection numerique 3/7/9 typique.'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 6 : LLM Mode (2 min)</b>", ST_H1))
story.append(Paragraph(
    "1. Switch toggle 'LLM Mode'<br/>"
    "2. Question complexe : 'Compare les masters IADS et MIAGE pour mon profil "
    "math.'<br/>"
    "3. Reponse longue, contextualisee, nuancee<br/>"
    "4. Montrer le badge 'provider: groq, model: llama-3.3-70b'<br/>"
    "5. Montrer 'contexts_used' (le RAG)<br/>"
    "<i>Phrase : 'Quand TF-IDF ne suffit pas, on bascule sur LLaMA 3 avec RAG. "
    "Le LLM utilise notre dataset comme contexte, donc pas d'hallucination.'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 7 : Swagger (1 min)</b>", ST_H1))
story.append(Paragraph(
    "1. Ouvrir <b>http://localhost:8001/docs</b><br/>"
    "2. Montrer la liste d'endpoints<br/>"
    "3. Click 'Try it out' sur POST /api/chat<br/>"
    "4. Executer en live<br/>"
    "<i>Phrase : 'FastAPI genere automatiquement cette doc interactive. Tres utile en "
    "developpement et pour les autres devs.'</i>",
    ST_BODY))

story.append(Paragraph("<b>SCENE 8 : BDD (1 min)</b>", ST_H1))
story.append(Paragraph(
    "1. Ouvrir MySQL Workbench<br/>"
    "2. Montrer la table 'conversations' -> la derniere conv en bas<br/>"
    "3. Ouvrir MongoDB Compass<br/>"
    "4. Montrer la collection 'sessions' avec le tableau messages<br/>"
    "<i>Phrase : 'Chaque interaction est tracee : MySQL pour les stats, MongoDB pour la "
    "session complete.'</i>",
    ST_BODY))
story.append(PageBreak())

# CH 5 - Vulgarisation
story.append(Paragraph("Chapitre 5 - Vulgarisation des concepts", ST_CHAPTER))

story.append(Paragraph(
    "Le jury n'est pas forcement specialiste de chaque techno. Il faut SAVOIR EXPLIQUER "
    "SIMPLEMENT.",
    ST_BODY))

story.append(Paragraph("5.1 'C'est quoi un microservice ?'", ST_H1))
story.append(Paragraph(
    "<i>'Imaginez un restaurant. L'approche classique = 1 cuisinier qui fait TOUT (entree, "
    "plat, dessert). Si il est malade, le restaurant ferme. Les microservices = plusieurs "
    "cuisiniers specialistes. L'un fait les entrees, l'autre les desserts. Si l'un est "
    "malade, les autres continuent. Notre projet a 2 services : un pour le chatbot, un "
    "pour les donnees academiques.'</i>",
    ST_BODY))

story.append(Paragraph("5.2 'C'est quoi TF-IDF ?'", ST_H1))
story.append(Paragraph(
    "<i>'TF-IDF c'est une facon de transformer du texte en chiffres. Imaginez que vous "
    "comparez 2 livres : si le mot ETUDIANT apparait dans tous les livres, il ne distingue "
    "rien. Mais ALGORITHMIQUE apparait surtout dans un livre informatique, donc c'est un "
    "indicateur fort. TF-IDF donne plus de poids aux mots distinctifs. On compare la question "
    "de l'user a TOUS nos patterns, et on choisit le plus similaire.'</i>",
    ST_BODY))

story.append(Paragraph("5.3 'C'est quoi un LLM ?'", ST_H1))
story.append(Paragraph(
    "<i>'Un LLM, comme LLaMA 3 ou GPT, c'est un modele entraine sur des MILLIARDS de mots. "
    "Il a appris la grammaire, les concepts, les patterns. Quand on lui pose une question, "
    "il genere une reponse mot par mot, en choisissant le plus probable a chaque etape. "
    "70 milliards de parametres dans LLaMA 3.3, ce qui le rend tres performant.'</i>",
    ST_BODY))

story.append(Paragraph("5.4 'C'est quoi RAG ?'", ST_H1))
story.append(Paragraph(
    "<i>'RAG = Retrieval Augmented Generation. Probleme : les LLM peuvent INVENTER. Solution "
    "RAG = AVANT de demander au LLM, on cherche dans notre base de donnees les infos "
    "pertinentes, et on les colle dans le prompt. Le LLM REFORMULE ces vrais infos au lieu "
    "d'inventer. Comme un eleve qui repond a partir de ses notes au lieu de bluffer.'</i>",
    ST_BODY))

story.append(Paragraph("5.5 'Pourquoi MySQL ET MongoDB ?'", ST_H1))
story.append(Paragraph(
    "<i>'MySQL = relationnel, parfait pour les donnees structurees rigides (etudiants, "
    "filieres, modules). Les relations sont strictes. MongoDB = NoSQL, parfait pour les "
    "donnees flexibles (conversations dont la longueur varie). Mettre tout dans MySQL = "
    "lent et rigide. Mettre tout dans MongoDB = perte des relations. On combine les forces "
    "des deux : polyglot persistence.'</i>",
    ST_BODY))

story.append(Paragraph("5.6 'C'est quoi FastAPI ?'", ST_H1))
story.append(Paragraph(
    "<i>'FastAPI est le framework Python le plus moderne pour creer des APIs. Il est async, "
    "donc tres rapide (10000+ req/sec). Il auto-documente via Swagger. Il valide les inputs "
    "automatiquement avec Pydantic. C'est devenu un standard pour les nouveaux projets, "
    "remplacant Flask et Django REST.'</i>",
    ST_BODY))

story.append(Paragraph("5.7 'Pourquoi Angular 17 et pas React ?'", ST_H1))
story.append(Paragraph(
    "<i>'Angular est un framework complet (routing, forms, HTTP), pret a l'emploi. C'est "
    "TypeScript native, donc moins de bugs. Angular 17 a introduit les SIGNALS, plus "
    "performants que le change detection classique. C'est aussi notre choix academique : "
    "plus structurant pour un projet de cette taille.'</i>",
    ST_BODY))
story.append(PageBreak())

# CH 6 - Q/R techniques
story.append(Paragraph("Chapitre 6 - Q/R techniques", ST_CHAPTER))

qa_tech = [
    ("Pourquoi async/await en Python ?",
     "Le serveur peut traiter plusieurs requetes en parallele sans creer 1 thread par requete. "
     "C'est crucial pour les operations I/O (DB, HTTP). Un endpoint async libere le thread "
     "pendant l'attente DB et peut servir un autre user."),
    ("Comment garantir la coherence des donnees entre MySQL et MongoDB ?",
     "Phase 1 : on accepte une coherence finale eventuelle. Phase 2 prevue : transactions "
     "distribuees via outbox pattern ou Saga. Aujourd'hui, MongoDB est append-only pour "
     "les conversations, donc pas de conflit."),
    ("Comment gerez-vous la scalabilite ?",
     "Architecture stateless permet le scale horizontal (lancer 10 instances de "
     "chatbot-service derriere un load balancer). MySQL : read replicas. MongoDB : "
     "sharding. NLP : cache TF-IDF en RAM, partage entre instances."),
    ("Quelle est la latence moyenne ?",
     "TF-IDF : ~150 ms p50, 200 ms p95. LLM Groq : ~250 ms p50, 600 ms p95. Sans cache. "
     "Avec cache Redis (Phase 2), on viserait 50 ms pour les reponses repetees."),
    ("Comment gerez-vous les pannes du Groq API ?",
     "Cascade fallback : Groq -> HuggingFace -> TF-IDF local. Donc 100% de disponibilite "
     "garantie meme si Groq est down. Les utilisateurs ont une reponse, juste moins "
     "naturelle si on est en mode TF-IDF."),
    ("Pourquoi choisir LLaMA et pas GPT-4 ?",
     "Trois raisons : (1) Groq offre LLaMA gratuitement, GPT-4 coute, (2) LLaMA 3.3-70B "
     "tourne sur Groq LPU a 200+ tokens/sec vs 50 pour GPT-4, (3) Open source = "
     "deployable on-premise plus tard si besoin de confidentialite."),
    ("Comment validez-vous la qualite des reponses ?",
     "Trois mecanismes : (1) Confidence score TF-IDF visible dans les reponses, (2) "
     "Feedback user (1-5 etoiles) stocke pour analyse, (3) Tests automatises sur 50 "
     "questions de reference. On vise un taux 'is_helpful' > 80%."),
    ("Quelle est la couverture de tests ?",
     "Aujourd'hui, tests manuels via Swagger + 50 questions canoniques. Pour Phase 2 : "
     "tests unitaires pytest sur classifier, integration tests sur endpoints, "
     "smoke tests E2E."),
    ("Comment evitez-vous le SQL injection ?",
     "On utilise EXCLUSIVEMENT SQLAlchemy avec requetes parametriees. Pas de "
     "concatenation manuelle de SQL. Pydantic valide les inputs avant. Donc immunise."),
    ("Pourquoi avoir code la detection de genre ?",
     "Pour la personnalisation darija. En darija, 'khoya' (mon frere) vs 'khti' (ma soeur) "
     "vs 'lalla' (madame) sont importants. On detecte le genre via prenom + mots-cles "
     "linguistiques ('ana mra' = je suis une femme). Le bot adapte son vocabulaire."),
    ("Vous avez utilise des modeles de ML pretraines ?",
     "Pour le NLP : pas de pretraine, on a entraine TF-IDF sur notre dataset (28 intents, "
     "~835 patterns). Pour le LLM : oui, LLaMA 3.3 et Mistral pretraines. C'est un mix "
     "intentionnel : leger local + puissant cloud."),
    ("Comment garantir la confidentialite des messages user ?",
     "Phase 1 : pas de personnal data dans les conversations (pas de mots de passe, etc.). "
     "Phase 2 : JWT pour auth, HTTPS obligatoire, RBAC pour acces aux logs. Anonymisation "
     "des analytics."),
]
for q, a in qa_tech:
    story.append(Paragraph(f"<b>Q :</b> {q}", ST_BODY))
    story.append(Paragraph(f"<b>R :</b> {a}", ST_LIST))
    story.append(Spacer(1, 4))
story.append(PageBreak())

# CH 7 - Q/R fonctionnelles
story.append(Paragraph("Chapitre 7 - Q/R fonctionnelles", ST_CHAPTER))

qa_func = [
    ("Quel est l'apport pour la FSBM ?",
     "Le service scolarite a une charge enorme : 2970 etudiants, ~50 questions/jour. "
     "Le bot repond 24/7 sur les 80% de questions repetitives (filieres, inscriptions, "
     "emplois du temps). La scolarite peut se concentrer sur les cas complexes."),
    ("Combien d'utilisateurs peut-il supporter ?",
     "Sur 1 serveur 4 cores 8GB RAM : ~200 reqs/sec simultanees. Avec scale horizontal, "
     "on peut monter a 10000+ reqs/sec. La FSBM compte ~3000 etudiants, donc largement "
     "couvert."),
    ("Comment les etudiants y accedent ?",
     "Phase 1 : web app responsive. Phase 2 : integration au site fsbm.ma + Messenger "
     "Facebook + WhatsApp Business API. Phase 3 : app mobile native (Flutter)."),
    ("Comment le contenu reste a jour ?",
     "Le dataset est en JSON modifiable. Phase 2 : interface admin pour scolarite, qui "
     "peut ajouter des FAQs sans toucher au code. Auto-rechargement du modele NLP."),
    ("Le chatbot peut-il aider au cas par cas ?",
     "Pour les questions genrales : oui. Pour les cas personnels (releves, notes, etc.) : "
     "Phase 2 prevue avec auth etudiant -> acces a son dossier personnel via JWT."),
    ("Comment validez-vous le contenu ?",
     "Le dataset a ete construit a partir des FAQ officielles + entretiens avec la "
     "scolarite. Le Google Form distribue a permis de collecter les questions reelles "
     "des etudiants."),
    ("Que se passe-t-il si le bot ne comprend pas ?",
     "Confidence < 0.3 : on retourne 'Je ne suis pas sur de comprendre, peux-tu "
     "reformuler ?' + suggestions de questions proches. On loggue ces cas pour ameliorer "
     "le dataset."),
    ("Et si l'etudiant pose une question hors scope (ex: politique) ?",
     "Le bot detecte une faible confidence et redirige vers les sujets supportes. Il ne "
     "repond JAMAIS sur des sujets politiques ou personnels. C'est garanti par notre "
     "dataset borne et le system prompt en mode LLM."),
    ("Avez-vous des metriques d'utilisation ?",
     "MongoDB analytics : count par intent, par langue, par jour. MySQL : conversations "
     "log + feedback. Tableau de bord Phase 2 prevu pour la scolarite."),
    ("Le projet est-il open source ?",
     "Pour l'instant non, c'est un projet PFE. Mais l'architecture est conforme aux "
     "standards open source. Si la FSBM le souhaite, on peut publier."),
]
for q, a in qa_func:
    story.append(Paragraph(f"<b>Q :</b> {q}", ST_BODY))
    story.append(Paragraph(f"<b>R :</b> {a}", ST_LIST))
    story.append(Spacer(1, 4))
story.append(PageBreak())

# CH 8 - Q/R pieges
story.append(Paragraph("Chapitre 8 - Q/R pieges", ST_CHAPTER))

story.append(Paragraph(
    "Les jurys aiment poser des questions <b>pieges</b> ou <b>ouvertes</b>. Voici comment y "
    "repondre intelligemment.",
    ST_BODY))

qa_pieges = [
    ("Pourquoi pas ChatGPT directement ?",
     "ChatGPT n'a pas le contexte FSBM. Il inventerait les infos. Il faut soit le "
     "fine-tuner (cher, complexe), soit faire du RAG. Notre architecture RAG +TF-IDF "
     "donne 100% d'infos fiables + 100% de disponibilite (fallback)."),
    ("C'est juste du chatbot, qu'y a-t-il d'innovant ?",
     "Trois innovations : (1) Cascade fallback Groq -> HF -> TF-IDF qui garantit 100% "
     "uptime, (2) Detection darija avec 461 patterns et algorithme numerique (rare), "
     "(3) Personnalisation genree pour la darija (khoya/khti/lalla)."),
    ("Vous avez quoi de plus qu'un FAQ statique ?",
     "Un FAQ statique force l'user a chercher. Le bot COMPREND une question formulee "
     "naturellement, dans 3 langues, et trouve la reponse pertinente. C'est un saut UX "
     "majeur. + memoire conversationnelle pour multi-tours."),
    ("Et si le dataset est biaise ?",
     "Bon point. On documente les biais : 461 patterns darija mais 188 en FR. On essaie "
     "de balancer. Et le feedback user permet de detecter les angles morts. Pas parfait, "
     "mais conscient."),
    ("Le LLM peut-il dire des choses inappropriees ?",
     "Risque limite par : (1) RAG impose le contexte FSBM, (2) System prompt strict "
     "interdit politique/religion, (3) Garde-fous Groq sur safety. Pas zero risque mais "
     "controle. En production : moderation manuelle prevue."),
    ("Combien coute le projet en production ?",
     "Hosting + DB : ~20 EUR/mois (VPS). Groq API : gratuit jusqu'a 30000 tokens/min. "
     "Largement suffisant. Domaine + SSL : ~50 EUR/an. Total : moins de 300 EUR/an."),
    ("Et si Groq devient payant ou ferme ?",
     "Architecture decouple. On switch vers HuggingFace, OpenAI, ou un LLM local "
     "(Ollama). Le code LLMService est concu pour ca : juste changer le client."),
    ("Pourquoi 28 intents et pas 100 ?",
     "Principe 80/20 : 28 intents couvrent 80% des questions. Au-dela, on a explosion "
     "combinatoire et confusion entre intents trop proches. Le LLM (RAG) prend le relais "
     "pour les 20% restants."),
    ("Pourquoi n'avez-vous pas fait de mobile app ?",
     "Scope du PFE limite a 3 mois. On a privilegie l'architecture solide + multilingue "
     "+ LLM. Une mobile app est juste un client de plus sur la meme API REST. C'est "
     "Phase 3."),
    ("Quelle est votre contribution personnelle (vs frameworks) ?",
     "Frameworks = outils (Angular, FastAPI). Notre travail : (1) Architecture "
     "microservices specifique, (2) Dataset trilingue de 835 patterns, (3) Algorithme "
     "de detection darija original, (4) Logique RAG avec TF-IDF retriever, (5) "
     "Cascade fallback, (6) Personnalisation genre/nom."),
]
for q, a in qa_pieges:
    story.append(Paragraph(f"<b>Q :</b> {q}", ST_BODY))
    story.append(Paragraph(f"<b>R :</b> {a}", ST_LIST))
    story.append(Spacer(1, 4))
story.append(PageBreak())

# CH 9 - Backup plan
story.append(Paragraph("Chapitre 9 - Backup plan", ST_CHAPTER))

story.append(Paragraph("9.1 Loi de Murphy : tout peut casser le jour J", ST_H1))
story.append(Paragraph(
    "Anticiper les pires scenarios. Voici les plans B/C/D.",
    ST_BODY))

story.append(Paragraph("9.2 Si pas de WiFi / pas d'internet", ST_H1))
for x in [
    "Hotspot 4G sur ton telephone (vraiment)",
    "<b>Tout doit tourner LOCAL</b> : MySQL local, MongoDB local",
    "Mode TF-IDF (sans Groq) doit fonctionner 100%",
    "Avoir desactive Groq par defaut dans .env : <b>GROQ_API_KEY vide</b>",
    "Au pire : video pre-enregistree de demo",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("9.3 Si le PC plante", ST_H1))
for x in [
    "<b>Backup PDF</b> des slides sur cle USB",
    "<b>Backup PDF</b> des captures d'ecran de demo",
    "Tablette en backup avec slides",
    "Pouvoir presenter SANS demo : juste les slides + capture"
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("9.4 Si un service crash en demo", ST_H1))
for x in [
    "Garder un terminal pre-lance pret a relancer",
    "Ne pas paniquer, dire : 'Un instant, je relance le service'",
    "Pendant le restart, EXPLIQUER ce qui se passe (architecture, ports, etc.)",
    "Si ca ne repart pas : passer aux captures d'ecran",
    "Si vraiment ca refuse : 'En conditions reelles, ce service tournerait sur un "
    "serveur dedie avec auto-restart. Voici les captures...'",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("9.5 Si Groq API down", ST_H1))
for x in [
    "<b>Pas grave</b> : la cascade fallback prend le relai (TF-IDF)",
    "Phrase : 'Vous remarquez le badge <i>provider: tfidf</i> : c'est notre fallback "
    "automatique qui s'active si Groq est indisponible. La reponse est moins fluide "
    "mais 100% fiable.'",
    "C'est en fait un AVANTAGE a demontrer : la robustesse de l'archi",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("9.6 Si question dont tu n'as pas la reponse", ST_H1))
for x in [
    "<b>Surtout ne pas mentir</b>",
    "'Excellente question, je n'ai pas la reponse precise. Mon hypothese serait... "
    "mais je verifierai apres la soutenance.'",
    "Tu peux dire : 'C'est dans les perspectives de Phase 2 / 3'",
    "Le jury VALORISE l'honnetete intellectuelle",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(alert_box(
    "<b>RAPPEL :</b> les jurys ne testent pas si tu sais TOUT. Ils testent si tu sais "
    "REFLECHIR. Une question sans reponse parfaite est une opportunite de montrer ta "
    "capacite a structurer ta pensee.",
    kind="tip"))
story.append(PageBreak())

# CH 10 - Erreurs
story.append(Paragraph("Chapitre 10 - Erreurs a eviter", ST_CHAPTER))

story.append(Paragraph("10.1 Erreurs de presentation", ST_H1))
for x in [
    "<b>Lire les slides</b> mot pour mot (le jury sait lire)",
    "Dire 'tu' au lieu de 'vous'",
    "Parler trop vite par stress",
    "Tourner le dos au jury pour regarder l'ecran",
    "Critiquer Angular/React/Python (rester neutre)",
    "Promettre des choses non realisees",
    "Sous-vendre ton travail ('c'est rien de special')",
    "Sur-vendre ton travail (mentir / exagerer)",
]:
    story.append(Paragraph(f"- {x}", ST_LIST))

story.append(Paragraph("10.2 Erreurs techniques", ST_H1))
for x in [
    "<b>Faire la demo sans avoir verifie 5 min avant</b>",
    "Avoir des warnings/errors visibles en console",
    "Coder en live (sauf si tres prepare)",
    "Faire 'rm -rf' devant le jury (le stress fait des betises)",
    "Avoir le mot de passe d'admin visible",
    "Avoir l'API key Groq visible a l'ecran (CRITIQUE)",
    "Ne pas connaitre une partie de TON code",
]:
    story.append(Paragraph(f"- {x}", ST_LIST))

story.append(Paragraph("10.3 Erreurs de fond", ST_H1))
for x in [
    "Ne pas savoir expliquer une ligne de TON code",
    "Avoir copie-colle StackOverflow sans comprendre",
    "Dire que tu as fait quelque chose si l'autre membre l'a fait",
    "Eviter une question (toujours mieux d'admettre)",
    "Comparer ton projet a Google / OpenAI (humilite)",
    "Pretendre que c'est innovant alors que c'est standard",
]:
    story.append(Paragraph(f"- {x}", ST_LIST))
story.append(PageBreak())

# CH 11 - Conclusion
story.append(Paragraph("Chapitre 11 - Conclusion", ST_CHAPTER))

story.append(Paragraph("11.1 Phrases de cloture", ST_H1))
story.append(Paragraph(
    "Termine sur une note positive et ouverte :<br/><br/>"
    "<i>'En conclusion, FSBM Platform repond aux 4 enjeux poses : disponibilite 24/7, "
    "support multilingue, comprehension du langage naturel, et scalabilite. Le systeme "
    "est deja fonctionnel et pret pour une phase pilote. Les perspectives incluent "
    "l'authentification etudiants, l'integration WhatsApp, et une app mobile. "
    "Nous sommes a votre disposition pour vos questions. Merci de votre attention.'</i>",
    ST_BODY))

story.append(Paragraph("11.2 Pendant les questions", ST_H1))
for x in [
    "Ecouter <b>jusqu'au bout</b> avant de repondre",
    "Reformuler la question : 'Si je comprends bien, vous demandez...'",
    "Repondre directement, sans broder",
    "Si question complexe : 'Je vais structurer ma reponse en 3 points'",
    "Si tu ne sais pas : reconnaitre + proposer une piste",
    "Remercier : 'Merci pour cette question'",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("11.3 Apres la soutenance", ST_H1))
for x in [
    "Remercier le jury, sourire, poignee de main",
    "Quitter avec ton support, ne rien laisser sur l'ecran",
    "Profite du moment, tu as termine !",
    "Quel que soit le resultat : tu as appris enormement",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("11.4 Recap des 10 PDFs", ST_H1))
for i, t in enumerate([
    "Architecture Globale",
    "Frontend Angular Complet",
    "Backend FastAPI Complet",
    "MySQL + SQLAlchemy Complet",
    "MongoDB + NoSQL Complet",
    "NLP + IA Chatbot Complet",
    "APIs + Communication",
    "Securite Complete",
    "Workflow Complet",
    "Guide Soutenance (ce PDF)",
], 1):
    story.append(Paragraph(f"• PDF {i:02d} - {t}", ST_LIST))

story.append(alert_box(
    "Bonne chance pour ta soutenance ! Tu as fait un travail solide. Le jury verra "
    "ton travail, ta rigueur, ta capacite a expliquer. Reste calme, sois honnete, et "
    "passe un bon moment. Tu vas reussir.",
    kind="success"))

build_doc("10_Guide_Soutenance.pdf", story,
          "PDF 10 - Guide Soutenance",
          "FSBM Platform - Guide Soutenance")
