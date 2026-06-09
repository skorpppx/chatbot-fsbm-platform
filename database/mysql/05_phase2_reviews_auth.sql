-- =============================================================================
--  FSBM Platform — Migration PHASE 2
--  Avis étudiants (reviews) + Compte administrateur (auth JWT)
--  À exécuter APRÈS 01_schema.sql ... 04_seed_data.sql
-- =============================================================================
--  Contenu :
--    * Table `reviews` : avis polymorphes (assistant IA, modules, profs,
--      filières, faculté, libre) avec note 1..5 + modération.
--    * Seed du compte ADMIN par défaut dans la table `users`.
-- =============================================================================

USE fsbm_db;

-- -----------------------------------------------------------------------------
-- 1. TABLE REVIEWS (avis & recommandations étudiants)
-- -----------------------------------------------------------------------------
--  target_type : sur quoi porte l'avis
--      AI_ASSISTANT = note de l'assistant IA (rating étoiles principal)
--      MODULE / PROFESSOR / FILIERE = avis ciblé (target_id rempli)
--      FACULTE = avis sur la faculté en général
--      GENERAL = zone libre d'avis (sans cible)
--  status : modération
--      APPROVED = visible publiquement (défaut : post-modération)
--      PENDING  = en attente de validation admin
--      HIDDEN   = masqué par l'admin (inapproprié)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    target_type     ENUM('AI_ASSISTANT','MODULE','PROFESSOR','FILIERE','FACULTE','GENERAL')
                        NOT NULL DEFAULT 'GENERAL',
    target_id       BIGINT NULL,                     -- id module/prof/filière ; NULL sinon
    target_label    VARCHAR(200) NULL,               -- libellé lisible (ex: "Assistant IA", "Module Analyse I")
    rating          TINYINT NULL,                    -- 1..5 (obligatoire pour AI_ASSISTANT)
    title           VARCHAR(200) NULL,
    comment         TEXT NOT NULL,
    author_name     VARCHAR(120) NULL,               -- anonyme possible
    author_email    VARCHAR(150) NULL,
    author_filiere  VARCHAR(120) NULL,               -- filière déclarée (texte libre)
    status          ENUM('PENDING','APPROVED','HIDDEN') NOT NULL DEFAULT 'APPROVED',
    is_pinned       BOOLEAN DEFAULT FALSE,
    admin_response  TEXT NULL,                        -- réponse officielle de l'admin
    ip_address      VARCHAR(45) NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_review_rating CHECK (rating IS NULL OR (rating BETWEEN 1 AND 5)),
    INDEX idx_review_target (target_type, target_id),
    INDEX idx_review_status (status),
    INDEX idx_review_created (created_at DESC),
    INDEX idx_review_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 2. COMPTE ADMIN PAR DÉFAUT
-- -----------------------------------------------------------------------------
--  Email    : admin@fsbm.ac.ma
--  Mot de passe : Admin@FSBM2026
--  (hash bcrypt cost 12 — À CHANGER en production)
-- -----------------------------------------------------------------------------
INSERT INTO users (email, password_hash, role, is_active, created_at, updated_at)
VALUES (
    'admin@fsbm.ac.ma',
    '$2b$12$F0i1N4ApvqR/Dxc7VW9HZuy5TXwjfrD0bV6BTzCA2e5cBiiEEONHS',
    'ADMIN',
    TRUE,
    NOW(),
    NOW()
)
ON DUPLICATE KEY UPDATE
    password_hash = VALUES(password_hash),
    role          = 'ADMIN',
    is_active     = TRUE,
    updated_at    = NOW();

-- -----------------------------------------------------------------------------
-- 3. QUELQUES AVIS DE DÉMONSTRATION (pour ne pas avoir un mur vide en soutenance)
-- -----------------------------------------------------------------------------
INSERT INTO reviews (target_type, target_label, rating, title, comment, author_name, author_filiere, status) VALUES
('AI_ASSISTANT', 'Assistant IA', 5, 'Très pratique',
 'L''assistant répond vite et même en darija, ça aide beaucoup pour les inscriptions !',
 'Yassine B.', 'SMI', 'APPROVED'),
('AI_ASSISTANT', 'Assistant IA', 4, 'Bien mais perfectible',
 'Bonnes réponses sur les filières. Parfois il ne comprend pas les questions trop longues.',
 'Salma R.', 'Master IADS', 'APPROVED'),
('FACULTE', 'Faculté FSBM', 5, 'Plateforme au top',
 'Enfin un site clair pour trouver les emplois du temps et les annonces. Bravo.',
 'Anonyme', NULL, 'APPROVED'),
('GENERAL', NULL, NULL, 'Suggestion',
 'Ce serait bien d''ajouter les notes des examens directement dans la plateforme.',
 'Omar K.', 'SMP', 'APPROVED');

-- =============================================================================
--  FIN MIGRATION PHASE 2
-- =============================================================================
SELECT 'Migration Phase 2 terminée — table reviews + admin créés.' AS resultat;
