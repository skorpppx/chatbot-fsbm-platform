-- =============================================================================
--  FSBM Platform - DONNEES REELLES (couche institutionnelle)
--  Genere automatiquement depuis le site officiel fsbm.ma (sources verifiables).
--  Seed idempotent : a executer APRES 01..06. UPSERT, n'ecrase pas l'operationnel.
-- =============================================================================
USE fsbm_db;
SET FOREIGN_KEY_CHECKS=1;

-- 6 departements reels (chefs : fsbm.ma)
INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)
  VALUES ('BIO', 'Biologie', 'Pr. FARH Mohamed', '#1C3F6E', NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();
INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)
  VALUES ('CHI', 'Chimie', 'Pr. EL KOUALI Mhammed', '#1C3F6E', NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();
INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)
  VALUES ('GEO', 'Geologie', 'Pr. MOUFLIH Mustapha', '#1C3F6E', NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();
INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)
  VALUES ('MI', 'Mathematiques et Informatique', 'Pr. ADNAOUI Khalid', '#1C3F6E', NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();
INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)
  VALUES ('PHY', 'Physiques', 'Pr. MAIZROUI M''hammed', '#1C3F6E', NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();
INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)
  VALUES ('SCH', 'Sciences de la Communication et Humanites', 'Pr. Nadia CHAFIQ', '#1C3F6E', NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();

-- Filieres reelles (responsables : fsbm.ma)
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('STATISTIQUES', 'Statistiques', 'LICENCE',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1),
    'Pr. FERJOUCHA Hanane', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('ANALYSE_MATHEMATIQ', 'Analyse Mathematique', 'LICENCE',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1),
    'Pr. BOUDKHIA Khadija', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('CYBERSECURITE_ET_A', 'Cybersecurite et Administration des Systemes et Reseaux', 'LICENCE',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1),
    'Pr. OUAHABI Sara', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('DEVELOPPEMENT_FULL', 'Developpement Full Stack', 'LICENCE',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1),
    'Pr. Mohssine Bensebii', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('ADMINISTRATION_RES', 'Administration Reseaux et Systemes', 'LICENCE',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1),
    'Pr. ACHTAICH Khadija', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('DEVELOPPEMENT_INFO', 'Developpement Informatique', 'LICENCE',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1),
    'Pr. SAEL Nihal', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('PHYSIQUE_APPLIQUEE', 'Physique Appliquee', 'LICENCE',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1),
    'Pr. SAID TADLFIK', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('ELECTRONIQUE_SYSTE', 'Electronique, Systemes embarques et Telecommunication', 'LICENCE',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1),
    'Pr. KASSMI Aziza', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('MECANIQUE_ENERGETI', 'Mecanique Energetique', 'LICENCE',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1),
    'Pr. MOURABIT M. Baika', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('PHYSIQUE_ET_INGENI', 'Physique et Ingenierie des Materiaux (PIM)', 'LICENCE',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1),
    'Pr. ABDERRATI Kamal', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('TRAITEMENT_DE_L_IN', 'Traitement de l''Information', 'MASTER',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1),
    'Pr. ATOUF Issam', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('MATERIAUX_INTELLIG', 'Materiaux Intelligents et Systemes Energetiques', 'MASTER',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1),
    'Pr. EDDIAI Adil', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('GENIE_DES_MATERIAU', 'Genie des Materiaux', 'LICENCE',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1),
    'Pr. MEHDAOUI Boubker', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('PROCEDES_ANALYTIQU', 'Procedes Analytiques et Industriels', 'LICENCE',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1),
    'Pr. BENHANI Laila', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('INSTRUMENTATION_PR', 'Instrumentation, Procedes, Analyse et Qualite', 'MASTER',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1),
    'Pr. MOUMOU Mohamed', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('GENIE_DES_MATER_2', 'Genie des Materiaux et Energie', 'MASTER',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1),
    'Pr. SADIK Chaouki', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('GESTION_DE_L_ENVIR', 'Gestion de l''Environnement et des Ressources Naturelles', 'LICENCE',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1),
    'Pr. ABDELMOTTALIB', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('SCIENCES_BIOMEDICA', 'Sciences Biomedicales Appliquees', 'LICENCE',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1),
    'Pr. FARH Mohamed', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('BIOTECHNOLOGIE_ET_', 'Biotechnologie et Production Vegetale', 'LICENCE',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1),
    'Pr. MOUHTADI Ahmed', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('SCIENCES_DE_LA_SAN', 'Sciences de la Sante', 'MASTER',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1),
    'Pr. Hassan TAKI', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('BIOLOGIE_ET_SANTE', 'Biologie et Sante', 'MASTER',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1),
    'Pr. Amal BOUSFIHA', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('BIOTECHNOLOGIE__2', 'Biotechnologie et Qualite', 'MASTER',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1),
    'Pr. ECH-CHEBRT EL KETTANI M. Anass', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('GEOSCIENCES_ET_GEO', 'Geosciences et Georessources', 'LICENCE',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1),
    'Pr. OUKASSOU Mustapha', 3, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('GEOMATIQUE_APPLIQU', 'Geomatique Appliquee aux Geosciences et a l''Environnement', 'MASTER',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1),
    'Pr. MAIMOUNI Soufiane', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();
INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)
  VALUES ('GEOLOGIE_APPLIQUEE', 'Geologie Appliquee a la Prospection des Ressources Naturelles', 'MASTER',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1),
    'Pr. ALAOUSS Sadok', 2, 80, TRUE, NOW(), NOW())
  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();

