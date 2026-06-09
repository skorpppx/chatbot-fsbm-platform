# -*- coding: utf-8 -*-
"""Demo_Chatbot_FSBM.pdf — Demonstration academique des capacites reelles du chatbot."""
import re
from report_engine import *
from report_engine import _hr, _scaled
from front import cc
from reportlab.platypus import NextPageTemplate, PageBreak, Spacer, Paragraph

# ─── Nettoyage des reponses reelles (retrait emojis pour reportlab) ────────────
_EMOJI = re.compile("[\U0001F000-\U0001FAFF←-⇿⌀-➿⬀-⯿️⃣]")
def clean(t, n=130):
    t = _EMOJI.sub("", t).replace("**", "").replace("\n", " ").replace("  ", " ").strip()
    t = t.replace("{name_comma}", "").replace("{voc}", "khoya").replace("{nta_nti}", "")
    t = t.replace("{dayer_dayra}", "dayer").replace("{name_space}", "")
    return (t[:n] + "…") if len(t) > n else t


def cov(story):
    story += [NextPageTemplate("cover")]
    story += [Spacer(1, 1.4*cm)]
    story.append(cc("Universite Hassan II de Casablanca", 13, True, NAVY, sa=1))
    story.append(cc("Faculte des Sciences Ben M'Sick — Departement de Mathematiques et Informatique", 10, False, MUTED, sa=10))
    try: story.append(_scaled(LOGO_FSBM, max_w=7*cm, max_h=3*cm))
    except Exception: pass
    story += [Spacer(1, 0.5*cm), _hr(NAVY, 1.6), Spacer(1, 0.5*cm)]
    story.append(cc("DEMONSTRATION ACADEMIQUE", 13, True, ACCENT, sa=3))
    story.append(cc("Capacites Reelles du Chatbot Intelligent FSBM", 22, True, NAVY, lead=27, sa=8))
    story.append(cc("Matrice des questions, moteurs de reponse, limites, et scenarios de soutenance", 12.5, False, BLUE, lead=17, sa=14))
    story.append(_hr(LINE, 1.0)); story.append(Spacer(1, 0.5*cm))
    story.append(cc("Realise par : Akram BELMOUSSA · Zakaria BENGHAZALE · Nouhaila BEN SOUMANE", 11, True, NAVY_D, sa=10))
    story.append(cc("Encadre par : Pr. Habib BENLAHMER  —  Co-encadre par : Pr. Salma HANNOUNI", 10.5, False, INK, sa=2))
    story.append(cc("Licence en Developpement Informatique — Annee universitaire 2025-2026", 10.5, True, NAVY, sa=2))
    story += [NextPageTemplate("normal"), PageBreak()]


