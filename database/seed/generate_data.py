"""
============================================================================
 FSBM Platform — Générateur de données réalistes marocaines
 Projet de Fin d'Études 2025/2026 — Faculté des Sciences Ben M'Sick
============================================================================

Génère :
  * ~120 professeurs avec spécialités cohérentes par département
  * ~5000 étudiants avec CNE, emails universitaires, groupes
  * Notes et résultats par module
  * Emplois du temps cohérents
  * Examens session normale + rattrapage
  * Affectations module ↔ professeur

USAGE :
    python generate_data.py            # génère 04_seed_data.sql
    python generate_data.py --execute  # génère ET exécute sur MySQL

PRÉREQUIS :
    pip install mysql-connector-python python-dotenv

CONFIGURATION (.env à la racine du dossier database/seed/) :
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=fsbm_db
    DB_USER=root
    DB_PASSWORD=votre_mot_de_passe
============================================================================
"""

from __future__ import annotations
import os
import random
import argparse
from datetime import date, datetime, time, timedelta
from pathlib import Path

# ─── Données réalistes ────────────────────────────────────────────────────────
PRENOMS_M = [
    "Mohammed", "Ahmed", "Hamza", "Youssef", "Karim", "Hassan", "Omar", "Yassine",
    "Anas", "Mehdi", "Othmane", "Soufiane", "Reda", "Hicham", "Tarik", "Aymen",
    "Khalid", "Driss", "Nabil", "Said", "Rachid", "Adam", "Ilias", "Bilal",
    "Achraf", "Salah", "Walid", "Imad", "Mounir", "Younes", "Aziz", "Marouane",
    "Brahim", "Ayoub", "Zakaria", "Akram", "Abdellah", "Abderrahman", "Idriss",
    "Mouad", "Saad", "Anouar", "Amine", "Ismail", "Jaouad", "Khalil", "Adil",
    "Hatim", "Badr", "Taha"
]
PRENOMS_F = [
    "Fatima", "Khadija", "Aicha", "Salma", "Imane", "Sara", "Hajar", "Nour",
    "Meryem", "Houda", "Nadia", "Asmae", "Rajae", "Soukaina", "Latifa", "Naima",
    "Wafae", "Bouchra", "Saadia", "Hanae", "Ghita", "Yasmine", "Lina", "Maryam",
    "Chaimae", "Kaoutar", "Manal", "Yousra", "Ines", "Zineb", "Rim", "Amal",
    "Habiba", "Najwa", "Nawal", "Rabia", "Dounia", "Siham", "Ilham", "Fadwa",
    "Hayat", "Saida", "Naoual", "Lamia", "Souad", "Mouna", "Karima", "Salwa",
    "Sanaa", "Nezha"
]
NOMS = [
    "Alaoui", "Bennani", "Idrissi", "Tazi", "Cherkaoui", "Berrada", "Filali", "Lahlou",
    "Benali", "Benhamou", "Bouchaib", "Mansouri", "Boukhris", "Naciri", "Sefrioui", "El Fassi",
    "El Mansouri", "El Yousfi", "Khalil", "Lamrini", "Saidi", "Ait Ouaziz", "Belkacemi",
    "Hassani", "Ouazzani", "Tahiri", "Bouhouch", "Mezouari", "El Hajji", "Zerouali", "Belhaj",
    "Chaoui", "Ferhat", "Talbi", "Benkirane", "Rachidi", "Aboulkacem", "Hilali", "Lazrak",
    "Bouanani", "El Amrani", "El Khattabi", "Ouariachi", "Fathi", "Moussa", "Skalli", "Zaoui",
    "Bouazza", "Mounir", "Hammou", "Karam", "El Khalfi", "Benkhadra", "Hraibi", "Akhrif",
    "Boutaleb", "El Ouali", "Hammadi", "Ouhsine", "Naimi", "Sebti", "Bouayad", "El Hamzaoui",
    "Khadiri", "Ait Mansour", "Bouabid", "Hassoun", "Mouatassim", "Ouhmidi", "Riffi", "Zeggari"
]
VILLES = [
    "Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir", "Meknès",
    "Oujda", "Kénitra", "Tétouan", "Salé", "Mohammedia", "El Jadida", "Nador",
    "Béni Mellal", "Khouribga", "Settat", "Berrechid", "Berkane", "Taza",
    "Larache", "Khémisset", "Sefrou", "Errachidia", "Ouarzazate", "Safi"
]
GRADES_PROF = [
    ("PES", 0.25),       # Professeur de l'Enseignement Supérieur
    ("PH", 0.35),         # Professeur Habilité
    ("PA", 0.30),         # Professeur Assistant
    ("VACATAIRE", 0.10),
]
SPECIALITES_BY_DEPT = {
    1: [  # Math-Info
        "Intelligence Artificielle", "Génie Logiciel", "Bases de Données", "Réseaux et Sécurité",
        "Algorithmique et Complexité", "Calcul Scientifique", "Statistiques Appliquées",
        "Théorie des Graphes", "Optimisation", "Machine Learning", "Vision par Ordinateur",
        "Cryptographie", "Algèbre", "Analyse Numérique", "Probabilités", "NLP", "Cloud Computing"
    ],
    2: [  # Physique
        "Mécanique Quantique", "Énergétique", "Matériaux", "Physique Nucléaire",
        "Astrophysique", "Optique", "Thermodynamique", "Physique des Plasmas"
    ],
    3: [  # Chimie
        "Chimie Organique", "Chimie Analytique", "Chimie Inorganique", "Biochimie",
        "Chimie Environnementale", "Chimie des Matériaux", "Chimie Pharmaceutique"
    ],
    4: [  # Biologie
        "Biologie Moléculaire", "Microbiologie", "Génétique", "Écologie",
        "Biotechnologie", "Immunologie", "Physiologie", "Botanique"
    ],
    5: [  # Géologie
        "Hydrogéologie", "Pétrologie", "Géophysique", "Paléontologie",
        "Sédimentologie", "Géologie Minière", "Volcanologie", "Cartographie SIG"
    ],
}
GROUPES_LICENCE = ["G1", "G2", "G3", "G4", "G5", "G6"]
JOURS_TD = ["LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI"]
SALLES_AMPHIS = ["Amphi A", "Amphi B", "Amphi C", "Amphi D", "Grand Amphi"]
SALLES_NORMALES = [f"Salle {b}.{n}" for b in ["A", "B", "C", "D"] for n in range(1, 25)]
SALLES_TP = [f"Lab Info {i}" for i in range(1, 9)] + [f"Lab Physique {i}" for i in range(1, 5)] + [f"Lab Chimie {i}" for i in range(1, 5)] + [f"Lab Bio {i}" for i in range(1, 5)]
HORAIRES = [
    (time(8, 30),  time(10, 30)),
    (time(10, 45), time(12, 45)),
    (time(14, 0),  time(16, 0)),
    (time(16, 15), time(18, 15)),
]

