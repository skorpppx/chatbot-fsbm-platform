# -*- coding: utf-8 -*-
"""Complete les reponses IA manquantes (quota 70B epuise) avec llama-3.1-8b-instant (bucket separe)."""
import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(__file__)
SVC = os.path.join(HERE, "..", "..", "services", "chatbot-service")
sys.path.insert(0, SVC); sys.path.insert(0, HERE)
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
# Modele leger 'llama-fast' = llama-3.1-8b-instant (quota journalier separe du 70B)
svc = LLMService(classifier=clf, groq_model="llama-fast")
print("Model:", svc.groq.model, "| available:", svc.groq.available)

path = os.path.join(HERE, "test_results_90.json")
data = json.load(open(path, encoding="utf-8"))
# Tag les rangs deja servis par le 70B
for r in data:
    if r.get("ia_provider") == "groq" and not r.get("ia_model"):
        r["ia_model"] = "llama-3.3-70b-versatile"

todo = [r for r in data if r.get("ia_provider") != "groq"]
print(f"A completer : {len(todo)} reponses IA")
done = 0
for r in todo:
    for attempt in range(3):
        g = svc.generate(r["q"], history=[])
        if g.provider == "groq":
            r["ia_provider"] = "groq"; r["ia_model"] = "llama-3.1-8b-instant"
            r["ia"] = (g.content or "")[:320]; r["ia_ms"] = g.latency_ms; r["ia_ctx"] = len(g.contexts_used)
            done += 1
            print(f"  OK [{r['id']:2}][{r['lang']:6}] {g.latency_ms}ms | {r['q'][:40]}")
            break
        print(f"  .. retry [{r['id']}] ({g.error or 'fallback'})")
        time.sleep(8)
    time.sleep(2.2)

json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
groq = sum(1 for r in data if r["ia_provider"] == "groq")
print(f"\nComplete : +{done}. Total Groq IA : {groq}/90 -> test_results_90.json")
