-- =============================================================================
--  FSBM Platform — Schéma MySQL 8.0
--  Projet de Fin d'Études 2025/2026 — Faculté des Sciences Ben M'Sick
--  Université Hassan II de Casablanca
-- =============================================================================
--  Conventions :
--    * snake_case pour les tables et colonnes
--    * Clés primaires : id BIGINT AUTO_INCREMENT
--    * Timestamps : created_at, updated_at (DEFAULT CURRENT_TIMESTAMP)
--    * Soft delete : deleted_at NULLABLE (à activer dans v2)
--    * Charset : utf8mb4 pour supporter les caractères arabes / emojis
--    * Engine : InnoDB pour les contraintes FK
-- =============================================================================

DROP DATABASE IF EXISTS fsbm_db;
CREATE DATABASE fsbm_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE fsbm_db;

-- =============================================================================
-- 1. DÉPARTEMENTS
-- =============================================================================
CREATE TABLE departments (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(20) NOT NULL UNIQUE,
    name            VARCHAR(150) NOT NULL,
    name_short      VARCHAR(50),
    description     TEXT,
    head_name       VARCHAR(150),
    head_email      VARCHAR(150),
    head_phone      VARCHAR(30),
    office_location VARCHAR(150),
    color_hex       VARCHAR(7) DEFAULT '#1C3F6E',
    logo_url        VARCHAR(255),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =============================================================================
-- 2. FILIÈRES (Licences + Masters)
-- =============================================================================
CREATE TABLE filieres (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(20) NOT NULL UNIQUE,    -- ex: SMI, DI, MIAGE
    name            VARCHAR(200) NOT NULL,
    type            ENUM('LICENCE', 'LICENCE_PRO', 'MASTER', 'MASTER_RECHERCHE', 'DOCTORAT') NOT NULL,
    department_id   BIGINT NOT NULL,
    coordinator     VARCHAR(150),
    coord_email     VARCHAR(150),
    duration_years  TINYINT DEFAULT 3,
    capacity        INT DEFAULT 100,
    description     TEXT,
    objectives      TEXT,
    careers         TEXT,                            -- débouchés
    admission       TEXT,                            -- conditions d'accès
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_filiere_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    INDEX idx_filiere_type (type),
    INDEX idx_filiere_dept (department_id)
) ENGINE=InnoDB;

-- =============================================================================
-- 3. MODULES (matières)
-- =============================================================================
CREATE TABLE modules (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(30) NOT NULL UNIQUE,    -- ex: M111, M212
    name            VARCHAR(200) NOT NULL,
    filiere_id      BIGINT NOT NULL,
    semester        TINYINT NOT NULL,                -- 1 à 6 (licence) ou 1 à 4 (master)
    credits         TINYINT DEFAULT 4,
    coefficient     DECIMAL(3,1) DEFAULT 1.0,
    hours_cours     INT DEFAULT 24,                  -- heures de cours
    hours_td        INT DEFAULT 18,                  -- heures de TD
    hours_tp        INT DEFAULT 12,                  -- heures de TP
    description     TEXT,
    prerequisites   TEXT,
    is_eliminatory  BOOLEAN DEFAULT FALSE,           -- note éliminatoire
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_module_filiere FOREIGN KEY (filiere_id) REFERENCES filieres(id) ON DELETE CASCADE,
    INDEX idx_module_semester (semester),
    INDEX idx_module_filiere (filiere_id)
) ENGINE=InnoDB;

-- =============================================================================
-- 4. PROFESSEURS
-- =============================================================================
CREATE TABLE professors (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    matricule       VARCHAR(30) NOT NULL UNIQUE,
    first_name      VARCHAR(80) NOT NULL,
    last_name       VARCHAR(80) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    phone           VARCHAR(30),
    grade           ENUM('PA', 'PH', 'PES', 'VACATAIRE', 'EMERITE') DEFAULT 'PA',
    department_id   BIGINT NOT NULL,
    specialty       VARCHAR(200),
    bureau          VARCHAR(50),
    photo_url       VARCHAR(255),
    bio             TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_prof_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    INDEX idx_prof_dept (department_id),
    INDEX idx_prof_name (last_name, first_name)
) ENGINE=InnoDB;

-- =============================================================================
-- 5. RELATION PROF ↔ MODULE (Many-to-Many)
-- =============================================================================
CREATE TABLE module_teachers (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    module_id       BIGINT NOT NULL,
    professor_id    BIGINT NOT NULL,
    role            ENUM('TITULAIRE', 'ASSISTANT', 'TD', 'TP') DEFAULT 'TITULAIRE',
    annee_univ      VARCHAR(9) DEFAULT '2025-2026',
    CONSTRAINT fk_mt_module FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    CONSTRAINT fk_mt_prof   FOREIGN KEY (professor_id) REFERENCES professors(id) ON DELETE CASCADE,
    UNIQUE KEY uk_module_prof_year (module_id, professor_id, annee_univ)
) ENGINE=InnoDB;

-- =============================================================================
-- 6. ÉTUDIANTS
-- =============================================================================
CREATE TABLE students (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    cne             VARCHAR(20) NOT NULL UNIQUE,     -- Code National Étudiant
    apogee          VARCHAR(20) UNIQUE,              -- Numéro Apogée
    first_name      VARCHAR(80) NOT NULL,
    last_name       VARCHAR(80) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    phone           VARCHAR(30),
    birth_date      DATE,
    birth_place     VARCHAR(100),
    gender          ENUM('M', 'F') NOT NULL,
    nationality     VARCHAR(50) DEFAULT 'Marocaine',
    cin             VARCHAR(20),
    address         VARCHAR(255),
    city            VARCHAR(80) DEFAULT 'Casablanca',
    filiere_id      BIGINT NOT NULL,
    annee_etude     TINYINT NOT NULL DEFAULT 1,      -- 1, 2, 3 (licence) ou 1, 2 (master)
    group_name      VARCHAR(20),                     -- ex: G1, G2A, TD3
    is_boursier     BOOLEAN DEFAULT FALSE,
    statut          ENUM('ACTIF', 'SUSPENDU', 'DIPLOME', 'ABANDON') DEFAULT 'ACTIF',
    photo_url       VARCHAR(255),
    enrolled_at     DATE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_filiere FOREIGN KEY (filiere_id) REFERENCES filieres(id) ON DELETE RESTRICT,
    INDEX idx_student_filiere (filiere_id),
    INDEX idx_student_year (annee_etude),
    INDEX idx_student_name (last_name, first_name),
    INDEX idx_student_group (group_name)
) ENGINE=InnoDB;

-- =============================================================================
-- 7. NOTES & RÉSULTATS
-- =============================================================================
CREATE TABLE grades (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id      BIGINT NOT NULL,
    module_id       BIGINT NOT NULL,
    note_cc         DECIMAL(4,2),                    -- contrôle continu /20
    note_examen     DECIMAL(4,2),                    -- examen final /20
    note_finale     DECIMAL(4,2),                    -- moyenne pondérée /20
    session         ENUM('NORMALE', 'RATTRAPAGE') DEFAULT 'NORMALE',
    annee_univ      VARCHAR(9) DEFAULT '2025-2026',
    is_validated    BOOLEAN DEFAULT FALSE,
    mention         ENUM('PASSABLE', 'AB', 'BIEN', 'TB', 'ELIMINE') NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_grade_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT fk_grade_module  FOREIGN KEY (module_id)  REFERENCES modules(id)  ON DELETE CASCADE,
    UNIQUE KEY uk_grade_unique (student_id, module_id, session, annee_univ),
    INDEX idx_grade_student (student_id),
    INDEX idx_grade_module (module_id)
) ENGINE=InnoDB;

-- =============================================================================
-- 8. EMPLOI DU TEMPS
-- =============================================================================
CREATE TABLE schedules (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    filiere_id      BIGINT NOT NULL,
    module_id       BIGINT NOT NULL,
    professor_id    BIGINT,
    semester        TINYINT NOT NULL,
    annee_etude     TINYINT NOT NULL,
    group_name      VARCHAR(20),
    day_of_week     ENUM('LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI') NOT NULL,
    start_time      TIME NOT NULL,
    end_time        TIME NOT NULL,
    salle           VARCHAR(50) NOT NULL,            -- ex: Amphi A, Salle 3.12
    type_seance     ENUM('COURS', 'TD', 'TP', 'EXAMEN') DEFAULT 'COURS',
    annee_univ      VARCHAR(9) DEFAULT '2025-2026',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_schedule_filiere FOREIGN KEY (filiere_id) REFERENCES filieres(id) ON DELETE CASCADE,
    CONSTRAINT fk_schedule_module  FOREIGN KEY (module_id)  REFERENCES modules(id)  ON DELETE CASCADE,
    CONSTRAINT fk_schedule_prof    FOREIGN KEY (professor_id) REFERENCES professors(id) ON DELETE SET NULL,
    INDEX idx_schedule_filiere_sem (filiere_id, semester),
    INDEX idx_schedule_day (day_of_week, start_time)
) ENGINE=InnoDB;

-- =============================================================================
-- 9. EXAMENS
-- =============================================================================
CREATE TABLE exams (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    module_id       BIGINT NOT NULL,
    filiere_id      BIGINT NOT NULL,
    exam_date       DATE NOT NULL,
    start_time      TIME NOT NULL,
    duration_min    INT DEFAULT 120,
    salle           VARCHAR(100) NOT NULL,
    session         ENUM('NORMALE_S1','NORMALE_S2','RATTRAPAGE') NOT NULL,
    annee_univ      VARCHAR(9) DEFAULT '2025-2026',
    surveillants    TEXT,                            -- noms séparés par virgules
    consignes       TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_exam_module  FOREIGN KEY (module_id)  REFERENCES modules(id)  ON DELETE CASCADE,
    CONSTRAINT fk_exam_filiere FOREIGN KEY (filiere_id) REFERENCES filieres(id) ON DELETE CASCADE,
    INDEX idx_exam_date (exam_date),
    INDEX idx_exam_session (session)
) ENGINE=InnoDB;

-- =============================================================================
-- 10. CATÉGORIES & FAQ
-- =============================================================================
CREATE TABLE faq_categories (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(50) NOT NULL UNIQUE,
    name            VARCHAR(150) NOT NULL,
    description     TEXT,
    icon            VARCHAR(20),                     -- emoji
    color_hex       VARCHAR(7),
    display_order   INT DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE faq_items (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    category_id     BIGINT,
    intent_tag      VARCHAR(80) NOT NULL,
    question        TEXT NOT NULL,
    answer          TEXT NOT NULL,
    keywords        TEXT,                            -- mots-clés séparés par virgules
    related_url     VARCHAR(255),
    consultations   INT DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_faq_category FOREIGN KEY (category_id) REFERENCES faq_categories(id) ON DELETE SET NULL,
    INDEX idx_faq_tag (intent_tag),
    INDEX idx_faq_category (category_id),
    FULLTEXT idx_faq_search (question, answer, keywords)
) ENGINE=InnoDB;

-- =============================================================================
-- 11. CONVERSATIONS (historique chatbot)
-- =============================================================================
CREATE TABLE conversations (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id      VARCHAR(100) NOT NULL,
    user_id         BIGINT,                          -- nullable si anonyme
    user_message    TEXT NOT NULL,
    bot_response    TEXT NOT NULL,
    intent_detected VARCHAR(80),
    confidence      DECIMAL(5,4),
    response_time_ms INT,
    user_agent      VARCHAR(255),
    ip_address      VARCHAR(45),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_conv_session (session_id),
    INDEX idx_conv_intent (intent_detected),
    INDEX idx_conv_date (created_at)
) ENGINE=InnoDB;

-- =============================================================================
-- 12. FEEDBACKS
-- =============================================================================
CREATE TABLE feedbacks (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    conversation_id BIGINT,
    note            TINYINT CHECK (note BETWEEN 1 AND 5),
    is_helpful      BOOLEAN,
    commentaire     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fb_conversation FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    INDEX idx_fb_note (note)
) ENGINE=InnoDB;

-- =============================================================================
-- 13. ANNONCES & ÉVÉNEMENTS
-- =============================================================================
CREATE TABLE announcements (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    content         TEXT NOT NULL,
    type            ENUM('INFO','URGENT','EXAMEN','EVENT','VACANCE') DEFAULT 'INFO',
    target_filiere  BIGINT NULL,                     -- NULL = tous
    target_year     TINYINT NULL,                    -- NULL = toutes années
    author          VARCHAR(150),
    published_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at      TIMESTAMP NULL,
    is_pinned       BOOLEAN DEFAULT FALSE,
    image_url       VARCHAR(255),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ann_filiere FOREIGN KEY (target_filiere) REFERENCES filieres(id) ON DELETE SET NULL,
    INDEX idx_ann_published (published_at DESC),
    INDEX idx_ann_type (type)
) ENGINE=InnoDB;

CREATE TABLE events (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    event_type      ENUM('CONFERENCE','HACKATHON','PORTES_OUVERTES','GALA','FORUM','AUTRE') DEFAULT 'AUTRE',
    start_date      DATETIME NOT NULL,
    end_date        DATETIME,
    location        VARCHAR(200),
    organizer       VARCHAR(150),
    registration_url VARCHAR(255),
    image_url       VARCHAR(255),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_date (start_date)
) ENGINE=InnoDB;

-- =============================================================================
-- 14. CLUBS
-- =============================================================================
CREATE TABLE clubs (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    description     TEXT,
    category        ENUM('SCIENTIFIQUE','CULTUREL','SPORTIF','HUMANITAIRE','TECHNIQUE') DEFAULT 'TECHNIQUE',
    president       VARCHAR(150),
    contact_email   VARCHAR(150),
    social_links    JSON,
    logo_url        VARCHAR(255),
    members_count   INT DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =============================================================================
-- 15. UTILISATEURS (pour auth JWT - student-service)
-- =============================================================================
CREATE TABLE users (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('STUDENT','PROFESSOR','SCOLARITE','ADMIN') NOT NULL DEFAULT 'STUDENT',
    student_id      BIGINT NULL,
    professor_id    BIGINT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    last_login      TIMESTAMP NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_student FOREIGN KEY (student_id)   REFERENCES students(id)   ON DELETE SET NULL,
    CONSTRAINT fk_user_prof    FOREIGN KEY (professor_id) REFERENCES professors(id) ON DELETE SET NULL,
    INDEX idx_user_role (role)
) ENGINE=InnoDB;

-- =============================================================================
-- 16. STATISTIQUES JOURNALIÈRES (agrégat pour analytics-service)
-- =============================================================================
CREATE TABLE daily_stats (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    stat_date           DATE NOT NULL UNIQUE,
    conversations_count INT DEFAULT 0,
    unique_sessions     INT DEFAULT 0,
    top_intent          VARCHAR(80),
    avg_confidence      DECIMAL(5,4),
    avg_satisfaction    DECIMAL(3,2),
    resolution_rate     DECIMAL(5,2),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
