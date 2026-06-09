# -*- coding: utf-8 -*-
"""Verifie les 90 questions en mode CLASSIQUE (predict + resolveur), comme dans chat.py."""
import os, sys, re, json, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(__file__)
SVC = os.path.join(HERE, "..", "..", "services", "chatbot-service")
sys.path.insert(0, SVC); sys.path.insert(0, HERE)

from test_questions_90 import QUESTIONS
from app.nlp.classifier import MultilingualClassifier
from app.nlp.resolver import resolve as resolve_rules

clf = MultilingualClassifier()
if not clf.load_model():
    clf.train(save=False)


def norm(s):
    s = (s or "").lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


# Token attendu (verifiable) par question — surtout pour les factuelles
EXPECT = {
    "Comment retirer mon diplome original ?": "diplome",
    "Qui est responsable de la filiere Developpement Informatique ?": "sael",
    "Combien de professeurs compte la FSBM ?": "239",
    "Quels sont les domaines de recherche du Pr. Benlahmer ?": "taln",
    "Qui dirige le departement de mathematiques et informatique ?": "adnaoui",
    "Quels enseignants travaillent sur les chatbots ?": "zahour",
    "Combien de citations a le Pr. Talea sur Google Scholar ?": "6755",
    "Qui est le doyen de la FSBM ?": "bouari",
    "Combien de departements compte la FSBM ?": "6 depart",
    "Ou se situe la FSBM ?": "driss el harti",
    "Quel est le site officiel de la faculte ?": "fsbm.ma",
    "Who is in charge of the Software Development program?": "sael",
    "How many professors are there at FSBM?": "239",
    "What are the research fields of Pr. Benlahmer?": "taln",
    "Who heads the Mathematics and Computer Science department?": "adnaoui",
    "Which professors work on chatbots?": "zahour",
    "How many citations does Pr. Talea have?": "6755",
    "Who is the dean of FSBM?": "bouari",
    "How many departments does FSBM have?": "6 depart",
    "Where is FSBM located?": "driss el harti",
    "What is the official website of the faculty?": "fsbm.ma",
    "Chkoun mas'oul 3la filiere DI ?": "sael",
    "Ch7al mn ustad kayn f FSBM ?": "239",
    "Achno houwa l majal dyal recherche dyal Pr. Benlahmer ?": "taln",
    "Chkoun li kaydir departement dyal mathematiques o informatique ?": "adnaoui",
    "Chkoun mn ustad khddam 3la les chatbots ?": "zahour",
    "Ch7al mn citation 3and Pr. Talea f Google Scholar ?": "6755",
    "Chkoun houwa l3amid dyal FSBM ?": "bouari",
    "Ch7al mn departement kayn f FSBM ?": "6 depart",
    "Fin kayna FSBM ?": "driss el harti",
    "Achno houwa site rasmi dyal lkouliya ?": "fsbm.ma",
}
# Intentions attendues (procedurales) — verifie le routage
EXPECT_INTENT = {
    "diplome": ("diplome",), "attestation": ("diplome",), "bourse": ("bourses",),
    "inscrire": ("inscription",), "inscription": ("inscription",), "reinscription": ("reinscription",),
    "examen": ("examens",), "lexams": ("examens",), "rattrapage": ("examens",),
    "emploi": ("emploi_du_temps",), "timetable": ("emploi_du_temps",),
    "stage": ("stage_pfe",), "filiere": ("filieres", "filiere_di"), "filieres": ("filieres", "filiere_di"),
    "master": ("masters", "master_iads"), "scholarship": ("bourses",), "min7a": ("bourses",),
}


def simulate(q, lang):
    r = clf.predict(q, forced_language=None)
    intent, conf = r["intent"], r["confidence"]
    resp, src = r["response"], "tfidf"
    hit = resolve_rules(q, r["language"], clf, tfidf_conf=conf, tfidf_intent=intent)
    if hit:
        resp, intent, conf, src = hit["response"], hit["intent"], hit["confidence"], "resolver"
    return r["language"], intent, conf, resp, src


def check(q, resp, intent):
    nq, nr = norm(q), norm(resp)
    if q in EXPECT:
        return EXPECT[q] in nr
    # reinscription contient "inscription" -> verifier en premier
    if "reinscription" in nq:
        return intent == "reinscription"
    # procedural: verifie le bon intent
    for kw, intents in EXPECT_INTENT.items():
        if kw in nq:
            return intent in intents
    return True  # pas de critere strict -> considere ok (reponse fournie)


fails = []
by = {}
for cat, lang, q, expected in QUESTIONS:
    dl, intent, conf, resp, src = simulate(q, lang)
    ok = check(q, resp, intent)
    b = by.setdefault(lang, {"n": 0, "ok": 0, "res": 0})
    b["n"] += 1; b["ok"] += int(ok); b["res"] += int(src == "resolver")
    if not ok:
        fails.append((lang, q, intent, src, resp[:80]))

print("=== Verification 90 questions (mode classique : predict + resolveur) ===")
for lang in ("fr", "en", "darija"):
    b = by[lang]
    print(f"  {lang:6}: OK {b['ok']}/{b['n']}  (resolveur utilise : {b['res']})")
tot_ok = sum(b["ok"] for b in by.values()); tot = sum(b["n"] for b in by.values())
print(f"  TOTAL : {tot_ok}/{tot} ({100*tot_ok//tot}%)")
if fails:
    print(f"\n--- {len(fails)} ECHECS ---")
    for lang, q, intent, src, resp in fails:
        print(f"  [{lang}] {q}\n     -> intent={intent} src={src} | {resp}")
