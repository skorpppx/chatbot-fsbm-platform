# -*- coding: utf-8 -*-
"""
Donnees REELLES et VERIFIEES de la Faculte des Sciences Ben M'Sick.
Sources : site officiel fsbm.ma (captures du 02/06/2026) + Google Scholar (encadrant).
AUCUNE donnee de ce fichier n'est inventee : tout provient d'une source verifiable.
"""

DOYEN = "Pr. Abdeslam EL BOUARI"

CONTACT = {
    "email": "fsbm.contact@univh2c.ma",
    "tel": "+212 6 61 44 24 27",
    "adresse": "Boulevard Driss El Harti, Ben M'Sik, Casablanca, Maroc",
    "site": "fsbm.ma",
}

NB_PROFS_REEL = 239   # affiche par fsbm.ma/faculty ("239 professeur(s) trouve(s) - 20 pages")

# Encadrant : profil Google Scholar verifie (user=upOdTrEAAAAJ)
ENCADRANT_SCHOLAR = {
    "nom": "Pr. El Habib BENLAHMAR",
    "affiliation": "Professeur d'Informatique, FSBM, Universite Hassan II de Casablanca",
    "interets": "Moteurs de recherche, Web semantique, TALN, apprentissage automatique et profond",
    "citations": 2785,
    "h_index": 24,
    "i10_index": 61,
    "pub_phare": "A system for educational and vocational guidance in Morocco: Chatbot "
                 "E-Orientation (2020)",
}

# 6 departements reels + chefs (fsbm.ma/departements)
DEPARTEMENTS = [
    {"code": "BIO", "nom": "Biologie", "chef": "Pr. FARH Mohamed"},
    {"code": "CHI", "nom": "Chimie", "chef": "Pr. EL KOUALI Mhammed"},
    {"code": "GEO", "nom": "Geologie", "chef": "Pr. MOUFLIH Mustapha"},
    {"code": "MI",  "nom": "Mathematiques et Informatique", "chef": "Pr. ADNAOUI Khalid"},
    {"code": "PHY", "nom": "Physiques", "chef": "Pr. MAIZROUI M'hammed"},
    {"code": "SCH", "nom": "Sciences de la Communication et Humanites", "chef": "Pr. Nadia CHAFIQ"},
]

# Filieres reelles (dept, intitule, type, responsable) — verifiees sur fsbm.ma
FILIERES = [
    # Mathematiques et Informatique
    ("MI", "Statistiques", "LICENCE", "Pr. FERJOUCHA Hanane"),
    ("MI", "Analyse Mathematique", "LICENCE", "Pr. BOUDKHIA Khadija"),
    ("MI", "Cybersecurite et Administration des Systemes et Reseaux", "LICENCE", "Pr. OUAHABI Sara"),
    ("MI", "Developpement Full Stack", "LICENCE", "Pr. Mohssine Bensebii"),
    ("MI", "Administration Reseaux et Systemes", "LICENCE", "Pr. ACHTAICH Khadija"),
    ("MI", "Developpement Informatique", "LICENCE", "Pr. SAEL Nihal"),
    # Physiques
    ("PHY", "Physique Appliquee", "LICENCE", "Pr. SAID TADLFIK"),
    ("PHY", "Electronique, Systemes embarques et Telecommunication", "LICENCE", "Pr. KASSMI Aziza"),
    ("PHY", "Mecanique Energetique", "LICENCE", "Pr. MOURABIT M. Baika"),
    ("PHY", "Physique et Ingenierie des Materiaux (PIM)", "LICENCE", "Pr. ABDERRATI Kamal"),
    ("PHY", "Traitement de l'Information", "MASTER", "Pr. ATOUF Issam"),
    ("PHY", "Materiaux Intelligents et Systemes Energetiques", "MASTER", "Pr. EDDIAI Adil"),
    # Chimie
    ("CHI", "Genie des Materiaux", "LICENCE", "Pr. MEHDAOUI Boubker"),
    ("CHI", "Procedes Analytiques et Industriels", "LICENCE", "Pr. BENHANI Laila"),
    ("CHI", "Instrumentation, Procedes, Analyse et Qualite", "MASTER", "Pr. MOUMOU Mohamed"),
    ("CHI", "Genie des Materiaux et Energie", "MASTER", "Pr. SADIK Chaouki"),
    # Biologie
    ("BIO", "Gestion de l'Environnement et des Ressources Naturelles", "LICENCE", "Pr. ABDELMOTTALIB"),
    ("BIO", "Sciences Biomedicales Appliquees", "LICENCE", "Pr. FARH Mohamed"),
    ("BIO", "Biotechnologie et Production Vegetale", "LICENCE", "Pr. MOUHTADI Ahmed"),
    ("BIO", "Sciences de la Sante", "MASTER", "Pr. Hassan TAKI"),
    ("BIO", "Biologie et Sante", "MASTER", "Pr. Amal BOUSFIHA"),
    ("BIO", "Biotechnologie et Qualite", "MASTER", "Pr. ECH-CHEBRT EL KETTANI M. Anass"),
    # Geologie
    ("GEO", "Geosciences et Georessources", "LICENCE", "Pr. OUKASSOU Mustapha"),
    ("GEO", "Geomatique Appliquee aux Geosciences et a l'Environnement", "MASTER", "Pr. MAIMOUNI Soufiane"),
    ("GEO", "Geologie Appliquee a la Prospection des Ressources Naturelles", "MASTER", "Pr. ALAOUSS Sadok"),
]

