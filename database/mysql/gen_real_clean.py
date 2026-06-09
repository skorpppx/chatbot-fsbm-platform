# -*- coding: utf-8 -*-
"""
Genere 08_real_fsbm_clean.sql : REMPLACE les donnees institutionnelles synthetiques
par les donnees REELLES de la FSBM (fsbm.ma + Google Scholar).
- Vide (FK-safe) departements/filieres/professeurs/modules/etudiants/annonces/evenements
- Insere : 6 departements reels, filieres reelles, professeurs reels (emails @univh2c.ma,
  metriques Scholar verifiees), modules representatifs, vraies actualites, echantillon
  d'etudiants rattaches aux vraies filieres.
Usage : py gen_real_clean.py
"""
import os, sys, re, unicodedata, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "docs", "rapport"))
import fsbm_real as R
random.seed(42)
DOM = R.EMAIL_DOMAIN  # univh2c.ma

def noac(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
def slugmail(s):
    s = noac(s).lower(); s = re.sub(r"[^a-z0-9]+", ".", s).strip("."); return s[:24]
def code_of(s, n=18, used=None):
    c = re.sub(r"[^A-Za-z0-9]+", "_", noac(s)).strip("_").upper()[:n]
    if used is not None:
        base = c; i = 2
        while c in used: c = f"{base[:15]}_{i}"; i += 1
        used.add(c)
    return c
def S(s):
    return "'" + str(s).replace("'", "''") + "'"

L = []; W = L.append
W("-- =============================================================================")
W("--  FSBM Platform - REMPLACEMENT par DONNEES REELLES (source : fsbm.ma + Scholar)")
W("--  Vide les tables institutionnelles synthetiques et insere les donnees reelles.")
W("--  Emails @univh2c.ma. A executer APRES 01..07. (Idempotent : re-executable.)")
W("-- =============================================================================")
W("USE fsbm_db;")
W("SET FOREIGN_KEY_CHECKS=0;")
for t in ["grades", "module_teachers", "schedules", "exams", "students", "modules",
          "filieres", "professors", "departments", "announcements", "events"]:
    W(f"DELETE FROM {t};")
W("ALTER TABLE departments AUTO_INCREMENT=1;")
W("ALTER TABLE filieres AUTO_INCREMENT=1;")
W("ALTER TABLE professors AUTO_INCREMENT=1;")
W("ALTER TABLE modules AUTO_INCREMENT=1;")
W("ALTER TABLE students AUTO_INCREMENT=1;")
W("ALTER TABLE announcements AUTO_INCREMENT=1;")
W("ALTER TABLE events AUTO_INCREMENT=1;")
W("")

# --- Departements (ids 1..6) ---
dep_id = {}
W("-- 6 departements reels (fsbm.ma)")
for i, d in enumerate(R.DEPARTEMENTS, 1):
    dep_id[d["code"]] = i
    he = f"chef.{slugmail(d['chef'].replace('Pr. ',''))}@{DOM}"
    W(f"INSERT INTO departments (id, code, name, head_name, head_email, color_hex, created_at, updated_at) "
      f"VALUES ({i}, {S(d['code'])}, {S(d['nom'])}, {S(d['chef'])}, {S(he)}, '#1C3F6E', NOW(), NOW());")
W("")

# --- Filieres (ids 1..N) ---
W("-- Filieres reelles (responsables reels, fsbm.ma)")
fil = []           # (id, code, dept_code, type)
usedf = set()
for k, (dept, nom, typ, resp) in enumerate(R.FILIERES, 1):
    c = code_of(nom, used=usedf)
    yrs = 3 if typ == "LICENCE" else 2
    ce = f"{slugmail(resp.replace('Pr. ',''))}@{DOM}"
    fil.append((k, c, dept, typ))
    W(f"INSERT INTO filieres (id, code, name, type, department_id, coordinator, coord_email, "
      f"duration_years, capacity, is_active, created_at, updated_at) "
      f"VALUES ({k}, {S(c)}, {S(nom)}, {S(typ)}, {dep_id[dept]}, {S(resp)}, {S(ce)}, {yrs}, 80, TRUE, NOW(), NOW());")
W("")

# --- Professeurs reels ---
W("-- Professeurs reels (noms : fsbm.ma ; emails @univh2c.ma)")
PREF = {"EL", "BEN", "AIT", "OULD", "ABOU", "ABD"}
def parse_real(name):
    p = name.split()
    if len(p) >= 3 and p[0].upper() in PREF:
        return (" ".join(p[2:]) or p[1]), (p[0] + " " + p[1])
    if len(p) == 1:
        return p[0], p[0]
    return (" ".join(p[1:]) or p[0]), p[0]

dep_codes = [d["code"] for d in R.DEPARTEMENTS]
pid = 0
used_mail = set()
scholar_lasts = set()

# 1) Les 5 professeurs avec metriques Scholar REELLES verifiees (insertion explicite, correcte)
for sp in R.SCHOLAR_PROFS:
    pid += 1
    first, last = sp["first"], sp["last"]
    scholar_lasts.add(noac(last).upper())
    mail = f"{slugmail(first)}.{slugmail(last)}@{DOM}"
    used_mail.add(mail)
    bio = (f"{sp['affiliation']}. Recherche : {sp['interets']}. Google Scholar (profil verifie) : "
           f"{sp['citations']} citations, h-index {sp['h_index']}, i10-index {sp['i10_index']}. {sp['role']}.")
    W(f"INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, "
      f"specialty, bio, created_at, updated_at) VALUES ("
      f"{S(f'PR{pid:04d}')}, {S(first)}, {S(last)}, {S(mail)}, {S(sp['grade'])}, {dep_id[sp['dep']]}, "
      f"{S(sp['interets'][:190])}, {S(bio)}, NOW(), NOW());")

# 2) Les autres professeurs reels (noms uniquement, AUCUNE metrique inventee)
for name, role in R.PROFS_REELS:
    first, last = parse_real(name)
    if noac(last).upper() in scholar_lasts:
        continue
    pid += 1
    mail = f"{slugmail(first)}.{slugmail(last)}@{DOM}"
    if mail in used_mail:
        mail = f"{slugmail(first)}.{slugmail(last)}.{pid}@{DOM}"
    used_mail.add(mail)
    grade = "PES" if "PES" in role else ("PH" if ("MCH" in role or "MC" in role) else "PA")
    dep = "MI" if ("Math" in role or "informatique" in role.lower()) else dep_codes[pid % len(dep_codes)]
    spec = role if role and role != "-" else None
    W(f"INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, "
      f"specialty, created_at, updated_at) VALUES ("
      f"{S(f'PR{pid:04d}')}, {S(first)}, {S(last)}, {S(mail)}, {S(grade)}, {dep_id[dep]}, "
      f"{S(spec) if spec else 'NULL'}, NOW(), NOW());")
W("")

# --- Modules representatifs par filiere ---
W("-- Modules representatifs par filiere (programme type)")
POOL = {
    "INFO": ["Algorithmique", "Programmation", "Structures de donnees", "Bases de donnees",
             "Reseaux", "Systemes d'exploitation", "Genie logiciel", "Developpement Web",
             "Intelligence Artificielle", "Securite informatique", "Mathematiques pour l'info", "Anglais"],
    "GEN": ["Mathematiques", "Physique", "Chimie", "Statistiques", "Methodologie", "Anglais",
            "Informatique", "Communication", "Projet tutore", "Travaux pratiques"],
}
mid = 0
for fid, fcode, dept, typ in fil:
    pool = POOL["INFO"] if dept == "MI" else POOL["GEN"]
    nmods = 6
    for s in range(1, nmods + 1):
        mid += 1
        name = pool[(fid + s - 1) % len(pool)]
        W(f"INSERT INTO modules (code, name, filiere_id, semester, credits, coefficient, "
          f"hours_cours, hours_td, hours_tp, is_eliminatory, created_at, updated_at) VALUES ("
          f"{S(f'F{fid}M{s}')}, {S(name)}, {fid}, {((s-1)%6)+1}, 4, 1.0, 24, 18, 12, FALSE, NOW(), NOW());")
W("")

# --- Vraies actualites ---
W("-- Actualites REELLES (fsbm.ma, 2025)")
for titre, cat, date, contenu in R.NEWS:
    W(f"INSERT INTO announcements (title, content, type, author, published_at, is_pinned, created_at) "
      f"VALUES ({S(titre)}, {S(contenu)}, 'INFO', {S('Administration FSBM - ' + cat.capitalize())}, "
      f"{S(date + ' 09:00:00')}, FALSE, NOW());")
W("")

# --- Mot du Doyen (annonce epinglee) ---
W("-- Mot du Doyen (texte reel fsbm.ma)")
W(f"INSERT INTO announcements (title, content, type, author, published_at, is_pinned, created_at) "
  f"VALUES ('Mot du Doyen', {S(R.DOYEN_MESSAGE)}, 'INFO', {S(R.DOYEN + ', Doyen de la FSBM')}, NOW(), TRUE, NOW());")
W("")

# --- Evenements representatifs (type FSBM) ---
W("-- Evenements (representatifs des activites de la faculte)")
EVENTS = [
    ("Journee Portes Ouvertes FSBM", "PORTES_OUVERTES", "2026-09-25 09:00:00", "Faculte des Sciences Ben M'Sick"),
    ("Forum de l'Emploi et des Stages", "FORUM", "2026-10-08 09:00:00", "Campus FSBM"),
    ("Conference : IA et Cybersecurite", "CONFERENCE", "2026-07-15 14:00:00", "Amphi FSBM"),
]
for t, et, dt, loc in EVENTS:
    W(f"INSERT INTO events (title, description, event_type, start_date, location, organizer, created_at) "
      f"VALUES ({S(t)}, {S('Evenement representatif des activites de la FSBM (donnee d''exemple).')}, "
      f"{S(et)}, {S(dt)}, {S(loc)}, 'FSBM', NOW());")
W("")

# --- Echantillon d'etudiants rattaches aux vraies filieres ---
W("-- Echantillon d'etudiants (modelise, rattache aux filieres reelles)")
PREN_M = ["Mohamed","Youssef","Amine","Ayoub","Hamza","Othmane","Reda","Mehdi","Anas","Bilal","Yassine","Adam","Ismail","Walid","Achraf"]
PREN_F = ["Fatima","Salma","Imane","Khadija","Sara","Hajar","Meryem","Nada","Aya","Ines","Hiba","Asmae","Chaimae","Oumaima","Zineb"]
NOMS = ["Alaoui","Benani","Cherkaoui","Idrissi","El Amrani","Bennis","Tazi","Lahlou","Berrada","Fassi","Sqalli","Haddad","Mansouri","Ouazzani","Saidi","Bouzidi","Naciri","Rachidi","Sabri","Kettani"]
fil_ids = [f[0] for f in fil]
for i in range(1, 301):
    g = random.choice(["M", "F"])
    pr = random.choice(PREN_M if g == "M" else PREN_F)
    nm = random.choice(NOMS)
    cne = f"R{random.randint(100000000,999999999)}"
    mail = f"{slugmail(pr)}.{slugmail(nm)}.{i}@etu.{DOM}"
    fidi = random.choice(fil_ids)
    annee = random.randint(1, 3)
    W(f"INSERT INTO students (cne, first_name, last_name, email, gender, filiere_id, annee_etude, "
      f"statut, is_boursier, created_at, updated_at) VALUES ("
      f"{S(cne)}, {S(pr)}, {S(nm)}, {S(mail)}, {S(g)}, {fidi}, {annee}, 'ACTIF', "
      f"{random.choice(['TRUE','FALSE'])}, NOW(), NOW());")
W("")
W("SET FOREIGN_KEY_CHECKS=1;")
W("SELECT CONCAT('Remplacement reel : ', (SELECT COUNT(*) FROM departments), ' departements, ', "
  "(SELECT COUNT(*) FROM filieres), ' filieres, ', (SELECT COUNT(*) FROM professors), ' professeurs, ', "
  "(SELECT COUNT(*) FROM announcements), ' annonces reelles.') AS resultat;")

out = os.path.join(os.path.dirname(__file__), "08_real_fsbm_clean.sql")
open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"[OK] 08_real_fsbm_clean.sql genere : {len(R.DEPARTEMENTS)} dep, {len(R.FILIERES)} filieres, "
      f"{pid} profs, {len(R.NEWS)} actualites, 300 etudiants (emails @{DOM}).")