def build_demo():
    reset_numbering()
    s = []
    cov(s)

    # Sommaire
    s += plain_heading("Sommaire")
    toc = make_toc(); s.append(toc)

    # Intro
    s += chapter("Introduction a la Demonstration")
    s.append(para(
        "Ce document presente, de maniere academique et honnete, les <b>capacites reelles</b> du "
        "chatbot intelligent de la FSBM, ses <b>moteurs de reponse</b>, ses <b>limites</b>, et "
        "l'apport determinant de la <b>base de connaissances (FAQ)</b>. Les exemples et niveaux de "
        "fiabilite presentes ont ete obtenus en <b>interrogeant directement le moteur reel</b> "
        "(classifieur TF-IDF) sur des questions concretes."))
    s.append(section("Les moteurs de reponse reels du systeme"))
    s += table([
        ["Moteur", "Role reel dans le projet"],
        ["FAQ / TF-IDF", "Classifieur d'intentions trilingue (28 intentions, ~835 patterns). Reponses predefinies fiables."],
        ["Base de connaissances FSBM", "Donnees reelles (6 departements, filieres, 239 profs, doyen) + fsbm_knowledge.json."],
        ["Groq (LLaMA 3.3-70B)", "Grand modele de langage, mode avance, encadre par RAG."],
        ["HuggingFace (LLaMA 3 8B)", "Modele de repli (fallback) si Groq indisponible."],
        ["RAG", "Recuperation TF-IDF des contextes + generation : limite les hallucinations."],
    ], "Moteurs de reponse reellement implementes", col_widths=[2.6, 7.4])
    s.append(alert(
        "<b>Important :</b> il n'existe pas de modele LLaMA execute en local dans ce projet. "
        "Le terme \"LLaMA\" designe le modele <b>LLaMA 3.3-70B accessible via l'API Groq</b> et le "
        "modele de repli <b>LLaMA 3 8B via HuggingFace</b>. La colonne \"LLaMA\" des tableaux "
        "correspond donc au repli generatif.", "key"))
    s.append(section("Langues reellement supportees"))
    s.append(para(
        "Le chatbot prend en charge <b>trois langues</b>, confirmees par le code "
        "(<i>SUPPORTED_LANGS = [fr, en, darija]</i>) : le <b>francais</b>, l'<b>anglais</b>, et la "
        "<b>darija marocaine</b> (arabe dialectal, graphie latine et arabe). Il ne s'agit pas de "
        "l'arabe standard (MSA) mais bien du dialecte reellement parle par les etudiants."))

    s += _part1_matrice()
    s += _part2_trilingue()
    s += _part3_comparaison()
    s += _part4_limites()
    s += _part5_faq()
    s += _part6_scenarios()
    s += _part7_jury()

    build("Demo_Chatbot_FSBM.pdf", s, title="Demo Chatbot FSBM",
          author="A. BELMOUSSA, Z. BENGHAZALE, N. BEN SOUMANE")