# Echantillon de professeurs reels (noms tels qu'affiches sur fsbm.ma/faculty)
PROFS_REELS = [
    ("AADJOUR Lalla Malika", "MCH"), ("RAJI Halima", "MC"), ("HANOUNE Mostafa", "Chef d'equipe"),
    ("TAKI Hassan", "-"), ("ZAHOUR Ghalem", "PES"), ("MOUNA Latifa Bouamrani", "PES, Directeur de labo"),
    ("ALIKOUSS Saida", "PES, Coordinatrice de Master"), ("EL KOUALI Mhammed", "Chef de dept Chimie"),
    ("ACHIK Imad", "MCH, Coordinateur de filiere"), ("Nadia CHAFIQ", "Chef de dept SCH"),
    ("BAROUDI Zouhir", "-"), ("SAMIR Mohamed", "-"), ("EL HILALI Mohamed", "-"),
    ("SADIK Chaouki", "MCH"), ("EL BERRAI Imane", "MCH, Chef d'equipe"), ("GHAFIRI Abdessamad", "-"),
    ("RADALLAH Driss", "-"), ("ADLOUNI Hassani Ahmed", "-"), ("SALIH-ALJ Hanane", "-"),
    ("BELOUAFA Soumia", "-"), ("NORDINE Aicha", "-"), ("ABOURRICHE Abdelmjid", "-"),
    ("BOURJA Lamia", "-"), ("YOUSFI Samia", "-"), ("BENNANI Laila", "-"), ("RADID Mohamed", "-"),
    ("BORIKY Driss", "-"), ("MOUNIR Bahija", "-"), ("AMEGRISSI Fatiha", "-"), ("MOULINE Jamal", "-"),
    ("ADNAOUI Khalid", "MCH, Chef de dept Math-Info"), ("BOUGGAR Driss", "MC"),
    ("ETTAOUFIK Abdelaziz", "PES"), ("FERJOUCHA Hanane", "-"), ("MOHTADI Karima", "-"),
    ("SAILE Rachid", "-"), ("EL KHASMI Mohammed", "-"), ("FARH Mohamed", "Chef de dept Biologie"),
    ("SLIMANI Abdellatif", "MC"), ("CHEMLAL Yiwen", "-"),
]

SOURCES = [
    "Site officiel de la Faculte des Sciences Ben M'Sick — fsbm.ma "
    "(pages Departements, Formation, Corps Professoral, Mot du Doyen ; captures du 02/06/2026)",
    "Google Scholar — profil de l'encadrant Pr. El Habib Benlahmar "
    "(scholar.google.com/citations?user=upOdTrEAAAAJ)",
    "Portail de l'Universite Hassan II de Casablanca — univh2c.ma",
]

