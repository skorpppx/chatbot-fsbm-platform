-- =============================================================================
--  FSBM Platform — Modules (matières) par filière
--  À exécuter APRÈS 02_seed_static.sql
-- =============================================================================

USE fsbm_db;

-- =============================================================================
--  Modules SMI (Sciences Mathématiques et Informatique) — Licence 3 ans = 6 semestres
-- =============================================================================
INSERT INTO modules (code, name, filiere_id, semester, credits, coefficient, hours_cours, hours_td, hours_tp, description) VALUES
-- Semestre 1
('SMI-S1-M1', 'Analyse I',                                      1, 1, 6, 1.5, 36, 24, 0,  'Suites, séries, fonctions d''une variable réelle.'),
('SMI-S1-M2', 'Algèbre I',                                       1, 1, 6, 1.5, 36, 24, 0,  'Logique, ensembles, structures algébriques.'),
('SMI-S1-M3', 'Programmation I (Algorithmique)',                 1, 1, 6, 1.5, 24, 18, 24, 'Algorithmique, structures de contrôle, premiers programmes en C.'),
('SMI-S1-M4', 'Physique I (Mécanique)',                          1, 1, 4, 1.0, 24, 18, 12, 'Cinématique, dynamique, énergétique.'),
('SMI-S1-M5', 'Langue et Communication I',                       1, 1, 2, 0.5, 24, 0,  0,  'Français technique, anglais.'),
-- Semestre 2
('SMI-S2-M1', 'Analyse II',                                      1, 2, 6, 1.5, 36, 24, 0,  'Intégration, équations différentielles, séries de Fourier.'),
('SMI-S2-M2', 'Algèbre II',                                      1, 2, 6, 1.5, 36, 24, 0,  'Espaces vectoriels, applications linéaires, matrices.'),
('SMI-S2-M3', 'Programmation II (POO en Java)',                  1, 2, 6, 1.5, 24, 18, 24, 'Programmation orientée objet, design patterns.'),
('SMI-S2-M4', 'Physique II (Électricité)',                       1, 2, 4, 1.0, 24, 18, 12, 'Électrostatique, électrocinétique, électromagnétisme.'),
('SMI-S2-M5', 'Langue et Communication II',                      1, 2, 2, 0.5, 24, 0,  0,  'Anglais scientifique, expression écrite.'),
-- Semestre 3
('SMI-S3-M1', 'Probabilités et Statistiques',                    1, 3, 6, 1.5, 36, 24, 0,  'Probabilités élémentaires, variables aléatoires, tests statistiques.'),
('SMI-S3-M2', 'Structures de Données et Algorithmes',            1, 3, 6, 1.5, 24, 18, 24, 'Listes, arbres, graphes, complexité, algorithmes de tri.'),
('SMI-S3-M3', 'Bases de Données',                                1, 3, 6, 1.5, 24, 18, 24, 'Modèle relationnel, SQL, normalisation, MySQL.'),
('SMI-S3-M4', 'Systèmes d''Exploitation',                        1, 3, 4, 1.0, 24, 18, 12, 'Processus, mémoire, fichiers, Linux/Unix.'),
('SMI-S3-M5', 'Analyse Numérique',                               1, 3, 4, 1.0, 24, 18, 12, 'Méthodes numériques, interpolation, résolution d''équations.'),
-- Semestre 4
('SMI-S4-M1', 'Théorie des Graphes',                             1, 4, 6, 1.5, 36, 24, 0,  'Graphes, parcours, plus court chemin, flots.'),
('SMI-S4-M2', 'Programmation Web (HTML/CSS/JS)',                 1, 4, 6, 1.5, 24, 18, 24, 'Front-end moderne, JavaScript ES6+, frameworks.'),
('SMI-S4-M3', 'Réseaux Informatiques',                           1, 4, 6, 1.5, 24, 18, 24, 'Modèle OSI, TCP/IP, sécurité réseaux.'),
('SMI-S4-M4', 'Compilation',                                     1, 4, 4, 1.0, 24, 18, 12, 'Analyse lexicale, syntaxique, sémantique, génération de code.'),
('SMI-S4-M5', 'Mathématiques Discrètes',                         1, 4, 4, 1.0, 24, 18, 0,  'Combinatoire, théorie des nombres, structures discrètes.'),
-- Semestre 5
('SMI-S5-M1', 'Intelligence Artificielle',                       1, 5, 6, 1.5, 24, 18, 24, 'IA symbolique, recherche, agents, introduction au ML.'),
('SMI-S5-M2', 'Génie Logiciel et UML',                           1, 5, 6, 1.5, 24, 18, 24, 'Cycle de vie, UML, patterns, méthodologies agiles.'),
('SMI-S5-M3', 'Programmation Mobile (Android)',                  1, 5, 6, 1.5, 24, 18, 24, 'Kotlin, Android SDK, architecture MVVM.'),
('SMI-S5-M4', 'Sécurité Informatique',                           1, 5, 4, 1.0, 24, 18, 12, 'Cryptographie, attaques web, sécurité applicative.'),
('SMI-S5-M5', 'Modélisation et Simulation',                      1, 5, 4, 1.0, 24, 18, 12, 'Simulation Monte Carlo, files d''attente, modèles stochastiques.'),
-- Semestre 6
('SMI-S6-M1', 'Big Data et Cloud',                               1, 6, 6, 1.5, 24, 18, 24, 'Hadoop, Spark, AWS/Azure, conteneurisation.'),
('SMI-S6-M2', 'Machine Learning',                                1, 6, 6, 1.5, 24, 18, 24, 'Apprentissage supervisé/non supervisé, deep learning.'),
('SMI-S6-M3', 'Projet de Fin d''Études (PFE)',                   1, 6, 12, 3.0, 0,  0,  0,  'Stage en entreprise + mémoire + soutenance.'),
('SMI-S6-M4', 'Anglais Professionnel',                           1, 6, 2, 0.5, 24, 0,  0,  'Communication professionnelle, présentations, CV.'),
('SMI-S6-M5', 'Management de Projet',                            1, 6, 4, 1.0, 24, 0,  0,  'Conduite de projet, agile, scrum, kanban.');