# ══════════════════════════════════════════════════════════════════════════════
def _part1_matrice():
    el = chapter("Partie 1 — Matrice des Questions du Chatbot")
    el.append(para(
        "Le tableau ci-dessous croise des <b>questions reelles</b> par categorie avec le comportement "
        "<b>reellement observe</b> du moteur FAQ/TF-IDF (intention detectee et score de confiance "
        "mesures en direct), le comportement du mode generatif (Groq/RAG) et le niveau de fiabilite. "
        "Les cas ou la FAQ se trompe sont presentes en toute transparence : ils justifient le "
        "complement generatif."))
    el.append(alert(
        "Legende fiabilite : <b>Elevee</b> = intention correcte, confiance >= 0,80. "
        "<b>Moyenne</b> = intention approximative, confiance 0,40-0,80. "
        "<b>Faible</b> = hors corpus ou mauvaise intention (le mode Groq+RAG prend alors le relais).", "info"))

    def row(cat, q, faq, groq, fia):
        return [cat, q, faq, groq, fia]
    rows = [["Categorie", "Question reelle", "FAQ / TF-IDF (mesure)", "Groq / RAG", "Fiabilite"]]
    rows += [
        row("Administration", "Ou se trouve le service de scolarite ?", "stage_pfe (0,44) — INCORRECT", "Reponse correcte (RAG + base)", "Faible (FAQ)"),
        row("Administration", "Comment obtenir une attestation ?", "diplome (0,58) — approximatif", "Reformulation ciblee", "Moyenne"),
        row("Administration", "Comment retirer mon diplome ?", "diplome (1,00) — correct", "Idem (contexte RAG)", "Elevee"),
        row("Etudes", "Quelles sont les filieres disponibles ?", "filieres (0,76) — correct", "Liste + conseils", "Elevee"),
        row("Etudes", "Quels sont les modules du semestre ?", "filieres (0,58) — pas d'intent dedie", "Reponse via base modules", "Moyenne"),
        row("Enseignants", "Qui dirige le departement informatique ?", "filiere_di (0,55) — approximatif", "Pr. ADNAOUI Khalid (base reelle)", "Moyenne"),
        row("Enseignants", "Domaines de recherche d'un professeur ?", "hors corpus FAQ", "Base Scholar (5 profs reels)", "Moyenne"),
        row("Horaires", "Ou trouver les emplois du temps ?", "emploi_du_temps (0,55) — correct", "Idem + liens", "Elevee"),
        row("Horaires", "Quand commencent les examens ?", "examens (1,00) — correct", "Idem (contexte)", "Elevee"),
        row("Recherche", "Publications d'un enseignant ?", "hors corpus FAQ", "Base Scholar (Benlahmer : 2785 cit.)", "Moyenne"),
        row("Orientation", "Quelle filiere choisir ?", "filieres (1,00) — liste", "Conseil personnalise (generatif)", "Elevee"),
        row("Orientation", "Quels sont les debouches ?", "partiel (careers en base)", "Synthese generative (RAG)", "Moyenne"),
        row("General", "Presente la FSBM", "identite_chatbot (0,82)", "Presentation + base (doyen, 239 profs)", "Elevee"),
        row("General", "Presente l'Universite Hassan II", "hors corpus FAQ", "Reponse generative (Groq)", "Moyenne"),
    ]
    el += table(rows, "Matrice reelle des questions et des moteurs de reponse",
                col_widths=[1.6, 3.1, 2.6, 2.4, 1.3], font=7.6)
    el.append(para(
        "Cette matrice illustre la <b>complementarite</b> des moteurs : la FAQ excelle sur les "
        "questions frequentes et bien formulees (examens, inscription, bourses : confiance 1,00), "
        "tandis que le mode generatif encadre par RAG prend le relais pour les questions hors corpus "
        "ou mal classees, en s'appuyant sur la base de donnees reelle de la FSBM."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _part2_trilingue():
    el = chapter("Partie 2 — Demonstration Trilingue")
    el.append(para(
        "Le chatbot detecte automatiquement la langue et repond dans celle-ci. Les echanges "
        "ci-dessous sont des <b>reponses reelles</b> du moteur (extraits), pour le francais, la "
        "darija marocaine et l'anglais — les trois langues effectivement supportees."))

    def echange(titre, q, r, lang):
        out = [Paragraph(titre, ST["h2n"])]
        out += table([
            ["Question (" + lang + ")", q],
            ["Reponse reelle du chatbot", clean(r, 220)],
        ], "Echange reel — " + lang, col_widths=[2.6, 7.4], font=8.4)
        return out

    el.append(section("Categorie Etudes — Filieres"))
    el += echange("Francais", "Quelles sont les filieres disponibles ?",
                  "La FSBM propose 7 licences + 18 masters : SMI Sciences Math & Informatique, DI Developpement Informatique...", "FR")
    el += echange("Darija", "shno hia les filieres ?",
                  "La FSBM propose 7 licences + 18 masters : SMI, DI, SMA... (detecte et repond)", "Darija")
    el += echange("Anglais", "What are the available programs?",
                  "I'm the FSBM Smart Chatbot! I can help you with Registration, Programs & Masters, Schedules & Exams...", "EN")

    el.append(section("Categorie Administration — Inscription"))
    el += echange("Francais", "Comment s'inscrire a la FSBM ?",
                  "Inscription FSBM - etapes : 1. Preinscription en ligne sur preins.univh2c.ma. Remplis le formulaire...", "FR")
    el += echange("Darija", "kifash ndir l'inscription ?",
                  "Tassjil f FSBM - l'etapes b tafassil : 1. Preinscription online : Mchi l preins.univh2c.ma o kml lformulaire...", "Darija")
    el += echange("Anglais", "How do I register at FSBM?",
                  "FSBM Enrollment - Step-by-step: 1. Online pre-registration: Go to preins.univh2c.ma. Fill the form...", "EN")

    el.append(section("Categorie Conversationnel — Accueil et soutien"))
    el += echange("Darija", "salam, ki dayer ?",
                  "L7amdulilah khoya ! Ana mzyan, jaheh n3awnek f ay haja. Wach kayna chi haja li bghiti tssawel ?", "Darija")
    el += echange("Francais", "Je suis stresse pour les examens",
                  "Je te comprends, le stress des examens est tres commun. Methode : Pomodoro 25 min + 5 min pause, annales...", "FR")
    el.append(alert(
        "La prise en charge de la <b>darija</b> (461 patterns) et la <b>personnalisation</b> "
        "(formules khoya/khti selon le genre detecte) constituent des apports originaux rarement "
        "presents dans les chatbots generalistes.", "tip"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _part3_comparaison():
    el = chapter("Partie 3 — Comparaison des Moteurs")
    el.append(para(
        "Le tableau suivant compare les trois moteurs selon des criteres operationnels. \"LLaMA\" "
        "designe ici le repli generatif (LLaMA 3 8B via HuggingFace)."))
    el += table([
        ["Critere", "FAQ / TF-IDF", "Groq (LLaMA 3.3-70B)", "LLaMA (repli HF 8B)"],
        ["Rapidite", "Tres rapide (~30 ms)", "Rapide (~150-250 ms)", "Lent (~1-3 s)"],
        ["Cout", "Nul (local)", "Gratuit (quota)", "Gratuit (quota)"],
        ["Precision (FSBM)", "Elevee si dans le corpus", "Elevee avec RAG", "Moyenne"],
        ["Reponses generales", "Faible (corpus borne)", "Tres bonne", "Bonne"],
        ["Multilingue", "FR / EN / Darija", "Oui (large)", "Oui"],
        ["Maintenance", "Mise a jour du dataset", "Aucune (API)", "Aucune (API)"],
        ["Dependance Internet", "Aucune", "Oui (API)", "Oui (API)"],
        ["Explicabilite", "Elevee (intention + score)", "Faible (boite noire)", "Faible"],
        ["Risque d'hallucination", "Nul", "Reduit par RAG", "Reduit par RAG"],
    ], "Comparaison des moteurs de reponse", col_widths=[2.4, 2.6, 2.7, 2.3], font=8.0)
    el.append(para(
        "Aucun moteur n'est superieur en tout : le systeme combine leurs forces via une "
        "<b>cascade</b> (Groq, puis HuggingFace, puis TF-IDF) garantissant rapidite, fiabilite et "
        "<b>disponibilite de 100 %</b>."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _part4_limites():
    el = chapter("Partie 4 — Limites du Chatbot")
    el.append(para(
        "Une presentation academique honnete exige d'exposer clairement les limites du systeme. "
        "Elles sont reelles et documentees ci-dessous."))
    el.append(section("Limites de la FAQ"))
    el += bullets([
        "Ne repond qu'aux <b>sujets presents dans le corpus</b> (28 intentions).",
        "<b>Ne raisonne pas</b> : elle reconnait une intention, elle ne deduit pas.",
        "<b>N'invente jamais</b> de reponse — ce qui est une force pour la fiabilite, une limite pour la couverture.",
        "Exemple reel observe : \"modules du semestre\" est classe en <i>filieres</i> faute d'intention dediee.",
    ])
    el.append(section("Limites du TF-IDF"))
    el += bullets([
        "Repose sur la <b>correspondance lexicale</b> : sensible aux mots-cles et reformulations.",
        "Depend de la <b>qualite et de la couverture du corpus</b> par langue.",
        "Exemple reel : \"Ou se trouve le service de scolarite ?\" mal classe (stage_pfe, 0,44) car proche lexicalement.",
        "Comprehension <b>semantique limitee</b> (pas d'embeddings neuronaux dans ce moteur).",
    ])
    el.append(section("Limites de Groq"))
    el += bullets([
        "<b>Necessite une connexion Internet</b> (API distante).",
        "Depend d'un <b>service externe</b> (disponibilite, conditions d'usage).",
        "<b>Cout potentiel futur</b> au-dela des quotas gratuits.",
        "Risque residuel d'<b>hallucination</b>, attenue mais non nul, controle par le RAG.",
    ])
    el.append(section("Limites de LLaMA (repli)"))
    el += bullets([
        "Un deploiement <b>local</b> exigerait des <b>ressources materielles</b> importantes (GPU, RAM).",
        "<b>Consommation memoire</b> et <b>temps de calcul</b> eleves pour les grands modeles.",
        "Le repli HuggingFace est <b>plus lent</b> (~1-3 s) que Groq.",
    ])
    el.append(section("Limites globales"))
    el += bullets([
        "<b>Donnees manquantes</b> : certaines informations (modules detailles) ne sont pas publiees.",
        "<b>Mises a jour necessaires</b> : la base doit etre tenue a jour (annonces, calendriers).",
        "<b>Informations potentiellement obsoletes</b> si la base n'est pas rafraichie.",
        "La qualite des reponses generatives depend de la <b>qualite des contextes</b> recuperes (RAG).",
    ])
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _part5_faq():
    el = chapter("Partie 5 — Importance de la FAQ")
    el.append(para(
        "Une question centrale du jury sera : <i>pourquoi conserver une FAQ alors qu'un grand modele "
        "de langage existe ?</i> La reponse tient en un mot : la <b>fiabilite institutionnelle</b>."))
    el.append(section("Sans FAQ : le risque d'hallucination"))
    el.append(para(
        "Un grand modele de langage seul, interroge sur des informations universitaires precises "
        "(dates d'examens, procedures, responsables), peut :"))
    el += bullets([
        "<b>Halluciner</b> : produire une reponse fausse mais plausible.",
        "<b>Inventer</b> des donnees universitaires (dates, noms, montants) inexistantes.",
        "Induire l'etudiant en erreur sur des demarches administratives sensibles.",
    ])
    el.append(section("Avec FAQ : la garantie d'exactitude"))
    el += bullets([
        "Fournit des <b>reponses verifiees</b> et controlees par l'administration.",
        "Garantit l'<b>exactitude institutionnelle</b> sur les sujets cles.",
        "<b>Reduit les hallucinations</b> : le RAG fournit au modele des contextes fiables a reformuler.",
        "Ameliore la <b>confiance</b> de l'utilisateur et la credibilite du service.",
    ])
    el.append(section("Schema de decision du systeme"))
    el += figure_mermaid(r'''flowchart TD
  U["Utilisateur"] --> Q["Question"]
  Q --> NLP["FAQ / TF-IDF<br/>(classification d'intention)"]
  NLP --> D{"Confiance suffisante ?"}
  D -- Oui --> R1["Reponse FIABLE<br/>(predefinie + base FSBM)"]
  D -- Non --> RAG["Recuperation RAG<br/>(contextes verifies)"]
  RAG --> G["Groq / LLaMA 3"]
  G --> R2["Reponse generative<br/>ENCADREE par les contextes"]
  G -. indisponible .-> HF["HuggingFace (repli)"]
  HF -. indisponible .-> NLP
''', "Architecture de decision : la FAQ d'abord, le generatif encadre ensuite", max_h=13*cm)
    el.append(alert(
        "La FAQ n'est pas en concurrence avec le LLM : elle le <b>fiabilise</b>. Le LLM apporte le "
        "naturel et la couverture ; la FAQ et le RAG apportent l'exactitude. C'est la combinaison "
        "qui fait la valeur du systeme.", "key"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _part6_scenarios():
    el = chapter("Partie 6 — Scenarios de Demonstration")
    el.append(para(
        "Voici 30 scenarios prets a etre joues lors de la soutenance, couvrant les moteurs et les "
        "langues. Pour chacun : la question, la reponse attendue, le moteur sollicite et l'objectif "
        "pedagogique."))
    sc = [
        ("Comment s'inscrire a la FSBM ?", "Etapes detaillees d'inscription", "FAQ (1,00)", "Montrer la fiabilite FAQ"),
        ("Quand commencent les examens ?", "Sessions hiver/ete + rattrapage", "FAQ (1,00)", "Confiance maximale"),
        ("Comment avoir une bourse ?", "Criteres + montants ONOUSC", "FAQ (1,00)", "Reponse institutionnelle"),
        ("Quelles sont les filieres ?", "7 licences + masters reels", "FAQ + base FSBM", "Donnees reelles"),
        ("shno hia les filieres ?", "Meme reponse en contexte darija", "FAQ darija", "Multilinguisme"),
        ("salam, ki dayer ?", "Accueil chaleureux en darija", "FAQ darija (0,90)", "Naturel conversationnel"),
        ("What are the programs?", "Reponse en anglais", "FAQ EN", "Support anglais"),
        ("Je suis stresse pour les examens", "Conseils + soutien", "FAQ empathie (0,80)", "Dimension humaine"),
        ("Ou se trouve le service de scolarite ?", "Localisation + horaires", "Groq + RAG (FAQ faible)", "Limite FAQ -> RAG"),
        ("Quels sont les modules du semestre ?", "Liste via base modules", "Groq + base", "Hors corpus FAQ"),
        ("Qui dirige le departement informatique ?", "Pr. ADNAOUI Khalid", "Base FSBM reelle", "Donnee reelle verifiee"),
        ("Qui est le doyen de la FSBM ?", "Pr. Abdeslam EL BOUARI", "Base FSBM reelle", "Donnee reelle"),
        ("Domaines de recherche du Pr. Benlahmer ?", "TALN, web semantique...", "Base Scholar reelle", "Recherche scientifique"),
        ("Combien de professeurs a la FSBM ?", "239 enseignants", "Base FSBM reelle", "Chiffre officiel"),
        ("Presente la FSBM", "Presentation + doyen + chiffres", "FAQ + base", "Synthese institutionnelle"),
        ("Presente l'Universite Hassan II", "Reponse generative", "Groq", "Connaissance generale"),
        ("Quelle filiere choisir apres le bac ?", "Conseil oriente", "Groq + RAG", "Orientation"),
        ("Quels debouches pour le DI ?", "Metiers du developpement", "Groq + base careers", "Insertion professionnelle"),
        ("Comment retirer mon diplome ?", "Procedure + documents", "FAQ (1,00)", "Procedure administrative"),
        ("Comment obtenir une attestation ?", "Reponse approximative -> precision", "FAQ (0,58) + Groq", "Montrer la nuance"),
        ("kifash ndir l'inscription ?", "Etapes en darija", "FAQ darija", "Procedure multilingue"),
        ("fin kayn emploi du temps ?", "Liens emplois du temps", "FAQ darija (0,84)", "Horaires en darija"),
        ("contact dyal scolarite ?", "Coordonnees scolarite", "FAQ darija (0,94)", "Contact en darija"),
        ("Y a-t-il des clubs etudiants ?", "Liste des clubs", "Base FSBM", "Vie etudiante"),
        ("Quelles sont les actualites ?", "Annonces reelles recentes", "Base + web fetch", "Information a jour"),
        ("Bonjour, qui es-tu ?", "Presentation du chatbot", "FAQ identite (0,82)", "Identite de l'agent"),
        ("Merci beaucoup !", "Formule de politesse", "FAQ remerciement", "Cloture courtoise"),
        ("Question hors sujet (meteo)", "Recentrage poli sur la FSBM", "FAQ/Groq", "Garde-fou de perimetre"),
        ("Question ambigue tres courte", "Demande de reformulation + suggestions", "FAQ (seuil)", "Gestion de l'incertitude"),
        ("Activer le mode IA avance (LLaMA 3)", "Reponse generative riche", "Groq + RAG", "Demonstration du mode LLM"),
    ]
    rows = [["#", "Question", "Reponse attendue", "Moteur", "Objectif pedagogique"]]
    for i, (q, r, m, o) in enumerate(sc, 1):
        rows.append([str(i), q, r, m, o])
    el += table(rows, "30 scenarios de demonstration pour la soutenance",
                col_widths=[0.6, 3.0, 2.7, 1.9, 2.2], font=7.4)
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _part7_jury():
    el = chapter("Partie 7 — Questions Potentielles du Jury")
    el.append(para(
        "Cinquante questions frequemment posees en soutenance, avec des elements de reponse "
        "concis et defendables."))
    qa = [
        ("Pourquoi un chatbot pour la FSBM ?", "Decharger la scolarite des questions repetitives et offrir un acces 24h/24, multilingue."),
        ("Pourquoi le TF-IDF et pas seulement un LLM ?", "Fiabilite, rapidite (~30 ms), cout nul, fonctionnement hors ligne et explicabilite."),
        ("Pourquoi Groq ?", "Inference LLaMA 3 a tres faible latence, gratuite (quota), sans infrastructure a gerer."),
        ("Pourquoi la FAQ reste-t-elle utile avec un LLM ?", "Elle garantit l'exactitude institutionnelle et reduit les hallucinations via le RAG."),
        ("Qu'est-ce que le RAG ?", "Retrieval-Augmented Generation : on injecte des contextes verifies dans l'invite du LLM."),
        ("Comment evitez-vous les hallucinations ?", "RAG + seuil de confiance + perimetre borne + repli FAQ local."),
        ("Pourquoi MySQL ?", "Donnees academiques fortement relationnelles, integrite forte (ACID), 3NF."),
        ("Pourquoi MongoDB ?", "Conversations et analytics semi-structurees, volumetrie et flexibilite."),
        ("Pourquoi deux bases (polyglotte) ?", "Choisir le bon outil par nature de donnee plutot qu'un modele unique."),
        ("Pourquoi Angular ?", "Framework complet, TypeScript, signals performants, structurant pour un projet de cette taille."),
        ("Pourquoi FastAPI ?", "Asynchrone, validation Pydantic automatique, documentation Swagger generee."),
        ("Pourquoi une architecture micro-services ?", "Decouplage, evolutivite, isolation des pannes, scalabilite par service."),
        ("Comment garantissez-vous la disponibilite ?", "Cascade de repli Groq -> HuggingFace -> TF-IDF local : 100 % de disponibilite."),
        ("Quelles langues sont supportees ?", "Francais, anglais et darija marocaine (graphie latine et arabe)."),
        ("Comment detectez-vous la langue ?", "Detecteur hybride : script arabe, chiffres darija 3/7/9, mots-cles lexicaux."),
        ("Comment fonctionne le TF-IDF ?", "Vectorisation ponderee des termes + similarite cosinus avec les patterns."),
        ("Qu'est-ce que la similarite cosinus ?", "Mesure de l'angle entre deux vecteurs, independante de la norme."),
        ("Comment est gere le multilinguisme ?", "Trois modeles TF-IDF independants, un par langue, aiguilles par la detection."),
        ("Combien d'intentions reconnait le chatbot ?", "28 intentions, ~835 patterns d'entrainement (188 FR, 186 EN, 461 darija)."),
        ("Comment securisez-vous l'administration ?", "Authentification JWT + bcrypt, controle d'acces par roles (RBAC)."),
        ("Comment evitez-vous les injections SQL ?", "Requetes parametrees via SQLAlchemy, jamais de concatenation."),
        ("Comment gerez-vous le XSS ?", "Angular echappe automatiquement le contenu interpole."),
        ("Comment validez-vous les entrees ?", "Schemas Pydantic (types, longueurs, formats) cote backend."),
        ("Ou sont stockes les secrets ?", "Dans un fichier .env exclu du depot, jamais dans le code."),
        ("Quelle est la latence moyenne ?", "~150 ms en mode classique, ~250 ms en mode Groq+RAG."),
        ("Comment avez-vous teste le systeme ?", "33 tests automatises (auth, CRUD, moderation, upload) + tests fonctionnels."),
        ("Les donnees sont-elles reelles ?", "Oui pour l'institutionnel (fsbm.ma, Scholar) ; les fiches etudiants sont modelisees (confidentialite)."),
        ("D'ou viennent les donnees professeurs ?", "Site officiel fsbm.ma (239 enseignants) + Google Scholar pour 5 profils verifies."),
        ("Comment la FAQ est-elle alimentee ?", "Dataset multilingue + base de connaissances reelle (fsbm_knowledge.json)."),
        ("Que se passe-t-il si Groq tombe ?", "Repli automatique vers HuggingFace, puis vers le TF-IDF local."),
        ("Le chatbot peut-il se tromper ?", "Oui : nous l'avons montre (ex. scolarite mal classee). D'ou le seuil et le RAG."),
        ("Comment gerez-vous une faible confiance ?", "Demande de reformulation + suggestions de questions proches."),
        ("Le systeme apprend-il en continu ?", "Pas encore : les questions a faible confiance sont journalisees pour enrichir le dataset."),
        ("Quelle est la part de la darija ?", "461 patterns, soit plus de la moitie du corpus : un differenciateur fort."),
        ("Comment personnalisez-vous les reponses ?", "Detection du genre/nom et substitution de formules (khoya, khti, lalla)."),
        ("Pourquoi pas ChatGPT directement ?", "Pas de contexte FSBM, risque d'hallucination, cout, pas de souverainete des donnees."),
        ("Quelle est la difference avec un FAQ statique ?", "Comprehension du langage naturel, multilingue, et complement generatif."),
        ("Comment l'admin met-il a jour les donnees ?", "Espace d'administration securise (CRUD annonces, academique, FAQ, moderation)."),
        ("La plateforme est-elle responsive ?", "Oui, avec mode sombre et design adapte mobile."),
        ("Comment deploieriez-vous en production ?", "Reverse proxy nginx + HTTPS, conteneurisation Docker, CI/CD (perspectives)."),
        ("Quelle est la taille du dataset NLP ?", "~835 patterns sur 28 intentions, 3 langues."),
        ("Comment mesurez-vous la qualite ?", "Confiance TF-IDF, feedback utilisateur (note 1-5), questions de reference."),
        ("Quelle note de satisfaction ?", "4,5/5 sur l'assistant (avis collectes dans la plateforme)."),
        ("Quelles perspectives d'evolution ?", "App mobile, apprentissage continu, embeddings, integration a l'ENT."),
        ("Pourquoi la Licence Developpement Informatique ?", "Le projet mobilise le full-stack, les BDD et l'IA : coeur de cette filiere reelle de la FSBM."),
        ("Quelle est votre contribution personnelle ?", "Architecture, dataset trilingue, RAG, cascade de repli, integration des donnees reelles."),
        ("Quelles difficultes avez-vous rencontrees ?", "Conflits de ports Windows, integrite des donnees reelles, encadrement des hallucinations."),
        ("Le projet est-il maintenable ?", "Oui : code modulaire, separation des responsabilites, documentation complete."),
        ("Quel est l'impact attendu ?", "Acces unifie 24h/24 pour les etudiants, decharge de la scolarite, image modernisee."),
        ("Que feriez-vous avec plus de temps ?", "Synchroniser la FAQ avec le NLP, ajouter la voix, et completer les 239 fiches profs."),
    ]
    rows = [["#", "Question du jury", "Element de reponse"]]
    for i, (q, a) in enumerate(qa, 1):
        rows.append([str(i), q, a])
    el += table(rows, "50 questions potentielles du jury et elements de reponse",
                col_widths=[0.6, 3.6, 5.8], font=7.4)
    el.append(spacer(0.3))
    el.append(quote("Un bon systeme n'est pas celui qui ne se trompe jamais, mais celui qui sait "
                    "quand il ne sait pas — et delegue alors a une source fiable.", "Principe de conception du projet"))
    return el


if __name__ == "__main__":
    build_demo()
