-- =============================================================================
--  FSBM Platform — Données statiques (référentiel)
--  À exécuter APRÈS 01_schema.sql et AVANT le générateur Python
-- =============================================================================

USE fsbm_db;

-- =============================================================================
--  DÉPARTEMENTS (5 départements officiels de la FSBM)
-- =============================================================================
INSERT INTO departments (code, name, name_short, description, head_name, head_email, head_phone, office_location, color_hex, logo_url) VALUES
('MI',    'Département de Mathématiques et Informatique', 'Math-Info',
 'Le département de Mathématiques et Informatique propose des formations en SMI, SMA, Développement Informatique et plusieurs masters de pointe.',
 'Pr. Mohammed ALAOUI', 'chef.mi@fsbm.ac.ma', '+212 522 70 46 71', 'Bâtiment B - Bureau B201',
 '#16B5A6', '/assets/logos/dept-math-info.png'),

('PH',    'Département de Physique', 'Physique',
 'Formations en Sciences de la Matière Physique avec spécialisations en énergétique, matériaux et physique fondamentale.',
 'Pr. Khadija BENNANI', 'chef.physique@fsbm.ac.ma', '+212 522 70 46 72', 'Bâtiment C - Bureau C105',
 '#3A7BD5', NULL),

('CH',    'Département de Chimie', 'Chimie',
 'Sciences de la Matière Chimie avec laboratoires de chimie organique, analytique et environnementale.',
 'Pr. Youssef LAHLOU', 'chef.chimie@fsbm.ac.ma', '+212 522 70 46 73', 'Bâtiment C - Bureau C201',
 '#E94B7E', NULL),

('BIO',   'Département de Biologie', 'Biologie',
 'Sciences de la Vie, biotechnologie, biologie moléculaire et microbiologie appliquée.',
 'Pr. Fatima ZAHIDI', 'chef.bio@fsbm.ac.ma', '+212 522 70 46 74', 'Bâtiment D - Bureau D101',
 '#22C55E', NULL),

('GEO',   'Département de Géologie', 'Géologie',
 'Sciences de la Terre et de l''Univers, géosciences appliquées, hydrogéologie et environnement.',
 'Pr. Hassan BERRADA', 'chef.geo@fsbm.ac.ma', '+212 522 70 46 75', 'Bâtiment D - Bureau D205',
 '#A0522D', NULL);

-- =============================================================================
--  FILIÈRES DE LICENCE (6 fondamentales)
-- =============================================================================
INSERT INTO filieres (code, name, type, department_id, coordinator, coord_email, duration_years, capacity, description, objectives, careers, admission, is_active) VALUES
('SMI', 'Sciences Mathématiques et Informatique', 'LICENCE', 1, 'Pr. Karim TAZI', 'karim.tazi@fsbm.ac.ma', 3, 180,
 'Filière formant des informaticiens avec une solide base mathématique. Programme équilibré entre théorie informatique et mathématiques appliquées.',
 'Maîtriser les fondements théoriques de l''informatique, développer des compétences en algorithmique, programmation, bases de données et réseaux.',
 'Ingénieur logiciel, data scientist, administrateur systèmes, analyste-programmeur, intégration dans des écoles d''ingénieurs.',
 'Bac scientifique (Sciences Mathématiques A/B, Sciences Physiques) — sélection sur dossier.',
 TRUE),

('DI', 'Développement Informatique', 'LICENCE_PRO', 1, 'Pr. Soufiane MEZOUARI', 'soufiane.mezouari@fsbm.ac.ma', 3, 120,
 'Licence professionnelle orientée pratique formant des développeurs full-stack opérationnels.',
 'Maîtriser le développement web (front et back), les bases de données, le génie logiciel et la cybersécurité.',
 'Développeur web/mobile full-stack, intégrateur, devops, ingénieur logiciel junior.',
 'Bac scientifique — sélection sur dossier + entretien possible.',
 TRUE),

('SMA', 'Sciences Mathématiques et Applications', 'LICENCE', 1, 'Pr. Nadia RAHMOUNI', 'nadia.rahmouni@fsbm.ac.ma', 3, 100,
 'Mathématiques pures et appliquées avec ouverture vers la modélisation et la statistique.',
 'Acquérir une solide formation mathématique préparant aux concours d''écoles d''ingénieurs ou aux masters de mathématiques.',
 'Actuaire, statisticien, analyste quantitatif, enseignant-chercheur, master de mathématiques appliquées.',
 'Bac Sciences Mathématiques de préférence.',
 TRUE),

