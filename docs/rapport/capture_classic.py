# -*- coding: utf-8 -*-
"""Capture les reponses MODE CLASSIQUE (TF-IDF + resolveur) des 90 questions -> JSON."""
import os, sys, json, unicodedata
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


out = []
for i, (cat, lang, q, expected) in enumerate(QUESTIONS, 1):
    r = clf.predict(q, forced_language=None)
    intent, conf, resp, src = r["intent"], r["confidence"], r["response"], "tfidf"
    hit = resolve_rules(q, r["language"], clf, tfidf_conf=conf, tfidf_intent=intent)
    if hit:
        resp, intent, conf, src = hit["response"], hit["intent"], hit["confidence"], "resolver"
    # nettoyage emojis/markdown pour le PDF
    clean = resp.replace("**", "").replace("\n", " ").strip()
    out.append({
        "id": i, "cat": cat, "lang": lang, "q": q, "expected": expected,
        "intent": intent, "conf": round(float(conf), 3), "source": src,
        "resp": clean[:200],
    })

json.dump(out, open(os.path.join(HERE, "test_results_classic.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
res = sum(1 for r in out if r["source"] == "resolver")
print(f"90 questions capturees (mode classique). Resolveur: {res}/90. -> test_results_classic.json")
