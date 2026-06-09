# -*- coding: utf-8 -*-
"""Interroge le VRAI classifieur TF-IDF du chatbot pour fonder la demo sur le reel."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "services", "chatbot-service"))
from app.nlp.classifier import MultilingualClassifier

clf = MultilingualClassifier()
if not clf.load_model():
    clf.train(save=False)

QUESTIONS = [
    ("fr", "Ou se trouve le service de scolarite ?"),
    ("fr", "Comment obtenir une attestation ?"),
    ("fr", "Quelles sont les filieres disponibles ?"),
    ("fr", "Quels sont les modules du semestre ?"),
    ("fr", "Qui est responsable du departement informatique ?"),
    ("fr", "Ou trouver les emplois du temps ?"),
    ("fr", "Quand commencent les examens ?"),
    ("fr", "Comment s'inscrire a la FSBM ?"),
    ("fr", "Comment avoir une bourse ?"),
    ("fr", "Presente la FSBM"),
    ("fr", "Quelle filiere choisir ?"),
    ("fr", "Comment retirer mon diplome ?"),
    ("fr", "Je suis stresse pour les examens"),
    ("en", "What are the available programs?"),
    ("en", "How do I register at FSBM?"),
    ("en", "When do the exams start?"),
    ("en", "Where can I find the timetable?"),
    ("darija", "salam, ki dayer ?"),
    ("darija", "shno hia les filieres ?"),
    ("darija", "kifash ndir l'inscription ?"),
    ("darija", "fin kayn emploi du temps ?"),
    ("darija", "ana 3ndi stress f les examens"),
    ("darija", "chno houwa contact dyal scolarite ?"),
]

out = []
for forced, q in QUESTIONS:
    r = clf.predict(q, forced_language=None)
    out.append({
        "q": q, "lang": r["language"], "intent": r["intent"],
        "conf": r["confidence"], "resp": r["response"][:180],
    })
    print(f"[{r['language']:6}] conf={r['confidence']:.2f} intent={r['intent']:24} | {q}")
    print(f"         -> {r['response'][:150]}")

json.dump(out, open(os.path.join(os.path.dirname(__file__), "probe_results.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"\n{len(out)} questions testees. Resultats -> probe_results.json")
