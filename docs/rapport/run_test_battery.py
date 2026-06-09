# -*- coding: utf-8 -*-
"""Execute les 90 questions sur le VRAI moteur : classifieur TF-IDF + pipeline RAG/Groq."""
import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(__file__)
SVC = os.path.join(HERE, "..", "..", "services", "chatbot-service")
sys.path.insert(0, SVC)
sys.path.insert(0, HERE)

# .env -> os.environ
envp = os.path.join(SVC, ".env")
if os.path.exists(envp):
    for line in open(envp, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from test_questions_90 import QUESTIONS
from app.nlp.classifier import MultilingualClassifier
from app.llm.llm_service import LLMService

RUN_GROQ = "--no-groq" not in sys.argv

clf = MultilingualClassifier()
if not clf.load_model():
    clf.train(save=False)
svc = LLMService(classifier=clf) if RUN_GROQ else None
if svc:
    print("STATUS:", json.dumps(svc.status(), ensure_ascii=False))

results = []
for i, (cat, lang, q, expected) in enumerate(QUESTIONS, 1):
    # 1) Mode FAQ / TF-IDF (instantane, deterministe)
    c = clf.predict(q, forced_language=None)
    row = {
        "id": i, "cat": cat, "lang": lang, "q": q, "expected": expected,
        "intent": c["intent"], "conf": round(float(c["confidence"]), 3),
        "faq": (c["response"] or "")[:160],
        "ia_provider": None, "ia": "", "ia_ms": 0, "ia_ctx": 0,
    }
    # 2) Mode IA (RAG + Groq) avec gestion du quota
    if svc:
        for attempt in range(2):
            t0 = time.time()
            r = svc.generate(q, history=[])
            row["ia_provider"] = r.provider
            row["ia"] = (r.content or "")[:320]
            row["ia_ms"] = int((time.time() - t0) * 1000)
            row["ia_ctx"] = len(r.contexts_used)
            if r.provider != "tfidf" or not svc.groq.available:
                break
            # Groq a probablement ete limite (quota) -> backoff + retry une fois
            print(f"  [{i}] Groq fallback -> retry apres pause...")
            time.sleep(6)
        time.sleep(1.1)  # pacing pour respecter le rate limit
    tag = (row["ia_provider"] or "faq")
    print(f"[{i:2}/90][{lang:6}] {tag:5} conf={row['conf']:.2f} {row['intent']:22} | {q[:42]}")
    results.append(row)

out = os.path.join(HERE, "test_results_90.json")
json.dump(results, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# Stats
groq_ok = sum(1 for r in results if r["ia_provider"] == "groq")
print(f"\n90 questions testees. Groq OK: {groq_ok}/90. -> test_results_90.json")