# Domaine de courriel institutionnel reel
EMAIL_DOMAIN = "univh2c.ma"

# Chiffres officiels reels affiches par fsbm.ma (page Programmes)
STATS_OFFICIELLES = {
    "etudiants": 11994,
    "departements": 6,
    "licences": 18,
    "masters": 12,
    "doctorats": 4,
    "filieres": 30,            # 18 licences + 12 masters
    "professeurs": 239,
    "laboratoires": 12,
    "entreprises_partenaires": 160,
}

# 5 professeurs avec metriques Google Scholar REELLES verifiees
# (obtenues via le reseau de co-auteurs de l'encadrant Pr. Benlahmar)
SCHOLAR_PROFS = [
    {"nom": "Pr. El Habib BENLAHMAR", "first": "El Habib", "last": "BENLAHMAR", "dep": "MI",
     "affiliation": "FSBM, UH2C", "grade": "PES",
     "interets": "TALN, web semantique, apprentissage automatique", "scholar_id": "upOdTrEAAAAJ",
     "citations": 2785, "h_index": 24, "i10_index": 61, "role": "Encadrant du projet"},
    {"nom": "Pr. Sanaa EL FILALI", "first": "Sanaa", "last": "EL FILALI", "dep": "MI",
     "affiliation": "FSBM, UH2C", "grade": "PES",
     "interets": "IoT, IA, apprentissage automatique, TALN", "scholar_id": "peesMqoAAAAJ",
     "citations": 1164, "h_index": 13, "i10_index": 14, "role": "Professeure d'informatique"},
    {"nom": "Pr. Omar ZAHOUR", "first": "Omar", "last": "ZAHOUR", "dep": "MI",
     "affiliation": "FSBM, UH2C", "grade": "PH",
     "interets": "Chatbots, orientation educative, TALN, BERT", "scholar_id": "wUlKz4UAAAAJ",
     "citations": 182, "h_index": 5, "i10_index": 4, "role": "Chercheur (chatbots educatifs)"},
    {"nom": "Pr. Kamal EL GUEMMAT", "first": "Kamal", "last": "EL GUEMMAT", "dep": "MI",
     "affiliation": "UH2C", "grade": "PH",
     "interets": "Data science, e-learning, big data, machine learning", "scholar_id": "JtS68twAAAAJ",
     "citations": 395, "h_index": 13, "i10_index": 15, "role": "Chercheur"},
    {"nom": "Pr. Mohamed TALEA", "first": "Mohamed", "last": "TALEA", "dep": "MI",
     "affiliation": "UH2C", "grade": "PES",
     "interets": "Theorie des graphes, systemes intelligents, reseaux", "scholar_id": "3ztbunUAAAAJ",
     "citations": 6755, "h_index": 39, "i10_index": 121, "role": "Professeur"},
]

# Actualites REELLES (page Actualites et Annonces de fsbm.ma, 2025)
NEWS = [
    ("Inscription au Cycle de Doctorat 2025-2026", "RECHERCHE", "2025-07-23",
     "La Faculte des Sciences Ben M'Sick - Universite Hassan II de Casablanca informe l'ensemble "
     "des doctorants et des nouveaux candidats au doctorat du lancement du calendrier universitaire "
     "officiel pour l'annee academique 2025-2026."),
    ("Avis d'ouverture de candidature au poste de Chef de service", "SERVICES", "2025-07-02",
     "Avis d'ouverture de candidature au poste de Chef de service vacant a la Faculte des Sciences "
     "Ben M'Sick."),
    ("Resultat du Conseil de Discipline", "CAMPUS", "2025-06-18",
     "Le Conseil de Discipline, reuni le 15 juin 2025, a statue sur plusieurs cas d'infractions au "
     "reglement interieur."),
    ("Calendrier universitaire 2025-2026", "CAMPUS", "2025-07-23",
     "Publication du calendrier universitaire officiel de la Faculte des Sciences Ben M'Sick pour "
     "l'annee academique 2025-2026."),
]

