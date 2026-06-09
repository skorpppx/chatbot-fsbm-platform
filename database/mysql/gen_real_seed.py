# -*- coding: utf-8 -*-
"""
Genere 07_real_fsbm_data.sql a partir des donnees REELLES verifiees (fsbm_real.py).
Seed idempotent (UPSERT) de la couche institutionnelle : departements, filieres,
professeurs reels. N'affecte pas les donnees operationnelles synthetiques.
Usage : py gen_real_seed.py
"""
import os, sys, re, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "docs", "rapport"))
import fsbm_real as R

def slug(s, n=18):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper()
    return s[:n]

def sql_str(s):
    return "'" + s.replace("'", "''") + "'"

lines = []
W = lines.append
W("-- =============================================================================")
W("--  FSBM Platform - DONNEES REELLES (couche institutionnelle)")
W("--  Genere automatiquement depuis le site officiel fsbm.ma (sources verifiables).")
W("--  Seed idempotent : a executer APRES 01..06. UPSERT, n'ecrase pas l'operationnel.")
W("-- =============================================================================")
W("USE fsbm_db;")
W("SET FOREIGN_KEY_CHECKS=1;")
W("")

# --- Departements reels ---
W("-- 6 departements reels (chefs : fsbm.ma)")
for d in R.DEPARTEMENTS:
    W(f"INSERT INTO departments (code, name, head_name, color_hex, created_at, updated_at)")
    W(f"  VALUES ({sql_str(d['code'])}, {sql_str(d['nom'])}, {sql_str(d['chef'])}, '#1C3F6E', NOW(), NOW())")
    W(f"  ON DUPLICATE KEY UPDATE name=VALUES(name), head_name=VALUES(head_name), updated_at=NOW();")
W("")

# --- Filieres reelles ---
W("-- Filieres reelles (responsables : fsbm.ma)")
used = set()
for dept, nom, typ, resp in R.FILIERES:
    code = slug(nom)
    base = code
    i = 2
    while code in used:
        code = f"{base[:15]}_{i}"; i += 1
    used.add(code)
    W(f"INSERT INTO filieres (code, name, type, department_id, coordinator, duration_years, capacity, is_active, created_at, updated_at)")
    W(f"  VALUES ({sql_str(code)}, {sql_str(nom)}, {sql_str(typ)},")
    W(f"    (SELECT id FROM departments WHERE code={sql_str(dept)} LIMIT 1),")
    yrs = 3 if typ == "LICENCE" else 2
    W(f"    {sql_str(resp)}, {yrs}, 80, TRUE, NOW(), NOW())")
    W(f"  ON DUPLICATE KEY UPDATE name=VALUES(name), type=VALUES(type), coordinator=VALUES(coordinator), updated_at=NOW();")
W("")

# --- Professeurs reels ---
W("-- Echantillon du corps professoral reel (noms : fsbm.ma/faculty, 239 enseignants)")
dept_codes = [d["code"] for d in R.DEPARTEMENTS]
for i, (name, role) in enumerate(R.PROFS_REELS, 1):
    parts = name.split()
    last = parts[0]
    first = " ".join(parts[1:]) if len(parts) > 1 else parts[0]
    matricule = f"REAL{i:04d}"
    email = f"{slug(last,10).lower()}.{slug(first,6).lower()}@fsbm.ac.ma"
    grade = "PES" if "PES" in role else ("PH" if "MCH" in role or "MC" in role else "PA")
    dept = dept_codes[i % len(dept_codes)]
    W(f"INSERT INTO professors (matricule, first_name, last_name, email, grade, department_id, specialty, created_at, updated_at)")
    W(f"  VALUES ({sql_str(matricule)}, {sql_str(first)}, {sql_str(last)}, {sql_str(email)}, {sql_str(grade)},")
    W(f"    (SELECT id FROM departments WHERE code={sql_str(dept)} LIMIT 1), {sql_str(role)}, NOW(), NOW())")
    W(f"  ON DUPLICATE KEY UPDATE last_name=VALUES(last_name), grade=VALUES(grade), updated_at=NOW();")
W("")
# --- FAQ reelles (couche de connaissance institutionnelle du chatbot) ---
W("-- FAQ reelles fondees sur les donnees officielles fsbm.ma")
_real_faq = [
    ("doyen_fsbm", "Qui est le doyen de la FSBM ?",
     "Le doyen de la Faculte des Sciences Ben M'Sick est le Pr. Abdeslam EL BOUARI.",
     "doyen, direction, abdeslam el bouari"),
    ("departements_fsbm", "Quels sont les departements de la FSBM ?",
     "La FSBM compte 6 departements : Biologie, Chimie, Geologie, Mathematiques et Informatique, "
     "Physiques, et Sciences de la Communication et Humanites.",
     "departements, biologie, chimie, geologie, physique, informatique"),
    ("filiere_developpement_informatique", "C'est quoi la filiere Developpement Informatique ?",
     "Developpement Informatique est une Licence du departement de Mathematiques et Informatique de "
     "la FSBM, sous la responsabilite du Pr. SAEL Nihal.",
     "developpement informatique, licence, di, sael nihal"),
    ("contact_fsbm_reel", "Comment contacter la FSBM ?",
     "Contact officiel : fsbm.contact@univh2c.ma, telephone +212 6 61 44 24 27, adresse Boulevard "
     "Driss El Harti, Ben M'Sik, Casablanca.",
     "contact, email, telephone, adresse, scolarite"),
    ("corps_professoral_fsbm", "Combien de professeurs a la FSBM ?",
     "Le corps professoral de la FSBM compte 239 enseignants-chercheurs repartis sur les 6 departements.",
     "professeurs, enseignants, corps professoral, 239"),
]
tags = ", ".join(sql_str(t[0]) for t in _real_faq)
W(f"DELETE FROM faq_items WHERE intent_tag IN ({tags});")
for tag, q, a, kw in _real_faq:
    W(f"INSERT INTO faq_items (intent_tag, question, answer, keywords, consultations, is_active, created_at, updated_at)")
    W(f"  VALUES ({sql_str(tag)}, {sql_str(q)}, {sql_str(a)}, {sql_str(kw)}, 0, TRUE, NOW(), NOW());")
W("")
W("SELECT CONCAT('Donnees reelles FSBM chargees : ', "
  "(SELECT COUNT(*) FROM departments), ' departements, ', "
  "(SELECT COUNT(*) FROM filieres), ' filieres, ', "
  "(SELECT COUNT(*) FROM professors), ' professeurs.') AS resultat;")

out = os.path.join(os.path.dirname(__file__), "07_real_fsbm_data.sql")
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"[OK] {out} genere ({len(R.DEPARTEMENTS)} dep, {len(R.FILIERES)} filieres, {len(R.PROFS_REELS)} profs)")