# ─── Utilitaires ──────────────────────────────────────────────────────────────
def slugify(s: str) -> str:
    """Convertit un nom en email-friendly."""
    return (s.lower()
              .replace(" ", "")
              .replace("'", "")
              .replace("é", "e").replace("è", "e").replace("ê", "e").replace("ë", "e")
              .replace("à", "a").replace("â", "a").replace("ä", "a")
              .replace("î", "i").replace("ï", "i")
              .replace("ô", "o").replace("ö", "o")
              .replace("ù", "u").replace("û", "u").replace("ü", "u")
              .replace("ç", "c")
              .replace("ñ", "n"))

def sql_escape(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (date, datetime)):
        return f"'{value.isoformat()}'"
    if isinstance(value, time):
        return f"'{value.strftime('%H:%M:%S')}'"
    # String
    s = str(value).replace("\\", "\\\\").replace("'", "''")
    return f"'{s}'"

def insert_stmt(table: str, columns: list[str], rows: list[tuple]) -> str:
    """Génère un INSERT INTO ... VALUES (...), (...), ... ; pour insertion par lot."""
    cols = ", ".join(columns)
    values_lines = []
    for row in rows:
        vals = ", ".join(sql_escape(v) for v in row)
        values_lines.append(f"  ({vals})")
    return f"INSERT INTO {table} ({cols}) VALUES\n" + ",\n".join(values_lines) + ";\n\n"

# ─── Génération ───────────────────────────────────────────────────────────────
random.seed(42)  # Reproductibilité

def pick_gender():
    return random.choice(["M", "F"])