# Noms reels supplementaires releves (pages 6 a 13 de fsbm.ma/faculty)
PROFS_REELS += [
    ("BENLATTAR Mourad", "-"), ("AHARRANE Nabil", "-"), ("CHAHID Mustapha", "-"),
    ("MAZROUI M'hammed", "Chef de dept Physiques"), ("MOULTIF Rachida", "-"), ("OUASKIT Said", "-"),
    ("EL HAITAMY Ouafae", "-"), ("DEZARI Aouatif", "-"), ("EL HAFIDI Moulay Youssef", "-"),
    ("SAKHI Zoubida", "-"), ("BENNAI Mohamed", "-"), ("KARTOUNI Abdelkrim", "-"),
    ("ZERDANI Ilham", "-"), ("BELGHITI Ayoub", "-"), ("MOUSLIM Assia", "-"), ("MENGGAD Mohammed", "-"),
    ("TABITE Rabab", "-"), ("AIT HAMOU Sanaa", "-"), ("IOUNES Nadia", "-"), ("ROHI Latifa", "-"),
]

def stats_reelles():
    nb_lic = sum(1 for f in FILIERES if f[2] == "LICENCE")
    nb_mas = sum(1 for f in FILIERES if f[2] == "MASTER")
    return {
        "departements": len(DEPARTEMENTS),
        "filieres": len(FILIERES),
        "licences": nb_lic,
        "masters": nb_mas,
        "professeurs": NB_PROFS_REEL,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  DONNEES COMPLETES (relevees sur fsbm.ma - remplacent les definitions ci-dessus)
# ═══════════════════════════════════════════════════════════════════════════════
DOYEN_MESSAGE = (
    "La Faculte des Sciences Ben M'Sick (FSBM) est un etablissement ouvert et inclusif, fier de "
    "former chaque annee des milliers d'etudiants marocains et internationaux. Portee par une "
    "vision d'excellence, d'innovation et de responsabilite sociale, la FSBM s'engage a offrir un "
    "enseignement de qualite, a stimuler une recherche scientifique ambitieuse et a promouvoir une "
    "gouvernance moderne et participative. Au coeur de notre projet, nos etudiants, nos chercheurs "
    "et l'ensemble de notre personnel administratif sont pleinement impliques pour faire de la "
    "Faculte un pole de savoir rayonnant, au service du developpement durable de notre societe. "
    "Ensemble, construisons une FSBM plus forte, plus innovante et plus ouverte sur l'avenir."
)

# Actualites REELLES (page Actualites et Annonces de fsbm.ma, 2025) - 7 items
NEWS = [
    ("Inscription au Cycle de Doctorat 2025-2026", "RECHERCHE", "2025-07-23",
     "La Faculte des Sciences Ben M'Sick - Universite Hassan II de Casablanca informe l'ensemble des "
     "doctorants et des nouveaux candidats au doctorat du lancement du calendrier universitaire "
     "officiel pour l'annee academique 2025-2026."),
    ("Candidats convoques aux epreuves ecrites - Technologies de l'information", "RECHERCHE", "2025-07-02",
     "Liste des candidats convoques pour passer les epreuves ecrites en technologies de "
     "l'information, prevues le 06 juillet 2025."),
    ("Avis d'ouverture de candidature au poste de Chef de service", "SERVICES", "2025-07-02",
     "Avis d'ouverture de candidature au poste de Chef de service vacant a la Faculte des Sciences "
     "Ben M'Sick."),
    ("Resultat du Conseil de Discipline", "CAMPUS", "2025-06-18",
     "Le Conseil de Discipline, reuni le 15 juin 2025, a statue sur plusieurs cas d'infractions au "
     "reglement interieur."),
    ("Examens de la session 1 du printemps - S6 Licence d'Excellence", "RECHERCHE", "2025-06-04",
     "Publication de la liste des examens de la session 1 du printemps pour le semestre 6 de la "
     "Licence d'Excellence."),
    ("La FSBM renforce sa cybersecurite avec un nouveau partenaire strategique", "PARTENARIAT", "2025-05-23",
     "A l'occasion du salon des nouvelles technologies, la FSBM a conclu un partenariat important "
     "avec un acteur majeur du domaine de la cybersecurite."),
    ("Calendrier universitaire officiel 2025-2026", "CAMPUS", "2025-07-23",
     "Publication du calendrier universitaire officiel de la Faculte des Sciences Ben M'Sick pour "
     "l'annee academique 2025-2026."),
    ("Listes des etudiants inscrits 2025-2026", "CAMPUS", "2025-02-14",
     "Les listes des etudiants inscrits par groupe et par section pour les semestres 2, 4 et 6 sont "
     "publiees pour les filieres IA, MI, PC et BG au titre de l'annee universitaire 2025-2026."),
    ("Listes des inscrits - Session d'automne 2025-2026", "CAMPUS", "2025-10-10",
     "Mise a jour des listes des inscrits pour la session d'automne de l'annee universitaire "
     "2025-2026 (mise a jour du 10-11-2025)."),
]

# Corps professoral REEL (noms releves sur fsbm.ma/faculty, pages 1 a 13, dedupliques)
PROFS_REELS = [
    ("AADJOUR Lalla Malika","MCH"),("RAJI Halima","MC"),("HANOUNE Mostafa","Chef d'equipe"),
    ("TAKI Hassan","-"),("ZAHOUR Ghalem","PES"),("MOUNA Latifa Bouamrani","PES, Directeur de labo"),
    ("ALIKOUSS Saida","PES, Coordinatrice de Master"),("EL KOUALI Mhammed","Chef de dept Chimie"),
    ("ACHIK Imad","MCH, Coordinateur de filiere"),("CHAFIQ Nadia","Chef de dept SCH"),
    ("BAROUDI Zouhir","-"),("SAMIR Mohamed","-"),("EL HILALI Mohamed","-"),("SADIK Chaouki","MCH"),
    ("EL BERRAI Imane","MCH, Chef d'equipe"),("GHAFIRI Abdessamad","-"),("RADALLAH Driss","-"),
    ("ADLOUNI Hassani Ahmed","-"),("SALIH-ALJ Hanane","-"),("BELOUAFA Soumia","-"),("NORDINE Aicha","-"),
    ("ABOURRICHE Abdelmjid","-"),("BOURJA Lamia","-"),("YOUSFI Samia","-"),("BENNANI Laila","-"),
    ("MOUMOU Mohamed","-"),("RADID Mohamed","-"),("BORIKY Driss","-"),("MOUNIR Bahija","-"),
    ("AMEGRISSI Fatiha","-"),("MOULINE Jamal","-"),("BENNISS Mohamed","-"),("BOUMANCHAR Imane","-"),
    ("BAKKALI Said","-"),("MEHDAOUI Boubker","-"),("ABBOUD Youness","-"),("HSSAIDA Touria","-"),
    ("EZZINE Mohammed","-"),("LAASRI Laila","-"),("RACHDI Bouchra","-"),("KENZ Abdelkebir","-"),
    ("ELAOUOUAD Hanan","-"),("FOUGRACH Hassan","-"),("BADRI Wadi","-"),("SAMIR Karima","-"),
    ("ZERDANI Ilham","-"),("BELGHITI Ayoub","-"),("MOUSLIM Assia","-"),("MOUSLIM Jamal","-"),
    ("MENGGAD Mohammed","-"),("TABITE Rabab","-"),("EL KHASMI Mohammed","-"),("EL HAMOUMI R'himou","-"),
    ("ROHI Latifa","-"),("AIT HAMOU Sanaa","-"),("IOUNES Nadia","-"),("SAEL Nawal","-"),
    ("ZAOUCH Amal","-"),("BENABBOU Faouzia","-"),("EL AMRANI Souad","PES"),("BELAAOUAD Said","PES"),
    ("ABOUSSOROR Abdelmalek","-"),("EL AZZABY Fouzia","-"),("AIT ABDELOUAHID Rachida","-"),
    ("ACHTAICH Naceur","-"),("ABDERRAFI Kamal","-"),("ADHIRI R'hma","-"),("LAHLOU Souad","-"),
    ("LACHHAB Touria","-"),("EL AARABI Laila","-"),("MOUAKKIR Laila","-"),("BOUBEKRI Abderrazak","-"),
    ("AKOUIBAA Abdelilah","-"),("ERRIFAIY Meriem","-"),("NASSIF Rachid","-"),("OUMAM Mina","-"),
    ("GMOUH Said","-"),("HAJJI Latifa","-"),("SLASSI Siham","-"),("BENLATTAR Mourad","-"),
    ("AHARRANE Nabil","-"),("CHAHID Mustapha","-"),("MOULTIF Rachida","-"),("OUASKIT Said","-"),
    ("EL HAITAMY Ouafae","-"),("DEZARI Aouatif","-"),("EL HAFIDI Moulay Youssef","-"),
    ("SAKHI Zoubida","-"),("BENNAI Mohamed","-"),("KARTOUNI Abdelkrim","-"),("EL OUARDI Brahim","-"),
    ("KHOUAJA Abdenbi","-"),("MORSAD Abdeltif","-"),("BENZOUINE Fatna","-"),("IDIRI Mohamed","-"),
    ("HAMDAOUI Abdellah","-"),("DAOUDI Othmane","-"),("EDDAOUI Ahmed","-"),("ADNAOUI Khalid","MCH, Chef de dept Math-Info"),
    ("BOUGGAR Driss","MC"),("ETTAOUFIK Abdelaziz","PES"),("MOURABIT M Barka","MCH, Coordinateur de filiere"),
    ("LAARABI Hassan","MCH"),("BASSOU Abdelhafid","-"),("EL OUARRACHI Mounir","-"),
    ("MAIMOUNI Soufiane","MCH, Coordinateur de filiere"),("ECH CHERIF EL KETTANI Mohammed Anass","-"),
    ("LABZAI Mohamed","-"),("EL MOUTAKI Saida","-"),("OUAHABI Sara","MCH, Coordinatrice de filiere"),
    ("AHARMIM Bouchra","-"),("BERGHOUT Mohammed","MCH"),("BENKADDOUR Said","-"),("BENNANI Samia","-"),
    ("LAHMIDI Fouad","-"),("ATOUF Issam","-"),("BELANGOUR Abdessamad","-"),("YALID Amal","-"),
    ("EL BOUHMADI Keltoum","-"),("AZOUAZI Mohammed","-"),("MARZAK Abdelaziz","-"),("BAZI Fathallaah","-"),
    ("AIT DAOUD Mohammed","MCH, Chef d'equipe"),("BACHRAOUI Moussa","MC"),("LOTFI EL Mehdi","MCH"),
    ("AGMOUR Imane","-"),("BOUKHOUIMA Adnane","-"),("BOUYAGHROUMNI Jamal","-"),("EL HAFFARI Mostafa","-"),
    ("AIT HSSI Abderrahim","MC"),("SAID Taoufik","MCH"),("BIDAH Sara","-"),("FERJOUCHA Hanane","-"),
    ("SAADI Smahane","-"),("RAHIM Souad","-"),("MOHTADI Karima","-"),("KEHAILOU Fatima Zahra","-"),
    ("LEBRAZI Halima","-"),("SAILE Rachid","-"),("EL OUAHABI Imane","-"),("SERGHAT Samira","-"),
    ("BOUZOUBAA Hind","-"),("BENNANI Houda","-"),("HASSEN Haoudya","-"),("SLIMANI Abdellatif","MC"),
    ("KANDALI Khalid","-"),("SEFRI Youssef","-"),("CHAFIQ Tarik","-"),("ALALI Abdelghani","-"),
    ("MAZROUI M'hammed","Chef de dept Physiques"),
]