('SMP', 'Sciences de la Matière Physique', 'LICENCE', 2, 'Pr. Omar IDRISSI', 'omar.idrissi@fsbm.ac.ma', 3, 120,
 'Formation en physique fondamentale et appliquée, énergétique et matériaux.',
 'Maîtriser les concepts fondamentaux de la physique (mécanique, thermo, optique, quantique) et leurs applications.',
 'Ingénieur en énergétique, matériaux, recherche, enseignement, masters spécialisés.',
 'Bac scientifique avec bonne moyenne en physique.',
 TRUE),

('SMC', 'Sciences de la Matière Chimie', 'LICENCE', 3, 'Pr. Asmae BENALI', 'asmae.benali@fsbm.ac.ma', 3, 110,
 'Chimie générale, organique, inorganique et analytique avec orientation industrie pharmaceutique et environnement.',
 'Comprendre les phénomènes chimiques, maîtriser les techniques d''analyse et de synthèse.',
 'Chimiste analyste, contrôle qualité, industrie pharmaceutique, environnement, enseignement.',
 'Bac scientifique.',
 TRUE),

('SV', 'Sciences de la Vie', 'LICENCE', 4, 'Pr. Hicham OUAZZANI', 'hicham.ouazzani@fsbm.ac.ma', 3, 150,
 'Biologie animale, végétale, moléculaire, génétique, écologie et biotechnologie.',
 'Comprendre les mécanismes du vivant à différentes échelles, de la molécule à l''écosystème.',
 'Biotechnologie, agroalimentaire, recherche médicale, environnement, enseignement.',
 'Bac scientifique SVT de préférence.',
 TRUE),

('STU', 'Sciences de la Terre et de l''Univers', 'LICENCE', 5, 'Pr. Latifa BENJELLOUN', 'latifa.benjelloun@fsbm.ac.ma', 3, 80,
 'Géologie, minéralogie, paléontologie, géophysique et environnement.',
 'Étudier la structure, la composition et l''évolution de la Terre et de son environnement.',
 'Géologue minier/pétrolier, hydrogéologue, géotechnicien, environnement, recherche.',
 'Bac scientifique.',
 TRUE);

-- =============================================================================
--  MASTERS (18 masters de la FSBM)
-- =============================================================================
INSERT INTO filieres (code, name, type, department_id, coordinator, coord_email, duration_years, capacity, description, careers, admission, is_active) VALUES
('MIAGE',   'Master Informatique et Gestion d''Entreprise', 'MASTER', 1, 'Pr. Rachid BENHAMOU', 'r.benhamou@fsbm.ac.ma', 2, 30,
 'Double compétence informatique et management : conduite de projets SI, BI, ERP.',
 'Chef de projet SI, consultant ERP, business analyst, manager IT.',
 'Licence en informatique ou management — étude de dossier + entretien.', TRUE),

('IDSI',    'Master Ingénierie Décisionnelle et Systèmes d''Information', 'MASTER', 1, 'Pr. Salma EL FATIMI', 's.elfatimi@fsbm.ac.ma', 2, 28,
 'Big Data, data warehousing, OLAP, machine learning appliqué.',
 'Data engineer, BI consultant, architecte SI décisionnel.',
 'Licence informatique — concours écrit + entretien.', TRUE),

('IADS',    'Master Intelligence Artificielle et Data Science', 'MASTER', 1, 'Pr. Mehdi FILALI', 'm.filali@fsbm.ac.ma', 2, 25,
 'Machine learning, deep learning, NLP, vision par ordinateur, MLOps.',
 'Data scientist, ingénieur ML, chercheur IA, consultant IA.',
 'Licence informatique ou mathématiques avec forte composante info — sélection compétitive.', TRUE),

('SECNUM',  'Master Sécurité Numérique et Cryptographie', 'MASTER', 1, 'Pr. Hamid MOUSSA', 'h.moussa@fsbm.ac.ma', 2, 25,
 'Cybersécurité, cryptographie moderne, sécurité réseaux et applications.',
 'Pentester, RSSI, analyste SOC, cryptologue, consultant cybersécurité.',
 'Licence informatique — étude de dossier rigoureuse.', TRUE),

('MMA',     'Master Mathématiques Appliquées', 'MASTER', 1, 'Pr. Sara NACIRI', 's.naciri@fsbm.ac.ma', 2, 25,
 'Modélisation, statistique avancée, EDP, optimisation, finance quantitative.',
 'Actuaire, ingénieur recherche, doctorat, enseignant-chercheur.',
 'Licence SMA ou équivalent.', TRUE),