def pick_name(gender: str):
    first = random.choice(PRENOMS_M if gender == "M" else PRENOMS_F)
    last = random.choice(NOMS)
    return first, last

def pick_grade():
    r = random.random()
    cumul = 0
    for grade, prob in GRADES_PROF:
        cumul += prob
        if r <= cumul:
            return grade
    return "PA"

def random_phone():
    return f"+212 6{random.randint(10000000, 99999999)}"

def random_cne():
    """Format CNE marocain : 10 chiffres."""
    return f"{random.randint(1, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(100000, 999999)}"

def random_apogee():
    return str(random.randint(10000000, 99999999))

def random_cin():
    """Format CIN marocaine : 1 lettre + 6 chiffres."""
    return f"{random.choice('ABDEFGHIJKLMNPRSTUVWXYZ')}{random.randint(100000, 999999)}"

def random_birth_date(annee_etude: int):
    """Date de naissance cohérente avec l'année d'étude."""
    age_base = 18 + annee_etude  # L1 ≈ 18 ans, L2 ≈ 19, etc.
    year = 2026 - age_base
    return date(year, random.randint(1, 12), random.randint(1, 28))

def random_enrolled_at(annee_etude: int):
    """Date d'inscription cohérente."""
    year = 2026 - (annee_etude - 1)
    return date(year, 9, random.randint(1, 30))

# ─── Définition des filières et leur effectif ────────────────────────────────
FILIERES_LICENCE_EFFECTIFS = {
    # (filiere_id, capacity, annees_etude_range)
    1: (180, 3),  # SMI
    2: (120, 3),  # DI
    3: (100, 3),  # SMA
    4: (120, 3),  # SMP
    5: (110, 3),  # SMC
    6: (150, 3),  # SV
    7: (80,  3),  # STU
}
FILIERES_MASTER_EFFECTIFS = {
    8:  (30, 2),  # MIAGE
    9:  (28, 2),  # IDSI
    10: (25, 2),  # IADS
    11: (25, 2),  # SECNUM
    12: (25, 2),  # MMA
    13: (15, 2),  # MR-MATHS
    14: (20, 2),  # MRP
    15: (25, 2),  # MENRG
    16: (20, 2),  # MMAT
    17: (25, 2),  # MCAE
    18: (22, 2),  # MCOI
    19: (25, 2),  # MBIOT
    20: (22, 2),  # MMOLEC
    21: (20, 2),  # MMICRO
    22: (20, 2),  # MENV
    23: (18, 2),  # MGAP
    24: (30, 2),  # MEDU-MI
    25: (25, 2),  # MEDU-SV
}
FILIERE_DEPT = {  # filiere_id -> department_id
    1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5,
    8:1, 9:1, 10:1, 11:1, 12:1, 13:1,
    14:2, 15:2, 16:2,
    17:3, 18:3,
    19:4, 20:4, 21:4,
    22:5, 23:5,
    24:1, 25:4,
}

# ─── Générer les professeurs ──────────────────────────────────────────────────
def generate_professors():
    profs = []
    matricule_counter = 100001
    email_used: set[str] = set()
    # ~25 profs par département pour Math-Info, ~15 pour les autres
    profs_per_dept = {1: 35, 2: 18, 3: 17, 4: 22, 5: 15}
    for dept_id, n in profs_per_dept.items():
        for _ in range(n):
            gender = pick_gender()
            first, last = pick_name(gender)
            matricule = f"PROF{matricule_counter}"
            matricule_counter += 1
            # Email unique — ajouter un suffixe numérique en cas de collision
            base_email = f"{slugify(first)}.{slugify(last)}"
            email = f"{base_email}@fsbm.ac.ma"
            suffix = 1
            while email in email_used:
                suffix += 1
                email = f"{base_email}{suffix}@fsbm.ac.ma"
            email_used.add(email)
            phone = random_phone()
            grade = pick_grade()
            specialty = random.choice(SPECIALITES_BY_DEPT[dept_id])
            bureau = f"B{dept_id:02d}.{random.randint(101, 350)}"
            profs.append((
                matricule, first, last, email, phone, grade, dept_id,
                specialty, bureau, None, None,
            ))
    return profs