-- =============================================================================
--  Modules DI (Développement Informatique) — 6 semestres
-- =============================================================================
INSERT INTO modules (code, name, filiere_id, semester, credits, coefficient, hours_cours, hours_td, hours_tp, description) VALUES
('DI-S1-M1', 'Introduction à la Programmation (C)',             2, 1, 6, 1.5, 24, 18, 30, 'Bases de la programmation impérative en C.'),
('DI-S1-M2', 'Mathématiques pour l''Informatique',              2, 1, 4, 1.0, 30, 24, 0,  'Logique, ensembles, fonctions, suites.'),
('DI-S1-M3', 'Algorithmique',                                    2, 1, 6, 1.5, 24, 24, 24, 'Conception et analyse d''algorithmes.'),
('DI-S1-M4', 'Architecture des Ordinateurs',                     2, 1, 4, 1.0, 24, 18, 12, 'CPU, mémoire, ALU, jeu d''instructions.'),
('DI-S1-M5', 'Anglais Technique I',                              2, 1, 2, 0.5, 24, 0,  0,  'Vocabulaire IT, lecture de documentation.'),
-- S2
('DI-S2-M1', 'POO en Java',                                      2, 2, 6, 1.5, 24, 24, 24, 'Héritage, polymorphisme, interfaces, JavaFX.'),
('DI-S2-M2', 'Structures de Données',                            2, 2, 6, 1.5, 24, 24, 24, 'Listes, piles, files, arbres, tables de hachage.'),
('DI-S2-M3', 'Bases de Données Relationnelles',                  2, 2, 6, 1.5, 24, 24, 24, 'Modèle E/A, SQL avancé, transactions, MySQL.'),
('DI-S2-M4', 'Systèmes d''Exploitation',                         2, 2, 4, 1.0, 24, 18, 12, 'Linux, scripts shell, processus.'),
('DI-S2-M5', 'Anglais Technique II',                             2, 2, 2, 0.5, 24, 0,  0,  'Présentations techniques, écriture de docs.'),
-- S3
('DI-S3-M1', 'Programmation Web Front-End',                      2, 3, 6, 1.5, 18, 18, 36, 'HTML5, CSS3, JavaScript ES6+, Bootstrap, responsive design.'),
('DI-S3-M2', 'Programmation Web Back-End',                       2, 3, 6, 1.5, 18, 18, 36, 'PHP/Laravel ou Node.js/Express, APIs REST.'),
('DI-S3-M3', 'Bases de Données Avancées',                        2, 3, 6, 1.5, 24, 18, 24, 'PL/SQL, procédures, triggers, NoSQL (MongoDB).'),
('DI-S3-M4', 'Génie Logiciel et UML',                            2, 3, 4, 1.0, 24, 18, 12, 'Cycle de vie, UML, design patterns, refactoring.'),
('DI-S3-M5', 'Mathématiques Appliquées',                         2, 3, 4, 1.0, 24, 18, 0,  'Statistiques descriptives, probabilités élémentaires.'),
-- S4
('DI-S4-M1', 'Framework Front-End (React/Angular)',              2, 4, 6, 1.5, 18, 18, 36, 'Angular 17 ou React 18, state management, routing.'),
('DI-S4-M2', 'Framework Back-End (Spring/Django)',               2, 4, 6, 1.5, 18, 18, 36, 'Java Spring Boot OU Python Django/FastAPI.'),
('DI-S4-M3', 'Réseaux et Sécurité Web',                          2, 4, 6, 1.5, 24, 18, 24, 'HTTPS, OAuth, JWT, OWASP Top 10.'),
('DI-S4-M4', 'Tests Logiciels et Qualité',                       2, 4, 4, 1.0, 18, 12, 24, 'Tests unitaires, intégration, e2e, CI/CD.'),
('DI-S4-M5', 'Projet Tutoré',                                    2, 4, 4, 1.0, 0,  0,  60, 'Mini-projet en équipe sur 6 semaines.'),
-- S5
('DI-S5-M1', 'Programmation Mobile (Android/iOS)',               2, 5, 6, 1.5, 18, 18, 36, 'Kotlin Android + Swift iOS OU Flutter cross-platform.'),
('DI-S5-M2', 'DevOps et Cloud',                                  2, 5, 6, 1.5, 18, 18, 36, 'Git, Docker, CI/CD, AWS/Azure/GCP, Kubernetes.'),
('DI-S5-M3', 'Microservices et Architectures Modernes',          2, 5, 6, 1.5, 24, 18, 24, 'Microservices, API Gateway, message brokers.'),
('DI-S5-M4', 'Sécurité Applicative',                             2, 5, 4, 1.0, 24, 18, 12, 'Cryptographie pratique, sécurité OWASP, pentest.'),
('DI-S5-M5', 'Soft Skills et Entrepreneuriat',                   2, 5, 4, 1.0, 24, 0,  0,  'Communication, leadership, business model canvas.'),
-- S6
('DI-S6-M1', 'Stage PFE en Entreprise',                          2, 6, 18, 4.0, 0, 0, 0, 'Stage de 4 mois minimum + mémoire + soutenance.'),
('DI-S6-M2', 'Veille Technologique',                             2, 6, 4, 1.0, 0, 0, 24, 'Suivi de l''actualité tech, rédaction d''articles.'),
('DI-S6-M3', 'Préparation Insertion Professionnelle',            2, 6, 4, 1.0, 18, 0, 12, 'CV, lettre de motivation, simulations d''entretien.'),
('DI-S6-M4', 'Anglais Professionnel Avancé',                     2, 6, 4, 1.0, 24, 0, 0,  'TOEIC preparation, négociation, présentations.');

