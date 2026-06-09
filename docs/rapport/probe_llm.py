# -*- coding: utf-8 -*-
"""Teste le pipeline COMPLET (RAG + LLaMA via Groq) apres branchement de la base de connaissances."""
import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8")
SVC = os.path.join(os.path.dirname(__file__), "..", "..", "services", "chatbot-service")
sys.path.insert(0, SVC)

# Charger .env (GROQ_API_KEY)
envp = os.path.join(SVC, ".env")
if os.path.exists(envp):
    for line in open(envp, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.nlp.classifier import MultilingualClassifier
from app.llm.llm_service import LLMService

clf = MultilingualClassifier()
if not clf.load_model():
    clf.train(save=False)
svc = LLMService(classifier=clf)
print("STATUS:", json.dumps(svc.status(), ensure_ascii=False))

TESTS = sys.argv[1:] or [
    "Qui est le doyen de la FSBM ?",
    "Domaines de recherche du Pr. Benlahmer ?",
    "Combien de professeurs a la FSBM ?",
    "Qui dirige le departement informatique ?",
]
for q in TESTS:
    t0 = time.time()
    r = svc.generate(q, history=[])
    print("\n" + "=" * 70)
    print("Q:", q)
    print(f"   provider={r.provider} lang={r.language} ctx={len(r.contexts_used)} {int((time.time()-t0)*1000)}ms")
    print("   R:", (r.content or "")[:400].replace("\n", " "))