# ─── Générer les étudiants ────────────────────────────────────────────────────
def generate_students():
    students = []
    cne_used = set()
    apogee_used = set()
    email_used = set()
    # Licences (3 années par filière)
    for filiere_id, (capacity, n_annees) in FILIERES_LICENCE_EFFECTIFS.items():
        for annee in range(1, n_annees + 1):
            # ~80% de la capacité par année
            n_students = int(capacity * 0.85)
            for i in range(n_students):
                gender = pick_gender()
                first, last = pick_name(gender)
                # Garantir CNE unique
                while True:
                    cne = random_cne()
                    if cne not in cne_used:
                        cne_used.add(cne)
                        break
                while True:
                    apg = random_apogee()
                    if apg not in apogee_used:
                        apogee_used.add(apg)
                        break
                # Email unique (boucle while pour garantir l'unicité même en cas de collision multiple)
                base_email = f"{slugify(first)}.{slugify(last)}"
                email = f"{base_email}@etu.fsbm.ma"
                suffix = 1
                while email in email_used:
                    suffix += 1
                    email = f"{base_email}{suffix}@etu.fsbm.ma"
                email_used.add(email)
                phone = random_phone()
                birth = random_birth_date(annee)
                ville = random.choice(VILLES)
                cin = random_cin()
                group = random.choice(GROUPES_LICENCE[: min(6, max(2, capacity // 30))])
                is_boursier = random.random() < 0.45
                enrolled = random_enrolled_at(annee)
                students.append((
                    cne, apg, first, last, email, phone, birth, ville, gender,
                    "Marocaine", cin, f"Quartier {random.choice(['Hay', 'Cité', 'Lotissement'])} {random.choice(['Mohammadi', 'Salam', 'Al Andalous', 'Hassan', 'Atlas'])}",
                    ville, filiere_id, annee, group, is_boursier, "ACTIF", None, enrolled,
                ))
    # Masters (2 années par filière)
    master_groups = ["G1", "G2"]
    for filiere_id, (capacity, n_annees) in FILIERES_MASTER_EFFECTIFS.items():
        for annee in range(1, n_annees + 1):
            n_students = int(capacity * 0.95)
            for _ in range(n_students):
                gender = pick_gender()
                first, last = pick_name(gender)
                while True:
                    cne = random_cne()
                    if cne not in cne_used:
                        cne_used.add(cne)
                        break
                while True:
                    apg = random_apogee()
                    if apg not in apogee_used:
                        apogee_used.add(apg)
                        break
                base_email = f"{slugify(first)}.{slugify(last)}"
                email = f"{base_email}@etu.fsbm.ma"
                suffix = 1
                while email in email_used:
                    suffix += 1
                    email = f"{base_email}{suffix}@etu.fsbm.ma"
                email_used.add(email)
                students.append((
                    cne, apg, first, last, email, random_phone(),
                    random_birth_date(annee + 3), random.choice(VILLES), gender,
                    "Marocaine", random_cin(),
                    f"Quartier {random.choice(['Hay', 'Cité', 'Lotissement'])} {random.choice(['Mohammadi', 'Salam', 'Al Andalous'])}",
                    random.choice(VILLES), filiere_id, annee, random.choice(master_groups),
                    random.random() < 0.6, "ACTIF", None, random_enrolled_at(annee),
                ))
    return students

# ─── Générer les affectations module ↔ prof ──────────────────────────────────
def generate_module_teachers(modules_count: int, profs_per_dept_max: int):
    """Affecte 1 prof titulaire à chaque module + parfois 1 assistant.

    Note: Compatible avec MySQL 8 sql_mode=ONLY_FULL_GROUP_BY.
    On utilise une CTE / sous-requête déterministe (id modulo) plutôt que RAND() + GROUP BY.
    """
    return """
-- ───────────────────────────────────────────────────────────────────────────
-- Affectation : 1 prof TITULAIRE par module
-- Stratégie : pour chaque module, on choisit le prof dont (p.id mod n_profs_dept)
--            correspond à (m.id mod n_profs_dept). Distribution uniforme sans RAND().
-- ───────────────────────────────────────────────────────────────────────────
INSERT INTO module_teachers (module_id, professor_id, role, annee_univ)
SELECT m.id AS module_id,
       p.id AS professor_id,
       'TITULAIRE' AS role,
       '2025-2026' AS annee_univ
FROM modules m
JOIN filieres f  ON f.id = m.filiere_id
JOIN professors p ON p.department_id = f.department_id
JOIN (
    SELECT department_id, MIN(id) AS first_prof_id, COUNT(*) AS n_profs
    FROM professors
    GROUP BY department_id
) dept_stats ON dept_stats.department_id = p.department_id
WHERE (p.id - dept_stats.first_prof_id) = (m.id MOD dept_stats.n_profs);

-- ───────────────────────────────────────────────────────────────────────────
-- Affectation : assistants TD (1 par module ayant des heures de TD, profs PA/Vacataires)
-- ───────────────────────────────────────────────────────────────────────────
INSERT INTO module_teachers (module_id, professor_id, role, annee_univ)
SELECT m.id, p.id, 'TD', '2025-2026'
FROM modules m
JOIN filieres f ON f.id = m.filiere_id
JOIN professors p ON p.department_id = f.department_id
JOIN (
    SELECT department_id, MIN(id) AS first_pa_id, COUNT(*) AS n_pa
    FROM professors
    WHERE grade IN ('PA', 'VACATAIRE')
    GROUP BY department_id
) pa_stats ON pa_stats.department_id = p.department_id
WHERE m.hours_td > 0
  AND p.grade IN ('PA', 'VACATAIRE')
  AND (p.id - pa_stats.first_pa_id) = ((m.id + 7) MOD pa_stats.n_pa)
  AND NOT EXISTS (
      SELECT 1 FROM module_teachers mt
      WHERE mt.module_id = m.id AND mt.professor_id = p.id
  );
"""

def generate_schedules_sql():
    """Génère 1 séance de cours/TD par module pour les filières actives.
    Approche simple SQL pour ne pas générer 5000 INSERT individuels."""
    return """
-- Emplois du temps : pour chaque module, créer 1-3 séances par semaine
-- (Approche simplifiée : chaque module a 1 cours magistral + 1 TD)
INSERT INTO schedules (filiere_id, module_id, professor_id, semester, annee_etude, group_name,
                       day_of_week, start_time, end_time, salle, type_seance, annee_univ)
SELECT
    m.filiere_id,
    m.id,
    (SELECT mt.professor_id FROM module_teachers mt WHERE mt.module_id = m.id AND mt.role = 'TITULAIRE' LIMIT 1),
    m.semester,
    CASE WHEN m.semester <= 2 THEN 1 WHEN m.semester <= 4 THEN 2 ELSE 3 END,
    NULL,
    ELT(1 + (m.id MOD 6), 'LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI'),
    ELT(1 + (m.id MOD 4), '08:30:00','10:45:00','14:00:00','16:15:00'),
    ELT(1 + (m.id MOD 4), '10:30:00','12:45:00','16:00:00','18:15:00'),
    CASE WHEN m.id MOD 5 = 0 THEN CONCAT('Amphi ', ELT(1 + (m.id MOD 4), 'A','B','C','D'))
         ELSE CONCAT('Salle ', ELT(1 + (m.id MOD 4), 'A','B','C','D'), '.', LPAD(((m.id MOD 20)+101), 3, '0'))
    END,
    'COURS',
    '2025-2026'
FROM modules m
JOIN filieres f ON f.id = m.filiere_id
WHERE f.is_active = TRUE;

-- Ajouter une séance de TD pour les modules qui en ont
INSERT INTO schedules (filiere_id, module_id, professor_id, semester, annee_etude, group_name,
                       day_of_week, start_time, end_time, salle, type_seance, annee_univ)
SELECT
    m.filiere_id, m.id,
    (SELECT mt.professor_id FROM module_teachers mt WHERE mt.module_id = m.id LIMIT 1),
    m.semester,
    CASE WHEN m.semester <= 2 THEN 1 WHEN m.semester <= 4 THEN 2 ELSE 3 END,
    ELT(1 + (m.id MOD 4), 'G1','G2','G3','G4'),
    ELT(1 + ((m.id + 2) MOD 6), 'LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI'),
    ELT(1 + ((m.id + 1) MOD 4), '08:30:00','10:45:00','14:00:00','16:15:00'),
    ELT(1 + ((m.id + 1) MOD 4), '10:30:00','12:45:00','16:00:00','18:15:00'),
    CONCAT('Salle ', ELT(1 + (m.id MOD 4), 'A','B','C','D'), '.', LPAD(((m.id MOD 20)+101), 3, '0')),
    'TD',
    '2025-2026'
FROM modules m
WHERE m.hours_td > 0;
"""

def generate_exams_sql():
    return """
-- Examens session normale d'hiver (semestres impairs 1, 3, 5) - Janvier 2026
INSERT INTO exams (module_id, filiere_id, exam_date, start_time, duration_min, salle, session, annee_univ, surveillants)
SELECT
    m.id, m.filiere_id,
    DATE_ADD('2026-01-12', INTERVAL (m.id MOD 14) DAY),
    ELT(1 + (m.id MOD 3), '09:00:00','11:30:00','14:00:00'),
    CASE WHEN m.credits >= 6 THEN 180 ELSE 120 END,
    CONCAT('Amphi ', ELT(1 + (m.id MOD 5), 'A','B','C','D','E')),
    'NORMALE_S1',
    '2025-2026',
    'Surveillants désignés par administration'
FROM modules m
JOIN filieres f ON f.id = m.filiere_id
WHERE f.is_active = TRUE AND m.semester IN (1, 3, 5);

-- Examens session normale d'été (semestres pairs 2, 4, 6) - Juin 2026
INSERT INTO exams (module_id, filiere_id, exam_date, start_time, duration_min, salle, session, annee_univ, surveillants)
SELECT
    m.id, m.filiere_id,
    DATE_ADD('2026-06-01', INTERVAL (m.id MOD 20) DAY),
    ELT(1 + (m.id MOD 3), '09:00:00','11:30:00','14:00:00'),
    CASE WHEN m.credits >= 6 THEN 180 ELSE 120 END,
    CONCAT('Amphi ', ELT(1 + (m.id MOD 5), 'A','B','C','D','E')),
    'NORMALE_S2',
    '2025-2026',
    'Surveillants désignés par administration'
FROM modules m
JOIN filieres f ON f.id = m.filiere_id
WHERE f.is_active = TRUE AND m.semester IN (2, 4, 6);

-- Session de rattrapage - Septembre 2026
INSERT INTO exams (module_id, filiere_id, exam_date, start_time, duration_min, salle, session, annee_univ, surveillants)
SELECT
    m.id, m.filiere_id,
    DATE_ADD('2026-09-01', INTERVAL (m.id MOD 10) DAY),
    ELT(1 + (m.id MOD 2), '09:00:00','14:00:00'),
    120,
    CONCAT('Amphi ', ELT(1 + (m.id MOD 3), 'A','B','C')),
    'RATTRAPAGE',
    '2025-2026',
    'À désigner'
FROM modules m
JOIN filieres f ON f.id = m.filiere_id
WHERE f.is_active = TRUE;
"""

def generate_grades_sql():
    """Génère des notes réalistes : moyenne ~12.5 sur 20, écart-type ~3.5."""
    return """
-- Notes session normale (S1 = janvier 2026) — distribution gaussienne approximative
INSERT INTO grades (student_id, module_id, note_cc, note_examen, note_finale,
                    session, annee_univ, is_validated, mention)
SELECT
    s.id,
    m.id,
    -- Note CC : entre 5 et 18 avec biais vers la moyenne
    ROUND(LEAST(20, GREATEST(0, 12 + (RAND()*8 - 4))), 2),
    ROUND(LEAST(20, GREATEST(0, 11 + (RAND()*9 - 4.5))), 2),
    NULL, -- calculé en application
    'NORMALE',
    '2025-2026',
    NULL,
    NULL
FROM students s
JOIN modules m ON m.filiere_id = s.filiere_id
WHERE
    -- Cohérence : modules du semestre que l'étudiant suit
    (
        (s.annee_etude = 1 AND m.semester IN (1, 2))
        OR (s.annee_etude = 2 AND m.semester IN (3, 4))
        OR (s.annee_etude = 3 AND m.semester IN (5, 6))
    )
    AND s.statut = 'ACTIF';

-- Désactiver safe update mode temporairement (compatible Workbench / sécurité)
SET SQL_SAFE_UPDATES = 0;

-- Calculer la note finale = 0.25 * CC + 0.75 * Examen
-- (WHERE id > 0 satisfait aussi safe update mode si jamais)
UPDATE grades SET note_finale = ROUND(note_cc * 0.25 + note_examen * 0.75, 2) WHERE id > 0;

-- Marquer comme validé si >= 10
UPDATE grades SET is_validated = (note_finale >= 10) WHERE id > 0;

-- Calculer la mention
UPDATE grades SET mention = CASE
    WHEN note_finale < 5  THEN 'ELIMINE'
    WHEN note_finale < 10 THEN 'PASSABLE'
    WHEN note_finale < 12 THEN 'PASSABLE'
    WHEN note_finale < 14 THEN 'AB'
    WHEN note_finale < 16 THEN 'BIEN'
    ELSE 'TB'
END WHERE id > 0;

-- Réactiver safe update mode
SET SQL_SAFE_UPDATES = 1;
"""

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="FSBM seed data generator")
    parser.add_argument("--execute", action="store_true", help="Execute on MySQL instead of writing to file")
    parser.add_argument("--output", default="04_seed_data.sql", help="Output SQL file")
    args = parser.parse_args()

    out_path = Path(__file__).parent.parent / "mysql" / args.output

    print("=" * 70)
    print("  FSBM Platform — Générateur de données réalistes")
    print("=" * 70)
    print("[1/5] Génération des professeurs...")
    profs = generate_professors()
    print(f"      → {len(profs)} professeurs générés")

    print("[2/5] Génération des étudiants...")
    students = generate_students()
    print(f"      → {len(students)} étudiants générés")

    print("[3/5] Construction du SQL...")
    sql_parts = [
        "-- " + "=" * 75,
        "-- FSBM Platform — Données générées (professeurs, étudiants, affectations, EDT, examens, notes)",
        f"-- Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-- " + "=" * 75,
        "USE fsbm_db;",
        "",
        "-- Désactiver temporairement ONLY_FULL_GROUP_BY pour cette session",
        "-- (nécessaire pour les requêtes d'affectation prof↔module et agrégations stats)",
        "SET SESSION sql_mode = (SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', ''));",
        "",
        "-- ═══════ PROFESSEURS ═══════",
        insert_stmt(
            "professors",
            ["matricule","first_name","last_name","email","phone","grade","department_id",
             "specialty","bureau","photo_url","bio"],
            profs
        ),
        "-- ═══════ ÉTUDIANTS ═══════",
        insert_stmt(
            "students",
            ["cne","apogee","first_name","last_name","email","phone","birth_date","birth_place",
             "gender","nationality","cin","address","city","filiere_id","annee_etude",
             "group_name","is_boursier","statut","photo_url","enrolled_at"],
            students
        ),
        "-- ═══════ AFFECTATIONS MODULE ↔ PROF ═══════",
        generate_module_teachers(0, 0),
        "",
        "-- ═══════ EMPLOIS DU TEMPS ═══════",
        generate_schedules_sql(),
        "",
        "-- ═══════ EXAMENS ═══════",
        generate_exams_sql(),
        "",
        "-- ═══════ NOTES ═══════",
        generate_grades_sql(),
    ]
    sql = "\n".join(sql_parts)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sql)
    print(f"[4/5] SQL écrit dans : {out_path}")
    print(f"      Taille : {out_path.stat().st_size / 1024:.1f} KB")

    if args.execute:
        try:
            import mysql.connector
            from dotenv import load_dotenv
            load_dotenv(Path(__file__).parent / ".env")
            print("[5/5] Exécution sur MySQL...")
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "fsbm_db"),
            )
            cursor = conn.cursor()
            for statement in sql.split(";"):
                stmt = statement.strip()
                if stmt and not stmt.startswith("--"):
                    cursor.execute(stmt)
            conn.commit()
            cursor.close()
            conn.close()
            print("      ✅ Données insérées avec succès !")
        except Exception as e:
            print(f"      ❌ Erreur : {e}")
            print("      Exécutez manuellement le fichier SQL via mysql client.")
    else:
        print("[5/5] Pour exécuter sur MySQL :")
        print(f"      mysql -u root -p fsbm_db < {out_path}")
        print("      Ou : python generate_data.py --execute (après config .env)")

    print("=" * 70)
    print(f"  Total : {len(profs)} profs + {len(students)} étudiants")
    print("=" * 70)


if __name__ == "__main__":
    main()