-- Echantillon du corps professoral reel (noms : fsbm.ma/faculty, 239 enseignants)
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0001', 'Lalla Malika', 'AADJOUR', 'aadjour.lalla_@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), 'MCH', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0002', 'Halima', 'RAJI', 'raji.halima@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), 'MC', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0003', 'Mostafa', 'HANOUNE', 'hanoune.mostaf@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), 'Chef d''equipe', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0004', 'Hassan', 'TAKI', 'taki.hassan@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0005', 'Ghalem', 'ZAHOUR', 'zahour.ghalem@fsbm.ac.ma', 'PES',
    (SELECT id FROM departments WHERE code='SCH' LIMIT 1), 'PES', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0006', 'Latifa Bouamrani', 'MOUNA', 'mouna.latifa@fsbm.ac.ma', 'PES',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1), 'PES, Directeur de labo', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0007', 'Saida', 'ALIKOUSS', 'alikouss.saida@fsbm.ac.ma', 'PES',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), 'PES, Coordinatrice de Master', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0008', 'KOUALI Mhammed', 'EL', 'el.kouali@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), 'Chef de dept Chimie', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0009', 'Imad', 'ACHIK', 'achik.imad@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), 'MCH, Coordinateur de filiere', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0010', 'CHAFIQ', 'Nadia', 'nadia.chafiq@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), 'Chef de dept SCH', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0011', 'Zouhir', 'BAROUDI', 'baroudi.zouhir@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='SCH' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0012', 'Mohamed', 'SAMIR', 'samir.mohame@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0013', 'HILALI Mohamed', 'EL', 'el.hilali@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0014', 'Chaouki', 'SADIK', 'sadik.chaouk@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), 'MCH', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0015', 'BERRAI Imane', 'EL', 'el.berrai@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), 'MCH, Chef d''equipe', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0016', 'Abdessamad', 'GHAFIRI', 'ghafiri.abdess@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0017', 'Driss', 'RADALLAH', 'radallah.driss@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='SCH' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0018', 'Hassani Ahmed', 'ADLOUNI', 'adlouni.hassan@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0019', 'Hanane', 'SALIH-ALJ', 'salih_alj.hanane@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0020', 'Soumia', 'BELOUAFA', 'belouafa.soumia@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0021', 'Aicha', 'NORDINE', 'nordine.aicha@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0022', 'Abdelmjid', 'ABOURRICHE', 'abourriche.abdelm@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0023', 'Lamia', 'BOURJA', 'bourja.lamia@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='SCH' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0024', 'Samia', 'YOUSFI', 'yousfi.samia@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0025', 'Laila', 'BENNANI', 'bennani.laila@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0026', 'Mohamed', 'RADID', 'radid.mohame@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0027', 'Driss', 'BORIKY', 'boriky.driss@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0028', 'Bahija', 'MOUNIR', 'mounir.bahija@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0029', 'Fatiha', 'AMEGRISSI', 'amegrissi.fatiha@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='SCH' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0030', 'Jamal', 'MOULINE', 'mouline.jamal@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0031', 'Khalid', 'ADNAOUI', 'adnaoui.khalid@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), 'MCH, Chef de dept Math-Info', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0032', 'Driss', 'BOUGGAR', 'bouggar.driss@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), 'MC', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0033', 'Abdelaziz', 'ETTAOUFIK', 'ettaoufik.abdela@fsbm.ac.ma', 'PES',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), 'PES', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0034', 'Hanane', 'FERJOUCHA', 'ferjoucha.hanane@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0035', 'Karima', 'MOHTADI', 'mohtadi.karima@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='SCH' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0036', 'Rachid', 'SAILE', 'saile.rachid@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='BIO' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0037', 'KHASMI Mohammed', 'EL', 'el.khasmi@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='CHI' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0038', 'Mohamed', 'FARH', 'farh.mohame@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='GEO' LIMIT 1), 'Chef de dept Biologie', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0039', 'Abdellatif', 'SLIMANI', 'slimani.abdell@fsbm.ac.ma', 'PH',
    (SELECT id FROM departments WHERE code='MI' LIMIT 1), 'MC', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();
INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)
  VALUES ('REAL0040', 'Yiwen', 'CHEMLAL', 'chemlal.yiwen@fsbm.ac.ma', 'PA',
    (SELECT id FROM departments WHERE code='PHY' LIMIT 1), '-', NOW(), NOW())
  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();

-- FAQ reelles fondees sur les donnees officielles fsbm.ma
DELETE FROM faq_items WHERE intent_tag IN ('doyen_fsbm', 'departements_fsbm', 'filiere_developpement_informatique', 'contact_fsbm_reel', 'corps_professoral_fsbm');
INSERT INTO faq_items (intent_tag, question, answer, keywords, consultations, is_active, created_at, updated_at)
  VALUES ('doyen_fsbm', 'Qui est le doyen de la FSBM ?', 'Le doyen de la Faculte des Sciences Ben M''Sick est le Pr. Abdeslam EL BOUARI.', 'doyen, direction, abdeslam el bouari', 0, TRUE, NOW(), NOW());
INSERT INTO faq_items (intent_tag, question, answer, keywords, consultations, is_active, created_at, updated_at)
  VALUES ('departements_fsbm', 'Quels sont les departements de la FSBM ?', 'La FSBM compte 6 departements : Biologie, Chimie, Geologie, Mathematiques et Informatique, Physiques, et Sciences de la Communication et Humanites.', 'departements, biologie, chimie, geologie, physique, informatique', 0, TRUE, NOW(), NOW());
INSERT INTO faq_items (intent_tag, question, answer, keywords, consultations, is_active, created_at, updated_at)
  VALUES ('filiere_developpement_informatique', 'C''est quoi la filiere Developpement Informatique ?', 'Developpement Informatique est une Licence du departement de Mathematiques et Informatique de la FSBM, sous la responsabilite du Pr. SAEL Nihal.', 'developpement informatique, licence, di, sael nihal', 0, TRUE, NOW(), NOW());
INSERT INTO faq_items (intent_tag, question, answer, keywords, consultations, is_active, created_at, updated_at)
  VALUES ('contact_fsbm_reel', 'Comment contacter la FSBM ?', 'Contact officiel : fsbm.contact@univh2c.ma, telephone +212 6 61 44 24 27, adresse Boulevard Driss El Harti, Ben M''Sik, Casablanca.', 'contact, email, telephone, adresse, scolarite', 0, TRUE, NOW(), NOW());
INSERT INTO faq_items (intent_tag, question, answer, keywords, consultations, is_active, created_at, updated_at)
  VALUES ('corps_professoral_fsbm', 'Combien de professeurs a la FSBM ?', 'Le corps professoral de la FSBM compte 239 enseignants-chercheurs repartis sur les 6 departements.', 'professeurs, enseignants, corps professoral, 239', 0, TRUE, NOW(), NOW());

SELECT CONCAT('Donnees reelles FSBM chargees : ', (SELECT COUNT(*) FROM departments), ' departements, ', (SELECT COUNT(*) FROM filieres), ' filieres, ', (SELECT COUNT(*) FROM professors), ' professeurs.') AS resultat;