('MR-MATHS','Master Recherche en Mathématiques', 'MASTER_RECHERCHE', 1, 'Pr. Aziz CHAFI', 'a.chafi@fsbm.ac.ma', 2, 15,
 'Algèbre, analyse, géométrie, topologie — orientation thèse de doctorat.',
 'Doctorat, enseignement supérieur, recherche fondamentale.',
 'Licence SMA avec excellent dossier.', TRUE),

('MRP',     'Master Physique des Rayonnements et Imagerie Médicale', 'MASTER', 2, 'Pr. Najat KHALIDI', 'n.khalidi@fsbm.ac.ma', 2, 20,
 'Imagerie médicale, dosimétrie, radioprotection.',
 'Physicien médical hospitalier, ingénieur en imagerie, recherche.',
 'Licence SMP — entretien.', TRUE),

('MENRG',   'Master Énergies Renouvelables et Environnement', 'MASTER', 2, 'Pr. Tarik EL AMRANI', 't.elamrani@fsbm.ac.ma', 2, 25,
 'Solaire, éolien, biomasse, efficacité énergétique, smart grids.',
 'Ingénieur ENR, consultant énergie, bureaux d''études, audits énergétiques.',
 'Licence SMP/SMC ou équivalent.', TRUE),

('MMAT',    'Master Matériaux et Nanotechnologies', 'MASTER', 2, 'Pr. Rabia EL FATIMI', 'r.elfatimi@fsbm.ac.ma', 2, 20,
 'Science des matériaux, nanotechnologies, caractérisation.',
 'R&D matériaux, industrie, recherche académique.',
 'Licence SMP/SMC.', TRUE),

('MCAE',    'Master Chimie Analytique et Environnementale', 'MASTER', 3, 'Pr. Brahim TAJEDDINE', 'b.tajeddine@fsbm.ac.ma', 2, 25,
 'Analyse instrumentale, chimie de l''environnement, traitement des eaux.',
 'Laboratoires d''analyse, environnement, agroalimentaire, contrôle qualité.',
 'Licence SMC ou équivalent.', TRUE),

('MCOI',    'Master Chimie Organique Industrielle', 'MASTER', 3, 'Pr. Wafae LARAKI', 'w.laraki@fsbm.ac.ma', 2, 22,
 'Synthèse organique, chimie médicinale, procédés industriels.',
 'Industrie pharmaceutique, cosmétique, R&D chimique.',
 'Licence SMC.', TRUE),

('MBIOT',   'Master Biotechnologie et Valorisation des Plantes', 'MASTER', 4, 'Pr. Saadia OUARGAGA', 's.ouargaga@fsbm.ac.ma', 2, 25,
 'Culture in vitro, génie génétique, valorisation de la biodiversité.',
 'Biotech, agroalimentaire, cosmétiques naturels, recherche.',
 'Licence SV.', TRUE),

('MMOLEC',  'Master Biologie Moléculaire et Cellulaire', 'MASTER', 4, 'Pr. Imane SEFRIOUI', 'i.sefrioui@fsbm.ac.ma', 2, 22,
 'Biologie moléculaire, génétique, immunologie, cancérologie.',
 'Recherche biomédicale, doctorat, industrie pharmaceutique.',
 'Licence SV avec excellent dossier.', TRUE),

('MMICRO',  'Master Microbiologie Appliquée', 'MASTER', 4, 'Pr. Bouchra ZAID', 'b.zaid@fsbm.ac.ma', 2, 20,
 'Microbiologie industrielle, alimentaire, environnementale.',
 'Industrie alimentaire, environnement, recherche, contrôle qualité.',
 'Licence SV.', TRUE),

('MENV',    'Master Géosciences et Environnement', 'MASTER', 5, 'Pr. Driss BENALI', 'd.benali@fsbm.ac.ma', 2, 20,
 'Géologie environnementale, ressources en eau, risques naturels.',
 'Hydrogéologue, environnement, géotechnique, mines.',
 'Licence STU.', TRUE),

('MGAP',    'Master Géologie Appliquée et Patrimoine', 'MASTER', 5, 'Pr. Younes EL HAJJI', 'y.elhajji@fsbm.ac.ma', 2, 18,
 'Géologie minière, pétrolière, patrimoine géologique.',
 'Mines, pétrole, bureaux d''études géologiques.',
 'Licence STU.', TRUE),

