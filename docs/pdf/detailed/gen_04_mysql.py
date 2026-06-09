"""PDF 4 - MySQL + SQLAlchemy Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 04/10", "MySQL + SQLAlchemy",
           "Bases relationnelles + ORM Python async",
           accent_color=HexColor('#00758F'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - C'est quoi une BDD relationnelle ?", "3"),
    ("Chapitre 2 - SQL : les bases", "6"),
    ("Chapitre 3 - Cles primaires et etrangeres", "10"),
    ("Chapitre 4 - Normalisation (1NF, 2NF, 3NF)", "13"),
    ("Chapitre 5 - Les 16 tables de fsbm_db", "16"),
    ("Chapitre 6 - Relations entre tables", "22"),
    ("Chapitre 7 - Index et performance", "25"),
    ("Chapitre 8 - C'est quoi un ORM ?", "28"),
    ("Chapitre 9 - SQLAlchemy 2.0", "31"),
    ("Chapitre 10 - SQLAlchemy async (aiomysql)", "35"),
    ("Chapitre 11 - CRUD avec SQLAlchemy", "38"),
    ("Chapitre 12 - Pagination", "42"),
    ("Chapitre 13 - Conclusion", "45"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1
story.append(Paragraph("Chapitre 1 - C'est quoi une BDD relationnelle ?", ST_CHAPTER))
story.append(Paragraph(
    "Une <b>base de donnees relationnelle</b> (RDBMS) stocke les donnees dans des "
    "<b>tableaux</b> (tables) lies entre eux par des <b>cles</b>. Le concept date des "
    "annees 70 (Edgar F. Codd, IBM).",
    ST_BODY))

story.append(analogy(
    "Une BDD relationnelle est comme un <b>classeur Excel</b> avec plusieurs feuilles : une "
    "feuille 'Etudiants', une feuille 'Filieres', une feuille 'Notes'. Les feuilles sont "
    "<b>liees</b> : chaque etudiant a une filiere, chaque note appartient a un etudiant + "
    "un module."))

story.append(Paragraph("1.1 Les 4 SGBD relationnels populaires", ST_H1))
story.append(std_table([
    ['SGBD', 'Createur', 'Forces'],
    ['MySQL', 'Oracle (rachat de Sun)', 'Tres rapide, gratuit, populaire'],
    ['PostgreSQL', 'Communaute', 'Tres complet, SQL standard, JSONB'],
    ['SQL Server', 'Microsoft', 'Excellent pour env Microsoft'],
    ['Oracle DB', 'Oracle', 'Entreprise, tres cher'],
    ['SQLite', 'D. Richard Hipp', 'Embarque (1 fichier)'],
], col_widths=[3*cm, 5*cm, 8*cm]))

story.append(alert_box(
    "Le cahier des charges PFE imposait <b>MySQL</b>. C'est aussi le SGBD le plus utilise au "
    "Maroc (WordPress, banques, e-commerce).",
    kind="info"))

story.append(Paragraph("1.2 Pourquoi MySQL pour notre projet ?", ST_H1))
for x in [
    "<b>Impose par le PFE</b> - on respecte le cahier des charges",
    "<b>Gratuit et open source</b>",
    "<b>Performant</b> pour les volumes moyens (millions de rows)",
    "<b>Compatible</b> avec phpMyAdmin, MySQL Workbench, DBeaver",
    "<b>Largement supporte</b> par tous les hebergeurs",
    "<b>Ecosysteme</b> Python tres mur (PyMySQL, aiomysql, SQLAlchemy)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 2 - SQL bases
story.append(Paragraph("Chapitre 2 - SQL : les bases", ST_CHAPTER))

story.append(Paragraph("2.1 C'est quoi SQL ?", ST_H1))
story.append(Paragraph(
    "<b>SQL = Structured Query Language</b>. C'est le langage standardise (ISO) pour parler "
    "aux BDD relationnelles. Tous les SGBD relationnels le supportent (avec des variantes).",
    ST_BODY))

story.append(Paragraph("2.2 Les 4 categories d'instructions", ST_H1))
story.append(std_table([
    ['Categorie', 'Acronyme', 'Exemples'],
    ['Definition', 'DDL', 'CREATE, ALTER, DROP'],
    ['Manipulation', 'DML', 'SELECT, INSERT, UPDATE, DELETE'],
    ['Controle', 'DCL', 'GRANT, REVOKE'],
    ['Transaction', 'TCL', 'BEGIN, COMMIT, ROLLBACK'],
], col_widths=[3*cm, 2*cm, 11*cm]))

story.append(Paragraph("2.3 CREATE TABLE", ST_H1))
story.append(code(
    "CREATE TABLE departments (\n"
    "    id              BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
    "    code            VARCHAR(20) NOT NULL UNIQUE,\n"
    "    name            VARCHAR(150) NOT NULL,\n"
    "    description     TEXT,\n"
    "    head_name       VARCHAR(150),\n"
    "    head_email      VARCHAR(150),\n"
    "    color_hex       VARCHAR(7) DEFAULT '#1C3F6E',\n"
    "    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
    "    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
    "                    ON UPDATE CURRENT_TIMESTAMP\n"
    ") ENGINE=InnoDB;"
))

story.append(Paragraph("2.4 INSERT", ST_H1))
story.append(code(
    "INSERT INTO departments (code, name, head_name) VALUES\n"
    "  ('MI',  'Departement de Mathematiques et Informatique', 'Pr. Mohammed ALAOUI'),\n"
    "  ('PH',  'Departement de Physique', 'Pr. Khadija BENNANI'),\n"
    "  ('CH',  'Departement de Chimie', 'Pr. Youssef LAHLOU'),\n"
    "  ('BIO', 'Departement de Biologie', 'Pr. Fatima ZAHIDI'),\n"
    "  ('GEO', 'Departement de Geologie', 'Pr. Hassan BERRADA');"
))

story.append(Paragraph("2.5 SELECT (lecture)", ST_H1))
story.append(code(
    "-- Tout :\n"
    "SELECT * FROM departments;\n"
    "\n"
    "-- Colonnes specifiques :\n"
    "SELECT code, name FROM departments;\n"
    "\n"
    "-- Avec filtre :\n"
    "SELECT * FROM departments WHERE code = 'MI';\n"
    "\n"
    "-- Avec tri :\n"
    "SELECT * FROM departments ORDER BY name ASC;\n"
    "\n"
    "-- Avec limite :\n"
    "SELECT * FROM departments LIMIT 10 OFFSET 20;  -- page 3 de 10\n"
    "\n"
    "-- Avec count :\n"
    "SELECT COUNT(*) FROM students WHERE statut = 'ACTIF';\n"
    "\n"
    "-- Avec group by :\n"
    "SELECT filiere_id, COUNT(*) AS nb_etudiants\n"
    "FROM students\n"
    "GROUP BY filiere_id\n"
    "ORDER BY nb_etudiants DESC;"
))

story.append(Paragraph("2.6 UPDATE et DELETE", ST_H1))
story.append(code(
    "UPDATE departments\n"
    "SET head_phone = '+212 522 70 46 71'\n"
    "WHERE code = 'MI';\n"
    "\n"
    "DELETE FROM faq_items WHERE consultations = 0;"
))
story.append(alert_box(
    "TOUJOURS mettre une clause WHERE sur UPDATE et DELETE. Sans, tu modifies/supprimes "
    "TOUTE la table !",
    kind="danger"))

story.append(Paragraph("2.7 JOIN", ST_H1))
story.append(Paragraph(
    "Les JOINs permettent de combiner plusieurs tables :",
    ST_BODY))
story.append(code(
    "-- INNER JOIN : intersection (etudiants qui ont une filiere)\n"
    "SELECT s.cne, s.first_name, s.last_name, f.code AS filiere\n"
    "FROM students s\n"
    "INNER JOIN filieres f ON s.filiere_id = f.id\n"
    "WHERE f.code = 'SMI';\n"
    "\n"
    "-- LEFT JOIN : tous les etudiants, meme sans filiere\n"
    "SELECT s.first_name, f.code AS filiere\n"
    "FROM students s\n"
    "LEFT JOIN filieres f ON s.filiere_id = f.id;"
))
story.append(PageBreak())

# CH 3 - Cles
story.append(Paragraph("Chapitre 3 - Cles primaires et etrangeres", ST_CHAPTER))

story.append(Paragraph("3.1 Cle primaire (PRIMARY KEY)", ST_H1))
story.append(Paragraph(
    "La cle primaire est <b>l'identifiant unique</b> d'une ligne. Une seule par table.",
    ST_BODY))
for x in [
    "<b>Unique</b> : aucune ligne n'a la meme valeur",
    "<b>Non null</b> : toujours definie",
    "<b>Indexee</b> automatiquement (recherche tres rapide)",
    "Souvent un BIGINT AUTO_INCREMENT (1, 2, 3, ...)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("3.2 Cle etrangere (FOREIGN KEY)", ST_H1))
story.append(Paragraph(
    "Une cle etrangere est une <b>reference</b> a la cle primaire d'une autre table. "
    "Elle garantit l'integrite referentielle.",
    ST_BODY))

story.append(code(
    "CREATE TABLE filieres (\n"
    "    id              BIGINT PRIMARY KEY AUTO_INCREMENT,\n"
    "    code            VARCHAR(20) UNIQUE,\n"
    "    name            VARCHAR(200) NOT NULL,\n"
    "    department_id   BIGINT NOT NULL,\n"
    "    \n"
    "    CONSTRAINT fk_filiere_department\n"
    "        FOREIGN KEY (department_id)\n"
    "        REFERENCES departments(id)\n"
    "        ON DELETE RESTRICT  -- empeche de supprimer un dept avec filieres\n"
    ") ENGINE=InnoDB;"
))

story.append(Paragraph("3.3 Les actions ON DELETE", ST_H1))
story.append(std_table([
    ['Action', 'Effet'],
    ['RESTRICT', 'Empeche la suppression si refs existent'],
    ['CASCADE', 'Supprime tout en cascade (DANGEREUX)'],
    ['SET NULL', 'Met la FK a NULL'],
    ['NO ACTION', 'Comme RESTRICT'],
], col_widths=[3*cm, 13*cm]))

story.append(Paragraph("3.4 Exemple dans notre projet", ST_H1))
story.append(diagram(
    "    departments (1)        filieres (N)\n"
    "    +---+--------+         +---+------+----------+\n"
    "    | id| code   |         | id| code | dept_id  |\n"
    "    +---+--------+         +---+------+----------+\n"
    "    | 1 | MI     | <----+  | 1 | SMI  | 1        |\n"
    "    | 2 | PH     |      +- | 2 | DI   | 1        |\n"
    "    | 3 | CH     |         | 3 | SMA  | 1        |\n"
    "    +---+--------+         | 4 | SMP  | 2        |\n"
    "                           +---+------+----------+\n"
    "\n"
    "    SMI, DI, SMA pointent vers le departement MI (id=1)"
))
story.append(PageBreak())

# CH 4 - Normalisation
story.append(Paragraph("Chapitre 4 - Normalisation (1NF, 2NF, 3NF)", ST_CHAPTER))

story.append(Paragraph("4.1 Pourquoi normaliser ?", ST_H1))
story.append(Paragraph(
    "La <b>normalisation</b> est le processus d'organiser une BDD pour <b>eviter la "
    "redondance</b> et garantir la coherence. C'est la theorie qui distingue les amateurs "
    "des pros.",
    ST_BODY))

story.append(Paragraph("4.2 Exemple non-normalise (mauvais)", ST_H1))
story.append(code(
    "TABLE bad_students :\n"
    "+----+--------+----------+---------------------+--------------+\n"
    "| id | name   | filiere  | filiere_dept        | filiere_chef |\n"
    "+----+--------+----------+---------------------+--------------+\n"
    "| 1  | Karim  | SMI      | Math-Info           | Pr. Alaoui   |\n"
    "| 2  | Salma  | SMI      | Math-Info           | Pr. Alaoui   |\n"
    "| 3  | Hamza  | SMI      | Math-Info           | Pr. Alaoui   |\n"
    "+----+--------+----------+---------------------+--------------+\n"
    "\n"
    "Probleme : si on change le chef du dept, il faut modifier\n"
    "TOUTES les lignes de Karim, Salma, Hamza..."
))

story.append(Paragraph("4.3 Apres normalisation", ST_H1))
story.append(code(
    "TABLE departments :\n"
    "+----+-----------+----------------+\n"
    "| id | name      | chef           |\n"
    "+----+-----------+----------------+\n"
    "| 1  | Math-Info | Pr. Alaoui     |\n"
    "+----+-----------+----------------+\n"
    "\n"
    "TABLE filieres :\n"
    "+----+------+-----------+\n"
    "| id | code | dept_id   |\n"
    "+----+------+-----------+\n"
    "| 1  | SMI  | 1         |\n"
    "+----+------+-----------+\n"
    "\n"
    "TABLE students :\n"
    "+----+--------+-----------+\n"
    "| id | name   | filiere_id|\n"
    "+----+--------+-----------+\n"
    "| 1  | Karim  | 1         |\n"
    "| 2  | Salma  | 1         |\n"
    "| 3  | Hamza  | 1         |\n"
    "+----+--------+-----------+\n"
    "\n"
    "Maintenant : changer le chef = modifier UNE seule ligne."
))

story.append(Paragraph("4.4 Les 3 formes normales", ST_H1))
for n, d in [
    ("1NF - Premiere forme normale",
     "Chaque cellule contient UNE valeur (pas de listes). Chaque ligne est unique."),
    ("2NF - Deuxieme forme normale",
     "1NF + tous les attributs non-cle dependent de TOUTE la cle primaire."),
    ("3NF - Troisieme forme normale",
     "2NF + aucun attribut non-cle ne depend d'un autre attribut non-cle."),
]:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(alert_box(
    "Notre projet respecte la 3NF. Cela rend les donnees coherentes, evite la duplication, "
    "et simplifie les mises a jour.",
    kind="success"))
story.append(PageBreak())

# CH 5 - 16 tables
story.append(Paragraph("Chapitre 5 - Les 16 tables de fsbm_db", ST_CHAPTER))

story.append(Paragraph(
    "Voici la liste complete des tables et leur role :",
    ST_BODY))

tables_detail = [
    ("1. departments",
     "Les 5 departements academiques. PK=id, UNIQUE=code (MI, PH, CH, BIO, GEO). "
     "Champs : name, description, head_name, head_email, color_hex pour l'UI."),
    ("2. filieres",
     "25 filieres : 7 licences + 18 masters. PK=id, FK=department_id. "
     "Champs : code (SMI, IADS), type (LICENCE/MASTER), coordinator, capacity, careers."),
    ("3. modules",
     "100+ modules pour chaque filiere. PK=id, FK=filiere_id. "
     "Champs : code (SMI-S1-M1), semester, credits, coefficient, hours_cours/td/tp."),
    ("4. professors",
     "107 profs. PK=id, FK=department_id, UNIQUE=matricule, email. "
     "Champs : grade (PA/PH/PES), specialty, bureau, photo_url."),
    ("5. students",
     "2970 etudiants. PK=id, FK=filiere_id, UNIQUE=cne, apogee, email. "
     "Champs : annee_etude, group_name, is_boursier, statut (ACTIF/SUSPENDU/DIPLOME)."),
    ("6. module_teachers",
     "Relation N:N entre modules et professors. FK=module_id, FK=professor_id. "
     "Champs : role (TITULAIRE/ASSISTANT/TD/TP), annee_univ."),
    ("7. schedules",
     "Emploi du temps. FK=filiere_id, FK=module_id, FK=professor_id. "
     "Champs : day_of_week, start_time, end_time, salle, type_seance."),
    ("8. exams",
     "Calendrier examens. FK=module_id, FK=filiere_id. "
     "Champs : exam_date, salle, session (NORMALE_S1/S2/RATTRAPAGE)."),
    ("9. grades",
     "9000+ notes. FK=student_id, FK=module_id. "
     "Champs : note_cc, note_examen, note_finale, mention (PASSABLE/AB/BIEN/TB)."),
    ("10. faq_categories",
     "16 categories pour le chatbot. PK=id, UNIQUE=code. "
     "Champs : name, icon (emoji), color_hex."),
    ("11. faq_items",
     "Items FAQ avec FULLTEXT search. FK=category_id. "
     "Champs : intent_tag, question, answer, keywords."),
    ("12. conversations",
     "Historique chatbot. Champs : session_id, user_message, bot_response, "
     "intent_detected, confidence, response_time_ms."),
    ("13. feedbacks",
     "Notes 1-5 utilisateurs. FK=conversation_id. "
     "Champs : note, is_helpful, commentaire."),
    ("14. announcements",
     "Annonces officielles. FK=target_filiere (optionnel). "
     "Champs : title, content, type (INFO/URGENT/EXAMEN/EVENT/VACANCE), is_pinned."),
    ("15. events",
     "Evenements (JPO, hackathon...). "
     "Champs : title, event_type, start_date, location, registration_url."),
    ("16. clubs",
     "8 clubs etudiants. "
     "Champs : name, category, president, social_links (JSON), members_count."),
]
for n, d in tables_detail:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))
story.append(PageBreak())

# CH 6 - Relations
story.append(Paragraph("Chapitre 6 - Relations entre tables", ST_CHAPTER))

story.append(Paragraph("6.1 Relation 1:N (un a plusieurs)", ST_H1))
story.append(Paragraph(
    "Un departement a PLUSIEURS filieres. Une filiere appartient a UN departement.",
    ST_BODY))
story.append(diagram(
    "    departments              filieres\n"
    "    +---+--------+            +---+------+------------+\n"
    "    | id| code   | 1 -----N>  | id| code | department_id\n"
    "    +---+--------+            +---+------+------------+"
))

story.append(Paragraph("6.2 Relation N:N (plusieurs a plusieurs)", ST_H1))
story.append(Paragraph(
    "Un module peut etre enseigne par PLUSIEURS profs. Un prof peut enseigner PLUSIEURS "
    "modules. Solution : table intermediaire <code>module_teachers</code>.",
    ST_BODY))
story.append(diagram(
    "    modules            module_teachers          professors\n"
    "    +---+         +-------+--------+-------+         +---+\n"
    "    | id| 1 ----N | mod_id| prof_id| role  | N---- 1 | id|\n"
    "    +---+         +-------+--------+-------+         +---+"
))

story.append(Paragraph("6.3 Toutes les relations de fsbm_db", ST_H1))
story.append(diagram(
    "departments (1) ----N filieres ----N modules\n"
    "                |          |              |\n"
    "                |          v              v\n"
    "                |       students       schedules\n"
    "                |          |              |\n"
    "                |          v              v\n"
    "                |       grades         exams\n"
    "                |\n"
    "departments (1) ----N professors ----N module_teachers >---- modules\n"
    "\n"
    "faq_categories (1) ----N faq_items\n"
    "\n"
    "conversations (1) ----N feedbacks\n"
    "\n"
    "filieres (1) ----0-N announcements"
))
story.append(PageBreak())

# CH 7 - Index
story.append(Paragraph("Chapitre 7 - Index et performance", ST_CHAPTER))

story.append(Paragraph("7.1 C'est quoi un index ?", ST_H1))
story.append(Paragraph(
    "Un <b>index</b> est une <b>structure de donnees auxiliaire</b> qui permet de retrouver "
    "rapidement les lignes correspondant a une valeur. C'est comme la <b>table des matieres</b> "
    "d'un livre.",
    ST_BODY))

story.append(analogy(
    "Sans index, MySQL lit toutes les lignes une par une jusqu'a trouver. C'est comme "
    "chercher 'apple' en lisant le dictionnaire de A a Z. Avec index, MySQL utilise un "
    "arbre B-tree (sorte d'index alphabetique) pour aller direct au bon endroit."))

story.append(Paragraph("7.2 Quand creer un index ?", ST_H1))
for x in [
    "Sur les colonnes utilisees dans des WHERE frequents",
    "Sur les FK (deja automatique en InnoDB)",
    "Sur les colonnes utilisees dans des ORDER BY",
    "PAS sur les colonnes peu selectives (ex: boolean)",
    "PAS sur des tables avec beaucoup d'INSERT (les index ralentissent l'ecriture)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("7.3 Index dans notre projet", ST_H1))
story.append(code(
    "CREATE TABLE students (\n"
    "    id              BIGINT PRIMARY KEY,\n"
    "    cne             VARCHAR(20) UNIQUE,\n"
    "    first_name      VARCHAR(80),\n"
    "    last_name       VARCHAR(80),\n"
    "    email           VARCHAR(150) UNIQUE,\n"
    "    filiere_id      BIGINT,\n"
    "    annee_etude     TINYINT,\n"
    "    \n"
    "    -- Index explicites :\n"
    "    INDEX idx_student_filiere (filiere_id),\n"
    "    INDEX idx_student_year (annee_etude),\n"
    "    INDEX idx_student_name (last_name, first_name),  -- index compose\n"
    "    INDEX idx_student_group (group_name)\n"
    ");"
))

story.append(Paragraph("7.4 FULLTEXT pour recherche texte", ST_H1))
story.append(code(
    "CREATE TABLE faq_items (\n"
    "    ...,\n"
    "    FULLTEXT idx_faq_search (question, answer, keywords)\n"
    ");\n"
    "\n"
    "-- Utilisation :\n"
    "SELECT * FROM faq_items\n"
    "WHERE MATCH(question, answer) AGAINST('inscription master');"
))
story.append(PageBreak())

# CH 8 - ORM
story.append(Paragraph("Chapitre 8 - C'est quoi un ORM ?", ST_CHAPTER))

story.append(Paragraph("8.1 Le probleme du SQL brut", ST_H1))
story.append(code(
    "# Approche raw SQL (pymysql)\n"
    "conn = pymysql.connect(host='localhost', user='root', password='...')\n"
    "cursor = conn.cursor()\n"
    "cursor.execute(\"SELECT * FROM filieres WHERE type = %s\", ('MASTER',))\n"
    "rows = cursor.fetchall()\n"
    "\n"
    "# Problemes :\n"
    "# - Strings SQL fragiles (risque d'injection)\n"
    "# - rows est juste une liste de tuples (pas tres lisible)\n"
    "# - Pas de type checking\n"
    "# - Difficile a maintenir"
))

story.append(Paragraph("8.2 La solution ORM", ST_H1))
story.append(Paragraph(
    "<b>ORM = Object-Relational Mapping</b>. Au lieu d'ecrire du SQL, on manipule des "
    "<b>objets Python</b>. L'ORM traduit en SQL automatiquement.",
    ST_BODY))

story.append(code(
    "# Approche ORM (SQLAlchemy)\n"
    "result = await db.execute(\n"
    "    select(Filiere).where(Filiere.type == 'MASTER')\n"
    ")\n"
    "masters = result.scalars().all()\n"
    "\n"
    "for m in masters:\n"
    "    print(m.code, m.name)  # acces objet, autocomplete IDE"
))

story.append(Paragraph("8.3 Avantages de l'ORM", ST_H1))
for x in [
    "<b>Securite</b> : protection auto contre les injections SQL",
    "<b>Type safety</b> : autocompletion IDE, type checking",
    "<b>Portabilite</b> : si tu changes de SGBD (MySQL -> PostgreSQL), peu de code a changer",
    "<b>Productivite</b> : moins de code a ecrire",
    "<b>Migrations</b> : Alembic genere les CREATE TABLE auto a partir des modeles",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("8.4 Inconvenients", ST_H1))
for x in [
    "Performance : ORM est 10-30% plus lent que SQL natif",
    "Complexite : pour requetes complexes, l'ORM peut etre verbeux",
    "Courbe d'apprentissage : apprendre les concepts ORM",
]:
    story.append(Paragraph(f"- {x}", ST_LIST))
story.append(PageBreak())

# CH 9 - SQLAlchemy 2.0
story.append(Paragraph("Chapitre 9 - SQLAlchemy 2.0", ST_CHAPTER))

story.append(Paragraph("9.1 SQLAlchemy en bref", ST_H1))
story.append(Paragraph(
    "<b>SQLAlchemy</b> est l'ORM Python <b>standard</b>. Version 2.0 (2023) apporte une "
    "syntaxe moderne avec <code>Mapped[T]</code> et un support async natif.",
    ST_BODY))

story.append(Paragraph("9.2 Definition d'un modele", ST_H1))
story.append(code(
    "from sqlalchemy import String, BigInteger, ForeignKey\n"
    "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship\n"
    "\n"
    "class Base(DeclarativeBase):\n"
    "    pass\n"
    "\n"
    "class Department(Base):\n"
    "    __tablename__ = 'departments'\n"
    "    \n"
    "    id:      Mapped[int] = mapped_column(BigInteger, primary_key=True)\n"
    "    code:    Mapped[str] = mapped_column(String(20), unique=True)\n"
    "    name:    Mapped[str] = mapped_column(String(150))\n"
    "    \n"
    "    # Relation 1:N\n"
    "    filieres: Mapped[list['Filiere']] = relationship(\n"
    "        back_populates='department'\n"
    "    )\n"
    "\n"
    "class Filiere(Base):\n"
    "    __tablename__ = 'filieres'\n"
    "    \n"
    "    id:            Mapped[int] = mapped_column(BigInteger, primary_key=True)\n"
    "    code:          Mapped[str] = mapped_column(String(20), unique=True)\n"
    "    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))\n"
    "    \n"
    "    # Relation inverse\n"
    "    department: Mapped['Department'] = relationship(\n"
    "        back_populates='filieres'\n"
    "    )"
))

story.append(Paragraph("9.3 Avantages de la syntaxe Mapped[T]", ST_H1))
for x in [
    "Type hints natifs Python (autocompletion)",
    "Mypy/Pyright peuvent verifier les types",
    "Plus lisible que la syntaxe Column() de SQLAlchemy 1.x",
    "Optionnel automatique : Mapped[Optional[str]] = NULL OK",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 10 - Async
story.append(Paragraph("Chapitre 10 - SQLAlchemy async (aiomysql)", ST_CHAPTER))

story.append(Paragraph("10.1 Pourquoi async ?", ST_H1))
story.append(Paragraph(
    "Sans async, chaque requete DB bloque le serveur pendant 1-100ms. Avec async, le serveur "
    "peut traiter d'autres requetes pendant l'attente.",
    ST_BODY))

story.append(Paragraph("10.2 Setup du moteur async", ST_H1))
story.append(code(
    "from sqlalchemy.ext.asyncio import (\n"
    "    create_async_engine, async_sessionmaker, AsyncSession\n"
    ")\n"
    "\n"
    "DATABASE_URL = (\n"
    "    'mysql+aiomysql://root:password@localhost:3306/fsbm_db'\n"
    ")\n"
    "\n"
    "engine = create_async_engine(\n"
    "    DATABASE_URL,\n"
    "    echo=False,             # True pour voir le SQL genere\n"
    "    pool_pre_ping=True,     # verifie la connexion avant usage\n"
    "    pool_recycle=3600,      # recycle apres 1h\n"
    ")\n"
    "\n"
    "SessionLocal = async_sessionmaker(\n"
    "    engine,\n"
    "    expire_on_commit=False,\n"
    "    class_=AsyncSession,\n"
    ")"
))

story.append(Paragraph("10.3 Dependency pour les routes", ST_H1))
story.append(code(
    "async def get_db() -> AsyncSession:\n"
    "    async with SessionLocal() as session:\n"
    "        yield session\n"
    "        # Apres yield : la session se ferme automatiquement\n"
    "\n"
    "@router.get('/api/filieres')\n"
    "async def list_filieres(db: AsyncSession = Depends(get_db)):\n"
    "    result = await db.execute(select(Filiere))\n"
    "    return result.scalars().all()"
))

story.append(Paragraph("10.4 Pool de connexions", ST_H1))
story.append(Paragraph(
    "SQLAlchemy maintient un <b>pool</b> de connexions reutilisables. Au lieu d'ouvrir/fermer "
    "une connexion par requete (couteux), on emprunte une connexion existante du pool.",
    ST_BODY))

story.append(alert_box(
    "Par defaut : 5 connexions max + 10 overflow. Pour 1000 utilisateurs concurrents, "
    "augmenter <code>pool_size=20, max_overflow=30</code>.",
    kind="info"))
story.append(PageBreak())

# CH 11 - CRUD
story.append(Paragraph("Chapitre 11 - CRUD avec SQLAlchemy", ST_CHAPTER))

story.append(Paragraph("11.1 CREATE (Insert)", ST_H1))
story.append(code(
    "new_dept = Department(code='INFO', name='Informatique nouvelle')\n"
    "db.add(new_dept)\n"
    "await db.commit()\n"
    "await db.refresh(new_dept)\n"
    "print(new_dept.id)  # ID auto-genere"
))

story.append(Paragraph("11.2 READ (Select)", ST_H1))
story.append(code(
    "# Tout\n"
    "result = await db.execute(select(Filiere))\n"
    "all_filieres = result.scalars().all()\n"
    "\n"
    "# Par ID\n"
    "fil = await db.get(Filiere, 1)\n"
    "\n"
    "# Avec WHERE\n"
    "stmt = select(Filiere).where(Filiere.type == 'MASTER')\n"
    "result = await db.execute(stmt)\n"
    "masters = result.scalars().all()\n"
    "\n"
    "# Avec JOIN\n"
    "stmt = (\n"
    "    select(Filiere, Department.name.label('dept_name'))\n"
    "    .join(Department, Department.id == Filiere.department_id)\n"
    ")\n"
    "result = await db.execute(stmt)\n"
    "for fil, dept_name in result.all():\n"
    "    print(fil.code, dept_name)\n"
    "\n"
    "# Count\n"
    "total = await db.scalar(select(func.count(Filiere.id)))\n"
    "\n"
    "# Group by\n"
    "stmt = (\n"
    "    select(Filiere.type, func.count(Filiere.id))\n"
    "    .group_by(Filiere.type)\n"
    ")\n"
    "result = await db.execute(stmt)\n"
    "for type_, count in result.all():\n"
    "    print(type_, count)"
))

story.append(Paragraph("11.3 UPDATE", ST_H1))
story.append(code(
    "# Methode 1 : update objet + commit\n"
    "fil = await db.get(Filiere, 1)\n"
    "fil.capacity = 200\n"
    "await db.commit()\n"
    "\n"
    "# Methode 2 : UPDATE en masse\n"
    "from sqlalchemy import update\n"
    "stmt = (\n"
    "    update(Filiere)\n"
    "    .where(Filiere.type == 'MASTER')\n"
    "    .values(is_active=True)\n"
    ")\n"
    "await db.execute(stmt)\n"
    "await db.commit()"
))

story.append(Paragraph("11.4 DELETE", ST_H1))
story.append(code(
    "# Methode 1 : delete objet\n"
    "fil = await db.get(Filiere, 99)\n"
    "if fil:\n"
    "    await db.delete(fil)\n"
    "    await db.commit()\n"
    "\n"
    "# Methode 2 : DELETE en masse\n"
    "from sqlalchemy import delete\n"
    "stmt = delete(FaqItem).where(FaqItem.consultations == 0)\n"
    "await db.execute(stmt)\n"
    "await db.commit()"
))
story.append(PageBreak())

# CH 12 - Pagination
story.append(Paragraph("Chapitre 12 - Pagination", ST_CHAPTER))

story.append(Paragraph("12.1 Pourquoi paginer ?", ST_H1))
story.append(Paragraph(
    "Sans pagination, GET /api/students renvoie 2970 etudiants d'un coup. C'est :",
    ST_BODY))
for x in [
    "Lent (transfert reseau lourd)",
    "Memory-intensive cote client",
    "Inutile (l'utilisateur regarde 20 etudiants a la fois)",
]:
    story.append(Paragraph(f"- {x}", ST_LIST))

story.append(Paragraph("12.2 Pagination avec offset/limit", ST_H1))
story.append(code(
    "@router.get('/api/students', response_model=PaginatedResponse)\n"
    "async def list_students(\n"
    "    page: int = Query(1, ge=1),\n"
    "    page_size: int = Query(20, ge=1, le=100),\n"
    "    db: AsyncSession = Depends(get_db),\n"
    "):\n"
    "    # Count total\n"
    "    total = await db.scalar(select(func.count(Student.id))) or 0\n"
    "    \n"
    "    # Paginer\n"
    "    stmt = (\n"
    "        select(Student)\n"
    "        .order_by(Student.last_name, Student.first_name)\n"
    "        .offset((page - 1) * page_size)\n"
    "        .limit(page_size)\n"
    "    )\n"
    "    result = await db.execute(stmt)\n"
    "    items = result.scalars().all()\n"
    "    \n"
    "    return PaginatedResponse(\n"
    "        items=items,\n"
    "        total=total,\n"
    "        page=page,\n"
    "        page_size=page_size,\n"
    "        total_pages=(total + page_size - 1) // page_size,\n"
    "    )"
))

story.append(Paragraph("12.3 Schema PaginatedResponse", ST_H1))
story.append(code(
    "from pydantic import BaseModel\n"
    "from typing import Generic, TypeVar\n"
    "\n"
    "T = TypeVar('T')\n"
    "\n"
    "class PaginatedResponse(BaseModel, Generic[T]):\n"
    "    items: list[T]\n"
    "    total: int\n"
    "    page: int = 1\n"
    "    page_size: int = 20\n"
    "    total_pages: int = 1\n"
    "\n"
    "# Usage avec type fort :\n"
    "@router.get('/api/students',\n"
    "    response_model=PaginatedResponse[StudentOut])\n"
    "async def list_students(...): ..."
))
story.append(PageBreak())

# CH 13 - Conclusion
story.append(Paragraph("Chapitre 13 - Conclusion", ST_CHAPTER))

story.append(Paragraph("13.1 Recap", ST_H1))
for x in [
    "BDD relationnelle = donnees structurees en tables liees par FK",
    "SQL = langage standard pour parler aux BDD",
    "Cles primaires (uniques) et etrangeres (references)",
    "Normalisation 3NF = pas de redondance",
    "Index = recherche rapide (B-tree, FULLTEXT)",
    "ORM = manipuler des objets Python au lieu de SQL",
    "SQLAlchemy 2.0 = ORM moderne async avec Mapped[T]",
    "Async + pool de connexions = perfs max",
    "CRUD = Create/Read/Update/Delete",
    "Pagination = ne pas tout renvoyer d'un coup",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("13.2 Pour aller plus loin", ST_H1))
for x in [
    "PDF 05 - pour MongoDB et les differences SQL vs NoSQL",
    "PDF 03 - pour comprendre comment FastAPI s'integre avec SQLAlchemy",
    "PDF 09 - pour le flux complet incluant une requete DB",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("04_MySQL_SQLAlchemy_Complet.pdf", story,
          "PDF 04 - MySQL + SQLAlchemy",
          "FSBM Platform - MySQL et SQLAlchemy Complet")
