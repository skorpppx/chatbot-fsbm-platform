-- =============================================================================
--  FSBM Platform — Migration PHASE 2 (suite)
--  Champs media : logos filieres + pieces jointes (PDF) annonces/evenements
--  A executer APRES 05_phase2_reviews_auth.sql
-- =============================================================================
--  Note : MySQL ne supporte pas "ADD COLUMN IF NOT EXISTS".
--  Si une colonne existe deja, ignore l'erreur "Duplicate column".
--  (Dans le flux SETUP.ps1, 01_schema DROP la base donc pas de conflit.)
-- =============================================================================

USE fsbm_db;

-- Logo pour les filieres (departments.logo_url existe deja)
ALTER TABLE filieres     ADD COLUMN logo_url       VARCHAR(255) NULL;

-- Piece jointe PDF pour annonces et evenements (image_url existe deja)
ALTER TABLE announcements ADD COLUMN attachment_url VARCHAR(255) NULL;
ALTER TABLE events        ADD COLUMN attachment_url VARCHAR(255) NULL;

SELECT 'Migration 06 terminee — logo_url + attachment_url ajoutes.' AS resultat;