('MEDU-MI', 'Master Didactique des Mathématiques et de l''Informatique', 'MASTER', 1, 'Pr. Habiba CHERKAOUI', 'h.cherkaoui@fsbm.ac.ma', 2, 30,
 'Didactique, pédagogie, technologie éducative pour l''enseignement secondaire.',
 'Enseignant qualifié du secondaire, formateur, conseiller pédagogique.',
 'Licence + concours d''entrée.', TRUE),

('MEDU-SV', 'Master Didactique des Sciences de la Vie', 'MASTER', 4, 'Pr. Khalid BOULAHIA', 'k.boulahia@fsbm.ac.ma', 2, 25,
 'Didactique SVT, conception pédagogique, formation enseignants.',
 'Enseignant SVT, formateur, inspecteur pédagogique.',
 'Licence SV + concours.', TRUE);

-- =============================================================================
--  CATÉGORIES FAQ
-- =============================================================================
INSERT INTO faq_categories (code, name, description, icon, color_hex, display_order) VALUES
('general',         'Général',                    'Salutations, présentation du chatbot',                '👋', '#7E8FA4', 1),
('inscription',     'Inscription',                'Inscription en licence et master',                    '📋', '#3A7BD5', 2),
('reinscription',   'Réinscription',              'Réinscription en année supérieure',                   '🔁', '#3A7BD5', 3),
('filieres',        'Filières',                   'Toutes les filières et formations',                   '📚', '#16B5A6', 4),
('masters',         'Masters',                    'Les 18 masters de la FSBM',                           '🎓', '#9333EA', 5),
('doctorat',        'Doctorat',                   'Centre d''études doctorales',                         '🔬', '#9333EA', 6),
('emploi_temps',    'Emploi du temps',            'Horaires des cours par filière',                      '📅', '#22C55E', 7),
('examens',         'Examens & Résultats',        'Calendrier, modalités, résultats',                    '📝', '#F59E0B', 8),
('attestations',    'Attestations & Diplômes',    'Documents officiels, retrait diplôme',                '📄', '#EAB308', 9),
('stages',          'Stages & PFE',               'Conventions, soutenances',                            '💼', '#EC4899', 10),
('bourses',         'Bourses & Aides',            'ONOUSC, bourses mérite, aides financières',           '💰', '#10B981', 11),
('vie_etudiante',   'Vie étudiante',              'Clubs, sport, événements, restauration, hébergement', '🌟', '#F97316', 12),
('services',        'Services',                   'Bibliothèque, infirmerie, wifi, e-learning',          '🛠️', '#6366F1', 13),
('contacts',        'Contacts',                   'Scolarité, départements, localisation',               '📞', '#0EA5E9', 14),
('reglement',       'Règlement',                  'Validation, compensation, discipline',                '⚖️', '#64748B', 15),
('transferts',      'Transferts',                 'Changement de filière, équivalences',                 '🔄', '#7C3AED', 16);

-- =============================================================================
--  CLUBS ÉTUDIANTS (réalistes)
-- =============================================================================
INSERT INTO clubs (name, description, category, president, contact_email, social_links, members_count, is_active) VALUES
('Club Info FSBM', 'Club informatique organisant hackathons, ateliers programmation et conférences tech.', 'TECHNIQUE', 'Yassine BOUKHRIS', 'club.info@fsbm.ac.ma',
 JSON_OBJECT('facebook', 'https://facebook.com/clubinfofsbm', 'instagram', '@clubinfo_fsbm', 'github', 'https://github.com/clubinfofsbm'), 120, TRUE),

('Club Robotique', 'Conception et programmation de robots, participation aux compétitions nationales.', 'TECHNIQUE', 'Salma BENALI', 'club.robotique@fsbm.ac.ma',
 JSON_OBJECT('facebook', 'https://facebook.com/clubrobotiquefsbm'), 45, TRUE),

('Club Sciences', 'Vulgarisation scientifique, expériences ouvertes, journée portes ouvertes.', 'SCIENTIFIQUE', 'Mehdi LAHLOU', 'club.sciences@fsbm.ac.ma',
 JSON_OBJECT('facebook', 'https://facebook.com/clubsciencesfsbm'), 80, TRUE),

('Club Environnement', 'Sensibilisation écologique, journées de nettoyage, conférences développement durable.', 'HUMANITAIRE', 'Imane ZAHIDI', 'club.env@fsbm.ac.ma',
 JSON_OBJECT('facebook', 'https://facebook.com/clubenvfsbm', 'instagram', '@env_fsbm'), 65, TRUE),

('Club Culturel', 'Théâtre, cinéma, expositions, débats culturels.', 'CULTUREL', 'Hamza ALAOUI', 'club.culture@fsbm.ac.ma',
 JSON_OBJECT('instagram', '@culture_fsbm'), 90, TRUE),