-- =============================================================================
--  Modules d'autres filières (résumés)
-- =============================================================================
INSERT INTO modules (code, name, filiere_id, semester, credits, coefficient, hours_cours, hours_td, hours_tp, description) VALUES
-- SMA quelques modules clés
('SMA-S1-M1', 'Analyse I',                                       3, 1, 6, 1.5, 36, 24, 0, 'Suites et fonctions.'),
('SMA-S1-M2', 'Algèbre Linéaire',                                3, 1, 6, 1.5, 36, 24, 0, 'Espaces vectoriels et applications linéaires.'),
('SMA-S5-M1', 'Topologie',                                       3, 5, 6, 1.5, 36, 24, 0, 'Topologie générale.'),
('SMA-S6-M1', 'Probabilités Avancées',                           3, 6, 6, 1.5, 36, 24, 0, 'Théorie de la mesure et probabilités.'),
-- SMP quelques modules clés
('SMP-S1-M1', 'Mécanique du Point',                              4, 1, 6, 1.5, 30, 24, 12, 'Cinématique et dynamique.'),
('SMP-S2-M1', 'Électromagnétisme',                               4, 2, 6, 1.5, 30, 24, 12, 'Champs électriques et magnétiques.'),
('SMP-S5-M1', 'Mécanique Quantique',                             4, 5, 6, 1.5, 36, 24, 0, 'Postulats, équation de Schrödinger.'),
('SMP-S6-M1', 'Physique des Matériaux',                          4, 6, 6, 1.5, 30, 18, 24, 'Solides, semi-conducteurs, supraconductivité.'),
-- SMC quelques modules clés
('SMC-S1-M1', 'Chimie Générale',                                 5, 1, 6, 1.5, 30, 18, 24, 'Atome, liaisons, thermodynamique chimique.'),
('SMC-S2-M1', 'Chimie Organique I',                              5, 2, 6, 1.5, 30, 18, 24, 'Fonctions, réactions, mécanismes.'),
('SMC-S5-M1', 'Chimie Analytique',                               5, 5, 6, 1.5, 24, 18, 30, 'Techniques d''analyse instrumentale.'),
-- SV quelques modules clés
('SV-S1-M1',  'Biologie Cellulaire',                             6, 1, 6, 1.5, 30, 18, 24, 'Structure et fonctions de la cellule.'),
('SV-S2-M1',  'Génétique',                                       6, 2, 6, 1.5, 30, 24, 12, 'Génétique mendélienne et moléculaire.'),
('SV-S5-M1',  'Biologie Moléculaire',                            6, 5, 6, 1.5, 24, 18, 24, 'ADN, ARN, expression génique.'),
('SV-S6-M1',  'Microbiologie',                                   6, 6, 6, 1.5, 24, 18, 24, 'Bactéries, virus, champignons.'),
-- STU quelques modules clés
('STU-S1-M1', 'Géologie Générale',                               7, 1, 6, 1.5, 30, 18, 24, 'Roches, minéraux, tectonique.'),
('STU-S2-M1', 'Cartographie et SIG',                             7, 2, 6, 1.5, 24, 18, 30, 'Cartes géologiques, SIG.'),
('STU-S5-M1', 'Hydrogéologie',                                   7, 5, 6, 1.5, 30, 18, 24, 'Eaux souterraines, ressources.'),
('STU-S6-M1', 'Sédimentologie',                                  7, 6, 6, 1.5, 30, 18, 24, 'Sédiments et bassins sédimentaires.');

