# -*- coding: utf-8 -*-
"""Teste de NOMBREUSES formulations (FR/EN/darija) + garde-fous conversationnels."""
import os, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(__file__)
SVC = os.path.join(HERE, "..", "..", "services", "chatbot-service")
sys.path.insert(0, SVC); sys.path.insert(0, HERE)
from app.nlp.classifier import MultilingualClassifier
from app.nlp.resolver import resolve as resolve_rules

clf = MultilingualClassifier()
if not clf.load_model():
    clf.train(save=False)


def norm(s):
    s = (s or "").lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def answer(q):
    r = clf.predict(q, forced_language=None)
    intent, conf, resp, src = r["intent"], r["confidence"], r["response"], "tfidf"
    hit = resolve_rules(q, r["language"], clf, tfidf_conf=conf, tfidf_intent=intent)
    if hit:
        resp, intent, src = hit["response"], hit["intent"], "resolver"
    return intent, resp, src


# (question, token_attendu_dans_reponse)  — token "" => garde-fou (voir GUARDS)
VARIANTS = [
    # ---- DOYEN (formulations variees) ----
    ("Qui est le doyen de la faculté ?", "bouari"),
    ("C'est qui le doyen de la FSBM ?", "bouari"),
    ("Le nom du doyen svp", "bouari"),
    ("Who is the dean?", "bouari"),
    ("Who's the dean of the faculty?", "bouari"),
    ("chkoun l3amid dyal lkouliya ?", "bouari"),
    ("3afak chkoun houwa l3amid ?", "bouari"),
    # ---- NB PROFS ----
    ("Combien de professeurs à la FSBM ?", "239"),
    ("Il y a combien d'enseignants ?", "239"),
    ("How many teachers are there at FSBM?", "239"),
    ("ch7al mn ustad f FSBM ?", "239"),
    ("chhal d les profs kaynin ?", "239"),
    # ---- RESPONSABLE DI ----
    ("Qui est le responsable de la filière DI ?", "sael"),
    ("Qui gère la filière développement informatique ?", "sael"),
    ("Who coordinates the Software Development program?", "sael"),
    ("chkoun mas'oul 3la DI ?", "sael"),
    ("chkoun li kaydir filiere developpement informatique ?", "sael"),
    # ---- RECHERCHE BENLAHMER ----
    ("Quels sont les axes de recherche du Pr Benlahmer ?", "taln"),
    ("Sur quoi travaille le professeur Benlahmer ?", "taln"),
    ("What does Pr Benlahmer research?", "taln"),
    ("3la ach kaykhdem Pr Benlahmer ?", "taln"),
    # ---- CHEF DEPARTEMENT ----
    ("Qui dirige le département de mathématiques et informatique ?", "adnaoui"),
    ("Le chef du département informatique ?", "adnaoui"),
    ("Who heads the math and CS department?", "adnaoui"),
    ("chkoun kaydir departement dyal info ?", "adnaoui"),
    # ---- PROF PAR THEME ----
    ("Quel professeur travaille sur les chatbots ?", "zahour"),
    ("Which researcher works on chatbots?", "zahour"),
    ("chmen ustad khddam 3la chatbots ?", "zahour"),
    # ---- CITATIONS ----
    ("Combien de citations a le Pr Talea ?", "6755"),
    ("How many citations does Talea have?", "6755"),
    # ---- NB DEPARTEMENTS ----
    ("Combien de départements à la FSBM ?", "6 depart"),
    ("How many departments are there?", "6 depart"),
    ("ch7al mn departement f FSBM ?", "6 depart"),
    # ---- ADRESSE ----
    ("Où se trouve la FSBM ?", "driss el harti"),
    ("C'est où la faculté ?", "driss el harti"),
    ("Where is the faculty located?", "driss el harti"),
    ("fin kayna lkouliya ?", "driss el harti"),
    # ---- SITE ----
    ("Quel est le site web de la FSBM ?", "fsbm.ma"),
    ("What's the FSBM website?", "fsbm.ma"),
    ("site dyal lkouliya ?", "fsbm.ma"),
    # ---- PROCEDURAL : DIPLOME ----
    ("Comment récupérer mon diplôme ?", "INTENT:diplome"),
    ("How do I get my diploma?", "INTENT:diplome"),
    ("kifash nakhod diplome dyali ?", "INTENT:diplome"),
    ("3afak kifash n7sel 3la diplome ?", "INTENT:diplome"),
    # ---- PROCEDURAL : BOURSE ----
    ("Comment avoir une bourse ?", "INTENT:bourses"),
    ("How to get a scholarship?", "INTENT:bourses"),
    ("kifash n7sel 3la min7a ?", "INTENT:bourses"),
    ("bghit n3ref 3la lmin7a", "INTENT:bourses"),
    # ---- PROCEDURAL : INSCRIPTION ----
    ("Comment s'inscrire ?", "INTENT:inscription"),
    ("kifash ndir tasjil ?", "INTENT:inscription"),
    # ---- PROCEDURAL : EXAMENS ----
    ("Quand sont les examens ?", "INTENT:examens"),
    ("imta lexams ?", "INTENT:examens"),
]

# Garde-fous : ces messages NE doivent PAS etre detournes vers une fiche factuelle/procedurale
GUARDS = [
    ("salam khoya", ("salutation", "comment_vas_tu", "identite_chatbot")),
    ("bonjour", ("salutation", "comment_vas_tu")),
    ("hello", ("salutation", "comment_vas_tu")),
    ("ki dayer ?", ("comment_vas_tu", "salutation")),
    ("merci beaucoup", ("remerciement",)),
    ("choukran bzaf", ("remerciement",)),
    ("ana 3ndi stress f les examens", ("stress_examens", "examens", "demande_aide_psychologique")),
    ("je suis stressé pour mes examens", ("stress_examens", "demande_aide_psychologique", "examens")),
    ("ana smiti Karim", ("identite_genre", "salutation", "default")),
    ("rani mra", ("identite_genre", "salutation", "default")),
]

ok = 0; fail = []
for q, exp in VARIANTS:
    intent, resp, src = answer(q)
    if exp.startswith("INTENT:"):
        good = intent == exp.split(":", 1)[1]
    else:
        good = exp in norm(resp)
    ok += int(good)
    if not good:
        fail.append((q, intent, src, resp[:70]))

gok = 0; gfail = []
for q, allowed in GUARDS:
    intent, resp, src = answer(q)
    good = intent in allowed
    gok += int(good)
    if not good:
        gfail.append((q, intent, src, resp[:70]))

print(f"=== Variantes de formulation : {ok}/{len(VARIANTS)} OK ===")
for q, i, s, r in fail:
    print(f"  X {q}\n     -> intent={i} src={s} | {r}")
print(f"\n=== Garde-fous conversationnels : {gok}/{len(GUARDS)} OK ===")
for q, i, s, r in gfail:
    print(f"  X {q}\n     -> intent={i} src={s} | {r}")
print(f"\nTOTAL : {ok+gok}/{len(VARIANTS)+len(GUARDS)}")