('Club Sportif', 'Tournois inter-facultés, football, basketball, tennis de table.', 'SPORTIF', 'Anas BENNANI', 'club.sport@fsbm.ac.ma',
 JSON_OBJECT('facebook', 'https://facebook.com/clubsportfsbm'), 150, TRUE),

('Club Humanitaire FSBM', 'Actions sociales, collectes pour orphelinats, soutien scolaire dans les quartiers défavorisés.', 'HUMANITAIRE', 'Fatima ZAHRA', 'club.humanitaire@fsbm.ac.ma',
 JSON_OBJECT('instagram', '@humanitaire_fsbm'), 75, TRUE),

('Club IA & Data Science', 'Apprentissage IA, projets ML, compétitions Kaggle.', 'TECHNIQUE', 'Othmane FILALI', 'club.ia@fsbm.ac.ma',
 JSON_OBJECT('github', 'https://github.com/clubia-fsbm', 'linkedin', 'https://linkedin.com/company/clubia-fsbm'), 60, TRUE);

-- =============================================================================
--  ÉVÉNEMENTS UNIVERSITAIRES (réalistes pour 2025/2026)
-- =============================================================================
INSERT INTO events (title, description, event_type, start_date, end_date, location, organizer, registration_url) VALUES
('Journée Portes Ouvertes FSBM 2026', 'Découverte des filières, ateliers, rencontres avec les enseignants.', 'PORTES_OUVERTES',
 '2026-03-15 09:00:00', '2026-03-15 17:00:00', 'Campus FSBM - Tous bâtiments', 'Service Communication FSBM', 'https://fsbm.ma/jpo2026'),

('Hackathon FSBM 2026', 'Compétition de programmation 48h sur le thème de l''IA et la santé.', 'HACKATHON',
 '2026-04-10 18:00:00', '2026-04-12 18:00:00', 'Amphi A + Salles informatiques', 'Club Info FSBM', 'https://fsbm.ma/hackathon2026'),

('Conférence : IA Générative et Éducation', 'Intervention du Pr. Mehdi FILALI sur l''impact de l''IA générative dans l''enseignement supérieur.', 'CONFERENCE',
 '2026-02-20 14:30:00', '2026-02-20 17:00:00', 'Amphi B', 'Département Math-Info', NULL),

('Forum Emploi FSBM 2026', 'Rencontres étudiants-entreprises, présentations, stages et CDI.', 'FORUM',
 '2026-05-08 09:00:00', '2026-05-08 17:00:00', 'Hall principal FSBM', 'Service Insertion Professionnelle', 'https://fsbm.ma/forum2026'),

('Gala de fin d''année FSBM', 'Soirée festive de fin d''année universitaire avec remise de prix.', 'GALA',
 '2026-06-25 19:00:00', '2026-06-26 01:00:00', 'Hôtel Sheraton Casablanca', 'Bureau des Étudiants', NULL);

-- =============================================================================
--  ANNONCES OFFICIELLES
-- =============================================================================
INSERT INTO announcements (title, content, type, author, is_pinned, published_at) VALUES
('Calendrier des examens — Session normale Juin 2026',
 'La session normale des examens du semestre de printemps se déroulera du 1er au 25 juin 2026. Le calendrier détaillé est disponible sur le portail étudiant.',
 'EXAMEN', 'Service Scolarité', TRUE, '2026-04-15 10:00:00'),

('Réouverture des inscriptions pour le Master IADS',
 'Suite à un nombre limité de places restantes, la candidature au Master Intelligence Artificielle et Data Science est rouverte jusqu''au 15 juin 2026.',
 'INFO', 'Coordination IADS', FALSE, '2026-05-20 14:00:00'),

('Vacances de printemps 2026',
 'La faculté sera fermée du 28 mars au 5 avril 2026 inclus pour les vacances de printemps. Reprise des cours le 6 avril.',
 'VACANCE', 'Doyen FSBM', FALSE, '2026-03-10 09:00:00'),

('Maintenance du portail étudiant',
 'Le portail étudiant sera indisponible le dimanche 31 mai 2026 de 22h à 03h pour maintenance technique.',
 'INFO', 'Service Informatique', FALSE, '2026-05-25 16:00:00'),

('Conférence inaugurale du Master IA — Reportée',
 'La conférence inaugurale du Master IADS prévue le 22 mai est reportée au 29 mai 2026. Mêmes horaires et lieu.',
 'URGENT', 'Coordination IADS', TRUE, '2026-05-18 11:30:00');