-- =============================================================================
--  Modules Master IADS (Intelligence Artificielle et Data Science) - 4 semestres
-- =============================================================================
INSERT INTO modules (code, name, filiere_id, semester, credits, coefficient, hours_cours, hours_td, hours_tp, description) VALUES
('IADS-S1-M1', 'Mathématiques pour l''IA',                       10, 1, 6, 1.5, 30, 30, 0,  'Algèbre linéaire avancée, optimisation, théorie de l''information.'),
('IADS-S1-M2', 'Machine Learning Fondamental',                   10, 1, 6, 1.5, 30, 18, 24, 'SVM, arbres de décision, ensembles, scikit-learn.'),
('IADS-S1-M3', 'Bases de Données pour Big Data',                 10, 1, 6, 1.5, 24, 18, 24, 'NoSQL, MongoDB, Cassandra, Elasticsearch.'),
('IADS-S1-M4', 'Python Avancé pour la Data Science',             10, 1, 6, 1.5, 18, 18, 36, 'NumPy, Pandas, Matplotlib, environnements virtuels.'),
('IADS-S2-M1', 'Deep Learning',                                  10, 2, 6, 1.5, 24, 18, 30, 'Réseaux neuronaux, CNN, RNN, TensorFlow/PyTorch.'),
('IADS-S2-M2', 'NLP et Traitement du Langage Naturel',           10, 2, 6, 1.5, 24, 18, 30, 'Word embeddings, transformers, BERT, GPT.'),
('IADS-S2-M3', 'Big Data Engineering',                           10, 2, 6, 1.5, 18, 18, 36, 'Hadoop, Spark, Kafka, streaming.'),
('IADS-S2-M4', 'Éthique et IA Responsable',                      10, 2, 4, 1.0, 24, 12, 0,  'Biais algorithmiques, fairness, RGPD, AI Act.'),
('IADS-S3-M1', 'Vision par Ordinateur',                          10, 3, 6, 1.5, 24, 18, 30, 'OpenCV, segmentation, détection, GANs.'),
('IADS-S3-M2', 'MLOps et Déploiement IA',                        10, 3, 6, 1.5, 18, 18, 36, 'CI/CD pour ML, monitoring, model serving.'),
('IADS-S3-M3', 'Reinforcement Learning',                         10, 3, 6, 1.5, 24, 18, 24, 'MDPs, Q-Learning, Deep RL.'),
('IADS-S3-M4', 'Projet IA Entreprise',                           10, 3, 6, 1.5, 0,  0, 60,  'Projet d''application en partenariat industriel.'),
('IADS-S4-M1', 'Stage de Recherche / Industriel',                10, 4, 24, 6.0, 0, 0, 0,   'Stage de 5 à 6 mois avec soutenance.');
